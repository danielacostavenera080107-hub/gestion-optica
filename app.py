import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from plyer import notification

# Configuración de la página
st.set_page_config(layout="wide", page_title="Gestión de Óptica")

# Inicialización de estado para la base de datos
if 'pedidos' not in st.session_state:
    st.session_state.pedidos = pd.DataFrame(columns=[
        "ID", "Nombre", "Apellido", "Cédula", 
        "Fecha Compra", "Fecha Entrega Estimada", "Estado"
    ])

# Título de la aplicación
st.title("Sistema de Gestión de Pedidos - Óptica")

# Función para enviar notificaciones al escritorio
def enviar_alerta(titulo, mensaje):
    try:
        notification.notify(
            title=titulo,
            message=mensaje,
            app_name="Gestión Óptica",
            timeout=10
        )
    except Exception:
        # En entornos cloud o si no hay soporte de escritorio nativo, evitamos que falle la app
        pass

# Barra lateral para ingreso de nuevos pedidos
with st.sidebar:
    st.header("Registrar Nuevo Pedido")
    with st.form("nuevo_pedido", clear_on_submit=True):
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        cedula = st.text_input("Número de Cédula")
        dias_espera = st.number_input("Plazo de Entrega (Días)", min_value=1, value=5)
        
        btn_registrar = st.form_submit_button("Registrar Pedido")
        
        if btn_registrar and nombre and cedula:
            fecha_compra = datetime.now()
            fecha_entrega = fecha_compra + timedelta(days=int(dias_espera))
            
            nuevo_id = len(st.session_state.pedidos) + 1
            nuevo_pedido = pd.DataFrame([{
                "ID": nuevo_id,
                "Nombre": nombre,
                "Apellido": apellido,
                "Cédula": cedula,
                "Fecha Compra": fecha_compra.strftime("%Y-%m-%d"),
                "Fecha Entrega Estimada": fecha_entrega.strftime("%Y-%m-%d"),
                "Estado": "Pendiente por Entregar"
            }])
            
            st.session_state.pedidos = pd.concat([st.session_state.pedidos, nuevo_pedido], ignore_index=True)
            enviar_alerta("Pedido Registrado", f"Pedido para {nombre} {apellido} registrado con éxito.")

# Verificación de estados y actualización automática
hoy_str = datetime.now().strftime("%Y-%m-%d")

for index, row in st.session_state.pedidos.iterrows():
    if row["Estado"] == "Pendiente por Entregar":
        fecha_entrega = datetime.strptime(row["Fecha Entrega Estimada"], "%Y-%m-%d")
        fecha_actual = datetime.strptime(hoy_str, "%Y-%m-%d")
        if fecha_entrega < fecha_actual:
            st.session_state.pedidos.at[index, "Estado"] = "Pasados de Fecha"
            enviar_alerta("Pedido Retrasado", f"El pedido de {row['Nombre']} {row['Apellido']} está pasado de la fecha de entrega.")

# Listado de pedidos organizados por columnas
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Pendientes por Entregar")
    pendientes = st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Pendiente por Entregar"]
    for idx, row in pendientes.iterrows():
        with st.expander(f"{row['Nombre']} {row['Apellido']} (Cédula: {row['Cédula']})"):
            st.write(f"Fecha Entrega Est.: {row['Fecha Entrega Estimada']}")
            if st.button("Marcar como Entregado", key=f"entregado_{row['ID']}"):
                st.session_state.pedidos.at[idx, "Estado"] = "Entregados"
                st.rerun()

with col2:
    st.subheader("Pasados de Fecha")
    atrasados = st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Pasados de Fecha"]
    for idx, row in atrasados.iterrows():
        with st.expander(f"{row['Nombre']} {row['Apellido']} (Cédula: {row['Cédula']})", expanded=True):
            st.write(f"Fecha Entrega Est.: {row['Fecha Entrega Estimada']}")
            if st.button("Marcar como Entregado", key=f"entregado_atrasado_{row['ID']}"):
                st.session_state.pedidos.at[idx, "Estado"] = "Entregados"
                st.rerun()

with col3:
    st.subheader("Entregados")
    entregados = st.session_state.pedidos[st.session_state.pedidos["Estado"] == "Entregados"]
    for _, row in entregados.iterrows():
        with st.expander(f"{row['Nombre']} {row['Apellido']} (Cédula: {row['Cédula']})"):
            st.write(f"Fecha Compra: {row['Fecha Compra']}")
            st.write(f"Fecha Entrega Estimada: {row['Fecha Entrega Estimada']}")
