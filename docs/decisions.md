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

## ADR-002: Progressive Credential Loading (PCL) Architecture
- **Context:** Production hardening required live backends (PostgreSQL, Redis, OpenAI, Anthropic), but removing mocks would break CI pipelines and create high developer onboarding friction.
- **Decision:** Implement Progressive Credential Loading. Keep in-memory and local mock heuristics as the default safe baseline, while wrapping external integrations in auto-promoting factory adapters triggered by environment variables.
- **Consequences:** 
  - *Pros:* 100% CI pass rate without requiring external secrets; zero setup friction for new contributors; progressive upgrade to production clusters.
  - *Cons:* Adds lightweight factory abstraction layers and runtime credential detection logic.
