# 🤖 Bot de Inversión en Criptomonedas

## 📚 Tabla de Contenidos

- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Cómo iniciar el bot](#-cómo-iniciar-el-bot)
- [Cómo iniciar el dashboard](#-cómo-iniciar-el-dashboard)
- [Funcionalidades](#-funcionalidades)
- [Requisitos](#-requisitos)
- [Notas adicionales](#-notas-adicionales)
- [Instalación](#-instalación)
- [Versión](#-versión)
- [Licencia](#-licencia)
- [Autor](#-autor)

Este proyecto es un bot de inversión automatizado que utiliza análisis técnico para detectar señales de compra y venta en el mercado de criptomonedas. También incluye un dashboard interactivo desarrollado con Streamlit para visualizar datos y señales.

## 📂 Estructura del proyecto

```
BotInversion/
├── main.py               # Punto de entrada principal del bot
├── dashboard.py          # Dashboard web con Streamlit
├── modules/              # Lógica modular del bot
│   ├── adapters/         # Adaptadores para APIs externas (Binance, CoinGecko, Telegram, etc.)
│   ├── strategies/       # Estrategias de trading y señales
│   ├── utils/            # Utilidades y funciones auxiliares
│   ├── styles/           # Archivos de estilos y configuración visual
│   └── ...               # Otros módulos específicos
├── data/                 # Archivos CSV generados automáticamente y symbol_map.csv
├── logs/                 # Registros avanzados del sistema y errores
├── requirements.txt      # Dependencias del entorno virtual
└── README.md             # Este archivo
```

## 🧪 Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/Coloro1985/BotInversion.git
   cd BotInversion

   # Crear y activar entorno virtual
   python -m venv .venv
   source .venv/bin/activate  # En Mac/Linux
   # .venv\Scripts\activate   # En Windows

   # Instalar dependencias
   pip install -r requirements.txt
   ```

2. Configura el archivo `.env` con tus claves y ajustes necesarios.

## 🚀 Cómo iniciar el bot

Primero, asegúrate de activar el entorno virtual:

```bash
source .venv/bin/activate  # MacOS/Linux
# .venv\Scripts\activate   # Windows
```

Luego, puedes ejecutar el bot con:

```bash
python main.py
```

## 📊 Cómo iniciar el dashboard

Para lanzar el dashboard web con Streamlit:

```bash
streamlit run dashboard.py
```

Esto abrirá automáticamente tu navegador web para ver la interfaz interactiva.

---

🧠 Funcionalidades
• Extracción de datos de criptomonedas desde CoinGecko y Binance
• Análisis técnico: RSI, MACD, Bollinger Bands, y detección de patrones como Triángulo Dorado
• Exportación automática de CSVs
• Visualización gráfica y filtros avanzados con Streamlit
• Integración con Telegram para envío de señales y notificaciones
• Ejecución automatizada y sistema de logging avanzado activo

---

🛠️ Requisitos

Instala las dependencias con:

pip install -r requirements.txt

---

📌 Notas adicionales
• El archivo symbol_map.csv dentro de data/ define qué criptomonedas serán analizadas.
• Todos los CSV se guardan automáticamente en data/ ordenados por fecha.
• Los reportes generados se guardan en la carpeta `reports/` en el directorio raíz.
• Los logs avanzados del sistema se almacenan en logs/ para seguimiento y depuración.

Ejemplo de `symbol_map.csv`:

```
nombre,símbolo_binance,símbolo_coingecko
Bitcoin,BTCUSDT,bitcoin
Ethereum,ETHUSDT,ethereum
...
```

```

## 🧾 Versión

Este proyecto sigue el estándar [Semantic Versioning](https://semver.org/).

### Versión actual: `v1.1.1` (2025-07-09)

#### Cambios:
- Se implementó un dashboard modular con componentes organizados en `dashboard_components/`, facilitando el mantenimiento y la escalabilidad del sistema.
- Nuevas funcionalidades de exportación de datos, incluyendo opciones desde la interfaz (`export_all_signals_ui`, `chart_export_ui`) para mejorar la experiencia del usuario.
- Sistema de gestión de favoritos persistente mediante el archivo `favoritas.json` en `data/`.
- Visualizaciones de correlación y gráficos técnicos con `seaborn` y `matplotlib`, agregando análisis visual más avanzado.
- Comparador de múltiples archivos de señales con filtros personalizables (RSI, MACD, volumen, etc.).
- Refactorización del código para separar lógica, mejorar la reutilización y legibilidad.
- Optimización del diseño visual y la usabilidad general del dashboard.

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## 👤 Autor

Desarrollado por Claudio Esteffan ✨
```
