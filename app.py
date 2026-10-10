import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from plyer import notification
import calendar

# Configuración de la página
st.set_page_config(layout="wide", page_title="Sistema de Gestión — Óptica")

# Estilos CSS avanzados para un diseño moderno, limpio y profesional
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background-color: #f8fafc;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Barra superior moderna */
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

    /* Tarjetas de Métricas (KPIs) */
    .metric-container {
        background: #ffffff;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -1px rgba(0, 0, 0, 0.02);
        border: 1px solid #f1f5f9;
        text-align: center;
        transition: transform 0.3s ease;
    }
    .metric-container:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
    }

    /* Tarjetas de Pedidos Individuales */
    .card-base {
        background: #ffffff;
        padding: 16px;
        border-radius: 14px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 12px;
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease;
    }
    .card-base:hover {
        box-shadow: 0 6px 12px rgba(0,0,0,0.05);
    }
    .border-pendientes { border-left: 6px solid #f59e0b; }
    .border-atrasados { border-left: 6px solid #ef4444; }
    .border-entregados { border-left: 6px solid #10b981; }

    /* Estilo barra lateral */
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

# Función para notificaciones
def enviar_alerta(titulo, mensaje):
    try:
        notification.notify(title=titulo, message=mensaje, app_name="Gestión Óptica", timeout=10)
    except Exception:
        pass

# --- BARRA SUPERIOR CON FECHA Y HORA ---
dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
meses_es = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

ahora = datetime.now()
dia_sem_str = dias_semana[ahora.weekday()]
mes_str = meses_es[ahora.month]
fecha_hora_formateada = f"{dia_sem_str}, {ahora.day} de {mes_str} de {ahora.year} — {ahora.strftime('%I:%M:%S %p')}"

st.markdown(
    f"""
    <div class="hero-banner">
        <div>
            <span style="font-weight: 700; font-size: 16px; letter-spacing: 0.5px;">⚡ Panel Ejecutivo de Control Óptico</span>
        </div>
        <div style="font-size: 13px; font-weight: 500; opacity: 0.9; background: rgba(255,255,255,0.1); padding: 6px 14px; border-radius: 20px;">
            🕒 {fecha_hora_formateada}
        </div>
    </div>
    """, unsafe_allow_html=True
)

# Encabezado Principal y Calendario Elegante Superior Derecho
col_title, col_cal = st.columns([1.6, 1.4], gap="large")

with col_title:
    st.markdown("<h1 style='color: #0f172a; font-size: 30px; font-weight: 800; margin-bottom: 0px;'>Órdenes de Lentes</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 14px; margin-top: 4px; margin-bottom: 24px;'>Supervisa eficientemente las entregas, plazos en días hábiles y el rendimiento del personal.</p>", unsafe_allow_html=True)
    
    # KPIs Modernos
    total_pendientes = len(st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Pendiente por Entregar"])
    total_atrasados = len(st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Pasados de Fecha"])
    total_entregados = len(st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Entregados"])
    
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.markdown(f"""<div class="metric-container"><span style="color: #f59e0b; font-size: 24px; font-weight: 800;">{total_pendientes}</span><br><span style="color: #64748b; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Pendientes</span></div>""", unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"""<div class="metric-container"><span style="color: #ef4444; font-size: 24px; font-weight: 800;">{total_atrasados}</span><br><span style="color: #64748b; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Atrasados</span></div>""", unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"""<div class="metric-container"><span style="color: #10b981; font-size: 24px; font-weight: 800;">{total_entregados}</span><br><span style="color: #64748b; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Entregados</span></div>""", unsafe_allow_html=True)

with col_cal:
    now = datetime.now()
    cal = calendar.monthcalendar(now.year, now.month)
    month_name = meses_es[now.month]
    
    fechas_pendientes =
