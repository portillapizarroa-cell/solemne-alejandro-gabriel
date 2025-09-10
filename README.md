
# 🏢 Oficinas, Teléfonos y Sucursales (Chile)

App Streamlit que consume el CSV público de datos.gob.cl:
- **Fuente**: https://datos.gob.cl/uploads/recursos/oficinasTelefonosSucursales.csv

## ✨ Funciones
- Descarga y lectura robusta (varios encodings y separadores).
- Búsqueda global por texto.
- Filtros por Región / Comuna / Ciudad / Tipo si existen esas columnas.
- Gráfico de conteo por Región (si la columna existe).
- Descarga del CSV filtrado.

## ▶️ Ejecutar localmente
```bash
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ Streamlit Cloud
Sube `app.py` y `requirements.txt` a la raíz de un repo público y despliega con **Main file path: app.py**.
