import base64
import json
import re
from pathlib import Path

path = Path("Scenario 2/runtime-data.js")
source = path.read_text(encoding="utf-8")

match = re.fullmatch(
    r'__jsonp\("runtime-data.js","([A-Za-z0-9+/=]+)"\);?\s*',
    source,
)
if not match:
    raise SystemExit("Unexpected runtime-data.js format; file was not changed.")

payload = base64.b64decode(match.group(1)).decode("utf-8")
json.loads(payload)

old_text = (
    "Tests whether the learner respects community autonomy and consent when a Nation "
    "declines participation or identifies other priorities, rather than continuing to "
    "push the initiative or assuming the work can proceed independently."
)
new_text = (
    "Respect community autonomy by stepping back when a Nation declines participation "
    "or shifts priorities."
)

if payload.count(old_text) != 1:
    raise SystemExit(
        "Expected to find the original goal exactly once; file was not changed."
    )

payload = payload.replace(old_text, new_text, 1)
json.loads(payload)

encoded = base64.b64encode(payload.encode("utf-8")).decode("ascii")
path.write_text(source.replace(match.group(1), encoded, 1), encoding="utf-8")
print(f"Updated {path}")
