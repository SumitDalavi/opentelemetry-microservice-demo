"""Tests for OpenTelemetry instrumentation configuration."""
import pytest
import yaml
import json
import os

SERVICES_DIR = os.path.join(os.path.dirname(__file__), '..', 'services')
K8S_DIR = os.path.join(os.path.dirname(__file__), '..', 'k8s')
GRAFANA_DIR = os.path.join(os.path.dirname(__file__), '..', 'grafana', 'dashboards')


def test_otel_collector_config_valid():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'otel-collector', 'config.yaml')
    with open(config_path) as f:
        config = yaml.safe_load(f)
    assert 'exporters' in config
    assert 'receivers' in config
    assert 'service' in config


def test_grafana_dashboard_json_valid():
    for fname in os.listdir(GRAFANA_DIR):
        if fname.endswith('.json'):
            with open(os.path.join(GRAFANA_DIR, fname)) as f:
                dash = json.load(f)
            assert 'panels' in dash, f"{fname}: missing panels"
            assert 'title' in dash, f"{fname}: missing title"
            assert len(dash['panels']) > 0, f"{fname}: no panels"


def test_all_services_have_tracing():
    for svc in ['api-gateway', 'order-service', 'payment-service']:
        svc_dir = os.path.join(SERVICES_DIR, svc)
        tracing_file = os.path.join(svc_dir, 'tracing.js')
        assert os.path.exists(tracing_file), f"Service {svc} missing tracing.js"
        content = open(tracing_file).read()
        assert 'opentelemetry' in content.lower() or 'NodeSDK' in content or 'tracer' in content.lower()


def test_k8s_manifests_valid_yaml():
    for fname in os.listdir(K8S_DIR):
        if fname.endswith(('.yaml', '.yml')):
            with open(os.path.join(K8S_DIR, fname)) as f:
                docs = list(yaml.safe_load_all(f))
            for doc in docs:
                if doc:
                    assert 'apiVersion' in doc
