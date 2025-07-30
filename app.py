import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Comparador de Universidades", layout="wide")

# Estilo empresarial y sobrio
st.markdown("""
<style>
/* Título principal */
.big-title {
    font-size: 30px !important;
    font-weight: 600;
    color: #002060;
    margin-bottom: 0.5rem;
}
.sub-title {
    font-size: 16px;
    color: #444;
    margin-top: -10px;
    margin-bottom: 1rem;
}

/* Tipografía general */
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
}

/* Margen superior reducido */
section.main > div:first-child {
    padding-top: 0rem;
}

/* Encabezados markdown */
h1, h2, h3 {
    color: #1a1a1a;
    font-weight: 500;
}

hr {
    border: none;
    border-top: 1px solid #ccc;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Navegación principal
st.sidebar.title("📚 Índice")
pagina = st.sidebar.radio("Selecciona una sección:", [
    "📘 Descripción del Proyecto",
    "🎓 Comparador de Becas para Grado",
    "🎓 Comparador de Becas para Máster",
    "💡 Recomendaciones para IE"
])

st.markdown('<div class="big-title">Comparador de Universidades por Ayuda Financiera</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Proyecto de Benchmarking · IE University · Verano 2025 · Valentina Bailon Cano</div>', unsafe_allow_html=True)


# Página 1 - Descripción del Proyecto
if pagina == "📘 Descripción del Proyecto":
    st.title("📘 Descripción del Proyecto")
    st.markdown("""
Este proyecto ha sido desarrollado como parte de una práctica profesional en el Departamento de Financial Aid de **IE University**, con el objetivo de realizar un análisis estructurado de las políticas de ayuda financiera de universidades líderes a nivel internacional.

La iniciativa responde a la necesidad de disponer de una herramienta comparativa clara, interactiva y profesional que permita evaluar la competitividad de la oferta de becas de IE frente a otras instituciones, identificando fortalezas, oportunidades de mejora y buenas prácticas replicables.

---

### 🎯 Objetivo Estratégico

Desarrollar una plataforma de benchmarking que permita:

- Evaluar el nivel de transparencia, cobertura y diversidad de las ayudas financieras ofrecidas por universidades internacionales.
- Comparar procesos, documentación, calendarios y herramientas digitales utilizadas en la comunicación de becas.
- Apoyar la toma de decisiones internas en IE University mediante datos estructurados y visualización interactiva.
- Servir como punto de referencia para implementar mejoras en el posicionamiento de la oferta institucional de IE.

---

### 🧩 Estructura del Proyecto

El sistema se organiza en cuatro módulos principales:

1. **Comparador de Becas para Programas de Grado** 
2. **Comparador de Becas para Programas de Máster**
3. **Recomendaciones Estratégicas para IE University**
4. **Descripción General y Propósito del Proyecto**

---

### ⚙️ Tecnología y Enfoque Metodológico

La solución ha sido desarrollada utilizando tecnologías de código abierto y un enfoque modular que permite su escalabilidad futura.  
Se ha empleado:

- **Python**, con soporte de bibliotecas como **Streamlit**, **Pandas** y **Plotly**.
- Visualizaciones interactivas y tablas comparativas en tiempo real.
- Infraestructura basada en **Streamlit Cloud** para despliegue público y GitHub como repositorio de código y control de versiones.

---

### 👩‍💼 Autora del Proyecto

Este proyecto ha sido desarrollado de forma individual por **Valentina Bailon Cano**, estudiante de Business Analytics y miembro del equipo de prácticas del Departamento de Ayuda Financiera de IE University, con el objetivo de generar valor institucional y aplicabilidad real.
""")



# Página 2 - Comparador de Grado
elif pagina == "🎓 Comparador de Becas para Grado":
    st.title("🎓 Comparador de Becas para Grado")
    st.markdown("""
Esta sección permite comparar la estrategia de ayuda financiera de universidades internacionales en titulaciones de grado.
Los datos provienen de un análisis realizado por IE University en verano de 2025.  
Puedes seleccionar universidades en el menú lateral para explorar su oferta de becas, transparencia y soporte al estudiante.
""")

    @st.cache_data
    def load_undergrad_data():
        return pd.read_csv("data/benchmarking_undergraduate.csv")

    df_u = load_undergrad_data()

    st.sidebar.header("🔍 Filtros")
    universidades_u = st.sidebar.multiselect(
        "Selecciona universidades (grado):",
        options=df_u["University"].unique(),
        default=df_u["University"].unique()
    )

    df_u_filtered = df_u[df_u["University"].isin(universidades_u)]

    st.subheader("📊 Tabla Comparativa")
    st.dataframe(df_u_filtered, use_container_width=True)

    st.subheader("📈 Comparativa Visual (Radar)")

    score_map = {
        "None": 1, "Basic": 2, "Limited": 2, "Medium": 3,
        "Good": 4, "Clear": 4, "Defined": 4,
        "Very clear": 5, "Excellent": 5, "Descriptive + stats": 4,
        "Clear eligibility descriptions": 5, "Clear coverage": 4,
        "Clear per type": 4, "Aggregated only": 2,
        "User estimates": 3, "Not integrated": 2
    }

    for col in ["Transparency of Info", "Application Process Clarity", "Data Disclosure", "Timeline Visibility", "Tools & Support", "Web UX & Accessibility"]:
        df_u_filtered[col + " (Score)"] = df_u_filtered[col].map(score_map).fillna(3)

    if len(df_u_filtered) > 1:
        radar_df = df_u_filtered[["University"] + [col + " (Score)" for col in [
            "Transparency of Info", "Application Process Clarity", "Data Disclosure",
            "Timeline Visibility", "Tools & Support", "Web UX & Accessibility"
        ]]]
        radar_df = radar_df.set_index("University").T
        st.plotly_chart(px.line_polar(
            radar_df.reset_index().melt(id_vars="index", var_name="University", value_name="Score"),
            r="Score", theta="index", color="University", line_close=True,
            title="Indicadores clave por universidad (Grado)"
        ), use_container_width=True)
    else:
        st.info("Selecciona al menos dos universidades para ver el gráfico radar.")

    if len(df_u_filtered) == 1:
        st.subheader("📄 Ficha Detallada")
        uni = df_u_filtered.iloc[0]
        st.markdown(f"### 🎓 {uni['University']}")
        st.markdown(f"**Tipos de ayuda**: {uni['Types of Aid']}")
        st.markdown(f"**Importe de las becas**: {uni['Scholarship Amounts']}")
        st.markdown(f"**Transparencia**: {uni['Transparency of Info']}")
        st.markdown(f"**Claridad del proceso**: {uni['Application Process Clarity']}")
        st.markdown(f"**Divulgación de datos**: {uni['Data Disclosure']}")
        st.markdown(f"**Visibilidad del calendario**: {uni['Timeline Visibility']}")
        st.markdown(f"**Préstamos ofrecidos**: {uni['Loans Offered']}")
        st.markdown(f"**Herramientas y soporte**: {uni['Tools & Support']}")
        st.markdown(f"**Accesibilidad web**: {uni['Web UX & Accessibility']}")
        st.markdown(f"**Coste de vida**: {uni['Cost of Living Info']}")
        st.markdown(f"**Valoración Global**: {uni['Overall Impression']} / 5 ⭐")

    st.subheader("🏆 Ranking por Valoración Global")
    ranking_df_u = df_u_filtered.sort_values(by="Overall Impression", ascending=False)

    fig = px.bar(
        ranking_df_u,
        x="Overall Impression",
        y="University",
        orientation='h',
        color="Overall Impression",
        color_continuous_scale="Blues",
        title="Universidades ordenadas por valoración general (Grado)",
        labels={"Overall Impression": "Valoración", "University": "Universidad"}
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

    st.download_button(
        label="⬇️ Descargar Comparativa (Grado)",
        data=ranking_df_u.to_csv(index=False).encode('utf-8'),
        file_name="benchmarking_undergraduate.csv",
        mime="text/csv"
    )


# Página 3 - Comparador de Máster
elif pagina == "🎓 Comparador de Becas para Máster":
    st.title("🎓 Comparador de Becas para Máster")
    st.markdown("""
Esta aplicación permite comparar las políticas de ayuda financiera de distintas universidades internacionales.
Los datos provienen de un análisis realizado por IE University en verano de 2025.  
Puedes seleccionar universidades en el menú lateral para explorar su oferta de becas, nivel de transparencia y herramientas de apoyo.
""")

    @st.cache_data
    def load_data():
        return pd.read_csv("data/benchmarking_master.csv")

    df = load_data()

    st.sidebar.header("🔍 Filtros")
    universidades = st.sidebar.multiselect(
        "Selecciona universidades:",
        options=df["University"].unique(),
        default=df["University"].unique()
    )

    df_filtered = df[df["University"].isin(universidades)]

    st.subheader("📊 Tabla Comparativa")
    st.dataframe(df_filtered, use_container_width=True)

    st.subheader("📈 Comparativa Visual (Radar)")

    scale_map = {
        "None": 1, "Basic": 2, "Limited": 2, "Medium": 3, "Some stats": 3,
        "Good": 4, "Defined": 4, "Structured": 4,
        "High": 5, "Very clear": 5, "Excellent": 5, "Descriptive + stats": 4,
        "Clear explanations": 5, "Strong descriptions": 4, "Centralized portal": 5,
        "Detailed listings": 4, "Clear": 4
    }

    for col in ["Transparency", "App Process Clarity", "Data Disclosure", "Timeline Visibility", "Tools & Support", "UX & Accessibility"]:
        df_filtered[col + " (Score)"] = df_filtered[col].map(scale_map).fillna(3)

    if len(df_filtered) > 1:
        radar_df = df_filtered[["University"] + [col + " (Score)" for col in ["Transparency", "App Process Clarity", "Data Disclosure", "Timeline Visibility", "Tools & Support", "UX & Accessibility"]]]
        radar_df = radar_df.set_index("University").T
        st.plotly_chart(px.line_polar(
            radar_df.reset_index().melt(id_vars="index", var_name="University", value_name="Score"),
            r="Score", theta="index", color="University", line_close=True,
            title="Criterios de Evaluación por Universidad"
        ), use_container_width=True)
    else:
        st.info("Selecciona al menos dos universidades para ver el gráfico radar.")

    if len(df_filtered) == 1:
        st.subheader("📄 Ficha Detallada")
        uni = df_filtered.iloc[0]
        st.markdown(f"### 🎓 {uni['University']}")
        st.markdown(f"**Tipos de ayuda**: {uni['Types of Aid']}")
        st.markdown(f"**Importe de las becas**: {uni['Scholarship Amounts']}")
        st.markdown(f"**Transparencia**: {uni['Transparency']}")
        st.markdown(f"**Claridad del proceso**: {uni['App Process Clarity']}")
        st.markdown(f"**Divulgación de datos**: {uni['Data Disclosure']}")
        st.markdown(f"**Visibilidad del calendario**: {uni['Timeline Visibility']}")
        st.markdown(f"**Información sobre préstamos**: {uni['Loans Offered']}")
        st.markdown(f"**Herramientas y soporte**: {uni['Tools & Support']}")
        st.markdown(f"**Accesibilidad y experiencia web**: {uni['UX & Accessibility']}")
        st.markdown(f"**Información sobre coste de vida**: {uni['Cost of Living Info']}")
        st.markdown(f"**Puntuación Global**: {uni['Overall Rating']} / 5 ⭐")

    st.subheader("🏆 Ranking por Puntuación Global")
    ranking_df = df_filtered.sort_values(by="Overall Rating", ascending=False)

    fig = px.bar(
        ranking_df,
        x="Overall Rating",
        y="University",
        orientation='h',
        color="Overall Rating",
        color_continuous_scale="Blues",
        title="Universidades ordenadas por puntuación global",
        labels={"Overall Rating": "Puntuación", "University": "Universidad"}
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

    st.download_button(
        label="⬇️ Descargar Ranking como CSV",
        data=ranking_df.to_csv(index=False).encode('utf-8'),
        file_name="ranking_universidades.csv",
        mime="text/csv"
    )

# Página 4 - Recomendaciones
elif pagina == "💡 Recomendaciones para IE":
    st.title("💡 Recomendaciones Estratégicas para el Departamento FAID")
    st.markdown("""
Estas recomendaciones están basadas en el análisis detallado de las páginas, procesos y políticas de ayuda financiera de universidades líderes en **grado y máster**, con el objetivo de fortalecer la propuesta de valor de IE frente a sus principales competidores directos en cada nivel.

---

## 🎓 Recomendaciones para GRADO

### 1. 📱 Mini app financiera pre-admisión
- Crear una **aplicación ligera o simulador interactivo** para móviles que muestre:
  - Coste total estimado por campus (Segovia/Madrid)
  - Ayudas disponibles por nacionalidad o perfil
  - Calendario de aplicación personalizado
- Esta app podría usarse como herramienta promocional en ferias o visitas.

### 2. 💬 Test de perfil financiero orientativo (sin compromiso)
- Implementar un test anónimo y visual donde el candidato pueda indicar:
  - Nacionalidad, ingresos familiares aproximados, tipo de programa
  - Interés en financiación o becas

- El sistema le sugiere:
  - Si su perfil encaja con ayudas disponibles
  - Qué tipo de documentación le será útil
  - Qué opciones financieras suele solicitar un perfil similar

> *Esto ayuda al alumno a preparar la solicitud con antelación y mejora la percepción de accesibilidad sin comprometer datos reales.*


> *KCL y Erasmus, por ejemplo, sí publican datos de contexto o cifras institucionales básicas.*

### 3. 🗺️ Mapa visual de ayudas por región/país
- Una sección visual en la web que permita seleccionar país y ver las becas activas, requisitos y estadísticas.

### 4. 🧾 Prevalidación informal de perfil
- Herramienta sin necesidad de login donde un candidato puede indicar: nacionalidad, programa deseado y situación financiera aproximada → y recibe:
  - Nivel orientativo de elegibilidad
  - Tipos de ayuda más probables
  - Documentación sugerida

---

## 🎓 Recomendaciones para MÁSTER

### 5. 📈 Transparencia sobre tasas de concesión
- Publicar rangos históricos orientativos del porcentaje de solicitudes de beca aprobadas por programa (MIM, MBA, etc.).
- Puede ser por tramos: `<25%`, `25–50%`, `>50%`.

> *Esto ya lo hace HEC Paris, Bocconi y parcialmente LBS, aumentando la confianza y segmentación de los candidatos.*

### 6. 💼 Segmentación avanzada en simulador financiero
- Mejorar el simulador para que:
  - Permita seleccionar programa exacto (no solo School)
  - Incluya tasas de éxito estimadas según perfil (edad, país, experiencia)
  - Genere informe descargable o compartible

### 7. 📬 Paquete informativo post-beca (claridad en siguiente paso)
- Después de recibir la beca, enviar un "Pack FAID" con:
  - Desglose financiero personalizado
  - Opciones reales de financiación y aplazamiento
  - Calendario y fecha límite para confirmar plaza

> *Esto ayuda a que el alumno no abandone la matriculación tras recibir la beca.*

### 8. 🧠 Visibilidad de criterios cualitativos en la evaluación
- Incluir en la web ejemplos de perfiles o factores cualitativos que FAID valora (impacto, trayectoria, motivación, etc.).
- Evita percepción de opacidad o arbitrariedad.

---

## 🌍 Recomendaciones Comunes

### 9. 🌱 Becas estratégicas temáticas visibles
- Crear una línea de becas con visibilidad internacional en temas como:
  - Tecnología con propósito
  - Liderazgo femenino
  - Impacto social en mercados emergentes
- Aumenta la percepción de compromiso institucional y se alinea con tendencias globales.

### 10. 📣 Casos de éxito reales, orientados a Financial Aid
- Publicar en la sección de becas:
  - Historias de candidatos que consiguieron ayuda y su trayectoria posterior
  - Preferiblemente por programa y región
- Mejora percepción de accesibilidad real y promueve diversidad.

---

Estas propuestas tienen como objetivo **potenciar el área de FAID** como parte integral de la experiencia del candidato, aumentar la conversión tras concesión de becas y posicionar a IE como una universidad clara, accesible y competitiva en ayuda financiera.
    """)


