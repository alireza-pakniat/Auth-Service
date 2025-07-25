# Auth-Service

## Running the Services

To start all required services for this project, use the following commands in separate terminals or as a script:

```bash
./prometheus/prometheus --config.file=prometheus/prometheus.yml
```

```bash
uvicorn app.main:app --reload
```

```bash
./alertmanager/alertmanager --config.file=alertmanager/alertmanager.yml
```

## Monitoring Expressions (Prometheus)

You can use these Prometheus expressions to monitor your service:

- `process_cpu_seconds_total`
- `http_requests_total`

Open the Prometheus web UI at [http://localhost:9090](http://localhost:9090) and enter these expressions in the "Expression" box to view metrics.