# teco-reels

Skill de Claude para hacer, analizar y rehacer los reels de Instagram de T-ECO Group. El método completo está en `skills/teco-reels/SKILL.md`, y los scripts y sonidos en `skills/teco-reels/herramientas/`.

## Instalar en otra sesión de Claude Code

```bash
git clone https://github.com/joelosiris11/teco-reels.git
mkdir -p ~/.claude/skills
cp -r teco-reels/skills/teco-reels ~/.claude/skills/
```

Si quieres que el skill quede solo dentro de un proyecto, cópialo en `.claude/skills/` de ese proyecto en lugar de `~/.claude/skills/`.

## Lo que necesita la máquina

- Node.js 22 o superior, más Playwright (`npm i -g playwright && npx playwright install chromium`)
- ffmpeg
- Python 3 con `opencv-python`, `pillow`, `numpy`, `scipy`, `librosa` y `fonttools`
- Opcional:
  - `rea-video`, para analizar videos de referencia: https://github.com/JuneYaooo/rea-video
  - HyperFrames, para editar los reels viejos: `npx skills add heygen-com/hyperframes`
- Para generar imágenes: Codex CLI en la Mac, que se usa desde la terminal

## Cómo usarlo

Pídele a Claude, por ejemplo: «Usa teco-reels para hacer un reel de 15 segundos sobre…».
