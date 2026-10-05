from dataclasses import dataclass


@dataclass
class Expense:
    id: int
    amount: float
    category: str
    description: str
    date: str
