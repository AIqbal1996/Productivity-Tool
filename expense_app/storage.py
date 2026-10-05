import json
from dataclasses import asdict
from pathlib import Path
from typing import TextIO

from .models import Expense


DEFAULT_STORAGE_FILE = Path("expenses.json")


def load_expenses(file_path: str | Path = DEFAULT_STORAGE_FILE) -> list[Expense]:
    path = Path(file_path)
    stream: TextIO | None = None

    try:
        try:
            stream = path.open("r", encoding="utf-8")
        except FileNotFoundError:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", encoding="utf-8") as new_file:
                json.dump([], new_file)
            return []

        records = json.load(stream)
        if not isinstance(records, list):
            raise ValueError("The expense data must be a JSON list.")
        return [Expense(**record) for record in records]
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as error:
        raise RuntimeError(f"Could not load expenses from {path}.") from error
    finally:
        if stream is not None:
            stream.close()


def save_expenses(
    expenses: list[Expense], file_path: str | Path = DEFAULT_STORAGE_FILE
) -> None:
    path = Path(file_path)
    stream: TextIO | None = None

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        stream = path.open("w", encoding="utf-8")
        json.dump([asdict(expense) for expense in expenses], stream, indent=2)
        stream.write("\n")
    except (OSError, TypeError, ValueError) as error:
        raise RuntimeError(f"Could not save expenses to {path}.") from error
    finally:
        if stream is not None:
            stream.close()
