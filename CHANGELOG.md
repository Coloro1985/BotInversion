# Changelog

All notable changes to this project will be documented in this file.

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
