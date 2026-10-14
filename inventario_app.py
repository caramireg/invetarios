import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="SENA - Simulador de Inventarios",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Archivos de almacenamiento
DATA_FILE = "inventario.csv"
KARDEX_FILE = "historial_kardex.csv"

# ==========================================
# ESTILOS CSS PERSONALIZADOS (UI MEJORADA)
# ==========================================
st.markdown("""
    <style>
    /* Encabezados */
    .main-header { 
        font-size: 2.3rem; 
        color: #39A900; 
        font-weight: 800; 
        margin-bottom: 0px;
        letter-spacing: -0.5px;
    }
    .sub-header { 
        font-size: 1.05rem; 
        color: #666666; 
        margin-bottom: 20px;
    }
    /* Estilo para las tarjetas de métricas (KPIs) */
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #E0E4E8;
        padding: 16px 20px;
        border-radius: 12px;
        border-left: 6px solid #39A900;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }
    /* Cajas pedagógicas */
    .pedagogical-box {
        background-color: #F4FBF0;
        border-left: 4px solid #39A900;
        padding: 12px 16px;
        border-radius: 6px;
        font-size: 0.92rem;
        color: #2B501E;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# FUNCIONES DE DATOS Y KARDEX
# ==========================================
COLUMNAS_INV = ["ID", "Nombre", "Categoría", "Cantidad", "Stock_Minimo", "Precio_Unitario", "Último_Movimiento"]
COLUMNAS_KAR = ["Fecha", "ID", "Nombre", "Tipo_Movimiento", "Cantidad", "Stock_Resultante"]

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df["ID"] = df["ID"].astype(str)
        # Compatibilidad con archivos CSV de la versión anterior
        if "Stock_Minimo" not in df.columns:
            df["Stock_Minimo"] = 5
        return df[COLUMNAS_INV]
    else:
        return pd.DataFrame(columns=COLUMNAS_INV)

def save_data(df):
    df[COLUMNAS_INV].to_csv(DATA_FILE, index=False)

def load_kardex():
    if os.path.exists(KARDEX_FILE):
        return pd.read_csv(KARDEX_FILE)
    else:
        return pd.DataFrame(columns=COLUMNAS_KAR)

def registrar_kardex(id_prod, nombre, tipo, cantidad, stock_final):
    df_k = load_kardex()
    nuevo = pd.DataFrame([{
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ID": id_prod,
        "Nombre": nombre,
        "Tipo_Movimiento": tipo,
        "Cantidad": cantidad,
        "Stock_Resultante": stock_final
    }])
    df_k = pd.concat([nuevo, df_k], ignore_index=True)
    df_k.to_csv(KARDEX_FILE, index=False)

def calcular_estado(row):
    if row["Cantidad"] == 0:
        return "🔴 Agotado"
    elif row["Cantidad"] <= row["Stock_Minimo"]:
        return "🟡 Reordenar"
    else:
        return "🟢 Óptimo"

def cargar_datos_ejemplo():
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    datos_demo = [
        {"ID": "EL-001", "Nombre": "MICROCONTROLADOR ESP32 WIFI/BT", "Categoría": "Insumo", "Cantidad": 35, "Stock_Minimo": 10, "Precio_Unitario": 28500.0, "Último_Movimiento": fecha},
        {"ID": "EL-002", "Nombre": "SENSOR DE HUMEDAD CAPACITIVO", "Categoría": "Insumo", "Cantidad": 8, "Stock_Minimo": 10, "Precio_Unitario": 8500.0, "Último_Movimiento": fecha},
        {"ID": "SO-001", "Nombre": "PANEL SOLAR MONOCRISTALINO 100W", "Categoría": "Producto Terminado", "Cantidad": 12, "Stock_Minimo": 5, "Precio_Unitario": 240000.0, "Último_Movimiento": fecha},
        {"ID": "SO-002", "Nombre": "BATERÍA CICLO PROFUNDO 12V 100AH", "Categoría": "Alta", "Cantidad": 3, "Stock_Minimo": 4, "Precio_Unitario": 680000.0, "Último_Movimiento": fecha},
        {"ID": "HE-001", "Nombre": "PONCHADORA CONECTORES MC4", "Categoría": "Media", "Cantidad": 15, "Stock_Minimo": 3, "Precio_Unitario": 65000.0, "Último_Movimiento": fecha},
        {"ID": "MP-001", "Nombre": "ROLLO CABLE AWG 12 ROJO (100M)", "Categoría": "Materia Prima", "Cantidad": 0, "Stock_Minimo": 2, "Precio_Unitario": 195000.0, "Último_Movimiento": fecha},
    ]
    df_demo = pd.DataFrame(datos_demo)
    save_data(df_demo)
    registrar_kardex("SISTEMA", "CARGA DE DATOS DEMO", "📥 Inicialización", len(datos_demo), 0)

df = load_data()

# ==========================================
# BARRA LATERAL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/8/83/Sena_Colombia_logo.svg", width=95)
    st.markdown("### Simulador de Inventarios")
    st.caption("Ambiente Virtual de Aprendizaje")
    
    menu = st.radio(
        "Navegación Principal",
        [
            "🏠 Panel de Control (Dashboard)",
            "📥 Registrar Entradas",
            "📤 Registrar Salidas",
            "📜 Historial Kardex",
            "📊 Datos y Archivos (CSV)"
        ],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Indicador rápido en barra lateral
    if not df.empty:
        alertas = df[df["Cantidad"] <= df["Stock_Minimo"]].shape[0]
        if alertas > 0:
            st.warning(f"⚠️ **{alertas} ítem(s)** en nivel crítico o agotado.")
        else:
            st.success("✅ Niveles de stock saludables.")
            
    st.info("💡 **Objetivo Didáctico:** Comprender el flujo de entradas/salidas, valoración de stock, punto de reorden y manejo de archivos CSV.")

# ==========================================
# 1. PANTALLA: DASHBOARD
# ==========================================
if menu == "🏠 Panel de Control (Dashboard)":
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        st.markdown('<p class="main-header">Panel de Control de Inventarios</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Monitoreo de existencias, valoración financiera y alertas de reabastecimiento</p>', unsafe_allow_html=True)
    with col_t2:
        st.write("")
        if st.button("🎲 Cargar Datos de Prueba", use_container_width=True, help="Carga un inventario de ejemplo para practicar en clase"):
            cargar_datos_ejemplo()
            st.rerun()

    if df.empty:
        st.info("👋 **¡El almacén está vacío!** Haz clic en el botón **'🎲 Cargar Datos de Prueba'** arriba a la derecha para explorar la herramienta con datos de ejemplo, o dirígete a **'📥 Registrar Entradas'**.")
    else:
        # Cálculos de vista
        df_view = df.copy()
        df_view["Valor_Total"] = df_view["Cantidad"] * df_view["Precio_Unitario"]
        df_view["Estado"] = df_view.apply(calcular_estado, axis=1)
        
        # 4 Tarjetas KPI
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        total_refs = df_view.shape[0]
        total_unidades = int(df_view["Cantidad"].sum())
        valor_inventario = df_view["Valor_Total"].sum()
        items_criticos = df_view[df_view["Cantidad"] <= df_view["Stock_Minimo"]].shape[0]
        
        kpi1.metric("📦 Referencias (SKUs)", f"{total_refs}")
        kpi2.metric("🔢 Unidades en Bodega", f"{total_unidades:,}")
        kpi3.metric("💰 Valor Total Inventario", f"${valor_inventario:,.0f}")
        kpi4.metric("⚠️ Stock Crítico / Bajo", f"{items_criticos}", delta="-Requiere atención" if items_criticos > 0 else "Óptimo", delta_color="inverse" if items_criticos > 0 else "normal")
        
        st.write("")
        
        # Pestañas para organizar Tabla vs Gráficos
        tab_tabla, tab_graficos = st.tabs(["📋 Explorador de Existencias", "📈 Análisis Gráfico"])
        
        with tab_tabla:
            # Barra de filtros interactivos
            f_col1, f_col2, f_col3 = st.columns([2, 1.5, 1.5])
            with f_col1:
                busqueda = st.text_input("🔍 Buscar por ID o Nombre del elemento:", placeholder="Ej: ESP32, Panel, EL-001...")
            with f_col2:
                categorias_disp = ["Todas"] + sorted(df_view["Categoría"].unique().tolist())
                filtro_cat = st.selectbox("📂 Filtrar por Categoría:", categorias_disp)
            with f_col3:
                filtro_est = st.selectbox("🚦 Filtrar por Estado de Stock:", ["Todos", "🟢 Óptimo", "🟡 Reordenar", "🔴 Agotado"])
            
            # Aplicar filtros
            if busqueda:
                df_view = df_view[df_view["Nombre"].str.contains(busqueda.upper(), na=False) | df_view["ID"].str.contains(busqueda.upper(), na=False)]
            if filtro_cat != "Todas":
                df_view = df_view[df_view["Categoría"] == filtro_cat]
            if filtro_est != "Todos":
                df_view = df_view[df_view["Estado"] == filtro_est]
                
            max_cant = int(df["Cantidad"].max()) if not df.empty and df["Cantidad"].max() > 0 else 100
            
            # Tabla enriquecida con Column Config
            st.dataframe(
                df_view[["Estado", "ID", "Nombre", "Categoría", "Cantidad", "Stock_Minimo", "Precio_Unitario", "Valor_Total", "Último_Movimiento"]],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Estado": st.column_config.TextColumn("Estado", width="small"),
                    "ID": st.column_config.TextColumn("Código (SKU)", width="small"),
                    "Nombre": st.column_config.TextColumn("Descripción del Elemento", width="medium"),
                    "Categoría": st.column_config.TextColumn("Categoría / Criticidad", width="small"),
                    "Cantidad": st.column_config.ProgressColumn(
                        "Existencias",
                        help="Unidades disponibles actualmente en bodega",
                        format="%d und",
                        min_value=0,
                        max_value=max_cant,
                    ),
                    "Stock_Minimo": st.column_config.NumberColumn("Mínimo (ROP)", format="%d und", help="Punto de reorden"),
                    "Precio_Unitario": st.column_config.NumberColumn("Costo Unitario", format="$%,.0f"),
                    "Valor_Total": st.column_config.NumberColumn("Valor Subtotal", format="$%,.0f"),
                    "Último_Movimiento": st.column_config.TextColumn("Última Actualización")
                }
            )
            
        with tab_graficos:
            st.markdown('<div class="pedagogical-box">📊 <b>Análisis Visual (Principio de Pareto / ABC):</b> Identifica rápidamente qué categorías concentran la mayor cantidad de dinero (Valorización) frente al volumen físico de unidades.</div>', unsafe_allow_html=True)
            g_col1, g_col2 = st.columns(2)
            with g_col1:
                st.subheader("💰 Valor Monetario por Categoría ($)")
                resumen_valor = df_view.groupby("Categoría")["Valor_Total"].sum().reset_index()
                st.bar_chart(resumen_valor, x="Categoría", y="Valor_Total", color="#39A900")
            with g_col2:
                st.subheader("🔢 Unidades Físicas por Categoría")
                resumen_cant = df_view.groupby("Categoría")["Cantidad"].sum().reset_index()
                st.bar_chart(resumen_cant, x="Categoría", y="Cantidad", color="#2B501E")

# ==========================================
# 2. PANTALLA: INGRESAR ELEMENTOS
# ==========================================
elif menu == "📥 Registrar Entradas":
    st.markdown('<p class="main-header">📥 Módulo de Entradas y Creación de SKUs</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header"> Alimenta el inventario registrando compras, devoluciones o nuevos productos</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="pedagogical-box">💡 <b>Nota de Normalización:</b> En bases de datos logísticas, los códigos (SKU) y nombres se convierten automáticamente a <b>MAYÚSCULAS</b> y sin espacios extra para evitar registros duplicados (ej. "cable" vs "CABLE ").</div>', unsafe_allow_html=True)

    modo_ingreso = st.radio(
        "¿Qué operación deseas realizar?",
        ["🆕 Crear Nuevo Producto (o ingresar por código)", "➕ Abastecer un Producto Existente"],
        horizontal=True
    )

    with st.container(border=True):
        if modo_ingreso == "➕ Abastecer un Producto Existente" and not df.empty:
            lista_prod = df["ID"] + " - " + df["Nombre"]
            seleccion = st.selectbox("Seleccione el producto a reabastecer:", lista_prod)
            id_sel = seleccion.split(" - ")[0]
            fila_actual = df[df["ID"] == id_sel].iloc[0]
            
            st.info(f"📊 **Stock Actual:** {fila_actual['Cantidad']} unidades | **Costo Unitario Actual:** ${fila_actual['Precio_Unitario']:,.0f} | **Categoría:** {fila_actual['Categoría']}")
            
            with st.form("reabastecer_form", clear_on_submit=True):
                c1, c2 = st.columns(2)
                with c1:
                    cant_ingreso = st.number_input("Cantidad que ingresa a bodega *", min_value=1, step=1, value=1)
                with c2:
                    nuevo_precio = st.number_input("Actualizar Costo Unitario ($)", min_value=0.0, step=100.0, value=float(fila_actual["Precio_Unitario"]))
                
                submit_reab = st.form_submit_button("📥 Confirmar Entrada de Almacén", type="primary", use_container_width=True)
                if submit_reab:
                    idx = df.index[df["ID"] == id_sel].tolist()[0]
                    df.at[idx, "Cantidad"] += cant_ingreso
                    df.at[idx, "Precio_Unitario"] = nuevo_precio
                    df.at[idx, "Último_Movimiento"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    save_data(df)
                    registrar_kardex(id_sel, fila_actual["Nombre"], "📥 Entrada (Reabastecimiento)", cant_ingreso, df.at[idx, "Cantidad"])
                    st.success(f"✅ Se sumaron **{cant_ingreso}** unidades a **{fila_actual['Nombre']}**. Nuevo total: **{df.at[idx, 'Cantidad']}** unidades.")
        
        else:
            if modo_ingreso == "➕ Abastecer un Producto Existente" and df.empty:
                st.warning("El inventario está vacío. Crea primero un producto nuevo.")
                
            with st.form("ingreso_form", clear_on_submit=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    id_prod = st.text_input("Código SKU / ID (Ej: EL-001) *")
                    nombre = st.text_input("Nombre o Descripción del Elemento *")
                with col2:
                    categoria = st.selectbox("Categoría / Criticidad ABC", ["Materia Prima", "Insumo", "Producto Terminado", "Alta", "Media", "Baja"])
                    stock_min = st.number_input("Stock Mínimo (Punto de Reorden)", min_value=0, value=5, step=1, help="El sistema generará alerta cuando la cantidad sea igual o menor a este valor.")
                with col3:
                    cantidad = st.number_input("Cantidad Inicial a Ingresar *", min_value=1, step=1)
                    precio = st.number_input("Costo Unitario ($) *", min_value=0.0, step=100.0)
                    
                st.caption("* Campos obligatorios")
                submit = st.form_submit_button("➕ Guardar y Registrar en Inventario", type="primary", use_container_width=True)
                
                if submit:
                    if not id_prod.strip() or not nombre.strip():
                        st.error("⚠️ El Código ID y el Nombre del elemento son obligatorios.")
                    else:
                        id_prod_norm = id_prod.strip().upper()
                        nombre_norm = nombre.strip().upper()
                        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        if id_prod_norm in df["ID"].values:
                            idx = df.index[df["ID"] == id_prod_norm].tolist()[0]
                            df.at[idx, "Cantidad"] += cantidad
                            df.at[idx, "Precio_Unitario"] = precio
                            df.at[idx, "Stock_Minimo"] = stock_min
                            df.at[idx, "Último_Movimiento"] = fecha_actual
                            save_data(df)
                            registrar_kardex(id_prod_norm, df.at[idx, "Nombre"], "📥 Entrada (Adición por ID)", cantidad, df.at[idx, "Cantidad"])
                            st.success(f"✅ El código **{id_prod_norm}** ya existía. Se sumaron {cantidad} unidades al producto **{df.at[idx, 'Nombre']}**.")
                        else:
                            nuevo_registro = pd.DataFrame([{
                                "ID": id_prod_norm,
                                "Nombre": nombre_norm,
                                "Categoría": categoria,
                                "Cantidad": cantidad,
                                "Stock_Minimo": stock_min,
                                "Precio_Unitario": precio,
                                "Último_Movimiento": fecha_actual
                            }])
                            df = pd.concat([df, nuevo_registro], ignore_index=True)
                            save_data(df)
                            registrar_kardex(id_prod_norm, nombre_norm, "🆕 Creación inicial", cantidad, cantidad)
                            st.success(f"✅ Producto **{nombre_norm}** (ID: `{id_prod_norm}`) creado exitosamente con {cantidad} unidades.")

# ==========================================
# 3. PANTALLA: EXTRAER ELEMENTOS
# ==========================================
elif menu == "📤 Registrar Salidas":
    st.markdown('<p class="main-header">📤 Módulo de Salidas y Despachos</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Registra órdenes de consumo interno, ventas o bajas de almacén</p>', unsafe_allow_html=True)
    
    if df.empty:
        st.warning("⚠️ No hay elementos registrados en el inventario para realizar extracciones.")
    else:
        with st.container(border=True):
            # Selector fuera del form para actualizar dinámicamente el stock en pantalla
            lista_productos = df["ID"] + " | " + df["Nombre"]
            producto_seleccionado = st.selectbox("1️⃣ Seleccione el Producto a retirar:", lista_productos)
            
            id_seleccionado = producto_seleccionado.split(" | ")[0]
            idx = df.index[df["ID"] == id_seleccionado].tolist()[0]
            item = df.loc[idx]
            stock_actual = int(item["Cantidad"])
            
            # Panel informativo en vivo del producto seleccionado
            c_info1, c_info2, c_info3 = st.columns(3)
            c_info1.metric("📦 Disponible en Bodega", f"{stock_actual} unidades")
            c_info2.metric("🚦 Punto de Reorden (Mínimo)", f"{int(item['Stock_Minimo'])} unidades")
            c_info3.metric("🏷️ Costo Unitario", f"${item['Precio_Unitario']:,.0f}")
            
            if stock_actual == 0:
                st.error(f"🚫 El producto **{item['Nombre']}** se encuentra **AGOTADO (0 unidades)**. Diríjase al módulo de Entradas para abastecerlo.")
            else:
                with st.form("salida_form", clear_on_submit=True):
                    col_s1, col_s2 = st.columns(2)
                    with col_s1:
                        cantidad_salida = st.number_input(
                            "2️⃣ Cantidad a Extraer *", 
                            min_value=1, 
                            max_value=stock_actual, 
                            step=1,
                            help=f"Máximo permitido según existencias: {stock_actual}"
                        )
                    with col_s2:
                        motivo = st.selectbox("Motivo de la Salida", ["Consumo en Formación / Taller", "Venta / Despacho a Cliente", "Mantenimiento / Proyecto", "Merma / Daño"])
                        
                    submit_salida = st.form_submit_button("➖ Confirmar Salida de Almacén", type="primary", use_container_width=True)
                    
                    if submit_salida:
                        df.at[idx, "Cantidad"] -= cantidad_salida
                        nuevo_saldo = df.at[idx, "Cantidad"]
                        df.at[idx, "Último_Movimiento"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        save_data(df)
                        registrar_kardex(id_seleccionado, item["Nombre"], f"📤 Salida ({motivo})", -cantidad_salida, nuevo_saldo)
                        
                        st.success(f"✅ Salida registrada con éxito. Quedan **{nuevo_saldo}** unidades de **{item['Nombre']}**.")
                        if nuevo_saldo <= item["Stock_Minimo"]:
                            st.warning(f"⚠️ **¡Atención Logística!** El producto ha alcanzado o bajado de su Stock Mínimo ({item['Stock_Minimo']} und). Se sugiere generar orden de reposición.")

# ==========================================
# 4. PANTALLA: HISTORIAL KARDEX
# ==========================================
elif menu == "📜 Historial Kardex":
    st.markdown('<p class="main-header">📜 Trazabilidad y Kardex de Movimientos</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Bitácora de auditoría con todas las entradas y salidas registradas en el sistema</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="pedagogical-box">🔍 <b>¿Qué es el Kardex?</b> Es el documento o registro administrativo que permite controlar la trazabilidad de cada movimiento (quién, cuándo, cuánto entró o salió y qué saldo quedó), evitando pérdidas de inventario.</div>', unsafe_allow_html=True)
    
    df_kardex = load_kardex()
    if df_kardex.empty:
        st.info("Aún no se han registrado movimientos en la bitácora.")
    else:
        col_k1, col_k2 = st.columns([4, 1])
        with col_k2:
            csv_k = df_kardex.to_csv(index=False).encode('utf-8-sig')
            st.download_button("⬇️ Descargar Bitácora CSV", data=csv_k, file_name="kardex_movimientos.csv", mime="text/csv", use_container_width=True)
            
        st.dataframe(df_kardex, use_container_width=True, hide_index=True)

# ==========================================
# 5. PANTALLA: GESTIÓN DE DATOS (CSV)
# ==========================================
elif menu == "📊 Datos y Archivos (CSV)":
    st.markdown('<p class="main-header">📊 Intercambio de Datos (ETL / CSV)</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Exporta o importa la base de datos para prácticas en Microsoft Excel, Power BI o Python</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.subheader("⬇️ Exportar Inventario Actual")
            st.markdown("Descarga la tabla en formato `.csv` (codificación `UTF-8 con BOM` para que Excel reconozca tildes y caracteres especiales directamente).")
            if not df.empty:
                # utf-8-sig garantiza que al abrir en Excel en español las tildes no se dañen
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="📥 Descargar inventario_sena.csv",
                    data=csv,
                    file_name='inventario_sena.csv',
                    mime='text/csv',
                    type="primary",
                    use_container_width=True
                )
            else:
                st.info("El inventario está vacío actualmente.")
                
        with st.container(border=True):
            st.subheader("🗑️ Zona de Reinicio (Prácticas)")
            st.markdown("Limpia todos los registros para iniciar un ejercicio desde cero.")
            if st.button("Borrar Todo el Inventario", use_container_width=True):
                if os.path.exists(DATA_FILE):
                    os.remove(DATA_FILE)
                if os.path.exists(KARDEX_FILE):
                    os.remove(KARDEX_FILE)
                st.success("Base de datos reiniciada.")
                st.rerun()
                
    with col2:
        with st.container(border=True):
            st.subheader("⬆️ Importar Inventario desde CSV")
            st.markdown("Carga un archivo `.csv` modificado por los aprendices para actualizar el sistema.")
            uploaded_file = st.file_uploader("Seleccionar archivo CSV", type=["csv"])
            if uploaded_file is not None:
                try:
                    df_imported = pd.read_csv(uploaded_file)
                    st.write("👀 **Vista previa del archivo cargado:**")
                    st.dataframe(df_imported.head(4), use_container_width=True, hide_index=True)
                    
                    columnas_requeridas = {"ID", "Nombre", "Categoría", "Cantidad", "Precio_Unitario"}
                    if not columnas_requeridas.issubset(set(df_imported.columns)):
                        st.error(f"❌ El archivo debe contener al menos las columnas: {', '.join(columnas_requeridas)}")
                    else:
                        if "Stock_Minimo" not in df_imported.columns:
                            df_imported["Stock_Minimo"] = 5
                        if "Último_Movimiento" not in df_imported.columns:
                            df_imported["Último_Movimiento"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                        if st.button("✅ Confirmar y Sobreescribir Base de Datos", type="primary", use_container_width=True):
                            save_data(df_imported)
                            registrar_kardex("CSV", "IMPORTACIÓN MASIVA", "⬆️ Carga archivo CSV", len(df_imported), 0)
                            st.success("🎉 ¡Datos importados exitosamente! Revisa el Panel de Control.")
                except Exception as e:
                    st.error(f"Error al leer el archivo: {e}")