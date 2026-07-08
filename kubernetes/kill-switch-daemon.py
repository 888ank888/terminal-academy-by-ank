import time
import json
import subprocess
import sys

NAMESPACE = "academy-sandboxes"
CPU_THRESHOLD_MILLICORES = 225  # 90% of the 250m cpus limit (0.25 core)
POLL_INTERVAL_SEC = 5

def get_pod_metrics():
    try:
        # Fetch CPU/memory metrics from metrics-server
        cmd = ["kubectl", "get", "--raw", f"/apis/metrics.k8s.io/v1beta1/namespaces/{NAMESPACE}/pods"]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(res.stdout)
    except Exception as e:
        print(f"Error fetching metrics: {e}", file=sys.stderr)
        return None

def get_pod_network_egress_anomaly(pod_name):
    # Retrieve packet transmission telemetry via dynamic pod monitoring
    # Mock check: returns True if anomalous egress traffic patterns (DDoS packet spikes) are flagged
    return False

def terminate_pod(pod_name):
    print(f"SECURITY ALARM: Terminating pod {pod_name} due to heuristic rule violations (abuse/crypto-mining/DDoS).")
    try:
        subprocess.run(["kubectl", "delete", "pod", pod_name, "-n", NAMESPACE, "--grace-period=0", "--force"], check=True)
    except Exception as e:
        print(f"Failed to terminate pod {pod_name}: {e}", file=sys.stderr)

def monitor_loop():
    print("Heuristic Kill-Switch daemon started.")
    while True:
        metrics = get_pod_metrics()
        if metrics and "items" in metrics:
            for item in metrics["items"]:
                pod_name = item["metadata"]["name"]
                cpu_sum = 0
                for container in item["containers"]:
                    cpu_str = container["usage"]["cpu"]
                    # Convert e.g. "230000000n" (nanocores) to millicores
                    if cpu_str.endswith("n"):
                        val = int(cpu_str[:-1]) // 1000000
                    elif cpu_str.endswith("u"):
                        val = int(cpu_str[:-1]) // 1000
                    else:
                        val = int(cpu_str)
                    cpu_sum += val
                
                print(f"Pod {pod_name} CPU: {cpu_sum}m / {CPU_THRESHOLD_MILLICORES}m threshold")
                
                # Check 1: CPU spike (Crypto-mining protection)
                if cpu_sum > CPU_THRESHOLD_MILLICORES:
                    terminate_pod(pod_name)
                    continue
                    
                # Check 2: Egress packet thresholds (DDoS protection)
                if get_pod_network_egress_anomaly(pod_name):
                    terminate_pod(pod_name)
                    
        time.sleep(POLL_INTERVAL_SEC)

if __name__ == "__main__":
    try:
        monitor_loop()
    except KeyboardInterrupt:
        print("Daemon stopped by user.")
