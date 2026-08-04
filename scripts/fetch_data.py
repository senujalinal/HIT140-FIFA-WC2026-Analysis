from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen


SOURCE = "https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"
EXPECTED_SHA256 = "0ae2c18109b5aa86bc11928b43586ca430c234804d5bbf808d2c3bf2051ecfca"
DESTINATION = Path(__file__).resolve().parents[1] / "data" / "raw" / "worldcup_2026.json"


def main() -> None:
    request = Request(SOURCE, headers={"User-Agent": "HIT140-course-project/1.0"})
    with urlopen(request, timeout=30) as response:
        raw = response.read()

    payload = json.loads(raw)
    matches = payload.get("matches", [])
    if len(matches) != 104:
        raise ValueError(f"Expected 104 matches; received {len(matches)}")
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError(
            "The upstream dataset changed. Review the changes and update the recorded hash before replacing the snapshot."
        )

    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_bytes(raw)
    print(f"Saved {len(matches)} validated matches to {DESTINATION}")


if __name__ == "__main__":
    main()
