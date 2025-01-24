# xray-otlp-dynatrace

## Initial Setup

### Python Prep
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
### Collector Prep

Change <environmentId> to your Dynatrace Environment ID
Example: abcd1234.live.dynatrace.com, the environment ID is abcd1234

Change <api-token> to an API token in Dynatrace with proper scopes to ingest traces.

## Tracing

### X-Ray tracing only

Start AWS Distro For OpenTelemetry Collector
```
    docker run --rm -p 2000:2000/udp -p 55680:55680 -p 8889:8888 \
      -e AWS_REGION=us-west-2 \
      -e AWS_PROFILE=default \
      -v ~/.aws:/home/aoc/.aws \
      -v "${PWD}/otel-collector-config.yaml":/otel-local-config.yaml \
      --name awscollector public.ecr.aws/aws-observability/aws-otel-collector:latest \
      --config otel-local-config.yaml;
```

Start Flask Application
```
flask --app app run
```

### X-Ray + OpenTelemetry Tracing (if you want to compare differences side by side)

Start AWS Distro For OpenTelemetry Collector
```
    docker run --rm -p 4317:4317 -p 4318:4318 -p 2000:2000/udp -p 55680:55680 -p 8889:8888 \
      -e AWS_REGION=us-west-2 \
      -e AWS_PROFILE=default \
      -v ~/.aws:/home/aoc/.aws \
      -v "${PWD}/otel-collector-config.yaml":/otel-local-config.yaml \
      --name awscollector public.ecr.aws/aws-observability/aws-otel-collector:latest \
      --config otel-local-config.yaml;
```

Start Flask Application
```
OTEL_PYTHON_DISTRO="aws_distro" \
OTEL_PYTHON_CONFIGURATOR="aws_configurator" \
OTEL_SERVICE_NAME="flask-demo"
opentelemetry-instrument flask --app app run
```

## Validate

Navigate to http://localhost:5000 and/or http://localhost:5000/trace

After a few seconds to minutes, the trace should be visible in Dynatrace in the Distributed Tracing or Distributed Traces Classic applications
