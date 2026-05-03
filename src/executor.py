import io
import contextlib
import threading
import pandas as pd
import numpy as np


def run_python(code: str, df: pd.DataFrame, datasets: dict = None) -> str:
    """Execute pandas code with df (and optionally datasets) in scope.

    Uses a background thread so execution can be interrupted after 10 seconds.
    """
    output = io.StringIO()
    namespace = {"df": df, "pd": pd, "np": np, "result": None}
    if datasets:
        namespace["datasets"] = datasets

    error_box: list = []

    def _target():
        try:
            with contextlib.redirect_stdout(output):
                exec(compile(code, "<string>", "exec"), namespace)  # noqa: S102
        except Exception as exc:
            error_box.append(exc)

    thread = threading.Thread(target=_target, daemon=True)
    thread.start()
    thread.join(timeout=10)

    if thread.is_alive():
        return "Error: code execution timed out (10 s limit)."
    if error_box:
        return f"Error: {error_box[0]}"

    text = output.getvalue().strip()
    if not text and namespace.get("result") is not None:
        text = str(namespace["result"])
    return text or "(no output)"
