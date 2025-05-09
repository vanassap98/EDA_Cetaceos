"""
visualizacion.py

Funciones de visualización para el análisis exploratorio.
Incluye gráficos temporales y categóricos.
"""

# =========================
# Librerías necesarias
# =========================

import matplotlib.pyplot as plt
import seaborn as sns


# --------------------------------------------------------
# 1. Visualización temporal: registros por año y por mes
#  --------------------------------------------------------

def graficar_distribucion_temporal(df, col_anio="anio", col_mes="mes"):
    """
    Genera dos gráficos de barras para mostrar la distribución de registros
    por año y por mes.

    Args:
        df (pd.DataFrame): DataFrame que contiene columnas temporales.
        col_anio (str): Nombre de la columna con el año.
        col_mes (str): Nombre de la columna con el mes.
    """
    # --- Gráfico por año ---
    plt.figure(figsize=(12, 5))
    orden_anio = sorted(df[col_anio].dropna().unique())
    sns.countplot(data=df, x=col_anio, order=orden_anio)
    plt.title("Número de registros por año")
    plt.xlabel("Año")
    plt.ylabel("Cantidad de registros")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # --- Gráfico por mes ---
    # Asegurar tipo entero para graficar correctamente
    df[col_mes] = df[col_mes].astype("Int64")

    plt.figure(figsize=(10, 5))
    sns.countplot(data=df, x=col_mes, order=range(1, 13))
    plt.title("Número de registros por mes")
    plt.xlabel("Mes")
    plt.ylabel("Cantidad de registros")
    plt.tight_layout()
    plt.show()


# --------------------------------------------------------
# 2. Visualización categórica: top especies o regiones
# --------------------------------------------------------

def graficar_top_categorias(df, columna, top_n=10, titulo=None, xlabel=None):
    """
    Genera un gráfico de barras con las 'top_n' categorías más frecuentes en una columna.

    Args:
        df (pd.DataFrame): DataFrame con los datos.
        columna (str): Nombre de la columna categórica.
        top_n (int): Número de categorías a mostrar.
        titulo (str): Título del gráfico (opcional).
        xlabel (str): Etiqueta del eje X (opcional).
    """
    conteo = df[columna].value_counts().head(top_n)

    plt.figure(figsize=(10, 5))
    sns.barplot(x=conteo.values, y=conteo.index)
    plt.title(titulo or f"Top {top_n} categorías en '{columna}'")
    plt.xlabel(xlabel or "Cantidad de registros")
    plt.ylabel(columna)
    plt.tight_layout()
    plt.show()


#  --------------------------------------------------------
# 3. Visualización univariante 
#  --------------------------------------------------------

def plot_dist_individualcount(df, bins=30):
    """
    Histograma de la distribución del número de individuos por registro.

    Args:
        df (pd.DataFrame): DataFrame con columna 'individualcount'.
        bins (int): Número de divisiones del histograma.
    """
    plt.figure(figsize=(10, 5))
    sns.histplot(df["individualcount"], bins=bins, kde=True, color="steelblue")
    plt.title("Distribución del número de individuos por registro")
    plt.xlabel("Número de individuos")
    plt.ylabel("Frecuencia")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

def plot_top_species(df, top=10):
    """
    Barra horizontal con las especies más frecuentemente registradas.

    Args:
        df (pd.DataFrame): DataFrame con columna 'scientificname'.
        top (int): Número de especies a mostrar.
    """
    conteo = df["scientificname"].value_counts().head(top)

    plt.figure(figsize=(12, 6))
    sns.barplot(x=conteo.values, y=conteo.index, palette="viridis")
    plt.title("Top 10 especies más registradas")
    plt.xlabel("Cantidad de registros")
    plt.ylabel("Especie")
    plt.tight_layout()
    plt.show()

def plot_distribution_by_province(df, top=10):
    """
    Muestra un gráfico de barras de las provincias con más registros.

    Args:
        df (pd.DataFrame): DataFrame con columna 'stateprovince'.
        top (int): Número de provincias a mostrar.
    """
    conteo = df["stateprovince"].value_counts().head(top)

    plt.figure(figsize=(12, 5))
    sns.barplot(x=conteo.index, y=conteo.values, palette="mako")
    plt.title("Top 10 regiones con más registros")
    plt.xlabel("Región")
    plt.ylabel("Cantidad de registros")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

#  --------------------------------------------------------
# 4. Visualización bivariante
#  --------------------------------------------------------

def plot_grouped_boxplot(df, x, y, titulo=None, xlabel=None, ylabel=None):
    """
    Crea un boxplot agrupado para comparar la distribución de una variable numérica
    en función de una variable categórica.

    Args:
        df (pd.DataFrame): DataFrame con los datos.
        x (str): Nombre de la columna categórica (eje x).
        y (str): Nombre de la columna numérica (eje y).
        titulo (str): Título del gráfico.
        xlabel (str): Etiqueta del eje x.
        ylabel (str): Etiqueta del eje y.
    """
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x=x, y=y, palette="Set2", showfliers=False)
    plt.xticks(rotation=45)
    plt.title(titulo or f'{y} por {x}')
    plt.xlabel(xlabel or x)
    plt.ylabel(ylabel or y)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()
