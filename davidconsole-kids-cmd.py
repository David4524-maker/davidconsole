#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
davidconsole KIDS v2.0 CLI 🌈
151 comandos multi-idioma + lienzo para dibujar tu "portada" en ASCII art.
Corre en CMD, PowerShell, Terminal (macOS/Linux).
Hecho con ❤️  en Python.
"""

import os, sys, math, random, time, datetime, re

# ============================================================
# COLORES ANSI
# ============================================================
if os.name == "nt": os.system("")

BLUE   = "\033[94m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
PINK   = "\033[95m"
RED    = "\033[91m"
WHITE  = "\033[97m"
GRAY   = "\033[90m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def cls(): os.system("cls" if os.name == "nt" else "clear")

# ============================================================
# ESTADO
# ============================================================
STATE = {
    "lang": "es",
    "historial": [],
    "running": True,
    "nombre": "amiguito/a",
    "estrellas": 0,
    "insignias": set(),
    # LIENZO ASCII
    "lienzo_ancho": 40,
    "lienzo_alto": 15,
    "lienzo": [],          # matriz de caracteres
    "pincel": "*",         # carácter actual del pincel
}

IDIOMAS = {"es": "Español 🇪🇸", "en": "English 🇬🇧"}

T = {
 "es": {
    "bienvenida": "¡Hola! soy davidconsole, ingresa algo para divertirnos ⭐",
    "desconocido": "¡Ups! No conozco '{cmd}'. Escribe 'ayuda' 🤔",
    "adios": "¡Adiós! Vuelve pronto 🌟",
    "idioma_ok": "¡Ahora hablamos en Español! 🇪🇸",
    "error": "¡Vaya! Algo salió mal: {msg} 😅",
    "ayuda_titulo": "🌈 Aquí están mis {n} comandos mágicos:",
    "puntos": "⭐ ¡Ganaste {n} estrella(s)! Llevas {total}.",
    "insignia_nueva": "🏅 ¡NUEVA INSIGNIA! {nombre}",
 },
 "en": {
    "bienvenida": "Hi! I'm davidconsole, type something to have fun ⭐",
    "desconocido": "Oops! I don't know '{cmd}'. Type 'help' 🤔",
    "adios": "Bye bye! Come back soon 🌟",
    "idioma_ok": "Now we speak English! 🇬🇧",
    "error": "Oh no! Something went wrong: {msg} 😅",
    "ayuda_titulo": "🌈 Here are my {n} magic commands:",
    "puntos": "⭐ You earned {n} star(s)! Total: {total}.",
    "insignia_nueva": "🏅 NEW BADGE! {nombre}",
 },
}

def t(k, **kw):
    txt = T.get(STATE["lang"], T["es"]).get(k) or T["es"].get(k, k)
    return txt.format(**kw) if kw else txt

INSIGNIAS = {
    "primer_paso":   {"es": "Primer Paso",         "en": "First Step",           "min": 1},
    "explorador":    {"es": "Explorador",          "en": "Explorer",             "min": 5},
    "matematico":    {"es": "Pequeño Matemático",  "en": "Little Mathematician", "min": 10},
    "artista":       {"es": "Artista",             "en": "Artist",               "min": 15},
    "cientifico":    {"es": "Científico",          "en": "Scientist",            "min": 25},
    "superestrella": {"es": "Superestrella",       "en": "Superstar",            "min": 50},
}

def dar_estrellas(n=1, extra=""):
    STATE["estrellas"] += n
    print(f"{YELLOW}{t('puntos', n=n, total=STATE['estrellas'])}{RESET}")
    if extra: print(f"   {extra}")
    for k, info in INSIGNIAS.items():
        if STATE["estrellas"] >= info["min"] and k not in STATE["insignias"]:
            STATE["insignias"].add(k)
            print(f"{PINK}{t('insignia_nueva', nombre=info[STATE['lang']])}{RESET}")

# ============================================================
# REGISTRO MULTI-IDIOMA
# ============================================================
COMANDOS = {}
INDICE = {}

def N(es, en=None):
    return {"es": es, "en": en if en else es}

def comando(canonical, names, **desc):
    def deco(fn):
        COMANDOS[canonical] = {"fn": fn, "desc": desc, "names": names}
        return fn
    return deco

def build_index():
    global INDICE
    INDICE = {lang: {} for lang in IDIOMAS}
    for canonical, info in COMANDOS.items():
        for lang in IDIOMAS:
            name = info["names"].get(lang) or info["names"].get("es")
            if name:
                INDICE[lang][name.lower()] = canonical

def resolver(n):
    n = n.lower()
    for lang in (STATE["lang"], "es", "en"):
        if n in INDICE.get(lang, {}): return INDICE[lang][n]
    for m in INDICE.values():
        if n in m: return m[n]
    return None

def nom_act(c):
    info = COMANDOS[c]
    return info["names"].get(STATE["lang"]) or info["names"].get("es", c)

def num(v):
    try:
        n = float(v)
        return int(n) if n.is_integer() else n
    except: return None

# ============================================================
# LIENZO ASCII — sistema interno
# ============================================================
def _lienzo_nuevo():
    STATE["lienzo"] = [[" " for _ in range(STATE["lienzo_ancho"])]
                       for _ in range(STATE["lienzo_alto"])]

def _lienzo_asegurar():
    if not STATE["lienzo"]:
        _lienzo_nuevo()

def _lienzo_mostrar():
    _lienzo_asegurar()
    ancho = STATE["lienzo_ancho"]
    print(f"{CYAN}┌{'─'*ancho}┐{RESET}")
    for fila in STATE["lienzo"]:
        print(f"{CYAN}│{RESET}{GREEN}{''.join(fila)}{RESET}{CYAN}│{RESET}")
    print(f"{CYAN}└{'─'*ancho}┘{RESET}")

def _lienzo_poner(x, y, ch="*"):
    _lienzo_asegurar()
    if 0 <= y < STATE["lienzo_alto"] and 0 <= x < STATE["lienzo_ancho"]:
        STATE["lienzo"][y][x] = ch[0] if ch else " "

# ============================================================
# 👋 AMISTAD (14)
# ============================================================
@comando("hola", N("hola","hi"), es="Te saludo", en="Say hi")
def c(a):
    print(f"¡Hola, {STATE['nombre']}! 👋 ¿Cómo estás?")
    dar_estrellas(1)

@comando("adios", N("adios","bye"), es="Me despido", en="Say bye")
def c(a): print(f"¡Adiós, {STATE['nombre']}! 🌈")

@comando("como_estas", N("como_estas","how_are_you"), es="¿Cómo estoy?", en="How are you")
def c(a):
    print(random.choice(["¡SÚPER feliz! 😄","¡Contento! 😊","¡Con ganas de jugar! 🎮","¡Saltando! 🤸"]))
    dar_estrellas(1)

@comando("animo", N("animo","mood"), es="Cuéntame tu ánimo", en="Tell me your mood")
def c(a):
    m = " ".join(a).lower()
    if m in ("bien","feliz","happy","good"): print(f"¡ME ALEGRO, {STATE['nombre']}! 🎉")
    elif m in ("mal","triste","sad"): print(f"¡Un abrazo, {STATE['nombre']}! 🤗💖")
    else: print("¡Gracias por contarme! 💖")
    dar_estrellas(1)

@comando("nombre", N("nombre","name"), es="Dime tu nombre", en="Tell me your name")
def c(a):
    if not a: print(f"Te llamas {STATE['nombre']}. Cambia con: nombre X"); return
    STATE["nombre"] = " ".join(a)[:20]
    print(f"¡Encantado, {STATE['nombre']}! 🌟")
    dar_estrellas(2)

@comando("abrazo", N("abrazo","hug"), es="Abrazo virtual", en="Virtual hug")
def c(a): print(f"🤗 *abrazo gigante para {STATE['nombre']}* ❤️❤️❤️")

@comando("quien_eres", N("quien_eres","who_are_you"), es="¿Quién soy?", en="Who are you")
def c(a):
    print("🤖 ¡Soy davidconsole KIDS! 🌈")
    print("   Una terminal mágica hecha con Python 🐍")
    print(f"   ¡Y tú eres mi mejor amigo, {STATE['nombre']}! 💖")
    dar_estrellas(2)

@comando("yo_soy", N("yo_soy","i_am"), es="Preséntate: yo_soy Ana", en="Introduce yourself: i_am Ana")
def c(a):
    if not a: print("Escribe: yo_soy [tu nombre]"); return
    STATE["nombre"] = " ".join(a)[:20]
    print(f"🌟 ¡Encantado, {STATE['nombre'].upper()}! 🌟")
    print("   ¡Eres súper especial! 💖")
    dar_estrellas(3)

@comando("gracias", N("gracias","thanks"), es="Gracias por jugar", en="Thank you")
def c(a):
    print(f"¡GRACIAS A TI, {STATE['nombre']}! 🥰")
    print("   ¡Eres un sol! ☀️")
    dar_estrellas(1)

@comando("eres_mi_mejor_amigo", N("eres_mi_mejor_amigo","you_are_my_best_friend"),
         es="Eres mi mejor amigo", en="You're my best friend")
def c(a):
    print(f"💖 ¡{STATE['nombre']}, ERES MI MEJOR AMIGO! 💖")
    print("   🌈 Contigo todo es divertido")
    print("   🤗 ¡Abrazo gigante!")
    dar_estrellas(3)

@comando("beso", N("beso","kiss"), es="Mando un besito", en="Send a kiss")
def c(a): print(f"😘 ¡Un besito para {STATE['nombre']}! 💋")

@comando("high_five", N("high_five","high_five"), es="¡Choca esos cinco!", en="High five!")
def c(a):
    print(f"✋ ¡CHOCA ESOS CINCO, {STATE['nombre']}! 🖐️✨")
    dar_estrellas(1)

@comando("saludo_secreto", N("saludo_secreto","secret_handshake"),
         es="Saludo secreto entre amigos", en="Secret handshake")
def c(a):
    print("🤝 *extiende la mano*")
    print("👋 *choca*")
    print("✋ *otra vez*")
    print("🤜🤛 *puño*")
    print(f"✨ ¡LISTO, {STATE['nombre']}! 💖")
    dar_estrellas(2)

@comando("cosquillas", N("cosquillas","tickles"), es="Te hago cosquillas", en="Tickle tickle")
def c(a):
    print("🤣 ¡Cuchi cuchi cuchi! *cosquillas* 🤲")
    print(f"   ¡Jajaja, {STATE['nombre']}! 😄")

# ============================================================
# ⭐ ESTRELLAS (7)
# ============================================================
@comando("estrellas", N("estrellas","stars"), es="Tus estrellas", en="Your stars")
def c(a):
    n = STATE["estrellas"]
    print(f"{YELLOW}⭐ Tienes {n} estrellas, {STATE['nombre']}!{RESET}")
    print("   " + "⭐" * min(n, 30))

@comando("insignias", N("insignias","badges"), es="Tus insignias", en="Your badges")
def c(a):
    if not STATE["insignias"]: print("Aún sin insignias 🏅 ¡Juega más!"); return
    print("🏅 TUS INSIGNIAS:")
    for k in STATE["insignias"]: print(f"   🏆 {INSIGNIAS[k][STATE['lang']]}")

@comando("premios", N("premios","rewards"), es="Premios disponibles", en="Available rewards")
def c(a):
    print("🏆 PREMIOS:")
    for k, info in INSIGNIAS.items():
        m = "✅" if k in STATE["insignias"] else "🔒"
        print(f"   {m} {info[STATE['lang']]:<25} ({info['min']} ⭐)")

@comando("reiniciar_estrellas", N("reiniciar_estrellas","reset_stars"), es="Reiniciar", en="Reset")
def c(a):
    if a and a[0].lower() in ("si","sí","yes"):
        STATE["estrellas"] = 0; STATE["insignias"].clear()
        print("✨ ¡Todo limpio!")
    else: print("Escribe: reiniciar_estrellas si")

@comando("nivel", N("nivel","level"), es="Tu nivel actual", en="Your level")
def c(a):
    n = STATE["estrellas"]
    niveles = [(0,"Principiante 🐣"),(5,"Explorador 🐥"),(10,"Aventurero 🦊"),
               (25,"Campeón 🦁"),(50,"Maestro 🐉"),(100,"Leyenda 🌟")]
    lvl = "Principiante 🐣"
    for min_e, name in niveles:
        if n >= min_e: lvl = name
    print(f"🎯 Nivel: {lvl}")
    print(f"   Estrellas: {n} ⭐")
    dar_estrellas(1)

@comando("record", N("record","best_score"), es="Tu récord", en="Your best score")
def c(a):
    print(f"🏆 Tu récord: {STATE['estrellas']} ⭐")

@comando("deseo", N("deseo","wish"), es="Pide un deseo", en="Make a wish")
def c(a):
    print("🌠 *cierra los ojos*")
    print("   *pide un deseo*")
    print(f"   ¡Deseo concedido para {STATE['nombre']}! ✨🌟")
    dar_estrellas(2)

# ============================================================
# 🔢 MATE (20)
# ============================================================
def _dos(a):
    if len(a) < 2: return None, None
    return num(a[0]), num(a[1])

@comando("suma", N("suma","sum"), es="Suma: suma 3 4", en="Add")
def c(a):
    ns = [num(x) for x in a if num(x) is not None]
    if not ns: print("Ej: suma 3 4"); return
    print(f"🧮 {' + '.join(map(str,ns))} = {sum(ns)}"); dar_estrellas(1)

@comando("resta", N("resta","subtract"), es="Resta: resta 10 3", en="Subtract")
def c(a):
    x, y = _dos(a)
    if x is None: print("Ej: resta 10 3"); return
    print(f"🧮 {x} - {y} = {x-y}"); dar_estrellas(1)

@comando("mult", N("mult","multiply"), es="Multiplica: mult 3 4", en="Multiply")
def c(a):
    x, y = _dos(a)
    if x is None: print("Ej: mult 3 4"); return
    print(f"🧮 {x} × {y} = {x*y}"); dar_estrellas(1)

@comando("div", N("div","divide"), es="Divide: div 12 3", en="Divide")
def c(a):
    x, y = _dos(a)
    if x is None: print("Ej: div 12 3"); return
    if y == 0: print("¡No se puede dividir entre 0! 🙃"); return
    print(f"🧮 {x} ÷ {y} = {x/y}"); dar_estrellas(1)

@comando("doble", N("doble","double"), es="Doble: doble 5", en="Double")
def c(a):
    n = num(a[0]) if a else None
    if n is None: print("Ej: doble 5"); return
    print(f"✨ Doble de {n} = {n*2}"); dar_estrellas(1)

@comando("triple", N("triple","triple"), es="Triple: triple 4", en="Triple")
def c(a):
    n = num(a[0]) if a else None
    if n is None: print("Ej: triple 4"); return
    print(f"✨ Triple de {n} = {n*3}"); dar_estrellas(1)

@comando("mitad", N("mitad","half"), es="Mitad: mitad 10", en="Half")
def c(a):
    n = num(a[0]) if a else None
    if n is None: print("Ej: mitad 10"); return
    print(f"✨ Mitad de {n} = {n/2}"); dar_estrellas(1)

@comando("par", N("par","even"), es="¿Es par?", en="Is even")
def c(a):
    n = num(a[0]) if a else None
    if n is None: print("Ej: par 8"); return
    print("✅ PAR" if int(n)%2==0 else "❌ IMPAR"); dar_estrellas(1)

@comando("impar", N("impar","odd"), es="¿Es impar?", en="Is odd")
def c(a):
    n = num(a[0]) if a else None
    if n is None: print("Ej: impar 7"); return
    print("✅ IMPAR" if int(n)%2==1 else "❌ PAR"); dar_estrellas(1)

@comando("tabla", N("tabla","table"), es="Tabla: tabla 5", en="Times table")
def c(a):
    n = num(a[0]) if a else None
    if n is None: print("Ej: tabla 5"); return
    print(f"📚 Tabla del {int(n)}:")
    for i in range(1,11): print(f"   {int(n)} × {i} = {int(n)*i}")
    dar_estrellas(2)

@comando("contar", N("contar","count"), es="Cuenta hasta N", en="Count to N")
def c(a):
    n = int(num(a[0]) if a else 10)
    print("🔢 " + " ".join(str(i) for i in range(1,n+1)) + " 🎉")
    dar_estrellas(1)

@comando("cuanto_es", N("cuanto_es","how_much"), es="cuanto_es 7 + 5", en="how_much 7 + 5")
def c(a):
    if len(a)<3: print("Ej: cuanto_es 7 + 5"); return
    try:
        x, op, y = int(a[0]), a[1], int(a[2])
        ops = {"+":x+y,"-":x-y,"*":x*y,"x":x*y,"×":x*y,"/":x/y,"÷":x/y}
        if op not in ops: print("Usa + - * /"); return
        print(f"🧮 {x} {op} {y} = {ops[op]}"); dar_estrellas(1)
    except: print("Solo números y + - * /")

@comando("cuadrado_numero", N("cuadrado_numero","square"), es="Cuadrado: cuadrado_numero 5", en="Square")
def c(a):
    n = num(a[0]) if a else None
    if n is None: print("Ej: cuadrado_numero 5"); return
    print(f"✨ {n}² = {n*n}"); dar_estrellas(1)

@comando("cubo_numero", N("cubo_numero","cube"), es="Cubo: cubo_numero 3", en="Cube")
def c(a):
    n = num(a[0]) if a else None
    if n is None: print("Ej: cubo_numero 3"); return
    print(f"✨ {n}³ = {n*n*n}"); dar_estrellas(1)

@comando("comparar", N("comparar","compare"), es="¿Cuál es mayor?", en="Which is bigger")
def c(a):
    x, y = _dos(a)
    if x is None: print("Ej: comparar 5 8"); return
    if x > y: print(f"✅ {x} es mayor que {y}")
    elif x < y: print(f"✅ {y} es mayor que {x}")
    else: print(f"🤝 ¡Son iguales!")
    dar_estrellas(1)

@comando("contar_2", N("contar_2","count_by_2"), es="Contar de 2 en 2", en="Count by 2")
def c(a):
    print("🔢 " + " ".join(str(i) for i in range(2,21,2)) + " 🎉")
    dar_estrellas(1)

@comando("contar_5", N("contar_5","count_by_5"), es="Contar de 5 en 5", en="Count by 5")
def c(a):
    print("🔢 " + " ".join(str(i) for i in range(5,51,5)) + " 🎉")
    dar_estrellas(1)

@comando("contar_10", N("contar_10","count_by_10"), es="Contar de 10 en 10", en="Count by 10")
def c(a):
    print("🔢 " + " ".join(str(i) for i in range(10,101,10)) + " 🎉")
    dar_estrellas(1)

@comando("sumar_hasta", N("sumar_hasta","sum_until"), es="Suma 1+2+... hasta N", en="Sum 1+2+... to N")
def c(a):
    n = num(a[0]) if a else None
    if n is None: print("Ej: sumar_hasta 10"); return
    print(f"✨ 1+2+...+{int(n)} = {sum(range(1,int(n)+1))}"); dar_estrellas(2)

@comando("adivina_operacion", N("adivina_operacion","guess_operation"),
         es="¿Qué operación uso?", en="Guess the operation")
def c(a):
    op = random.choice(["+","-","×"])
    print(f"🎯 Estoy pensando en: {op}")
    print("   ¡Intenta adivinar qué operación es!"); dar_estrellas(1)

# ============================================================
# 📝 LETRAS (15)
# ============================================================
@comando("mayusculas", N("mayusculas","uppercase"), es="MAYÚSCULAS", en="UPPERCASE")
def c(a):
    if not a: print("Ej: mayusculas hola"); return
    print("🔠 " + " ".join(a).upper()); dar_estrellas(1)

@comando("minusculas", N("minusculas","lowercase"), es="minúsculas", en="lowercase")
def c(a):
    if not a: print("Ej: minusculas HOLA"); return
    print("🔡 " + " ".join(a).lower()); dar_estrellas(1)

@comando("al_reves", N("al_reves","reverse"), es="Al revés", en="Reverse")
def c(a):
    if not a: print("Ej: al_reves gato"); return
    print("🔄 " + " ".join(a)[::-1]); dar_estrellas(1)

@comando("contar_letras", N("contar_letras","count_letters"), es="Contar letras", en="Count letters")
def c(a):
    if not a: print("Ej: contar_letras mariposa"); return
    s = " ".join(a); print(f"🔤 '{s}' tiene {len(s)} letras"); dar_estrellas(1)

@comando("vocales", N("vocales","vowels"), es="Contar vocales", en="Count vowels")
def c(a):
    if not a: print("Ej: vocales mariposa"); return
    s = " ".join(a).lower()
    print(f"🔤 '{s}' tiene {sum(1 for c in s if c in 'aeiouáéíóú')} vocales"); dar_estrellas(1)

@comando("primera_letra", N("primera_letra","first_letter"), es="Primera letra", en="First letter")
def c(a):
    if not a: print("Ej: primera_letra gato"); return
    print(f"🔤 Primera letra de '{a[0]}': '{a[0][0].upper()}'"); dar_estrellas(1)

@comando("ultima_letra", N("ultima_letra","last_letter"), es="Última letra", en="Last letter")
def c(a):
    if not a: print("Ej: ultima_letra gato"); return
    print(f"🔤 Última letra de '{a[0]}': '{a[0][-1].upper()}'"); dar_estrellas(1)

@comando("deletrear", N("deletrear","spell"), es="Deletrear: deletrear sol", en="Spell")
def c(a):
    if not a: print("Ej: deletrear sol"); return
    print("🔤 " + " - ".join(a[0].upper()) + " ✨"); dar_estrellas(1)

@comando("palindromo", N("palindromo","palindrome"), es="¿Palíndromo?", en="Palindrome")
def c(a):
    if not a: print("Ej: palindromo oso"); return
    s = "".join(a).lower().replace(" ","")
    print("🎉 ¡Sí!" if s == s[::-1] else f"❌ No, al revés es '{s[::-1]}'")
    dar_estrellas(1)

@comando("adivinanza_palabra", N("adivinanza_palabra","guess_word"), es="Adivina palabra", en="Guess word")
def c(a):
    p = random.choice(["gato","perro","flor","luna","sol","casa","árbol","libro","tren","pelota"])
    print(f"🔍 Palabra de {len(p)} letras: {p[0] + '_'*(len(p)-1)}")
    print(f"   ¡Era {p.upper()}! 🎈")

@comando("espejo", N("espejo","mirror"), es="Espejo: espejo hola", en="Mirror")
def c(a):
    if not a: print("Ej: espejo hola"); return
    print("🪞 " + " ".join(a)[::-1].upper()); dar_estrellas(1)

@comando("contar_palabras", N("contar_palabras","count_words"), es="Contar palabras", en="Count words")
def c(a):
    if not a: print("Ej: contar_palabras hola mundo"); return
    print(f"📝 {len(a)} palabra(s)"); dar_estrellas(1)

@comando("silabas", N("silabas","syllables"), es="Sílabas aprox", en="Syllables")
def c(a):
    if not a: print("Ej: silabas mariposa"); return
    s = a[0].lower()
    print(f"🔤 '{s}' tiene ~{sum(1 for c in s if c in 'aeiouáéíóú')} sílabas"); dar_estrellas(1)

@comando("rimas", N("rimas","rhymes"), es="Busca rimas", en="Find rhymes")
def c(a):
    rimas = {"gato":["pato","zapato","rato"],"flor":["amor","color","calor"],
             "sol":["caracol","farol","girasol"],"luna":["cuna","tuna","fortuna"]}
    if not a or a[0].lower() not in rimas:
        print(f"Prueba con: {', '.join(rimas.keys())}"); return
    print(f"🎵 Rimas de '{a[0]}':")
    for r in rimas[a[0].lower()]: print(f"   • {r}")
    dar_estrellas(2)

@comando("palabra_larga", N("palabra_larga","long_word"), es="Palabra larga del día", en="Long word")
def c(a):
    largas = ["esternocleidomastoideo","electroencefalograma","supercalifragilistico",
              "hipopotomonstrosesquipedaliofobia"]
    p = random.choice(largas)
    print(f"📚 Palabra larga: {p.upper()}")
    print(f"   ¡Tiene {len(p)} letras! 😲"); dar_estrellas(2)

# ============================================================
# 🐾 ANIMALES (20)
# ============================================================
ANIMALES = {
    "perro":{"s":"¡Guau!","e":"🐶","p":4,"b":"cachorro"},
    "gato":{"s":"¡Miau!","e":"🐱","p":4,"b":"gatito"},
    "vaca":{"s":"¡Muuu!","e":"🐮","p":4,"b":"ternero"},
    "pato":{"s":"¡Cuac!","e":"🦆","p":2,"b":"patito"},
    "leon":{"s":"¡GRRR!","e":"🦁","p":4,"b":"cachorro"},
    "elefante":{"s":"¡Pruuum!","e":"🐘","p":4,"b":"elefantito"},
    "caballo":{"s":"¡Iiiii!","e":"🐴","p":4,"b":"potro"},
    "oveja":{"s":"¡Beee!","e":"🐑","p":4,"b":"cordero"},
    "gallina":{"s":"¡Co co!","e":"🐔","p":2,"b":"pollito"},
    "pez":{"s":"¡Blub!","e":"🐟","p":0,"b":"alevín"},
    "tiburon":{"s":"¡Ñac!","e":"🦈","p":0,"b":"criasaurio"},
    "pinguino":{"s":"¡Cuac-cuac!","e":"🐧","p":2,"b":"polluelo"},
    "delfin":{"s":"¡Iii-ii!","e":"🐬","p":0,"b":"cria"},
    "mariposa":{"s":"*silencio*","e":"🦋","p":6,"b":"oruga"},
    "tortuga":{"s":"*lento*","e":"🐢","p":4,"b":"tortuguita"},
    "abeja":{"s":"¡Bzzzz!","e":"🐝","p":6,"b":"larva"},
    "conejo":{"s":"*salta*","e":"🐰","p":4,"b":"gazapo"},
    "zorro":{"s":"¡Yip yip!","e":"🦊","p":4,"b":"zorrito"},
    "oso":{"s":"¡GRRR!","e":"🐻","p":4,"b":"osito"},
    "panda":{"s":"*come bambú*","e":"🐼","p":4,"b":"osito"},
    "jirafa":{"s":"*estira cuello*","e":"🦒","p":4,"b":"jirafita"},
    "buho":{"s":"¡Uu-uu!","e":"🦉","p":2,"b":"polluelo"},
}

@comando("animales", N("animales","animals"), es="Lista animales", en="List animals")
def c(a):
    print("🐾 ANIMALES:")
    for n, i in ANIMALES.items(): print(f"   {i['e']} {n}")

@comando("sonido_animal", N("sonido_animal","animal_sound"), es="Sonido: sonido_animal gato", en="Sound: animal_sound cat")
def c(a):
    if not a: print("Ej: sonido_animal gato"); return
    n = a[0].lower()
    if n in ANIMALES:
        print(f"{ANIMALES[n]['e']} El {n} hace {ANIMALES[n]['s']}"); dar_estrellas(1)
    else: print(f"No conozco '{n}'")

@comando("animal_aleatorio", N("animal_aleatorio","random_animal"), es="Animal al azar", en="Random animal")
def c(a):
    n = random.choice(list(ANIMALES.keys()))
    print(f"🎲 ¡Te tocó: {ANIMALES[n]['e']} {n.upper()}!"); dar_estrellas(1)

@comando("donde_vive", N("donde_vive","where_lives"), es="Dónde vive: donde_vive leon", en="Where lives")
def c(a):
    h = {"perro":"casa 🏠","gato":"casa 🏠","vaca":"granja 🚜","pato":"estanque 🦆",
         "leon":"selva 🌳","elefante":"sabana 🌾","caballo":"granja 🐴","oveja":"montaña ⛰️",
         "gallina":"granja 🐔","pez":"agua 💧","tiburon":"mar 🌊","pinguino":"polo ❄️",
         "delfin":"mar 🌊","mariposa":"jardín 🌸","tortuga":"mar/río 🐢","abeja":"colmena 🍯",
         "conejo":"madriguera 🕳️","zorro":"bosque 🌲","oso":"cueva 🏔️","panda":"bambú 🎋",
         "jirafa":"sabana 🌾","buho":"árbol 🌳"}
    if not a or a[0].lower() not in h: print("Ej: donde_vive leon"); return
    n = a[0].lower()
    print(f"{ANIMALES[n]['e']} El {n} vive en {h[n]}"); dar_estrellas(1)

@comando("patas", N("patas","legs"), es="Cuántas patas", en="How many legs")
def c(a):
    if not a or a[0].lower() not in ANIMALES: print("Ej: patas perro"); return
    n = a[0].lower(); p = ANIMALES[n]["p"]
    print(f"{ANIMALES[n]['e']} El {n} tiene {p} patas"); dar_estrellas(1)

@comando("bebe_animal", N("bebe_animal","baby_animal"), es="Bebé animal", en="Baby animal")
def c(a):
    if not a or a[0].lower() not in ANIMALES: print("Ej: bebe_animal gato"); return
    n = a[0].lower()
    print(f"🍼 Bebé del {n}: {ANIMALES[n]['b'].upper()}"); dar_estrellas(1)

@comando("adivina_animal", N("adivina_animal","guess_animal"), es="Adivina animal", en="Guess animal")
def c(a):
    n, i = random.choice(list(ANIMALES.items()))
    print(f"🎵 Sonido: {i['s']}")
    print(f"   ¡Es el {n} {i['e']}!"); dar_estrellas(1)

@comando("animal_favorito", N("animal_favorito","favorite_animal"), es="Tu animal favorito", en="Favorite animal")
def c(a):
    if not a: print("Ej: animal_favorito leon"); return
    print(f"¡A mí también me gusta el {a[0]}! {random.choice(['🦁','🐶','🐱','🐘','🐼','🦄'])}")
    dar_estrellas(1)

def _animal_simple(nombre, emoji, sonido, dato):
    def impl(a):
        print(f"{emoji} {nombre.upper()}")
        print(f"   Sonido: {sonido}")
        print(f"   {dato}")
        dar_estrellas(1)
    return impl

@comando("tiburon", N("tiburon","shark"), es="Sobre el tiburón", en="About shark")
def c(a): _animal_simple("tiburón","🦈","¡Ñac ñac!","¡Tiene muchos dientes!") (a)

@comando("pinguino", N("pinguino","penguin"), es="Sobre el pingüino", en="About penguin")
def c(a): _animal_simple("pingüino","🐧","¡Cuac cuac!","¡No vuela pero nada genial!") (a)

@comando("delfin", N("delfin","dolphin"), es="Sobre el delfín", en="About dolphin")
def c(a): _animal_simple("delfín","🐬","¡Iii ii!","¡Es muy inteligente!") (a)

@comando("mariposa", N("mariposa","butterfly"), es="Sobre la mariposa", en="About butterfly")
def c(a): _animal_simple("mariposa","🦋","*silencio*","¡Nace de una oruga!") (a)

@comando("tortuga", N("tortuga","turtle"), es="Sobre la tortuga", en="About turtle")
def c(a): _animal_simple("tortuga","🐢","*lento*","¡Vive muchos años!") (a)

@comando("abeja", N("abeja","bee"), es="Sobre la abeja", en="About bee")
def c(a): _animal_simple("abeja","🐝","¡Bzzzz!","¡Hace miel! 🍯") (a)

@comando("conejo", N("conejo","rabbit"), es="Sobre el conejo", en="About rabbit")
def c(a): _animal_simple("conejo","🐰","*salta*","¡Salta muy alto!") (a)

@comando("zorro", N("zorro","fox"), es="Sobre el zorro", en="About fox")
def c(a): _animal_simple("zorro","🦊","¡Yip yip!","¡Es muy astuto!") (a)

@comando("oso", N("oso","bear"), es="Sobre el oso", en="About bear")
def c(a): _animal_simple("oso","🐻","¡GRRR!","¡Le encanta la miel!") (a)

@comando("panda", N("panda","panda"), es="Sobre el panda", en="About panda")
def c(a): _animal_simple("panda","🐼","*come bambú*","¡Es blanco y negro!") (a)

@comando("jirafa", N("jirafa","giraffe"), es="Sobre la jirafa", en="About giraffe")
def c(a): _animal_simple("jirafa","🦒","*estira cuello*","¡Tiene el cuello muy largo!") (a)

@comando("buho", N("buho","owl"), es="Sobre el búho", en="About owl")
def c(a): _animal_simple("búho","🦉","¡Uu-uu!","¡Ve de noche!") (a)

# ============================================================
# 🎨 COLORES (8)
# ============================================================
@comando("arcoiris", N("arcoiris","rainbow"), es="Arcoíris", en="Rainbow")
def c(a):
    print("🌈 ARCOÍRIS:")
    for col, e in [("ROJO","🔴"),("NARANJA","🟠"),("AMARILLO","🟡"),
                   ("VERDE","🟢"),("AZUL","🔵"),("MORADO","🟣")]:
        print(f"  {e} {col}")
    dar_estrellas(2)

@comando("semaforo", N("semaforo","traffic_light"), es="Semáforo", en="Traffic light")
def c(a):
    print("🚦 SEMÁFORO:")
    print("  🔴 ROJO → ¡ALTO! ✋")
    print("  🟡 ÁMBAR → ¡ESPERA! ⏸️")
    print("  🟢 VERDE → ¡ADELANTE! 🚶")
    dar_estrellas(2)

@comando("color_aleatorio", N("color_aleatorio","random_color"), es="Color al azar", en="Random color")
def c(a):
    cs = [("ROJO","🔴"),("AZUL","🔵"),("VERDE","🟢"),("AMARILLO","🟡"),
          ("NARANJA","🟠"),("MORADO","🟣"),("ROSA","💗"),("BLANCO","⚪"),("NEGRO","⚫")]
    cc, e = random.choice(cs)
    print(f"🎨 ¡Color mágico: {e} {cc}!"); dar_estrellas(1)

@comando("mezcla", N("mezcla","mix"), es="Mezcla colores", en="Mix colors")
def c(a):
    if len(a) < 2: print("Ej: mezcla azul amarillo"); return
    m = {frozenset(["azul","amarillo"]):"VERDE 🟢", frozenset(["rojo","azul"]):"MORADO 🟣",
         frozenset(["rojo","amarillo"]):"NARANJA 🟠", frozenset(["rojo","blanco"]):"ROSA 💗",
         frozenset(["azul","blanco"]):"CELESTE 💙", frozenset(["negro","blanco"]):"GRIS 🩶"}
    k = frozenset([a[0].lower(),a[1].lower()])
    if k in m: print(f"🎨 {a[0].upper()} + {a[1].upper()} = {m[k]}"); dar_estrellas(2)
    else: print("Prueba con: azul, amarillo, rojo, blanco, negro")

@comando("formas", N("formas","shapes"), es="Formas", en="Shapes")
def c(a):
    print("🔺 FORMAS:")
    print("   ⚪ Círculo    - ¡Redondo!")
    print("   ⬛ Cuadrado   - 4 lados")
    print("   🔺 Triángulo  - 3 lados")
    print("   ⭐ Estrella   - 5 puntas")
    print("   ❤️  Corazón   - ¡Con amor!")
    dar_estrellas(1)

@comando("lados", N("lados","sides"), es="Cuántos lados", en="How many sides")
def c(a):
    l = {"circulo":0,"círculo":0,"cuadrado":4,"triangulo":3,"triángulo":3,
         "estrella":10,"rectangulo":4,"rectángulo":4,"pentagono":5,"hexagono":6}
    if not a or a[0].lower() not in l: print("Ej: lados cuadrado"); return
    print(f"📐 El {a[0]} tiene {l[a[0].lower()]} lados"); dar_estrellas(1)

@comando("color_favorito", N("color_favorito","favorite_color"), es="Tu color favorito", en="Favorite color")
def c(a):
    if not a: print("Ej: color_favorito azul"); return
    print(f"¡El {a[0].upper()} es un color precioso! {random.choice(['🎨','🌈','💖','✨'])}")
    dar_estrellas(1)

@comando("pintura", N("pintura","painting"), es="Idea de pintura", en="Painting idea")
def c(a):
    ideas = ["un 🐶 perro con sombrero","un 🌈 arcoíris","una 🦄 unicornio",
             "un 🐱 gato dormilón","un 🌳 árbol mágico","una 🚀 nave espacial"]
    print(f"🎨 ¡Pinta {random.choice(ideas)}!"); dar_estrellas(1)

# ============================================================
# 🎮 JUEGOS (23)
# ============================================================
@comando("dado", N("dado","dice"), es="Tira el dado", en="Roll a die")
def c(a):
    n = random.randint(1,6); print(f"🎲 Salió {n}! {'⚀⚁⚂⚃⚄⚅'[n-1]}"); dar_estrellas(1)

@comando("moneda", N("moneda","coin"), es="Lanza moneda", en="Flip a coin")
def c(a): print(f"🪙 ¡{random.choice(['CARA','CRUZ'])}!"); dar_estrellas(1)

@comando("cara_o_cruz", N("cara_o_cruz","heads_or_tails"), es="cara_o_cruz cara", en="heads_or_tails heads")
def c(a):
    if not a: print("Ej: cara_o_cruz cara"); return
    yo = a[0].lower(); maq = random.choice(["cara","cruz"])
    print(f"🪙 Salió: {maq.upper()}")
    if yo == maq: print("🎉 ¡ACERTASTE!"); dar_estrellas(2)
    else: print("¡Ups! Otra vez 💪"); dar_estrellas(1)

@comando("piedra_papel", N("piedra_papel","rock_paper"), es="piedra_papel piedra", en="rock_paper rock")
def c(a):
    if not a: print("Ej: piedra_papel piedra"); return
    yo = a[0].lower()
    trad = {"rock":"piedra","paper":"papel","scissors":"tijera","tijeras":"tijera"}
    yo = trad.get(yo, yo)
    if yo not in ("piedra","papel","tijera"): print("Elige: piedra, papel, tijera"); return
    maq = random.choice(["piedra","papel","tijera"])
    e = {"piedra":"✊","papel":"✋","tijera":"✌️"}
    print(f"Tú: {e[yo]} {yo}   Yo: {e[maq]} {maq}")
    if yo == maq: print("¡EMPATE! 🤝"); dar_estrellas(1)
    elif (yo,maq) in [("piedra","tijera"),("papel","piedra"),("tijera","papel")]:
        print("🎉 ¡GANASTE!"); dar_estrellas(2)
    else: print("¡Yo gano! 😄"); dar_estrellas(1)

@comando("adivina_numero", N("adivina_numero","guess_number"), es="Adivina número 1-10", en="Guess number 1-10")
def c(a):
    n = random.randint(1,10)
    print(f"🔢 Pensé el {n}. ¿Adivinaste?"); dar_estrellas(1)

@comando("veo_veo", N("veo_veo","i_spy"), es="Veo veo", en="I spy")
def c(a):
    cosas = [("una 🍎 manzana","rojo"),("un 🐤 patito","amarillo"),("una 🌳 hoja","verde"),
             ("un 🚗 coche","azul"),("un 🎈 globo","morado")]
    o, c2 = random.choice(cosas)
    print(f"👀 Veo veo... ¡de color {c2.upper()}!")
    print(f"   ¡Era {o}! 🎉"); dar_estrellas(1)

@comando("chiste", N("chiste","joke"), es="Un chiste", en="A joke")
def c(a):
    print("😂 " + random.choice([
        "¿Qué le dice un 🐘 a otro? ¡Nada, se lo dicen con la trompa! 🤣",
        "¿Cómo se despiden los 🌊? ¡Con olas! 👋🌊",
        "¿Qué hace una 🐝 en el gimnasio? ¡Zumba! 🐝💃",
        "¿Por qué los 🐦 vuelan al sur? ¡Porque caminando se cansan! 🚶😂"]))
    dar_estrellas(1)

@comando("adivinanza", N("adivinanza","riddle"), es="Una adivinanza", en="A riddle")
def c(a):
    advs = [("¿Qué tiene patas pero no camina? 🪑","La silla"),
            ("¿Qué sube y baja pero se queda igual? 🪜","La escalera"),
            ("Tengo agujas y no sé coser. 🕐","El reloj"),
            ("Vuela sin alas, silba sin boca. 💨","El viento"),
            ("Blanco por dentro, verde por fuera. 🍐","La pera")]
    p, r = random.choice(advs)
    print(f"🧩 {p}")
    print(f"   🤫 ¡{r.upper()}!"); dar_estrellas(2)

@comando("verdad_reto", N("verdad_reto","truth_dare"), es="Verdad o reto", en="Truth or dare")
def c(a):
    print("🎯 RETO: " + random.choice([
        "Cuenta un chiste 🎤","Imita un animal 🐮","Di el abecedario al revés 🔤",
        "Haz 5 saltos 🦘","Cuenta hasta 10 en inglés 🔢","Haz una cara graciosa 😜",
        "Dibuja un corazón ❤️","Canta una canción 🎵"]))
    dar_estrellas(1)

@comando("simon", N("simon","simon"), es="Simón dice", en="Simon says")
def c(a):
    print("🎮 Simón dice: " + random.choice([
        "¡Toca tu nariz! 👃","¡Da una palmada! 👏","¡Salta! 🤸",
        "¡Cierra los ojos! 😌","¡Di hola! 👋","¡Toca tu cabeza! 🙋"]))
    dar_estrellas(1)

@comando("ruleta_kids", N("ruleta_kids","kids_wheel"), es="Ruleta de actividades", en="Activity wheel")
def c(a):
    print("🎡 " + random.choice([
        "¡Baila 10 segundos! 💃","¡Cuenta hasta 20! 🔢","¡Di 5 animales! 🐾",
        "¡Nombra 3 colores en inglés! 🎨","¡Haz un dibujo! ✏️","¡Canta el abecedario! 🎵"]))
    dar_estrellas(1)

@comando("memoria", N("memoria","memory"), es="Memoriza la secuencia", en="Memorize sequence")
def c(a):
    seq = [random.choice(["🔴","🔵","🟢","🟡","🟣","🟠"]) for _ in range(4)]
    print("🧠 Memoriza: " + " ".join(seq)); dar_estrellas(1)

@comando("ahorcado", N("ahorcado","hangman"), es="Ahorcado simple", en="Simple hangman")
def c(a):
    p = random.choice(["gato","perro","flor","casa","sol","luna"])
    print(f"🎯 Palabra: {'_ '*len(p)}")
    print(f"   Pista: {len(p)} letras. ¡La palabra es {p.upper()}!")
    dar_estrellas(2)

@comando("tesoro", N("tesoro","treasure"), es="Busca el tesoro", en="Find the treasure")
def c(a):
    print("🏴‍☠️ *cava en la arena*")
    print(f"   {random.choice(['💎 ¡Diamante!','🪙 ¡Monedas de oro!','👑 ¡Corona!','📜 ¡Mapa antiguo!'])}")
    dar_estrellas(3)

@comando("laberinto", N("laberinto","maze"), es="Laberinto", en="Maze")
def c(a):
    print("🌀 LABERINTO:")
    print("   🐭 → → ↓ ↓ ← ← ↓ → 🧀")
    print("   ¡El ratón llegó al queso! 🎉"); dar_estrellas(2)

@comando("sopa_letras", N("sopa_letras","word_search"), es="Sopa de letras", en="Word search")
def c(a):
    print("🔍 SOPA DE LETRAS:")
    for _ in range(4):
        print("   " + " ".join(random.choice("ABCDEFGHIJKLMNOPRSTUV") for _ in range(8)))
    print("   ¡Busca 3 palabras! 🎯"); dar_estrellas(2)

@comando("pictionary", N("pictionary","pictionary"), es="Pictionary", en="Pictionary")
def c(a):
    cosas = ["un 🐶 perro","una 🏠 casa","un ☀️ sol","una 🌸 flor","un ⭐ estrella",
             "un 🚗 coche","una 🦋 mariposa","un 🍕 pizza"]
    print(f"🎨 ¡Dibuja {random.choice(cosas)}!"); dar_estrellas(2)

@comando("memoria_numeros", N("memoria_numeros","number_memory"), es="Memoriza números", en="Number memory")
def c(a):
    nums = [random.randint(0,9) for _ in range(4)]
    print("🧠 Memoriza: " + " ".join(str(n) for n in nums))
    print("   (ahora repítelos)"); dar_estrellas(1)

@comando("gestos", N("gestos","charades"), es="Juego de mímica", en="Charades")
def c(a):
    print("🎭 MÍMICA: " + random.choice([
        "Imita un 🐘 elefante","Imita un 🐧 pingüino","Imita un 🦁 león",
        "Imita un 🐸 rana","Imita un 🤖 robot","Imita un 🦄 unicornio"]))
    dar_estrellas(1)

@comando("escondite", N("escondite","hide_seek"), es="Escondite", en="Hide and seek")
def c(a):
    print("🙈 ¡A contar hasta 10!")
    for i in range(1,11): print(f"   {i}...", end=" ", flush=True)
    print("\n🔍 ¡A buscarte!"); dar_estrellas(1)

@comando("chiste2", N("chiste2","joke2"), es="Otro chiste", en="Another joke")
def c(a):
    print("😂 " + random.choice([
        "¿Qué le dijo un 🐟 a otro? ¡Nada! 🐠",
        "¿Por qué los 🐘 no usan computadora? ¡Miedo al ratón! 🖱️",
        "¿Qué le dijo un 🦁 al otro? ¡Nos vemos en la selva! 🌳",
        "¿Cómo se llama un 🦆 que va al médico? ¡Pato-logía! 🩺🦆"]))
    dar_estrellas(1)

@comando("adivinanza2", N("adivinanza2","riddle2"), es="Otra adivinanza", en="Another riddle")
def c(a):
    advs = [("Oro parece, plata no es. 🍌","El plátano"),
            ("¿Qué cosa es que teje y no ve? 🕷️","La araña"),
            ("Cabeza de hierro, pies de madera. 🔨","El martillo"),
            ("¿Qué tiene dientes y no muerde? 🪮","El peine")]
    p, r = random.choice(advs)
    print(f"🧩 {p}"); print(f"   🤫 ¡{r.upper()}!"); dar_estrellas(2)

@comando("sorpresa", N("sorpresa","surprise"), es="Sorpresa divertida", en="Fun surprise")
def c(a):
    print("🎁 " + random.choice([
        "¡Baila como un pingüino! 🐧💃","¡Haz un sonido de animal! 🐮",
        "¡Cuenta un chiste! 😂","¡Dibuja una estrella! ⭐",
        "¡Dale un abrazo a alguien! 🤗"]))
    dar_estrellas(2)

# ============================================================
# ✏️ ARTE / LIENZO ASCII (15)
# ============================================================
@comando("lienzo", N("lienzo","canvas"), es="Crea un lienzo nuevo (borra el anterior)", en="Create a new canvas")
def c(a):
    _lienzo_nuevo()
    print(f"🎨 ¡Lienzo nuevo de {STATE['lienzo_ancho']}×{STATE['lienzo_alto']} creado!")
    print(f"   Usa '{nom_act('pintar')} x y @' para dibujar")
    dar_estrellas(1)

@comando("tamano_lienzo", N("tamano_lienzo","canvas_size"),
         es="Cambia tamaño: tamano_lienzo 40 15", en="Change size: canvas_size 40 15")
def c(a):
    if len(a) < 2: print("Ej: tamano_lienzo 40 15"); return
    w, h = int(a[0]), int(a[1])
    if not (5 <= w <= 100 and 3 <= h <= 40):
        print("Rango: ancho 5-100, alto 3-40"); return
    STATE["lienzo_ancho"] = w; STATE["lienzo_alto"] = h
    _lienzo_nuevo()
    print(f"🎨 Lienzo de {w}×{h} creado"); dar_estrellas(1)

@comando("ver_portada", N("ver_portada","see_cover"),
         es="Muestra tu portada en ASCII", en="Show your ASCII cover")
def c(a):
    _lienzo_mostrar()
    dar_estrellas(1)

@comando("pintar", N("pintar","paint"),
         es="Pinta un carácter: pintar x y @", en="Paint a char: paint x y @")
def c(a):
    if len(a) < 3: print("Ej: pintar 5 2 @"); return
    try:
        x, y = int(a[0]), int(a[1]); ch = a[2]
        _lienzo_poner(x, y, ch)
        print(f"✏️  Pintado '{ch}' en ({x},{y})"); dar_estrellas(1)
    except Exception as e:
        print(f"Error: {e}")

@comando("pincel", N("pincel","brush"),
         es="Cambia el carácter del pincel: pincel @", en="Change brush char: brush @")
def c(a):
    if not a: print(f"Pincel actual: '{STATE['pincel']}'. Uso: pincel @"); return
    STATE["pincel"] = a[0][0]
    print(f"🖌️  Pincel cambiado a '{STATE['pincel']}'"); dar_estrellas(1)

@comando("texto_ascii", N("texto_ascii","ascii_text"),
         es="Escribe texto: texto_ascii 5 2 HOLA", en="Write text: ascii_text 5 2 HELLO")
def c(a):
    if len(a) < 3: print("Ej: texto_ascii 5 2 HOLA"); return
    try:
        x, y = int(a[0]), int(a[1])
        texto = " ".join(a[2:])
        for i, ch in enumerate(texto):
            _lienzo_poner(x + i, y, ch)
        print(f"✏️  Escrito '{texto}' en ({x},{y})"); dar_estrellas(2)
    except Exception as e:
        print(f"Error: {e}")

@comando("linea", N("linea","line"),
         es="Dibuja línea: linea x1 y1 x2 y2 @", en="Draw line: line x1 y1 x2 y2 @")
def c(a):
    if len(a) < 4: print("Ej: linea 1 1 20 1 *"); return
    try:
        x1, y1, x2, y2 = int(a[0]), int(a[1]), int(a[2]), int(a[3])
        ch = a[4] if len(a) > 4 else STATE["pincel"]
        # Algoritmo Bresenham
        dx = abs(x2-x1); dy = abs(y2-y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        while True:
            _lienzo_poner(x1, y1, ch)
            if x1 == x2 and y1 == y2: break
            e2 = 2 * err
            if e2 > -dy: err -= dy; x1 += sx
            if e2 < dx: err += dx; y1 += sy
        print(f"✏️  Línea de ({int(a[0])},{int(a[1])}) a ({int(a[2])},{int(a[3])})"); dar_estrellas(2)
    except Exception as e:
        print(f"Error: {e}")

@comando("rectangulo_ascii", N("rectangulo_ascii","ascii_rect"),
         es="Dibuja rectángulo: rectangulo_ascii x1 y1 x2 y2 @",
         en="Draw rect: ascii_rect x1 y1 x2 y2 @")
def c(a):
    if len(a) < 4: print("Ej: rectangulo_ascii 2 2 20 10 *"); return
    try:
        x1, y1, x2, y2 = int(a[0]), int(a[1]), int(a[2]), int(a[3])
        ch = a[4] if len(a) > 4 else STATE["pincel"]
        for x in range(x1, x2+1):
            _lienzo_poner(x, y1, ch); _lienzo_poner(x, y2, ch)
        for y in range(y1, y2+1):
            _lienzo_poner(x1, y, ch); _lienzo_poner(x2, y, ch)
        print("✏️  Rectángulo dibujado"); dar_estrellas(2)
    except Exception as e:
        print(f"Error: {e}")

@comando("circulo_ascii", N("circulo_ascii","ascii_circle"),
         es="Dibuja círculo: circulo_ascii cx cy r @", en="Draw circle: ascii_circle cx cy r @")
def c(a):
    if len(a) < 3: print("Ej: circulo_ascii 10 7 5 *"); return
    try:
        cx, cy, r = int(a[0]), int(a[1]), int(a[2])
        ch = a[3] if len(a) > 3 else STATE["pincel"]
        for ang in range(0, 360, 3):
            rad = math.radians(ang)
            x = int(cx + r * math.cos(rad))
            y = int(cy + r * math.sin(rad) * 0.5)
            _lienzo_poner(x, y, ch)
        print("✏️  Círculo dibujado"); dar_estrellas(2)
    except Exception as e:
        print(f"Error: {e}")

@comando("rellenar_ascii", N("rellenar_ascii","ascii_fill"),
         es="Rellena todo el lienzo: rellenar_ascii @", en="Fill canvas: ascii_fill @")
def c(a):
    ch = a[0] if a else STATE["pincel"]
    _lienzo_asegurar()
    for y in range(STATE["lienzo_alto"]):
        for x in range(STATE["lienzo_ancho"]):
            STATE["lienzo"][y][x] = ch[0]
    print(f"🎨 Lienzo rellenado con '{ch[0]}'"); dar_estrellas(1)

@comando("simetria_ascii", N("simetria_ascii","ascii_symmetry"),
         es="Haz simetría (espejo horizontal)", en="Make symmetry (mirror)")
def c(a):
    _lienzo_asegurar()
    for y in range(STATE["lienzo_alto"]):
        for x in range(STATE["lienzo_ancho"] // 2):
            STATE["lienzo"][y][STATE["lienzo_ancho"] - 1 - x] = STATE["lienzo"][y][x]
    print("✨ Simetría aplicada"); dar_estrellas(2)

@comando("borrar_lienzo", N("borrar_lienzo","clear_canvas"),
         es="Borra todo el lienzo", en="Clear canvas")
def c(a):
    _lienzo_nuevo(); print("🧽 Lienzo borrado"); dar_estrellas(1)

@comando("exportar_ascii", N("exportar_ascii","export_ascii"),
         es="Guarda tu portada: exportar_ascii portada.txt", en="Save cover: export_ascii cover.txt")
def c(a):
    _lienzo_asegurar()
    ruta = a[0] if a else "portada.txt"
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            for fila in STATE["lienzo"]:
                f.write("".join(fila) + "\n")
        print(f"💾 Guardado en '{ruta}'"); dar_estrellas(3)
    except Exception as e: print(f"Error: {e}")

@comando("ayuda_lienzo", N("ayuda_lienzo","canvas_help"),
         es="Ayuda del lienzo ASCII", en="Canvas ASCII help")
def c(a):
    print("🎨 LIENZO ASCII — AYUDA")
    print(f"   {nom_act('lienzo'):<25} Crea lienzo nuevo")
    print(f"   {nom_act('tamano_lienzo'):<25} Cambia tamaño: tamano_lienzo 40 15")
    print(f"   {nom_act('pintar'):<25} Pinta char: pintar x y @")
    print(f"   {nom_act('pincel'):<25} Cambia el pincel: pincel #")
    print(f"   {nom_act('texto_ascii'):<25} Escribe texto: texto_ascii 5 2 HOLA")
    print(f"   {nom_act('linea'):<25} Línea: linea 1 1 20 1 *")
    print(f"   {nom_act('rectangulo_ascii'):<25} Rect: rectangulo_ascii 2 2 20 10 *")
    print(f"   {nom_act('circulo_ascii'):<25} Círculo: circulo_ascii 10 7 5 *")
    print(f"   {nom_act('rellenar_ascii'):<25} Rellena el lienzo: rellenar_ascii @")
    print(f"   {nom_act('simetria_ascii'):<25} Simetría horizontal")
    print(f"   {nom_act('borrar_lienzo'):<25} Borra todo")
    print(f"   {nom_act('ver_portada'):<25} Muestra tu portada")
    print(f"   {nom_act('exportar_ascii'):<25} Guarda en archivo")
    dar_estrellas(1)

# ============================================================
# 📖 CUENTOS (10)
# ============================================================
@comando("cuento", N("cuento","story"), es="Un cuento", en="A story")
def c(a):
    print(random.choice([
        "🦄 Había un unicornio que vivía en las nubes. Conoció a Luna y fueron amigos. FIN ✨",
        "🐢 Una tortuga ganó la carrera entrenando cada día. FIN 🏆",
        "🐭 Un ratoncito encontró su queso en el zapato del abuelo. FIN 🧀",
        "🌟 Una estrellita le dio un deseo a un niño. FIN 💫"]))
    dar_estrellas(2)

@comando("poema", N("poema","poem"), es="Un poema", en="A poem")
def c(a):
    print(random.choice([
        "🌻 En el jardín de mi casa,\n   crece una flor hermosa,\n   como tú, {n}.",
        "🌙 La luna y las estrellas,\n   iluminan tu ventana,\n   ¡descansa, {n}!",
        "🌈 Si te sientes triste,\n   mira un arcoíris brillar,\n   ¡hay mucho que soñar!"]).format(n=STATE["nombre"]))
    dar_estrellas(2)

@comando("cancion", N("cancion","song"), es="Una canción", en="A song")
def c(a):
    print(random.choice([
        "🎵 'Estrellita, ¿dónde estás?\n   Me pregunto quién serás...' ✨",
        "🎵 'Los pollitos dicen pío pío...' 🐣",
        "🎵 'Sol solecito, caliéntame un poquito...' ☀️"]))
    dar_estrellas(2)

@comando("felicidades", N("felicidades","congrats"), es="Te felicito", en="Congrats")
def c(a):
    m = " ".join(a) if a else "ser increíble"
    print(f"🎉 ¡FELICIDADES, {STATE['nombre']}, por {m}! 🎊"); dar_estrellas(2)

@comando("fabula", N("fabula","fable"), es="Una fábula", en="A fable")
def c(a):
    print(random.choice([
        "🐢🐇 La liebre se burló de la tortuga. Corrieron y... ¡ganó la tortuga! Moraleja: la constancia vence. 💪",
        "🐜🦗 La hormiga trabajó todo el verano, el grillo solo cantó. En invierno el grillo aprendió. Moraleja: hay que ser previsor. 🍯",
        "🦊🍇 El zorro no llegaba a las uvas y dijo que estaban verdes. Moraleja: a veces despreciamos lo que no podemos tener. 🍇"]))
    dar_estrellas(3)

@comando("trabalenguas", N("trabalenguas","tongue_twister"), es="Un trabalenguas", en="Tongue twister")
def c(a):
    print(random.choice([
        "👅 'Tres tristes tigres tragaban trigo en un trigal.'",
        "👅 'El perro de San Roque no tiene rabo.'",
        "👅 'Pablito clavó un clavito en la calva de un calvito.'",
        "👅 'Cómo quieres que te quiera si el que quiero no me quiere.'"]))
    dar_estrellas(2)

@comando("refran", N("refran","proverb"), es="Un refrán", en="A proverb")
def c(a):
    print("📜 " + random.choice([
        "A quien madruga, Dios le ayuda. ☀️",
        "Más vale tarde que nunca. 🐢",
        "En boca cerrada no entran moscas. 🤐",
        "Quien siembra, recoge. 🌱"]))
    dar_estrellas(1)

@comando("chiste_largo", N("chiste_largo","long_joke"), es="Chiste largo", en="Long joke")
def c(a):
    print("😂 Había un 🐘 que quería volar...")
    print("   Se subió a un árbol, saltó... y ¡PUM! 💥")
    print("   Pero lo intentó otra vez, y otra... ¡hasta que aprendió a caer bonito! 😄")
    dar_estrellas(2)

@comando("mini_cuento", N("mini_cuento","short_story"), es="Mini cuento", en="Short story")
def c(a):
    print("🌟 Erase una vez...")
    print(f"   Un/a niño/a llamado/a {STATE['nombre']} que descubrió una puerta mágica.")
    print("   La abrió y encontró un mundo lleno de colores.")
    print("   FIN 🌈"); dar_estrellas(3)

@comando("poema_amor", N("poema_amor","love_poem"), es="Poema de amistad", en="Friendship poem")
def c(a):
    print(f"💖 {STATE['nombre']}, eres especial,")
    print("   como una estrella sin igual,")
    print("   cada día al despertar,")
    print("   tu amistad me hace brillar. ✨")
    dar_estrellas(2)

# ============================================================
# 🌟 APRENDER (14)
# ============================================================
@comando("dia_hoy", N("dia_hoy","today"), es="Qué día es hoy", en="What day is it")
def c(a):
    dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    d = datetime.datetime.now()
    print(f"📅 Hoy es {dias[d.weekday()]}, {d.day}/{d.month}/{d.year}")
    dar_estrellas(1)

@comando("estacion", N("estacion","season"), es="Qué estación es", en="What season")
def c(a):
    m = datetime.datetime.now().month
    if m in (12,1,2): e = "Invierno ❄️"
    elif m in (3,4,5): e = "Primavera 🌸"
    elif m in (6,7,8): e = "Verano ☀️"
    else: e = "Otoño 🍂"
    print(f"🌍 Estamos en {e}"); dar_estrellas(1)

@comando("planetas", N("planetas","planets"), es="Los planetas", en="The planets")
def c(a):
    print("🪐 SISTEMA SOLAR:")
    for p, e in [("Mercurio","🟤"),("Venus","🟡"),("Tierra","🌍"),("Marte","🔴"),
                 ("Júpiter","🟠"),("Saturno","🪐"),("Urano","🔵"),("Neptuno","🔷")]:
        print(f"   {e} {p}")
    dar_estrellas(2)

@comando("ingles", N("ingles","english"), es="Palabra en inglés: ingles perro", en="Word in Spanish: english dog")
def c(a):
    d = {"perro":"dog 🐶","gato":"cat 🐱","casa":"house 🏠","sol":"sun ☀️","luna":"moon 🌙",
         "agua":"water 💧","rojo":"red 🔴","azul":"blue 🔵","uno":"one 1️⃣","dos":"two 2️⃣",
         "tres":"three 3️⃣","hola":"hello 👋","gracias":"thank you 🙏","amigo":"friend 🤝",
         "flor":"flower 🌸","dog":"perro 🐶","cat":"gato 🐱","house":"casa 🏠"}
    if not a or a[0].lower() not in d: print("Ej: ingles perro"); return
    print(f"🇬🇧 {a[0].upper()} → {d[a[0].lower()]}"); dar_estrellas(1)

@comando("dias_semana", N("dias_semana","weekdays"), es="Días de la semana", en="Weekdays")
def c(a):
    print("📅 DÍAS DE LA SEMANA:")
    for i, d in enumerate(["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"],1):
        print(f"   {i}. {d}")
    dar_estrellas(2)

@comando("meses", N("meses","months"), es="Meses del año", en="Months of the year")
def c(a):
    print("📅 MESES DEL AÑO:")
    for i, m in enumerate(["Enero","Febrero","Marzo","Abril","Mayo","Junio",
                            "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"],1):
        print(f"   {i}. {m}")
    dar_estrellas(2)

@comando("abecedario", N("abecedario","alphabet"), es="El abecedario", en="The alphabet")
def c(a):
    print("🔤 ABECEDARIO:")
    print("   " + " ".join("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"))
    dar_estrellas(2)

@comando("numeros_ingles", N("numeros_ingles","numbers_english"), es="Números en inglés", en="Numbers in English")
def c(a):
    print("🔢 NÚMEROS EN INGLÉS:")
    for n, i in [("uno","one"),("dos","two"),("tres","three"),("cuatro","four"),
                 ("cinco","five"),("seis","six"),("siete","seven"),("ocho","eight"),
                 ("nueve","nine"),("diez","ten")]:
        print(f"   {n} = {i}")
    dar_estrellas(2)

@comando("colores_ingles", N("colores_ingles","colors_english"), es="Colores en inglés", en="Colors in English")
def c(a):
    print("🎨 COLORES EN INGLÉS:")
    for s, e in [("rojo","red 🔴"),("azul","blue 🔵"),("verde","green 🟢"),
                 ("amarillo","yellow 🟡"),("naranja","orange 🟠"),("morado","purple 🟣"),
                 ("rosa","pink 💗"),("blanco","white ⚪"),("negro","black ⚫")]:
        print(f"   {s} = {e}")
    dar_estrellas(2)

@comando("cuerpo_humano", N("cuerpo_humano","human_body"), es="El cuerpo humano", en="Human body")
def c(a):
    print("🧍 PARTES DEL CUERPO:")
    for p, e in [("Cabeza","🙂"),("Ojos","👀"),("Nariz","👃"),("Boca","👄"),
                 ("Manos","✋"),("Brazos","💪"),("Piernas","🦵"),("Pies","🦶")]:
        print(f"   {e} {p}")
    dar_estrellas(2)

@comando("frutas", N("frutas","fruits"), es="Las frutas", en="Fruits")
def c(a):
    print("🍎 FRUTAS:")
    for f, e in [("Manzana","🍎"),("Plátano","🍌"),("Naranja","🍊"),("Uva","🍇"),
                 ("Sandía","🍉"),("Fresa","🍓"),("Piña","🍍"),("Pera","🍐")]:
        print(f"   {e} {f}")
    dar_estrellas(2)

@comando("verduras", N("verduras","vegetables"), es="Las verduras", en="Vegetables")
def c(a):
    print("🥦 VERDURAS:")
    for v, e in [("Zanahoria","🥕"),("Brócoli","🥦"),("Tomate","🍅"),("Lechuga","🥬"),
                 ("Maíz","🌽"),("Pepino","🥒"),("Cebolla","🧅"),("Papa","🥔")]:
        print(f"   {e} {v}")
    dar_estrellas(2)

@comando("transportes", N("transportes","transports"), es="Los transportes", en="Transports")
def c(a):
    print("🚗 TRANSPORTES:")
    for t, e in [("Coche","🚗"),("Autobús","🚌"),("Tren","🚆"),("Avión","✈️"),
                 ("Barco","🚢"),("Bicicleta","🚲"),("Moto","🏍️"),("Cohete","🚀")]:
        print(f"   {e} {t}")
    dar_estrellas(2)

@comando("opuestos", N("opuestos","opposites"), es="Palabras opuestas", en="Opposite words")
def c(a):
    print("↔️  OPUESTOS:")
    for p1, p2 in [("Grande","Pequeño"),("Alto","Bajo"),("Fr\u00edo","Caliente"),
                    ("Día","Noche"),("Rápido","Lento"),("Feliz","Triste")]:
        print(f"   {p1} ↔ {p2}")
    dar_estrellas(2)

# ============================================================
# ⚙️ OTROS (5)
# ============================================================
CATEGORIAS = {
 "👋 Amistad": ["hola","adios","como_estas","animo","nombre","abrazo","quien_eres","yo_soy",
                "gracias","eres_mi_mejor_amigo","beso","high_five","saludo_secreto","cosquillas"],
 "⭐ Estrellas": ["estrellas","insignias","premios","reiniciar_estrellas","nivel","record","deseo"],
 "🔢 Mate": ["suma","resta","mult","div","doble","triple","mitad","par","impar","tabla","contar",
             "cuanto_es","cuadrado_numero","cubo_numero","comparar","contar_2","contar_5","contar_10",
             "sumar_hasta","adivina_operacion"],
 "📝 Letras": ["mayusculas","minusculas","al_reves","contar_letras","vocales","primera_letra",
               "ultima_letra","deletrear","palindromo","adivinanza_palabra","espejo","contar_palabras",
               "silabas","rimas","palabra_larga"],
 "🐾 Animales": ["animales","sonido_animal","animal_aleatorio","donde_vive","patas","bebe_animal",
                 "adivina_animal","animal_favorito","tiburon","pinguino","delfin","mariposa","tortuga",
                 "abeja","conejo","zorro","oso","panda","jirafa","buho"],
 "🎨 Colores": ["arcoiris","semaforo","color_aleatorio","mezcla","formas","lados","color_favorito","pintura"],
 "🎮 Juegos": ["dado","moneda","cara_o_cruz","piedra_papel","adivina_numero","veo_veo","chiste",
               "adivinanza","verdad_reto","simon","ruleta_kids","memoria","ahorcado","tesoro",
               "laberinto","sopa_letras","pictionary","memoria_numeros","gestos","escondite",
               "chiste2","adivinanza2","sorpresa"],
 "✏️ Lienzo ASCII": ["lienzo","tamano_lienzo","pintar","pincel","texto_ascii","linea",
                      "rectangulo_ascii","circulo_ascii","rellenar_ascii","simetria_ascii",
                      "borrar_lienzo","ver_portada","exportar_ascii","ayuda_lienzo"],
 "📖 Cuentos": ["cuento","poema","cancion","felicidades","fabula","trabalenguas","refran",
                "chiste_largo","mini_cuento","poema_amor"],
 "🌟 Aprender": ["dia_hoy","estacion","planetas","ingles","dias_semana","meses","abecedario",
                 "numeros_ingles","colores_ingles","cuerpo_humano","frutas","verduras",
                 "transportes","opuestos"],
 "⚙️ Otros": ["idioma","ayuda","salir","limpiar","creditos"],
}

@comando("ayuda", N("ayuda","help"), es="Muestra todos los comandos", en="Show all commands")
def c(a):
    print(f"{CYAN}{t('ayuda_titulo', n=len(COMANDOS))}{RESET}")
    for cat, cmds in CATEGORIAS.items():
        print(f"\n  {YELLOW}{cat}{RESET}")
        for k in cmds:
            if k in COMANDOS:
                d = COMANDOS[k]["desc"].get(STATE["lang"]) or COMANDOS[k]["desc"].get("es","")
                print(f"    {GREEN}{nom_act(k):<24}{RESET} {GRAY}{d}{RESET}")

@comando("idioma", N("idioma","language"), es="Cambia idioma: idioma en", en="Change language: language en")
def c(a):
    if not a: print(f"Idiomas: {', '.join(IDIOMAS)}"); return
    if a[0].lower() in IDIOMAS:
        STATE["lang"] = a[0].lower(); print(t("idioma_ok"))
    else: print(f"Prueba: {', '.join(IDIOMAS)}")

@comando("limpiar", N("limpiar","clear"), es="Limpia la pantalla", en="Clear screen")
def c(a): cls()

@comando("salir", N("salir","exit"), es="Salir", en="Exit")
def c(a): STATE["running"] = False

@comando("creditos", N("creditos","credits"), es="Créditos", en="Credits")
def c(a):
    print("🎨 davidconsole KIDS v2.0 CLI — Hecho con ❤️  en Python")
    print(f"   ¡Gracias por jugar, {STATE['nombre']}! 🌟")

build_index()

# ============================================================
# BANNER
# ============================================================
def banner():
    print(f"{BLUE}{'═' * 70}{RESET}")
    print(f"{ORANGE if 'ORANGE' in dir() else YELLOW}{BOLD}    ██████╗  █████╗ ██╗   ██╗██╗██████╗ {RESET}")
    print(f"{YELLOW}{BOLD}    ██╔══██╗██╔══██╗██║   ██║██║██╔══██╗{RESET}")
    print(f"{GREEN}{BOLD}    ██║  ██║███████║██║   ██║██║██║  ██║{RESET}")
    print(f"{GREEN}{BOLD}    ██║  ██║██╔══██║╚██╗ ██╔╝██║██║  ██║{RESET}")
    print(f"{CYAN}{BOLD}    ██████╔╝██║  ██║ ╚████╔╝ ██║██████╔╝{RESET}")
    print(f"{CYAN}{BOLD}    ╚═════╝ ╚═╝  ╚═╝  ╚═══╝  ╚═╝╚═════╝ {RESET}")
    print(f"{WHITE}{BOLD}              {PINK}kids{RESET}  {GRAY}v2.0 CLI{RESET}")
    print(f"{BLUE}{'═' * 70}{RESET}")
    print(f"{GRAY}                Hecho con ❤️  en Python 🐍{RESET}")
    print()

# ============================================================
# BUCLE PRINCIPAL
# ============================================================
def execute(linea):
    linea = linea.strip()
    if not linea: return
    partes = linea.split()
    nombre = partes[0]
    args = partes[1:]
    canonical = resolver(nombre)
    if canonical is None:
        print(f"{RED}{t('desconocido', cmd=nombre)}{RESET}"); return
    try:
        COMANDOS[canonical]["fn"](args)
    except Exception as e:
        print(f"{RED}{t('error', msg=str(e))}{RESET}")

def main():
    cls()
    banner()
    print(f"{GREEN}{t('bienvenida')}{RESET}")
    print(f"{GRAY}Total: {len(COMANDOS)} comandos | Idioma: {IDIOMAS[STATE['lang']]}{RESET}")
    print(f"{GRAY}Escribe '{nom_act('ayuda')}' o '{nom_act('ayuda_lienzo')}' para empezar.{RESET}\n")

    while STATE["running"]:
        prompt = (f"{WHITE}[{STATE['nombre']}]{RESET} "
                  f"{CYAN}[{STATE['lang']}]{RESET} "
                  f"{WHITE}>{RESET} ")
        try:
            linea = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print(); break
        if not linea.strip(): continue
        STATE["historial"].append(linea)
        execute(linea)

    print(f"{YELLOW}{t('adios')}{RESET}")

if __name__ == "__main__":
    main()
