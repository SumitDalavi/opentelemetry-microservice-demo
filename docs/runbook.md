# Runbook — opentelemetry-microservice-demo
> Last updated: 2026-08-29

## Prerequisites
| Tool | Required Version | How to check |
|---|---|---|
| Docker & Compose | Latest | `docker-compose version` |

## Quick Start
```bash
# Start the full stack
docker-compose up -d --build

# Generate traffic
curl http://localhost:3000/api/orders
```

## Run Tests
```bash
# In an actual deployment, you might have unit tests
# For this demo, run the failure walkthrough script:
bash tests/e2e/test_failure_simulation.sh
```

## Environment Variables
| Variable | Default | Purpose |
|---|---|---|
| OTEL_EXPORTER_OTLP_ENDPOINT | `http://otel-collector:4317` | Where services send OTLP data |
| OTEL_SERVICE_NAME | Varies | Identifies the service in traces |

## Common Failure Modes
| Symptom | Cause | Fix |
|---|---|---|
| Missing traces in Jaeger | Collector is down | Restart the `otel-collector` container |
| API Gateway unreachable | Container failed to start | `docker-compose logs api-gateway` |
