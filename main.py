from datetime import date

from expense_app.exceptions import ExpenseError
from expense_app.logger import logger
from expense_app.manager import ExpenseManager


def _add_expense(manager: ExpenseManager) -> None:
    amount = float(input("Amount: "))
    category = input("Category: ").strip()
    description = input("Description: ").strip()
    expense_date = input("Date (YYYY-MM-DD, blank for today): ").strip()
    expense_date = expense_date or date.today().isoformat()

    expense = manager.add_expense(amount, category, description, expense_date)
    print(f"Added expense #{expense.id}.")


def _view_expenses(manager: ExpenseManager) -> None:
    expenses = manager.list_expenses()
    if not expenses:
        print("No expenses found.")
        return

    print("ID | Date       | Category       | Amount   | Description")
    for expense in expenses:
        print(
            f"{expense.id:<2} | {expense.date:<10} | {expense.category:<14} | "
            f"{expense.amount:>8.2f} | {expense.description}"
        )


def _update_expense(manager: ExpenseManager) -> None:
    expense_id = int(input("Expense ID: "))
    changes: dict[str, str | float] = {}

    amount = input("New amount (blank to keep current): ").strip()
    category = input("New category (blank to keep current): ").strip()
    description = input("New description (blank to keep current): ").strip()
    expense_date = input("New date (blank to keep current): ").strip()

    if amount:
        changes["amount"] = float(amount)
    if category:
        changes["category"] = category
    if description:
        changes["description"] = description
    if expense_date:
        changes["date"] = expense_date

    if not changes:
        print("No changes provided.")
        return

    manager.update_expense(expense_id, **changes)
    print(f"Updated expense #{expense_id}.")


def _delete_expense(manager: ExpenseManager) -> None:
    expense_id = int(input("Expense ID: "))
    manager.delete_expense(expense_id)
    print(f"Deleted expense #{expense_id}.")


def main() -> None:
    manager = ExpenseManager()
    logger.info("Expense tracker CLI started")

    try:
        while True:
            print("\nPersonal Expense Tracker")
            print("1. Add expense")
            print("2. View expenses")
            print("3. Update expense")
            print("4. Delete expense")
            print("5. Exit")
            choice = input("Choose an option: ").strip()

            if choice == "5":
                break

            try:
                if choice == "1":
                    _add_expense(manager)
                elif choice == "2":
                    _view_expenses(manager)
                elif choice == "3":
                    _update_expense(manager)
                elif choice == "4":
                    _delete_expense(manager)
                else:
                    logger.error("Invalid menu option: %s", choice)
                    print("Please choose an option from 1 to 5.")
            except (ExpenseError, RuntimeError, ValueError) as error:
                logger.error("Expense operation failed: %s", error)
                print(f"Error: {error}")
            except Exception:
                logger.exception("Unexpected error during an expense operation")
                print("An unexpected error occurred. See expense_tracker.log.")
            finally:
                logger.info("CLI operation finished")
    except (EOFError, KeyboardInterrupt):
        print("\nExiting the expense tracker.")
        logger.info("CLI input interrupted")
    finally:
        logger.info("Application exited")


if __name__ == "__main__":
    main()
