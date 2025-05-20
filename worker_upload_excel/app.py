
import streamlit as st
import pandas as pd
import uuid
from action.get_data_from_excel import get_data_from_excel
from action.create_title_for_links import get_title_for_links
from action.get_processed_array import get_processed_array
from action.make_script_data import make_script_data
from action.get_analysis import get_analysis
from action.set_api_key import set_api_key
from action.set_api_key import clear_api_key
from action.fetch_api_key import fetch_api_key,clear_api_key_db,set_api_key_db
from action.connect_to_db import connect_to_db
from action.redis_queue import RedisQueue
import time

seo_tasks_queue = RedisQueue("upload_excel")


def process_upload_link(url,inserted_id):
    link_title =  get_title_for_links(url)
    processed_item = get_processed_array(link_title)
    processed_item = make_script_data(processed_item)
    res = get_analysis(processed_item,inserted_id)
    print(f"Analysis completed for {url}")
    
def process_seo_task(task_data):
    """Process an SEO task (example function)"""
    print(f"Processing SEO analysis for {task_data['url']}")
    process_upload_link(task_data["url"],task_data["inserted_id"])
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