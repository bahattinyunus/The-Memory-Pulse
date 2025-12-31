from typing import Callable, Dict, List, Any
import time

class MemoryEvent:
    def __init__(self, event_type: str, data: Any):
        self.timestamp = time.time()
        self.type = event_type
        self.data = data

class OmniBus:
    """
    The Omni-Bus: A central nervous system for Memory Pulse.
    Handles event propagation between Collectors, Analyzers, and Visualizers.
    """
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[MemoryEvent], None]]] = {}
        self._history: List[MemoryEvent] = []

    def subscribe(self, event_type: str, callback: Callable[[MemoryEvent], None]):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def publish(self, event_type: str, data: Any):
        event = MemoryEvent(event_type, data)
        self._history.append(event)
        
        # Keep history clean
        if len(self._history) > 5000:
            self._history.pop(0)

        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                try:
                    callback(event)
                except Exception as e:
                    print(f"Error in subscriber for {event_type}: {e}")
                    
    def get_recent_events(self, limit: int = 10) -> List[MemoryEvent]:
        return self._history[-limit:]
