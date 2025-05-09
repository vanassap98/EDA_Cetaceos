# scripts/limpieza.py

# ============================================
# Módulo de limpieza de datos
# Proyecto: A la deriva - Análisis de cetáceos
# Autor: Cecilia Mendoza Peña
# Última actualización: [30/04/2025]
# ============================================



# =====================
# Librerías necesarias
# =====================
import pandas as pd


# --------------------------------------------
# 1. Cargar dataset
# --------------------------------------------

def cargar_dataset(ruta):
    """
    Carga un archivo CSV en formato TSV (tab-separated) y lo convierte en un DataFrame.

    Parámetros:
        ruta (str): Ruta relativa o absoluta al archivo CSV.

    Retorna:
        df (DataFrame): Dataset cargado.
    """
    return pd.read_csv(
        ruta,
        sep='\t',
        on_bad_lines='skip',   # Evita errores por filas mal formateadas
        low_memory=False
    )

# --------------------------------------------
# 2. Estandarizar nombres de columnas
# --------------------------------------------

def limpiar_nombres_columnas(df):
    """
    Estandariza los nombres de las columnas:
    - Minúsculas
    - Reemplaza espacios por guiones bajos
    - Elimina acentos y caracteres especiales

    Parámetros:
        df (DataFrame): Dataset original.

    Retorna:
        df (DataFrame): Dataset con nombres de columnas limpios.
    """
    df.columns = (
        df.columns.str.strip()
                   .str.lower()
                   .str.replace(" ", "_")
                   .str.normalize("NFKD")
                   .str.encode("ascii", errors="ignore")
                   .str.decode("utf-8")
                   .str.replace(r"[^\w\s]", "", regex=True)
    )
    return df

# --------------------------------------------
# 3. Filtrar por año
# --------------------------------------------

def filtrar_por_anio(df, anio_min=2000, anio_max=2024):
    """
    Filtra el DataFrame por un rango de años en la columna 'year'.

    Parámetros:
        df (DataFrame): Dataset con columna 'year'.
        anio_min (int): Año mínimo permitido.
        anio_max (int): Año máximo permitido.

    Retorna:
        df (DataFrame): Dataset filtrado por año.
    """
    return df[(df["year"] >= anio_min) & (df["year"] <= anio_max)]

# --------------------------------------------
# 4. Eliminar registros irrelevantes
# --------------------------------------------

def eliminar_filas_irrelevantes(df):
    """
    Elimina duplicados y registros sin coordenadas (latitude y longitude).

    Parámetros:
        df (DataFrame): Dataset original.

    Retorna:
        df (DataFrame): Dataset limpio.
    """
    df = df.drop_duplicates()
    df = df.dropna(subset=["decimallatitude", "decimallongitude"])
    return df


# --------------------------------------------
# 5. Convertir fechas al formato datetime
# --------------------------------------------

# Ya no se usa. Función reemplazada por 'extraer_anio_mes()', que es más robusta.

def convertir_a_fecha(df): 
    """
    Convierte la columna 'eventDate' a tipo datetime.
    Extrae columnas auxiliares 'anio' y 'mes'.

    Parámetros:
        df (DataFrame): Dataset con columna 'eventDate'.

    Retorna:
        df (DataFrame): Dataset con columnas 'anio' y 'mes' procesadas.
    """
    df["eventdate"] = pd.to_datetime(df["eventdate"], errors="coerce")
    df["anio"] = df["eventdate"].dt.year
    df["mes"] = df["eventdate"].dt.month
    return df

# --------------------------------------------
# 6. Extraer año y mes desde columnas separadas
# --------------------------------------------

def extraer_anio_mes(df):
    """
    Extrae las columnas 'anio' y 'mes' combinando 'eventDate' y, en caso de fallo o nulo,
    rellena con 'year' y 'month' para asegurar completitud.

    Parámetros:
        df (DataFrame): Dataset con columnas 'eventDate', 'year' y 'month'.

    Retorna:
        df (DataFrame): Dataset con 'anio' y 'mes' completas y trazables.
    """
    df["eventdate"] = pd.to_datetime(df["eventdate"], errors="coerce")

    df["anio"] = df["eventdate"].dt.year
    df["mes"] = df["eventdate"].dt.month

    df["anio"] = df["anio"].fillna(df["year"])
    df["mes"] = df["mes"].fillna(df["month"])

    return df


# --------------------------------------------
# 7. Mapeo de provincias y variantes a Comunidades Autónomas
# --------------------------------------------

# Función de limpieza para mapear provincias y variantes a comunidades autónomas
def mapear_comunidades_autonomas(df):
    """
    Normaliza y agrupa valores de la columna 'stateprovince' en 17 comunidades autónomas + 'no asignado'.
    Devuelve el DataFrame original con una nueva columna 'comunidad_autonoma'.
    """
    # Crear una copia normalizada, sin alterar la original
    state_norm = df["stateprovince"].str.lower().str.strip()


    mapa = {
        # Andalucía
        "sevilla": "andalucía", "cádiz": "andalucía", "cádiz": "andalucía", "huelva": "andalucía",
        "granada": "andalucía", "jaén": "andalucía", "jaen": "andalucía", "almería": "andalucía",
        "cordoba": "andalucía", "málaga": "andalucía", "malaga": "andalucía", "andalucía": "andalucía",

        # Aragón
        "zaragoza": "aragón", "huesca": "aragón", "teruel": "aragón",

        # Asturias
        "asturias": "asturias", "principado de asturias": "asturias",

        # Cantabria
        "cantabria": "cantabria",

        # Castilla y León
        "valladolid": "castilla y león", "león": "castilla y león", "zamora": "castilla y león",
        "burgos": "castilla y león", "palencia": "castilla y león", "soria": "castilla y león",
        "avila": "castilla y león", "segovia": "castilla y león", "castilla y león": "castilla y león",

        # Castilla-La Mancha
        "cuenca": "castilla-la mancha", "albacete": "castilla-la mancha", "toledo": "castilla-la mancha",
        "guadalajara": "castilla-la mancha", "ciudad real": "castilla-la mancha",

        # Cataluña
        "barcelona": "cataluña", "girona": "cataluña", "lleida": "cataluña", "tarragona": "cataluña",
        "cataluña": "cataluña", "catalonia": "cataluña",

        # Comunidad Valenciana
        "valencia": "comunidad valenciana", "alicante": "comunidad valenciana",
        "castellón": "comunidad valenciana", "castelló": "comunidad valenciana",
        "castellón/castelló": "comunidad valenciana", "valencia/valència": "comunidad valenciana",
        "comunidad valenciana": "comunidad valenciana", "alicante/alicant": "comunidad valenciana",

        # Extremadura
        "badajoz": "extremadura", "cáceres": "extremadura",

        # Galicia
        "a coruña": "galicia", "la coruña": "galicia", "la coruna": "galicia", "lugo": "galicia",
        "ourense": "galicia", "pontevedra": "galicia", "galicia": "galicia",

        # Madrid
        "madrid": "madrid",

        # Murcia
        "murcia": "murcia", "región de murcia": "murcia",

        # Navarra
        "navarra": "navarra",

        # País Vasco
        "bizkaia": "país vasco", "gipuzkoa": "país vasco", "guipúzcoa": "país vasco", "guipuzcoa": "país vasco",
        "álava": "país vasco", "alava": "país vasco", "país vasco": "país vasco",

        # La Rioja
        "la rioja": "la rioja",

        # Islas Baleares
        "illes balears": "islas baleares", "islas baleares": "islas baleares",

        # Canarias
        "santa cruz de tenerife": "canarias", "las palmas": "canarias", "islas canarias": "canarias",
        "canarias, canary islands": "canarias", "canary islands": "canarias", "canarias": "canarias",

        # No asignado
        "mar": "no asignado", "northern atlantic ocean": "no asignado", "desconocido": "no asignado",
        "": "no asignado"
    }

    df["comunidad_autonoma"] = state_norm.replace(mapa)
    return df

