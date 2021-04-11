import json
import os
from utils import dbStatus


def load():
  try:
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "videos.json")) as f:
      data = json.load(f)
      dbStatus(data)
      return data
  except Exception:
    return {}


def save(data):
  with open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "videos.json"), "w") as f:
    json.dump(data, f, sort_keys=True, indent=2)
    print("Database saved")


if __name__ == "__main__":
  load()
