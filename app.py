import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from plyer import notification
import calendar

# Configuración de la página
st.set_page_config(layout="wide", page_title="Gestión de Óptica")

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
            "Fecha Entrega Estimada": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
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

# Título de la aplicación
st.title("👓 Sistema de Gestión de Pedidos - Óptica")

# Función para enviar notificaciones al escritorio
def enviar_alerta(titulo, mensaje):
    try:
        notification.notify(title=titulo, message=mensaje, app_name="Gestión Óptica", timeout=10)
    except Exception:
        pass

# Barra lateral: Registro y Calendario de Entregas
with st.sidebar:
    st.header("📝 Registrar Nuevo Pedido")
    with st.form("nuevo_pedido", clear_on_submit=True):
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        cedula = st.text_input("Número de Cédula")
        asesora = st.text_input("Asesora Responsable")
        dias_espera = st.number_input("Plazo de Entrega (Días)", min_value=1, value=5)
        
        btn_registrar = st.form_submit_button("Registrar Pedido")
        
        if btn_registrar and nombre and cedula:
            fecha_compra = datetime.now()
            fecha_entrega = fecha_compra + timedelta(days=int(dias_espera))
            
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

    st.markdown("---")
    st.header("📅 Calendario de Entregas")
    
    # Extraer fechas con entregas pendientes o atrasadas para resaltarlas
    fechas_pendientes = st.session_state.pedidos[
        st.session_state.pedidos["Estado"].isin(["Pendiente por Entregar", "Pasados de Fecha"])
    ]["Fecha Entrega Estimada"].tolist()
    
    now = datetime.now()
    cal = calendar.monthcalendar(now.year, now.month)
    month_name = calendar.month_name[now.month]
    
    st.markdown(f"**Mes actual: {month_name} {now.year}**")
    
    # Renderizar mini calendario visual en texto enriquecido/markdown
    cal_markdown = "Lu Ma Mi Ju Vi Sá Do\n"
    for week in cal:
        week_str = ""
        for day in week:
            if day == 0:
                week_str += " .  "
            else:
                fecha_str = f"{now.year}-{now.month:02d}-{day:02d}"
                if fecha_str in fechas_pendientes:
                    week_str += f"**[{day:2d}]** "
                else:
                    week_str += f"{day:2d}  "
        cal_markdown += week_str + "\n"
    
    st.text(cal_markdown)
    st.caption("Nota: Los días entre corchetes **[ ]** indican fechas con lentes programados para entrega o vencidos.")

# Verificación de estados y actualización automática
hoy_str = datetime.now().strftime("%Y-%m-%d")

for index, row in st.session_state.pedidos.iterrows():
    if row["Estado"] == "Pendiente por Entregar":
        fecha_entrega = datetime.strptime(row["Fecha Entrega Estimada"], "%Y-%m-%d")
        fecha_actual = datetime.strptime(hoy_str, "%Y-%m-%d")
        if fecha_entrega < fecha_actual:
            st.session_state.pedidos.at[index, "Estado"] = "Pasados de Fecha"
            enviar_alerta("Pedido Retrasado", f"El pedido de {row['Nombre']} {row['Apellido']} está pasado de la fecha de entrega.")

# Listado de pedidos organizados por columnas con estilos visuales
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ⏳ Pendientes por Entregar")
    pendientes = st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Pendiente por Entregar"]
    if pendientes.empty:
        st.info("No hay pedidos pendientes.")
    for idx, row in pendientes.iterrows():
        with st.container():
            st.markdown(
                f"""
                <div style="background-color: #f0f4f8; padding: 12px; border-radius: 8px; border-left: 5px solid #ffa500; margin-bottom: 10px;">
                    <strong>{row['Nombre']} {row['Apellido']}</strong><br>
                    <small>Cédula: {row['Cédula']}</small>
                </div>
                """, unsafe_allow_html=True
            )
            with st.expander("Ver detalles / Acciones"):
                st.write(f"📅 **Entrega Est:** {row['Fecha Entrega Estimada']}")
                st.write(f"👤 **Asesora:** {row['Asesora']}")
                st.write(f"🛒 **Compra:** {row['Fecha Compra']}")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("✅ Entregar", key=f"ent_{row['ID']}"):
                        st.session_state.pedidos.at[idx, "Estado"] = "Entregados"
                        st.rerun()
                with col_btn2:
                    if st.button("🗑️ Borrar", key=f"del_{row['ID']}"):
                        st.session_state.pedidos = st.session_state.pedidos.drop(idx).reset_index(drop=True)
                        st.rerun()

with col2:
    st.markdown("### ⚠️ Pasados de Fecha")
    atrasados = st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Pasados de Fecha"]
    if atrasados.empty:
        st.info("No hay pedidos atrasados.")
    for idx, row in atrasados.iterrows():
        with st.container():
            st.markdown(
                f"""
                <div style="background-color: #fdf2f2; padding: 12px; border-radius: 8px; border-left: 5px solid #ff4d4d; margin-bottom: 10px;">
                    <strong>{row['Nombre']} {row['Apellido']}</strong><br>
                    <small>Cédula: {row['Cédula']}</small>
                </div>
                """, unsafe_allow_html=True
            )
            with st.expander("Ver detalles / Acciones", expanded=True):
                st.write(f"📅 **Entrega Est:** {row['Fecha Entrega Estimada']}")
                st.write(f"👤 **Asesora:** {row['Asesora']}")
                st.write(f"🛒 **Compra:** {row['Fecha Compra']}")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("✅ Entregar", key=f"ent_atrasado_{row['ID']}"):
                        st.session_state.pedidos.at[idx, "Estado"] = "Entregados"
                        st.rerun()
                with col_btn2:
                    if st.button("🗑️ Borrar", key=f"del_atrasado_{row['ID']}"):
                        st.session_state.pedidos = st.session_state.pedidos.drop(idx).reset_index(drop=True)
                        st.rerun()

with col3:
    st.markdown("### ✅ Entregados")
    entregados = st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Entregados"]
    if entregados.empty:
        st.info("No hay pedidos entregados.")
    for idx, row in entregados.iterrows():
        with st.container():
            st.markdown(
                f"""
                <div style="background-color: #f2f9f2; padding: 12px; border-radius: 8px; border-left: 5px solid #28a745; margin-bottom: 10px;">
                    <strong>{row['Nombre']} {row['Apellido']}</strong><br>
                    <small>Cédula: {row['Cédula']}</small>
                </div>
                """, unsafe_allow_html=True
            )
            with st.expander("Ver detalles / Acciones"):
                st.write(f"📅 **Entrega Est:** {row['Fecha Entrega Estimada']}")
                st.write(f"👤 **Asesora:** {row['Asesora']}")
                st.write(f"🛒 **Compra:** {row['Fecha Compra']}")
                
                if st.button("🗑️ Borrar", key=f"del_entregado_{row['ID']}"):
                    st.session_state.pedidos = st.session_state.pedidos.drop(idx).reset_index(drop=True)
                    st.rerun()
