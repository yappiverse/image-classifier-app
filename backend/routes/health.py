import psutil
import time
from fastapi import APIRouter

router = APIRouter()

@router.get("/health/")
def health_check():
    """Health check endpoint with system resource usage."""
    
    # Get system stats
    cpu_usage = psutil.cpu_percent(interval=0) 
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    load_avg = psutil.getloadavg() if hasattr(psutil, "getloadavg") else (0, 0, 0)
    uptime = time.time() - psutil.boot_time()
    
    is_healthy = cpu_usage < 90 and ram.percent < 90 and disk.percent < 90
    status = "healthy" if is_healthy else "unhealthy"
    
    return {
        "status": status,
        "cpu_usage": f"{cpu_usage}%",
        "ram_usage": f"{ram.percent}%",
        "available_ram": f"{ram.available / (1024**3):.2f} GB",
        "total_ram": f"{ram.total / (1024**3):.2f} GB",
        "disk_usage": f"{disk.percent}%",
        "available_disk": f"{disk.free / (1024**3):.2f} GB",
        "total_disk": f"{disk.total / (1024**3):.2f} GB",
        "load_average": {
            "1m": f"{load_avg[0]:.2f}",
            "5m": f"{load_avg[1]:.2f}",
            "15m": f"{load_avg[2]:.2f}"
        },
        "uptime": f"{uptime / 3600:.2f} hours"
    }