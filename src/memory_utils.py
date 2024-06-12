import os
import gc
import psutil
import tracemalloc
from logger import logger

def run_cleanup():
    gc.collect()
    logger.info("Garbage collection completed.")

def start_memory_trace():
    tracemalloc.start()
    log_memory_usage()

def stop_memory_trace():
    log_memory_usage()
    current, peak = tracemalloc.get_traced_memory()
    logger.info(f"Current memory usage: {current / 1024 / 1024:.2f} MB")
    logger.info(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")
    tracemalloc.stop()

def log_memory_usage():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    logger.info(f"RSS: {mem_info.rss / 1024 / 1024:.2f} MB; VMS: {mem_info.vms / 1024 / 1024:.2f} MB")


# # Example Usage:
# import memory_utils

# if __name__ == "__main__":
#     # Start memory trace
#     memory_utils.start_memory_trace()

#     # Your main code here

#     # Stop memory trace
#     memory_utils.stop_memory_trace()