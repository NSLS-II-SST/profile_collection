import os
import re
from pprint import pprint

from bluesky.utils import PersistentDict

md_path = os.environ.get("RE_METADATA")
if not md_path:
    raise RuntimeError("Env. variable 'RE_METADATA' is not defined or empty.")

# Get all keys based on the RE.md occurrences in the module.
md_keys = set()
with open("startup/SST/RSoXS/Functions/alignment.py") as f:
    lines = f.readlines()

for line in lines:
    if re.search(r"=\s*RE.md", line):
        # Parsing lines such as:
        # sample_state = RE.md['sample_state']
        # proposal_id=RE.md['proposal_id'],
        key = line.split("=")[-1].strip().split("'")[1]
        md_keys.add(key)
    elif re.search(r"RE.md\S+\s*=", line):
        # Parsing lines such as:
        # RE.md['project_name'] = project_name
        key = line.split("=")[0].strip().split("'")[1]
        md_keys.add(key)
md_keys = sorted(list(md_keys))

md = PersistentDict(md_path)

# Add the keys to the metadata dict with fake values:
for k in md_keys:
    md[k] = f"test_{k}"

# Special cases:
md["bar_loc"] = {"spot": 0, "th": 0}

print(f"Metadata dir: {md.directory}")
print(f"Repr: {md.__repr__()}")
pprint(dict(md))
