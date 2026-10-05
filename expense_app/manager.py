import math
from pathlib import Path
from typing import NoReturn

from . import storage
from .exceptions import ExpenseError
from .logger import logger
from .models import Expense


def _raise_error(message: str) -> NoReturn:
    logger.error(message)
    raise ExpenseError(message)


def _load_expenses(file_path: str | Path) -> list[Expense]:
    try:
        return storage.load_expenses(file_path)
    except RuntimeError:
        logger.exception("Could not load expenses.")
        raise


def _save_expenses(expenses: list[Expense], file_path: str | Path) -> None:
    try:
        storage.save_expenses(expenses, file_path)
    except RuntimeError:
        logger.exception("Could not save expenses.")
        raise


def _validate_amount(amount: int | float) -> None:
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        _raise_error("Amount must be a number greater than zero.")
    if not math.isfinite(amount) or amount <= 0:
        _raise_error("Amount must be a finite number greater than zero.")


def _validate_text(value: str, field_name: str, allow_empty: bool = False) -> None:
    if not isinstance(value, str):
        _raise_error(f"{field_name} must be text.")
    if not allow_empty and not value.strip():
        _raise_error(f"{field_name} cannot be empty.")


def add_expense(
    amount: int | float,
    category: str,
    description: str,
    date: str,
    file_path: str | Path = storage.DEFAULT_STORAGE_FILE,
) -> Expense:
    _validate_amount(amount)
    _validate_text(category, "Category")
    _validate_text(description, "Description", allow_empty=True)
    _validate_text(date, "Date")

    expenses = _load_expenses(file_path)
    expense = Expense(
        id=max((item.id for item in expenses), default=0) + 1,
        amount=float(amount),
        category=category.strip(),
        description=description,
        date=date.strip(),
    )
    expenses.append(expense)
    _save_expenses(expenses, file_path)
    logger.info("Expense added: id=%s", expense.id)
    return expense


def list_expenses(file_path: str | Path = storage.DEFAULT_STORAGE_FILE) -> list[Expense]:
    return _load_expenses(file_path)


def update_expense(
    expense_id: int,
    amount: int | float | None = None,
    category: str | None = None,
    description: str | None = None,
    date: str | None = None,
    file_path: str | Path = storage.DEFAULT_STORAGE_FILE,
) -> Expense:
    if amount is not None:
        _validate_amount(amount)
    if category is not None:
        _validate_text(category, "Category")
    if description is not None:
        _validate_text(description, "Description", allow_empty=True)
    if date is not None:
        _validate_text(date, "Date")

    expenses = _load_expenses(file_path)
    expense = next((item for item in expenses if item.id == expense_id), None)
    if expense is None:
        _raise_error(f"Expense {expense_id} was not found.")

    if amount is not None:
        expense.amount = float(amount)
    if category is not None:
        expense.category = category.strip()
    if description is not None:
        expense.description = description
    if date is not None:
        expense.date = date.strip()

    _save_expenses(expenses, file_path)
    logger.info("Expense updated: id=%s", expense.id)
    return expense


def delete_expense(
    expense_id: int, file_path: str | Path = storage.DEFAULT_STORAGE_FILE
) -> None:
    expenses = _load_expenses(file_path)
    remaining_expenses = [item for item in expenses if item.id != expense_id]
    if len(remaining_expenses) == len(expenses):
        _raise_error(f"Expense {expense_id} was not found.")
    _save_expenses(remaining_expenses, file_path)
    logger.info("Expense deleted: id=%s", expense_id)


class ExpenseManager:
    def __init__(self, file_path: str | Path = storage.DEFAULT_STORAGE_FILE) -> None:
        self.file_path = file_path

    def add_expense(
        self, amount: int | float, category: str, description: str, date: str
    ) -> Expense:
        return add_expense(amount, category, description, date, self.file_path)

    def list_expenses(self) -> list[Expense]:
        return list_expenses(self.file_path)

    def update_expense(
        self,
        expense_id: int,
        amount: int | float | None = None,
        category: str | None = None,
        description: str | None = None,
        date: str | None = None,
    ) -> Expense:
        return update_expense(
            expense_id,
            amount=amount,
            category=category,
            description=description,
            date=date,
            file_path=self.file_path,
        )

    def delete_expense(self, expense_id: int) -> None:
        delete_expense(expense_id, self.file_path)
