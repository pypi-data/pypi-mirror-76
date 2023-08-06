import json
import os
from pathlib import Path

EXEC_DIR = Path(os.path.dirname(os.path.realpath(__file__)))

f = EXEC_DIR / "data" / "lookups.json"
lookups = json.loads(f.read_text())
actorlookup: dict = {}
for hash, value in lookups["actorlookup"].items():
    actorlookup[int(hash)] = value
taglookup: dict = {}
for hash, value in lookups["taglookup"].items():
    taglookup[int(hash)] = value
