from datetime import datetime


class Account:
    """Класс, моделирующий банковский счёт с детальным учётом операций."""

    def __init__(self, account_holder: str, balance: float = 0):
        if balance < 0:
            raise ValueError("Начальный баланс не может быть отрицательным.")
        self.holder = account_holder
        self._balance = float(balance)
        self.operations_history = []

    def _record_operation(self, op_type: str, amount: float, status: str):
        """Добавляет запись об операции в историю."""
        self.operations_history.append({
            "type": op_type,
            "amount": float(amount),
            "datetime": datetime.now(),
            "balance_after": self._balance,
            "status": status,
        })

    @staticmethod
    def _validate_amount(amount):
        """Проверяет, что сумма — положительное число."""
        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise TypeError("Сумма должна быть числом.")
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной.")
        return float(amount)

    # ---------- Основные операции ----------

    def deposit(self, amount: float) -> bool:
        """Пополнение счёта. Возвращает True при успехе."""
        try:
            amount = self._validate_amount(amount)
        except (TypeError, ValueError) as e:
            print(f"[Ошибка deposit] {e}")
            self._record_operation(
                "deposit", amount if isinstance(
                    amount, (int, float)
                ) else 0, "fail"
            )
            return False

        self._balance += amount
        self._record_operation("deposit", amount, "success")
        return True

    def withdraw(self, amount: float) -> bool:
        """Снятие средств. Возвращает True при успехе."""
        try:
            amount = self._validate_amount(amount)
        except (TypeError, ValueError) as e:
            print(f"[Ошибка withdraw] {e}")
            self._record_operation(
                "withdraw", amount if isinstance(
                    amount, (int, float)
                ) else 0, "fail"
            )
            return False

        if amount > self._balance:
            # Недостаточно средств — фиксируем неудачную попытку
            self._record_operation("withdraw", amount, "fail")
            print(
                f"Недостаточно средств:"
                f"запрошено {amount}, доступно {self._balance}"
            )
            return False

        self._balance -= amount
        self._record_operation("withdraw", amount, "success")
        return True

    def get_balance(self) -> float:
        """Возвращает текущий баланс."""
        return self._balance

    def get_history(self):
        """Возвращает копию истории операций."""
        return [dict(op) for op in self.operations_history]

    def get_statistics(self) -> dict:
        """Возвращает сводную статистику по операциям."""
        success = [
            op for op in self.operations_history if op["status"] == "success"
        ]
        failed = [
            op for op in self.operations_history if op["status"] == "fail"
        ]

        total_deposits = sum(
            op["amount"] for op in success if op["type"] == "deposit"
        )
        total_withdrawals = sum(
            op["amount"] for op in success if op["type"] == "withdraw"
        )

        return {
            "total_operations": len(self.operations_history),
            "successful": len(success),
            "failed": len(failed),
            "total_deposits": total_deposits,
            "total_withdrawals": total_withdrawals,
            "current_balance": self._balance,
        }

    def print_history(self):
        """Красивый вывод истории операций в консоль."""
        if not self.operations_history:
            print("История операций пуста.")
            return
        print(f"История операций счёта '{self.holder}':")
        for i, op in enumerate(self.operations_history, 1):
            print(
                f"{i:>2}. [{op['datetime'].strftime('%Y-%m-%d %H:%M:%S')}] "
                f"{op['type']:<8} {op['amount']:>10.2f} | "
                f"баланс: {op['balance_after']:>10.2f} | {op['status']}"
            )