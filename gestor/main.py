from transactions import Transactions
from manager import FinanceManager
import os

def menu():
    print("\n=== Gestor de Gastos ===")
    print("1. Agregar ingreso")
    print("2. Agregar gasto")
    print("3. Ver balance total")
    print("4. Ver todos los gastos")
    print("5. Ver gastos por categoría")
    print("6. Gráficas")
    print("7. Guardar y salir")

manager = FinanceManager()
manager.load_csv(filename=os.path.join(os.path.dirname(__file__), 'data.csv'))

while True:
    menu()
    choice = input("Seleccione una opción: ")
      
    if choice == '1':   ##Agregar ingreso##
        try:
            amount = float(input("Ingrese el monto del ingreso: "))       
            category = input("Ingrese la categoría del ingreso: ")
            if category.strip() == "":
                category = "Correcciones"
            description = input("Ingrese una descripción del ingreso: ")
            date = input("Ingrese una fecha (dd-mm-YYYY HH:MM:SS) o deje en blanco para usar la fecha actual: ")
            transaction = Transactions('income', amount, category, description, date)
            manager.add_transaction(transaction)
            print("\nIngreso agregado exitosamente.")
        except ValueError:
            print(f"Valor incorrecto, por favor ingrese un número válido para el monto.")

    elif choice == '2': ##Agregar gasto##
        amount = float(input("Ingrese el monto del gasto: "))
        category = input("Ingrese la categoría del gasto: ")
        description = input("Ingrese una descripción del gasto: ")
        date = input("Ingrese una fecha (dd-mm-YYYY HH:MM:SS) o deje en blanco para usar la fecha actual: ")
        transaction = Transactions('expense', amount, category, description, date)
        manager.add_transaction(transaction)
        print("\nGasto agregado exitosamente.")

    elif choice == '3': ##Ver balance total##
        total = manager.total_balance()
        print(f"\nEl balance total es: {total}")
    
    elif choice == '4': ##Ver todos los gastos##
        expenses = manager.historial_expenses()
        if expenses:
            print("\nHistorial de gastos:")
            for expense in expenses:
                print(expense)
        else:
            print("\nNo hay gastos registrados.")

    elif choice == '5': ##Ver gastos por categoría##
        expenses_by_category = manager.categories_expenses()
        if expenses_by_category:
            print("\nGastos por categoría:")
            for category, total in expenses_by_category.items():
                print(f"{category}: {total}")
        else:
            print("\nNo hay gastos registrados por categoría.")

    elif choice == '6': ##Ver gráfico de gastos por categoría##
        election = input("\nTipos de gráficos disponibles:"
                         "\n1. Gastos por Categorías"
                         "\n2. Gastos Diarios por mes"
                         "\n3. Gastos Mensuales por año"
                         "\nSeleccione una opción: ")
        if election == '1':
            manager.categories_expenses_graphic()
        elif election == '2':
            print("\nPara obtener datos actuales dejar vacío el año y mes.")
            year = input("\nIngrese el año (YYYY): ")
            month = input("\nIngrese el mes (MM): ")
            manager.monthly_expenses_graphic(year, month)
        elif election == '3':
            manager.anual_expenses_graphic()

    elif choice == '7': ##Guardar y salir##
        filename = os.path.join(os.path.dirname(__file__), 'data.csv')
        manager.save_csv(filename)
        print(f"\nDatos guardados en {filename}. Saliendo...")
        break

    else:
        print("\nOpción no válida. Intente de nuevo.")