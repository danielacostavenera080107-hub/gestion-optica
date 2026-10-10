import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from plyer import notification
import calendar

# Configuración de la página (ancho completo)
st.set_page_config(layout="wide", page_title="Gestión de Óptica")

# Función para sumar días hábiles (excluyendo fines de semana)
def sumar_dias_habiles(fecha_inicio, dias_a_sumar):
    actual = fecha_inicio
    agregados = 0
    while agregados < dias_a_sumar:
        actual += timedelta(days=1)
        if actual.weekday() < 5:  # 0: Lunes - 4: Viernes
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
    <div style="background-color: #eef2f7; padding: 10px 15px; border-radius: 8px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; font-family: sans-serif;">
        <span style="font-weight: bold; color: #2c3e50; font-size: 14px;">🕒 Fecha y Hora Actual:</span>
        <span style="color: #34495e; font-size: 14px; font-weight: 500;">{fecha_hora_formateada}</span>
    </div>
    """, unsafe_allow_html=True
)

# Encabezado superior dividido: Título a la izquierda, Calendario elegante a la derecha
col_title, col_cal = st.columns([1.8, 1.2])

with col_title:
    st.title("👓 Sistema de Gestión de Pedidos - Óptica")
    st.markdown("Control de órdenes, asesoras y plazos de entrega hábiles.")

with col_cal:
    now = datetime.now()
    cal = calendar.monthcalendar(now.year, now.month)
    month_name = meses_es[now.month]
    
    # Extraer fechas con entregas pendientes o atrasadas
    fechas_pendientes = st.session_state.pedidos[
        st.session_state.pedidos["Estado"].isin(["Pendiente por Entregar", "Pasados de Fecha"])
    ]["Fecha Entrega Estimada"].tolist()
    
    # Renderizar calendario visual con HTML/CSS estilizado arriba a la derecha
    html_cal = f"""
    <div style="background-color: #ffffff; padding: 10px; border-radius: 10px; border: 1px solid #e0e0e0; box-shadow: 0 2px 4px rgba(0,0,0,0.05); font-family: sans-serif; font-size: 13px;">
        <div style="font-weight: bold; text-align: center; margin-bottom: 6px; color: #2c3e50;">📅 {month_name} {now.year}</div>
        <table style="width: 100%; text-align: center; border-collapse: collapse;">
            <tr style="color: #7f8c8d; font-size: 11px;">
                <th>Lu</th><th>Ma</th><th>Mi</th><th>Ju</th><th>Vi</th><th>Sá</th><th>Do</th>
            </tr>
    """
    for week in cal:
        html_cal += "<tr>"
        for day in week:
            if day == 0:
                html_cal += "<td style='padding: 3px;'></td>"
            else:
                fecha_str = f"{now.year}-{now.month:02d}-{day:02d}"
                is_delivery = fecha_str in fechas_pendientes
                if is_delivery:
                    html_cal += f"<td style='padding: 3px;'><span style='background-color: #28a745; color: white; padding: 2px 6px; border-radius: 50%; font-weight: bold;'>{day}</span></td>"
                else:
                    html_cal += f"<td style='padding: 3px; color: #333;'>{day}</td>"
        html_cal += "</tr>"
    html_cal += "</table></div>"
    st.markdown(html_cal, unsafe_allow_html=True)

st.markdown("---")

# Barra lateral para ingreso de nuevos pedidos
with st.sidebar:
    st.header("📝 Registrar Nuevo Pedido")
    with st.form("nuevo_pedido", clear_on_submit=True):
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        cedula = st.text_input("Número de Cédula")
        asesora = st.text_input("Asesora Responsable")
        dias_espera = st.number_input("Plazo de Entrega (Días Hábiles)", min_value=1, value=5)
        
        btn_registrar = st.form_submit_button("Registrar Pedido")
        
        if btn_registrar and nombre and cedula:
            fecha_compra = datetime.now()
            # Calcular fecha de entrega sumando solo días hábiles
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

# Verificación de estados y actualización automática
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
    st.markdown("### ⏳ Pendientes por Entregar")
    pendientes = st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Pendiente por Entregar"]
    if pendientes.empty:
        st.info("No hay pedidos pendientes.")
    for idx, row in pendientes.iterrows():
        st.markdown(
            f"""
            <div style="background-color: #f8f9fa; padding: 12px; border-radius: 8px 8px 0 0; border-left: 5px solid #ffa500; border-top: 1px solid #e0e0e0; border-right: 1px solid #e0e0e0;">
                <strong>{row['Nombre']} {row['Apellido']}</strong><br>
                <small style="color: #666;">Cédula: {row['Cédula']}</small>
            </div>
            """, unsafe_allow_html=True
        )
        with st.expander("📌 Ver Detalles y Acciones"):
            st.
