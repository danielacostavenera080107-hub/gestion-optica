import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from plyer import notification
import calendar

# Configuración de la página (ancho completo)
st.set_page_config(layout="wide", page_title="Gestión de Óptica Profesional")

# Estilos CSS personalizados para mejorar el aspecto visual (eliminar aspecto plano)
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e3e6f0;
        text-align: center;
    }
    .card-pendientes {
        background: #ffffff;
        padding: 14px;
        border-radius: 10px;
        border-left: 6px solid #f6c23e;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        margin-bottom: 12px;
        border-top: 1px solid #eaecf4;
        border-right: 1px solid #eaecf4;
        border-bottom: 1px solid #eaecf4;
    }
    .card-atrasados {
        background: #ffffff;
        padding: 14px;
        border-radius: 10px;
        border-left: 6px solid #e74a3b;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        margin-bottom: 12px;
        border-top: 1px solid #eaecf4;
        border-right: 1px solid #eaecf4;
        border-bottom: 1px solid #eaecf4;
    }
    .card-entregados {
        background: #ffffff;
        padding: 14px;
        border-radius: 10px;
        border-left: 6px solid #1cc88a;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        margin-bottom: 12px;
        border-top: 1px solid #eaecf4;
        border-right: 1px solid #eaecf4;
        border-bottom: 1px solid #eaecf4;
    }
    </style>
""", unsafe_allow_html=True)

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

# --- BARRA SUPERIOR CON FECHA, HORA Y ESTILO ELEGANTE ---
dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
meses_es = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

ahora = datetime.now()
dia_sem_str = dias_semana[ahora.weekday()]
mes_str = meses_es[ahora.month]
fecha_hora_formateada = f"{dia_sem_str}, {ahora.day} de {mes_str} de {ahora.year} — {ahora.strftime('%I:%M:%S %p')}"

st.markdown(
    f"""
    <div style="background: linear-gradient(135deg, #4e73df 0%, #224abe 100%); padding: 12px 20px; border-radius: 10px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <span style="font-weight: 600; font-size: 15px;">🚀 Panel de Control Óptica</span>
        <span style="font-size: 14px; font-weight: 400;">🕒 {fecha_hora_formateada}</span>
    </div>
    """, unsafe_allow_html=True
)

# Encabezado principal y Calendario visual superior derecho
col_title, col_cal = st.columns([1.7, 1.3])

with col_title:
    st.title("👓 Sistema de Gestión de Pedidos")
    st.markdown("Administración avanzada de órdenes, control de plazos hábiles y seguimiento de asesoras.")
    
    # Métricas rápidas (KPIs) para dar vida al panel superior
    total_pendientes = len(st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Pendiente por Entregar"])
    total_atrasados = len(st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Pasados de Fecha"])
    total_entregados = len(st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Entregados"])
    
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.markdown(f"""<div class="metric-card"><span style="color: #f6c23e; font-size: 20px; font-weight: bold;">{total_pendientes}</span><br><small style="color: #6e707e;">Pendientes</small></div>""", unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"""<div class="metric-card"><span style="color: #e74a3b; font-size: 20px; font-weight: bold;">{total_atrasados}</span><br><small style="color: #6e707e;">Atrasados</small></div>""", unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"""<div class="metric-card"><span style="color: #1cc88a; font-size: 20px; font-weight: bold;">{total_entregados}</span><br><small style="color: #6e707e;">Entregados</small></div>""", unsafe_allow_html=True)

with col_cal:
    now = datetime.now()
    cal = calendar.monthcalendar(now.year, now.month)
    month_name = meses_es[now.month]
    
    fechas_pendientes = st.session_state.pedidos[
        st.session_state.pedidos["Estado"].isin(["Pendiente por Entregar", "Pasados de Fecha"])
    ]["Fecha Entrega Estimada"].tolist()
    
    html_cal = f"""
    <div style="background-color: #ffffff; padding: 14px; border-radius: 12px; border: 1px solid #e3e6f0; box-shadow: 0 4px 6px rgba(0,0,0,0.05); font-family: sans-serif; font-size: 13px;">
        <div style="font-weight: bold; text-align: center; margin-bottom: 8px; color: #4e73df; font-size: 14px;">📅 Calendario de Entregas — {month_name}</div>
        <table style="width: 100%; text-align: center; border-collapse: collapse;">
            <tr style="color: #b7b9cc; font-size: 11px; font-weight: bold;">
                <th>Lu</th><th>Ma</th><th>Mi</th><th>Ju</th><th>Vi</th><th>Sá</th><th>Do</th>
            </tr>
    """
    for week in cal:
        html_cal += "<tr>"
        for day in week:
            if day == 0:
                html_cal += "<td style='padding: 4px;'></td>"
            else:
                fecha_str = f"{now.year}-{now.month:02d}-{day:02d}"
                is_delivery = fecha_str in fechas_pendientes
                if is_delivery:
                    html_cal += f"<td style='padding: 4px;'><span style='background-color: #1cc88a; color: white; padding: 3px 7px; border-radius: 50%; font-weight: bold; font-size: 11px;'>{day}</span></td>"
                else:
                    html_cal += f"<td style='padding: 4px; color: #5a5c69;'>{day}</td>"
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

# Listado de pedidos organizados en 3 columnas principales con tarjetas mejoradas
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ⏳ Pendientes por Entregar")
    pendientes = st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Pendiente por Entregar"]
    if pendientes.empty:
        st.info("No hay pedidos pendientes.")
    for idx, row in pendientes.iterrows():
        st.markdown(
            f"""
            <div class="card-pendientes">
                <span style="font-size: 15px; font-weight: bold; color: #3a3b45;">{row['Nombre']} {row['Apellido']}</span><br>
                <span style="font-size: 12px; color: #858796;">🆔 Cédula: {row['Cédula']}</span>
            </div>
            """, unsafe_allow_html=True
        )
        with st.expander("📌 Ver Detalles y Acciones"):
            st.markdown(f"<div style='background-color: #fdf3dc; padding: 8px; border-radius: 6px; text-align: center; font-weight: bold; color: #b78103; font-size: 13px;'>📅 Entrega Est: {row['Fecha Entrega Estimada']}</div>", unsafe_allow_html=True)
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
            <div class="card-atrasados">
                <span style="font-size: 15px; font-weight: bold; color: #3a3b45;">{row['Nombre']} {row['Apellido']}</span><br>
                <span style="font-size: 12px; color: #858796;">🆔 Cédula: {row['Cédula']}</span>
            </div>
            """, unsafe_allow_html=True
        )
        with st.expander("📌 Ver Detalles y Acciones", expanded=True):
            st.markdown(f"<div style='background-color: #fce8e6; padding: 8px; border-radius: 6px; text-align: center; font-weight: bold; color: #c5221f; font-size: 13px;'>📅 Vencido Est: {row['Fecha Entrega Estimada']}</div>", unsafe_allow_html=True)
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
            <div class="card-entregados">
                <span style="font-size: 15px; font-weight: bold; color: #3a3b45;">{row['Nombre']} {row['Apellido']}</span><br>
                <span style="font-size: 12px; color: #858796;">🆔 Cédula: {row['Cédula']}</span>
            </div>
            """, unsafe_allow_html=True
        )
        with st.expander("📌 Ver Detalles y Acciones"):
            st.markdown(f"<div style='background-color: #e6f4ea; padding: 8px; border-radius: 6px; text-align: center; font-weight: bold; color: #137333; font-size: 13px;'>📅 Entregado el: {row['Fecha Entrega Estimada']}</div>", unsafe_allow_html=True)
            st.write(f"👤 **Asesora:** {row['Asesora']}")
            st.write(f"🛒 **Compra:** {row['Fecha Compra']}")
            
            if st.button("🗑️ Borrar", key=f"del_entregado_{row['ID']}"):
                st.session_state.pedidos = st.session_state.pedidos.drop(idx).reset_index(drop=True)
                st.rerun()
