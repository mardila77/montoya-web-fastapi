# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to a custom 4-section versioning logic.

## [1.0.0.006] - 2026-04-17

### Added
- **Automatización de Copyright**: Implementación dinámica del año de copyright en todo el portal web y correos electrónicos.
- **Personalización del Trato**: Lógica de extracción del primer nombre para un saludo más cercano y profesional en el email de agradecimiento.
- **Robustez Industrial**: Transición a un flujo de registro síncrono en Google Sheets para garantizar la integridad de los leads antes del éxito visual.

### Changed
- Refactorización del servidor para aceptar archivos de forma tolerante (opcional) en el flujo de WhatsApp, eliminando errores 422 por inconsistencia de FormData.
- Limpieza automática de estados de adjuntos al alternar canales en el formulario de contacto para evitar el envío de datos obsoletos.

## [1.0.0.005] - 2026-04-16

### Added
- Registro visual premium en emails mediante adjuntos CID para asegurar la visibilidad del logo en clientes modernos (Gmail/Outlook).
- Prevención de duplicados en el registro de leads.

## [1.0.0.004] - 2026-04-15

### Changed
- Estabilización de rutas de activos estáticos y optimización de carga de imágenes corporativas.

## [1.0.0.003] - 2026-04-15

### Added
- Implementación de motor de audio persistente (`audio_engine.html`) con control de volumen vertical dinámico.
- Reestructuración del formulario de contacto (v7.1) con lógica condicional segmentada por canal (Email vs WhatsApp).
- Integración de sistema de bloqueo/desbloqueo reactivo en el flujo de consulta técnica.

### Changed
- Sincronización site-wide de la "Atmósfera GMPC" en todas las plantillas de sectores.
- Unificación de controles de envío en el formulario de contacto mediante un botón dinámico unificado.
- Mejora de la precisión en la segmentación de prospectos eliminando el campo "Área de Operación" en favor del canal de contacto.

## [1.0.0.001] - 2026-04-14

### Added
- Integración del sistema de automatización Antigravity para versiones y changelog.
- Configuración de Git Hooks (`pre-commit`) para versionado automático.
- Creación de archivo `.version` de control.

### Changed
- Análisis histórico condensado:
    - Finalización del portal de contacto y optimización de UX global.
    - Integración de identidad visual (logos) y diseño responsivo avanzado.
    - Implementación de carrusel interactivo y secciones industriales (Agrícola, Construcción, etc.).
    - Limpieza profunda de estilos CSS y estandarización de navegación.
