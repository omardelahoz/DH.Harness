import pytest
from dh_harness.observability.tracker import TokenUsageTracker
from dh_harness.observability.tracer import SpanTracer

def test_token_tracker_calculates_costs_for_gemini():
    tracker = TokenUsageTracker()

    # Gemini 1.5 Pro: $3.50/M input, $10.50/M output
    entry = tracker.record_usage(
        model_name="gemini-1.5-pro",
        prompt_tokens=1_000_000,
        completion_tokens=1_000_000,
        cached_tokens=0
    )

    assert entry.total_tokens == 2_000_000
    assert abs(entry.cost_usd - 14.00) < 0.01

def test_token_tracker_aggregates_summary():
    tracker = TokenUsageTracker()
    tracker.record_usage("gemini-1.5-flash", prompt_tokens=100_000, completion_tokens=50_000)
    tracker.record_usage("claude-3-5-sonnet", prompt_tokens=200_000, completion_tokens=100_000)

    summary = tracker.get_summary()
    assert summary.total_prompt_tokens == 300_000
    assert summary.total_completion_tokens == 150_000
    assert summary.total_tokens == 450_000
    assert summary.total_cost_usd > 0.0
    assert "gemini-1.5-flash" in summary.model_breakdown
    assert "claude-3-5-sonnet" in summary.model_breakdown

def test_span_tracer_creates_and_exports_opentelemetry_spans():
    tracer = SpanTracer()
    span_id = tracer.start_span("agent_execution", attributes={"agent": "dotnet-lead-engineer"})

    # Simulate step
    tracer.end_span(span_id, attributes={"status": "SUCCESS"})

    spans = tracer.get_spans()
    assert len(spans) == 1
    assert spans[0].name == "agent_execution"
    assert spans[0].duration_ms >= 0.0
    assert spans[0].attributes.get("agent") == "dotnet-lead-engineer"

    json_export = tracer.export_spans_json()
    assert "agent_execution" in json_export
