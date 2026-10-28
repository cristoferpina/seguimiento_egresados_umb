<div align="center">

<sub>CRISTOFER PIÑA · DESARROLLO DE SOFTWARE</sub>

# Seguimiento de egresados UMB

Aplicación web y herramientas de Telegram para el seguimiento académico.

<img alt="Python" src="https://img.shields.io/badge/Python-0F172A?style=for-the-badge" />
<img alt="Flask" src="https://img.shields.io/badge/Flask-1D4ED8?style=for-the-badge" />
<img alt="MySQL" src="https://img.shields.io/badge/MySQL-0F766E?style=for-the-badge" />
<img alt="Telegram" src="https://img.shields.io/badge/Telegram-475569?style=for-the-badge" />

**Universidad Mexiquense del Bicentenario**

[Código fuente](https://github.com/cristoferpina/seguimiento_egresados_umb) &nbsp; / &nbsp; [Incidencias](https://github.com/cristoferpina/seguimiento_egresados_umb/issues) &nbsp; / &nbsp; [Perfil](https://github.com/cristoferpina)

</div>

---

[Características](#seccion-1) · [Estructura del proyecto](#seccion-2) · [Requisitos previos](#seccion-3) · [Instalación](#seccion-4) · [Configuración de base de datos](#seccion-5)

---

Aplicación web con Flask y un Bot de Telegram para gestionar el seguimiento de egresados de la Universidad Mexiquense del Bicentenario. Incluye paneles por rol, registro y actualización de egresados, consulta de catálogos (carreras, UES, municipios, localidades), subida de archivos (fotografías y documentos de modalidad), y notificaciones automáticas por Telegram sobre el tiempo límite de titulación.

<a id="seccion-1"></a>

## Características
- Paneles por rol: Administrador, Control Escolar, Encargado HCT y Egresados.
- Autenticación por rol y sesión.
- Registro, actualización, consulta y eliminación de egresados.
- Subida de archivos: fotografía de egresado y documentos de modalidad.
- Endpoints JSON para catálogos: carreras, UES, municipios, localidades.
- Bot de Telegram para enlazar teléfono → perfil y consultar información.
- Script de notificaciones automáticas (último año, un año restante, plazo vencido).

<a id="seccion-2"></a>

## Estructura del proyecto
- [app.py](app.py): Aplicación Flask (rutas, vistas, CRUD de egresados, endpoints JSON).
- [botfather.py](botfather.py): Bot de Telegram (enlace por teléfono, consultas y cálculos de titulación).
- [notificador_automatico.py](notificador_automatico.py): Envío programado de recordatorios por Telegram.
- [requirements_bot.txt](requirements_bot.txt): Requisitos del bot (añade Flask y requests si hace falta).
- [seguimiento_egresados_umb (3).sql](seguimiento_egresados_umb%20(3).sql): Script SQL de base de datos.
- [templates/](templates): Plantillas HTML (paneles y formularios).
- [static/](static): CSS, JS, imágenes, y carpetas de subida (`static/uploads/egresados`, `static/uploads/modalidades`).

<a id="seccion-3"></a>

## Requisitos previos
- Python 3.10+
- MySQL/MariaDB
- Telegram Bot Token (creado con @BotFather)

<a id="seccion-4"></a>

## Instalación
1. (Opcional) Activar el entorno virtual existente en Windows PowerShell:
   ```powershell
   .\seguimiento_egresados_umb\Scripts\Activate.ps1
   ```
2. Instalar dependencias mínimas:
   ```powershell
   pip install -r requirements_bot.txt
   pip install Flask requests
   ```
   Si necesitas reconstruir completo:
   ```powershell
   pip install Flask PyMySQL python-dotenv pyTelegramBotAPI requests
   ```

<a id="seccion-5"></a>

## Configuración de base de datos
1. Crear la base de datos e importar el script:
   ```powershell
   mysql -u root -p < "seguimiento_egresados_umb (3).sql"
   ```
2. Verificar la conexión en [app.py](app.py):
   - Host: `localhost`
   - Usuario: `root`
   - Password: `''` (vacío por defecto)
   - BD: `seguimiento_egresados_umb`

> Nota: Las credenciales están actualmente hardcodeadas en `app.py`, `botfather.py` y `notificador_automatico.py`. Ajusta estos archivos si tu entorno difiere.

<a id="seccion-6"></a>

## Variables de entorno (.env) — opcional
Puedes crear un archivo `.env` en la raíz para centralizar credenciales:
```
TELEGRAM_BOT_TOKEN=tu_token_bot
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=seguimiento_egresados_umb
```
En el código del bot ya se carga `dotenv`, pero el token está hardcodeado. Reemplázalo o modifica el archivo para leer `TELEGRAM_BOT_TOKEN` desde `.env`.

<a id="seccion-7"></a>

## Ejecución
- Iniciar la aplicación web (Flask):
  ```powershell
  python app.py
  ```
  - Servirá en `http://0.0.0.0:5000` (acceso local: `http://localhost:5000`).

- Iniciar el Bot de Telegram:
  ```powershell
  python botfather.py
  ```
  - Comandos disponibles: `/start`, `/ayuda`, `/enlazar`, `/info`, `/titulacion`.
  - El comando `/enlazar` vincula el teléfono del egresado (10 dígitos) con su `chat_id` de Telegram en la tabla `egresados.id_bot`.

- Ejecutar el notificador automático:
  ```powershell
  python notificador_automatico.py
  ```
  - Envía recordatorios a egresados con `id_bot` enlazado y `estatus_titulacion` distinto de `Titulado`.

<a id="seccion-8"></a>

## Rutas principales (Flask)
- `/` → Inicio (login por rol en [index.html](templates/index.html)).
- `/admin` → Panel Administrador ([dashboard_admin.html](templates/dashboard_admin.html)).
- `/control` → Panel Control Escolar ([dashboard_control_escolar.html](templates/dashboard_control_escolar.html)).
- `/ehct` → Panel Encargado HCT ([dashboard_ehct.html](templates/dashboard_ehct.html)).
- `/egresados` → Panel Egresados ([dashboard_estudiante.html](templates/dashboard_estudiante.html)).

### Endpoints de autenticación
- `POST /login_admin` (tabla `coordinador`)
- `POST /login_control` (tabla `control_escolar`)
- `POST /login_ehct` (tabla `encargado_hct`)
- `POST /login_egresados` (tabla `egresados`)

### CRUD y consultas
- `GET /consulta_egresados` → Render de lista de egresados.
- `POST /registrar_egresado` → Alta con subida de foto y documentos.
- `POST /actualizar_egresado` → Actualización de datos del egresado.
- `DELETE|POST /eliminar_egresado/<id_egresado>` → Baja y eliminación de fotografía.
- `GET /consulta_carrera` → JSON `{id_carrera, nombre_carrera}`.
- `GET /consulta_ues` → JSON `{id_ues, nombre_ues}`.
- `GET /consulta_municipio` → JSON `{id_municipio, nombre_municipio}`.
- `GET /consulta_localidades/<id_municipio>` → JSON `{id_localidad, nombre_localidad}` por municipio.

<a id="seccion-9"></a>

## Subida de archivos
- Fotografías: `static/uploads/egresados/`
- Documentos de modalidad: `static/uploads/modalidades/`
- Se crean automáticamente si no existen.

<a id="seccion-10"></a>

## Seguridad y recomendaciones
- Reemplaza el token del bot hardcodeado en [botfather.py](botfather.py) y [notificador_automatico.py](notificador_automatico.py) por una variable de entorno.
- No uses credenciales vacías en producción. Configura usuario y contraseña de MySQL seguros.
- Considera hashear y verificar contraseñas con `werkzeug.security` en todos los flujos (algunos ya usan `generate_password_hash`).
- Configura `SECRET_KEY` mediante entorno y desactiva `debug=True` en producción.

<a id="seccion-11"></a>

## Despliegue y tareas programadas
- Despliegue Flask: usar `gunicorn`/`waitress` detrás de Nginx/IIS según plataforma.
- Bot de Telegram: ejecutar como servicio o proceso en segundo plano.
- Notificaciones automáticas:
  - Windows: Programar con Task Scheduler (por ejemplo, diario a las 08:00).
  - Linux: `cron` (ejemplo: `0 8 * * * /usr/bin/python /ruta/notificador_automatico.py`).

<a id="seccion-12"></a>

## Licencia
Proyecto interno académico/administrativo. Ajusta la licencia según las políticas de la UMB.

---

<div align="center">
<sub>Desarrollado por <a href="https://github.com/cristoferpina">Cristofer Piña</a> · Universidad Mexiquense del Bicentenario</sub>
</div>
