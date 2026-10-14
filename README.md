# EchoTrace MVP

Correlates physical audio anomalies with digital access logs to identify insider threats.

## Setup
pip install -r requirements.txt

## Run Demo
python main.py

## Run Tests
pytest -q

## Architecture

![Architecture](docs/architecture.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    A[AudioCapture] -->|Audio Events| B[Buffer]
    C[AccessLogger] -->|Access Logs| D[Log Store]
    B --> E[AnomalyDetector]
    D --> E
    E -->|Correlated Threats| F[Alert System]
```

</details>
