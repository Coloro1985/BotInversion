# Changelog

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-07-28

### Added

- **Configuración Centralizada:** Se creó un archivo `config.py` para gestionar fácilmente los parámetros del bot (límite de criptomonedas, intervalos, etc.) sin modificar el código fuente.
- **Análisis Dinámico de Criptomonedas:** El bot ahora obtiene las criptomonedas más relevantes por capitalización de mercado directamente desde la API, eliminando la dependencia de un archivo `symbol_map.csv` estático.

### Changed

- **Reestructuración del Proyecto:** Se reorganizó todo el código fuente en un directorio `src/`, separando la lógica del bot (`src/bot`), el dashboard (`src/dashboard`) y las estrategias (`src/strategies`) para una mayor claridad y escalabilidad.
- **Refactorización del Código:** Se refactorizaron módulos clave como `runner.py`, `analyzer.py` y `data_fetcher.py` para mejorar la legibilidad, mantenibilidad y separar responsabilidades.
- **Mejora en la Detección de Señales:** La lógica para identificar el "Cruce Dorado" y "Cruce de la Muerte" ahora es más precisa, detectando el cruce exacto de las medias móviles.

### Fixed

- **Robustez y Manejo de Errores:** Se corrigieron errores críticos (`KeyError`, `TypeError`, `AttributeError`) que detenían la ejecución del bot y el dashboard. El sistema ahora es más resiliente a datos incompletos de la API y a interacciones inesperadas.
- **Corrección de Imports:** Se actualizaron todas las rutas de importación para funcionar con la nueva estructura de directorios, solucionando todos los `ModuleNotFoundError`.
- **Estabilidad de Conexión:** Se optimizó la frecuencia de las llamadas a las APIs para minimizar errores de "Too Many Requests".

## [1.1.1] - 2025-07-09

### Added

- Sección del dashboard completamente refactorizada e integrada modularmente.
- Nuevos componentes visuales en `dashboard_components/` para filtros, reportes, gráficos, favoritos, análisis técnico, correlaciones y exportaciones.
- Funcionalidad para gestionar y visualizar reportes guardados desde la interfaz.
- Compatibilidad con múltiples archivos y filtros avanzados en el dashboard.
- Soporte visual para favoritos, correlaciones y gráficos técnicos.
- Implementación de gráficos de dispersión y correlación con `seaborn`.

### Changed

- Lógica de exportación CSV y manipulación de reportes movida desde `utils.py` a módulos dedicados en `dashboard_components/`.
- Código del dashboard reorganizado siguiendo principios SOLID y separación de responsabilidades.

### Fixed

- Corrección de rutas para guardar los reportes en el directorio raíz `reports/`.
- Solución a errores de variables no definidas y mejoras de robustez en la carga de archivos.

## [1.1.0] - 2025-07-08

### Added

- Estructura modular del proyecto reordenada para mayor claridad y mantenibilidad.
- Implementación del sistema de logging con configuración centralizada en `logger.py`.
- Carpeta `strategies/` creada para soportar múltiples estrategias de análisis.
- Reportes de señales exportados en formato CSV en la carpeta `reports/`.
- Función `analyze_coin` ahora permite identificar tendencia usando EMAs.
- Soporte inicial para integración con Telegram bot.
- Nuevo archivo `config.py` para centralizar configuraciones.

### Fixed

- Problemas de importación circular resueltos al separar responsabilidades.
- Corrección de rutas erróneas en los módulos `utils` y `runner`.
- Manejo de errores más robusto al cargar archivos CSV.

### Removed

- Eliminación del archivo duplicado `bot.py` y carpeta `historicos/`.
