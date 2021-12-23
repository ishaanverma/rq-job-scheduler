import time
from collections import defaultdict


def call_endpoint(params=defaultdict(str)):
  print(f"hello {params['name']}")
  time.sleep(10)

  return f"hello {params['name']}"

if __name__ == "__main__":
  print(call_endpoint())