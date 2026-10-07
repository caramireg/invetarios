import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Gestión de Inventarios - Formación", page_icon="📦", layout="wide")

# Archivo de almacenamiento
DATA_FILE = "inventario.csv"

# ==========================================
# FUNCIONES DE DATOS
# ==========================================
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df["ID"] = df["ID"].astype(str)
        return df
    else:
        return pd.DataFrame(columns=["ID", "Nombre", "Categoría", "Cantidad", "Precio_Unitario", "Último_Movimiento"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# ==========================================
# ESTILOS CSS ADICIONALES
# ==========================================
st.markdown("""
    <style>
    .main-header { font-size: 2.5rem; color: #39A900; font-weight: bold; margin-bottom: 0px;}
    .sub-header { font-size: 1.2rem; color: #555555; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

df = load_data()

# ==========================================
# BARRA LATERAL (SIDEBAR)
# ==========================================
# Se utiliza el logo del SENA como aspecto institucional
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/8/83/Sena_Colombia_logo.svg", width=120)
st.sidebar.markdown("### Menú de Navegación")
menu = st.sidebar.radio("", ["🏠 Inicio (Dashboard)", "📥 Ingresar Elementos", "📤 Extraer Elementos", "📊 Gestión de Datos (CSV)"])

st.sidebar.divider()
st.sidebar.info("💡 **Herramienta Didáctica:** Creada para apoyar la formación virtual en gestión de inventarios y datos.")

# ==========================================
# PANTALLAS
# ==========================================

if menu == "🏠 Inicio (Dashboard)":
    st.markdown('<p class="main-header">Sistema de Gestión de Inventarios</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Panel de Control General</p>', unsafe_allow_html=True)
    
    if df.empty:
        st.info("👋 ¡Bienvenido! El inventario está vacío. Diríjase a 'Ingresar Elementos' para comenzar.")
    else:
        # Métricas (Tarjetas visuales)
        col1, col2, col3 = st.columns(3)
        total_items = df.shape[0]
        total_unidades = df["Cantidad"].sum()
        valor_total = (df["Cantidad"] * df["Precio_Unitario"]).sum()
        
        col1.metric("📦 Total de Referencias", total_items)
        col2.metric("🔢 Unidades Totales", f"{total_unidades:,}")
        col3.metric("💰 Valor Total del Inventario", f"${valor_total:,.2f}")
        
        st.divider()
        st.subheader("📋 Inventario Actual")
        
        # Mostrar tabla interactiva (resaltando cantidades bajas si es necesario)
        st.dataframe(df, use_container_width=True, hide_index=True)

elif menu == "📥 Ingresar Elementos":
    st.markdown('<p class="main-header">📥 Módulo de Entradas</p>', unsafe_allow_html=True)
    st.markdown("Registre productos nuevos o agregue existencias. *(Nota: El sistema normalizará automáticamente los textos a mayúsculas).*")
    
    with st.container(border=True):
        with st.form("ingreso_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                id_prod = st.text_input("ID del Producto (Ej: P-001) *")
                nombre = st.text_input("Nombre del Elemento *")
                categoria = st.selectbox("Categoría / Nivel de Criticidad", ["Alta", "Media", "Baja", "Materia Prima", "Insumo", "Producto Terminado"])
            with col2:
                cantidad = st.number_input("Cantidad a Ingresar", min_value=1, step=1)
                precio = st.number_input("Precio Unitario ($)", min_value=0.0, step=0.01)
                
            st.markdown("*Campos obligatorios")
            submit = st.form_submit_button("➕ Registrar Ingreso", type="primary")
            
            if submit:
                if not id_prod or not nombre:
                    st.error("⚠️ El ID y el Nombre son obligatorios.")
                else:
                    # Normalización
                    id_prod_norm = id_prod.strip().upper()
                    nombre_norm = nombre.strip().upper()
                    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    if id_prod_norm in df["ID"].values:
                        idx = df.index[df["ID"] == id_prod_norm].tolist()[0]
                        df.at[idx, "Cantidad"] += cantidad
                        df.at[idx, "Precio_Unitario"] = precio
                        df.at[idx, "Último_Movimiento"] = fecha_actual
                        st.success(f"✅ Se agregaron {cantidad} unidades al producto existente: **{nombre_norm}**.")
                    else:
                        nuevo_registro = pd.DataFrame([{
                            "ID": id_prod_norm,
                            "Nombre": nombre_norm,
                            "Categoría": categoria,
                            "Cantidad": cantidad,
                            "Precio_Unitario": precio,
                            "Último_Movimiento": fecha_actual
                        }])
                        df = pd.concat([df, nuevo_registro], ignore_index=True)
                        st.success(f"✅ Producto **{nombre_norm}** creado exitosamente.")
                    save_data(df)

elif menu == "📤 Extraer Elementos":
    st.markdown('<p class="main-header">📤 Módulo de Salidas</p>', unsafe_allow_html=True)
    st.markdown("Registre consumos o ventas para descontar del inventario.")
    
    if df.empty:
        st.warning("⚠️ No hay elementos en el inventario para extraer.")
    else:
        with st.container(border=True):
            with st.form("salida_form"):
                lista_productos = df["Nombre"] + " (ID: " + df["ID"] + ")"
                producto_seleccionado = st.selectbox("Seleccione el Producto", lista_productos)
                cantidad_salida = st.number_input("Cantidad a Extraer", min_value=1, step=1)
                
                submit_salida = st.form_submit_button("➖ Registrar Salida", type="primary")
                
                if submit_salida:
                    id_seleccionado = producto_seleccionado.split("(ID: ")[1].replace(")", "")
                    idx = df.index[df["ID"] == id_seleccionado].tolist()[0]
                    stock_actual = df.at[idx, "Cantidad"]
                    
                    if cantidad_salida > stock_actual:
                        st.error(f"❌ **Stock insuficiente.** Solo dispone de {stock_actual} unidades de {df.at[idx, 'Nombre']}.")
                    else:
                        df.at[idx, "Cantidad"] -= cantidad_salida
                        df.at[idx, "Último_Movimiento"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        save_data(df)
                        st.success(f"✅ Extracción exitosa. Quedan **{df.at[idx, 'Cantidad']}** unidades de {df.at[idx, 'Nombre']}.")

elif menu == "📊 Gestión de Datos (CSV)":
    st.markdown('<p class="main-header">📊 Gestión de Datos</p>', unsafe_allow_html=True)
    st.markdown("Exporte o importe la base de datos completa. Ideal para ejercicios prácticos de Excel.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.subheader("⬇️ Exportar Inventario")
            st.markdown("Descargue el estado actual en formato delimitado por comas (.csv).")
            if not df.empty:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Descargar CSV",
                    data=csv,
                    file_name='inventario_sena.csv',
                    mime='text/csv',
                    use_container_width=True
                )
            else:
                st.info("Inventario vacío.")
                
    with col2:
        with st.container(border=True):
            st.subheader("⬆️ Importar Inventario")
            st.markdown("Cargue un archivo .csv para sobreescribir la base de datos actual.")
            uploaded_file = st.file_uploader("Seleccionar archivo", type=["csv"], label_visibility="collapsed")
            if uploaded_file is not None:
                try:
                    df_imported = pd.read_csv(uploaded_file)
                    st.write("Vista previa:")
                    st.dataframe(df_imported.head(2), use_container_width=True)
                    if st.button("Confirmar Importación", type="primary", use_container_width=True):
                        save_data(df_imported)
                        st.success("✅ Datos importados. Vaya a 'Inicio' para verlos.")
                except Exception as e:
                    st.error(f"Error en el formato: {e}")
