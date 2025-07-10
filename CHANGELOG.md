# Changelog

All notable changes to this project will be documented in this file.

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
