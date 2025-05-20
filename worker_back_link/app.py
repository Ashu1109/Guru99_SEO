from action.redis_queue import RedisQueue
from Back_Link import get_data
import time

seo_tasks_queue = RedisQueue("seo_tasks")

def process_seo_task(task_data):
    """Process an SEO task (example function)"""
    print(f"Processing SEO analysis for {task_data['url']}")
    get_data(task_data["url"])
    return {"status": "completed", "url": task_data["url"]}




def run_worker():
    """Run a worker process that processes tasks from the queue"""
    print("Starting SEO analysis worker...")
    while True:
        # Block until a task is available
        task = seo_tasks_queue.dequeue(timeout=0)  # 0 means block indefinitely
        
        if task:
            print(f"Received task: {task}")
            try:
                result = process_seo_task(task)
                print(f"Task completed: {result}")
            except Exception as e:
                print(f"Error processing task: {e}")
        else:
            print("No task available or error occurred")
            time.sleep(1)  # Prevent CPU spinning



if __name__ == "__main__":
    run_worker()
