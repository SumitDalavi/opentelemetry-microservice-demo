# Trace-to-Incident Walkthrough

**Demo:** How to identify, diagnose, and resolve a latency regression using distributed tracing.

## Setup

```bash
make up      # Starts all services (Jaeger on :16686, Prometheus on :9090, Grafana on :3000)
make traffic # Generates synthetic traffic with artificial latency injection
```

---

## Step 1 — Inject Artificial Latency

The demo app includes a latency injection middleware. To simulate a slow downstream service:

```bash
# Set the order-service to respond slowly (500ms artificial delay)
curl -X POST http://localhost:3001/admin/inject-latency \
  -H "Content-Type: application/json" \
  -d '{"delay_ms": 500, "service": "payment-service"}'
```

Expected behavior: The `/checkout` endpoint latency increases from ~20ms to ~520ms.

---

## Step 2 — Observe the Prometheus Alert

Open Grafana at **http://localhost:3000** (admin/admin).

Navigate to **Alerting > Alert Rules**. You should see:

```
FIRING: HighRequestLatency
  Condition: http_request_duration_seconds{quantile="0.99"} > 0.5
  Labels: service=checkout-service
  Started: 14s ago
```

This is the first signal that something is wrong. Now you need to find *why*.

---

## Step 3 — Drill Into the Trace in Jaeger

Open Jaeger at **http://localhost:16686**.

1. Select **Service**: `checkout-service`
2. Select **Operation**: `POST /checkout`
3. Set **Min Duration**: `400ms` to filter for the slow traces
4. Click **Find Traces**

You should see traces where the total duration jumped from ~20ms to ~520ms.

Click on the slowest trace. You'll see the waterfall:

```
checkout-service  POST /checkout                     521ms
  ├── inventory-service   GET /stock/check             4ms  ✅ OK
  ├── payment-service     POST /payment/authorize    503ms  ⚠️ SLOW
  │     └── db-postgres   query: INSERT payments        2ms  ✅ OK
  └── notification-service  POST /notify                3ms  ✅ OK
```

**Root cause identified:** `payment-service → POST /payment/authorize` is taking 503ms, but its own database query is only 2ms. The latency is inside the payment service's application logic (the injected delay), not at the database level.

---

## Step 4 — Read the Span Attributes

Click on the `payment-service: POST /payment/authorize` span. You'll see span attributes:

```
http.method:          POST
http.url:             /payment/authorize
http.status_code:     200
custom.latency_mode:  injected
custom.delay_ms:      500
service.version:      2.1.0
deployment.env:       staging
```

The `custom.latency_mode: injected` tag immediately tells you this is a deliberate delay — in production this would be replaced by e.g., `db.connection_pool: exhausted` or `external_api.timeout: true`.

---

## Step 5 — Remove the Latency and Verify Recovery

```bash
curl -X DELETE http://localhost:3001/admin/inject-latency
```

Wait ~30 seconds. In Grafana, the `HighRequestLatency` alert should resolve (turn green).

In Jaeger, new traces for `POST /checkout` should show the original ~20ms total duration.

---

## Key Observability Insights

| Tool | Role in This Walkthrough |
|---|---|
| **Prometheus + Grafana** | First signal — P99 latency alert told us *something* was wrong |
| **Jaeger (distributed tracing)** | Root cause — showed *exactly which service and span* was slow |
| **Span attributes** | Context — revealed the latency was injected at application level, not DB |

### Why This Matters at Staff/Principal Level

A common anti-pattern is relying solely on dashboards. Dashboards show *what* is wrong (latency spike in service X). Only distributed tracing shows *why* — which specific operation in which specific downstream dependency caused the latency, and what its attributes were at the time.

This is the difference between a 45-minute incident investigation ("which service is slow?") and a 2-minute one ("payment-service span 503ms, attribute shows injected delay in v2.1.0 deployment").

---

## Architecture Reference

```
Client
  │
  ▼ POST /checkout
checkout-service (OTel SDK instrumented)
  ├── traces → Jaeger Collector (OTLP :4317)
  ├── metrics → Prometheus (:9090)
  │
  ├─► inventory-service (OTel SDK instrumented)
  ├─► payment-service   (OTel SDK instrumented) ← LATENCY SOURCE
  └─► notification-service (OTel SDK instrumented)
         │
         ▼
    Jaeger UI (:16686) — trace correlation, service graphs, critical path
    Grafana (:3000) — alerting, SLO dashboards, metric trends
```
