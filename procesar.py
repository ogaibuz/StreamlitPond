import pandas as pd

# 🔹 Cargar los datos
df = pd.read_csv("clientes_pagos.csv", sep=';')

# Convertir la fecha con el formato correcto
df["fecha_factura"] = pd.to_datetime(df["fecha_factura"], format="%m-%d-%Y", errors="coerce")
df["fecha_pago"] = pd.to_datetime(df["fecha_pago"], format="%m-%d-%Y", errors="coerce")

print(df)

# 🔹 Calcular "Días en la Calle"
df["dias_en_calle"] = (pd.to_datetime(df["fecha_pago"]) - pd.to_datetime(df["fecha_factura"])).dt.days

# 🔹 Calcular promedio ponderado de "Días en la Calle" por cliente
df["dias_en_calle_ponderado"] = df["dias_en_calle"] * (df["importe_factura"] / df.groupby("codigo_cliente")["importe_factura"].transform("sum"))

# 🔹 Agrupar por cliente y calcular el total
df_clientes = df.groupby("codigo_cliente").agg(
    dias_en_calle=("dias_en_calle_ponderado", "sum"),
    importe_total=("importe_factura", "sum")
).reset_index()

# 🔹 Guardar el resultado en un CSV
df_clientes.to_csv("clientes_clusterizados.csv", index=False)

print("✅ Archivo 'clientes_clusterizados.csv' generado con éxito.")
