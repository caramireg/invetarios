# Herramienta Didáctica de Gestión de Inventarios (SENA)

Esta aplicación fue creada como herramienta de apoyo para formaciones virtuales sobre gestión de inventarios, normalización y clasificación de datos, y manejo de archivos delimitados (CSV) en Excel.

## Cómo ejecutar localmente
1. Asegúrese de tener Python instalado.
2. Instale las dependencias ejecutando:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecute la aplicación con:
   ```bash
   streamlit run inventario_app.py
   ```

## Cómo desplegar en la web gratuitamente (Streamlit Community Cloud)
Para que sus aprendices puedan acceder a la herramienta mediante un enlace de internet, siga estos pasos:

1. **Crear cuenta en GitHub:** Si no la tiene, regístrese en [github.com](https://github.com/).
2. **Subir los archivos:**
   - Cree un nuevo repositorio (por ejemplo `inventario-sena`).
   - Suba los siguientes archivos a ese repositorio:
     - `inventario_app.py`
     - `requirements.txt`
     - La carpeta `.streamlit` y su contenido `config.toml` (opcional, para mantener los colores).
3. **Desplegar en Streamlit:**
   - Inicie sesión en [share.streamlit.io](https://share.streamlit.io/) vinculando su cuenta de GitHub.
   - Haga clic en **"New app"**.
   - Seleccione el repositorio que acaba de crear.
   - En *Main file path*, escriba `inventario_app.py`.
   - Haga clic en **"Deploy"**.

¡Listo! En un par de minutos le darán un enlace web público que podrá compartir con sus estudiantes.
