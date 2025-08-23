#!/usr/bin/python3
import time
import psutil

def collect_metrics(duration: int = 3, interval: int = 1):
    """
    Collect CPU and RAM usage over a given duration.
    
    :param duration: total time (seconds) to collect metrics
    :param interval: time (seconds) between samples
    :return: list of dicts with cpu and ram usage
    """
    data = []
    end_time = time.time() + duration
    
    while time.time() < end_time:
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        data.append({"cpu": cpu, "ram": ram})
        time.sleep(interval)
    
    return data

# Example usage
if __name__ == "__main__":
    metrics = collect_metrics(duration=5, interval=1)
    print(metrics)