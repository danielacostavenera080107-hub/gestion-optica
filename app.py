import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from plyer import notification
import calendar
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(layout="wide", page_title="Sistema de Gestión — LENS VISION")

# Estilos CSS avanzados con contraste total y 4 columnas
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Plus Jakarta Sans', sans-serif; 
    }
    
    /* Fondo de pantalla completa */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: linear-gradient(rgba(15, 23, 42, 0.88), rgba(15, 23, 42, 0.92)), 
                    url('https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=1920&q=80') !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .hero-banner {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
        padding: 20px 30px;
        border-radius: 16px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 25px;
    }
    .metric-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 16px;
        border-radius: 14px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Estilo nítido para los botones de navegación de meses */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-weight: 700 !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    div.stButton > button:hover {
        background-color: #f8fafc !important;
        border-color: #38bdf8 !important;
    }

    /* Cajas informativas sólidas */
    .stAlert {
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #0f172a !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Corrección total para los Expanders (Listas desplegables de pedidos) */
    [data-testid="stExpander"] {
        background-color: rgba(255, 255, 255, 0.98) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15) !important;
        margin-bottom: 12px;
    }
    
    [data-testid="stExpander"] summary p, [data-testid="stExpander"] summary span {
        color: #0f172a !important;
        font-weight: 700 !important;
    }

    [data-testid="stExpander"] div[data-testid="stVerticalBlock"] p, 
    [data-testid="stExpander"] div[data-testid="stVerticalBlock"] span {
        color: #0f172a !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Función para sumar días hábiles (excluyendo fines de semana)
def sumar_dias_habiles(fecha_inicio, dias_a_sumar):
    actual = fecha_inicio
    agregados = 0
    while agregados < dias_a_sumar:
        actual += timedelta(days=1)
        if actual.weekday() < 5:  # Lunes a Viernes
            agregados += 1
    return actual

# Inicialización de estado con datos de ejemplo
if 'pedidos' not in st.session_state:
    p1 = {
        "ID": 1, "Nombre": "Carlos", "Apellido": "Pérez", "Cédula": "12345678",
        "Asesora": "Laura Gómez", "Fecha Compra": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
        "Fecha Entrega Estimada": sumar_dias_habiles(datetime.now(), 3).strftime("%Y-%m-%d"),
        "Estado": "Pendiente por Entregar"
    }
    p2 = {
        "ID": 2, "Nombre": "María", "Apellido": "Gómez", "Cédula": "87654321",
        "Asesora": "Andrea Ruiz", "Fecha Compra": (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d"),
        "Fecha Entrega Estimada": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "Estado": "Pasados de Fecha"
    }
    p3 = {
        "ID": 3, "Nombre": "Ana", "Apellido": "Rodríguez", "Cédula": "11223344",
        "Asesora": "Laura Gómez", "Fecha Compra": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
        "Fecha Entrega Estimada": datetime.now().strftime("%Y-%m-%d"),
        "Estado": "Entregados"
    }
    p4 = {
        "ID": 4, "Nombre": "Pedro", "Apellido": "Martínez", "Cédula": "99887766",
        "Asesora": "Andrea Ruiz", "Fecha Compra": (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d"),
        "Fecha Entrega Estimada": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
        "Estado": "En Garantía"
    }
    st.session_state.pedidos = pd.DataFrame([p1, p2, p3, p4])

if 'cal_year' not in st.session_state:
    st.session_state.cal_year = datetime.now().year
if 'cal_month' not in st.session_state:
    st.session_state.cal_month = datetime.now().month

# Función para notificaciones
def enviar_alerta(titulo, mensaje):
    try:
        notification.notify(title=titulo, message=mensaje, app_name="LENS VISION", timeout=10)
    except Exception:
        pass

# --- BARRA SUPERIOR CON RELOJ EN TIEMPO REAL ---
reloj_html = """
<div style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%); padding: 20px 30px; border-radius: 16px; color: white; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 25px; font-family: 'Plus Jakarta Sans', sans-serif;">
    <div><span style="font-weight: 700; font-size: 16px;">⚡ LENS VISION — Panel Ejecutivo de Control Óptico</span></div>
    <div id="reloj-vivo" style="font-size: 13px; font-weight: 500; background: rgba(255,255,255,0.15); padding: 6px 14px; border-radius: 20px;">🕒 Cargando reloj...</div>
</div>

<script>
function actualizarReloj() {
    const dias = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"];
    const meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];
    
    const now = new Date();
    const diaSemana = dias[now.getDay()];
    const diaMes = now.getDate();
    const mes = meses[now.getMonth() + 1];
    const anio = now.getFullYear();
    
    let horas = now.getHours();
    const minutos = String(now.getMinutes()).padStart(2, '0');
    const segundos = String(now.getSeconds()).padStart(2, '0');
    const ampm = horas >= 12 ? 'PM' : 'AM';
    
    horas = horas % 12;
    horas = horas ? horas : 12;
    const horaStr = String(horas).padStart(2, '0');
    
    const formatoFinal = `🕒 ${diaSemana}, ${diaMes} de ${mes} de ${anio} — ${horaStr}:${minutos}:${segundos} ${ampm}`;
    document.getElementById('reloj-vivo').innerText = formatoFinal;
}
setInterval(actualizarReloj, 1000);
actualizarReloj();
</script>
"""
components.html(reloj_html, height=90)

# Encabezado Principal y Calendario Interactivo con Navegación de Meses
col_title, col_cal = st.columns([1.6, 1.4], gap="large")

with col_title:
    st.markdown("<h1 style='color: #ffffff; font-size: 30px; font-weight: 800; margin-bottom: 0px; text-shadow: 0 2px 4px rgba(0,0,0,0.5);'>Órdenes de Lentes 👓</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #e2e8f0; font-size: 14px; margin-top: 4px; margin-bottom: 24px; font-weight: 600; text-shadow: 0 1px 2px rgba(0,0,0,0.5);'>Supervisa eficientemente las entregas, plazos en días hábiles, ventas mensuales y garantías.</p>", unsafe_allow_html=True)
    
    df_p = st.session_state.pedidos
    total_pendientes = len(df_p[df_p["Estado"] == "Pendiente por Entregar"])
    total_atrasados = len(df_p[df_p["Estado"] == "Pasados de Fecha"])
    total_entregados = len(df_p[df_p["Estado"] == "Entregados"])
    total_garantias = len(df_p[df_p["Estado"] == "En Garantía"])
    
    # Cálculo dinámico de lentes vendidos y entregados en el MES y AÑO seleccionados
    c_y = st.session_state.cal_year
    c_m = st.session_state.cal_month
    
    def es_del_mes_seleccionado(fecha_str):
        try:
            f_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
            return f_obj.year == c_y and f_obj.month == c_m
        except Exception:
            return False

    df_entregados = df_p[df_p["Estado"] == "Entregados"]
    total_vendidos_mes = len(df_entregados[df_entregados["Fecha Entrega Estimada"].apply(es_del_mes_seleccionado)])
    
    # 5 Métricas KPIs Organizadas
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        st.markdown(f'<div class="metric-container"><span style="color: #f59e0b; font-size: 20px; font-weight: 800;">{total_pendientes}</span><br><span style="color: #64748b; font-size: 10px; font-weight: 700;">PENDIENTES</span></div>', unsafe_allow_html=True)
    with kpi2:
        st.markdown(f'<div class="metric-container"><span style="color: #ef4444; font-size: 20px; font-weight: 800;">{total_atrasados}</span><br><span style="color: #64748b; font-size: 10px; font-weight: 700;">ATRASADOS</span></div>', unsafe_allow_html=True)
    with kpi3:
        st.markdown(f'<div class="metric-container"><span style="color: #10b981; font-size: 20px; font-weight: 800;">{total_entregados}</span><br><span style="color: #64748b; font-size: 10px; font-weight: 700;">ENTREGADOS</span></div>', unsafe_allow_html=True)
    with kpi4:
        st.markdown(f'<div class="metric-container"><span style="color: #8b5cf6; font-size: 20px; font-weight: 800;">{total_garantias}</span><br><span style="color: #64748b; font-size: 10px; font-weight: 700;">GARANTÍAS</span></div>', unsafe_allow_html=True)
    with kpi5:
        st.markdown(f'<div class="metric-container"><span style="color: #0ea5e9; font-size: 20px; font-weight: 800;">{total_vendidos_mes}</span><br><span style="color: #64748b; font-size: 10px; font-weight: 700;">VENDIDOS (MES)</span></div>', unsafe_allow_html=True)

with col_cal:
    c_ant, c_sig = st.columns([1, 1])
    with c_ant:
        if st.button("◀ Mes Anterior", use_container_width=True, key="prev_month"):
            if st.session_state.cal_month == 1:
                st.session_state.cal_month = 12
                st.session_state.cal_year -= 1
            else:
                st.session_state.cal_month -= 1
            st.rerun()
    with c_sig:
        if st.button("Mes Siguiente ▶", use_container_width=True, key="next_month"):
            if st.session_state.cal_month == 12:
                st.session_state.cal_month = 1
                st.session_state.cal_year += 1
            else:
                st.session_state.cal_month += 1
            st.rerun()

    meses_es = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    month_name = meses_es[c_m]
    
    cal = calendar.monthcalendar(c_y, c_m)
    filtro_fechas = df_p["Estado"].isin(["Pendiente por Entregar", "Pasados de Fecha"])
    fechas_pendientes = df_p[filtro_fechas]["Fecha Entrega Estimada"].tolist()
    
    html_cal = f'<div style="background-color: rgba(255, 255, 255, 0.95); padding: 16px; border-radius: 14px; border: 1px solid rgba(255,255,255,0.2); box-shadow: 0 4px 6px rgba(0,0,0,0.1); font-family: sans-serif;"><div style="font-weight: 700; text-align: center; margin-bottom: 12px; color: #0f172a; font-size: 15px;">📅 {month_name} {c_y}</div><table style="width: 100%; text-align: center; border-collapse: collapse;"><tr style="color: #94a3b8; font-size: 11px; font-weight: 700;"><th style="padding-bottom: 8px;">Lu</th><th style="padding-bottom: 8px;">Ma</th><th style="padding-bottom: 8px;">Mi</th><th style="padding-bottom: 8px;">Ju</th><th style="padding-bottom: 8px;">Vi</th><th style="padding-bottom: 8px;">Sá</th><th style="padding-bottom: 8px;">Do</th></tr>'
    
    for week in cal:
        html_cal += "<tr>"
        for day in week:
            if day == 0:
                html_cal += "<td style='padding: 5px;'></td>"
            else:
                fecha_str = f"{c_y}-{c_m:02d}-{day:02d}"
                is_delivery = fecha_str in fechas_pendientes
                if is_delivery:
                    html_cal += f"<td style='padding: 5px;'><span style='background-color: #10b981; color: white; padding: 4px 8px; border-radius: 50%; font-weight: 700; font-size: 12px;'>{day}</span></td>"
                else:
                    html_cal += f"<td style='padding: 5px; color: #475569; font-weight: 500; font-size: 13px;'>{day}</td>"
        html_cal += "</tr>"
    html_cal += "</table></div>"
    st.markdown(html_cal, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Logotipo LENS VISION grande para la barra lateral
logo_svg_grande = """
<div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 22px 15px; border-radius: 16px; text-align: center; margin-bottom: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.15);">
    <svg width="80" height="45" viewBox="0 0 100 60" style="margin-bottom: 8px;">
        <circle cx="30" cy="30" r="20" fill="none" stroke="#38bdf8" stroke-width="6"/>
        <circle cx="70" cy="30" r="20" fill="none" stroke="#38bdf8" stroke-width="6"/>
        <line x1="50" y1="30" x2="50" y2="20" stroke="#38bdf8" stroke-width="6"/>
        <circle cx="50" cy="30" r="4" fill="#10b981"/>
    </svg>
    <div style="color: white; font-weight: 800; font-size: 20px; letter-spacing: 1.5px; font-family: 'Plus Jakarta Sans', sans-serif;">LENS VISION</div>
    <div style="color: #94a3b8; font-size: 11px; letter-spacing: 3px; text-transform: uppercase; margin-top: 2px;">Optica & Gestión</div>
</div>
"""

with st.sidebar:
    st.markdown(logo_svg_grande, unsafe_allow_html=True)
    
    st.markdown("<h2 style='font-size: 18px; font-weight: 700; color: #0f172a;'>📝 Registrar Nuevo Pedido</h2>", unsafe_allow_html=True)
    with st.form("nuevo_pedido", clear_on_submit=True):
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        cedula = st.text_input("Número de Cédula")
        asesora = st.text_input("Asesora Responsable")
        dias_espera = st.number_input("Plazo de Entrega (Días Hábiles)", min_value=1, value=5)
        
        btn_registrar = st.form_submit_button("Registrar Pedido", use_container_width=True)
        
        if btn_registrar and nombre and cedula:
            fecha_compra = datetime.now()
            fecha_entrega = sumar_dias_habiles(fecha_compra, int(dias_espera))
            
            nuevo_id = int(st.session_state.pedidos["ID"].max() + 1) if not st.session_state.pedidos.empty else 1
            nuevo_dict = {
                "ID": nuevo_id, "Nombre": nombre, "Apellido": apellido, "Cédula": cedula,
                "Asesora": asesora if asesora else "No asignada",
                "Fecha Compra": fecha_compra.strftime("%Y-%m-%d"),
                "Fecha Entrega Estimada": fecha_entrega.strftime("%Y-%m-%d"),
                "Estado": "Pendiente por Entregar"
            }
            st.session_state.pedidos = pd.concat([st.session_state.pedidos, pd.DataFrame([nuevo_dict])], ignore_index=True)
            enviar_alerta("Pedido Registrado", f"Pedido para {nombre} {apellido} registrado con éxito.")
            st.rerun()

# Verificación automática de estados
hoy_str = datetime.now().strftime("%Y-%m-%d")

for index, row in st.session_state.pedidos.iterrows():
    if row["Estado"] == "Pendiente por Entregar":
        fecha_entrega = datetime.strptime(row["Fecha Entrega Estimada"], "%Y-%m-%d")
        fecha_actual = datetime.strptime(hoy_str, "%Y-%m-%d")
        if fecha_entrega < fecha_actual:
            st.session_state.pedidos.at[index, "Estado"] = "Pasados de Fecha"
            enviar_alerta("Pedido Retrasado", f"El pedido de {row['Nombre']} {row['Apellido']} está pasado de la fecha de entrega.")

# Listado de pedidos organizado en 4 columnas principales
col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    st.markdown("<h3 style='color: #f59e0b; font-size: 16px; font-weight: 800; text-shadow: 0 2px 4px rgba(0,0,0,0.8); background: rgba(15, 23, 42, 0.6); padding: 8px 10px; border-radius: 8px;'>⏳ Pendientes</h3>", unsafe_allow_html=True)
    pendientes = st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Pendiente por Entregar"]
    if pendientes.empty:
        st.info("No hay pendientes.")
    for idx, row in pendientes.iterrows():
        with st.expander(f"👓 {row['Nombre']} {row['Apellido']} (Cédula: {row['Cédula']})"):
            st.warning(f"📅 **Entrega Est:** {row['Fecha Entrega Estimada']}")
            st.write(f"👤 **Asesora:** {row['Asesora']}")
            st.write(f"🛒 **Compra:** {row['Fecha Compra']}")
            
            c_b1, c_b2, c_b3 = st.columns(3)
            with c_b1:
                if st.button("✅", key=f"ent_{row['ID']}", help="Entregar"):
                    st.session_state.pedidos.at[idx, "Estado"] = "Entregados"
                    st.rerun()
            with c_b2:
                if st.button("🛡️", key=f"gar_{row['ID']}", help="Enviar a Garantía"):
                    st.session_state.pedidos.at[idx, "Estado"] = "En Garantía"
                    st.rerun()
            with c_b3:
                if st.button("🗑️", key=f"del_{row['ID']}", help="Borrar"):
                    st.session_state.pedidos = st.session_state.pedidos.drop(idx).reset_index(drop=True)
                    st.rerun()

with col2:
    st.markdown("<h3 style='color: #ef4444; font-size: 16px; font-weight: 800; text-shadow: 0 2px 4px rgba(0,0,0,0.8); background: rgba(15, 23, 42, 0.6); padding: 8px 10px; border-radius: 8px;'>⚠️ Atrasados</h3>", unsafe_allow_html=True)
    atrasados = st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Pasados de Fecha"]
    if atrasados.empty:
        st.info("No hay atrasados.")
    for idx, row in atrasados.iterrows():
        with st.expander(f"⚠️ {row['Nombre']} {row['Apellido']} (Cédula: {row['Cédula']})"):
            st.error(f"📅 **Vencido Est:** {row['Fecha Entrega Estimada']}")
            st.write(f"👤 **Asesora:** {row['Asesora']}")
            st.write(f"🛒 **Compra:** {row['Fecha Compra']}")
            
            c_b1, c_b2, c_b3 = st.columns(3)
            with c_b1:
                if st.button("✅", key=f"ent_at_{row['ID']}", help="Entregar"):
                    st.session_state.pedidos.at[idx, "Estado"] = "Entregados"
                    st.rerun()
            with c_b2:
                if st.button("🛡️", key=f"gar_at_{row['ID']}", help="Enviar a Garantía"):
                    st.session_state.pedidos.at[idx, "Estado"] = "En Garantía"
                    st.rerun()
            with c_b3:
                if st.button("🗑️", key=f"del_at_{row['ID']}", help="Borrar"):
                    st.session_state.pedidos = st.session_state.pedidos.drop(idx).reset_index(drop=True)
                    st.rerun()

with col3:
    st.markdown("<h3 style='color: #10b981; font-size: 16px; font-weight: 800; text-shadow: 0 2px 4px rgba(0,0,0,0.8); background: rgba(15, 23, 42, 0.6); padding: 8px 10px; border-radius: 8px;'>✅ Entregados</h3>", unsafe_allow_html=True)
    entregados = st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Entregados"]
    if entregados.empty:
        st.info("No hay entregados.")
    for idx, row in entregados.iterrows():
        with st.expander(f"📦 {row['Nombre']} {row['Apellido']} (Cédula: {row['Cédula']})"):
            st.success(f"📅 **Entregado el:** {row['Fecha Entrega Estimada']}")
            st.write(f"👤 **Asesora:** {row['Asesora']}")
            st.write(f"🛒 **Compra:** {row['Fecha Compra']}")
            
            c_b1, c_b2 = st.columns(2)
            with c_b1:
                if st.button("🛡️", key=f"gar_ent_{row['ID']}", help="Enviar a Garantía", use_container_width=
