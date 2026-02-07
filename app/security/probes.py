# app/security/probes.py

import json
from dataclasses import dataclass
from typing import List

@dataclass
class Probe:
    id: str
    text: str
    expected_allowed: bool

def load_probes_jsonl(path: str) -> List[Probe]:
    probes: List[Probe] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            probes.append(Probe(
                id=str(obj["id"]),
                text=str(obj["text"]),
                expected_allowed=bool(obj["expected_allowed"])
            ))
    return probes
