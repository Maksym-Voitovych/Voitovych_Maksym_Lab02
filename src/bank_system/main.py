import sys
from bank_system.data import create_account, get_sample_accounts
from bank_system.processors import (
    build_account_index, find_account, 
    create_min_balance_filter, filter_accounts, universal_sort
)
from bank_system.analytics import (
    group_accounts_by_type, calculate_total_balance,
    get_average_balance, get_max_balance_account,
    get_account_type_stats, add_to_history, get_history
)

def display_menu() -> None:
    print("\n=== СИСТЕМА БАНКІВСЬКИХ РАХУНКІВ ===")
    print("1. Створити новий рахунок (**kwargs)")
    print("2. Поповнити / Списати кошти")
    print("3. Знайти рахунок (Dict index)")
    print("4. Переглянути загальну статистику (*args, Generator)")
    print("5. Статистика типів рахунків (Counter)")
    print("6. Фільтрація за мін. балансом (Closure)")
    print("7. Універсальне сортування (за будь-яким полем)")
    print("8. Переглянути історію останніх операцій (deque)")
    print("9. Вийти з програми")

def main() -> None:
    accounts = get_sample_accounts()

    while True:
        display_menu()
        choice = input("Оберіть дію (1-9): ").strip()

        if choice == "1":
            acc_num = input("Номер рахунку: ").strip()
            owner = input("ПІБ власника: ").strip()
            acc_type = input("Тип (Checking/Savings/Credit/Deposit): ").strip()
            try:
                initial_bal = float(input("Початковий баланс: "))
                new_acc = create_account(
                    account_number=acc_num, 
                    client_name=owner, 
                    balance=initial_bal, 
                    account_type=acc_type
                )
                accounts.append(new_acc)
                add_to_history(f"Створено рахунок {acc_num} ({owner})")
                print(f"Створено рахунок {acc_num}!")
            except ValueError as err:
                print(f"Помилка: {err}")

        elif choice == "2":
            acc_num = input("Введіть номер рахунку: ").strip()
            index = build_account_index(accounts)
            acc = find_account(index, acc_num)
            if not acc:
                print("Рахунок не знайдено.")
                continue
            
            action = input("1 - Поповнити, 2 - Списати: ").strip()
            try:
                amount = float(input("Сума: "))
                if action == "1":
                    acc['balance'] += amount
                    add_to_history(f"Поповнення {acc_num} на {amount} грн")
                    print(f"Новий баланс: {acc['balance']:.2f} грн")
                elif action == "2":
                    if acc['balance'] < amount:
                        print("Недостатньо коштів.")
                    else:
                        acc['balance'] -= amount
                        add_to_history(f"Списання {acc_num} на {amount} грн")
                        print(f"Новий баланс: {acc['balance']:.2f} грн")
            except ValueError:
                print("Некоректне число.")

        elif choice == "3":
            query = input("Введіть номер або ім'я: ").strip()
            index = build_account_index(accounts)
            found = find_account(index, query)
            if found:
                print(f"Знайдено: {found['account_number']} | {found['client_name']} | {found['balance']} грн")
            else:
                print("Нічого не знайдено.")

        elif choice == "4":
            total = calculate_total_balance(*(a["balance"] for a in accounts))
            avg = get_average_balance(accounts)
            max_acc = get_max_balance_account(accounts)
            print(f"\nЗагальна сума: {total:.2f} грн")
            print(f"Середній баланс: {avg:.2f} грн")
            print(f"Найбільший баланс: {max_acc.get('client_name')} ({max_acc.get('balance')} грн)")

        elif choice == "5":
            stats = get_account_type_stats(accounts)
            print("\nКількість рахунків за типами (Counter):")
            for acc_type, count in stats.items():
                print(f" - {acc_type}: {count}")

        elif choice == "6":
            try:
                min_val = float(input("Мінімальний баланс: "))
                min_filter = create_min_balance_filter(min_val)
                filtered = filter_accounts(accounts, min_filter)
                print(f"Знайдено {len(filtered)} рахунків:")
                for a in filtered:
                    print(f" - {a['client_name']}: {a['balance']} грн")
            except ValueError:
                print("Некоректне число.")

        elif choice == "7":
            field = input("Введіть поле для сортування (balance / client_name / account_type): ").strip()
            sorted_accs = universal_sort(accounts, key=field, reverse=True)
            print(f"\nСортування за полем '{field}':")
            for a in sorted_accs:
                print(f" - {a['client_name']} ({a['account_type']}): {a['balance']} грн")

        elif choice == "8":
            history = get_history()
            print("\nІсторія останніх операцій (до 5 дій):")
            if not history:
                print("Історія порожня.")
            for i, h in enumerate(history, 1):
                print(f"{i}. {h}")

        elif choice == "9":
            print("Вихід з програми.")
            sys.exit(0)

if __name__ == "__main__":
    main()