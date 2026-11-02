from account import Account
from creditaccount import CreditAccount


def main():
    #дописать ввод параметров для проверки
    pass


if __name__ == "__main__":
    acc = Account("Иван Иванов", 100)

    acc.deposit(50)
    acc.withdraw(30)
    acc.withdraw(500)   # неудачная попытка — не хватает средств
    acc.deposit(-10)    # неудачная попытка — отрицательная сумма

    print(f"\nТекущий баланс: {acc.get_balance()}")
    print()

    acc.print_history()

    print("\nСтатистика:")
    for k, v in acc.get_statistics().items():
        print(f"  {k}: {v}")
