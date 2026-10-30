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
- `scripts/update-sitemap.py`: genera el sitemap desde los enlaces canónicos.
- `.github/workflows/sitemap.yml`: comprueba que el sitemap esté actualizado.

## Desarrollo local

Puedes abrir `index.html` directamente en el navegador.

También puedes levantar un servidor local:

```bash
cd /home/cococov/code/rolatools-index
python3 -m http.server 8080
```

Luego abre `http://localhost:8080`.

## Mantener el sitemap actualizado

Al publicar, retirar o cambiar la URL de una página HTML, regenerar el sitemap
antes de desplegar y guardar ambos cambios en el mismo commit:

```bash
python3 scripts/update-sitemap.py
python3 scripts/update-sitemap.py --check
```

El generador lee los enlaces `<link rel="canonical">` de las páginas HTML,
excluye páginas con `<meta name="robots" content="noindex">` y solo acepta URLs
de `https://rolatools.com` que apunten a archivos existentes. No incluye los
subdominios ni inventa fechas de modificación. Una página nueva debe declarar
su URL canónica o marcarse como `noindex`. Esto controla la indexación, no el
acceso: los archivos privados no deben publicarse en la raíz web.

CI ejecuta `--check` en cada push y PR. Falla si el sitemap contiene páginas
retiradas, omite páginas nuevas, usa canónicas inválidas o deja de estar
referenciado desde `robots.txt`.

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

Los resultados esperados son `checks.discoverability.robotsTxt.status = "pass"`
y `checks.discoverability.sitemap.status = "pass"`.
El chequeo remoto evalúa lo publicado, no los archivos locales ni una rama
pendiente de desplegar.
