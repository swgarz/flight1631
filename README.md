# Sitio web de Flight 1631

Landing informativa del taller de drones Flight 1631 (Sucre 77, Benito Juárez, CDMX).

- **Producción:** https://flight1631.com/ (Hostinger, despliegue desde este repositorio: hPanel → Avanzado → Git)
- **Previa:** https://swgarz.github.io/flight1631/ (GitHub Pages, rama `main`)

Los dos ambientes se alimentan del mismo repositorio: cada `git push` a `main` actualiza ambos.

## Estructura

```
index.html              La página completa (HTML + CSS + JS en un solo archivo)
404.html                Página de error (Hostinger la usa vía .htaccess; GitHub Pages la toma sola)
.htaccess               Reglas del servidor en Hostinger: https sin www, bloqueo de archivos ocultos, caché
robots.txt, sitemap.xml Para buscadores; apuntan a flight1631.com
favicon.ico/.png, apple-touch-icon.png   Íconos del sitio
img/                    Imágenes optimizadas para web (SÍ se suben)
fotos-originales/       Fotos tal cual llegan del cliente (NO se suben: está en .gitignore)
herramientas/           Scripts de apoyo (no se sirven al público)
```

## Reglas para que funcione igual en los dos ambientes

1. **Rutas relativas siempre**: `img/foto.webp`, nunca `/img/foto.webp`. En GitHub Pages el sitio vive en `/flight1631/`
   y en producción en la raíz; con rutas relativas el mismo archivo sirve en ambos.
2. Las URL absolutas (`canonical`, `og:url`, `og:image`, sitemap, schema.org) apuntan a `https://flight1631.com/`
   a propósito: le dicen a Google cuál es el sitio oficial.
3. El `index.html` es la única fuente de verdad. No se editan archivos en el Administrador de archivos de Hostinger:
   el siguiente despliegue los pisaría.

## Cómo agregar fotos

1. Copia los originales a `fotos-originales/<categoria>/` (`reparacion`, `cursos`, `armado`, `taller`).
2. Ejecuta `python herramientas/optimizar-fotos.py <categoria>` (requiere `pip install pillow`).
   Genera `img/<categoria>-NN.webp` (grande) y `img/<categoria>-NN-800.webp` (chica) e imprime sus anchos reales.
3. En `index.html`, dentro de la galería, duplica una `<figure>` existente y ajusta su `<img>` (los anchos del `srcset` son los que imprime el script):

   ```html
   <img src="img/reparacion-11-800.webp"
        srcset="img/reparacion-11-800.webp 800w, img/reparacion-11.webp 1280w"
        sizes="(max-width: 560px) 100vw, (max-width: 1000px) 50vw, 33vw"
        width="1280" height="960" loading="lazy" alt="Qué se ve en la foto">
   ```

   Cada `<figure>` necesita su `data-cat` (para los filtros) y un `view-transition-name` único.

## Publicar cambios

```
git add -A
git commit -m "Qué cambió"
git push
```
