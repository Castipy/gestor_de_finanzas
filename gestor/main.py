from transactions import Transactions
from core import FinanceManager
from visualizations import Graphs
import pandas as pd

#Iniciando instancias#
manager= FinanceManager()
graphs = Graphs(manager)
##Cargando Archivo CSV##
manager.load_excel()

def menu():
    print("\n=== Gestor de Gastos ===")
    print("1. Agregar ingreso")
    print("2. Agregar gasto")
    print("3. Ver balance total")
    print("4. Ver Gastos")
    print("5. Gráficas")
    print("6. Guardar y salir")

while True:
    menu()
    choice = input("Seleccione una opción: ")
      
    if choice == '1':   ##Agregar ingreso##
        try:
            amount = abs(float(input("Ingrese el monto del ingreso: ")))       
            category = input("Ingrese la categoría del ingreso: ")
            if not category.strip() == "":
                category = "Correcciones"
            description = input("Ingrese una descripción del ingreso: ")
            date = input("Ingrese una fecha (dd-mm-YYYY HH:MM:SS) o deje en blanco para usar la fecha actual: ")
            transaction = Transactions('income', amount, category, description, date)
            manager.add_transaction(transaction)
            print("\nIngreso agregado exitosamente.")
        except ValueError:
            print(f"Valor incorrecto, por favor ingrese un número válido para el monto.")

    elif choice == '2': ##Agregar gasto##
        try:
            amount = abs(float(input("Ingrese el monto del gasto: ")))
            category = input("Ingrese la categoría del gasto: ")
            description = input("Ingrese una descripción del gasto: ")
            date = input("Ingrese una fecha (dd-mm-YYYY HH:MM:SS) o deje en blanco para usar la fecha actual: ")
            transaction = Transactions('expense', amount, category, description, date)
            manager.add_transaction(transaction)
            print("\nGasto agregado exitosamente.")
        except ValueError:
            print(f"Valor incorrecto, por favor ingrese un número válido para el monto.")

    elif choice == '3': ##Ver balance total##
        total = manager.total_balance()
        print(f"\nEl balance total es: {total}")

    elif choice == '4': ##Ver gastos##
        _,resumen = manager.expenses()
        if resumen.empty:
                print("\nNo hay gastos registrados")
                continue
        print('\nQue tipo de datos desea ver?',
              '\n1. Gastos Totales',
              '\n2. Gastos Mensuales',
              "\n3. Gastos Diarios"
              "\n4. Gasto Anual"
              "\n5. Gastos Anuales (últimos 10 años)")
        selection = input("Seleccione una opción: ")

        if selection == '1':
            resumen = resumen.set_index('Category').T
            print(resumen)
            total= resumen.iloc[0].sum()
            print(f'\nTotal de gastos {total}')
        elif selection == '2':
            print('\nPara obtener estadisticas actuales NO introduzca datos')
            year = input("\nIngrese el año (YYYY): ")
            month = input("\nIngrese el mes (MM): ")
            resumen = manager.monthly_expenses(year, month)
            if resumen.empty:
                print(f"\n""No hay gastos registrados para el mes {month} del año {year}.")
                continue
            print(f'\nLos gastos del mes {month if month else pd.Timestamp.now().month} son:')
            resumen = resumen.set_index('Category').T
            print('\n', resumen)
            total= resumen.iloc[0].sum()
            print(f'\nTotal de gastos {total}')
        elif selection == '3':
            print('\nPara obtener estadisticas actuales NO introduzca datos')
            year = input("\nIngrese el año (YYYY): ")
            month = input("\nIngrese el mes (MM): ")
            resumen = manager.monthly_expenses(year, month, daily=True)
            if resumen.empty:
                print(f"\n""No hay gastos registrados para el mes {month} del año {year}.")
                continue
            print(f'\nLos gastos diarios para el mes {month if month else pd.Timestamp.now().month} son:')
            print('\n', resumen.to_string(index=False))
            total = resumen.iloc[:,1:].values.sum()
            print(f'\nTotal de gastos {total}')
        elif selection == '4':
            print('\nPara obtener estadisticas actuales NO introduzca datos')
            year = input("\nIngrese el año (YYYY): ")
            resumen = manager.anual_expenses(year)
            if resumen.empty:
                print(f"\n""No hay gastos registrados para el año {year}.")
                continue
            resumen = resumen.reindex(range(1, 13), fill_value=0)
            # Transponer para tener una sola fila y meses como columnas
            resumen = resumen.T.to_frame().T
            resumen.columns = [f'Mes_{m}' for m in resumen.columns]
            resumen.index = [f'Año_{year}']
            print(f'\nLos gastos del año {year if year else pd.Timestamp.now().year} son :')
            print('\n', resumen.to_string(index=False))
            total = resumen.values.sum()
            print(f'\nTotal de gastos {total}')
        elif selection == '5':
            resumen = manager.anual_expenses(all_years=True)
            if resumen.empty:
                print(f"\n""No hay gastos registrados para los últimos 10 años.")
                continue
            actual_year = pd.Timestamp.now().year
            resumen = resumen.reindex(range(actual_year-9,actual_year + 1),fill_value=0)
            resumen = resumen.T.to_frame().T
            print(f'\n Los gastos de los ultimos 10 años son:')
            print('\n', resumen.to_string(index=False))
            total= resumen.values.sum()
            print(f'\nTotal de gastos {total}')
        else:
            print("\nOpción no válida. Por favor, seleccione una opción válida.")
            continue

    elif choice == '5': ##Ver gráficos de gastos##
        _,resumen = manager.expenses()
        if resumen.empty:
            print("\nNo hay gastos registrados")
            continue
        selection = input("\nTipos de gráficos disponibles:"
                        "\n1. Gastos Mensuales"
                        "\n2. Gastos Diarios"
                        "\n3. Gastos Anuales"
                        "\n4. Gastos de todos los Años"
                        "\nSeleccione una opción: ")
        if selection == '1':
            print('\nPara obtener estadisticas actuales NO introduzca datos')
            year = input("\nIngrese el año (YYYY): ")
            month = input("\nIngrese el mes (MM): ")
            resumen = manager.monthly_expenses(year, month)
            if resumen.empty:
                print(f"\n""No hay gastos registrados para la fecha.")
                continue
            title = (f'Gastos Mensuales {month if month else pd.Timestamp.now().month}-'
                     f'{year if year else pd.Timestamp.now().year}')
            graphs.expenses_graphics(resumen, title=title, graph_type='pie')

        elif selection == '2':
            print('\nPara obtener estadisticas actuales NO introduzca datos')
            year = input("\nIngrese el año (YYYY): ")
            month = input("\nIngrese el mes (MM): ")
            resumen = manager.monthly_expenses(year, month, daily=True)
            if resumen.empty:
                print(f"\n""No hay gastos registrados para la fecha escogida.")
                continue
            title = (f'Gastos Diarios {month if month else pd.Timestamp.now().month}-'
                     f'{year if year else pd.Timestamp.now().year}')
            graphs.expenses_graphics(resumen, title=title, graph_type='lineplot')

        elif selection == '3':
            print('\nPara obtener estadisticas actuales NO introduzca datos')
            year = input("\nIngrese el año (YYYY): ")
            resumen = manager.anual_expenses(year)
            if resumen.empty:
                print("\n"f"No hay gastos registrados para el año {year if year else pd.Timestamp.now().year}.")
                continue
            resumen = resumen.reindex(range(1,13),fill_value=0).reset_index()
            graphs.expenses_graphics(resumen, f'Gasto anual del {year if year else pd.Timestamp.now().year}')

        elif selection == '4':
            resumen = manager.anual_expenses(all_years=True)
            print(resumen)
            if resumen.empty:
                print(f"\n""No hay gastos registrados para los últimos 10 años.")
                continue
            year = pd.Timestamp.now().year
            resumen = resumen.reindex(range(year-9,year + 1),fill_value=0).reset_index()
            graphs.expenses_graphics(resumen, f'Gastos de los últimos 10 años {year-10}-{year}' )
        else:
            print("\nOpción no válida. Por favor, seleccione una opción válida.")
            continue

    elif choice == '6': ##Guardar y salir##
        file_path = manager.save_excel()
        print(f"\nDatos guardados en {file_path}. Saliendo...")
        break

    else:
        print("\nOpción no válida. Intente de nuevo.")