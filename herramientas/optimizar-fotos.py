#!/usr/bin/env python3
"""
Optimiza fotos para la web (flight1631.com).

Uso:
    python herramientas/optimizar-fotos.py reparacion

Lee   fotos-originales/reparacion/*.jpg | .jpeg | .png | .webp   (en orden alfabético)
Crea  img/reparacion-01.webp (grande, máx. 1600 px)  e  img/reparacion-01-800.webp  (y así para cada foto)

Qué hace con cada foto:
  - corrige la orientación EXIF (fotos de celular que salen giradas)
  - elimina los metadatos, incluida la ubicación GPS que guarda el celular
  - la reduce a 1600 px (si es más grande; nunca la agranda) y a 800 px de lado mayor, en WebP
  - imprime el ancho real de cada archivo para que lo pongas en el srcset

Requiere Pillow:  pip install pillow
"""
import sys, pathlib
from PIL import Image, ImageOps

if len(sys.argv) < 2:
    print(__doc__); sys.exit(1)

categoria = sys.argv[1]
raiz = pathlib.Path(__file__).resolve().parent.parent
origen = raiz / 'fotos-originales' / categoria
destino = raiz / 'img'
fotos = sorted(p for p in origen.iterdir() if p.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp'))
if not fotos:
    print(f'No hay fotos en {origen}'); sys.exit(1)

destino.mkdir(exist_ok=True)
for i, ruta in enumerate(fotos, 1):
    imagen = ImageOps.exif_transpose(Image.open(ruta)).convert('RGB')
    for lado in (1600, 800):
        copia = imagen.copy()
        copia.thumbnail((lado, lado), Image.LANCZOS)
        salida = destino / (f'{categoria}-{i:02d}.webp' if lado == 1600 else f'{categoria}-{i:02d}-800.webp')
        copia.save(salida, 'WEBP', quality=82, method=6)
        print(f'{ruta.name:40} -> {salida.name}  {copia.width}x{copia.height}  {salida.stat().st_size // 1024} KB')
print(f'\nListo: {len(fotos)} fotos en {destino}')
