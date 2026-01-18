"""
Script para enviar notificaciones automáticas de recordatorio de titulación.
Puede ejecutarse como tarea programada (cron o Task Scheduler).
"""

import os
import pymysql
import requests
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Token del bot de Telegram desde variables de entorno
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN no configurado. Define el token en un archivo .env o variable de entorno.")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}"

# Configuración de la base de datos
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'seguimiento_egresados_umb'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def conectar_db():
    """Establece conexión con la base de datos"""
    try:
        conexion = pymysql.connect(**DB_CONFIG)
        return conexion
    except pymysql.Error as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return None

def calcular_tiempo_titulacion(generacion):
    """Calcula el tiempo restante para titularse"""
    try:
        # Manejar diferentes formatos de generación
        generacion_str = str(generacion).strip()
        
        # Si contiene guión, tomar el último año (ejemplo: "2018-2023" -> 2023)
        if '-' in generacion_str:
            anio_generacion = int(generacion_str.split('-')[-1])
        else:
            # Si es solo un año (ejemplo: "2023")
            anio_generacion = int(generacion_str)
        
        anio_limite = anio_generacion + 4
        anio_actual = datetime.now().year
        anios_restantes = anio_limite - anio_actual
        
        return {
            'anio_limite': anio_limite,
            'anios_restantes': anios_restantes,
            'vencido': anios_restantes < 0
        }
    except (ValueError, TypeError, IndexError):
        return None

def send_telegram_message(chat_id, text):
    """Envía mensaje por Telegram"""
    try:
        url = f"{TELEGRAM_API_URL}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, json=data, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")
        return False

def obtener_egresados_a_notificar():
    """Obtiene egresados que necesitan notificación"""
    conexion = conectar_db()
    if not conexion:
        return []
    
    try:
        with conexion.cursor() as cursor:
            sql = """
                SELECT matricula, nombre_encargado, apellido_paterno, apellido_materno, 
                       generacion, estatus_titulacion, id_bot
                FROM egresados 
                WHERE id_bot IS NOT NULL 
                  AND id_bot != ''
                  AND estatus_titulacion != 'Titulado'
            """
            cursor.execute(sql)
            egresados = cursor.fetchall()
            
            # Filtrar por criterios de notificación
            resultado = []
            anio_actual = datetime.now().year
            
            for egresado in egresados:
                try:
                    anio_gen = int(egresado['generacion'])
                    anio_limite = anio_gen + 4
                    anios_restantes = anio_limite - anio_actual
                    
                    # Notificar si:
                    # 1. Está en su último año (anios_restantes == 0)
                    # 2. Le queda 1 año (anios_restantes == 1)
                    # 3. Ya venció (anios_restantes < 0)
                    if anios_restantes <= 1:
                        tiempo_info = calcular_tiempo_titulacion(egresado['generacion'])
                        if tiempo_info:
                            egresado['tiempo_info'] = tiempo_info
                            resultado.append(egresado)
                except (ValueError, TypeError):
                    continue
            
            return resultado
    except pymysql.Error as e:
        print(f"Error en la consulta: {e}")
        return []
    finally:
        conexion.close()

def enviar_notificaciones():
    """Envía notificaciones a todos los egresados que lo necesitan"""
    print("="*60)
    print(f"🤖 NOTIFICADOR AUTOMÁTICO DE TITULACIÓN")
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    egresados = obtener_egresados_a_notificar()
    
    if not egresados:
        print("✅ No hay egresados que notificar en este momento.")
        return
    
    print(f"\n📊 Egresados a notificar: {len(egresados)}\n")
    
    enviados = 0
    errores = 0
    
    for egresado in egresados:
        try:
            tiempo_info = egresado['tiempo_info']
            chat_id = egresado['id_bot']
            nombre = egresado['nombre_encargado']
            matricula = egresado['matricula']
            
            # Construir mensaje según el caso
            if tiempo_info['vencido']:
                # Plazo vencido
                mensaje = f"""
🚨 *ATENCIÓN URGENTE - PLAZO VENCIDO*

Hola {nombre},

Tu plazo de titulación *YA VENCIÓ* hace {abs(tiempo_info['anios_restantes'])} año(s).

📅 *Año límite:* {tiempo_info['anio_limite']}
🎓 *Matrícula:* {matricula}

⚠️ *ACCIÓN REQUERIDA:*
Contacta a control escolar URGENTEMENTE para revisar tu situación y conocer las opciones disponibles.

📞 No dejes pasar más tiempo.

🎓 Universidad Manuela Beltrán
"""
                tipo = "VENCIDO"
            elif tiempo_info['anios_restantes'] == 0:
                # Último año
                mensaje = f"""
🚨 *¡ÚLTIMO AÑO PARA TITULARTE!*

Hola {nombre},

Este es tu *ÚLTIMO AÑO* para completar tu proceso de titulación.

📅 *Año límite:* {tiempo_info['anio_limite']}
🎓 *Matrícula:* {matricula}

⏰ *¡ACTÚA AHORA!*
No dejes que se venza tu plazo. Contacta a control escolar para avanzar con tu titulación.

📞 El tiempo se agota.

🎓 Universidad Manuela Beltrán
"""
                tipo = "ÚLTIMO AÑO"
            else:
                # 1 año restante
                mensaje = f"""
⚠️ *RECORDATORIO DE TITULACIÓN*

Hola {nombre},

Te queda *{tiempo_info['anios_restantes']} año* para completar tu proceso de titulación.

📅 *Año límite:* {tiempo_info['anio_limite']}
🎓 *Matrícula:* {matricula}

💡 *Recomendación:*
Comienza o continúa con tu proceso de titulación para evitar que se venza el plazo.

📞 Contacta a control escolar si necesitas orientación.

🎓 Universidad Manuela Beltrán
"""
                tipo = "1 AÑO RESTANTE"
            
            # Enviar mensaje
            if send_telegram_message(chat_id, mensaje):
                print(f"  ✅ {matricula} - {nombre} ({tipo})")
                enviados += 1
            else:
                print(f"  ❌ {matricula} - Error al enviar")
                errores += 1
        
        except Exception as e:
            print(f"  ❌ {egresado.get('matricula', 'N/A')} - Error: {e}")
            errores += 1
    
    print("\n" + "="*60)
    print(f"📊 RESUMEN:")
    print(f"  ✅ Enviados: {enviados}")
    print(f"  ❌ Errores: {errores}")
    print(f"  📋 Total: {len(egresados)}")
    print("="*60 + "\n")

if __name__ == '__main__':
    enviar_notificaciones()