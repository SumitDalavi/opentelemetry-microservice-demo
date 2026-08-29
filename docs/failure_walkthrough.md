# Failure Walkthrough: Investigating a 500 Error

This walkthrough demonstrates how an SRE uses the OpenTelemetry stack to investigate a simulated failure in production.

## 1. The Incident
Alert fires: High 500 error rate on `/api/orders` endpoint in the `api-gateway`.

## 2. Metrics (Prometheus / Grafana)
We open the Grafana dashboard (`http://localhost:3001`):
1. We check the `HTTP Request Duration` panel and notice a spike in P99 latency.
2. We check the `HTTP Status Codes` panel and see a spike in HTTP 500s from the `api-gateway`.

*Insight*: The API Gateway is throwing errors, but we don't know *why*.

## 3. Tracing (Jaeger)
We pivot to Jaeger (`http://localhost:16686`) to inspect individual failing requests:
1. We search for traces where `service=api-gateway` and `error=true`.
2. We click into a trace. We see the following span hierarchy:
   - `[api-gateway] POST /api/orders` (Error = true)
     - `[order-service] ProcessOrder` (Error = true)
       - `[payment-service] ChargeCard` (Error = true, Status: `connection_refused`)

*Insight*: The root cause is not in the API Gateway. The `payment-service` rejected the connection.

## 4. Logs (Loki via OTel Correlation)
Because our OTel auto-instrumentation injects `trace_id` into the logs, we can search Loki for the exact `trace_id` found in Jaeger.
1. We search Loki: `{app="payment-service"} |= "trace_id=1234567890abcdef"`
2. The exact log line appears: `ERROR [payment-service] Database connection pool exhausted.`

## 5. Resolution
The root cause was a connection pool exhaustion in the `payment-service`'s database, cascading up to the `api-gateway` as a 500 error.

**Remediation**: Increase the DB connection pool size in `payment-service` and add a circuit breaker in `order-service`.
