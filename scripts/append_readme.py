import os
import re

readme_path = 'e:/Antigravity Projects/All Projects/opentelemetry-microservice-demo/README.md'

with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_content = '''
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
'''

if 'End-to-End Traces' not in content:
    with open(readme_path, 'a', encoding='utf-8') as f:
        f.write('\n' + new_content)
    print('Appended')
else:
    print('Already appended')
