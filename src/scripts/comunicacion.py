"""
comunicacion.py

Funciones de visualización para el análisis comparativo y narrativo.
Incluye gráficos temporales y categóricos.
"""

# =========================
# Librerías necesarias
# =========================

import folium
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------------------
# 1. Visualización temporal: registros por año y por mes
#  --------------------------------------------------------

def plot_individuals_per_year(df, species_list):
    """
    Genera un gráfico de líneas comparando el número total de individuos observados por año
    para una lista de especies dada.

    Parámetros:
    - df: DataFrame con las columnas 'anio', 'nombre_cientifico' e 'individualcount'.
    - species_list: Lista de nombres científicos a comparar.

    Retorna:
    - Matplotlib figure.
    """

    # Filtrar solo las especies de interés
    df_filtered = df[df['nombre_cientifico'].isin(species_list)].copy()
    
    # Agrupar por especie y año
    yearly_counts = (
        df_filtered.groupby(['anio', 'nombre_cientifico'])['individualcount']
        .sum()
        .reset_index()
    )

    # Plot
    palette = {
        "Stenella coeruleoalba": "#2A9D8F",
        "Delphinus delphis": "#B55656"}

    plt.figure(figsize=(10, 6))
    sns.lineplot(
    data=yearly_counts,
    x='anio',
    y='individualcount',
    hue='nombre_cientifico',
    palette=palette,
    marker='o'
    )


    plt.title('Evolución anual del número de individuos observados')
    plt.xlabel('Año')
    plt.ylabel('Número de individuos')
    plt.legend(title='Especie')
    plt.grid(True, linestyle='--', alpha=0.2)
    plt.tight_layout()

    # Guardar figura
    plt.savefig("../outputs/figuras/evolucion_registros_anuales.png", dpi=300, bbox_inches="tight")

    plt.show()


# --------------------------------------------------------------
# 2. Visualización espacial: mapa de distribución de especies
# --------------------------------------------------------------

def plot_species_map(df, species_list, color_dict=None):
    """
    Genera un scatterplot geográfico con la localización de registros de varias especies.

    Args:
        df (pd.DataFrame): DataFrame con columnas 'nombre_cientifico', 'decimallatitude', 'decimallongitude'.
        species_list (list): Lista de especies a mostrar.
        color_dict (dict, opcional): Diccionario de colores por especie.

    Returns:
        None
    """

    # Filtrar datos válidos
    df_filtered = df[
        (df['nombre_cientifico'].isin(species_list)) &
        (df['decimallatitude'].notna()) &
        (df['decimallongitude'].notna())
    ]

    plt.figure(figsize=(10, 8))
    
    color_dict = {
        "Stenella coeruleoalba": "#2A9D8F",
        "Delphinus delphis": "#B55656"
        }

    for species in species_list:
        subset = df_filtered[df_filtered['nombre_cientifico'] == species]
        plt.scatter(
            subset['decimallongitude'],
            subset['decimallatitude'],
            s=20,
            alpha=0.6,
            label=species,
            color=color_dict[species] if color_dict and species in color_dict else None
        )
    
    plt.xlabel('Longitud')
    plt.ylabel('Latitud')
    plt.title('Distribución geográfica de registros por especie')
    plt.legend(title='Especie')
    plt.grid(True, linestyle='--', alpha=0.2)
    plt.tight_layout()

    # Guardar figura
    plt.savefig("../outputs/figuras/distribucion_registros_sp.png", dpi=300, bbox_inches="tight")

    plt.show()


# --------------------------------------------------------------
# 2.1 Visualización interactiva: mapa con Folium
# --------------------------------------------------------------

def plot_species_map_folium(df, species_list, color_dict=None, zoom_start=5):
    """
    Genera un mapa interactivo con registros de varias especies usando Folium.

    Args:
        df (pd.DataFrame): DataFrame con columnas 'nombre_cientifico', 'decimallatitude', 'decimallongitude'.
        species_list (list): Lista de especies a mostrar.
        color_dict (dict, opcional): Diccionario de colores por especie.
        zoom_start (int): Nivel de zoom inicial del mapa.

    Returns:
        folium.Map: Mapa interactivo con los puntos por especie.
    """
    
    from folium import FeatureGroup

    # Filtrar datos válidos
    df_filtered = df[
        (df['nombre_cientifico'].isin(species_list)) &
        (df['decimallatitude'].notna()) &
        (df['decimallongitude'].notna())
    ]

    # Punto medio para centrar el mapa
    lat_center = df_filtered['decimallatitude'].mean()
    lon_center = df_filtered['decimallongitude'].mean()

    # Crear mapa base
    m = folium.Map(location=[lat_center, lon_center], zoom_start=zoom_start, tiles="CartoDB positron")

    # Añadir capa por especie
    color_dict = {
        "Stenella coeruleoalba": "#2A9D8F",
        "Delphinus delphis": "#B55656"
        }
    
    for species in species_list:
        grupo = FeatureGroup(name=species)
        subset = df_filtered[df_filtered['nombre_cientifico'] == species]
        color = color_dict[species] if color_dict and species in color_dict else 'blue'

        for _, row in subset.iterrows():
            folium.CircleMarker(
                location=[row['decimallatitude'], row['decimallongitude']],
                radius=3,
                color=color,
                fill=True,
                fill_opacity=0.6,
                popup=species
            ).add_to(grupo)

        grupo.add_to(m)

    folium.LayerControl().add_to(m)
    return m
    


# --------------------------------------------
# 3. Visualización temporal: registros por mes
# --------------------------------------------

def plot_individuals_per_month(df, species_list):
    """
    Genera un gráfico de líneas con la cantidad total de individuos observados por mes,
    para cada especie de interés.

    Parámetros:
    - df: DataFrame con las columnas 'mes', 'nombre_cientifico' e 'individualcount'.
    - species_list: Lista con los nombres científicos simplificados de las especies a comparar.

    Retorna:
    - Matplotlib figure.
    """
    df_filtered = df[df["nombre_cientifico"].isin(species_list)].copy()
    
    monthly_counts = (
        df_filtered.groupby(["mes", "nombre_cientifico"])["individualcount"]
        .sum()
        .reset_index()
    )
    # Plot
    palette = {
        "Stenella coeruleoalba": "#2A9D8F",
        "Delphinus delphis": "#B55656"
        }

    plt.figure(figsize=(10, 6))
    sns.lineplot(
        data=monthly_counts,
        x="mes",
        y="individualcount",
        hue="nombre_cientifico",
        palette=palette,
        marker="o"
    )


    plt.title("Distribución mensual del número de individuos observados")
    plt.xlabel("Mes")
    plt.ylabel("Número de individuos")
    plt.grid(True, linestyle='--', alpha=0.2)
    plt.legend(title="Especie")
    plt.tight_layout()
    

    # Guardar figura
    plt.savefig("../outputs/figuras/estacionalidad_individuos_mes.png", dpi=300, bbox_inches="tight")
    
    plt.show()

# ---------------------------------------------------------------
# 4. Visualización espacio-temporal: distribución por décadas
# ---------------------------------------------------------------

def plot_distribution_by_decade(df, species_name, color, decade_split=2010):
    """
    Genera dos subgráficos de dispersión para comparar la distribución geográfica de una especie
    en dos periodos de tiempo (antes y después de una década específica).

    Args:
        df (pd.DataFrame): DataFrame limpio con columnas 'anio', 'nombre_cientifico', 'decimallatitude', 'decimallongitude'.
        species_name (str): Nombre científico de la especie (sin autor).
        color (str): Código HEX del color a usar para los puntos.
        decade_split (int): Año que separa las dos décadas (por defecto: 2010).

    Returns:
        None
    """

    df_sp = df[df["nombre_cientifico"] == species_name].copy()
    df_sp = df_sp[df_sp["decimallatitude"].notna() & df_sp["decimallongitude"].notna()]

    df_early = df_sp[df_sp["anio"] < decade_split]
    df_recent = df_sp[df_sp["anio"] >= decade_split]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharex=True, sharey=True)

    axes[0].scatter(
        df_early["decimallongitude"],
        df_early["decimallatitude"],
        alpha=0.4,
        s=15,
        color=color
    )
    axes[0].set_title(f"(2000–{decade_split - 1})")
    axes[0].set_xlabel("Longitud")
    axes[0].set_ylabel("Latitud")
    axes[0].grid(True, linestyle="--", alpha=0.2)

    axes[1].scatter(
        df_recent["decimallongitude"],
        df_recent["decimallatitude"],
        alpha=0.4,
        s=15,
        color=color
    )
    axes[1].set_title(f"({decade_split}–2024)")
    axes[1].set_xlabel("Longitud")
    axes[1].grid(True, linestyle="--", alpha=0.2)

    fig.suptitle(f"Cambio en la distribución geográfica por décadas de {species_name}", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Guardar figura
    safe_name = species_name.lower().replace(" ", "_")
    filename = f"../outputs/figuras/cambio_distribucion_{safe_name}.png"
    fig.savefig(filename, dpi=300, bbox_inches="tight")

    plt.show()



# ---------------------------------------------------------------------
# 5. Visualización espacio-temporal detallada por especie (por periodos)
# ---------------------------------------------------------------------
def plot_distribution_by_periods(df, species_name, color, years_ranges):
    """
    Genera subgráficos para comparar la distribución geográfica de una especie
    en varios periodos definidos por el usuario (ej. cada 6 años).

    Args:
        df (pd.DataFrame): DataFrame limpio con columnas 'anio', 'nombre_cientifico', 'decimallatitude', 'decimallongitude'.
        species_name (str): Nombre científico de la especie (sin autor).
        color (str): Código HEX del color a usar para los puntos.
        years_ranges (list of tuples): Lista de tuplas con rangos de años (ej. [(2000, 2005), (2006, 2011), ...]).

    Returns:
        None
    """

    df_sp = df[df["nombre_cientifico"] == species_name].copy()
    df_sp = df_sp[df_sp["decimallatitude"].notna() & df_sp["decimallongitude"].notna()]

    n = len(years_ranges)
    cols = 2
    rows = (n + 1) // 2

    fig, axes = plt.subplots(rows, cols, figsize=(14, 6 * rows), sharex=True, sharey=True)

    for i, (start, end) in enumerate(years_ranges):
        ax = axes.flat[i]
        df_period = df_sp[(df_sp["anio"] >= start) & (df_sp["anio"] <= end)]

        ax.scatter(
            df_period["decimallongitude"],
            df_period["decimallatitude"],
            alpha=0.4,
            s=15,
            color=color
        )
        ax.set_title(f"{start}–{end}", fontsize=14)

        # Mostrar etiquetas solo en subgráficos exteriores
        if i // cols == rows - 1:
            ax.set_xlabel("Longitud")
        else:
            ax.set_xlabel("")
        if i % cols == 0:
            ax.set_ylabel("Latitud")
        else:
            ax.set_ylabel("")

        ax.grid(True, linestyle="--", alpha=0.2)

    for j in range(i + 1, len(axes.flat)):
        axes.flat[j].axis("off")  # Ocultar subgráficos vacíos

    # Título en cursiva
    fig.suptitle(
        f"Distribución de {species_name}",
        fontdict={'family': 'serif', 'style': 'italic'},
        y=1.02
    )

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Guardar figura
    safe_name = species_name.lower().replace(" ", "_")
    filename = f"../outputs/figuras/cambio_detallado_distribucion_{safe_name}.png"
    fig.savefig(filename, dpi=300, bbox_inches="tight")

    plt.show()



# --------------------------------------------------------------------------------

def plot_compare_species_by_periods_split(df, species_list, color_dict, years_ranges):
    """
    Genera un gráfico por periodo, con dos subplots (uno por especie), para comparar
    visualmente su distribución geográfica dentro de ese rango temporal.

    Args:
        df (pd.DataFrame): DataFrame limpio con columnas 'anio', 'nombre_cientifico', 'decimallatitude', 'decimallongitude'.
        species_list (list): Lista con los dos nombres científicos a comparar.
        color_dict (dict): Diccionario con colores para cada especie.
        years_ranges (list of tuples): Lista de tuplas con rangos de años.

    Returns:
        None
    """

    for (start, end) in years_ranges:
        fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharex=True, sharey=True)

        for ax, species in zip(axes, species_list):
            df_sub = df[
                (df["nombre_cientifico"] == species) &
                (df["anio"] >= start) & (df["anio"] <= end) &
                df["decimallatitude"].notna() & df["decimallongitude"].notna()
            ]

            ax.scatter(
                df_sub["decimallongitude"],
                df_sub["decimallatitude"],
                alpha=0.4,
                s=15,
                color=color_dict[species]
            )

            ax.set_title(
                species,
                fontdict={'family': 'serif', 'style': 'italic', 'size': 12}
            )

            ax.grid(True, linestyle="--", alpha=0.2)

            # Etiquetas solo en exteriores
            if ax == axes[0]:
                ax.set_ylabel("Latitud")
            ax.set_xlabel("Longitud")

        fig.suptitle(
            f"Comparativa de distribución geográfica ({start}–{end})",
            fontsize=14
        )

        plt.tight_layout(rect=[0, 0, 1, 0.95])
    

        # Guardar figura
        filename = f"../outputs/figuras/comparativa_distribucion_{start}_{end}.png"
        fig.savefig(filename, dpi=300, bbox_inches="tight")

        plt.show()

