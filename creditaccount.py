from account import Account


class CreditAccount(Account):
    """Класс описывающий кредитный лемит счета."""
    def __init__(
            self, account_holder,
            balance: float = 0,
            credit_limit: float = 0
    ):
        super().__init__(account_holder, balance)
        self._credit_limit = float(credit_limit)
        self._balance = float(balance)

        if self._balance < -self._credit_limit:
            raise ValueError(
                f"Начальный баланс ({balance}) не может быть ниже "
                f"-credit_limit (-{self._credit_limit})."
            )

    def _record_operation(self, op_type: str, amount: float, status: str):
        """Записывает операцию, добавляя флаг использования кредита.
        Кредит считается использованным, если успешное снятие привело
        к отрицательному балансу (средства взяты из кредитной линии).
        """
        super()._record_operation(op_type, amount, status)

        credit_used = (
            op_type == "withdraw"
            and status == "success"
            and self._balance < 0
        )
        self.operations_history[-1]["credit_used"] = credit_used

    def get_available_credit(self) -> float:
        """Возвращает доступную сумму (баланс + кредитный лимит).
        По формуле из ТЗ: текущий баланс + кредитный лимит.
        Пример: баланс = -200, лимит = 1000 → доступно 800.
        """
        return self._balance + self._credit_limit

    def withdraw(self, amount: float) -> bool:
        """Снятие средств с учётом кредитного лимита.
        Допускает увод баланса в минус, пока он не ниже -credit_limit.
        """
        try:
            amount = self._validate_amount(amount)
        except (TypeError, ValueError) as e:
            print(f"[Ошибка withdraw] {e}")
            self._record_operation(
                "withdraw",
                amount if isinstance(amount, (int, float)) else 0,
                "fail"
            )
            return False

        available = self._balance + self._credit_limit
        if amount > available:
            self._record_operation("withdraw", amount, "fail")
            print(
                f"Превышен кредитный лимит: запрошено {amount}, "
                f"доступно {available:.2f} "
                f"(баланс {self._balance:.2f}"
                f"лимит {self._credit_limit:.2f})"
            )
            return False

        self._balance -= amount
        self._record_operation("withdraw", amount, "success")
        return True

    def print_history(self):
        """Вывод истории с индикацией использования кредита."""
        if not self.operations_history:
            print("История операций пуста.")
            return
        print(f"История кредитного счёта '{self.holder}' "
              f"(лимит: {self._credit_limit:.2f}):")
        for i, op in enumerate(self.operations_history, 1):
            credit_flag = ""
            if op.get("credit_used"):
                credit_flag = " [кредит]"
            print(
                f"{i:>2}. [{op['datetime'].strftime('%Y-%m-%d %H:%M:%S')}] "
                f"{op['type']:<8} {op['amount']:>10.2f} | "
                f"баланс: {op['balance_after']:>10.2f} | "
                f"{op['status']}{credit_flag}"
            )

    def get_statistics(self) -> dict:
        """Расширенная статистика: добавляет данные по кредиту."""
        stats = super().get_statistics()
        stats["credit_limit"] = self._credit_limit
        stats["available_credit"] = self.get_available_credit()
        stats["credit_in_use"] = max(0, -self._balance)
        return stats
