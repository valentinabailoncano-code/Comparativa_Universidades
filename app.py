import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Comparador de Universidades", layout="wide")

# Navegación principal
st.sidebar.title("📚 Índice")
pagina = st.sidebar.radio("Selecciona una sección:", [
    "📘 Descripción del Proyecto",
    "🎓 Comparador de Becas para Grado",
    "🎓 Comparador de Becas para Máster",
    "💡 Recomendaciones para IE"
])

# Estilos visuales
st.markdown("""
<style>
.big-title {
    font-size:40px !important;
    font-weight: bold;
    color: #003262;
}
.sub-title {
    font-size:20px;
    color: #666666;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">📘 Comparador de Universidades por Ayuda Financiera</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Proyecto de Benchmarking – IE University · Verano 2025 · Desarrollado por Valentina Bailon Cano</div>', unsafe_allow_html=True)
st.markdown("---")

# Página 1 - Descripción del Proyecto
if pagina == "📘 Descripción del Proyecto":
    st.title("📘 Descripción del Proyecto")
    st.markdown("""
Este proyecto nace del análisis comparativo de las políticas de ayuda financiera de universidades internacionales de prestigio, realizado durante una práctica en el departamento de Financial Aid de IE University en verano de 2025.

### 🧭 Objetivo
Ofrecer una plataforma interactiva que permita comparar rápidamente el nivel de transparencia, tipos de becas, documentación requerida, calendario y herramientas que ofrecen distintas universidades.

### 🧩 Estructura del comparador
1. **Comparador para Grado** (en desarrollo)
2. **Comparador para Máster** (disponible)
3. **Recomendaciones estratégicas para IE University**

La app está desarrollada en Python con Streamlit, Plotly y Pandas.  
Desarrollada por: **Valentina Bailon Cano**
    """)

# Página 2 - Comparador de Grado
elif pagina == "🎓 Comparador de Becas para Grado":
    st.title("🎓 Comparador de Becas para Grado")
    st.info("🔧 Esta sección está actualmente en desarrollo. Pronto incluirá datos y visualizaciones comparativas para titulaciones de grado.")

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
    st.title("💡 Recomendaciones Estratégicas para IE University")
    st.markdown("""
Basado en el análisis de 12 universidades top europeas y globales, IE podría mejorar su estrategia de ayuda financiera en los siguientes aspectos:

---

### 🧭 1. Mayor Transparencia de Datos
- Publicar estadísticas reales sobre:
  - % de estudiantes becados
  - Importe medio
  - Presupuesto total de becas

### 🤝 2. Más Herramientas de Apoyo al Usuario
- Añadir calculadoras de elegibilidad / estimadores.
- Incluir un chatbot funcional o guía interactiva.

### 🌍 3. Información de Coste de Vida más Visible
- Integrar los costes mensuales directamente en las páginas de becas.
- Comparativas entre Segovia y Madrid.

### 🗓️ 4. Mejores Cronogramas y Visibilidad de Rondas
- Mostrar fechas claras para cada tipo de ayuda.
- Especificar impacto de aplicar en Ronda 1 vs 4.

### 💬 5. Centralización del Portal
- Unificar becas, préstamos, y FAQ en una sola página intuitiva.

---

Estas ideas pueden posicionar a IE como referente europeo no solo en diversidad de fondos, sino también en **claridad y experiencia del usuario**.
    """)