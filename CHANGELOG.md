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

## [1.2.0] - 2025-07-28

### Added

- **Configuración Centralizada:** Se ha creado un archivo `config.py` que permite modificar fácilmente los parámetros clave del bot (límite de criptomonedas, intervalos, etc.) sin alterar el código fuente.
- **Análisis Dinámico de Criptomonedas:** El bot ahora obtiene automáticamente las criptomonedas más relevantes por capitalización de mercado desde la API, en lugar de depender de una lista estática.

### Changed

- **Refactorización del Módulo de Análisis:** El archivo `analyzer.py` fue reestructurado por completo, dividiendo la lógica en funciones más pequeñas y mantenibles para una mayor claridad y escalabilidad.
- **Mejora en la Detección de Señales:** La lógica para identificar el "Cruce Dorado" y "Cruce de la Muerte" ahora es más precisa, detectando el momento exacto del cruce de las medias móviles.

### Fixed

- **Estabilidad del Bot:** Se corrigieron errores críticos (`KeyError`) que causaban la detención del bot si los datos de una moneda llegaban incompletos. El bot ahora continúa su ejecución de forma robusta.
- **Exportación de Reportes:** Se solucionó un error que impedía la correcta exportación de los resultados a archivos CSV.
- **Conexión con APIs:** Se optimizó la frecuencia de las llamadas a las APIs para minimizar errores de "Too Many Requests" y mejorar la fiabilidad.
