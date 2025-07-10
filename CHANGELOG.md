# Changelog

All notable changes to this project will be documented in this file.

## [1.1.1] - 2025-07-09

### Added

- Sección de dashboard completamente refactorizada e integrada modularmente.
- Nuevos componentes en `dashboard_components/`: `filters_ui.py`, `reporting_ui.py`, `charts_ui.py`, `correlation_ui.py`, `technical_chart_ui.py`, `favorites_ui.py`, `signal_summary_ui.py`, `export_all_signals_ui.py`, `report_charts_ui.py`, `saved_reports_ui.py`, `multi_file_comparator.py`, `chart_export_ui.py`.
- Funcionalidad para gestionar y visualizar reportes guardados desde la interfaz.
- Compatibilidad con múltiples archivos y filtros avanzados en el dashboard.
- Soporte visual para favoritos, correlaciones y gráficos técnicos.
- Implementación de gráficos de dispersión y correlación con `seaborn`.

### Changed

- Lógica de exportación CSV y manipulación de reportes movida desde `utils.py` a módulos dedicados en `dashboard_components/`.
- Código del dashboard reorganizado para seguir principios SOLID y separación de responsabilidades.

### Fixed

- Corrección de rutas para guardar los reportes en el directorio `reports/`.
- Solución a errores de variables no definidas y mejoras de robustez en carga de archivos.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-07-08

### Added

- Estructura modular del proyecto reordenada para mayor claridad y mantenibilidad.
- Implementación del sistema de logging con configuración centralizada en `logger.py`.
- Carpeta `strategies/` creada para soportar múltiples estrategias de análisis.
- Reportes de señales exportados en formato CSV en la carpeta `reports/`.
- Función `analyze_coin` ahora permite identificar tendencia usando EMAs.
- Soporte inicial para integración con Telegram bot (aún en progreso).
- Nuevo archivo `config.py` para centralizar configuraciones.

### Fixed

- Problemas de importación circular resueltos al separar responsabilidades.
- Corrección de rutas erróneas en los módulos `utils` y `runner`.
- Manejo de errores más robusto al cargar archivos CSV.

### Removed

- Eliminación del archivo duplicado `bot.py` y carpeta `historicos/`.
