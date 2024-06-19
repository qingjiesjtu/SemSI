import os
import time

def proxy_on():
    os.environ["http_proxy"] = "http://127.0.0.1:7890"
    os.environ["https_proxy"] = "http://127.0.0.1:7890"

def proxy_off():
    if "http_proxy" in os.environ:
        del os.environ["http_proxy"]
    if "https_proxy" in os.environ:
        del os.environ["https_proxy"]
import argparse


def get_opts():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, default='gpt-4o')
    parser.add_argument('--source_file', type=str, default='realNews')
    parser.add_argument('--question', type=str, default='Why ', choices=['Why ', 'How '])
    parser.add_argument('--datafilename', type=str, default="")

    opts = parser.parse_args()
    return opts

def run_with_retry(func, *args, retry_delay=10, **kwargs):
    retries = 0
    while True:
        try:
            func(*args, **kwargs)
            break  
        except Exception as e:
            retries += 1
            print(f"Error occurred: {e}. Retrying {retries}...")
            time.sleep(retry_delay)  