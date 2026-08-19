import mysql.connector
from mysql.connector import Error
from colorama import init, Fore, Back, Style

init(autoreset=True)

# Parámetros del servidor MySQL
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_USER = 'root'
DB_PASS = 'root'      # ⚠️ Recordá verificar tu contraseña de Workbench
DB_NAME = 'estacionmetereologica_proa'

print(Fore.CYAN + Style.BRIGHT + "=" * 60)
print(Fore.WHITE + Back.BLUE + Style.BRIGHT + " 🔍 PROBADOR DE CONEXIÓN A BASE DE DATOS (SIN ARDUINO) 🔍 ".center(60))
print(Fore.CYAN + Style.BRIGHT + "=" * 60)

try:
    # 1. Intentamos la conexión
    db = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )
    cursor = db.cursor()
    print(Fore.BLUE + Style.BRIGHT + f"✅ [EXITO] Conexión establecida con MySQL Workbench en el puerto {DB_PORT}.")

    # 2. Inserción de prueba
    sql = "INSERT INTO mediciones (temperatura, humedad, gas, fecha_hora) VALUES (%s, %s, %s, NOW())"
    valores_prueba = (22, 50, 180)  # Valores simulados de prueba
    
    cursor.execute(sql, valores_prueba)
    db.commit()
    print(Fore.CYAN + "💾 [TEST] Inserción de prueba realizada correctamente.")

    # 3. Consulta de verificación
    cursor.execute("SELECT id_mediciones, fecha_hora, temperatura, humedad, gas FROM mediciones ORDER BY id_mediciones DESC LIMIT 1;")
    ultimo_registro = cursor.fetchone()

    print("\n" + Fore.BLUE + Style.BRIGHT + "┌" + "─" * 58 + "┐")
    print(Fore.WHITE + Style.BRIGHT + f" │ ÚLTIMO REGISTRO GUARDADO EN LA BASE DE DATOS ".ljust(58) + "│")
    print(Fore.BLUE + Style.BRIGHT + "├" + "─" * 58 + "┤")
    print(Fore.WHITE + f" │ ID: {ultimo_registro[0]} | Fecha: {ultimo_registro[1]}".ljust(58) + "│")
    print(Fore.WHITE + f" │ 🌡️ Temp: {ultimo_registro[2]}°C | 💧 Humedad: {ultimo_registro[3]}% | 💨 Gas: {ultimo_registro[4]} PPM".ljust(58) + "│")
    print(Fore.BLUE + Style.BRIGHT + "└" + "─" * 58 + "┘\n")

    cursor.close()
    db.close()
    print(Fore.WHITE + Back.BLUE + Style.BRIGHT + " 🎉 ¡La base de datos está funcionando al 100%! Podés estar tranquila. ")

except Error as e:
    print(Fore.RED + Style.BRIGHT + f"\n❌ [ERROR] No se pudo conectar a MySQL Workbench: {e}")
    print(Fore.WHITE + "💡 Verificá que el servicio de MySQL esté corriendo y que la contraseña DB_PASS sea la correcta.")
