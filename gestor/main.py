from transactions import Transactions
from manager import FinanceManager
import os
import csv

def menu():
    print("\n=== Gestor de Gastos ===")
    print("1. Agregar ingreso")
    print("2. Agregar gasto")
    print("3. Ver balance total")
    print("4. Ver gastos por categoría")
    print("5. Guardar y salir")

manager = FinanceManager()
manager.load_csv(filename=os.path.join(os.path.dirname(__file__), 'data.csv'))

while True:
    menu()
    choice = input("Seleccione una opción: ")

    if choice == '1':
        amount = float(input("Ingrese el monto del ingreso: "))
        category = input("Ingrese la categoría del ingreso: ")
        description = input("Ingrese una descripción del ingreso: ")
        transaction = Transactions('income', amount, category, description)
        manager.add_transaction(transaction)
        print("Ingreso agregado exitosamente.")

    elif choice == '2':
        amount = float(input("Ingrese el monto del gasto: "))
        category = input("Ingrese la categoría del gasto: ")
        description = input("Ingrese una descripción del gasto: ")
        transaction = Transactions('expense', amount, category, description)
        manager.add_transaction(transaction)
        print("Gasto agregado exitosamente.")

    elif choice == '3':
        total = manager.total_balance()
        print(f"El balance total es: {total}")

    elif choice == '4':
        expenses_by_category = manager.categories_expenses()
        print("Gastos por categoría:")
        for category, total in expenses_by_category.items():
            print(f"{category}: {total}")

    elif choice == '5':
        filename = os.path.join(os.path.dirname(__file__), 'data.csv')
        manager.save_csv(filename)
        print(f"Datos guardados en {filename}. Saliendo...", "Eugenio te amo")
        break

    else:
        print("Opción no válida. Intente de nuevo.")




