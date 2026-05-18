import json
import os
from datetime import datetime

VARIABLES_DIR = os.path.join(os.path.dirname(__file__), "..", "variables")


def load_all() -> dict:

    variables = {}

    if not os.path.isdir(VARIABLES_DIR):
        return variables

    for filename in sorted(os.listdir(VARIABLES_DIR)):
        if not filename.endswith(".json"):
            continue

        name = filename[:-5]  # strip .json
        path = os.path.join(VARIABLES_DIR, filename)

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            variables[name] = data
        except Exception as e:
            variables[name] = {"value": f"[read error: {e}]", "refreshed_at": None}

    return variables


def get_variables_context() -> str:

    variables = load_all()

    if not variables:
        return ""

    lines = ["[Live Variables — refreshed at startup]"]

    for name, entry in variables.items():
        value = entry.get("value", "unknown")

        if isinstance(value, dict):
            parts = []
            if value.get("os"):
                parts.append(f"OS={value['os']}")
            if value.get("architecture"):
                parts.append(f"arch={value['architecture']}")
            if value.get("cpu_count"):
                parts.append(f"CPU={value['cpu_count']}")
            if value.get("disk") and isinstance(value["disk"], dict):
                parts.append(f"disk {value['disk'].get('free_gb', '?')} GB free")
            value = ", ".join(parts) if parts else str(value)

        lines.append(f"  • {name:<14}: {value}")

    return "\n".join(lines)


def get_variable(name: str):

    variables = load_all()
    entry = variables.get(name)
    return entry["value"] if entry else None