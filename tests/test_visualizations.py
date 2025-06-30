from gestor.visualizations import Graphs
from gestor.core import FinanceManager
import os
import pandas as pd
import matplotlib.pyplot as plt

#En pytests no es necesario crear una clase que herede como en unittest#

def test_expenses_graphics_creates_figure(tmp_path):
    # Simular datos de gastos
    data = {'Category': ['Comida', 'Transporte'], 'Amount': [100, 50]}
    df = pd.DataFrame(data)

    # Instanciar Graphs
    manager = FinanceManager()
    graph = Graphs(manager)

    # Cambiar temporalmente la carpeta de imágenes
    original_dir = os.getcwd()
    os.chdir(tmp_path)  # Carpeta temporal
    fig = graph.expenses_graphics(df, title="Gastos Test", graph_type='bar')
    os.chdir(original_dir)

    # Verifica que se retorna una figura
                                                

    # Verifica que el archivo se haya guardado
    assert os.path.exists(os.path.join(tmp_path, 'images', 'Gastos Test.png'))