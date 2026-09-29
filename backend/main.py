import json
import ollama

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from qdrant_client import QdrantClient


app = FastAPI(
    title="AI Research Analyst API",
    description="RAG-based research report generation API",
    version="1.0.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Qdrant
# --------------------------------------------------

client = QdrantClient(
    path="data/qdrant"
)

collection_name = "research_documents"


class ResearchRequest(BaseModel):
    topic: str


# --------------------------------------------------
# Root
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "AI Research Analyst API is running"
    }

def evaluate_report(topic, context, report):
    """
    Evaluate the generated report against the retrieved research context.
    """

    evaluation_prompt = f"""
You are a strict research-quality evaluator.

Evaluate the generated research report using ONLY the provided
research context.

Research Question:
{topic}

Research Context:
{context}

Generated Report:
{json.dumps(report, indent=2)}

Evaluate these three dimensions:

1. Faithfulness
Are the claims in the report supported by the research context?

2. Relevance
Does the report directly answer the research question?

3. Completeness
Does the report cover the important points needed to answer
the research question based on the available context?

Give each score between 0.0 and 1.0.

Scoring:
1.0 = excellent
0.8 = strong
0.6 = moderate
0.4 = weak
0.2 = very weak
0.0 = unsupported / missing

Return ONLY this JSON object:

{{
  "faithfulness": {{
    "score": 0.0,
    "reason": ""
  }},
  "relevance": {{
    "score": 0.0,
    "reason": ""
  }},
  "completeness": {{
    "score": 0.0,
    "reason": ""
  }}
}}

/no_think
"""

    try:

        response = ollama.chat(
            model="qwen3:4b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict research quality evaluator. Return only JSON."
                },
                {
                    "role": "user",
                    "content": evaluation_prompt
                }
            ],
            think=False,
            options={
                "temperature": 0.0,
                "num_predict": 1200,
                "repeat_penalty": 1.1
            }
        )

        raw_output = response["message"]["content"]

        print("\nRAW QUALITY OUTPUT:")
        print(raw_output)

        # Remove Qwen reasoning if present
        if "</think>" in raw_output:
            raw_output = raw_output.split("</think>", 1)[1].strip()

        # Find JSON
        start = raw_output.find("{")
        end = raw_output.rfind("}")

        if start == -1 or end == -1:
            print("Quality evaluation returned no JSON.")
            return None

        json_text = raw_output[start:end + 1]

        evaluation = json.loads(json_text)

        # Calculate overall score
        scores = [
            evaluation["faithfulness"]["score"],
            evaluation["relevance"]["score"],
            evaluation["completeness"]["score"]
        ]

        evaluation["overall_score"] = round(
            sum(scores) / len(scores),
            2
        )

        return evaluation

    except Exception as e:

        print("\nQuality evaluation failed:")
        print(e)

        return None

# --------------------------------------------------
# Research
# --------------------------------------------------

@app.post("/research")
def generate_research(request: ResearchRequest):

    topic = request.topic.strip()

    if not topic:
        return {
            "error": "Research topic cannot be empty."
        }

    print(f"\nResearch topic: {topic}")

    # --------------------------------------------------
    # Embed query
    # --------------------------------------------------

    embedding_response = ollama.embed(
        model="nomic-embed-text",
        input=topic
    )

    query_vector = embedding_response["embeddings"][0]

    # --------------------------------------------------
    # Retrieve top 3 chunks
    # --------------------------------------------------

    search_results = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=3
    ).points

    if not search_results:
        return {
            "error": "No relevant research documents found."
        }

    print(f"Retrieved {len(search_results)} research chunks.")

    # --------------------------------------------------
    # Build context
    # --------------------------------------------------

    context_parts = []

    for i, result in enumerate(search_results, start=1):

        context_parts.append(
            f"""
[Source {i} - Page {result.payload["page"]}]

{result.payload["text"]}
"""
        )

    context = "\n".join(context_parts)

    # --------------------------------------------------
    # Prompt
    # --------------------------------------------------

    system_prompt = """
You are an expert research analyst.

Answer the research question using ONLY the provided research context.

Rules:

1. Do not use outside knowledge.
2. Do not invent facts, statistics, or sources.
3. Preserve uncertainty from the research.
4. Do not turn correlations into causal claims.
5. Do not exaggerate findings.
6. The provided research is a preliminary study.
7. Keep the answer concise.

After reasoning, output ONLY this JSON object:

{
  "executive_summary": "short summary",
  "key_findings": [
    "finding 1",
    "finding 2",
    "finding 3"
  ],
  "research_gaps": [
    "gap 1",
    "gap 2"
  ],
  "citations": [
    "Source 1 - Page X",
    "Source 2 - Page X"
  ]
}
"""

    user_prompt = f"""
Research Question:

{topic}

Research Context:

{context}

Return the requested JSON object after analyzing the context.

/no_think
"""


    # --------------------------------------------------
    # Generate report
    # --------------------------------------------------

    print("Generating report with Qwen3...")

    response = ollama.chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        think=False,
        options={
            "temperature": 0.1,
            "num_predict": 2500,
            "repeat_penalty": 1.1
        }
    )

    raw_report = response["message"]["content"]

    print("\nRAW QWEN OUTPUT:")
    print(raw_report)

    # --------------------------------------------------
    # Remove Qwen thinking section
    # --------------------------------------------------

    if "</think>" in raw_report:
        raw_report = raw_report.split("</think>", 1)[1].strip()

    # --------------------------------------------------
    # Extract JSON object
    # --------------------------------------------------

    start = raw_report.find("{")
    end = raw_report.rfind("}")

    if start == -1 or end == -1 or end <= start:

        print("\nNo JSON object found.")

        return {
            "error": "The model did not return a valid research report."
        }

    json_text = raw_report[start:end + 1]

    print("\nEXTRACTED JSON:")
    print(json_text)

    # --------------------------------------------------
    # Parse JSON
    # --------------------------------------------------

    try:

        report = json.loads(json_text)

    except json.JSONDecodeError as e:

        print("\nJSON parsing failed:")
        print(e)

        return {
            "error": "The model returned invalid JSON."
        }

    # --------------------------------------------------
    # Final response
    # --------------------------------------------------

        print("\nReport generated successfully.")

    # --------------------------------------------------
    # Quality Check
    # --------------------------------------------------

    print("Running quality check...")

    quality = evaluate_report(
        topic,
        context,
        report
    )

    if quality:
        print("\nQuality Check:")
        print(json.dumps(quality, indent=2))
    else:
        print("\nQuality check unavailable.")

    return {
        "topic": topic,
        "report": report,
        "quality": quality
    }