# 📘 Comparador de Universidades por Ayuda Financiera – IE University

**Autores:** Valentina Bailon Cano y Beatriz De Marcos

**Proyecto desarrollado para:** Departamento de Financial Aid – IE University  
**Fecha:** Verano 2025  
**Tecnologías:** Python · Streamlit · Pandas · Plotly · GitHub · OCR

---

## 🎯 Objetivo del Proyecto

Este proyecto nace con el propósito de analizar y comparar las políticas de ayuda financiera de universidades internacionales de prestigio en titulaciones de **Grado** y **Máster**.  
El sistema permite a IE University:

- Evaluar su posicionamiento frente a competidores clave.
- Identificar buenas prácticas replicables en transparencia, claridad y soporte financiero.
- Mejorar la estrategia de comunicación y conversión en el área de becas.

---

## 🧩 Estructura de la Aplicación

La app está desarrollada en Python con Streamlit y se organiza en las siguientes secciones:

### 1. 📘 Descripción del Proyecto
Resumen institucional, objetivos, enfoque y metodología aplicada.

### 2. 🎓 Comparador de Becas para Grado
- Tabla interactiva con filtros por universidad.
- Radar Chart comparativo por criterios clave.
- Ficha individual de cada universidad.
- Ranking por valoración general.

### 3. 🎓 Comparador de Becas para Máster
- Mismo funcionamiento que la sección de Grado, pero orientado a másteres.
- Universidades como LBS, Bocconi, LSE, HEC, ESADE, etc.

### 4. 💡 Recomendaciones para IE University
Recomendaciones estratégicas separadas por GRADO y MÁSTER, orientadas a fortalecer la propuesta del departamento de FAID.

---

## 🗃️ Fuentes de Datos

Los datos han sido recopilados mediante investigación directa en páginas oficiales, simuladores y documentos públicos de universidades europeas y globales.  
- [`benchmarking_master.csv`](data/benchmarking_master.csv)  
- [`benchmarking_undergraduate.csv`](data/benchmarking_undergraduate.csv)

---

## 💡 Ejemplos de Recomendaciones para FAID

### Grado:
- Mini app de simulación de ayuda financiera personalizada.
- Test de perfil financiero sin compromiso.
- Representación visual del proceso de aplicación.

### Máster:
- Publicar tasas orientativas de concesión por programa y ronda.
- Segmentación avanzada en el simulador financiero.
- “Paquete post-beca” con orientación clara y calendario financiero.

---

## 🚀 Tecnologías Utilizadas

| Herramienta     | Uso Principal                              |
|-----------------|--------------------------------------------|
| `Streamlit`     | Desarrollo del frontend y backend de la app |
| `Pandas`        | Limpieza y manejo de datasets               |
| `Plotly`        | Visualizaciones interactivas (Radar, Bar)  |
| `GitHub`        | Control de versiones y despliegue en la nube|
| `OCR`           | Extracción de datos desde PDF escaneados    |

---

## 🖥️ Despliegue y Visualización

La aplicación está desplegada en **Streamlit Cloud** y puede ejecutarse localmente clonando este repositorio.

```bash
git clone https://github.com/valentinabailoncano-code/Comparativa_Universidades.git
cd Comparativa_Universidades
pip install -r requirements.txt
streamlit run main.py
```
--- 
## 📬 Contacto

Este proyecto ha sido desarrollado de forma individual como parte de una iniciativa de mejora estratégica dentro del área de ayuda financiera de **IE University**.

**Valentina Bailon Cano**  
Estudiante de Business Analytics – Universidad Pontificia Comillas (ICADE)  
Prácticas de Verano 2025 – Departamento FAID – IE University  
[LinkedIn](https://www.linkedin.com/in/valentinabailoncano)

**Beatriz De Marcos**
Estudiante de Administración de Empresa en Inglés- Universidad Pontificia Comillas (ICADE)
Prácticas de Verano 2025 – Departamento FAID – IE University  
