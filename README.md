# Turnos de atención — demo

Aplicación de demostración con Angular y Flask para una sucursal bancaria: generación automática de turnos A01, A02…, tablero de llamados, cuatro ventanillas, cola de espera y tiempo estimado de 8 minutos por turno.

## Ejecutar

Requisitos: Python 3.10+, Node.js 20.19+.

1. Instala dependencias del frontend con `npm install`.
2. En una terminal instala Flask: `python -m pip install -r requirements.txt`.
3. Inicia el API: `python -m flask --app api.index run --debug --port 5000`.
4. Inicia Angular: `npm start` y abre `http://localhost:4200`.

La interfaz de demostración guarda su estado en el navegador. El API Flask dispone de rutas equivalentes bajo `/api`; el estado del API vive en memoria y se reinicia al volver a iniciar el proceso. Para desplegar en Vercel con datos compartidos entre varias pantallas se debe conectar una base de datos persistente y configurar `API_URL`.

## Publicación

Configura Vercel con el repositorio Git y define el proyecto como Angular. El despliegue del frontend está listo con `npm run build`. Vercel puede ejecutar Flask como función Python; para operar varias pantallas o instancias hace falta almacenamiento compartido (por ejemplo Postgres). No subas credenciales al repositorio.
