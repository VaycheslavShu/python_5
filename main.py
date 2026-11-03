from account import Account
from creditaccount import CreditAccount


def main():
    name = str(input("Введите имя: "))
    person_accaunt = float(input("Введите сумму на счету:"))
    type_account = str(input("Выберите тип счета (депозит/кредитный): "))
    if type_account == "депозит":
        acc = Account(name, person_accaunt)
        acc.deposit(50)
        acc.withdraw(30)
        acc.withdraw(500)
        acc.deposit(-10)
        print(f"\nТекущий баланс: {acc.get_balance()}")
        print()
        acc.print_history()
        print("\nСтатистика:")
        for k, v in acc.get_statistics().items():
            print(f"  {k}: {v}")
    else:
        credits = float(input("Введите кредитный лимит: "))
        acc = CreditAccount(name, person_accaunt, credits)
        acc.deposit(50)
        acc.withdraw(30)
        acc.withdraw(500)
        acc.withdraw(10)
        acc.print_history()

        print("\nСтатистика:")
        for k, v in acc.get_statistics().items():
            print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
