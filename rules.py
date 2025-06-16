from collections import defaultdict
from datetime import timedelta

def detect_brute_force(logs, threshold=5, interval_minutes=5):
    alerts = []
    failed_attempts = defaultdict(list)

    # Group failed login attempts by IP
    for log in logs:
        if log.status == "failed":
            failed_attempts[log.source_ip].append(log.timestamp)

    # Check each IP for rapid multiple failures
    for ip, timestamps in failed_attempts.items():
        timestamps.sort()
        for i in range(len(timestamps) - threshold + 1):
            window_start = timestamps[i]
            window_end = timestamps[i + threshold - 1]
            if (window_end - window_start) <= timedelta(minutes=interval_minutes):
                alerts.append(f"🔐 Brute force detected from {ip} - {threshold} failed attempts within {interval_minutes} mins")
                break  # Alert once per IP

    return alerts