import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# 🔹 Cargar los datos clusterizados
df_clientes = pd.read_csv("clientes_clusterizados.csv")

# 🔹 Cargar el modelo de clustering entrenado
scaler = StandardScaler()
scaler.fit(df_clientes[["dias_pago_ponderado", "importe_total"]])
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
kmeans.fit(df_clientes[["dias_pago_ponderado", "importe_total"]])

# 🔹 Interfaz de Streamlit
st.title("🚀 Clasificación de Clientes según Pagos")

# 🔹 Opción 1: Consultar cliente existente
codigo_cliente = st.text_input("Ingrese el código del cliente:")

if codigo_cliente:
    if codigo_cliente in df_clientes["codigo_cliente"].astype(str).values:
        cliente_info = df_clientes[df_clientes["codigo_cliente"].astype(str) == codigo_cliente].iloc[0]
        st.write(f"**Días de pago ponderado:** {int(cliente_info['dias_pago_ponderado'])}")
        st.write(f"**Importe total comprado:** ${cliente_info['importe_total']:,.2f}")
        st.write(f"**Categoría del cliente:** {cliente_info['cluster']}")
    else:
        st.warning("⚠️ Cliente no encontrado en la base de datos.")

# 🔹 Opción 2: Ingresar un nuevo cliente para predecir su categoría
st.subheader("🆕 Evaluar un nuevo cliente")

dias_pago_nuevo = st.number_input("Días de pago ponderado:", min_value=0, max_value=180, step=1)
importe_nuevo = st.number_input("Importe total comprado:", min_value=0, step=100)

if st.button("Predecir categoría"):
    # Normalizar los valores ingresados
    new_data = np.array([[dias_pago_nuevo, importe_nuevo]])
    new_data_scaled = scaler.transform(new_data)

    # Predecir el cluster
    cluster_predicho = kmeans.predict(new_data_scaled)[0]
    
    st.success(f"✅ Este cliente pertenece a la categoría {cluster_predicho}")
