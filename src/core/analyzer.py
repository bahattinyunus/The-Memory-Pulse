import numpy as np
from typing import List, Dict, Any

class PulseAnalyzer:
    """
    Analyzes the collected memory pulse data to find anomalies and trends.
    """
    
    @staticmethod
    def analyze_trend(history: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        Simple linear regression to see if memory usage is trending up, down, or stable.
        """
        if len(history) < 2:
            return {"status": "INSUFFICIENT_DATA", "trend": "flat"}
            
        y = np.array([h['ram']['percent'] for h in history])
        x = np.arange(len(y))
        
        # Linear fit (y = mx + c)
        m, _ = np.polyfit(x, y, 1)
        
        if m > 0.05:
            trend = "RISING"
        elif m < -0.05:
            trend = "FALLING"
        else:
            trend = "STABLE"
            
        return {
            "status": "OK", 
            "trend": trend, 
            "slope": f"{m:.4f}"
        }

    @staticmethod
    def detect_anomalies(history: List[Dict[str, Any]], threshold_std: float = 2.0) -> List[Dict[str, Any]]:
        """
        Detects spikes in memory usage that deviate significantly from the mean.
        """
        if len(history) < 10:
            return []
            
        data = np.array([h['ram']['percent'] for h in history])
        mean = np.mean(data)
        std = np.std(data)
        
        anomalies = []
        if std == 0:
            return anomalies

        for i, val in enumerate(data):
            z_score = (val - mean) / std
            if abs(z_score) > threshold_std:
                anomalies.append({
                    "index": i,
                    "value": val,
                    "z_score": z_score,
                    "timestamp": history[i]['timestamp']
                })
        
        return anomalies
