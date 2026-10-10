import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from plyer import notification
import calendar

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

# Inicialización de estado con datos de ejemplo para el mes actual
if 'pedidos' not in st.session_state:
    mes_actual_default = datetime.now().strftime("%Y-%m")
    p1 = {
        "ID": 1, "Nombre": "Carlos", "Apellido": "Pérez", "Cédula": "12345678",
        "Asesora": "Laura Gómez", "Fecha Compra": datetime.now().strftime("%Y-%m-%d"),
        "Fecha Entrega Estimada": sumar_dias_habiles(datetime.now(), 3).strftime("%Y-%m-%d"),
        "Estado": "Pendiente por Entregar", "Mes Periodo": mes_actual_default
    }
    p2 = {
        "ID": 2, "Nombre": "Ana", "Apellido": "Rodríguez", "Cédula": "11223344",
        "Asesora": "Andrea Ruiz", "Fecha Compra": datetime.now().strftime("%Y-%m-%d"),
        "Fecha Entrega Estimada": datetime.now().strftime("%Y-%m-%d"),
        "Estado": "Entregados", "Mes Periodo": mes_actual_default
    }
    st.session_state.pedidos = pd.DataFrame([p1, p2])

if 'cal_year' not in st.session_state:
    st.session_state.cal_year = datetime.now().year
if 'cal_month' not in st.session_state:
    st.session_state.cal_month = datetime.now().month

# Función para notificaciones nativas
def enviar_alerta(titulo, mensaje):
    try:
        notification.notify(title=titulo, message=mensaje, app_name="LENS VISION", timeout=10)
    except Exception:
        pass

# --- BARRA SUPERIOR NATIVA ---
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%); padding: 18px 25px; border-radius: 14px; color: white; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 25px;">
    <span style="font-weight: 700; font-size: 16px;">⚡ LENS VISION — Panel Ejecutivo de Control Óptico</span>
    <span style="font-size: 13px; font-weight: 600; background: rgba(255,255,255,0.15); padding: 6px 14px; border-radius: 20px;">📅 Gestión y Trazabilidad</span>
</div>
""", unsafe_allow_html=True)

# Variables de Mes y Año seleccionados en el calendario
c_y = st.session_state.cal_year
c_m = st.session_state.cal_month
periodo_actual_str = f"{c_y}-{c_m:02d}"

# Encabezado Principal y Calendario Interactivo con Navegación de Meses
col_title, col_cal = st.columns([1.6, 1.4], gap="large")

with col_title:
    st.markdown("<h1 style='color: #ffffff; font-size: 28px; font-weight: 800; margin-bottom: 0px; text-shadow: 0 2px 4px rgba(0,0,0,0.5);'>Órdenes de Lentes 👓</h1>", unsafe_allow_html=True)
    meses_es = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    month_name = meses_es[c_m]
    st.markdown(f"<p style='color: #e2e8f0; font-size: 14px; margin-top: 4px; margin-bottom: 24px; font-weight: 600; text-shadow: 0 1px 2px rgba(0,0,0,0.5);'>Viendo registros independientes del periodo: <b>{month_name} {c_y}</b></p>", unsafe_allow_html=True)
    
    df_p = st.session_state.pedidos
    
    # Filtrar estrictamente los pedidos del mes activo
    df_mes = df_p[df_p["Mes Periodo"] == periodo_actual_str] if "Mes Periodo" in df_p.columns else pd.DataFrame(columns=df_p.columns)
    
    total_pendientes = len(df_mes[df_mes["Estado"] == "Pendiente por Entregar"]) if not df_mes.empty else 0
    total_atrasados = len(df_mes[df_mes["Estado"] == "Pasados de Fecha"]) if not df_mes.empty else 0
    total_entregados = len(df_mes[df_mes["Estado"] == "Entregados"]) if not df_mes.empty else 0
    total_garantias = len(df_mes[df_mes["Estado"] == "En Garantía"]) if not df_mes.empty else 0
    total_vendidos_mes = total_entregados  # Cuenta los entregados exclusivamente de este mes
    
    # 5 Métricas KPIs Organizadas
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        st.markdown(f'<div class="metric-container"><span style="color: #f59e0b; font-size: 18px; font-weight: 800;">{total_pendientes}</span><br><span style="color: #64748b; font-size: 9px; font-weight: 700;">PENDIENTES</span></div>
