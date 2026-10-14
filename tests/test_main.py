import pytest
from main import AudioCapture, AccessLogger, AnomalyDetector, CorrelationEngine, Alert

def test_startup():
    capture = AudioCapture(zone="TestZone")
    assert capture.zone == "TestZone"
    assert len(capture.buffer) == 0

def test_happy_path():
    capture = AudioCapture(zone="Room1")
    logger = AccessLogger()
    detector = AnomalyDetector(threshold=0.8)
    engine = CorrelationEngine(time_window=1.0)

    # Inject high amplitude
    capture.ingest(0.95)
    # Inject correlated log
    logger.log_access("user1", "pc", "access")

    anomalies = detector.detect(capture.buffer)
    assert len(anomalies) == 1

    alerts = engine.correlate(anomalies, logger.logs)
    assert len(alerts) == 1
    assert alerts[0].severity == "HIGH"

def test_failure_path_no_correlation():
    capture = AudioCapture(zone="Room2")
    logger = AccessLogger()
    detector = AnomalyDetector(threshold=0.8)
    engine = CorrelationEngine(time_window=0.001) # Tiny window

    capture.ingest(0.95)
    import time
    time.sleep(0.1) # Delay log
    logger.log_access("user2", "pc", "access")

    anomalies = detector.detect(capture.buffer)
    alerts = engine.correlate(anomalies, logger.logs)
    assert len(alerts) == 0