
import io
import requests
import pandas as pd
import streamlit as st
import altair as alt

CSV_URL = "https://datos.gob.cl/uploads/recursos/oficinasTelefonosSucursales.csv"

st.set_page_config(page_title="Oficinas, Teléfonos y Sucursales - Chile", page_icon="🏢", layout="wide")
st.title("🏢 Oficinas, Teléfonos y Sucursales (Chile)")
st.caption("Fuente: datos.gob.cl")

@st.cache_data(show_spinner=True)
def fetch_csv(url: str) -> pd.DataFrame:
    # Descarga el CSV desde la URL y lo carga en un DataFrame, probando encodings comunes y separadores.
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    for enc in ("utf-8-sig", "utf-8", "latin-1", "cp1252"):
        # intento con separador por defecto
        try:
            return pd.read_csv(io.BytesIO(resp.content), encoding=enc)
        except UnicodeDecodeError:
            pass
        except Exception:
            # intento con separador ';'
            try:
                return pd.read_csv(io.BytesIO(resp.content), encoding=enc, sep=";")
            except Exception:
                pass
    # último intento sin encoding explícito
    return pd.read_csv(io.BytesIO(resp.content))

try:
    df = fetch_csv(CSV_URL)
except Exception as e:
    st.error(f"Error al descargar o leer el CSV: {e}")
    st.stop()

# Limpieza básica de columnas
df.columns = [c.strip() for c in df.columns]

st.subheader("👀 Vista rápida")
st.write("Filtra por texto o por columnas si existen (Región, Ciudad, Comuna, Dirección, Teléfono, etc.).")

# Búsqueda de texto libre
q = st.text_input("🔎 Búsqueda global (coincidencia en cualquier columna)", "")
filtered = df.copy()

if q:
    q_lower = q.lower()
    mask = df.apply(lambda s: s.astype(str).str.lower().str.contains(q_lower, na=False))
    filtered = df[mask.any(axis=1)]

# Filtros condicionales si existen las columnas
def optional_select(label, candidates):
    for colname in candidates:
        if colname in df.columns:
            options = ["(Todas)"] + sorted([str(x) for x in df[colname].dropna().unique()])
            val = st.selectbox(f"{label} — columna: {colname}", options, key=colname)
            return colname, (None if val == "(Todas)" else val)
    return None, None

with st.expander("🔧 Filtros avanzados", expanded=True):
    reg_col, region_val = optional_select("Región", ["Region","REGION","REGIÓN","Región"])
    com_col, comuna_val = optional_select("Comuna", ["Comuna","COMUNA"])
    ciu_col, ciudad_val = optional_select("Ciudad", ["Ciudad","CIUDAD"])
    tip_col, tipo_val   = optional_select("Tipo",   [c for c in df.columns if "tipo" in c.lower()])

    if reg_col and region_val is not None:
        filtered = filtered[filtered[reg_col] == region_val]
    if com_col and comuna_val is not None:
        filtered = filtered[filtered[com_col] == comuna_val]
    if ciu_col and ciudad_val is not None:
        filtered = filtered[filtered[ciu_col] == ciudad_val]
    if tip_col and tipo_val is not None:
        filtered = filtered[filtered[tip_col] == tipo_val]

st.write(f"**Registros visibles:** {len(filtered):,} de {len(df):,}")

st.dataframe(filtered, use_container_width=True, hide_index=True)

# Grafico por región si existe
region_cols = [c for c in df.columns if c.lower() in ("region","región")]
if region_cols:
    st.subheader("📈 Conteo por Región")
    chart_df = filtered[region_cols[0]].value_counts(dropna=False).reset_index()
    chart_df.columns = ["Region", "Cantidad"]
    chart = alt.Chart(chart_df).mark_bar().encode(
        x=alt.X("Region:N", sort="-y"),
        y="Cantidad:Q",
        tooltip=["Region","Cantidad"]
    ).properties(height=320)
    st.altair_chart(chart, use_container_width=True)

# Botón de descarga
@st.cache_data
def to_csv_bytes(df_in: pd.DataFrame) -> bytes:
    return df_in.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    "⬇️ Descargar CSV filtrado",
    data=to_csv_bytes(filtered),
    file_name="oficinas_filtrado.csv",
    mime="text/csv",
)

st.info("Si alguna columna no aparece en los filtros, es porque el CSV no la contiene o viene con otro nombre. Usa la búsqueda global para encontrar registros.")
