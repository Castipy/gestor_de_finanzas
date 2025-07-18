from transactions import Transactions
from core import FinanceManager
from visualizations import Graphs
import pandas as pd

#Iniciando instancias#
manager= FinanceManager()
graphs = Graphs(manager)
##Cargando Archivo CSV##
ERROR=manager.load_excel()

def menu():
    print("\n=== Gestor de Gastos ===")
    print("1. Agregar ingreso")
    print("2. Agregar gasto")
    print("3. Ver balance total")
    print("4. Ver Gastos")
    print("5. Gráficas")
    print("6. Eliminar transacción")
    print("7. Editar transacción")
    print("8. Filtrar Transacciones")
    print("9. Guardar y salir")

while True:
    menu()
    choice = input("Seleccione una opción: ")
    if choice not in ['1', '2', '3', '4', '5', '6','7','8','9']:
        print("\nOpción no válida. Por favor, seleccione una opción válida.")
        continue 

    if choice == '1':   ##Agregar ingreso##
        try:
            Amount = abs(float(input("Ingrese el monto del ingreso: ")))       
            Category = input("Ingrese la categoría del ingreso: ")
            if not Category.strip():
                Category = "Correcciones"
            Description = input("Ingrese una descripción del ingreso: ")
            Date = input("Ingrese una fecha (dd-mm-YYYY HH:MM:SS) o deje en blanco para usar la fecha actual: ")
            transaction = Transactions('income', Amount, Category, Description, Date)
            manager.add_transaction(transaction)
            print("\nIngreso agregado exitosamente.")
        except ValueError:
            print(f"Valor incorrecto, por favor ingrese un número válido para el monto.")
        # Guardar los cambios en el archivo Excel#
        manager.save_excel()

    elif choice == '2': ##Agregar gasto##
        try:
            Amount = abs(float(input("Ingrese el monto del gasto: ")))
            Category = input("Ingrese la categoría del gasto: ")
            if not Category.strip():
                Category = "Correcciones"
            Description = input("Ingrese una descripción del gasto: ")
            Date = input("Ingrese una fecha (dd-mm-YYYY HH:MM:SS) o deje en blanco para usar la fecha actual: ")
            transaction = Transactions('expense', Amount, Category, Description, Date)
            manager.add_transaction(transaction)
            print("\nGasto agregado exitosamente.")
        except ValueError:
            print(f"Valor incorrecto, por favor ingrese un número válido para el monto.")
        # Guardar los cambios en el archivo Excel#
        manager.save_excel()

    elif choice == '3': ##Ver balance total##
        total = manager.total_balance()
        print(f"\nEl balance total es: {total:.2f}")
            
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
        if selection not in ['1', '2', '3', '4', '5']:
            print("\nOpción no válida. Por favor, seleccione una opción válida.")
            continue

        if selection == '1':
            resumen = resumen.set_index('Category').T
            print(resumen)
            total= resumen.iloc[0].sum()
            print(f'\nTotal de gastos {total}')

        elif selection == '2':
            print('\nPara obtener estadisticas actuales NO introduzca datos')
            year = input("\nIngrese el año (YYYY): ")
            month = input("\nIngrese el mes (MM): ")
            status,resumen = manager.monthly_expenses(year, month)

            if status == 'invalid_date':
                print('\nFecha inválida. Por favor ingrese un año y mes como números')
                continue
            elif status == 'no_data':
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
            status,resumen = manager.monthly_expenses(year, month, daily=True)

            if status == 'invalid_date':
                print('\nFecha inválida. Por favor ingrese un año y mes como números')
                continue
            elif status == 'no_data':
                print(f"\n""No hay gastos registrados para el mes {month} del año {year}.")
                continue

            print(f'\nLos gastos diarios para el mes {month if month else pd.Timestamp.now().month} son:')
            print('\n', resumen.to_string(index=False))
            total = resumen.iloc[:,1:].values.sum()
            print(f'\nTotal de gastos {total}')

        elif selection == '4':
            print('\nPara obtener estadisticas actuales NO introduzca datos')
            year = input("\nIngrese el año (YYYY): ")
            status,resumen = manager.anual_expenses(year)

            if status == 'invalid_year':
                print("\nAño inválido. Por favor ingrese un año como número (ej: 2024).")
                continue
            elif status == 'no_data':
                print(f"\nNo hay gastos registrados para el año {year}.")
                continue

            # Reindexar para asegurar que todos los meses estén presentes
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
            status, resumen = manager.anual_expenses(year)

            if status == 'invalid_year':
                print("\nAño inválido. Por favor ingrese un año como número (ej: 2024).")
                continue
            elif status == 'no_data':
                print(f"\nNo hay gastos registrados para el año {year}.")
                continue

            actual_year = pd.Timestamp.now().year
            resumen = resumen.reindex(range(actual_year-9,actual_year + 1),fill_value=0)
            resumen = resumen.T.to_frame().T
            print(f'\n Los gastos de los ultimos 10 años son:')
            print('\n', resumen.to_string(index=False))
            total= resumen.values.sum()
            print(f'\nTotal de gastos {total}')

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
        
        if selection not in ['1', '2', '3', '4']:
            print("\nOpción no válida. Por favor, seleccione una opción válida.")
            continue

        if selection == '1':
            print('\nPara obtener estadisticas actuales NO introduzca datos')
            year = input("\nIngrese el año (YYYY): ")
            month = input("\nIngrese el mes (MM): ")
            status,resumen = manager.monthly_expenses(year, month)

            if status == 'invalid_date':
                print('\nFecha inválida. Por favor ingrese un año y mes como números')
                continue
            elif status == 'no_data':
                print(f"\n""No hay gastos registrados para el mes {month} del año {year}.")
                continue

            title = (f'Gastos Mensuales {month if month else pd.Timestamp.now().month}-'
                     f'{year if year else pd.Timestamp.now().year}')
            graphs.expenses_graphics(resumen, title=title, graph_type='pie')

        elif selection == '2':
            print('\nPara obtener estadisticas actuales NO introduzca datos')
            year = input("\nIngrese el año (YYYY): ")
            month = input("\nIngrese el mes (MM): ")
            status,resumen = manager.monthly_expenses(year, month, daily=True)

            if status == 'invalid_date':
                print('\nFecha inválida. Por favor ingrese un año y mes como números')
                continue
            elif status == 'no_data':
                print(f"\n""No hay gastos registrados para el mes {month} del año {year}.")
                continue

            title = (f'Gastos Diarios {month if month else pd.Timestamp.now().month}-'
                     f'{year if year else pd.Timestamp.now().year}')
            graphs.expenses_graphics(resumen, title=title, graph_type='lineplot')

        elif selection == '3':
            print('\nPara obtener estadisticas actuales NO introduzca datos')
            year = input("\nIngrese el año (YYYY): ")
            status,resumen = manager.anual_expenses(year)

            if status == 'invalid_date':
                print('\nFecha inválida. Por favor ingrese un año y mes como números')
                continue
            elif status == 'no_data':
                print(f"\n""No hay gastos registrados para el mes {month} del año {year}.")
                continue

            resumen = resumen.reindex(range(1,13),fill_value=0).reset_index()
            graphs.expenses_graphics(resumen, f'Gasto anual del {year if year else pd.Timestamp.now().year}')

        elif selection == '4':
            status, resumen = manager.anual_expenses(all_years=True)
            
            if status == 'invalid_date':
                print('\nFecha inválida. Por favor ingrese un año y mes como números')
                continue
            elif status == 'no_data':
                print(f"\n""No hay gastos registrados para el mes {month} del año {year}.")
                continue

            year = pd.Timestamp.now().year
            resumen = resumen.reindex(range(year-9,year + 1),fill_value=0).reset_index()
            graphs.expenses_graphics(resumen, f'Gastos de los últimos 10 años {year-10}-{year}' )
    
    elif choice == '6': ##Eliminar transacción##
        if manager.df_transactions.empty:
            print("\nNo hay transacciones registradas para eliminar.")
            continue

        print("\n========Lista de Transacciones========")
        df_aux = manager.df_transactions.copy()
        print(df_aux[['Model', 'Amount', 'Category', 'Description', 'Date']].to_string(index=True))
        
        try:
            idx = int(input("\nIngrese el índice de la transacción a eliminar: "))
            if manager.delete_transaction(idx):
                print(f"\nTransacción con índice {idx} eliminada correctamente.")
            else:
                print(f"\nÍndice inválido. No se pudo eliminar la transacción.")
        except ValueError:
            print("\nEntrada inválida. Debe ingresar un número entero.")

        manager.save_excel()
    
    elif choice == '7': ##Editar transacción##
        if manager.df_transactions.empty:
            print("\nNo hay transacciones registradas para editar.")
            continue
        # Mostrar todas las transacciones con índice
        df_temp = manager.list_transactions()
        print("\nTransacciones registradas:")
        print(df_temp.to_string(index=False))

        try:
            index = int(input("Ingrese el índice de la transacción que desea editar: "))
        except ValueError:
            print("Índice inválido.")
            continue

        if index < 0 or index >= len(manager.df_transactions):
            print("Índice fuera de rango.")
            continue

        print("\nCampos disponibles: Model, Amount, Category, Description, Date")
        campo = input("Ingrese el nombre del campo que desea editar: ").strip()
        if campo not in ['Model', 'Amount', 'Category', 'Description', 'Date']:
            print("Campo no válido.")
            continue

        nuevo_valor = input(f"Ingrese el nuevo valor para '{campo}': ").strip()
        
        if campo == 'Amount':
            try:
                nuevo_valor = float(nuevo_valor)
            except ValueError:
                print("Monto inválido.")
                continue

        actualizado = manager.edit_transaction(index, **{campo: nuevo_valor})
        if actualizado:
            print("\nTransacción actualizada exitosamente.")
        else:
            print("\nError al actualizar la transacción.")

    elif choice == '8': ##Filtrar transacciones##
        print("\n=== Buscar transacciones ===")
        model = input("Tipo (income/expense) o dejar en blanco: ").strip()
        category = input("Categoría o dejar en blanco: ").strip()
        description = input("Descripción o dejar en blanco: ").strip()
        start_date = input("Fecha inicio (dd-mm-YYYY HH:MM:SS) o dejar en blanco: ").strip()
        end_date = input("Fecha fin (dd-mm-YYYY HH:MM:SS) o dejar en blanco: ").strip()
        
        search = manager.search_transactions(
            model=model if model else None,
            category=category if category else None,
            description=description if description else None,
            start_date=start_date if start_date else None,
            end_date=end_date if end_date else None
        )

        if search.empty:
            print("\nNo se encontraron transacciones con los criterios dados.")
        else:
            print(f"\nSe encontraron {len(search)} transacciones:\n")
            print(search.to_string(index=True))
        

    elif choice == '9': ##Guardar y salir##
        file_path = manager.save_excel()
        print(f"\nDatos guardados en {file_path}. Saliendo...")
        break
    
#Comprobando errores#
if not ERROR.empty:
    print("\nSe han registrado errores durante la ejecución del programa.")
    print(ERROR.to_string(index=False))
    