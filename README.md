# OpenTelemetry Microservice Demo 📡📊

> **Maturity:** Partial Prototype
> _Unified traces, metrics, and logs across a Node.js microservice fleet — demonstrating vendor-neutral observability with the CNCF standard._

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

> **💡 Trace Sampling:** This demo uses the default `AlwaysOn` sampler for full visibility. In production, switch to `ParentBased(TraceIdRatioBased(0.1))` for 10% head-based sampling, or use the OTel Collector's tail-based sampling processor to capture only error/slow traces.

> **💡 Trace Sampling:** This demo uses the default `AlwaysOn` sampler for full visibility. In production, switch to `ParentBased(TraceIdRatioBased(0.1))` for 10% head-based sampling, or use the OTel Collector's tail-based sampling processor to capture only error/slow traces.

## Mock Boundaries (Honest Scope)

| What | Status | Details |
|---|---|---|
| OTel Pipeline | **Real** | Full Jaeger, Prometheus, Loki, Grafana stack running via Docker Compose. |
| Microservices | **Real** | Node.js services auto-instrumented with OTel emitting real telemetry. |
| Traffic | **Mocked** | Simulated curl traffic replaces real user load. |

## 📚 Documentation

- [Architecture](docs/ARCHITECTURE.md) — System diagram and component details
- [Runbook](docs/runbook.md) — Setup, commands, and expected outputs
- [Decisions](docs/decisions.md) — ADRs for observability stack choices
- [Changelog](docs/changelog.md) — Change history
- [Failure Walkthrough](docs/failure_walkthrough.md) — Guide to debugging a simulated failure using OTel traces.

## Decision Log

| Decision | Rationale |
|----------|-----------|
| OTel over vendor SDKs | Vendor-neutral; avoids Datadog/New Relic lock-in |
| OTel Collector over direct export | Collector acts as a gateway, enabling fan-out to multiple backends without code changes |
| Jaeger over Tempo | Jaeger has standalone mode ideal for PoC; Tempo requires object storage |
| 3 services (not 1) | Demonstrates distributed tracing context propagation across service boundaries |


## 📋 Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| [Docker](https://www.docker.com/) | >= 24.x | Container runtime |
| [Docker Compose](https://docs.docker.com/compose/) | >= 2.x | Multi-container orchestration |
| [curl](https://curl.se/) or browser | Any | API testing & UI access |

## 🚀 Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/SumitDalavi/opentelemetry-microservice-demo.git
cd opentelemetry-microservice-demo

# 2. Build and start all services (3 microservices + observability stack)
docker-compose up -d --build

# 3. Verify all containers are running
docker-compose ps
```

### Services & Ports

| Service | URL | Purpose |
|---------|-----|---------|
| API Gateway | http://localhost:3000 | Application entry point |
| Jaeger UI | http://localhost:16686 | Distributed tracing |
| Prometheus | http://localhost:9090 | Metrics collection |
| Grafana | http://localhost:3001 | Dashboards (admin/admin) |
| OTEL Collector | http://localhost:4318 | Telemetry pipeline |

## 🧪 Usage & Demo

### Step 1: Generate traces by calling the API
```bash
# Hit the API Gateway multiple times to generate trace data
curl http://localhost:3000/api/orders
curl http://localhost:3000/api/orders
curl http://localhost:3000/api/orders
```

### Step 2: View distributed traces in Jaeger
1. Open **http://localhost:16686**
2. Select **"api-gateway"** from the Service dropdown
3. Click **"Find Traces"**
4. Click on a trace to see the full request flow across microservices (api-gateway â†’ order-service â†’ payment-service)

### Step 3: View metrics in Prometheus
1. Open **http://localhost:9090**
2. Try queries like:
   - `http_requests_total` â€” Total HTTP requests per service
   - `http_request_duration_seconds_bucket` â€” Request latency distribution

### Step 4: Explore Grafana dashboards
1. Open **http://localhost:3001** (login: **admin** / **admin**)
2. Add Prometheus as a data source (URL: `http://prometheus:9090`)
3. Add Jaeger as a data source (URL: `http://jaeger:16686`)

## ✅ Verification

| Check | Command / Action | Expected |
|-------|-----------------|----------|
| All services up | `docker-compose ps` | 7 containers running |
| API responds | `curl http://localhost:3000/api/orders` | Order JSON response |
| Traces visible | Open Jaeger UI â†’ Find Traces | Multi-span traces |
| Metrics flowing | Prometheus â†’ `http_requests_total` | Incrementing counters |

```bash
# Stop all services
docker-compose down
```

## 👨‍💻 Author

**Sumit Dalavi** — Senior DevSecOps / Platform Engineer
[GitHub](https://github.com/SumitDalavi) | [LinkedIn](https://in.linkedin.com/in/sumit-dalavi-762838129)

---

*Built with a focus on production-grade patterns, not toy demos.*