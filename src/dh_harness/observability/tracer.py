"""OpenTelemetry-compatible span tracer for agent workflows."""
import json
import time
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

from dh_harness.core.contracts import SpanTrace


class SpanTracer:
    """Manages active and completed spans for distributed workflow tracing."""

    def __init__(self, trace_id: Optional[str] = None) -> None:
        self.trace_id = trace_id or uuid.uuid4().hex
        self._active_spans: Dict[str, Dict[str, Any]] = {}
        self.completed_spans: List[SpanTrace] = []

    def start_span(
        self,
        name: str,
        attributes: Optional[Dict[str, Any]] = None,
        parent_id: Optional[str] = None
    ) -> str:
        """Starts a new span and records initial timestamp."""
        span_id = uuid.uuid4().hex[:16]
        start_dt = datetime.now(timezone.utc)
        start_monotonic = time.perf_counter()

        self._active_spans[span_id] = {
            "name": name,
            "parent_id": parent_id,
            "start_time": start_dt.isoformat(),
            "start_monotonic": start_monotonic,
            "attributes": dict(attributes or {})
        }
        return span_id

    def end_span(
        self,
        span_id: str,
        attributes: Optional[Dict[str, Any]] = None
    ) -> Optional[SpanTrace]:
        """Ends an active span, calculating duration and recording to trace list."""
        span_data = self._active_spans.pop(span_id, None)
        if not span_data:
            return None

        end_dt = datetime.now(timezone.utc)
        end_monotonic = time.perf_counter()
        duration_ms = round((end_monotonic - span_data["start_monotonic"]) * 1000.0, 3)

        combined_attributes = dict(span_data["attributes"])
        if attributes:
            combined_attributes.update(attributes)

        span_trace = SpanTrace(
            trace_id=self.trace_id,
            span_id=span_id,
            parent_id=span_data["parent_id"],
            name=span_data["name"],
            start_time=span_data["start_time"],
            end_time=end_dt.isoformat(),
            duration_ms=duration_ms,
            attributes=combined_attributes
        )
        self.completed_spans.append(span_trace)
        return span_trace

    def get_spans(self) -> List[SpanTrace]:
        """Returns the list of all completed spans."""
        return list(self.completed_spans)

    def export_spans_json(self) -> str:
        """Exports traces formatted according to OpenTelemetry JSON schema."""
        otel_export = {
            "resourceSpans": [
                {
                    "resource": {
                        "attributes": [
                            {"key": "service.name", "value": {"stringValue": "dh-engineering-harness"}},
                            {"key": "telemetry.sdk.language", "value": {"stringValue": "python"}}
                        ]
                    },
                    "scopeSpans": [
                        {
                            "scope": {"name": "dh_harness.observability.tracer"},
                            "spans": [
                                {
                                    "traceId": span.trace_id,
                                    "spanId": span.span_id,
                                    "parentSpanId": span.parent_id or "",
                                    "name": span.name,
                                    "kind": 1,
                                    "startTimeUnixNano": int(datetime.fromisoformat(span.start_time).timestamp() * 1e9),
                                    "endTimeUnixNano": int(datetime.fromisoformat(span.end_time).timestamp() * 1e9),
                                    "attributes": [
                                        {"key": k, "value": {"stringValue": str(v)}}
                                        for k, v in span.attributes.items()
                                    ],
                                    "durationMs": span.duration_ms
                                }
                                for span in self.completed_spans
                            ]
                        }
                    ]
                }
            ]
        }
        return json.dumps(otel_export, indent=2)
