# OpenTelemetry Microservice Demo 📡📊

[![CI Pipeline](https://github.com/SumitDalavi/opentelemetry-microservice-demo/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/SumitDalavi/opentelemetry-microservice-demo/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/SumitDalavi/opentelemetry-microservice-demo?color=0969da&label=release&logo=github)](https://github.com/SumitDalavi/opentelemetry-microservice-demo/releases)
[![Release Workflow](https://github.com/SumitDalavi/opentelemetry-microservice-demo/actions/workflows/release.yml/badge.svg)](https://github.com/SumitDalavi/opentelemetry-microservice-demo/actions/workflows/release.yml)
[![GHCR Container](https://img.shields.io/badge/ghcr.io-v0.2.0-blue?logo=docker&logoColor=white)](https://github.com/SumitDalavi/opentelemetry-microservice-demo/pkgs/container/opentelemetry-microservice-demo)
[![Node.js](https://img.shields.io/badge/Node.js-20+-339933?logo=nodedotjs&logoColor=white)](https://nodejs.org)
[![SBOM](https://img.shields.io/badge/SBOM-SPDX%202.3-blueviolet?logo=spdx)](https://github.com/SumitDalavi/opentelemetry-microservice-demo/releases/tag/v0.2.0)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

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

> **💡 Trace Sampling:** This demo uses the default `AlwaysOn` sampler for full visibility. In production, switch to `ParentBased(TraceIdRatioBased(0.1))` for 10% head-based sampling, or use the OTel Collector's tail-based sampling processor to capture only error/slow traces.

> **💡 Trace Sampling:** This demo uses the default `AlwaysOn` sampler for full visibility. In production, switch to `ParentBased(TraceIdRatioBased(0.1))` for 10% head-based sampling, or use the OTel Collector's tail-based sampling processor to capture only error/slow traces.

## Mock Boundaries (Honest Scope)

| What | Status | Details |
|---|---|---|
| OTel Pipeline | **Real** | Full Jaeger, Prometheus, Loki, Grafana stack running via Docker Compose. |
| Microservices | **Real** | Node.js services auto-instrumented with OTel emitting real telemetry. |
| Traffic | **Mocked** | Simulated curl traffic replaces real user load. |

## 🚀 Progressive Credential Loading & Execution Tiers

This project implements **Progressive Credential Loading (PCL)**, allowing it to run immediately out-of-the-box without external dependencies while seamlessly upgrading as credentials are provided.

### Tier 1: Zero-Config Mock Mode (Default)
Ideal for CI, testing, and rapid local evaluation.
- **Execution:** Run with default configuration (`cp .env.example .env`). Zero API keys, databases, or cloud credentials required.
- **Fallback Behavior:** In-memory caches, deterministic offline heuristics, mock vector embeddings, and local mock storage are automatically used.
- **Health Verification:** Endpoints report `{"mode": "mock"}` for unconfigured dependencies.

### Tier 2: Local Development with Live Services
Connect specific external services while keeping others mocked.
- **Execution:** Provide credentials in `.env` for the services you want active (e.g., `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT, OTEL_EXPORTER_OTLP_METRICS_ENDPOINT, SERVICE_NAME`).
- **Progressive Upgrade:** The runtime inspects environment variables on boot and dynamically promotes only configured modules to live mode.
- **Safe Fallback:** Any missing credentials automatically remain on mock fallbacks with no crashes or missing service errors.

### Tier 3: Production Hardened
Enterprise deployment with production-grade backends, security scans, and container distributions.
- **OCI Container Image:** Pre-built, multi-arch image on GitHub Container Registry:
  ```bash
  docker pull ghcr.io/sumitdalavi/opentelemetry-microservice-demo:v0.2.0
  ```
- **Production Orchestration:** Mount secrets via Kubernetes Secrets or cloud secret managers with atomic config reload support.
- **Release Verification:** Checksums and SPDX SBOM available on [GitHub Releases](https://github.com/SumitDalavi/opentelemetry-microservice-demo/releases).

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
| Traces visible | Open Jaeger UI → Find Traces | Multi-span traces |
| Metrics flowing | Prometheus → `http_requests_total` | Incrementing counters |

```bash
# Stop all services
docker-compose down
```

## End-to-End Traces (Evidence)

The services in this repository are instrumented with the OpenTelemetry Node.js SDK, including custom spans within the `order-service`. Traces are exported via OTLP to the OpenTelemetry Collector and visualized in Jaeger.

You can verify the end-to-end trace propagation by running the traffic generation script:

```bash
make traffic
```

After generating traffic, you can view the resulting traces by querying the Jaeger API:

```bash
curl -s "http://localhost:16686/api/traces?service=order-service&limit=1"
```

**Simulated Trace Output (Evidence):**
```json
[
    {
        "operationName":  "GET /api/orders",
        "startTime":  1788016728636000,
        "duration":  6679
    },
    {
        "operationName":  "process-orders",
        "startTime":  1788016728639000,
        "duration":  3615
    },
    {
        "operationName":  "GET /payments/verify",
        "startTime":  1788016728640000,
        "duration":  716
    }
]
```

## 🔒 Release & Security Verification

The project includes an automated DevSecOps release pipeline (`.github/workflows/release.yml`) triggered on semantic version tags (`v*.*.*`).

Each release automatically:
1. Executes test suite gates.
2. Builds the container image.
3. Performs vulnerability scanning via Trivy.
4. Generates an SPDX SBOM (`sbom.spdx.json`) using Anchore Syft.
5. Publishes a GitHub Release with attached SBOM.

### Verifying the Release
```bash
# Verify release via GitHub CLI
gh release view v0.2.0 --repo SumitDalavi/opentelemetry-microservice-demo

# Download and inspect SBOM
gh release download v0.2.0 --repo SumitDalavi/opentelemetry-microservice-demo --pattern "sbom.spdx.json"
cat sbom.spdx.json | jq .
```

## 📚 Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Runbook](docs/runbook.md)
- [Decisions](docs/decisions.md)
- [Changelog](docs/changelog.md)

## 👨‍💻 Author

**Sumit Dalavi** — Senior DevSecOps / Platform Engineer
[GitHub](https://github.com/SumitDalavi) | [LinkedIn](https://in.linkedin.com/in/sumit-dalavi-762838129)

---
*Built with a focus on robust patterns, not toy demos.*
