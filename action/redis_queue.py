import json
import os
import time
import redis
from typing import Dict, Any, Optional, List, Callable

class RedisQueue:
    """Simple Redis Queue implementation for SEO tasks"""
    
    def __init__(self, queue_name: str, host: str = None, port: int = None):
        """Initialize Redis queue"""
        self.queue_name = queue_name
        self.host = host or os.environ.get('REDIS_HOST', 'redis')
        self.port = port or int(os.environ.get('REDIS_PORT', 6379))
        self.redis_client = redis.Redis(
            host=self.host,
            port=self.port,
            decode_responses=True  # Auto-decode byte responses to strings
        )
    
    def enqueue(self, data: Dict[str, Any]) -> bool:
        """Add task to the queue"""
        try:
            # Convert dictionary to JSON string
            json_data = json.dumps(data)
            # Use RPUSH to add to the end of the list
            self.redis_client.rpush(self.queue_name, json_data)
            return True
        except Exception as e:
            print(f"Error enqueueing task: {e}")
            return False
    
    def dequeue(self, timeout: int = 0) -> Optional[Dict[str, Any]]:
        """Remove and return task from queue
        
        Args:
            timeout: Time in seconds to wait for an item (0 = indefinite)
        """
        try:
            # Use BLPOP to remove from the beginning of the list with blocking
            result = self.redis_client.blpop(self.queue_name, timeout)
            if result:
                # BLPOP returns [queue_name, item]
                _, json_data = result
                return json.loads(json_data)
            return None
        except Exception as e:
            print(f"Error dequeueing task: {e}")
            return None
    
    def peek(self) -> Optional[Dict[str, Any]]:
        """View the first task without removing it"""
        try:
            json_data = self.redis_client.lindex(self.queue_name, 0)
            if json_data:
                return json.loads(json_data)
            return None
        except Exception as e:
            print(f"Error peeking at task: {e}")
            return None
    
    def queue_size(self) -> int:
        """Return the number of items in the queue"""
        return self.redis_client.llen(self.queue_name)
    
    def clear_queue(self) -> bool:
        """Clear all items from the queue"""
        try:
            self.redis_client.delete(self.queue_name)
            return True
        except Exception as e:
            print(f"Error clearing queue: {e}")
            return False