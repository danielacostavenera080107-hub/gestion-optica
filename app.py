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

# Encabezado superior dividido: Título a la izquierda, Calendario elegante a la derecha
col_title, col_cal = st.columns([1.8, 1.2])

with col_title:
    st.title("👓 Sistema de Gestión de Pedidos - Óptica")
    st.markdown("Control de órdenes, asesoras y plazos de entrega hábiles.")

with col_cal:
    now = datetime.now()
    cal = calendar.monthcalendar(now.year, now.month)
    meses_es = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
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
            st.markdown(f"<div style='background-color: #fff3cd; padding: 8px; border-radius: 6px; text-align: center; font-weight: bold; color: #856404;'>📅 Entrega Estimada: {row['Fecha Entrega Estimada']}</div>", unsafe_allow_html=True)
            st.write(f"👤 **Asesora:** {row['Asesora']}")
            st.write(f"🛒 **Compra:** {row['Fecha Compra']}")
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Entregar", key=f"ent_{row['ID']}"):
                    st.session_state.pedidos.at[idx, "Estado"] = "Entregados"
                    st.rerun()
            with c2:
                if st.button("🗑️ Borrar", key=f"del_{row['ID']}"):
                    st.session_state.pedidos = st.session_state.pedidos.drop(idx).reset_index(drop=True)
                    st.rerun()

with col2:
    st.markdown("### ⚠️ Pasados de Fecha")
    atrasados = st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Pasados de Fecha"]
    if atrasados.empty:
        st.info("No hay pedidos atrasados.")
    for idx, row in atrasados.iterrows():
        st.markdown(
            f"""
            <div style="background-color: #fdf2f2; padding: 12px; border-radius: 8px 8px 0 0; border-left: 5px solid #ff4d4d; border-top: 1px solid #e0e0e0; border-right: 1px solid #e0e0e0;">
                <strong>{row['Nombre']} {row['Apellido']}</strong><br>
                <small style="color: #666;">Cédula: {row['Cédula']}</small>
            </div>
            """, unsafe_allow_html=True
        )
        with st.expander("📌 Ver Detalles y Acciones", expanded=True):
            st.markdown(f"<div style='background-color: #f8d7da; padding: 8px; border-radius: 6px; text-align: center; font-weight: bold; color: #721c24;'>📅 Vencido Est: {row['Fecha Entrega Estimada']}</div>", unsafe_allow_html=True)
            st.write(f"👤 **Asesora:** {row['Asesora']}")
            st.write(f"🛒 **Compra:** {row['Fecha Compra']}")
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Entregar", key=f"ent_atrasado_{row['ID']}"):
                    st.session_state.pedidos.at[idx, "Estado"] = "Entregados"
                    st.rerun()
            with c2:
                if st.button("🗑️ Borrar", key=f"del_atrasado_{row['ID']}"):
                    st.session_state.pedidos = st.session_state.pedidos.drop(idx).reset_index(drop=True)
                    st.rerun()

with col3:
    st.markdown("### ✅ Entregados")
    entregados = st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Entregados"]
    if entregados.empty:
        st.info("No hay pedidos entregados.")
    for idx, row in entregados.iterrows():
        st.markdown(
            f"""
            <div style="background-color: #f2f9f2; padding: 12px; border-radius: 8px 8px 0 0; border-left: 5px solid #28a745; border-top: 1px solid #e0e0e0; border-right: 1px solid #e0e0e0;">
                <strong>{row['Nombre']} {row['Apellido']}</strong><br>
                <small style="color: #666;">Cédula: {row['Cédula']}</small>
            </div>
            """, unsafe_allow_html=True
        )
        with st.expander("📌 Ver Detalles y Acciones"):
            st.markdown(f"<div style='background-color: #d4edda; padding: 8px; border-radius: 6px; text-align: center; font-weight: bold; color: #155724;'>📅 Entregado el: {row['Fecha Entrega Estimada']}</div>", unsafe_allow_html=True)
            st.write(f"👤 **Asesora:** {row['Asesora']}")
            st.write(f"🛒 **Compra:** {row['Fecha Compra']}")
            
            if st.button("🗑️ Borrar", key=f"del_entregado_{row['ID']}"):
                st.session_state.pedidos = st.session_state.pedidos.drop(idx).reset_index(drop=True)
                st.rerun()
