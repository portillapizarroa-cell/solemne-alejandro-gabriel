
import pandas as pd
import streamlit as st

CSV_URL = "https://datos.gob.cl/uploads/recursos/oficinasTelefonosSucursales.csv"

st.set_page_config(page_title="Oficinas y Teléfonos de Sucursales", page_icon="📊", layout="wide")

@st.cache_data(ttl=3600, show_spinner=True)
def load_data():
    try:
        df = pd.read_csv(CSV_URL, encoding="utf-8", sep=",")
        if df.shape[1] == 1:
            df = pd.read_csv(CSV_URL, encoding="utf-8", sep=";")
    except Exception:
        df = pd.read_csv(CSV_URL, encoding="latin1", sep=";")
    df.columns = [c.strip() for c in df.columns]
    return df

def pick_col(df, options):
    for name in options:
        if name in df.columns:
            return name
    return None

def text_filter(df, text):
    if not text:
        return df
    text = text.strip()
    mask = df.apply(lambda row: row.astype(str).str.contains(text, case=False, na=False).any(), axis=1)
    return df[mask]

def main():
    st.title("📊 Oficinas y Teléfonos de Sucursales")
    st.caption(f"Fuente de datos: {CSV_URL}")

    try:
        df = load_data()
    except Exception as e:
        st.error("No se pudieron cargar los datos del CSV.")
        st.exception(e)
        return

    if df.empty:
        st.warning("⚠️ No hay datos disponibles para mostrar.")
        return

    col_region = pick_col(df, ["Región", "Region", "REGION", "region"])
    col_comuna = pick_col(df, ["Comuna", "COMUNA", "comuna"])
    col_ciudad = pick_col(df, ["Ciudad", "CIUDAD", "ciudad"])
    col_tipo = pick_col(df, ["Tipo", "TIPO", "tipo"])

    with st.sidebar:
        st.header("Filtros")
        q = st.text_input("🔎 Búsqueda global", placeholder="Ej: Santiago, Servicio, 22...")
        region_sel = st.multiselect("Región", sorted(df[col_region].dropna().astype(str).unique().tolist())) if col_region else []
        comuna_sel = st.multiselect("Comuna", sorted(df[col_comuna].dropna().astype(str).unique().tolist())) if col_comuna else []
        ciudad_sel = st.multiselect("Ciudad", sorted(df[col_ciudad].dropna().astype(str).unique().tolist())) if col_ciudad else []
        tipo_sel = st.multiselect("Tipo", sorted(df[col_tipo].dropna().astype(str).unique().tolist())) if col_tipo else []

    filtered = df.copy()
    if region_sel and col_region:
        filtered = filtered[filtered[col_region].astype(str).isin(region_sel)]
    if comuna_sel and col_comuna:
        filtered = filtered[filtered[col_comuna].astype(str).isin(comuna_sel)]
    if ciudad_sel and col_ciudad:
        filtered = filtered[filtered[col_ciudad].astype(str).isin(ciudad_sel)]
    if tipo_sel and col_tipo:
        filtered = filtered[filtered[col_tipo].astype(str).isin(tipo_sel)]

    filtered = text_filter(filtered, q)

    c1, c2, c3 = st.columns(3)
    c1.metric("Registros totales", len(df))
    c2.metric("Registros filtrados", len(filtered))
    c3.metric("Columnas", df.shape[1])

    st.subheader("Tabla")
    st.dataframe(filtered, use_container_width=True)

    if col_region:
        st.subheader("Distribución por Región")
        st.bar_chart(filtered[col_region].value_counts())

    csv_bytes = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Descargar CSV filtrado",
        data=csv_bytes,
        file_name="oficinas_filtrado.csv",
        mime="text/csv",
    )

if __name__ == "__main__":
    main()
