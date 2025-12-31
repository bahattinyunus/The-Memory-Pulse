import psutil
from typing import List, Dict, Any

class MemoryGrid:
    """
    The Memory Grid: Visualizes the memory addressing space as a structured grid.
    Focuses on identifying 'Hot Zones' (processes consuming specific types of memory).
    """
    
    def scan_sector(self) -> List[Dict[str, Any]]:
        """
        Scans all running processes to map their memory footprint (RSS, VMS).
        Effectively creates a heatmap of memory usage.
        """
        grid_data = []
        
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                mem_info = proc.info['memory_info']
                grid_data.append({
                    "pid": proc.info['pid'],
                    "name": proc.info['name'],
                    "rss": mem_info.rss,     # Resident Set Size (Physical Memory)
                    "vms": mem_info.vms,     # Virtual Memory Size
                    "heat_score": self._calculate_heat(mem_info.rss)
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        # Sort by heat score (descending)
        grid_data.sort(key=lambda x: x['rss'], reverse=True)
        return grid_data[:20]  # Return top 20 hottest sectors

    def _calculate_heat(self, rss_bytes: int) -> float:
        """
        Calculates a normalized 'heat' score (0.0 to 1.0) based on typical extensive usage.
        Assume 4GB is 'Critical Heat' for a single process for now.
        """
        CRITICAL_THRESHOLD = 4 * 1024 * 1024 * 1024  # 4 GB
        return min(rss_bytes / CRITICAL_THRESHOLD, 1.0)
