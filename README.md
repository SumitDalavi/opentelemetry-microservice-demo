# OpenTelemetry Microservice Demo 📡📊

> Unified traces, metrics, and logs across a Node.js microservice fleet — demonstrating vendor-neutral observability with the CNCF standard.

## The Problem

Most teams bolt on monitoring as an afterthought: Prometheus for metrics, a separate tool for traces, another for logs. This creates vendor lock-in, data silos, and incomplete observability. You can see *that* a request is slow, but not *why* — because traces, metrics, and logs aren't correlated.

## The Solution

This project instruments a small Node.js service set with **OpenTelemetry** — the vendor-neutral CNCF standard — providing unified traces, metrics, and logs that flow through a single collector into open-source backends:

```
┌────────────┐  ┌────────────┐  ┌────────────┐
│ API Gateway│──│ Order Svc  │──│ Payment Svc│
└─────┬──────┘  └─────┬──────┘  └─────┬──────┘
      │               │               │
      └───────────────┼───────────────┘
                      │  OTLP
              ┌───────▼───────┐
              │  OTel Collector│
              └───┬───┬───┬───┘
                  │   │   │
            ┌─────┘   │   └─────┐
            ▼         ▼         ▼
       ┌────────┐ ┌───────┐ ┌────────┐
       │ Jaeger │ │Prom.  │ │ Loki   │
       │(Traces)│ │(Metr.)│ │ (Logs) │
       └────────┘ └───────┘ └────────┘
                      │
                 ┌────▼────┐
                 │ Grafana  │
                 │Dashboard │
                 └──────────┘
```

## Why This Over the Obvious Alternative

Adding `prom-client` to an Express app is a 10-minute tutorial. This project demonstrates the **full OpenTelemetry pipeline**: auto-instrumented traces that propagate context across services, custom metrics, structured logs with trace correlation, and a Collector that routes telemetry to multiple backends. That's what SRE interviews actually test.

## 🛠️ Tech Stack

- **Instrumentation**: OpenTelemetry Node.js SDK
- **Collection**: OTel Collector
- **Traces**: Jaeger
- **Metrics**: Prometheus
- **Logs**: Loki
- **Dashboards**: Grafana
- **Orchestration**: Docker Compose

## 📁 Project Structure

```
├── services/
│   ├── api-gateway/        # Express gateway with OTel auto-instrumentation
│   ├── order-service/      # Order processing service
│   └── payment-service/    # Payment processing service
├── otel-collector/
│   └── config.yaml         # OTel Collector pipeline configuration
├── grafana/
│   └── dashboards/         # Pre-configured Grafana dashboards
├── docker-compose.yaml     # Full stack: services + collector + backends
├── docs/ARCHITECTURE.md
└── README.md
```

## 🚀 Getting Started

```bash
docker-compose up -d --build
```

| UI | URL |
|----|-----|
| API Gateway | http://localhost:3000 |
| Jaeger (Traces) | http://localhost:16686 |
| Prometheus (Metrics) | http://localhost:9090 |
| Grafana (Dashboards) | http://localhost:3001 |

## Decision Log

| Decision | Rationale |
|----------|-----------|
| OTel over vendor SDKs | Vendor-neutral; avoids Datadog/New Relic lock-in |
| OTel Collector over direct export | Collector acts as a gateway, enabling fan-out to multiple backends without code changes |
| Jaeger over Tempo | Jaeger has standalone mode ideal for PoC; Tempo requires object storage |
| 3 services (not 1) | Demonstrates distributed tracing context propagation across service boundaries |

## 👨‍💻 Author

*Built to extend Prometheus/Grafana/Datadog expertise with the vendor-neutral CNCF observability standard.*
