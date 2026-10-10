import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from plyer import notification
import calendar
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(layout="wide", page_title="Sistema de Gestión — LENS VISION")

# Estilos CSS generales limpios
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #f8fafc; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 20px 30px;
        border-radius: 16px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.15);
        margin-bottom: 25px;
    }
    .metric-container {
        background: #ffffff;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
        border: 1px solid #f1f5f9;
        text-align: center;
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
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
        "Fecha Entrega Estimada": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
        "Estado": "Entregados"
    }
    st.session_state.pedidos = pd.DataFrame([p1, p2, p3])

# Función para notificaciones
def enviar_alerta(titulo, mensaje):
    try:
        notification.notify(title=titulo, message=mensaje, app_name="LENS VISION", timeout=10)
    except Exception:
        pass

# --- BARRA SUPERIOR CON RELOJ EN TIEMPO REAL (SEGUNDO A SEGUNDO) ---
reloj_html = """
<div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 20px 30px; border-radius: 16px; color: white; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.15); margin-bottom: 25px; font-family: 'Plus Jakarta Sans', sans-serif;">
    <div><span style="font-weight: 700; font-size: 16px;">⚡ LENS VISION — Panel Ejecutivo de Control Óptico</span></div>
    <div id="reloj-vivo" style="font-size: 13px; font-weight: 500; background: rgba(255,255,255,0.1); padding: 6px 14px; border-radius: 20px;">🕒 Cargando reloj...</div>
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

# Encabezado Principal y Calendario Elegante Superior Derecho
col_title, col_cal = st.columns([1.6, 1.4], gap="large")

with col_title:
    st.markdown("<h1 style='color: #0f172a; font-size: 30px; font-weight: 800; margin-bottom: 0px;'>Órdenes de Lentes 👓</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 14px; margin-top: 4px; margin-bottom: 24px;'>Supervisa eficientemente las entregas, plazos en días hábiles y el rendimiento del personal.</p>", unsafe_allow_html=True)
    
    df_p = st.session_state.pedidos
    total_pendientes = len(df_p[df_p["Estado"] == "Pendiente por Entregar"])
    total_atrasados = len(df_p[df_p["Estado"] == "Pasados de Fecha"])
    total_entregados = len(df_p[df_p["Estado"] == "Entregados"])
    
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.markdown(f'<div class="metric-container"><span style="color: #f59e0b; font-size: 24px; font-weight: 800;">{total_pendientes}</span><br><span style="color: #64748b; font-size: 12px; font-weight: 600;">PENDIENTES</span></div>', unsafe_allow_html=True)
    with kpi2:
        st.markdown(f'<div class="metric-container"><span style="color: #ef4444; font-size: 24px; font-weight: 800;">{total_atrasados}</span><br><span style="color: #64748b; font-size: 12px; font-weight: 600;">ATRASADOS</span></div>', unsafe_allow_html=True)
    with kpi3:
        st.markdown(f'<div class="metric-container"><span style="color: #10b981; font-size: 24px; font-weight: 800;">{total_entregados}</span><br><span style="color: #64748b; font-size: 12px; font-weight: 600;">ENTREGADOS</span></div>', unsafe_allow_html=True)

with col_cal:
    now = datetime.now()
    cal = calendar.monthcalendar(now.year, now.month)
    meses_es = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    month_name = meses_es[now.month]
    
    filtro_fechas = df_p["Estado"].isin(["Pendiente por Entregar", "Pasados de Fecha"])
    fechas_pendientes = df_p[filtro_fechas]["Fecha Entrega Estimada"].tolist()
    
    html_cal = f'<div style="background-color: #ffffff; padding: 20px; border-radius: 14px; border: 1px solid #e2e8f0; font-family: sans-serif;"><div style="font-weight: 700; text-align: center; margin-bottom: 12px; color: #0f172a; font-size: 15px;">📅 Calendario Activo — {month_name}</div><table style="width: 100%; text-align: center; border-collapse: collapse;"><tr style="color: #94a3b8; font-size: 11px; font-weight: 700;"><th style="padding-bottom: 8px;">Lu</th><th style="padding-bottom: 8px;">Ma</th><th style="padding-bottom: 8px;">Mi</th><th style="padding-bottom: 8px;">Ju</th><th style="padding-bottom: 8px;">Vi</th><th style="padding-bottom: 8px;">Sá</th><th style="padding-bottom: 8px;">Do</th></tr>'
    
    for week in cal:
        html_cal += "<tr>"
        for day in week:
            if day == 0:
                html_cal += "<td style='padding: 6px;'></td>"
            else:
                fecha_str = f"{now.year}-{now.month:02d}-{day:02d}"
                is_delivery = fecha_str in fechas_pendientes
                if is_delivery:
                    html_cal += f"<td style='padding: 6px;'><span style='background-color: #10b981; color: white; padding: 5px 9px; border-radius: 50%; font-weight: 700; font-size: 12px;'>{day}</span></td>"
                else:
                    html_cal += f"<td style='padding: 6px; color: #475569; font-weight: 500; font-size: 13px;'>{day}</td>"
        html_cal += "</tr>"
    html_cal += "</table></div>"
    st.markdown(html_cal, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Barra lateral estilizada con el logotipo vectorial de LENS VISION (Opción B)
logo_svg = """
<div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <svg width="50" height="30" viewBox="0 0 100 60" style="margin-bottom: 5px;">
        <circle cx="30" cy="30" r="20" fill="none" stroke="#38bdf8" stroke-width="6"/>
        <circle cx="70" cy="30" r="20" fill="none" stroke="#38bdf8" stroke-width="6"/>
        <line x1="50" y1="30" x2="50" y2="20" stroke="#38bdf8" stroke-width="6"/>
        <circle cx="50" cy="30" r="4" fill="#10b981"/>
    </svg>
    <div style="color: white; font-weight: 800; font-size: 16px; letter-spacing: 1px; font-family: 'Plus Jakarta Sans', sans-serif;">LENS VISION</div>
    <div style="color: #94a3b8; font-size: 10px; letter-spacing: 2px; text-transform: uppercase;">Optica & Gestión</div>
</div>
"""

with st.sidebar:
    st.markdown(logo_svg, unsafe_allow_html=True)
    
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

# Listado de pedidos con componentes estables y robustos
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("### ⏳ Pendientes por Entregar")
    pendientes = st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Pendiente por Entregar"]
    if pendientes.empty:
        st.info("No hay pedidos pendientes.")
    for idx, row in pendientes.iterrows():
        with st.expander(f"👓 {row['Nombre']} {row['Apellido']} (Cédula: {row['Cédula']})"):
            st.warning(f"📅 **Entrega Est:** {row['Fecha Entrega Estimada']}")
            st.write(f"👤 **Asesora:** {row['Asesora']}")
            st.write(f"🛒 **Compra:** {row['Fecha Compra']}")
            
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("✅ Entregar", key=f"ent_{row['ID']}", use_container_width=True):
                    st.session_state.pedidos.at[idx, "Estado"] = "Entregados"
                    st.rerun()
            with c_btn2:
                if st.button("🗑️ Borrar", key=f"del_{row['ID']}", use_container_width=True):
                    st.session_state.pedidos = st.session_state.pedidos.drop(idx).reset_index(drop=True)
                    st.rerun()

with col2:
    st.markdown("### ⚠️ Pasados de Fecha")
    atrasados = st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Pasados de Fecha"]
    if atrasados.empty:
        st.info("No hay pedidos atrasados.")
    for idx, row in atrasados.iterrows():
        with st.expander(f"⚠️ {row['Nombre']} {row['Apellido']} (Cédula: {row['Cédula']})", expanded=True):
            st.error(f"📅 **Vencido Est:** {row['Fecha Entrega Estimada']}")
            st.write(f"👤 **Asesora:** {row['Asesora']}")
            st.write(f"🛒 **Compra:** {row['Fecha Compra']}")
            
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("✅ Entregar", key=f"ent_atrasado_{row['ID']}", use_container_width=True):
                    st.session_state.pedidos.at[idx, "Estado"] = "Entregados"
                    st.rerun()
            with c_btn2:
                if st.button("🗑️ Borrar", key=f"del_atrasado_{row['ID']}", use_container_width=True):
                    st.session_state.pedidos = st.session_state.pedidos.drop(idx).reset_index(drop=True)
                    st.rerun()

with col3:
    st.markdown("### ✅ Entregados")
    entregados = st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Entregados"]
    if entregados.empty:
        st.info("No hay pedidos entregados.")
    for idx, row in entregados.iterrows():
        with st.expander(f"📦 {row['Nombre']} {row['Apellido']} (Cédula: {row['Cédula']})"):
            st.success(f"📅 **Entregado el:** {row['Fecha Entrega Estimada']}")
            st.write(f"👤 **Asesora:** {row['Asesora']}")
            st.write(f"🛒 **Compra:** {row['Fecha Compra']}")
            
            if st.button("🗑️ Borrar", key=f"del_entregado_{row['ID']}", use_container_width=True):
                st.session_state.pedidos = st.session_state.pedidos.drop(idx).reset_index(drop=True)
                st.rerun()
