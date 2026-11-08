---
name: teco-reels
description: Hacer, analizar o rehacer reels/videos de Instagram para T-ECO Group: motion graphics, fotos reales con Codex, animación dibujada, sincronía con música/voz y exportación con audio.
---

# T-ECO Reels — super skill

Reúne en un solo lugar lo que antes estaba repartido en Bang Motion, HyperFrames (hyperframes, -cli, -registry, media-use), rea-video y los flujos propios (Codex por terminal, fotos reales, animación limitada, beats). El 3D (3dviz-pro-max) queda FUERA a pedido de Joel.

Todo se responde y se escribe en español, claro y sin tecnicismos.

## 1. Dónde está todo

- Scripts del skill: carpeta `herramientas/` junto a este archivo (copia también en la Mac: `teco-videos/herramientas/`): `export.cjs`, `snap.cjs`, `export-http-rango.cjs`, `foto-pantalla-verde.py`, `titulo-y-cierre.py`, `animacion-limitada.py`, `alinear-voz.py`, `sfx-sintetizar.py` y los sonidos `whoosh/pop/ding/buzz/teclas/hit.wav`.
- Carpeta de trabajo en la Mac de Joel: `~/Documents/Claude/Projects/T-ecogrouop/teco-videos/`
  - `proyectos/<reel>/` — un proyecto por reel
  - `imagenes-nivel/base-reales/`, `imagenes-proyectos/base-reales/` — FOTOS REALES de los espacios vacíos de T-ECO (también en los archivos del Proyecto IMG_1677…1684; rotar con `ImageOps.exif_transpose`)
  - `brand-kit/` — logos y tokens; `CLAUDE.md` — contexto de la carpeta
  - `_to_delete/` — aquí van los .tgz de paso (no se borra sin permiso)
- Videos finales en la raíz de `teco-videos/` como `teco-reel-<nombre>.mp4`.

## 2. Reglas de Joel (no negociables)

1. **Solo se entrega la versión CON audio.** Nunca la muda.
2. **Logo original y PLANO** (`teco-logo.png`), nunca redibujado, deformado ni en 3D. Va en el cierre.
3. **Espacios reales:** las personas se ponen SOBRE las fotos reales vacías de T-ECO; no se inventan espacios. Codex > Gemini (Gemini inventó lugares).
4. **Cada reel lleva imágenes nuevas** y animaciones nuevas; no repetir las de reels anteriores.
5. **El programa dura 6 meses.** Áreas del sílabo: IA, Programación, Diseño gráfico, Modelado 3D; al final Scrum + Game Jam (Unity).
6. **No tomar control de su pantalla.** Todo por terminal (`Control your Mac` → osascript). Codex por CLI, nunca la app.
7. Tras entregar, darle el **tag/caption de Instagram** si lo pide (texto + hashtags: #TECOAcademy #TECOGroup #Tecnología #Programación #InteligenciaArtificial #RepúblicaDominicana …).
8. Cuando pide revisar contra un original, ser brutalmente honesto: medir, no opinar.

## 3. Marca

- Colores: navy `#082567`, azul `#2383D0`, cian `#4FC3F0`, verde `#6CC24A`/`#52B84F`, amarillo `#FFD12A`, naranja `#F8A51B` (`#A35C00` texto sobre claro), crema `#F6F3EC`.
- Fuentes (fontsource, woff2 → convertir a ttf con fontTools si se usa PIL): Sora 600/700, Montserrat, JetBrains Mono, Press Start 2P (arcade), Libre Baskerville 700 (subtítulos serif).
- Formato: 1080×1920, 30 fps. Texto importante entre y=168 y y=1330 (zona segura de la interfaz de IG).
- Cierre habitual: cortina crema en 6 escalones → logo con rebote (easeBack) → línea en navy → `t-ecogroup.net` en azul.

## 4. Elegir la ruta

| Pedido | Ruta |
|---|---|
| Motion graphics, tipografía, arcade/plataformero, neón | **A. Página HTML con `render(t)`** (estilo Bang Motion) |
| Editar un reel viejo hecho en HyperFrames (`teco-jovenes`, `teco-genz`…) | **B. HyperFrames** |
| Personas/objetos en los espacios reales, pantallas, laptops | **C. Foto real + Codex + composición** |
| Historia dibujada a mano (estilo TikTok de autor) | **D. Animación limitada** |
| "¿Cómo está hecho este video? ¿Es IA?" | **E. Análisis de referencia** |

Se combinan: p. ej. C para las imágenes + A para títulos y cierre.

## 5. Leyes de calidad (de Bang Motion, condensadas)

1. **Es video, no diapositivas.** Una idea + un objeto principal por escena; nada de títulos+subtítulos+chips apilados. Información nueva = respuesta visual nueva.
2. **Determinista o nada.** Todo es función del tiempo `t`. Prohibido `Date.now()`, `Math.random()` sin semilla, timers. Usar PRNG con semilla y sinusoides para vibraciones.
3. **El estilo nace del tema**, no del proyecto anterior: antes de codificar, escribir un brief corto (3 adjetivos, paleta con origen, fuente, firma de movimiento) y la escaleta `segundo | escena | texto | visual`.
4. **Texto vivo, fondo sumiso:** sentence case, peso 600-700, sin punto final en frases cortas; bajo el texto el fondo es oscuro (≤25 % lum) o claro (≥80 %); nada de texto < 30 px.
5. **Verificar con FOTOGRAMAS.** Hojas de contacto (6–20 segundos clave) y mirarlas como director antes de exportar. Nunca describir un cuadro que no se vio.
6. Dos reels seguidos no comparten paleta, fuente, fondo y firma de movimiento a la vez.

## 6. Ruta A — página `render(t)` + exportación

Contrato de la página (`index.html`, todo inline, assets relativos):
```js
const tl=gsap.timeline({paused:true}); tl.to({}, {duration:D, onUpdate:()=>render(tl.time())});
window.OPENER={W:1080,H:1920,DURATION:D,tl,seek:t=>{tl.seek(t);render(t)},ready:true};
// ?clean=1 → sin autoplay (exportar)   ?debug=1 → barra para recorrer
// sin ?clean: autoplay + audio; si el navegador bloquea el audio, esperar al primer clic
```
- Revisar: `NODE_PATH=$(npm root -g) node herramientas/snap.cjs <dir> <salida> 0.5 2 4 …`
- Exportar: `NODE_PATH=$(npm root -g) node herramientas/export.cjs <dir> /tmp/frX 30` (Playwright, JPG por cuadro). WebGL: Chromium con `--use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist --use-gl=angle` y el canvas con z-index alto.
- Si la página usa módulos ES (three.js…), servir por http (`python3 -m http.server`) y usar `export-http-rango.cjs <url> <out> <desde> <hasta>`; con 2 núcleos, dos rangos en paralelo.
- Unir: `ffmpeg -framerate 30 -i f%05d.jpg -i pista.m4a -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart salida.mp4`.

### Sincronía con la música
- Convertir a wav con ffmpeg (librosa no lee m4a) → `librosa.beat.beat_track` → BPM y beats; RMS por tramos para hallar dónde sube la canción y cortar ahí la pista (`-ss`).
- Rejilla: `B0` (primer beat) y `BP=60/BPM`; `beat(n)=B0+n*BP`. Las escenas cambian en inicio de compás (múltiplos de 4); cada acción cae EN un beat.
- Joel rechazó un reel por "aburrido y fofo, no sigue los beats": en cada beat debe pasar algo (aterrizaje, sacudida de cámara ~12 px que decae en 0.12 s, pulso de zoom 1+0.025·e^(−10·tiempo desde el beat), más fuerte en el compás; destello corto en el compás; textos que entran de golpe con escala 1.8→1 en 0.1 s, no tecleados lento).

## 7. Ruta B — HyperFrames (proyectos viejos)

Desde la carpeta del proyecto: `npx --yes hyperframes@0.8.217 check | snapshot --at 1,5,10 | preview | render -o ../../salida.mp4`. Skills oficiales si hacen falta: `npx skills add heygen-com/hyperframes`.
Contrato: cada elemento con tiempo lleva `class="clip"`, `data-start`, `data-duration`; un timeline pausado por composición registrado en `window.__timelines[id]`; nada de `Date.now()`/aleatorio/`repeat:-1`; no animar `display/visibility`; rutas `assets/...` sin `/` inicial; fuentes por `@font-face`; cada escena en `<template>` con estilos en `#root`. Ejecutar `check` tras cada cambio y corregir todo.

## 8. Codex por terminal (imágenes)

- Codex CLI: `/opt/homebrew/bin/codex`. Se lanza por osascript, en segundo plano, con un `PEDIDO-*.md` en la carpeta:
```applescript
do shell script "/bin/zsh -lc 'cd ~/Documents/Claude/Projects/T-ecogrouop/teco-videos && echo <PEDIDO en base64> | base64 -D > PEDIDO-X.md && nohup codex exec --skip-git-repo-check --sandbox workspace-write -C . \"Lee PEDIDO-X.md y haz exactamente lo que pide, en orden. Usa tu herramienta de generacion y edicion de imagenes pasando como referencia los archivos indicados. Al terminar lista los archivos.\" > codex-x.log 2>&1 < /dev/null & echo lanzado'"
```
- El osascript corta a ~30 s: esperar con `sleep` en la nube y luego un `ls` rápido. ~40–60 s por imagen.
- Pasar a JPG antes de traer: `sips -s format jpeg -s formatOptions 95 x.png --out jpg/x.jpg`. Traer con `device_stage_files`; devolver con `SendUserFile` + `device_commit_files` (< 30 MB; si pesa más, reencodar con `-vf hqdn3d=0:0:3:3 -crf 23`).
- Borrar en la Mac: mover a la Papelera (`mv … ~/.Trash/`) solo si Joel lo pide; si no, a `_to_delete/`.
- **Reglas del pedido:** editar SIEMPRE la foto real indicada ("no cambies el espacio; solo añade …"); para reemplazar una pantalla, pedirla en verde puro `#00FF00` con el marco y las 4 esquinas visibles; personajes consistentes con una **hoja de personaje** (`00-personajes.png`) pasada como referencia en TODAS las escenas; variantes de acción: "EDITA <base>; cambia SOLO <parte>; mismo encuadre, mismo trazo"; sin texto salvo lo pedido; sin logos de marcas.

## 9. Ruta C — foto real + composición (`foto-pantalla-verde.py`, `titulo-y-cierre.py`)

1. Detectar la pantalla verde en HSV (40–85, s>90, v>90) sobre la foto ENTERA, contorno mayor, 4 esquinas (min/max de x+y y x−y), agrandar 1.2 %.
2. Quitar el verde que se cuela en reflejos (`G -= G − max(R,B)`).
3. Encuadre 9:16: alto 1920 y recorte horizontal centrado en la pantalla (o ampliar por arriba con reflejo difuminado).
4. Por cuadro: cámara = matriz afín (acercamiento suave, temblor de mano con sinusoides, fondo algo desenfocado al acercarse); el contenido de la pantalla se proyecta con `A @ homografía` directo al cuadro final (queda nítido); máscara con la misma homografía.
5. Título animado letra por letra con degradado de marca y cierre crema con logo (`titulo-y-cierre.py`).
- Lección: Joel no quiso una Mac inventada; sí la foto real del aula con la Mac añadida por Codex y la cámara acercándose.

## 10. Ruta D — animación limitada dibujada (lecciones del reel "La beca")

- **Dibujo FIJO.** En la referencia ~45 % de los cuadros son idénticos al anterior. Nada de temblor de línea ni zoom constante (eso hace que "el dibujo se mueva").
- **Planos cortos:** ~1 s por plano (87 planos en 82 s en la referencia), cortes secos, sin destellos.
- **Acción con dibujos alternados** (2–4 de la misma escena): vibrar 0.08 s, teclear 0.1 s, rascarse 0.12 s, caminar 0.25 s por paso; cambios de expresión una sola vez en el momento justo.
- **Variantes pegadas solo donde cambian:** alinear con ECC afín, diferencia > 16, regiones > 1500 px, dilatar 21 px, suavizar poco (σ≈3, ×2.5) para no ver dobles pupilas; si cambia > 60 % del cuadro, usar la variante entera.
- **Estilo para Codex:** grises PLANOS (3 tonos + blanco + negro), sin degradados ni brillos ni texturas, entintado suelto, fondos mínimos; un único color de marca (amarillo `#FFD12A`) en un detalle.
- **La voz manda:** subtítulo de UNA palabra a la vez, siempre en el mismo sitio (~47 % de alto), serif blanca con borde negro y sombra, sincronizada con la voz. Las voces en español de la Mac (Paulina, Mónica) suenan robóticas: solo como provisional; pedir a Joel que grabe la final (darle guion y cómo grabar).
- `alinear-voz.py frases f1.wav …` (provisional) o `alinear-voz.py una voz.wav` (grabación: separa frases por silencios ≥0.22 s y reparte palabras por sílabas) → `tiempos.json`. Los planos se anclan a índices de palabra en `animacion-limitada.py`.
- Efectos en cada acción visible con `sfx-sintetizar.py`; música muy baja (~0.1). Cierre en la misma paleta (fondo claro para que se lea el logo).

## 11. Ruta E — analizar un video de referencia

- `rea-video` (`git clone https://github.com/JuneYaooo/rea-video`, `pip install --break-system-packages -e .`; en Python 3.13 instalar `rapidocr>=3` aparte). `rea-video decompose video.mp4 -o out --lang en` → `report.html`, `breakdown.json`.
- Sin modelo de visión su veredicto "IA / 3D / código" suele fallar. Confirmar SIEMPRE mirando fotogramas (`ffmpeg -vf "fps=1/2.5,scale=180:-1,tile=11x3"` y cuadros a resolución completa).
- Medir el ritmo: duración media de plano, % de cuadros idénticos, cortes; comparar el resultado propio con los mismos números.
- Señales de dibujo a mano: personaje idéntico en muchos planos, manos bien resueltas, animación limitada, encuadres de cómic.

## 12. Herramientas disponibles y límites

- Funciona: Codex CLI en la Mac, ffmpeg, Playwright, librosa, OpenCV, PIL, npm/pip.
- No disponible desde la nube: huggingface.co, api.openai.com, generativelanguage.googleapis.com (por eso las imágenes van con Codex en la Mac). Figma Weave requiere enlazar la cuenta de Figma en app.weavy.ai; Canva no mantiene personajes mejor que Codex.
- Si la Mac no responde: puede estar dormida o con la app de Claude cerrada; pedir a Joel que abra ESTE chat en la app de la Mac y escriba ahí.

## 13. Entrega

1. Hoja de contacto revisada → exportar → unir con audio.
2. `SendUserFile` solo del MP4 con audio (+ .tgz del proyecto como adjunto si cambió).
3. Guardar en la Mac: video en `teco-videos/`, proyecto en `proyectos/<nombre>`.
4. Mensaje final corto: qué salió, qué cambió, dónde quedó. Sin recapitular pasos.
