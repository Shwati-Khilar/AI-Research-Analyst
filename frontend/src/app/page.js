"use client";

import { useState } from "react";

export default function Home() {
  const [topic, setTopic] = useState("");
  const [report, setReport] = useState(null);
  const [quality, setQuality] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("overview");

  const generateReport = async () => {
    if (!topic.trim()) {
      setError("Please enter a research question.");
      return;
    }

    setLoading(true);
    setError("");
    setReport(null);
    setQuality(null);
    setActiveTab("overview");

    try {
      const response = await fetch("http://127.0.0.1:8000/research", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          topic: topic.trim(),
        }),
      });

      const data = await response.json();

      console.log("API RESPONSE:", data);

      if (!response.ok) {
        throw new Error(
          data.error || "Failed to generate research report."
        );
      }

      if (data.error) {
        throw new Error(data.error);
      }

      let reportData = data.report;

      if (typeof reportData === "string") {
        try {
          reportData = JSON.parse(reportData);
        } catch {
          throw new Error("The model returned an invalid research report.");
        }
      }

      if (!reportData || typeof reportData !== "object") {
        throw new Error("The model returned an invalid research report.");
      }

      setReport(reportData);

      if (data.quality) {
        console.log("QUALITY RESULT:", data.quality);
        setQuality(data.quality);
      } else {
        console.warn("No quality evaluation returned by backend.");
        setQuality(null);
      }
    } catch (err) {
      console.error("Research error:", err);

      setError(
        err.message || "Could not generate the research report."
      );

      setReport(null);
      setQuality(null);
    } finally {
      setLoading(false);
    }
  };

  const resetResearch = () => {
    setTopic("");
    setReport(null);
    setQuality(null);
    setError("");
    setActiveTab("overview");
  };

  const tabs = [
    { id: "overview", label: "Overview", icon: "◈" },
    { id: "findings", label: "Findings", icon: "▣" },
    { id: "quality", label: "Quality Check", icon: "◇" },
    { id: "report", label: "Final Report", icon: "□" },
    { id: "sources", label: "Sources", icon: "▥" },
  ];

  const pipeline = [
    {
      number: "01",
      title: "Document Processing",
      description: "Extract & chunk",
    },
    {
      number: "02",
      title: "Embedding",
      description: "Vector indexing",
    },
    {
      number: "03",
      title: "Retrieval",
      description: "Semantic search",
    },
    {
      number: "04",
      title: "RAG Generation",
      description: "Qwen3 synthesis",
    },
    {
      number: "05",
      title: "Evaluation",
      description: "Quality check",
    },
    {
      number: "06",
      title: "Final Report",
      description: "Structured output",
    },
  ];

  const overallPercentage =
    quality && typeof quality.overall_score === "number"
      ? Math.round(quality.overall_score * 100)
      : null;

  return (
    <div className="min-h-screen bg-[#f6f8fc] text-[#101828]">

      {/* =====================================================
          SIDEBAR
      ====================================================== */}

      <aside className="fixed inset-y-0 left-0 z-30 hidden w-[270px] border-r border-[#e5e7eb] bg-[#0a0f19] text-white lg:flex lg:flex-col">

        {/* Logo */}

        <div className="flex h-[74px] items-center gap-3 border-b border-white/10 px-6">

          <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-indigo-400/30 bg-indigo-500/10 text-xl text-indigo-300">
            ✦
          </div>

          <div>
            <h1 className="text-[17px] font-semibold tracking-tight">
              AI Research
            </h1>

            <p className="font-mono text-[9px] uppercase tracking-[0.25em] text-slate-500">
              Analyst Engine
            </p>
          </div>

        </div>


        {/* Navigation */}

        <div className="px-4 pt-7">

          <button
            onClick={resetResearch}
            className="mb-5 flex w-full items-center gap-3 rounded-xl px-4 py-3 text-left text-sm text-slate-300 transition hover:bg-white/5 hover:text-white"
          >
            <span className="text-lg text-slate-400">⊕</span>
            <span>New Research</span>
          </button>


          <p className="mb-2 px-4 font-mono text-[10px] uppercase tracking-[0.25em] text-slate-600">
            Workspace
          </p>


          <div className="space-y-1">

            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex w-full items-center gap-3 rounded-xl px-4 py-3 text-left text-sm transition ${
                  activeTab === tab.id
                    ? "bg-indigo-600 text-white shadow-lg shadow-indigo-900/20"
                    : "text-slate-400 hover:bg-white/5 hover:text-white"
                }`}
              >
                <span className="w-5 text-center text-sm">
                  {tab.icon}
                </span>

                <span>{tab.label}</span>
              </button>
            ))}

          </div>

        </div>


        {/* Session */}

        <div className="mt-8 px-4">

          <p className="mb-3 px-3 font-mono text-[10px] uppercase tracking-[0.25em] text-slate-600">
            Current Session
          </p>

          <div className="rounded-xl border border-white/10 bg-white/[0.03] p-4">

            <div className="mb-3 flex items-center gap-2">

              <span
                className={`h-2 w-2 rounded-full ${
                  report
                    ? "bg-emerald-400"
                    : loading
                    ? "animate-pulse bg-blue-400"
                    : "bg-slate-600"
                }`}
              />

              <span className="text-xs font-medium text-slate-200">
                {loading
                  ? "Research running"
                  : report
                  ? "Research ready"
                  : "No active research"}
              </span>

            </div>

            <p className="line-clamp-3 text-xs leading-5 text-slate-500">
              {topic || "Enter a research question to begin your analysis."}
            </p>

          </div>

        </div>


        {/* Bottom */}

        <div className="mt-auto border-t border-white/10 p-4">

          <div className="flex items-center gap-3 rounded-xl px-3 py-3">

            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-indigo-500/20 text-xs font-semibold text-indigo-300">
              AI
            </div>

            <div>
              <p className="text-xs font-medium text-slate-300">
                Local Research
              </p>

              <p className="font-mono text-[9px] uppercase tracking-wider text-slate-600">
                Qdrant · Ollama
              </p>
            </div>

          </div>

        </div>

      </aside>


      {/* =====================================================
          MAIN
      ====================================================== */}

      <main className="lg:ml-[270px]">

        {/* TOP BAR */}

        <header className="sticky top-0 z-20 flex h-[74px] items-center justify-between border-b border-[#e5e7eb] bg-white/90 px-6 backdrop-blur lg:px-10">

          <div className="min-w-0">

            <p className="font-mono text-[10px] uppercase tracking-[0.25em] text-indigo-500">
              Research Workspace
            </p>

            <p className="mt-1 truncate text-sm font-medium text-slate-600">
              {topic || "New research session"}
            </p>

          </div>


          <div className="flex items-center gap-3">

            <div className="hidden items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-xs text-slate-500 sm:flex">
              <span className="h-2 w-2 rounded-full bg-emerald-400" />
              Local Engine
            </div>

            {report && (
              <button
                onClick={() => setActiveTab("report")}
                className="rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-indigo-500"
              >
                Open Final Report →
              </button>
            )}

          </div>

        </header>


        {/* CONTENT */}

        <div className="mx-auto max-w-[1450px] px-5 py-8 sm:px-8 lg:px-10 lg:py-10">

          {/* =================================================
              START SCREEN
          ================================================== */}

          {!report && !loading && (

            <section className="mx-auto max-w-4xl py-12">

              <div className="mb-10 text-center">

                <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-indigo-200 bg-indigo-50 px-4 py-2 font-mono text-[10px] uppercase tracking-[0.2em] text-indigo-600">
                  <span>✦</span>
                  Evidence-grounded intelligence
                </div>

                <h2 className="text-4xl font-semibold tracking-tight text-slate-900 sm:text-5xl">
                  What do you want to research?
                </h2>

                <p className="mx-auto mt-4 max-w-2xl text-base leading-7 text-slate-500">
                  Ask a question about your indexed research material.
                  The system retrieves relevant evidence, generates a
                  structured report, and evaluates the result.
                </p>

              </div>


              <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-7">

                <textarea
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder="Example: What impact does Generative AI have on software developer productivity?"
                  rows={5}
                  className="w-full resize-none rounded-xl border border-slate-200 bg-slate-50 p-5 text-sm leading-6 text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-indigo-400 focus:bg-white focus:ring-4 focus:ring-indigo-500/10"
                />

                {error && (
                  <div className="mt-4 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-600">
                    <span className="font-semibold">Error:</span>{" "}
                    {error}
                  </div>
                )}

                <div className="mt-4 flex justify-end">

                  <button
                    onClick={generateReport}
                    className="rounded-xl bg-indigo-600 px-7 py-3.5 text-sm font-semibold text-white shadow-lg shadow-indigo-600/20 transition hover:bg-indigo-500"
                  >
                    Start Research →
                  </button>

                </div>

              </div>


              <div className="mt-6 grid gap-3 sm:grid-cols-3">

                {[
                  ["RAG", "Evidence retrieval"],
                  ["Qdrant", "Vector search"],
                  ["Qwen3", "Local generation"],
                ].map(([title, subtitle]) => (
                  <div
                    key={title}
                    className="rounded-xl border border-slate-200 bg-white p-4"
                  >
                    <p className="text-sm font-semibold text-slate-800">
                      {title}
                    </p>
                    <p className="mt-1 text-xs text-slate-500">
                      {subtitle}
                    </p>
                  </div>
                ))}

              </div>

            </section>

          )}


          {/* =================================================
              LOADING
          ================================================== */}

          {loading && (

            <section className="py-10">

              <div className="mb-8">

                <p className="font-mono text-[10px] uppercase tracking-[0.25em] text-emerald-500">
                  Research in progress
                </p>

                <h2 className="mt-2 text-3xl font-semibold tracking-tight">
                  Analyzing your research question
                </h2>

                <p className="mt-2 text-sm text-slate-500">
                  Retrieving evidence and generating an
                  evidence-grounded report.
                </p>

              </div>


              <div className="grid gap-4 md:grid-cols-3 xl:grid-cols-6">

                {pipeline.map((step, index) => (

                  <div
                    key={step.number}
                    className="rounded-2xl border border-indigo-200 bg-white p-5 shadow-sm"
                  >

                    <div className="mb-5 flex items-center justify-between">

                      <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-indigo-50 text-indigo-600">
                        <span className="animate-pulse">◌</span>
                      </div>

                      <span className="font-mono text-[10px] text-slate-400">
                        {step.number}
                      </span>

                    </div>

                    <h3 className="text-sm font-semibold text-slate-800">
                      {step.title}
                    </h3>

                    <p className="mt-1 text-xs text-slate-500">
                      {step.description}
                    </p>

                    <div className="mt-5 flex items-center gap-2 text-[10px] font-medium uppercase tracking-wider text-indigo-500">
                      <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-indigo-500" />
                      Processing
                    </div>

                  </div>

                ))}

              </div>

            </section>

          )}


          {/* =================================================
              WORKSPACE
          ================================================== */}

          {report && !loading && (

            <>

              {/* HEADER */}

              <section className="mb-8">

                <div className="flex flex-col justify-between gap-5 lg:flex-row lg:items-end">

                  <div>

                    <div className="mb-3 flex items-center gap-2">

                      <span className="h-2 w-2 rounded-full bg-emerald-500" />

                      <span className="font-mono text-[10px] font-medium uppercase tracking-[0.2em] text-emerald-600">
                        Research Complete
                      </span>

                    </div>

                    <h2 className="max-w-4xl text-3xl font-semibold tracking-tight text-slate-900 sm:text-4xl">
                      {topic}
                    </h2>

                    <p className="mt-2 font-mono text-[10px] text-slate-400">
                      LOCAL RESEARCH SESSION
                    </p>

                  </div>


                  <button
                    onClick={resetResearch}
                    className="rounded-xl border border-slate-200 bg-white px-5 py-3 text-sm font-medium text-slate-600 transition hover:bg-slate-50"
                  >
                    + New Research
                  </button>

                </div>

              </section>


              {/* TABS */}

              <div className="mb-7 flex gap-1 overflow-x-auto border-b border-slate-200">

                {tabs.map((tab) => (

                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`whitespace-nowrap border-b-2 px-4 py-3 text-sm font-medium transition ${
                      activeTab === tab.id
                        ? "border-indigo-600 text-indigo-600"
                        : "border-transparent text-slate-500 hover:text-slate-800"
                    }`}
                  >
                    {tab.label}
                  </button>

                ))}

              </div>


              {/* =================================================
                  OVERVIEW
              ================================================== */}

              {activeTab === "overview" && (

                <div className="space-y-7">

                  {/* PIPELINE */}

                  <section>

                    <div className="mb-4 flex items-center justify-between">

                      <div>
                        <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-indigo-500">
                          Verified Pipeline
                        </p>

                        <h3 className="mt-1 text-xl font-semibold">
                          Research progression
                        </h3>
                      </div>

                    </div>


                    <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-6">

                      {pipeline.map((step) => (

                        <div
                          key={step.number}
                          className="rounded-2xl border border-emerald-200 bg-emerald-50/40 p-5"
                        >

                          <div className="mb-5 flex items-center justify-between">

                            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-emerald-100 text-emerald-600">
                              ✓
                            </div>

                            <span className="font-mono text-[10px] text-slate-400">
                              {step.number}
                            </span>

                          </div>

                          <h4 className="text-sm font-semibold text-slate-800">
                            {step.title}
                          </h4>

                          <p className="mt-1 text-xs text-slate-500">
                            {step.description}
                          </p>

                          <div className="mt-5 flex items-center gap-2 font-mono text-[9px] uppercase tracking-wider text-emerald-600">
                            <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                            Complete
                          </div>

                        </div>

                      ))}

                    </div>

                  </section>


                  {/* METRICS */}

                  <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">

                    <Metric
                      label="Chunks Retrieved"
                      value="3"
                      description="Top semantic matches"
                      icon="◈"
                    />

                    <Metric
                      label="Sources Used"
                      value={report.citations?.length || 0}
                      description="Cited in report"
                      icon="▥"
                    />

                    <Metric
                      label="Model"
                      value="Qwen3"
                      description="Local LLM"
                      icon="✦"
                    />

                    <Metric
                      label="Research Quality"
                      value={
                        overallPercentage !== null
                          ? `${overallPercentage}%`
                          : "—"
                      }
                      description={
                        quality
                          ? "LLM evaluation"
                          : "Evaluation unavailable"
                      }
                      icon="◇"
                    />

                  </section>


                  {/* PROGRESSION */}

                  <section className="grid gap-5 lg:grid-cols-[1.5fr_1fr]">

                    <div className="rounded-2xl border border-slate-200 bg-white p-7">

                      <div className="mb-7 flex items-center justify-between">

                        <div>

                          <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-indigo-500">
                            Research progression
                          </p>

                          <h3 className="mt-1 text-xl font-semibold">
                            Evidence pipeline
                          </h3>

                        </div>

                        <span className="rounded-full bg-emerald-50 px-3 py-1.5 font-mono text-[9px] uppercase tracking-wider text-emerald-600">
                          Verified
                        </span>

                      </div>


                      <div className="space-y-7">

                        {[
                          [
                            "Research question received",
                            "The system accepted the research query.",
                          ],
                          [
                            "Relevant evidence retrieved",
                            "Qdrant returned the highest similarity chunks.",
                          ],
                          [
                            "Research report generated",
                            "Qwen3 synthesized the retrieved context.",
                          ],
                          [
                            "Quality evaluation completed",
                            quality
                              ? "The generated report was evaluated."
                              : "Quality evaluation was unavailable.",
                          ],
                        ].map(([title, description], index) => (

                          <div
                            key={title}
                            className="relative flex gap-4"
                          >

                            <div className="relative flex flex-col items-center">

                              <span className="z-10 h-3 w-3 rounded-full bg-indigo-500 ring-4 ring-indigo-50" />

                              {index < 3 && (
                                <span className="absolute top-3 h-12 w-px bg-slate-200" />
                              )}

                            </div>

                            <div>

                              <p className="text-sm font-semibold text-slate-800">
                                {title}
                              </p>

                              <p className="mt-1 text-xs leading-5 text-slate-500">
                                {description}
                              </p>

                            </div>

                          </div>

                        ))}

                      </div>

                    </div>


                    {/* QUALITY CARD */}

                    <div className="rounded-2xl bg-[#101827] p-7 text-white">

                      <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-indigo-300">
                        Final Evaluation
                      </p>

                      <div className="mt-6">

                        <p className="text-5xl font-semibold">
                          {overallPercentage !== null
                            ? overallPercentage
                            : "—"}
                          {overallPercentage !== null && (
                            <span className="text-2xl text-slate-500">
                              %
                            </span>
                          )}
                        </p>

                        <p className="mt-2 text-sm text-slate-400">
                          Overall research quality
                        </p>

                      </div>

                      <div className="mt-8 space-y-4">

                        <QualityMini
                          label="Faithfulness"
                          value={quality?.faithfulness?.score}
                        />

                        <QualityMini
                          label="Relevance"
                          value={quality?.relevance?.score}
                        />

                        <QualityMini
                          label="Completeness"
                          value={quality?.completeness?.score}
                        />

                      </div>

                    </div>

                  </section>

                </div>

              )}


              {/* =================================================
                  FINDINGS
              ================================================== */}

              {activeTab === "findings" && (

                <div className="space-y-6">

                  <SectionTitle
                    eyebrow="Research Findings"
                    title="Key findings"
                    description="Evidence-grounded findings generated from the retrieved research context."
                  />


                  {report.executive_summary && (
                    <ReportCard
                      title="Executive Summary"
                      icon="✦"
                    >
                      <p className="leading-8 text-slate-600">
                        {report.executive_summary}
                      </p>
                    </ReportCard>
                  )}


                  {report.key_findings?.length > 0 && (

                    <ReportCard
                      title="Key Findings"
                      icon="01"
                    >

                      <div className="space-y-3">

                        {report.key_findings.map((finding, index) => (

                          <div
                            key={index}
                            className="flex gap-4 rounded-xl border border-slate-200 bg-slate-50 p-4"
                          >

                            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-indigo-100 text-xs font-semibold text-indigo-600">
                              {String(index + 1).padStart(2, "0")}
                            </div>

                            <p className="pt-1 text-sm leading-6 text-slate-700">
                              {finding}
                            </p>

                          </div>

                        ))}

                      </div>

                    </ReportCard>

                  )}


                  {report.research_gaps?.length > 0 && (

                    <ReportCard
                      title="Research Gaps"
                      icon="◇"
                    >

                      <div className="grid gap-3 md:grid-cols-2">

                        {report.research_gaps.map((gap, index) => (

                          <div
                            key={index}
                            className="rounded-xl border border-slate-200 bg-slate-50 p-5"
                          >

                            <div className="mb-3 text-indigo-500">
                              ◇
                            </div>

                            <p className="text-sm leading-6 text-slate-600">
                              {gap}
                            </p>

                          </div>

                        ))}

                      </div>

                    </ReportCard>

                  )}

                </div>

              )}


              {/* =================================================
                  QUALITY
              ================================================== */}

              {activeTab === "quality" && (

                <div className="space-y-6">

                  <SectionTitle
                    eyebrow="Automated Evaluation"
                    title="Quality Check"
                    description="Evaluation of the generated report against the retrieved research context."
                  />

                  {!quality ? (

                    <div className="rounded-2xl border border-amber-200 bg-amber-50 p-6 text-sm text-amber-700">
                      Quality evaluation was not returned by the backend.
                    </div>

                  ) : (

                    <>

                      <div className="grid gap-4 md:grid-cols-3">

                        <QualityCard
                          label="Faithfulness"
                          score={quality.faithfulness}
                        />

                        <QualityCard
                          label="Relevance"
                          score={quality.relevance}
                        />

                        <QualityCard
                          label="Completeness"
                          score={quality.completeness}
                        />

                      </div>


                      <div className="rounded-2xl bg-[#101827] p-8 text-white">

                        <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-indigo-300">
                          Overall Evaluation
                        </p>

                        <p className="mt-3 text-5xl font-semibold">
                          {(quality.overall_score * 100).toFixed(0)}%
                        </p>

                        <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-400">
                          Quality scores are generated by an LLM-based
                          evaluator and should be interpreted as an
                          automated assessment rather than ground truth.
                        </p>

                      </div>

                    </>

                  )}

                </div>

              )}


              {/* =================================================
                  FINAL REPORT
              ================================================== */}

              {activeTab === "report" && (

                <div className="mx-auto max-w-4xl space-y-6">

                  <SectionTitle
                    eyebrow="Final Output"
                    title="Research Report"
                    description="Structured report generated from retrieved research evidence."
                  />


                  {report.executive_summary && (

                    <ReportCard title="Executive Summary" icon="✦">

                      <p className="leading-8 text-slate-600">
                        {report.executive_summary}
                      </p>

                    </ReportCard>

                  )}


                  {report.key_findings?.length > 0 && (

                    <ReportCard title="Key Findings" icon="▣">

                      <div className="space-y-4">

                        {report.key_findings.map((finding, index) => (

                          <div
                            key={index}
                            className="border-b border-slate-100 pb-4 last:border-0 last:pb-0"
                          >

                            <p className="text-sm leading-7 text-slate-700">
                              <span className="mr-3 font-mono text-xs text-indigo-500">
                                {String(index + 1).padStart(2, "0")}
                              </span>

                              {finding}
                            </p>

                          </div>

                        ))}

                      </div>

                    </ReportCard>

                  )}


                  {report.research_gaps?.length > 0 && (

                    <ReportCard title="Research Gaps" icon="◇">

                      <ul className="space-y-4">

                        {report.research_gaps.map((gap, index) => (

                          <li
                            key={index}
                            className="flex gap-3 text-sm leading-7 text-slate-600"
                          >

                            <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-indigo-500" />

                            {gap}

                          </li>

                        ))}

                      </ul>

                    </ReportCard>

                  )}

                </div>

              )}


              {/* =================================================
                  SOURCES
              ================================================== */}

              {activeTab === "sources" && (

                <div className="space-y-6">

                  <SectionTitle
                    eyebrow="Traceability"
                    title="Evidence & Sources"
                    description="Research sources referenced by the generated report."
                  />


                  <div className="space-y-3">

                    {report.citations?.length > 0 ? (

                      report.citations.map((citation, index) => (

                        <div
                          key={index}
                          className="flex items-center gap-4 rounded-2xl border border-slate-200 bg-white p-5"
                        >

                          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600">
                            ▤
                          </div>

                          <div>

                            <p className="text-sm font-medium text-slate-800">
                              {citation}
                            </p>

                            <p className="mt-1 text-xs text-slate-400">
                              Retrieved research evidence
                            </p>

                          </div>

                        </div>

                      ))

                    ) : (

                      <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center text-sm text-slate-500">
                        No source citations were returned.
                      </div>

                    )}

                  </div>

                </div>

              )}

            </>

          )}

        </div>

      </main>

    </div>
  );
}


/* =============================================================
   COMPONENTS
============================================================= */

function Metric({ label, value, description, icon }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">

      <div className="flex items-start justify-between">

        <div>

          <p className="font-mono text-[9px] uppercase tracking-[0.18em] text-slate-400">
            {label}
          </p>

          <p className="mt-3 text-2xl font-semibold tracking-tight text-slate-900">
            {value}
          </p>

          <p className="mt-1 text-xs text-slate-500">
            {description}
          </p>

        </div>

        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-50 text-indigo-500">
          {icon}
        </div>

      </div>

    </div>
  );
}


function SectionTitle({ eyebrow, title, description }) {
  return (
    <div>

      <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-indigo-500">
        {eyebrow}
      </p>

      <h3 className="mt-1 text-3xl font-semibold tracking-tight text-slate-900">
        {title}
      </h3>

      <p className="mt-2 text-sm text-slate-500">
        {description}
      </p>

    </div>
  );
}


function ReportCard({ title, icon, children }) {
  return (
    <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">

      <div className="flex items-center gap-3 border-b border-slate-100 px-6 py-5">

        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-indigo-50 text-sm text-indigo-600">
          {icon}
        </div>

        <h3 className="font-semibold text-slate-900">
          {title}
        </h3>

      </div>

      <div className="px-6 py-6">
        {children}
      </div>

    </section>
  );
}


function QualityCard({ label, score }) {
  const percentage =
    score && typeof score.score === "number"
      ? Math.round(score.score * 100)
      : 0;

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

      <p className="text-sm font-medium text-slate-500">
        {label}
      </p>

      <p className="mt-3 text-4xl font-semibold text-slate-900">
        {percentage}%
      </p>

      <div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-100">

        <div
          className="h-full rounded-full bg-indigo-500 transition-all"
          style={{
            width: `${percentage}%`,
          }}
        />

      </div>

      <p className="mt-4 text-xs leading-5 text-slate-500">
        {score?.reason || "No evaluation reason returned."}
      </p>

    </div>
  );
}


function QualityMini({ label, value }) {
  const percentage =
    typeof value === "number"
      ? Math.round(value * 100)
      : null;

  return (
    <div>

      <div className="mb-2 flex justify-between text-xs">

        <span className="text-slate-400">
          {label}
        </span>

        <span className="font-medium text-white">
          {percentage !== null ? `${percentage}%` : "—"}
        </span>

      </div>

      <div className="h-1.5 overflow-hidden rounded-full bg-white/10">

        <div
          className="h-full rounded-full bg-indigo-400"
          style={{
            width: `${percentage || 0}%`,
          }}
        />

      </div>

    </div>
  );
}