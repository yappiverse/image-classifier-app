import psutil  # For system resource monitoring
from fastapi import APIRouter

router = APIRouter()

@router.get("/health/")
def health_check():
    """Health check endpoint with system resource usage."""
    
    # Get system stats
    cpu_usage = psutil.cpu_percent(interval=1)  # CPU usage (%)
    ram = psutil.virtual_memory()  # RAM details
    disk = psutil.disk_usage("/")  # Disk usage
    
    return {
        "status": "healthy",
        "cpu_usage": f"{cpu_usage}%",
        "ram_usage": f"{ram.percent}%",
        "available_ram": f"{ram.available / (1024**3):.2f} GB",
        "total_ram": f"{ram.total / (1024**3):.2f} GB",
        "disk_usage": f"{disk.percent}%",
        "available_disk": f"{disk.free / (1024**3):.2f} GB",
        "total_disk": f"{disk.total / (1024**3):.2f} GB",
    }