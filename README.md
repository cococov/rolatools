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

El comodín `User-agent: *` permite rastrear páginas públicas y excluye las
rutas internas `/cdn-cgi/` de Cloudflare. La política de IA permite búsqueda y
consultas, y solicita excluir el entrenamiento con grupos explícitos, salvo
la excepción autorizada de Google-Extended:

- Búsqueda: `OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`, `Amzn-SearchBot`.
- Consultas de usuarios: `ChatGPT-User`, `Claude-User`, `Perplexity-User`, `Amzn-User`.
- Gemini (consultas y entrenamiento): `Google-Extended`.
- Excluidos del sitio: `GPTBot`, `ClaudeBot`,
  `Applebot-Extended`, `CCBot`, `Bytespider`, `Amazonbot` y el identificador
  antiguo `Claude-Web` (conservado por compatibilidad).

El comodín y los grupos de búsqueda/consultas declaran la misma preferencia:

```text
Content-Signal: ai-train=no, search=yes, ai-input=yes
```

Esto permite indexación y consultas de IA (incluido RAG), y excluye entrenamiento
y ajuste de modelos. Los agentes ya bloqueados declaran los tres valores en
`no` y conservan `Disallow: /`. Las señales se repiten por grupo; no reemplazan
Allow/Disallow ni las protecciones del servidor. Son una extensión de
robots.txt que algunos clientes pueden ignorar.

Google-Extended tiene un grupo independiente con `Allow: /` y
`Content-Signal: ai-train=yes, search=yes, ai-input=yes`. Esta excepción permite
las respuestas de Gemini y acepta también el uso para entrenamiento vinculado
a ese control. No cambia la preferencia de entrenamiento de los demás agentes.

Los grupos permitidos repiten `Disallow: /cdn-cgi/`: los agentes específicos
no heredan las reglas del comodín. El sitemap incluye la portada y la política
de privacidad; los subdominios de herramientas mantienen sus propios archivos.

[Google-Extended](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers#google-extended)
controla tanto entrenamiento como el uso de contenido para fundamentar
respuestas de Gemini y Vertex AI. Se permite expresamente porque excluirlo
también limita ese segundo uso. Es un token de política, no un User-Agent HTTP
independiente; no afecta la inclusión ni el ranking en Google Search.

Robots.txt declara preferencias a los bots que lo respetan. Algunos fetchers
activados por usuarios no lo aplican; los bots desconocidos siguen el comodín.
No se modifican Cloudflare ni límites de peticiones. Robots.txt no garantiza
el bloqueo de scrapers abusivos.

Referencias: [Content Signals](https://contentsignals.org/),
[skill de Content Signals](https://isitagentready.com/.well-known/agent-skills/content-signals/SKILL.md),
[skill de reglas de bots](https://isitagentready.com/.well-known/agent-skills/ai-rules/SKILL.md),
[OpenAI](https://developers.openai.com/api/docs/bots),
[Anthropic](https://privacy.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler),
[Perplexity](https://docs.perplexity.ai/docs/resources/perplexity-crawlers) y
[Amazon](https://developer.amazon.com/amazonbot).

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

Los resultados esperados son `checks.discoverability.robotsTxt.status = "pass"`,
`checks.discoverability.sitemap.status = "pass"`,
`checks.botAccessControl.robotsTxtAiRules.status = "pass"`
y `checks.botAccessControl.contentSignals.status = "pass"`.
El chequeo de reglas de bots también pasa con solo un comodín: verificar además que
GPTBot esté excluido y OAI-SearchBot permitido en el detalle del resultado.
El chequeo remoto evalúa lo publicado, no los archivos locales ni una rama
pendiente de desplegar.
