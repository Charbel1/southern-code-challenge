from datetime import datetime

fecha_inicio = "12/21/2021"
fecha_fin = "12/30/2021"
fecha3 = "12/25/2021"
fecha_inicio_1 = datetime.strptime(fecha_inicio, '%m/%d/%Y')
fecha_fin_2 = datetime.strptime(fecha_fin, '%m/%d/%Y')
fecha_dt3 = datetime.strptime(fecha3, '%m/%d/%Y')
if fecha_dt3 in [fecha_inicio_1,fecha_fin_2]:
    print("claro que yes")
if fecha_inicio_1 < fecha_dt3 and fecha_dt3 < fecha_fin_2:
    print("yes")
print(fecha_fin_2 - fecha_inicio_1)

print(type(fecha_fin_2))