import os
import re
from pprint import pprint

from bluesky.utils import PersistentDict

md_path = os.environ.get("RE_METADATA")
if not md_path:
    raise RuntimeError("Env. variable 'RE_METADATA' is not defined or empty.")

# Get all keys based on the RE.md occurrences in the module.
md_keys = []
with open("startup/90b-samples_users.py") as f:
    lines = f.readlines()

    for line in lines:
        if re.search(r"=\s*RE.md", line):
            # Parsing lines such as:
            # ...
            # sample_state = RE.md['sample_state']
            # ...
            # proposal_id=RE.md['proposal_id'],
            # ...
            key = line.split("=")[-1].strip().split("'")[1]
            md_keys.append(key)
    md_keys.append("user_email")  # not captured by the code above
    md_keys.sort()

md = PersistentDict(md_path)

# Add the keys to the metadata dict with fake values:
for k in md_keys:
    md[k] = f"test_{k}"

print(f"Metadata dir: {md.directory}")
print(f"Repr: {md.__repr__()}")
pprint(dict(md))
