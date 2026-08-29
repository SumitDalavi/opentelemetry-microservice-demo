# Decisions

## ADR-001: OTel Collector vs Direct Export
**Date:** 2026-08-29  
**Status:** Accepted

**Context:**  
We can instrument Node.js apps to export traces directly to Jaeger (e.g. via `JaegerExporter`).

**Decision:**  
We will use `OTLPTraceExporter` to send traces to an OpenTelemetry Collector, which then routes them to Jaeger.

**Consequences:**  
- ✅ Application code is completely unaware of the backend (Jaeger).
- ✅ We can swap Jaeger for Datadog or Zipkin by only changing `otel-collector-config.yaml`.
- ⚠️ Requires running an extra infrastructure component (the Collector).
