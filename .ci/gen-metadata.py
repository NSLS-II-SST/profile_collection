import os
from pprint import pprint

from bluesky.utils import PersistentDict

md_path = os.environ.get("RE_METADATA")
if not md_path:
    raise RuntimeError("Env. variable 'RE_METADATA' is not defined or empty.")

md = PersistentDict(md_path)

keys = [
    "institution",
    "project_desc",
    "project_name",
    "proposal_id",
    "saf_id",
    "user_id",
    "user_name",
    "user_start_date",
]

for k in keys:
    md[k] = f"test_{k}"
md["user_email"] = ""

print(f"Metadata dir: {md.directory}")
print(f"Repr: {md.__repr__()}")
pprint(dict(md))
