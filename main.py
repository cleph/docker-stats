from fastapi import FastAPI
import docker
import time

app = FastAPI()
client = docker.from_env()

def convert_to_megabytes(value):
    """Convert bytes to megabytes."""
    return round(value / (1024 * 1024), 2)

def calculate_cpu_percentage(stats):
    """Calculate the CPU usage percentage."""
    try:
        cpu_stats = stats['cpu_stats']
        precpu_stats = stats['precpu_stats']

        # Ensure 'precpu_stats' is not empty
        if not precpu_stats or 'cpu_usage' not in precpu_stats:
            return 0.0

        cpu_delta = cpu_stats['cpu_usage']['total_usage'] - precpu_stats['cpu_usage']['total_usage']
        system_delta = cpu_stats['system_cpu_usage'] - precpu_stats['system_cpu_usage']

        if system_delta > 0 and cpu_delta > 0:
            cpu_percent = (cpu_delta / system_delta) * len(cpu_stats['cpu_usage'].get('percpu_usage', [])) * 100
            return round(cpu_percent, 2)
        else:
            return 0.0
    except KeyError as e:
        print(f"KeyError: {e}")
        return 0.0

@app.get("/docker-stats")
async def get_docker_stats():
    containers = client.containers.list()
    stats = []

    for container in containers:
        # Fetch stats
        stats_data = container.stats(stream=False)

        # Calculate CPU percentage
        cpu_percent = calculate_cpu_percentage(stats_data)

        # Memory usage
        mem_usage = stats_data['memory_stats'].get('usage', 0)
        mem_limit = stats_data['memory_stats'].get('limit', 1)  # Avoid division by zero
        mem_usage_mb = convert_to_megabytes(mem_usage)
        mem_limit_mb = convert_to_megabytes(mem_limit)
        mem_percent = round((mem_usage / mem_limit) * 100, 2) if mem_limit > 0 else 0.0

        # Network I/O
        net_io = stats_data.get('networks', {})
        net_rx = sum(interface.get('rx_bytes', 0) for interface in net_io.values())
        net_tx = sum(interface.get('tx_bytes', 0) for interface in net_io.values())
        net_rx_mb = convert_to_megabytes(net_rx)
        net_tx_mb = convert_to_megabytes(net_tx)

        # Block I/O
        blkio_stats = stats_data.get('blkio_stats', {}).get('io_service_bytes_recursive', [])
        blk_read = sum(entry.get('value', 0) for entry in blkio_stats if entry.get('op') == 'Read')
        blk_write = sum(entry.get('value', 0) for entry in blkio_stats if entry.get('op') == 'Write')
        blk_read_mb = convert_to_megabytes(blk_read)
        blk_write_mb = convert_to_megabytes(blk_write)

        # PIDs
        pids = stats_data.get('pids_stats', {}).get('current', 0)

        stats.append({
            'container_id': container.id,
            'name': container.name,
            'cpu_percent': cpu_percent,
            'mem_usage_mb': mem_usage_mb,
            'mem_limit_mb': mem_limit_mb,
            'mem_percent': mem_percent,
            'net_rx_mb': net_rx_mb,
            'net_tx_mb': net_tx_mb,
            'blk_read_mb': blk_read_mb,
            'blk_write_mb': blk_write_mb,
            'pids': pids
        })

    return {'containers': stats}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
