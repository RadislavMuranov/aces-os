"""In-memory + file-backed store for reconstructible records."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any, Optional, List

class RecordStore:
    def __init__(self, root: str):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        for sub in ["evidence", "admissibility", "verification", "acceptance", "accepted_state", "authority", "policy"]:
            (self.root / sub).mkdir(exist_ok=True)
        self._index: Dict[str, str] = {}

    def _write(self, subdir: str, obj_id: str, data: Dict[str, Any]) -> str:
        path = self.root / subdir / f"{obj_id}.json"
        path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
        rel = f"{subdir}/{obj_id}.json"
        self._index[obj_id] = rel
        return str(path)

    def put(self, kind: str, obj_id: str, data: Dict[str, Any]) -> str:
        return self._write(kind, obj_id, data)

    def get(self, obj_id: str) -> Optional[Dict[str, Any]]:
        rel = self._index.get(obj_id)
        if not rel:
            for sub in ["evidence", "admissibility", "verification", "acceptance", "accepted_state", "authority", "policy"]:
                p = self.root / sub / f"{obj_id}.json"
                if p.exists():
                    return json.loads(p.read_text(encoding="utf-8"))
            return None
        p = self.root / rel
        if not p.exists():
            return None
        return json.loads(p.read_text(encoding="utf-8"))

    def list_ids(self, kind: str) -> List[str]:
        d = self.root / kind
        if not d.exists():
            return []
        return [p.stem for p in d.glob("*.json")]

    def dump_index(self) -> Dict[str, str]:
        return dict(self._index)
