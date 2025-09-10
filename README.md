# 📊 Oficinas y Teléfonos de Sucursales (Streamlit)

App que consume el CSV público desde datos.gob.cl y permite buscar/filtrar y descargar resultados.

**Fuente:** https://datos.gob.cl/uploads/recursos/oficinasTelefonosSucursales.csv

## ▶️ Ejecutar localmente
```bash
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ Deploy en Streamlit Cloud
1. Sube `app.py` y `requirements.txt` a la **raíz** de un repo público de GitHub.
2. En https://streamlit.io/cloud → **New app**:
   - Branch: `main`
   - Main file path: `app.py`
3. Deploy.
