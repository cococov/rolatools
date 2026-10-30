# RolaTools Index

Sitio estático en **HTML + CSS** que funciona como índice central de herramientas de RolaTools para la comunidad de Ragnarok Online LATAM.

## Qué es este proyecto

Esta web presenta RolaTools y entrega acceso rápido a las herramientas activas del ecosistema desde una sola página.

## Herramientas enlazadas

- https://replay.rolatools.com/
- https://dps.rolatools.com/
- https://tracker.rolatools.com/

## Estructura del repositorio

- `index.html`: página principal con presentación y enlaces.
- `privacy.html`: política de privacidad.
- `styles.css`: estilos del sitio y temas.
- `icon.svg`: ícono del sitio.
- `og-image.svg`: imagen para vista previa en redes.
- `robots.txt`: reglas de rastreo y URL del sitemap.
- `sitemap.xml`: páginas públicas del dominio raíz.

## Desarrollo local

Puedes abrir `index.html` directamente en el navegador.

También puedes levantar un servidor local:

```bash
cd /home/cococov/code/rolatools-index
python3 -m http.server 8080
```

Luego abre `http://localhost:8080`.

## Rastreo y despliegue

Publicar `robots.txt` y `sitemap.xml` en la misma raíz web que `index.html`.
El servidor debe responder `GET /robots.txt` con HTTP 200 y `Content-Type:
text/plain` (UTF-8), sin redirección ni autenticación. `sitemap.xml` debe
responder 200 como XML.

Las reglas permiten rastrear las páginas públicas y excluyen las rutas internas
`/cdn-cgi/` de Cloudflare. El sitemap incluye la portada y la política de
privacidad; los subdominios de herramientas mantienen sus propios sitemaps.

Si Cloudflare administra `robots.txt`, comprobar la respuesta pública después
del despliegue: debe conservar el grupo `User-agent: *`, sus reglas y la URL
del sitemap, además de cualquier regla de bots configurada en el dashboard.
Si sigue sirviendo una versión anterior, purgar únicamente la caché de
`https://rolatools.com/robots.txt` y `https://rolatools.com/sitemap.xml`.

Validación después de publicar:

```bash
curl -i https://rolatools.com/robots.txt
curl -i https://rolatools.com/sitemap.xml
curl --fail-with-body --max-time 60 https://isitagentready.com/api/scan \
  -H 'Content-Type: application/json' \
  --data '{"url":"https://rolatools.com"}'
```

El resultado esperado es `checks.discoverability.robotsTxt.status = "pass"`.
El chequeo remoto evalúa lo publicado, no los archivos locales ni una rama
pendiente de desplegar.
