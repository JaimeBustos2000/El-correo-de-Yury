import cx_Oracle

# Datos de conexión a la base de datos Oracle
usuario = 'correosyurymda'
contraseña = "53492840Aa!!!"
direccion_ip = '68.154.50.137'  # Reemplaza con la IP pública de tu máquina virtual
puerto = "1521"  # Puerto estándar de Oracle
nombre_servicio = 'orcl'  # Nombre del servicio de la base de datos Oracle

# Construir el string de conexión
dsn = cx_Oracle.makedsn(direccion_ip, puerto, service_name=nombre_servicio)
connection = cx_Oracle.connect(user=usuario, password=contraseña, dsn=dsn)

# Verificar si la conexión es exitosa
if connection:
    print("Conexión exitosa a Oracle desde Python en VSCode.")
    connection.close()
else:
    print("No se pudo establecer la conexión.")