import telebot
import pymysql
import os
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Token del bot de Telegram desde variables de entorno
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN no configurado. Define el token en un archivo .env o variable de entorno.")

# Configuración de la base de datos
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'seguimiento_egresados_umb'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# Crear instancia del bot
bot = telebot.TeleBot(TOKEN)

def conectar_db():
    """Establece conexión con la base de datos"""
    try:
        conexion = pymysql.connect(**DB_CONFIG)
        return conexion
    except pymysql.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def buscar_egresado_por_telefono(telefono):
    """Busca un egresado por número de teléfono"""
    conexion = conectar_db()
    if not conexion:
        return None
    
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM egresados WHERE telefono = %s"
            cursor.execute(sql, (telefono,))
            resultado = cursor.fetchone()
            return resultado
    except pymysql.Error as e:
        print(f"Error en la consulta: {e}")
        return None
    finally:
        conexion.close()

def actualizar_id_bot(telefono, chat_id):
    """Actualiza el campo id_bot con el chat_id de Telegram"""
    conexion = conectar_db()
    if not conexion:
        return False
    
    try:
        with conexion.cursor() as cursor:
            sql = "UPDATE egresados SET id_bot = %s WHERE telefono = %s"
            cursor.execute(sql, (str(chat_id), telefono))
            conexion.commit()
            return cursor.rowcount > 0
    except pymysql.Error as e:
        print(f"Error al actualizar: {e}")
        return False
    finally:
        conexion.close()

def calcular_tiempo_titulacion(generacion):
    """Calcula el tiempo límite de titulación basado en la generación"""
    try:
        # Extraer año de egreso de la generación (ejemplo: "2016-2021" -> 2021)
        if '-' in generacion:
            año_egreso = int(generacion.split('-')[1])
        else:
            año_egreso = int(generacion)
        
        # El límite de titulación es 4 años después del egreso
        año_limite = año_egreso + 10
        año_actual = datetime.now().year
        
        años_restantes = año_limite - año_actual
        
        if años_restantes > 0:
            estado = "✅ EN PLAZO"
            mensaje_estado = f"Te quedan {años_restantes} año(s) para titularte."
        elif años_restantes == 0:
            estado = "⚠️ ÚLTIMO AÑO"
            mensaje_estado = f"Este es tu último año para titularte."
        else:
            estado = "❌ PLAZO VENCIDO"
            años_vencidos = abs(años_restantes)
            mensaje_estado = f"Plazo vencido hace: {años_vencidos} año(s)\n\n⚠️ ATENCIÓN: Contacta a control escolar URGENTEMENTE."
        
        return {
            'estado': estado,
            'año_limite': año_limite,
            'años_restantes': años_restantes,
            'mensaje_estado': mensaje_estado
        }
    except:
        return None

def obtener_egresado_por_chat_id(chat_id):
    """Obtiene información del egresado por chat_id"""
    conexion = conectar_db()
    if not conexion:
        return None
    
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM egresados WHERE id_bot = %s"
            cursor.execute(sql, (str(chat_id),))
            resultado = cursor.fetchone()
            return resultado
    except pymysql.Error as e:
        print(f"Error: {e}")
        return None
    finally:
        conexion.close()

@bot.message_handler(commands=['start', 'ayuda'])
def enviar_bienvenida(message):
    """Mensaje de bienvenida"""
    texto_bienvenida = """
🎓 *Bienvenido al Bot de Egresados UMB*

Este bot te permite enlazar tu número de teléfono con tu perfil de egresado y recibir recordatorios importantes.

*Comandos disponibles:*
/start - Mostrar este mensaje
/enlazar - Enlazar tu número de teléfono
/info - Ver tu información enlazada
/titulacion - Ver tiempo límite de titulación
/ayuda - Mostrar ayuda

Para comenzar, usa el comando /enlazar
"""
    bot.reply_to(message, texto_bienvenida, parse_mode='Markdown')

@bot.message_handler(commands=['enlazar'])
def solicitar_telefono(message):
    """Solicita el número de teléfono al usuario"""
    texto = """
📱 *Enlace de Egresado*

Por favor, envía tu número de teléfono registrado en la base de datos.

*Formato:* 10 dígitos sin espacios ni guiones
*Ejemplo:* 7121948875

Escribe tu número a continuación:
"""
    msg = bot.reply_to(message, texto, parse_mode='Markdown')
    bot.register_next_step_handler(msg, procesar_telefono)

def procesar_telefono(message):
    """Procesa el número de teléfono enviado"""
    telefono = message.text.strip()
    chat_id = message.chat.id
    
    # Validar formato del teléfono (10 dígitos)
    if not telefono.isdigit() or len(telefono) != 10:
        bot.reply_to(message, "❌ *Error:* El número debe tener exactamente 10 dígitos.\n\nIntenta nuevamente con /enlazar", parse_mode='Markdown')
        return
    
    # Buscar egresado
    egresado = buscar_egresado_por_telefono(telefono)
    
    if not egresado:
        bot.reply_to(message, f"❌ *No encontrado*\n\nNo se encontró ningún egresado con el teléfono: {telefono}\n\nVerifica el número e intenta nuevamente con /enlazar", parse_mode='Markdown')
        return
    
    # Verificar si ya está enlazado
    if egresado['id_bot'] and egresado['id_bot'].strip():
        texto_ya_enlazado = f"""
⚠️ *Ya Enlazado*

Este número ya está enlazado a una cuenta de Telegram.

*Egresado:* {egresado['nombre_encargado']} {egresado['apellido_paterno']} {egresado['apellido_materno']}
*Matrícula:* {egresado['matricula']}

Si necesitas actualizar el enlace, contacta al administrador.
"""
        bot.reply_to(message, texto_ya_enlazado, parse_mode='Markdown')
        return
    
    # Actualizar id_bot en la base de datos
    if actualizar_id_bot(telefono, chat_id):
        # MENSAJE 1: Información del egresado
        texto_exito = f"""
✅ *¡Enlace Exitoso!*

Tu número ha sido enlazado correctamente con tu perfil de egresado.

*Información del Egresado:*
👤 *Nombre:* {egresado['nombre_encargado']} {egresado['apellido_paterno']} {egresado['apellido_materno']}
🎓 *Matrícula:* {egresado['matricula']}
📱 *Teléfono:* {telefono}
📧 *Correo:* {egresado['correo']}
📅 *Generación:* {egresado['generacion']}
🎯 *Estatus Titulación:* {egresado['estatus_titulacion']}
"""
        bot.send_message(chat_id, texto_exito, parse_mode='Markdown')
        
        # MENSAJE 2: Tiempo límite de titulación
        tiempo_titulacion = calcular_tiempo_titulacion(egresado['generacion'])
        
        if tiempo_titulacion:
            if tiempo_titulacion['años_restantes'] >= 0:
                emoji_estado = "✅" if tiempo_titulacion['años_restantes'] > 1 else "⚠️"
            else:
                emoji_estado = "❌"
            
            texto_titulacion = f"""
━━━━━━━━━━━━━━━━━━━━━━━
📋 *TIEMPO LÍMITE DE TITULACIÓN*

{tiempo_titulacion['estado']}

📅 *Año límite:* {tiempo_titulacion['año_limite']}

{tiempo_titulacion['mensaje_estado']}
━━━━━━━━━━━━━━━━━━━━━━━

Ahora recibirás notificaciones y recordatorios importantes.

💡 Usa /info para ver tu información completa
📊 Usa /titulacion para detalles de titulación
"""
            bot.send_message(chat_id, texto_titulacion, parse_mode='Markdown')
        else:
            texto_simple = """
━━━━━━━━━━━━━━━━━━━━━━━

Ahora recibirás notificaciones y recordatorios importantes.

💡 Usa /info para ver tu información completa
📊 Usa /titulacion para detalles de titulación
"""
            bot.send_message(chat_id, texto_simple, parse_mode='Markdown')
    else:
        bot.reply_to(message, "❌ *Error:* No se pudo completar el enlace. Intenta nuevamente más tarde.", parse_mode='Markdown')

@bot.message_handler(commands=['info'])
def mostrar_info(message):
    """Muestra la información del egresado enlazado"""
    chat_id = str(message.chat.id)
    egresado = obtener_egresado_por_chat_id(chat_id)
    
    if not egresado:
        bot.reply_to(message, "❌ *No encontrado*\n\nNo tienes un perfil enlazado.\n\nUsa /enlazar para vincular tu número.", parse_mode='Markdown')
        return
    
    texto_info = f"""
📋 *Tu Información de Egresado*

👤 *Nombre Completo:*
{egresado['nombre_encargado']} {egresado['apellido_paterno']} {egresado['apellido_materno']}

🎓 *Matrícula:* {egresado['matricula']}
📱 *Teléfono:* {egresado['telefono']}
📧 *Correo:* {egresado['correo']}
📅 *Generación:* {egresado['generacion']}
💼 *Estatus Laboral:* {egresado['estatus_laboral']}
🎯 *Estatus Titulación:* {egresado['estatus_titulacion']}
👨‍💼 *Perfil:* {egresado['perfil']}

💡 Usa /titulacion para ver el tiempo límite de titulación
"""
    bot.reply_to(message, texto_info, parse_mode='Markdown')

@bot.message_handler(commands=['titulacion'])
def mostrar_titulacion(message):
    """Muestra información detallada sobre el tiempo límite de titulación"""
    chat_id = str(message.chat.id)
    egresado = obtener_egresado_por_chat_id(chat_id)
    
    if not egresado:
        bot.reply_to(message, "❌ *No encontrado*\n\nNo tienes un perfil enlazado.\n\nUsa /enlazar para vincular tu número.", parse_mode='Markdown')
        return
    
    tiempo_titulacion = calcular_tiempo_titulacion(egresado['generacion'])
    
    if not tiempo_titulacion:
        bot.reply_to(message, "❌ No se pudo calcular el tiempo de titulación.", parse_mode='Markdown')
        return
    
    # Determinar el emoji según el estado
    if tiempo_titulacion['años_restantes'] > 1:
        emoji = "✅"
    elif tiempo_titulacion['años_restantes'] >= 0:
        emoji = "⚠️"
    else:
        emoji = "❌"
    
    texto_titulacion = f"""
━━━━━━━━━━━━━━━━━━━━━━━
📋 *TIEMPO LÍMITE DE TITULACIÓN*

👤 *Egresado:* {egresado['nombre_encargado']} {egresado['apellido_paterno']}
🎓 *Matrícula:* {egresado['matricula']}
📅 *Generación:* {egresado['generacion']}

{tiempo_titulacion['estado']}

📅 *Año límite:* {tiempo_titulacion['año_limite']}

{tiempo_titulacion['mensaje_estado']}
━━━━━━━━━━━━━━━━━━━━━━━

🎯 *Estatus actual:* {egresado['estatus_titulacion']}

💡 Usa /info para ver tu información completa
"""
    bot.reply_to(message, texto_titulacion, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def responder_mensaje_general(message):
    """Responde a mensajes no reconocidos"""
    texto = """
ℹ️ *Comando no reconocido*

Por favor, usa uno de los siguientes comandos:

/start - Inicio
/enlazar - Enlazar tu número
/info - Ver tu información
/titulacion - Ver tiempo límite de titulación
/ayuda - Ayuda

Escribe /ayuda para más información.
"""
    bot.reply_to(message, texto, parse_mode='Markdown')

if __name__ == '__main__':
    print("🤖 Bot iniciado correctamente...")
    print(f"Bot: @egresados_umb_cristoferpina_bot")
    print("Esperando mensajes...")
    
    # Iniciar el bot
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"Error: {e}")
        print("Reiniciando bot...")
        bot.polling(none_stop=True, interval=0, timeout=20)