# Prompt Engineering Experiments

## Experiment 1 — Role Prompting

### Prompt V1

Explain Generative AI in simple terms.

### Prompt V2

System:

You are an expert research analyst.

Explain technical concepts clearly and accurately.

Avoid unnecessary jargon.

Use examples when helpful.

User:

Explain Generative AI in simple terms.

### Observations

- V1 already produced a clear and beginner-friendly explanation.
- V2 produced a similarly clear response but with more structured
  explanations and examples.
- The system prompt influenced the tone and behavior of the model.
- V2 was not necessarily better simply because it was longer.
- This showed that role instructions can influence the style and
  structure of an LLM response.

### Questions

1. Which response is clearer?
2. Which response is better structured?
3. Which response gives better examples?
4. Is V2 actually better, or is it just longer?
5. Did the system instruction change the behavior?


---

## Experiment 2 — Structured Prompt

### Prompt V3

The prompt contains:

- Role
- Task
- Audience
- Requirements
- Constraints
- Output format

### Questions

1. Did the model follow the requested structure?
2. Did it include all required sections?
3. Did it stay under 500 words?
4. Did it explain the topic at the requested level?
5. Did it avoid unnecessary information?
6. Is the output more predictable than V1 and V2?

### Observations

- The model followed the requested six-section structure.
- All required sections were present.
- The response was 249 words, staying below the 500-word limit.
- The explanation was appropriate for a third-year computer science
  student.
- The output was more predictable because the required structure
  was explicitly specified.
- This demonstrated that explicit output constraints can make LLM
  responses more consistent.

### Conclusion

Adding task requirements, constraints, audience information, and an
explicit output format gives the model less freedom to choose the
structure of the response and makes the output more predictable.


---

## Experiment 3 — Temperature

### Prompt

Explain the impact of Generative AI on software development
in approximately 100 words.

### Temperature Values

- 0.0
- 0.5
- 1.0

### Observations

#### Temperature 0.0

The response focused on:

- Code generation
- Debugging
- Documentation
- Developer productivity
- Security
- Human oversight

#### Temperature 0.5

The response used similar core ideas but changed some wording
and examples, including:

- Testing
- GitHub Copilot
- Security vulnerabilities
- Ethical concerns

#### Temperature 1.0

The response again covered similar ideas but used different
phrasing and examples, including:

- Code snippets
- Entire functions
- Framework learning
- Testing
- Hallucination risks

### Overall Observation

All three responses remained semantically similar because the
prompt strongly constrained the task.

The higher temperature introduced some variation in wording and
examples, but it did not completely change the content or topic.

### Conclusion

Temperature affects generation variability, but it does not
directly determine factual accuracy or response quality.

Prompt instructions and task constraints also strongly influence
the final response.

---

## Experiment 4 — Prompt Templates

### Goal

Create reusable prompts with dynamic variables instead of
hardcoding a research topic into the application.

### Variables

- topic
- audience

### Fixed Instructions

- Research analyst role
- Required report sections
- Accuracy constraints
- Word limit
- Clear language

### Experiment

Same topic:

"Impact of Generative AI on software development"

Audience 1:

"Non-technical business manager"

Audience 2:

"Third-year computer science student"

### Observation — Audience 1

The response was more general and business-oriented.

It discussed:

- Developer productivity
- Business impact
- Risks
- Human-AI collaboration
- Adoption considerations

It used less technical terminology.

### Observation — Audience 2

The response was more technical and detailed.

It discussed concepts such as:

- Large Language Models
- Code generation
- Boilerplate code
- Unit testing
- Security vulnerabilities
- AI-assisted development

It also used more technical terminology appropriate for
a computer science student.

### Comparison

The research topic remained the same, but changing the audience
changed the way the model explained the topic.

This demonstrates that prompt variables can influence the
presentation and depth of an LLM response without changing the
underlying research topic.

### Conclusion

Prompt templates allow an application to reuse the same prompt
structure while dynamically changing input-specific information.

This will allow our final AI Research Analyst to generate reports
for different topics and audiences without modifying the underlying
prompt code.


---

# Key Lessons From Phase 1

### 1. Role Prompting

A system instruction can influence how the model approaches
a task.

### 2. Structured Prompting

Explicitly specifying role, task, context, requirements,
constraints, and output format makes responses more predictable.

### 3. Structured Outputs

LLMs can be instructed to return JSON so that application code
can consume the output programmatically.

### 4. Schema Validation

Pydantic can validate whether the generated output follows the
expected structure.

### 5. Temperature

Temperature controls generation variability but does not directly
determine factual accuracy.

### 6. Prompt Templates

Dynamic prompt variables allow the same prompt structure to be
reused for different inputs.

### Overall Phase 1 Pipeline

Research Input
        ↓
Prompt Template
        ↓
System + User Instructions
        ↓
LLM
        ↓
Structured Output
        ↓
Pydantic Validation
        ↓
Application

---

## Experiment 5 — Few-Shot Prompting

### Goal

Test whether providing examples improves the model's ability
to follow a classification task.

### Zero-Shot

The model receives only the task instruction and the statement.

### Few-Shot

The model receives multiple examples showing:

- Input statement
- Expected classification

before receiving the new statement.

### Task

Classify research statements as:

- FACT
- OPINION
- UNSUPPORTED

### Observation

Compare the zero-shot and few-shot outputs.

Check:

1. Did both approaches produce the same classification?
2. Did the examples make the classification criteria clearer?
3. Did the model follow the requested output format?
4. Would the examples become more useful for a more ambiguous statement?

### Conclusion

Few-shot prompting provides examples of the desired behavior
inside the prompt without changing or retraining the underlying
model.

It can be useful when the desired behavior or output format is
difficult to describe using instructions alone.

However, examples should be selected carefully because poor or
ambiguous examples can negatively influence the model's output.