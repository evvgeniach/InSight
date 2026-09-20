import os
import json
import shutil
from datetime import datetime
import pandas as pd

WORKSPACE_DIR = "workspaces"


def list_workspaces() -> list[dict]:
    if not os.path.exists(WORKSPACE_DIR):
        return []
    result = []
    for name in sorted(os.listdir(WORKSPACE_DIR)):
        meta_path = os.path.join(WORKSPACE_DIR, name, "metadata.json")
        if os.path.exists(meta_path):
            with open(meta_path) as f:
                result.append(json.load(f))
    return result


def save_workspace(name: str, datasets: dict, messages: list) -> None:
    path = os.path.join(WORKSPACE_DIR, name)
    os.makedirs(path, exist_ok=True)

    data_dir = os.path.join(path, "data")
    os.makedirs(data_dir, exist_ok=True)

    dataset_files = {}
    for key, df in datasets.items():
        safe = key.replace("/", "_").replace("\\", "_").replace(" ", "_")
        csv_path = os.path.join(data_dir, f"{safe}.csv")
        df.to_csv(csv_path, index=False)
        dataset_files[key] = f"data/{safe}.csv"

    with open(os.path.join(path, "conversation.json"), "w") as f:
        json.dump(messages, f, indent=2)

    with open(os.path.join(path, "metadata.json"), "w") as f:
        json.dump({
            "name": name,
            "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "datasets": dataset_files,
            "message_count": len(messages),
        }, f, indent=2)


def load_workspace(name: str) -> tuple[dict, list, dict]:
    path = os.path.join(WORKSPACE_DIR, name)

    with open(os.path.join(path, "metadata.json")) as f:
        meta = json.load(f)

    datasets = {}
    for key, rel_path in meta["datasets"].items():
        datasets[key] = pd.read_csv(os.path.join(path, rel_path))

    with open(os.path.join(path, "conversation.json")) as f:
        messages = json.load(f)

    return datasets, messages, meta


def delete_workspace(name: str) -> None:
    path = os.path.join(WORKSPACE_DIR, name)
    if os.path.exists(path):
        shutil.rmtree(path)
