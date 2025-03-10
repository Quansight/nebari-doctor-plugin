import pathlib
from get_pod_logs import get_nebari_pod_logs_tool

def main():
    """Test the get_nebari_pod_logs_tool function with a specific pod."""
    pod_name = "nebari-grafana-74874bd867-67t7c"
    # Get logs for the last 10 minutes by default
    logs = get_nebari_pod_logs_tool(pod_names=[pod_name])
    
    print(f"Logs for {pod_name}:")
    print("=" * 50)
    print(logs)
    print("=" * 50)

if __name__ == "__main__":
    main()
