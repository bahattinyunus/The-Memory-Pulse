import psutil
import time
from typing import Dict, Any

class MemoryPulse:
    """
    The Digital Cortex Monitor.
    Captures the physiological pulse of the system's memory.
    """
    def __init__(self):
        self.history = []

    def get_pulse(self) -> Dict[str, Any]:
        """
        Captures a single snapshot of memory state.
        """
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        timestamp = time.time()
        
        pulse_data = {
            "timestamp": timestamp,
            "ram": {
                "total": mem.total,
                "available": mem.available,
                "percent": mem.percent,
                "used": mem.used,
                "free": mem.free
            },
            "swap": {
                "total": swap.total,
                "used": swap.used,
                "free": swap.free,
                "percent": swap.percent
            }
        }
        
        self.history.append(pulse_data)
        # Keep only last 1000 pulses to avoid memory bloat in the monitor itself
        if len(self.history) > 1000:
            self.history.pop(0)
            
        return pulse_data

    def get_system_bandwidth_proxy(self):
        """
        A proxy for system bandwidth load using disk and net limits.
        Real memory bandwidth requires kernel level drivers, this is a user-mode correlation.
        """
        net = psutil.net_io_counters()
        disk = psutil.disk_io_counters()
        
        return {
            "net_bytes_sent": net.bytes_sent,
            "net_bytes_recv": net.bytes_recv,
            "disk_read_bytes": disk.read_bytes,
            "disk_write_bytes": disk.write_bytes
        }
