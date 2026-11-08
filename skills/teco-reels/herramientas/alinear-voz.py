# Tiempos de cada palabra a partir de la voz.
# Modo A (frases sueltas): python3 alinear.py frases f1.wav f2.wav ... -> une con pausas y reparte palabras por sílabas
# Modo B (una grabación):  python3 alinear.py una voz.wav -> separa las 7 frases por silencios
import sys, json, re, numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly
FRASES = ["Ana recibió una beca.", "Primer día en T-ECO.", "Nunca había escrito una línea de código.", "Se trababa en todo…",
          "hasta que aprendió a pedirle ayuda a la IA.", "Hoy, Ana programa.", "¿Y tú, qué esperas?"]
PAUSAS = [0.75, 0.3, 0.3, 0.35, 0.3, 1.0, 0.0]
SR = 44100
def read(p):
    sr, x = wavfile.read(p); x = x.astype(np.float32)
    if x.ndim > 1: x = x.mean(1)
    x /= (np.abs(x).max() + 1e-9)
    if sr != SR: x = resample_poly(x, SR, sr).astype(np.float32)
    return x
def env(x, hop=441):
    n = len(x) // hop; e = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)); return e
def trim(x):
    e = env(x); thr = max(e.max() * 0.06, 1e-4); idx = np.where(e > thr)[0]
    a, b = idx[0] * 441, (idx[-1] + 1) * 441; return x[max(0, a - 800):b + 1500]
def syl(w):
    w = re.sub(r'[^a-záéíóúüñ]', '', w.lower().replace('t-eco', 'teeco').replace('ia', 'ia'))
    if w in ('ia',): return 2
    return max(1, len(re.findall(r'[aeiouáéíóú]+', w)))
def words_in(phrase, t0, t1):
    ws = phrase.split(); s = np.array([syl(w) for w in ws], float); s /= s.sum()
    out = []; t = t0
    for w, f in zip(ws, s):
        d = (t1 - t0) * f; out.append([w, round(t, 3), round(t + d, 3)]); t += d
    return out
mode = sys.argv[1]
res = []; audio = []
if mode == 'frases':
    t = 0.0
    for k, (p, fr) in enumerate(zip(sys.argv[2:], FRASES)):
        x = trim(read(p)); d = len(x) / SR
        res += words_in(fr, t + 0.03, t + d - 0.05)
        audio.append(x); pause = PAUSAS[k]; audio.append(np.zeros(int(pause * SR), np.float32)); t += d + pause
    voz = np.concatenate(audio)
else:
    voz = read(sys.argv[2]); e = env(voz); thr = max(np.percentile(e, 95) * 0.08, 1e-4)
    on = e > thr
    # segmentos de voz separados por silencios >= 0.22 s
    segs = []; i = 0; n = len(on)
    while i < n:
        if on[i]:
            j = i
            while j < n and (on[j] or (j + 22 < n and on[j:j + 22].any())): j += 1
            segs.append([i * 0.01, j * 0.01]); i = j
        else: i += 1
    segs = [s for s in segs if s[1] - s[0] > 0.15]
    while len(segs) > len(FRASES):     # unir los huecos más cortos
        g = [segs[k + 1][0] - segs[k][1] for k in range(len(segs) - 1)]; k = int(np.argmin(g))
        segs[k] = [segs[k][0], segs[k + 1][1]]; del segs[k + 1]
    if len(segs) < len(FRASES): print('AVISO: solo', len(segs), 'frases detectadas')
    for fr, (a, b) in zip(FRASES, segs): res += words_in(fr, a, b)
wavfile.write('voz.wav', SR, (voz / np.abs(voz).max() * 0.9 * 32767).astype(np.int16))
json.dump({'words': res, 'dur': round(len(voz) / SR, 3)}, open('tiempos.json', 'w'), ensure_ascii=False, indent=0)
print(len(res), 'palabras', round(len(voz) / SR, 2), 's'); print(res[:6], res[-3:])
