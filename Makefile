.PHONY: up down traffic demo walkthrough help

## up: Start all observability services (Jaeger, Prometheus, Grafana + microservices)
up:
	docker compose up --build -d
	@echo "✅ Services started. Jaeger: http://localhost:16686 | Grafana: http://localhost:3000"

## down: Stop all services and remove volumes
down:
	docker compose down -v

## traffic: Generate synthetic traffic for 1 minute to produce traces
traffic:
	@echo "Generating synthetic traffic for 1 minute..."
	powershell -File .\scripts\generate_traffic.ps1

## demo: Start services, generate traffic, and open Jaeger UI
demo: up
	@echo "⏳ Waiting 10s for services to stabilize..."
	sleep 10
	$(MAKE) traffic
	@echo "✅ Demo complete. Open Jaeger at http://localhost:16686 to view traces."
	@echo "   See docs/trace-to-incident-walkthrough.md for guided analysis."

## walkthrough: Print the trace-to-incident walkthrough
walkthrough:
	@cat docs/trace-to-incident-walkthrough.md

## help: Show this help
help:
	@grep -E '^## ' Makefile | sed 's/## /  /'

