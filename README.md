# 🤖 Bot de Inversión en Criptomonedas

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
• Los logs avanzados del sistema se almacenan en logs/ para seguimiento y depuración.

```

```
