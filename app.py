import streamlit as st
import pandas as pd

# 🔹 Cargar los datos de clientes con su historial de pagos
df_clientes = pd.read_csv("clientes_clusterizados.csv")

# 🔹 Interfaz de Streamlit
st.title("🚀 Evaluación de Crédito para Clientes")

# 🔹 Ingreso del código de cliente
codigo_cliente = st.text_input("Ingrese el código del cliente:")

if codigo_cliente:
    if codigo_cliente in df_clientes["codigo_cliente"].astype(str).values:   # astype(str) --> para cambiar al tipo de dato String
        cliente_info = df_clientes[df_clientes["codigo_cliente"].astype(str) == codigo_cliente].iloc[0]   # iloc[x] ---> para seleccionar la row deseada

        # 🔹 Mostrar información del cliente
        dias_pago = int(cliente_info['dias_en_calle'])
        importe_total = cliente_info['importe_total']

        st.write(f"**Días de pago ponderado:** {dias_pago} días")
        st.write(f"**Importe total comprado:** ${importe_total:,.2f}")

        # 🔹 Evaluar viabilidad de crédito
        if dias_pago <= 15:
            st.success("✅ **Buen pagador** - Cliente APTO para crédito")
        elif 16 <= dias_pago <= 30:
            st.warning("⚠️ **Pagador regular** - Crédito con condiciones")
        else:
            st.error("❌ **Mal pagador** - Cliente NO APTO para crédito")
    
    else:
        st.warning("⚠️ Cliente no encontrado en la base de datos.")
