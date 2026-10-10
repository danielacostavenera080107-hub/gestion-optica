import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from plyer import notification
import calendar

# Configuración de la página
st.set_page_config(layout="wide", page_title="Sistema de Gestión — Óptica")

# Estilos CSS avanzados para un aspecto ultra moderno, elegante y limpio
st.markdown("""
    <style>
    /* Ocultar elementos predeterminados de Streamlit para limpieza visual */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stApp {
        background-color: #f4f6f9;
        font-family: 'Inter', sans-serif;
    }
    
    /* Contenedor de la barra superior */
    .top-bar {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 15px 25px;
        border-radius: 12px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-bottom: 25px;
    }
    
    /* Tarjetas de Métricas (KPIs) */
    .kpi-card {
        background: #ffffff;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        text-align: center;
        transition: transform 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
    }
    
    /* Tarjetas de Pedidos Individuales */
    .card-pendientes {
        background: #ffffff;
        padding: 16px;
        border-radius: 10px;
        border-left: 5px solid #f59e0b;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 12px;
        border-top: 1px solid #f1f5f9;
        border-right: 1px solid #f1f5f9;
        border-bottom: 1px solid #f1f5f9;
    }
    .card-atrasados {
        background: #ffffff;
        padding: 16px;
        border-radius: 10px;
        border-left: 5px solid #ef4444;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 12px;
        border-top: 1px solid #f1f5f9;
        border-right: 1px solid #f1f5f9;
        border-bottom: 1px solid #f1f5f9;
    }
    .card-entregados {
        background: #ffffff;
        padding: 16px;
        border-radius: 10px;
        border-left: 5px solid #10b981;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 12px;
        border-top: 1px solid #f1f5f9;
        border-right: 1px solid #f1f5f9;
        border-bottom: 1px solid #f1f5f9;
    }
    
    /* Estilos de Botones Personalizados dentro de Expanders */
    .stButton button {
        border-radius: 8px;
        font-weight: 500;
        font-size: 13px;
        padding: 4px 12px;
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
    st.session_state.pedidos = pd.DataFrame([
        {
            "ID": 1,
            "Nombre": "Carlos",
            "Apellido": "Pérez",
            "Cédula": "12345678",
            "Asesora": "Laura Gómez",
            "Fecha Compra": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            "Fecha Entrega Estimada": sumar_dias_habiles(datetime.now(), 3).strftime("%Y-%m-%d"),
            "Estado": "Pendiente por Entregar"
        },
        {
            "ID": 2,
            "Nombre": "María",
            "Apellido": "Gómez",
            "Cédula": "87654321",
            "Asesora": "Andrea Ruiz",
            "Fecha Compra": (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d"),
            "Fecha Entrega Estimada": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            "Estado": "Pasados de Fecha"
        },
        {
            "ID": 3,
            "Nombre": "Ana",
            "Apellido": "Rodríguez",
            "Cédula": "11223344",
            "Asesora": "Laura Gómez",
            "Fecha Compra": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
            "Fecha Entrega Estimada": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
            "Estado": "Entregados"
        }
    ])

# Función para enviar notificaciones al escritorio
def enviar_alerta(titulo, mensaje):
    try:
        notification.notify(title=titulo, message=mensaje, app_name="Gestión Óptica", timeout=10)
    except Exception:
        pass

# --- BARRA SUPERIOR CON FECHA Y HORA EN TIEMPO REAL ---
dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
meses_es = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

ahora = datetime.now()
dia_sem_str = dias_semana[ahora.weekday()]
mes_str = meses_es[ahora.month]
fecha_hora_formateada = f"{dia_sem_str}, {ahora.day} de {mes_str} de {ahora.year} — {ahora.strftime('%I:%M:%S %p')}"

st.markdown(
    f"""
    <div class="top-bar">
        <span style="font-weight: 600; font-size: 15px; letter-spacing: 0.5px;">⚡ Panel Ejecutivo — Control de Óptica</span>
        <span style="font-size: 13px; font-weight: 300; opacity: 0.9;">🕒 {fecha_hora_formateada}</span>
    </div>
    """, unsafe_allow_html=True
)

# Encabezado Principal y Calendario Elegante Superior Derecho
col_title, col_cal = st.columns([1.6, 1.4])

with col_title:
    st.markdown("<h1 style='color: #0f172a; font-size: 28px; font-weight: 800; margin-bottom: 0px;'>Gestión de Órdenes</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 14px; margin-top: 4px; margin-bottom: 20px;'>Supervisa el estado de entrega de lentes, plazos hábiles y asignación de asesoras.</p>", unsafe_allow_html=True)
    
    # KPIs Modernos
    total_pendientes = len(st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Pendiente por Entregar"])
    total_atrasados = len(st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Pasados de Fecha"])
    total_entregados = len(st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Entregados"])
    
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.markdown(f"""<div class="kpi-card"><span style="color: #f59e0b; font-size: 22px; font-weight: 700;">{total_pendientes}</span><br><span style="color: #64748b; font-size: 12px; font-weight: 500;">Pendientes</span></div>""", unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"""<div class="kpi-card"><span style="color: #ef4444; font-size: 22px; font-weight: 700;">{total_atrasados}</span><br><span style="color: #64748b; font-size: 12px; font-weight: 500;">Atrasados</span></div>""", unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"""<div class="kpi-card"><span style="color: #10b981; font-size: 22px; font-weight: 700;">{total_entregados}</span><br><span style="color: #64748b; font-size: 12px; font-weight: 500;">Entregados</span></div>""", unsafe_allow_html=True)

with col_cal:
    now = datetime.now()
    cal = calendar.monthcalendar(now.year, now.month)
    month_name = meses_es[now.month]
    
    fechas_pendientes = st.session_state.pedidos[
        st.session_state.pedidos["Estado"].isin(["Pendiente por Entregar", "Pasados de Fecha"])
    ]["Fecha Entrega Estimada"].tolist()
    
    html_cal = f"""
    <div style="background-color: #ffffff; padding: 16px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); font-family: sans-serif; font-size: 13px;">
        <div style="font-weight: 700; text-align: center; margin-bottom: 10px; color: #1e293b; font-size: 14px;">📅 Calendario Activo — {month_name}</div>
        <table style="width: 100%; text-align: center; border-collapse: collapse;">
            <tr style="color: #94a3b8; font-size: 11px; font-weight: 600;">
                <th>Lu</th><th>Ma</th><th>Mi</th><th>Ju</th><th>Vi</th><th>Sá</th><th>Do</th>
            </tr>
    """
    for week in cal:
        html_cal += "<tr>"
        for day in week:
            if day == 0:
                html_cal += "<td style='padding: 5px;'></td>"
            else:
                fecha_str = f"{now.year}-{now.month:02d}-{day:02d}"
                is_delivery = fecha_str in fechas_pendientes
                if is_delivery:
                    html_cal += f"<td style='padding: 5px;'><span style='background-color: #10b981; color: white; padding: 4px 8px; border-radius: 50%; font-weight: 700; font-size: 11px;'>{day}</span></td>"
                else:
                    html_cal += f"<td style='padding: 5px; color: #475569; font-weight: 400;'>{day}</td>"
        html_cal += "</tr>"
    html_cal += "</table></div>"
    st.markdown(html_cal, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Barra lateral estilizada para registro de nuevos pedidos
with st.sidebar:
    st.markdown("<h2 style='font-size: 20px; font-weight: 700; color: #1e293b;'>📝 Nuevo Pedido</h2>", unsafe_allow_html=True)
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
            nuevo_pedido = pd.DataFrame([{
                "ID": nuevo_id,
                "Nombre": nombre,
                "Apellido": apellido,
                "Cédula": cedula,
                "Asesora": asesora if asesora else "No asignada",
                "Fecha Compra": fecha_compra.strftime("%Y-%m-%d"),
                "Fecha Entrega Estimada": fecha_entrega.strftime("%Y-%m-%d"),
                "Estado": "Pendiente por Entregar"
            }])
            
            st.session_state.pedidos = pd.concat([st.session_state.pedidos, nuevo_pedido], ignore_index=True)
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

# Listado de pedidos organizados en 3 columnas principales
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<h3 style='color: #d97706; font-size: 17px; font-weight: 700;'>⏳ Pendientes por Entregar</h3>", unsafe_allow_html=True)
    pendientes = st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Pendiente por Entregar"]
    if pendientes.empty:
        st.info("No hay pedidos pendientes.")
    for idx, row in pendientes.iterrows():
        st.markdown(
            f"""
            <div class="card-pendientes">
                <span style="font-size: 15px; font-weight: 700; color: #1e293b;">{row['Nombre']} {row['Apellido']}</span><br>
                <span style="font-size: 12px; color: #64748b;">🆔 Cédula: {row['Cédula']}</span>
            </div>
            """, unsafe_allow_html=True
        )
        with st.expander("📌 Ver Detalles y Acciones"):
            st.markdown(f"<div style='background-color: #fef3c7; padding: 8px; border-radius: 6px; text-align: center; font-weight: 700; color: #b45309; font-size: 13px; margin-bottom: 8px;'>📅 Entrega Estimada: {row['Fecha Entrega Estimada']}</div>", unsafe_allow_html=True)
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
    st.markdown("<h3 style='color: #dc2626; font-size: 17px; font-weight: 700;'>⚠️ Pasados de Fecha</h3>", unsafe_allow_html=True)
    atrasados = st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Pasados de Fecha"]
    if atrasados.empty:
        st.info("No hay pedidos atrasados.")
    for idx, row in atrasados.iterrows():
        st.markdown(
            f"""
            <div class="card-atrasados">
                <span style="font-size: 15px; font-weight: 700; color: #1e293b;">{row['Nombre']} {row['Apellido']}</span><br>
                <span style="font-size: 12px; color: #64748b;">🆔 Cédula: {row['Cédula']}</span>
            </div>
            """, unsafe_allow_html=True
        )
        with st.expander("📌 Ver Detalles y Acciones", expanded=True):
            st.markdown(f"<div style='background-color: #fee2e2; padding: 8px; border-radius: 6px; text-align: center; font-weight: 700; color: #b91c1c; font-size: 13px; margin-bottom: 8px;'>📅 Vencido Est: {row['Fecha Entrega Estimada']}</div>", unsafe_allow_html=True)
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
    st.markdown("<h3 style='color: #059669; font-size: 17px; font-weight: 700;'>✅ Entregados</h3>", unsafe_allow_html=True)
    entregados = st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Entregados"]
    if entregados.empty:
        st.info("No hay pedidos entregados.")
    for idx, row in entregados.iterrows():
        st.markdown(
            f"""
            <div class="card-entregados">
                <span style="font-size: 15px; font-weight: 700; color: #1e293b;">{row['Nombre']} {row['Apellido']}</span><br>
                <span style="font-size: 12px; color: #64748b;">🆔 Cédula: {row['Cédula']}</span>
            </div>
            """, unsafe_allow_html=True
        )
        with st.expander("📌 Ver Detalles y Acciones"):
            st.markdown(f"<div style='background-color: #d1fae5; padding: 8px; border-radius: 6px; text-align: center; font-weight: 700; color: #047857; font-size: 13px; margin-bottom: 8px;'>📅 Entregado el: {row['Fecha Entrega Estimada']}</div>", unsafe_allow_html=True)
            st.write(f"👤 **Asesora:** {row['Asesora']}")
            st.write(f"🛒 **Compra:** {row['Fecha Compra']}")
            
            if st.button("🗑️ Borrar", key=f"del_entregado_{row['ID']}", use_container_width=True):
                st.session_state.pedidos = st.session_state.pedidos.drop(idx).reset_index(drop=True)
                st.rerun()
