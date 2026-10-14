import time
import random
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class AudioEvent:
    timestamp: float
    amplitude: float
    zone: str

class AudioCapture:
    def __init__(self, zone: str):
        self.zone = zone
        self.buffer: List[AudioEvent] = []

    def ingest(self, amplitude: float, duration: float = 0.1) -> AudioEvent:
        event = AudioEvent(
            timestamp=time.time(),
            amplitude=amplitude,
            zone=self.zone
        )
        self.buffer.append(event)
        return event

class AccessLogger:
    def __init__(self):
        self.logs: List[Dict] = []

    def log_access(self, user: str, device: str, action: str) -> Dict:
        entry = {
            "user": user,
            "device": device,
            "action": action,
            "timestamp": time.time()
        }
        self.logs.append(entry)
        return entry

class AnomalyDetector:
    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold

    def detect(self, audio_buffer: List[AudioEvent]) -> List[AudioEvent]:
        anomalies = []
        for event in audio_buffer:
            if event.amplitude > self.threshold:
                anomalies.append(event)
        return anomalies

class VectorStore:
    def __init__(self):
        self.embeddings: List[Dict] = []

    def add(self, text: str, metadata: Dict):
        self.embeddings.append({"text": text, "meta": metadata})

    def query(self, text: str, k: int = 5) -> List[Dict]:
        return self.embeddings[-k:] if self.embeddings else []

@dataclass
class Alert:
    severity: str
    message: str
    timestamp: float
    details: Dict = field(default_factory=dict)

class CorrelationEngine:
    def __init__(self, time_window: float = 1.0):
        self.time_window = time_window
        self.vector_store = VectorStore()
        self.alerts: List[Alert] = []

    def correlate(self, anomalies: List[AudioEvent], logs: List[Dict]) -> List[Alert]:
        alerts = []
        for anomaly in anomalies:
            for log in logs:
                if abs(anomaly.timestamp - log["timestamp"]) <= self.time_window:
                    alert = Alert(
                        severity="HIGH",
                        message=f"Audio spike in {anomaly.zone} correlates with {log['user']} access.",
                        timestamp=anomaly.timestamp,
                        details={"zone": anomaly.zone, "user": log["user"]}
                    )
                    alerts.append(alert)
                    self.vector_store.add(
                        f"Anomaly in {anomaly.zone}",
                        {"user": log["user"], "time": log["timestamp"]}
                    )
        self.alerts.extend(alerts)
        return alerts

def demo():
    print("Starting EchoTrace MVP...")
    capture = AudioCapture(zone="ServerRoomA")
    logger = AccessLogger()
    detector = AnomalyDetector(threshold=0.8)
    engine = CorrelationEngine(time_window=1.0)

    # Normal activity
    capture.ingest(0.2)
    logger.log_access("admin", "laptop", "login")

    # Anomalous activity
    capture.ingest(0.95)
    logger.log_access("unknown", "usb_drive", "copy")

    anomalies = detector.detect(capture.buffer)
    alerts = engine.correlate(anomalies, logger.logs)

    print(f"Detected {len(anomalies)} anomalies.")
    print(f"Generated {len(alerts)} alerts.")
    for a in alerts:
        print(f"ALERT: {a.message}")
    return alerts

if __name__ == "__main__":
    demo()