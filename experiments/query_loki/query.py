import requests
import json
from datetime import datetime, timedelta
import urllib.parse
from rich import print as rprint
from typing import Optional

def query_loki_logs(
    query: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = 100
) -> dict:
    """Query Loki logs for given parameters"""
    
    # Default to last 1 hour if no time range specified
    if not end_time:
        end_time = datetime.now()
    if not start_time:
        start_time = end_time - timedelta(hours=1)

    # Convert to Unix nanoseconds
    start_ns = int(start_time.timestamp() * 1e9)
    end_ns = int(end_time.timestamp() * 1e9)

    params = {
        'query': query,
        'start': start_ns,
        'end': end_ns,
        'limit': limit,
    }

    url = f"http://localhost:8080/loki/api/v1/query_range"
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        rprint(f"[red]Error querying Loki: {e}[/red]")
        return None

def get_pod_logs_by_stream(
    namespace: str = "dev",
    hours: int = 1,
    streams: list[str] = ["stdout", "stderr"]
):
    """Get logs for specific streams from all pods in namespace"""
    
    # Build stream matcher
    stream_selector = '|'.join(streams)
    query = f'{{namespace="{namespace}", stream=~"({stream_selector})"}}'
    
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours)
    
    results = query_loki_logs(query, start_time, end_time)
    
    if results and results.get('status') == 'success':
        for stream in results['data']['result']:
            pod_name = stream['stream'].get('pod', 'unknown')
            stream_type = stream['stream'].get('stream', 'unknown')
            rprint(f"[cyan]Pod: {pod_name} ({stream_type})[/cyan]")
            for timestamp, log in stream['values']:
                dt = datetime.fromtimestamp(int(timestamp) / 1e9)
                rprint(f"[grey]{dt}[/grey]: {log}")
            print()

if __name__ == "__main__":
    get_pod_logs_by_stream(namespace="dev", hours=1, streams=["stderr", "stdout"])