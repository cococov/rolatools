# RolaTools Index

Página estática en **HTML + CSS** que funciona como índice central de las herramientas de RolaTools.

## Herramientas enlazadas

- https://replay.rolatools.com/
- https://dps.rolatools.com/
- https://tracker.rolatools.com/

## Objetivo

Esta página presenta qué es **RolaTools** y ofrece acceso rápido a las herramientas activas del ecosistema.

## Estructura

- `index.html`: markup principal, contenido y script de tema.
- `styles.css`: estilos visuales y variables de tema.

## Tema oscuro / claro

La implementación replica el comportamiento usado en `rola_replays`:

- Usa `data-theme="dark|light"` en `<html>`.
- Sincroniza con `localStorage` (`theme`).
- Si no hay preferencia guardada, usa `prefers-color-scheme` del sistema.

## Security headers

Se agregaron configuraciones para aplicar estas cabeceras en hosting estático:

- `Content-Security-Policy`
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`

## Ejecutar localmente

Puedes abrir `index.html` directamente en el navegador.

Si prefieres levantar un servidor local:

```bash
cd /home/cococov/code/rolatools-index
python3 -m http.server 8080
```

Luego abre `http://localhost:8080`.
