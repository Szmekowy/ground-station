class MQTTConfig:
    BROKER = "mqtt"
    PORT = 1883

class MQTTTopics:
    RAW = "balloon/raw"
    PROCESSED = "balloon/processed"
    STATUS = "balloon/status"
    COMMAND = "balloon/command"
    ALARMS = "balloon/alarm"
    TELEMETRY = "balloon/telemetry"
    GPS = "balloon/telemetry/gps"
    IMU = "balloon/telemetry/imu"