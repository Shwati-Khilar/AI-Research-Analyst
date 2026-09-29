# AI Research Analyst 🔎

An AI-powered research system that uses Retrieval-Augmented Generation (RAG), local Large Language Models, prompt engineering, and LLM-based evaluation to generate evidence-grounded research reports.

## 🚀 Overview

AI Research Analyst allows users to enter a research question and automatically:

1. Retrieve relevant information from indexed research documents.
2. Generate an evidence-grounded research report using a local LLM.
3. Structure the report into key findings, research gaps, and sources.
4. Evaluate the generated report for faithfulness, relevance, and completeness.

The system is designed to reduce unsupported responses by grounding generation in retrieved research context.

---

## ✨ Features

### 🔍 Retrieval-Augmented Generation

Research documents are:

- Extracted from PDF files
- Cleaned and chunked
- Converted into vector embeddings
- Stored in Qdrant
- Retrieved using semantic similarity

### 🧠 Local LLM

The project uses:

- Ollama
- Qwen3:4b

The model runs locally instead of relying on a hosted LLM API.

### 📝 Structured Research Reports

Generated reports contain:

- Executive Summary
- Key Findings
- Research Gaps
- Evidence & Sources

### 📊 LLM-Based Evaluation

Generated reports are evaluated on:

- Faithfulness
- Relevance
- Completeness

An overall quality score is calculated from these three dimensions.

The evaluation is an automated LLM-based assessment and should not be treated as ground truth.

### 🎯 Prompt Engineering

The project experiments with:

- System prompts
- Role prompting
- Structured prompts
- Few-shot prompting
- Temperature
- Prompt templates
- Output validation
- Prompt optimization

---

## 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │      Next.js UI      │
                         │   Research Question  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      FastAPI         │
                         │      Backend         │
                         └──────────┬───────────┘
                                    │
                         ┌──────────▼───────────┐
                         │   Query Embedding    │
                         │   nomic-embed-text   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       Qdrant         │
                         │   Vector Database    │
                         └──────────┬───────────┘
                                    │
                              Top-k Chunks
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      Qwen3:4b        │
                         │    Local LLM         │
                         │       Ollama         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Structured Research  │
                         │       Report         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    LLM Evaluation    │
                         │  Faithfulness        │
                         │  Relevance           │
                         │  Completeness        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      Next.js UI      │
                         │ Report + Evaluation  │
                         └──────────────────────┘