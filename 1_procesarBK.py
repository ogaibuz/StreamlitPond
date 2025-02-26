import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# 🔹 Cargar los datos
df = pd.read_csv("clientes_pagos.csv")

# 🔹 Calcular días de pago ponderados
df["dias_pago"] = (pd.to_datetime(df["fecha_pago"]) - pd.to_datetime(df["fecha_factura"])).dt.days
df["dias_pago_ponderado"] = df["dias_pago"] * (df["importe_factura"] / df.groupby("codigo_cliente")["importe_factura"].transform("sum"))

print(df)

# 🔹 Agrupar por cliente y calcular el promedio ponderado
df_clientes = df.groupby("codigo_cliente").agg(
    dias_pago_ponderado=("dias_pago_ponderado", "sum"),
    importe_total=("importe_factura", "sum")
).reset_index()

# 🔹 Normalizar los datos
scaler = StandardScaler()
df_clientes[["dias_pago_ponderado", "importe_total"]] = scaler.fit_transform(df_clientes[["dias_pago_ponderado", "importe_total"]])

# 🔹 Aplicar K-Means para segmentar clientes
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df_clientes["cluster"] = kmeans.fit_predict(df_clientes[["dias_pago_ponderado", "importe_total"]])

# 🔹 Guardar el resultado en un nuevo CSV
df_clientes.to_csv("clientes_clusterizados.csv", index=False)

print("✅ Proceso completado. Archivo 'clientes_clusterizados.csv' generado correctamente.")
