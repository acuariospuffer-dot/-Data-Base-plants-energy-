
import serial
import time
import csv
import os

# --- CONFIGURACIÓN INICIAL ---
puerto_arduino = 'COM3' 
baudios = 9600
nombre_archivo = "datos_planta.csv"

try:
    # 1. INICIO DE LA COMUNICACIÓN
    arduino = serial.Serial(puerto_arduino, baudios)
    time.sleep(2) 
    print(f"--- CONECTADO EXITOSAMENTE AL {puerto_arduino} ---")
    print("Grabando datos... Presiona Ctrl+C para dejar de grabar y buscar un dato.")

    # 2. PROCESO DE GRABACIÓN
    with open(nombre_archivo, "w", newline='') as archivo:
        archivo.write("Tiempo,Voltaje(V)\n")
        
        try:
            while True:
                if arduino.in_waiting > 0:
                    # Leer dato y obtener hora actual
                    linea = arduino.readline().decode('utf-8').strip()
                    tiempo_actual = time.strftime("%H:%M:%S")
                    
                    # Mostrar en pantalla y guardar
                    print(f"Registro -> Hora: {tiempo_actual} | Voltaje: {linea}V")
                    archivo.write(f"{tiempo_actual},{linea}\n")
                    archivo.flush() 
        
        except KeyboardInterrupt:
            print("\n--- GRABACIÓN DETENIDA ---")

    # 3. PROCESO DE CONSULTA (Se activa al presionar Ctrl+C)
    if os.path.exists(nombre_archivo):
        print("\n¿Deseas consultar el voltaje de una hora específica?")
        hora_buscada = input("Introduce la hora en formato HH:MM:SS (ejemplo 15:00:00) o pulsa Enter para salir: ")
        
        if hora_buscada:
            encontrado = False
            with open(nombre_archivo, mode='r') as archivo_lectura:
                lector = csv.DictReader(archivo_lectura)
                for fila in lector:
                    if fila["Tiempo"] == hora_buscada:
                        print(f"\n>>> RESULTADO: A las {hora_buscada}, el voltaje era de {fila['Voltaje(V)']}V")
                        encontrado = True
                        break
                
                if not encontrado:
                    print(f"\nLo siento, no se encontró ningún dato registrado exactamente a las {hora_buscada}.")

except serial.SerialException:
    print(f"ERROR: No se pudo conectar al {puerto_arduino}. Revisa el cable o el número de puerto.")
finally:
    if 'arduino' in locals() and arduino.is_open:
        arduino.close()
        print("Puerto serie cerrado correctamente.")