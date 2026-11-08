# "La beca" v2: animación limitada como en el original.
# - Cada plano es un dibujo FIJO (cuadros idénticos); solo se alternan dibujos de acción.
# - Sin zoom constante ni temblor de línea; cortes secos; ~1 s por plano.
# - Subtítulo: UNA palabra a la vez, sincronizada con la voz, siempre en el mismo lugar.
# Uso: python3 animar2.py <dir_imagenes> <tiempos.json> <salida_frames> [segundos...]
import sys, json, os, cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

IMG, TJ, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
ONLY = [float(x) for x in sys.argv[4:]]
W, H, FPS = 1080, 1920, 30
T = json.load(open(TJ))           # {"words":[[palabra,inicio,fin],...], "dur": segundos de voz}
words = T['words']
# momento de cada palabra por índice (para anclar planos y acciones a la voz)
wt = [w[1] for w in words]
def at(i, off=0.0): return wt[i] + off

# ---- planos: [inicio, dibujos, modo, parámetros]
#  modo 'hold'  : un dibujo fijo
#  modo 'cycle' : alterna dibujos cada 'paso' segundos (acción repetida: vibrar, caminar, teclear)
#  modo 'cambio': pasa del dibujo A al B en el instante dado (una sola vez)
END_VOICE = T['dur']
SHOTS = [
    (0.0,          ['p01', 'p01b'], 'cycle',  {'paso': 0.083}),            # Ana recibió (celular vibra)
    (at(2) - 0.05, ['p02'],         'hold',   {}),                          # una beca
    (words[3][2] + 0.05, ['p03', 'p03b'], 'cambio', {'t': words[3][2] + 0.4, 'sacudir': True}),   # reacción
    (at(4) - 0.05, ['p04', 'p04b'], 'cycle',  {'paso': 0.25}),              # Primer día (camina)
    (at(6) - 0.05, ['p05', 'p05b'], 'cambio', {'t': at(7)}),                # en T-ECO (abre la laptop)
    (at(8) - 0.05, ['p06'],         'hold',   {}),                          # Nunca había escrito
    (at(11) - 0.05,['p07', 'p07b'], 'cycle',  {'paso': 0.12}),              # una línea de código (se rasca)
    (at(15) - 0.05,['p08'],         'hold',   {'sacudir_en': at(15) + 0.05}),  # Se trababa en todo
    (at(19) - 0.05,['p09', 'p09b'], 'cambio', {'t': at(21)}),               # hasta que aprendió (Kevin señala)
    (at(22) - 0.05,['p10', 'p10b'], 'cycle',  {'paso': 0.1}),               # a pedirle ayuda (teclea)
    (at(25) - 0.05,['p11', 'p11b'], 'cambio', {'t': at(27)}),               # a la IA (la respuesta crece)
    (at(28) - 0.05,['p12'],         'hold',   {}),                          # Hoy
    (at(29) - 0.05,['p13'],         'hold',   {}),                          # Ana programa
    (words[30][2] + 0.05,['p14', 'p14b'], 'cambio', {'t': words[30][2] + 0.35, 'sacudir': True}),  # choque de manos
    (at(31) - 0.05,['p15', 'p15b'], 'cambio', {'t': at(34) + 0.1}),         # ¿Y tú, qué esperas? (guiño)
]
END_T = max(END_VOICE + 0.35, at(34) + 0.9)
END_DUR = 1.8
DUR = END_T + END_DUR

def load(name):
    im = cv2.imread(os.path.join(IMG, name + '.jpg'))
    h, w = im.shape[:2]; sc = H / h
    im = cv2.resize(im, (round(w * sc), H), interpolation=cv2.INTER_AREA)
    x0 = (im.shape[1] - W) // 2
    return im[:, x0:x0 + W].copy()
CACHE = {}
def get(n):
    if n not in CACHE: CACHE[n] = load(n)
    return CACHE[n]

def align_to(base, var):
    """Pega en la base solo lo que cambió en el dibujo de acción (el resto queda idéntico)."""
    g1 = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    g2 = cv2.cvtColor(var, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    warp = np.eye(2, 3, dtype=np.float32)
    try:
        _, warp = cv2.findTransformECC(g1, g2, warp, cv2.MOTION_AFFINE,
                                       (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 150, 1e-6), None, 5)
        var = cv2.warpAffine(var, warp, (W, H), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE)
    except cv2.error:
        pass
    d = cv2.GaussianBlur(cv2.absdiff(base, var).max(axis=2).astype(np.float32), (0, 0), 5)
    m = (d > 16).astype(np.uint8)
    # solo regiones grandes (ignora ruido de recompresión disperso)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    keep = np.zeros_like(m)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 1500: keep[lab == i] = 1
    keep = cv2.dilate(keep, np.ones((21, 21), np.uint8))
    keep = np.clip(cv2.GaussianBlur(keep.astype(np.float32), (0, 0), 3) * 2.5, 0, 1)[..., None]
    share = float(keep.mean())
    if share > 0.6:          # el dibujo de acción cambió casi todo: se usa entero
        return var
    return (base * (1 - keep) + var * keep).astype(np.uint8)

PAIRS = {}
def pair(a, b):
    if (a, b) not in PAIRS: PAIRS[(a, b)] = align_to(get(a), get(b))
    return PAIRS[(a, b)]

FONT = ImageFont.truetype('/tmp/baskerville-700.ttf', 74)
def caption(word):
    bb = FONT.getbbox(word); pad = 36
    m = Image.new('L', (bb[2] - bb[0] + pad * 2, bb[3] - bb[1] + pad * 2))
    ImageDraw.Draw(m).text((pad - bb[0], pad - bb[1]), word, font=FONT, fill=255)
    im = Image.new('RGBA', m.size, (0, 0, 0, 0))
    im.paste((0, 0, 0, 210), (0, 0), m.filter(ImageFilter.GaussianBlur(7)))
    im.paste((0, 0, 0, 255), (0, 0), m.filter(ImageFilter.MaxFilter(7)))
    im.paste((255, 255, 255, 255), (0, 0), m)
    return im
CAPS = {}

logo = Image.open(os.path.join(os.path.dirname(__file__), 'teco-logo.png')).convert('RGBA')
F_END = ImageFont.truetype('/tmp/baskerville-700.ttf', 66)
F_URL = ImageFont.truetype('/tmp/sora-600.ttf', 44)
def end_frame(lt):
    im = Image.new('RGB', (W, H), (232, 232, 230))
    L = logo.resize((480, 480), Image.LANCZOS); im.paste(L, ((W - 480) // 2, 560), L)
    d = ImageDraw.Draw(im)
    for txt, y, f, col, ts in [('Becas T-ECO Academy', 1080, F_END, (20, 20, 22), 0.2), ('t-ecogroup.net', 1180, F_URL, (35, 131, 208), 0.45)]:
        if lt >= ts:
            tw = d.textlength(txt, font=f); d.text(((W - tw) / 2, y), txt, font=f, fill=col)
    return np.array(im)[..., ::-1]

def shot_at(t):
    cur = None
    for s in SHOTS:
        if s[0] <= t: cur = s
    return cur

def frame(i):
    t = i / FPS
    if t >= END_T:
        return end_frame(t - END_T)
    s0, imgs, mode, p = shot_at(t)
    lt = t - s0
    if mode == 'hold':
        img = get(imgs[0])
    elif mode == 'cycle':
        k = int(lt / p['paso']) % 2
        img = get(imgs[0]) if k == 0 else pair(imgs[0], imgs[1])
    else:
        img = get(imgs[0]) if t < p['t'] else pair(imgs[0], imgs[1])
    # sacudida corta solo en los impactos
    sh = None
    if mode == 'cambio' and p.get('sacudir'): sh = p['t']
    if p.get('sacudir_en'): sh = p['sacudir_en']
    if sh is not None and 0 <= t - sh < 0.2:
        d = t - sh; a = 12 * (1 - d / 0.2)
        M = np.float32([[1.03, 0, -16 + a * np.sin(d * 120)], [0, 1.03, -29 + a * np.cos(d * 95)]])
        img = cv2.warpAffine(img, M, (W, H), borderMode=cv2.BORDER_REPLICATE)
    out = Image.fromarray(img[..., ::-1]).convert('RGBA')
    cw = None
    for w, a, b in words:
        if a - 0.02 <= t < b: cw = w
    if cw:
        if cw not in CAPS: CAPS[cw] = caption(cw)
        c = CAPS[cw]; out.alpha_composite(c, ((W - c.width) // 2, int(H * 0.47) - c.height // 2))
    return np.array(out.convert('RGB'))[..., ::-1]

os.makedirs(OUT, exist_ok=True)
idx = [round(x * FPS) for x in ONLY] if ONLY else range(int(round(DUR * FPS)))
for i in idx:
    cv2.imwrite(f'{OUT}/f{i:05d}.jpg', frame(i), [cv2.IMWRITE_JPEG_QUALITY, 93])
json.dump({'dur': DUR, 'end_t': END_T, 'shots': [s[0] for s in SHOTS]}, open(os.path.join(OUT, 'info.json'), 'w'))
print('ok', round(DUR, 2))
