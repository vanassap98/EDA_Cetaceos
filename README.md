# A la deriva: análisis exploratorio de la distribución de cetáceos en España (1990–2024)
**Repositorio del proyecto personal de ciencia de datos enfocado en biodiversidad marina.**  
Este análisis exploratorio de datos (EDA) estudia los registros de observación de cetáceos en las costas españolas a lo largo del tiempo, extraídos de la plataforma GBIF.

## Objetivos del proyecto

- Estudiar los patrones espaciales y temporales de observación de cetáceos en España.
- Identificar las especies más observadas y sus distribuciones geográficas.
- Evaluar si existen diferencias entre regiones (Atlántico vs. Mediterráneo).
- Investigar posibles desplazamientos o cambios de distribución de especies concretas.

---

## Dataset

- **Fuente**: GBIF (Global Biodiversity Information Facility).
- **Formato**: CSV (descarga directa desde el portal GBIF).
- **Cobertura temporal**: Últimos 24 años.
- **Variables destacadas**: nombre_cientifico, anio, mes, latitud, longitud

---

## Herramientas utilizadas

- `Python`: pandas, numpy, matplotlib, seaborn, plotly, geopandas, folium
- `Jupyter Notebook`
- Notion y GitHub para documentación

---


## Estructura del repositorio

EDA_Cetaceos/
│
├── README.md
├── requirements.txt
│
├── docs/
│   ├── Memoria.pdf
│   └── Presentacion.pdf
│
├── src/
│   ├── data/
│   │   ├── raw/             # Datos originales (GBIF)
│   │   └── clean/           # Dataset limpio
│   │
│   ├── notebooks/
│   │   ├── EDA_cetaceos.ipynb
│   │   └── informe_cetaceos.ipynb
│   │
│   ├── scripts/
│   │   ├── limpieza.py
│   │   ├── visualizacion.py
│   │   └── comunicacion.py
│   │
│   └── outputs/
│       ├── figuras/
│       └── mapas_interactivos/



---

## Notebooks

- `EDA_cetaceos.ipynb`: análisis exploratorio principal del dataset.
- `informe_cetaceos.ipynb`: generación de visualizaciones finales para la presentación y memoria.

---

## Preguntas clave
- ¿Qué especies de cetáceos se observan con más frecuencia en las costas españolas?
- ¿Existen patrones estacionales o tendencias temporales claras?
- ¿Qué diferencias hay entre las regiones Atlántica y Mediterránea?
- ¿Se ha modificado la distribución de alguna especie concreta a lo largo del tiempo?

---

## Autora

**Cecilia Mendoza**  
Bióloga ambiental especializada en ciencia de datos y conservación.  
[LinkedIn](https://www.linkedin.com/in/cecilia-mendoza-/) 

---
