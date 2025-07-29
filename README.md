# 🤖 Bot de Inversión en Criptomonedas v1.2.0

Este proyecto es un bot de inversión automatizado que utiliza análisis técnico para detectar señales de trading en el mercado de criptomonedas. Incluye un dashboard interactivo desarrollado con Streamlit para visualizar y analizar los datos.

## 📚 Tabla de Contenidos

- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Cómo Iniciar](#-cómo-iniciar)
- [Funcionalidades](#-funcionalidades)
- [Versión](#-versión)
- [Licencia](#-licencia)
- [Autor](#-autor)

## 📂 Estructura del Proyecto

El proyecto sigue una estructura limpia y escalable, separando el código fuente de los archivos generados.

BotInversion/
├── src/ # Directorio principal del código fuente
│ ├── bot/ # Lógica principal del bot de análisis
│ ├── dashboard/ # Código de la aplicación web con Streamlit
│ └── strategies/ # Estrategias de trading
├── config.py # Archivo central de configuración
├── main.py # Punto de entrada para ejecutar el bot
├── requirements.txt # Dependencias del proyecto
├── logs/ # Archivos de log generados por el bot
├── reports/ # Reportes CSV con las señales generadas
└── README.md # Este archivo

## 🧪 Instalación

1.  Clona el repositorio:
    ```bash
    git clone [https://github.com/Coloro1985/BotInversion.git](https://github.com/Coloro1985/BotInversion.git)
    cd BotInversion
    ```
2.  Crea y activa un entorno virtual:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # En Mac/Linux
    # .venv\Scripts\activate   # En Windows
    ```
3.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuración

1.  Crea un archivo `.env` en la raíz del proyecto.
2.  Añade tus claves de API de Binance en el archivo `.env`:
    ```env
    BINANCE_API_KEY="TU_API_KEY"
    BINANCE_SECRET_KEY="TU_SECRET_KEY"
    ```
3.  Ajusta los parámetros del bot (como el número de monedas a analizar o el intervalo de tiempo) directamente en el archivo `config.py`.

## 🚀 Cómo Iniciar

### Iniciar el Bot de Análisis

Asegúrate de tener el entorno virtual activado. Para ejecutar el bot y generar los reportes CSV:

````bash
python main.py

¡Entendido! Aquí tienes ambos textos formateados en Markdown para que los puedas copiar y pegar directamente en tus archivos.

Para tu archivo README.md
Markdown

# 🤖 Bot de Inversión en Criptomonedas v1.2.0

Este proyecto es un bot de inversión automatizado que utiliza análisis técnico para detectar señales de trading en el mercado de criptomonedas. Incluye un dashboard interactivo desarrollado con Streamlit para visualizar y analizar los datos.

## 📚 Tabla de Contenidos
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Cómo Iniciar](#-cómo-iniciar)
- [Funcionalidades](#-funcionalidades)
- [Versión](#-versión)
- [Licencia](#-licencia)
- [Autor](#-autor)

## 📂 Estructura del Proyecto
El proyecto sigue una estructura limpia y escalable, separando el código fuente de los archivos generados.

BotInversion/
├── src/                      # Directorio principal del código fuente
│   ├── bot/                  # Lógica principal del bot de análisis
│   ├── dashboard/            # Código de la aplicación web con Streamlit
│   └── strategies/           # Estrategias de trading
├── config.py                 # Archivo central de configuración
├── main.py                   # Punto de entrada para ejecutar el bot
├── requirements.txt          # Dependencias del proyecto
├── logs/                     # Archivos de log generados por el bot
├── reports/                  # Reportes CSV con las señales generadas
└── README.md                 # Este archivo


## 🧪 Instalación
1.  Clona el repositorio:
    ```bash
    git clone [https://github.com/Coloro1985/BotInversion.git](https://github.com/Coloro1985/BotInversion.git)
    cd BotInversion
    ```
2.  Crea y activa un entorno virtual:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # En Mac/Linux
    # .venv\Scripts\activate   # En Windows
    ```
3.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuración
1.  Crea un archivo `.env` en la raíz del proyecto.
2.  Añade tus claves de API de Binance en el archivo `.env`:
    ```env
    BINANCE_API_KEY="TU_API_KEY"
    BINANCE_SECRET_KEY="TU_SECRET_KEY"
    ```
3.  Ajusta los parámetros del bot (como el número de monedas a analizar o el intervalo de tiempo) directamente en el archivo `config.py`.

## 🚀 Cómo Iniciar

### Iniciar el Bot de Análisis
Asegúrate de tener el entorno virtual activado. Para ejecutar el bot y generar los reportes CSV:
```bash
python main.py
Iniciar el Dashboard
Para lanzar la interfaz web con Streamlit:

Bash

streamlit run src/dashboard/dashboard.py
Esto abrirá una nueva pestaña en tu navegador con el dashboard interactivo.

✨ Funcionalidades
Análisis Dinámico: Obtiene y analiza las principales criptomonedas por capitalización de mercado en tiempo real.

Análisis Técnico Avanzado: Calcula indicadores como RSI, MACD, Medias Móviles y detecta cruces dorados/de la muerte.

Dashboard Interactivo: Visualiza, filtra y explora todas las señales generadas con una interfaz amigable.

Configuración Centralizada: Modifica fácilmente el comportamiento del bot a través del archivo config.py.

Exportación de Reportes: Genera y guarda automáticamente los resultados en formato CSV.

Notificaciones por Telegram: Envía alertas de señales importantes directamente a tu cuenta de Telegram (configurable).

🧾 Versión
Este proyecto sigue el estándar Semantic Versioning.

Versión actual: v1.2.0 (2025-07-28)
Consulta el archivo CHANGELOG.md para un historial detallado de los cambios.

📝 Licencia
Este proyecto está bajo la Licencia MIT.

👤 Autor
Desarrollado por Claudio Esteffan ✨
````
