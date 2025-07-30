🤖 Bot de Inversión v2.0.0
Este proyecto es una plataforma de trading automatizado que ejecuta múltiples estrategias de inversión en el mercado de criptomonedas. Incluye un dashboard interactivo para el análisis de señales y un sistema de ejecución configurable.

📚 Tabla de Contenidos
Funcionalidades Clave

Estructura del Proyecto

Instalación

Configuración

Cómo Iniciar

Versión

Autor

✨ Funcionalidades Clave
Gestor de Estrategias: Ejecuta múltiples bots (Momentum, DCA, Grid Trading) definidos en un archivo strategies.yaml.

Arquitectura Modular: Permite añadir nuevos exchanges y estrategias de forma sencilla gracias a su diseño basado en clases base.

Análisis Técnico Avanzado: Calcula indicadores como RSI, MACD, Medias Móviles y detecta patrones de cruce.

Servidor de Webhooks: Se integra con servicios externos como TradingView para ejecutar operaciones basadas en alertas.

Dashboard Interactivo: Visualiza, filtra y explora todas las señales generadas con una interfaz amigable.

Configuración Centralizada: Modifica fácilmente el comportamiento global del bot a través de config.py.

📂 Estructura del Proyecto
BotInversion/
├── src/ # Código fuente de la aplicación
│ ├── bot/ # Lógica principal del bot y gestor de estrategias
│ ├── dashboard/ # Aplicación web con Streamlit
│ └── strategies/ # Implementación de las estrategias de trading
├── config.py # Configuración global del bot
├── main.py # Punto de entrada para ejecutar el bot
├── strategies.yaml # Archivo para definir y configurar las estrategias a ejecutar
├── requirements.txt # Dependencias del proyecto
└── README.md # Este archivo

🧪 Instalación
Clona el repositorio:

git clone https://github.com/Coloro1985/BotInversion.git
cd BotInversion

Crea y activa un entorno virtual:

python -m venv .venv
source .venv/bin/activate # En Mac/Linux

Instala las dependencias:

pip install -r requirements.txt

⚙️ Configuración
Crea un archivo .env en la raíz del proyecto y añade tus claves de API:

BINANCE_API_KEY="TU_API_KEY"
BINANCE_SECRET_KEY="TU_SECRET_KEY"
TELEGRAM_TOKEN="TU_TOKEN_DE_TELEGRAM"
TELEGRAM_CHAT_ID="TU_CHAT_ID"

Define tus estrategias en el archivo strategies.yaml. Puedes activar, desactivar y configurar los parámetros de cada bot.

Ajusta los parámetros globales en config.py.

🚀 Cómo Iniciar
Iniciar el Bot
Ejecuta todas las estrategias activadas en strategies.yaml. El bot se ejecutará una vez al inicio y luego periódicamente.

python main.py

Iniciar el Dashboard de Análisis
Para visualizar los reportes generados por la estrategia de Momentum:

streamlit run src/dashboard/dashboard.py

🧾 Versión
Este proyecto sigue el estándar Semantic Versioning.

Versión actual: v2.0.0 (2025-07-30)
Consulta el archivo CHANGELOG.md para un historial detallado de los cambios.

👤 Autor
Desarrollado por Claudio Esteffan ✨
