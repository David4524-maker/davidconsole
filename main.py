#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
davidconsole v1.2 — 151 comandos multi-idioma con GUI.
Nuevo: comando especial 'url:' para abrir enlaces en el navegador.
Idiomas: es, en, fr, de, pt, it
"""

import tkinter as tk
import os, sys, math, random, datetime, platform, time, socket, webbrowser, re
import hashlib, base64, uuid, shlex
from collections import Counter

# ============================================================
# ESTADO GLOBAL
# ============================================================
STATE = {"lang": "es", "historial": [], "alias": {}, "running": True}

IDIOMAS = {"es": "Español", "en": "English", "fr": "Français",
           "de": "Deutsch", "pt": "Português", "it": "Italiano"}

T = {
 "es": {"bienvenida": "/davidconsole 1.2/ escribe \"ayuda\" para ver todos los comandos disponibles",
        "desconocido": "Comando desconocido: '{cmd}'. Prueba con 'ayuda'.",
        "idioma_ok": "Idioma cambiado a {lang}. Los comandos ahora están en {lang}.",
        "idioma_bad": "Idioma no soportado. Disponibles: {langs}",
        "adios": "¡Hasta pronto!", "faltan_args": "Faltan argumentos. Uso: {uso}",
        "error": "Error: {msg}", "ayuda_titulo": "Comandos disponibles ({n}):",
        "hecho": "Hecho.", "no_existe": "No existe: {x}", "si_existe": "Sí existe: {x}",
        "hola": "¡Hola! ¿En qué puedo ayudarte?",
        "gracias": "¡De nada! Siempre a tu servicio.",
        "sobre": "davidconsole v1.2 — Terminal de 151 comandos multi-idioma. Hecho en Python.",
        "quien": "Soy davidconsole, una terminal creada por David en Python. 151 comandos en 6 idiomas.",
        "url_abriendo": "🌐 Abriendo: {url}",
        "url_invalida": "URL inválida: {url}"},
 "en": {"bienvenida": "/davidconsole 1.2/ type \"help\" to see all available commands",
        "desconocido": "Unknown command: '{cmd}'. Try 'help'.",
        "idioma_ok": "Language changed to {lang}. Commands are now in {lang}.",
        "idioma_bad": "Unsupported language. Available: {langs}",
        "adios": "See you soon!", "faltan_args": "Missing arguments. Usage: {uso}",
        "error": "Error: {msg}", "ayuda_titulo": "Available commands ({n}):",
        "hecho": "Done.", "no_existe": "Does not exist: {x}", "si_existe": "Exists: {x}",
        "hola": "Hi! How can I help you?",
        "gracias": "You're welcome! Always at your service.",
        "sobre": "davidconsole v1.2 — 151-command multi-language terminal. Made in Python.",
        "quien": "I am davidconsole, a terminal created by David in Python. 151 commands in 6 languages.",
        "url_abriendo": "🌐 Opening: {url}",
        "url_invalida": "Invalid URL: {url}"},
 "fr": {"bienvenida": "/davidconsole 1.2/ tapez \"aide\" pour voir toutes les commandes",
        "desconocido": "Commande inconnue : '{cmd}'. Essayez 'aide'.",
        "idioma_ok": "Langue changée en {lang}. Les commandes sont maintenant en {lang}.",
        "idioma_bad": "Langue non supportée. Disponibles : {langs}",
        "adios": "À bientôt !", "faltan_args": "Arguments manquants. Usage : {uso}",
        "error": "Erreur : {msg}", "ayuda_titulo": "Commandes disponibles ({n}) :",
        "hecho": "Fait.", "no_existe": "N'existe pas : {x}", "si_existe": "Existe : {x}",
        "hola": "Salut ! Comment puis-je t'aider ?",
        "gracias": "De rien ! Toujours à ton service.",
        "sobre": "davidconsole v1.2 — Terminal multi-langue de 151 commandes. Fait en Python.",
        "quien": "Je suis davidconsole, un terminal créé par David en Python. 151 commandes en 6 langues.",
        "url_abriendo": "🌐 Ouverture : {url}",
        "url_invalida": "URL invalide : {url}"},
 "de": {"bienvenida": "/davidconsole 1.2/ tippe \"hilfe\" für alle Befehle",
        "desconocido": "Unbekannter Befehl: '{cmd}'. Versuche 'hilfe'.",
        "idioma_ok": "Sprache geändert zu {lang}. Befehle sind jetzt auf {lang}.",
        "idioma_bad": "Sprache nicht unterstützt. Verfügbar: {langs}",
        "adios": "Bis bald!", "faltan_args": "Argumente fehlen. Nutzung: {uso}",
        "error": "Fehler: {msg}", "ayuda_titulo": "Verfügbare Befehle ({n}):",
        "hecho": "Fertig.", "no_existe": "Existiert nicht: {x}", "si_existe": "Existiert: {x}",
        "hola": "Hallo! Wie kann ich dir helfen?",
        "gracias": "Gern geschehen! Immer zu Diensten.",
        "sobre": "davidconsole v1.2 — 151-Befehl Multi-Sprache Terminal. In Python gemacht.",
        "quien": "Ich bin davidconsole, ein von David in Python erstelltes Terminal. 151 Befehle in 6 Sprachen.",
        "url_abriendo": "🌐 Öffne: {url}",
        "url_invalida": "Ungültige URL: {url}"},
 "pt": {"bienvenida": "/davidconsole 1.2/ digite \"ajuda\" para ver todos os comandos",
        "desconocido": "Comando desconhecido: '{cmd}'. Tente 'ajuda'.",
        "idioma_ok": "Idioma alterado para {lang}. Comandos agora em {lang}.",
        "idioma_bad": "Idioma não suportado. Disponíveis: {langs}",
        "adios": "Até logo!", "faltan_args": "Faltam argumentos. Uso: {uso}",
        "error": "Erro: {msg}", "ayuda_titulo": "Comandos disponíveis ({n}):",
        "hecho": "Feito.", "no_existe": "Não existe: {x}", "si_existe": "Existe: {x}",
        "hola": "Olá! Como posso ajudar?",
        "gracias": "De nada! Sempre ao seu dispor.",
        "sobre": "davidconsole v1.2 — Terminal multi-idioma de 151 comandos. Feito em Python.",
        "quien": "Sou davidconsole, um terminal criado por David em Python. 151 comandos em 6 idiomas.",
        "url_abriendo": "🌐 Abrindo: {url}",
        "url_invalida": "URL inválida: {url}"},
 "it": {"bienvenida": "/davidconsole 1.2/ digita \"aiuto\" per tutti i comandi",
        "desconocido": "Comando sconosciuto: '{cmd}'. Prova 'aiuto'.",
        "idioma_ok": "Lingua cambiata in {lang}. Comandi ora in {lang}.",
        "idioma_bad": "Lingua non supportata. Disponibili: {langs}",
        "adios": "A presto!", "faltan_args": "Argomenti mancanti. Uso: {uso}",
        "error": "Errore: {msg}", "ayuda_titulo": "Comandi disponibili ({n}):",
        "hecho": "Fatto.", "no_existe": "Non esiste: {x}", "si_existe": "Esiste: {x}",
        "hola": "Ciao! Come posso aiutarti?",
        "gracias": "Prego! Sempre al tuo servizio.",
        "sobre": "davidconsole v1.2 — Terminal multi-lingua da 151 comandi. Fatto in Python.",
        "quien": "Sono davidconsole, un terminale creato da David in Python. 151 comandi in 6 lingue.",
        "url_abriendo": "🌐 Apertura: {url}",
        "url_invalida": "URL non valida: {url}"},
}

def t(k, **kw):
    txt = T.get(STATE["lang"], T["es"]).get(k) or T["es"].get(k, k)
    return txt.format(**kw) if kw else txt

# ============================================================
# REGISTRO DE COMANDOS MULTI-IDIOMA
# ============================================================
COMANDOS = {}
INDICE = {}

def N(es, en=None, fr=None, de=None, pt=None, it=None):
    """Construye el diccionario de nombres por idioma."""
    d = {"es": es}
    if en: d["en"] = en
    if fr: d["fr"] = fr
    if de: d["de"] = de
    if pt: d["pt"] = pt
    if it: d["it"] = it
    return d

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

def resolver(nombre):
    """Busca el ID canónico de un comando por su nombre, priorizando el idioma activo."""
    n = nombre.lower()
    for lang in (STATE["lang"], "es", "en"):
        if n in INDICE.get(lang, {}):
            return INDICE[lang][n]
    for m in INDICE.values():
        if n in m: return m[n]
    return None

def nombre_actual(canonical):
    info = COMANDOS[canonical]
    return info["names"].get(STATE["lang"]) or info["names"].get("es", canonical)

# ============================================================
# 1-10 · TERMINAL
# ============================================================
@comando("ayuda", N("ayuda","help","aide","hilfe","ajuda","aiuto"),
         es="Lista todos los comandos", en="List all commands")
def c_ayuda(a):
    print(t("ayuda_titulo", n=len(COMANDOS)))
    for k in sorted(COMANDOS):
        nm = nombre_actual(k)
        d = COMANDOS[k]["desc"].get(STATE["lang"]) or COMANDOS[k]["desc"].get("es", "")
        print(f"  {nm:<22} {d}")

@comando("salir", N("salir","exit","quitter","beenden","sair","esci"),
         es="Sale de la terminal", en="Exit the terminal")
def c_salir(a): STATE["running"] = False

@comando("limpiar", N("limpiar","clear","effacer","leeren","limpar","pulisci"),
         es="Limpia la pantalla", en="Clear the screen")
def c_limpiar(a): print("\n" * 60)

@comando("historial", N("historial","history","historique","verlauf","historico","cronologia"),
         es="Historial de comandos", en="Command history")
def c_hist(a):
    for i, h in enumerate(STATE["historial"], 1): print(f"  {i:>3}  {h}")

@comando("repetir", N("repetir","repeat","repeter","wiederholen","repetir","ripeti"),
         es="Repite el último comando N veces", en="Repeat last command N times")
def c_rep(a):
    if not a: print(t("faltan_args", uso=f"{nombre_actual('repetir')} N")); return
    if len(STATE["historial"]) < 2: print(t("error", msg="sin comando previo")); return
    last = STATE["historial"][-2]
    for _ in range(int(a[0])):
        p = shlex.split(last)
        if p and resolver(p[0]): COMANDOS[resolver(p[0])]["fn"](p[1:])

@comando("alias", N("alias","alias","alias","alias","alias","alias"),
         es="Crea un alias: alias nombre comando", en="Create alias: alias name command")
def c_alias(a):
    if len(a) < 2: print(t("faltan_args", uso="alias nombre comando...")); return
    STATE["alias"][a[0]] = " ".join(a[1:]); print(t("hecho"))

@comando("version", N("version","version","version","version","versao","versione"),
         es="Muestra la versión", en="Show version")
def c_version(a): print("davidconsole 1.2 — Python", sys.version.split()[0])

@comando("hola", N("hola","hi","salut","hallo","ola","ciao"),
         es="Saludo amistoso", en="Friendly greeting")
def c_hola(a): print(t("hola"))

@comando("gracias", N("gracias","thanks","merci","danke","obrigado","grazie"),
         es="Agradecimiento", en="Thanks")
def c_gracias(a): print(t("gracias"))

@comando("quien_eres", N("quien_eres","who_are_you","qui_es_tu","wer_bist_du","quem_e_voce","chi_sei"),
         es="Sobre davidconsole", en="About davidconsole")
def c_quien(a): print(t("quien"))

# ============================================================
# 11-15 · IDIOMA
# ============================================================
@comando("idioma", N("idioma","language","langue","sprache","idioma","lingua"),
         es="Cambia el idioma: idioma [es|en|fr|de|pt|it]", en="Change language: language [code]")
def c_idioma(a):
    if not a: print(t("idioma_bad", langs=", ".join(IDIOMAS))); return
    code = a[0].lower()
    if code in IDIOMAS:
        STATE["lang"] = code
        print(t("idioma_ok", lang=IDIOMAS[code]))
    else:
        print(t("idioma_bad", langs=", ".join(IDIOMAS)))

@comando("idiomas", N("idiomas","languages","langues","sprachen","idiomas","lingue"),
         es="Lista los idiomas disponibles", en="List available languages")
def c_idiomas(a):
    for k, v in IDIOMAS.items(): print(f"  {k}  {v}")

@comando("traduccion", N("traduccion","translation","traduction","ubersetzung","traducao","traduzione"),
         es="Traduce una clave: traduccion clave", en="Translate a key: translation key")
def c_trad(a):
    if not a: print(t("faltan_args", uso=f"{nombre_actual('traduccion')} clave")); return
    print(t(a[0]))

@comando("reiniciar", N("reiniciar","reset","reinitialiser","zurucksetzen","reiniciar","riavvia"),
         es="Reinicia el estado (historial y alias)", en="Reset state (history and aliases)")
def c_reiniciar(a):
    STATE["historial"].clear(); STATE["alias"].clear()
    print(t("hecho"))

@comando("sobre", N("sobre","about","a_propos","uber","sobre","informazioni"),
         es="Acerca de davidconsole", en="About davidconsole")
def c_sobre(a): print(t("sobre"))

# ============================================================
# 16-30 · SISTEMA
# ============================================================
@comando("info", N("info","info","infos","info","info","info"),
         es="Información general del sistema", en="General system info")
def c_info(a):
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"CWD: {os.getcwd()}")

@comando("sistema", N("sistema","system","systeme","system","sistema","sistema"),
         es="Sistema operativo", en="Operating system")
def c_sis(a): print(platform.system(), platform.release())

@comando("usuario", N("usuario","user","utilisateur","benutzer","usuario","utente"),
         es="Usuario actual", en="Current user")
def c_user(a):
    try: print(os.getlogin())
    except Exception: print(os.environ.get("USERNAME") or os.environ.get("USER") or "?")

@comando("hostname", N("hostname","hostname","nom_hote","hostname","hostname","hostname"),
         es="Nombre del host", en="Host name")
def c_host(a): print(platform.node())

@comando("plataforma", N("plataforma","platform","plateforme","plattform","plataforma","piattaforma"),
         es="Plataforma completa", en="Full platform")
def c_plat(a): print(platform.platform())

@comando("python", N("python","python","python","python","python","python"),
         es="Versión de Python", en="Python version")
def c_py(a): print(sys.version)

@comando("cwd", N("cwd","cwd","cwd","cwd","cwd","cwd"),
         es="Directorio de trabajo actual", en="Current working directory")
def c_cwd(a): print(os.getcwd())

@comando("hora", N("hora","time","heure","zeit","hora","ora"),
         es="Hora actual", en="Current time")
def c_hora(a): print(datetime.datetime.now().strftime("%H:%M:%S"))

@comando("fecha", N("fecha","date","date","datum","data","data"),
         es="Fecha actual", en="Current date")
def c_fecha(a): print(datetime.datetime.now().strftime("%Y-%m-%d"))

@comando("fecha_hora", N("fecha_hora","datetime","date_heure","datum_zeit","data_hora","data_ora"),
         es="Fecha y hora completas", en="Full date and time")
def c_fh(a): print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@comando("uptime", N("uptime","uptime","uptime","uptime","uptime","uptime"),
         es="Tiempo del proceso", en="Process uptime")
def c_uptime(a):
    if "_start" not in STATE: STATE["_start"] = time.time()
    print(f"{time.time() - STATE['_start']:.1f}s")

@comando("memoria", N("memoria","memory","memoire","speicher","memoria","memoria"),
         es="Información de memoria", en="Memory info")
def c_mem(a):
    try:
        import psutil; m = psutil.virtual_memory()
        print(f"Total: {m.total//(1024**2)} MB  Libre: {m.available//(1024**2)} MB")
    except ImportError: print("psutil no instalado (pip install psutil)")

@comando("cpu", N("cpu","cpu","cpu","cpu","cpu","cpu"),
         es="Número de núcleos", en="CPU core count")
def c_cpu(a): print("Cores:", os.cpu_count())

@comando("entorno", N("entorno","env","environnement","umgebung","ambiente","ambiente"),
         es="Variables de entorno (20)", en="Env variables (20)")
def c_env(a):
    for k in sorted(os.environ)[:20]: print(f"  {k}={os.environ[k][:60]}")

@comando("timestamp", N("timestamp","timestamp","horodatage","zeitstempel","timestamp","timestamp"),
         es="Marca de tiempo Unix", en="Unix timestamp")
def c_ts(a): print(int(time.time()))

# ============================================================
# 31-50 · ARCHIVOS
# ============================================================
@comando("ls", N("ls","ls","ls","ls","ls","ls"),
         es="Lista archivos del directorio", en="List files")
def c_ls(a):
    ruta = a[0] if a else "."
    for x in sorted(os.listdir(ruta)): print("  " + x)

@comando("listar", N("listar","list","lister","auflisten","listar","elenca"),
         es="Alias de ls", en="List files (alias)")
def c_listar(a): c_ls(a)

@comando("cd", N("cd","cd","cd","cd","cd","cd"),
         es="Cambia directorio: cd ruta", en="Change directory: cd path")
def c_cd(a):
    if not a: print(t("faltan_args", uso="cd ruta")); return
    os.chdir(a[0]); print(os.getcwd())

@comando("cat", N("cat","cat","cat","cat","cat","cat"),
         es="Muestra el contenido de un archivo", en="Show file contents")
def c_cat(a):
    if not a: print(t("faltan_args", uso="cat archivo")); return
    with open(a[0], encoding="utf-8", errors="replace") as f: print(f.read())

@comando("mkdir", N("mkdir","mkdir","mkdir","mkdir","mkdir","mkdir"),
         es="Crea un directorio", en="Create directory")
def c_mkdir(a):
    if not a: print(t("faltan_args", uso="mkdir nombre")); return
    os.makedirs(a[0], exist_ok=True); print(t("hecho"))

@comando("rmdir", N("rmdir","rmdir","rmdir","rmdir","rmdir","rmdir"),
         es="Elimina un directorio vacío", en="Remove empty directory")
def c_rmdir(a):
    if not a: print(t("faltan_args", uso="rmdir nombre")); return
    os.rmdir(a[0]); print(t("hecho"))

@comando("rm", N("rm","rm","rm","rm","rm","rm"),
         es="Elimina un archivo", en="Delete a file")
def c_rm(a):
    if not a: print(t("faltan_args", uso="rm archivo")); return
    os.remove(a[0]); print(t("hecho"))

@comando("touch", N("touch","touch","touch","touch","touch","touch"),
         es="Crea un archivo vacío", en="Create empty file")
def c_touch(a):
    if not a: print(t("faltan_args", uso="touch archivo")); return
    open(a[0], "a").close(); print(t("hecho"))

@comando("cp", N("cp","cp","cp","cp","cp","cp"),
         es="Copia: cp origen destino", en="Copy: cp src dst")
def c_cp(a):
    if len(a) < 2: print(t("faltan_args", uso="cp origen destino")); return
    import shutil; shutil.copy2(a[0], a[1]); print(t("hecho"))

@comando("mv", N("mv","mv","mv","mv","mv","mv"),
         es="Mueve/renombra: mv origen destino", en="Move/rename: mv src dst")
def c_mv(a):
    if len(a) < 2: print(t("faltan_args", uso="mv origen destino")); return
    import shutil; shutil.move(a[0], a[1]); print(t("hecho"))

@comando("existe", N("existe","exists","existe","existiert","existe","esiste"),
         es="Comprueba si existe: existe ruta", en="Check existence: exists path")
def c_existe(a):
    if not a: print(t("faltan_args", uso=f"{nombre_actual('existe')} ruta")); return
    print(t("si_existe", x=a[0]) if os.path.exists(a[0]) else t("no_existe", x=a[0]))

@comando("tamanio", N("tamanio","size","taille","grosse","tamanho","dimensione"),
         es="Tamaño de un archivo en bytes", en="File size in bytes")
def c_tam(a):
    if not a: print(t("faltan_args", uso=f"{nombre_actual('tamanio')} archivo")); return
    print(os.path.getsize(a[0]), "bytes")

@comando("escribir", N("escribir","write","ecrire","schreiben","escrever","scrivi"),
         es="Escribe texto en archivo", en="Write text to file")
def c_escribir(a):
    if len(a) < 2: print(t("faltan_args", uso=f"{nombre_actual('escribir')} archivo texto...")); return
    with open(a[0], "w", encoding="utf-8") as f: f.write(" ".join(a[1:]))
    print(t("hecho"))

@comando("append", N("append","append","ajouter","anhaengen","anexar","aggiungi"),
         es="Añade texto al final: append archivo texto...", en="Append text: append file text...")
def c_append(a):
    if len(a) < 2: print(t("faltan_args", uso="append archivo texto...")); return
    with open(a[0], "a", encoding="utf-8") as f: f.write(" ".join(a[1:]) + "\n")
    print(t("hecho"))

@comando("buscar", N("buscar","find","chercher","finden","procurar","cerca"),
         es="Busca archivos por patrón", en="Find files by pattern")
def c_buscar(a):
    import glob
    for x in glob.glob(a[0] if a else "*")[:50]: print("  " + x)

@comando("arbol", N("arbol","tree","arbre","baum","arvore","albero"),
         es="Árbol del directorio (2 niveles)", en="Directory tree (2 levels)")
def c_arbol(a):
    r = a[0] if a else "."
    for root, dirs, files in os.walk(r):
        nivel = root.replace(r, "").count(os.sep)
        if nivel > 2: continue
        print("  " * nivel + os.path.basename(root) + "/")
        for f in files: print("  " * (nivel + 1) + f)

@comando("cabecera", N("cabecera","head","tete","kopf","cabeca","testa"),
         es="Primeras N líneas: cabecera archivo N", en="First N lines: head file N")
def c_head(a):
    if not a: print(t("faltan_args", uso=f"{nombre_actual('cabecera')} archivo N")); return
    n = int(a[1]) if len(a) > 1 else 10
    with open(a[0], encoding="utf-8", errors="replace") as f:
        for i, l in enumerate(f):
            if i >= n: break
            print(l.rstrip())

@comando("cola", N("cola","tail","queue","schwanz","cauda","coda"),
         es="Últimas N líneas: cola archivo N", en="Last N lines: tail file N")
def c_tail(a):
    if not a: print(t("faltan_args", uso=f"{nombre_actual('cola')} archivo N")); return
    n = int(a[1]) if len(a) > 1 else 10
    with open(a[0], encoding="utf-8", errors="replace") as f:
        for l in f.readlines()[-n:]: print(l.rstrip())

@comando("archivos", N("archivos","files","fichiers","dateien","arquivos","file"),
         es="Cuenta archivos del directorio", en="Count files in directory")
def c_arch(a):
    r = a[0] if a else "."
    print(len([x for x in os.listdir(r) if os.path.isfile(os.path.join(r, x))]))

@comando("pausa", N("pausa","pause","pause","pause","pausa","pausa"),
         es="Pausa breve: pausa N", en="Brief pause: pause N")
def c_pausa(a): time.sleep(float(a[0]) if a else 1); print(t("hecho"))

# ============================================================
# 51-70 · MATEMÁTICAS
# ============================================================
def _n(a, n=2): return [float(x) for x in a[:n]]

@comando("suma", N("suma","sum","somme","summe","soma","somma"),
         es="Suma: suma a b c...", en="Sum: sum a b c...")
def c_suma(a): print(sum(_n(a, len(a))))

@comando("resta", N("resta","subtract","soustraction","subtraktion","subtracao","sottrazione"),
         es="Resta: resta a b", en="Subtract: subtract a b")
def c_resta(a): n = _n(a); print(n[0] - n[1])

@comando("mult", N("mult","mult","mult","mult","mult","mult"),
         es="Multiplica: mult a b", en="Multiply: mult a b")
def c_mult(a): n = _n(a); print(n[0] * n[1])

@comando("div", N("div","div","div","div","div","div"),
         es="Divide: div a b", en="Divide: div a b")
def c_div(a): n = _n(a); print(n[0] / n[1])

@comando("potencia", N("potencia","power","puissance","potenz","potencia","potenza"),
         es="Potencia: potencia base exp", en="Power: power base exp")
def c_pot(a): n = _n(a); print(n[0] ** n[1])

@comando("raiz", N("raiz","sqrt","racine","wurzel","raiz","radice"),
         es="Raíz cuadrada: raiz x", en="Square root: sqrt x")
def c_raiz(a): print(math.sqrt(_n(a, 1)[0]))

@comando("modulo", N("modulo","modulo","modulo","modulo","modulo","modulo"),
         es="Módulo: modulo a b", en="Modulo: modulo a b")
def c_mod(a): n = _n(a); print(n[0] % n[1])

@comando("abs", N("abs","abs","abs","abs","abs","abs"),
         es="Valor absoluto: abs x", en="Absolute value: abs x")
def c_abs(a): print(abs(_n(a, 1)[0]))

@comando("redondeo", N("redondeo","round","arrondi","runden","arredondar","arrotonda"),
         es="Redondea: redondeo x", en="Round: round x")
def c_red(a): print(round(_n(a, 1)[0]))

@comando("techo", N("techo","ceil","plafond","decke","teto","soffitto"),
         es="Techo: techo x", en="Ceil: ceil x")
def c_techo(a): print(math.ceil(_n(a, 1)[0]))

@comando("piso", N("piso","floor","plancher","boden","chao","pavimento"),
         es="Piso: piso x", en="Floor: floor x")
def c_piso(a): print(math.floor(_n(a, 1)[0]))

@comando("seno", N("seno","sin","sinus","sinus","seno","seno"),
         es="Seno: seno x (radianes)", en="Sine: sin x (radians)")
def c_sin(a): print(math.sin(_n(a, 1)[0]))

@comando("coseno", N("coseno","cos","cosinus","cosinus","cosseno","coseno"),
         es="Coseno: coseno x", en="Cosine: cos x")
def c_cos(a): print(math.cos(_n(a, 1)[0]))

@comando("tangente", N("tangente","tan","tangente","tangens","tangente","tangente"),
         es="Tangente: tangente x", en="Tangent: tan x")
def c_tan(a): print(math.tan(_n(a, 1)[0]))

@comando("log", N("log","log","log","log","log","log"),
         es="Logaritmo natural: log x", en="Natural log: log x")
def c_log(a): print(math.log(_n(a, 1)[0]))

@comando("log10", N("log10","log10","log10","log10","log10","log10"),
         es="Logaritmo base 10: log10 x", en="Log base 10: log10 x")
def c_log10(a): print(math.log10(_n(a, 1)[0]))

@comando("exp", N("exp","exp","exp","exp","exp","exp"),
         es="Exponencial: exp x", en="Exponential: exp x")
def c_exp(a): print(math.exp(_n(a, 1)[0]))

@comando("factorial", N("factorial","factorial","factorielle","fakultaet","fatorial","fattoriale"),
         es="Factorial: factorial n", en="Factorial: factorial n")
def c_fact(a): print(math.factorial(int(_n(a, 1)[0])))

@comando("primo", N("primo","prime","premier","prim","primo","primo"),
         es="¿Es primo?: primo n", en="Is prime?: prime n")
def c_primo(a):
    n = int(_n(a, 1)[0])
    if n < 2: print(False); return
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: print(False); return
    print(True)

@comando("aleatorio", N("aleatorio","random","aleatoire","zufall","aleatorio","casuale"),
         es="Aleatorio: aleatorio min max", en="Random: random min max")
def c_rand(a):
    if len(a) < 2: print(random.random()); return
    print(random.randint(int(a[0]), int(a[1])))

# ============================================================
# 71-95 · TEXTO
# ============================================================
@comando("mayus", N("mayus","upper","majuscule","gross","maiuscula","maiuscola"),
         es="Mayúsculas: mayus texto...", en="Uppercase: upper text...")
def c_mayus(a): print(" ".join(a).upper())

@comando("minus", N("minus","lower","minuscule","klein","minuscula","minuscola"),
         es="Minúsculas: minus texto...", en="Lowercase: lower text...")
def c_minus(a): print(" ".join(a).lower())

@comando("titulo", N("titulo","title","titre","titel","titulo","titolo"),
         es="Formato título: titulo texto...", en="Title case: title text...")
def c_tit(a): print(" ".join(a).title())

@comando("invertir", N("invertir","reverse","inverser","umkehren","inverter","inverti"),
         es="Invierte el texto: invertir texto...", en="Reverse text: reverse text...")
def c_inv(a): print(" ".join(a)[::-1])

@comando("longitud", N("longitud","length","longueur","laenge","comprimento","lunghezza"),
         es="Longitud: longitud texto...", en="Length: length text...")
def c_len(a): print(len(" ".join(a)))

@comando("repetir_txt", N("repetir_txt","repeat_txt","repeter_txt","wiederholen_txt","repetir_txt","ripeti_txt"),
         es="Repite texto: repetir_txt texto N", en="Repeat text: repeat_txt text N")
def c_reptxt(a):
    if len(a) < 2: print(t("faltan_args", uso=f"{nombre_actual('repetir_txt')} texto N")); return
    print(" ".join(a[:-1]) * int(a[-1]))

@comando("reemplazar", N("reemplazar","replace","remplacer","ersetzen","substituir","sostituisci"),
         es="Reemplaza: reemplazar viejo nuevo texto...", en="Replace: replace old new text...")
def c_reempl(a):
    if len(a) < 3: print(t("faltan_args", uso=f"{nombre_actual('reemplazar')} viejo nuevo texto...")); return
    print(" ".join(a[2:]).replace(a[0], a[1]))

@comando("dividir", N("dividir","split","diviser","teilen","dividir","dividi"),
         es="Divide por separador: dividir , texto...", en="Split by sep: split , text...")
def c_divtxt(a):
    if len(a) < 2: print(t("faltan_args", uso=f"{nombre_actual('dividir')} sep texto...")); return
    print(" ".join(a[1:]).split(a[0]))

@comando("unir", N("unir","join","joindre","verbinden","unir","unisci"),
         es="Une: unir sep partes...", en="Join: join sep parts...")
def c_unir(a):
    if len(a) < 2: print(t("faltan_args", uso=f"{nombre_actual('unir')} sep partes...")); return
    print(a[0].join(a[1:]))

@comando("contiene", N("contiene","contains","contient","enthaelt","contem","contiene"),
         es="¿Contiene?: contiene texto sub", en="Contains?: contains text sub")
def c_cont(a):
    if len(a) < 2: print(t("faltan_args", uso=f"{nombre_actual('contiene')} texto sub")); return
    print(a[1] in a[0])

@comando("empezar", N("empezar","startswith","commence","beginnt","comeca","inizia"),
         es="¿Empieza con?: empezar texto prefijo", en="Starts with?: startswith text prefix")
def c_emp(a):
    if len(a) < 2: print(t("faltan_args", uso=f"{nombre_actual('empezar')} texto prefijo")); return
    print(a[0].startswith(a[1]))

@comando("terminar", N("terminar","endswith","finit","endet","termina","finisce"),
         es="¿Termina con?: terminar texto sufijo", en="Ends with?: endswith text suffix")
def c_term(a):
    if len(a) < 2: print(t("faltan_args", uso=f"{nombre_actual('terminar')} texto sufijo")); return
    print(a[0].endswith(a[1]))

@comando("contar", N("contar","count","compter","zaehlen","contar","conta"),
         es="Cuenta ocurrencias: contar texto sub", en="Count occurrences: count text sub")
def c_contar(a):
    if len(a) < 2: print(t("faltan_args", uso=f"{nombre_actual('contar')} texto sub")); return
    print(a[0].count(a[1]))

@comando("indice", N("indice","index","indice","index","indice","indice"),
         es="Índice de: indice texto sub", en="Index of: index text sub")
def c_idx(a):
    if len(a) < 2: print(t("faltan_args", uso=f"{nombre_actual('indice')} texto sub")); return
    print(a[0].find(a[1]))

@comando("limpiar_txt", N("limpiar_txt","strip","depouiller","entfernen","limpar_txt","pulisci_txt"),
         es="Quita espacios extremos: limpiar_txt texto...", en="Strip text: strip text...")
def c_strip(a): print(" ".join(a).strip())

@comando("ascii", N("ascii","ascii","ascii","ascii","ascii","ascii"),
         es="Código ASCII: ascii A", en="ASCII code: ascii A")
def c_ascii(a): print(ord(a[0][0]))

@comando("char", N("char","char","char","char","char","char"),
         es="Carácter por código: char 65", en="Char by code: char 65")
def c_char(a): print(chr(int(a[0])))

@comando("binario", N("binario","binary","binaire","binaer","binario","binario"),
         es="Decimal a binario: binario N", en="Decimal to binary: binary N")
def c_bin(a): print(bin(int(a[0])))

@comando("hexa", N("hexa","hex","hexa","hex","hexa","hex"),
         es="Decimal a hex: hexa N", en="Decimal to hex: hex N")
def c_hex(a): print(hex(int(a[0])))

@comando("octal", N("octal","octal","octal","oktal","octal","ottale"),
         es="Decimal a octal: octal N", en="Decimal to octal: octal N")
def c_oct(a): print(oct(int(a[0])))

@comando("base64", N("base64","base64","base64","base64","base64","base64"),
         es="Codifica base64: base64 texto...", en="Base64 encode: base64 text...")
def c_b64(a): print(base64.b64encode(" ".join(a).encode()).decode())

@comando("md5", N("md5","md5","md5","md5","md5","md5"),
         es="Hash MD5: md5 texto...", en="MD5 hash: md5 text...")
def c_md5(a): print(hashlib.md5(" ".join(a).encode()).hexdigest())

@comando("sha256", N("sha256","sha256","sha256","sha256","sha256","sha256"),
         es="Hash SHA-256: sha256 texto...", en="SHA-256 hash: sha256 text...")
def c_sha(a): print(hashlib.sha256(" ".join(a).encode()).hexdigest())

@comando("uuid", N("uuid","uuid","uuid","uuid","uuid","uuid"),
         es="Genera UUID v4", en="Generate UUID v4")
def c_uuid(a): print(uuid.uuid4())

@comando("utc", N("utc","utc","utc","utc","utc","utc"),
         es="Hora UTC actual", en="Current UTC time")
def c_utc(a): print(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))

# ============================================================
# 96-115 · UTILIDADES
# ============================================================
@comando("eco", N("eco","echo","echo","echo","eco","echo"),
         es="Repite lo que escribas: eco texto...", en="Echo: echo text...")
def c_eco(a): print(" ".join(a))

@comando("dormir", N("dormir","sleep","dormir","schlafen","dormir","dormi"),
         es="Pausa N segundos: dormir 2", en="Sleep N seconds: sleep 2")
def c_dormir(a): time.sleep(float(a[0]) if a else 1); print(t("hecho"))

@comando("contar_letras", N("contar_letras","count_letters","compter_lettres","zaehle_buchstaben","contar_letras","conta_lettere"),
         es="Cuenta letras: contar_letras texto...", en="Count letters: count_letters text...")
def c_cl(a): print(Counter(" ".join(a).replace(" ", "")))

@comando("contar_palabras", N("contar_palabras","count_words","compter_mots","zaehle_woerter","contar_palavras","conta_parole"),
         es="Cuenta palabras: contar_palabras texto...", en="Count words: count_words text...")
def c_cp(a): print(len(" ".join(a).split()))

@comando("palindromo", N("palindromo","palindrome","palindrome","palindrom","palindromo","palindromo"),
         es="¿Es palíndromo?: palindromo texto", en="Is palindrome?: palindrome text")
def c_pal(a):
    s = "".join(a).lower().replace(" ", "")
    print(s == s[::-1])

@comando("reverso", N("reverso","reverse_args","inverse_args","umkehr_args","reverso","inverso"),
         es="Revierte argumentos: reverso a b c", en="Reverse args: reverse_args a b c")
def c_rev(a): print(" ".join(reversed(a)))

@comando("suma_digitos", N("suma_digitos","sum_digits","somme_chiffres","summe_ziffern","soma_digitos","somma_cifre"),
         es="Suma dígitos: suma_digitos 1234", en="Sum digits: sum_digits 1234")
def c_sd(a): print(sum(int(c) for c in a[0] if c.isdigit()))

@comando("par", N("par","even","pair","gerade","par","pari"),
         es="¿Es par?: par N", en="Is even?: even N")
def c_par(a): print(int(a[0]) % 2 == 0)

@comando("impar", N("impar","odd","impair","ungerade","impar","dispari"),
         es="¿Es impar?: impar N", en="Is odd?: odd N")
def c_impar(a): print(int(a[0]) % 2 == 1)

@comando("fibonacci", N("fibonacci","fibonacci","fibonacci","fibonacci","fibonacci","fibonacci"),
         es="N primeros Fibonacci: fibonacci N", en="First N Fibonacci: fibonacci N")
def c_fib(a):
    n = int(a[0]) if a else 10
    x, y = 0, 1
    for _ in range(n): print(x, end=" "); x, y = y, x + y
    print()

@comando("tabla", N("tabla","table","table","tabelle","tabela","tavola"),
         es="Tabla de multiplicar: tabla N", en="Multiplication table: table N")
def c_tabla(a):
    n = int(a[0])
    for i in range(1, 11): print(f"  {n} x {i} = {n * i}")

@comando("promedio", N("promedio","average","moyenne","durchschnitt","media","media"),
         es="Promedio: promedio 1 2 3", en="Average: average 1 2 3")
def c_prom(a):
    nums = [float(x) for x in a]; print(sum(nums) / len(nums))

@comando("maximo", N("maximo","max","max","max","maximo","massimo"),
         es="Máximo: maximo 1 2 3", en="Max: max 1 2 3")
def c_max(a): print(max(float(x) for x in a))

@comando("minimo", N("minimo","min","min","min","minimo","minimo"),
         es="Mínimo: minimo 1 2 3", en="Min: min 1 2 3")
def c_min(a): print(min(float(x) for x in a))

@comando("ordenar", N("ordenar","sort","trier","sortieren","ordenar","ordina"),
         es="Ordena: ordenar 3 1 2", en="Sort: sort 3 1 2")
def c_ord(a): print(sorted(a))

@comando("unicos", N("unicos","unique","uniques","eindeutig","unicos","unici"),
         es="Elementos únicos: unicos a b a", en="Unique: unique a b a")
def c_uni(a): print(sorted(set(a)))

@comando("lista_aleatoria", N("lista_aleatoria","shuffle","melanger","mischen","lista_aleatoria","mescola"),
         es="Lista aleatoria: lista_aleatoria 1 2 3", en="Shuffle list: shuffle 1 2 3")
def c_la(a): print(random.sample(a, len(a)))

@comando("contrasena", N("contrasena","password","motdepasse","passwort","senha","password"),
         es="Genera contraseña: contrasena N", en="Generate password: password N")
def c_pass(a):
    n = int(a[0]) if a else 16
    import string as st
    chars = st.ascii_letters + st.digits + "!@#$%^&*"
    print("".join(random.choice(chars) for _ in range(n)))

@comando("rango", N("rango","range","intervalle","bereich","intervalo","intervallo"),
         es="Rango: rango inicio fin", en="Range: range start end")
def c_rango(a):
    ini, fin = int(a[0]), int(a[1]); print(list(range(ini, fin)))

@comando("ip_local", N("ip_local","local_ip","ip_locale","lokale_ip","ip_local","ip_locale"),
         es="Dirección IP local", en="Local IP address")
def c_ip(a):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)); ip = s.getsockname()[0]; s.close(); print(ip)
    except Exception as e: print(t("error", msg=str(e)))

# ============================================================
# 116-135 · ENTRETENIMIENTO
# ============================================================
@comando("dado", N("dado","dice","de","wurfel","dado","dado"),
         es="Tira un dado (6 caras)", en="Roll a die (6 sides)")
def c_dado(a): print(random.randint(1, int(a[0]) if a else 6))

@comando("moneda", N("moneda","coin","piece","munze","moeda","moneta"),
         es="Lanza una moneda", en="Flip a coin")
def c_mon(a): print(random.choice(["cara", "cruz"]))

@comando("ppt", N("ppt","rps","pfc","sss","ppt","pts"),
         es="Piedra papel tijera: ppt piedra", en="Rock paper scissors: rps rock")
def c_ppt(a):
    if not a: print(t("faltan_args", uso=f"{nombre_actual('ppt')} piedra|papel|tijera")); return
    yo = a[0].lower(); maq = random.choice(["piedra", "papel", "tijera"])
    print(f"Tú: {yo}  Máquina: {maq}")
    if yo == maq: print("Empate")
    elif (yo, maq) in [("piedra", "tijera"), ("papel", "piedra"), ("tijera", "papel")]:
        print("¡Ganaste!")
    else: print("Perdiste")

@comando("chiste", N("chiste","joke","blague","witz","piada","barzelletta"),
         es="Cuenta un chiste", en="Tell a joke")
def c_chiste(a):
    print(random.choice([
        "¿Por qué los programadores prefieren el modo oscuro? Porque la luz atrae bugs.",
        "Un byte entra a un bar... y pide 8 bits.",
        "¿Cuántos programadores se necesitan para cambiar una bombilla? Ninguno, es un problema de hardware."]))

@comando("frase", N("frase","quote","phrase","zitat","frase","frase"),
         es="Frase motivacional", en="Motivational quote")
def c_frase(a):
    print(random.choice(["El código es poesía.", "Primero hazlo funcionar, luego hazlo bonito.",
                         "La simplicidad es la máxima sofisticación.", "Sigue aprendiendo cada día."]))

@comando("dato", N("dato","fact","fait","fakt","fato","fatto"),
         es="Dato curioso", en="Fun fact")
def c_dato(a):
    print(random.choice(["Los pulpos tienen 3 corazones.", "El Sol contiene el 99% de la masa del sistema solar.",
                         "Python fue nombrado por Monty Python."]))

@comando("color", N("color","color","couleur","farbe","cor","colore"),
         es="Color HEX aleatorio", en="Random HEX color")
def c_color(a): print(f"#{random.randint(0, 0xFFFFFF):06X}")

@comando("emoji", N("emoji","emoji","emoji","emoji","emoji","emoji"),
         es="Emoji aleatorio", en="Random emoji")
def c_emoji(a): print(random.choice(["😀","🚀","🐍","🎉","⭐","💻","🌍","🔥","🍀","🎮"]))

@comando("arte", N("arte","art","art","kunst","arte","arte"),
         es="Arte ASCII", en="ASCII art")
def c_arte(a): print("\n    _____\n   /     \\\n  | () () |\n   \\  ^  /\n    |||||\n")

@comando("banner", N("banner","banner","banniere","banner","banner","banner"),
         es="Banner: banner texto...", en="Banner: banner text...")
def c_banner(a):
    txt = " ".join(a) if a else "davidconsole"
    print("*" * (len(txt) + 4)); print(f"* {txt} *"); print("*" * (len(txt) + 4))

@comando("cuenta_atras", N("cuenta_atras","countdown","compte_a_rebours","countdown","contagem","conto"),
         es="Cuenta atrás: cuenta_atras N", en="Countdown: countdown N")
def c_ca(a):
    for i in range(int(a[0]) if a else 5, 0, -1): print(i, end=" "); time.sleep(0.3)
    print("🚀")

@comando("temporizador", N("temporizador","timer","minuteur","timer","temporizador","timer"),
         es="Temporizador: temporizador N", en="Timer: timer N")
def c_temp(a):
    n = float(a[0]) if a else 5; time.sleep(n); print(f"⏰ Tiempo cumplido ({n}s)")

@comando("calendario", N("calendario","calendar","calendrier","kalender","calendario","calendario"),
         es="Calendario del mes actual", en="Calendar of current month")
def c_cal(a):
    import calendar
    print(calendar.month(datetime.date.today().year, datetime.date.today().month))

@comando("loteria", N("loteria","lottery","lotterie","lotterie","loteria","lotteria"),
         es="Números de lotería", en="Lottery numbers")
def c_lot(a): print(sorted(random.sample(range(1, 50), 6)))

@comando("bingo", N("bingo","bingo","bingo","bingo","bingo","bingo"),
         es="Cartón de bingo", en="Bingo card")
def c_bingo(a): print(sorted(random.sample(range(1, 91), 15)))

@comando("carta", N("carta","card","carte","karte","carta","carta"),
         es="Carta de la baraja", en="Playing card")
def c_carta(a):
    palos = ["♠","♥","♦","♣"]; valores = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    print(random.choice(valores) + random.choice(palos))

@comando("ruleta", N("ruleta","roulette","roulette","roulette","roleta","roulette"),
         es="Gira la ruleta (0-36)", en="Spin the roulette (0-36)")
def c_ruleta(a): print(random.randint(0, 36))

@comando("oraculo", N("oraculo","oracle","oracle","orakel","oraculo","oracolo"),
         es="El oráculo responde sí o no", en="Oracle answers yes/no")
def c_orac(a): print(random.choice(["Sí","No","Tal vez","Definitivamente","Ni lo sueñes"]))

@comando("magia", N("magia","magic","magie","magie","magia","magia"),
         es="Bola mágica: magia pregunta...", en="Magic 8-ball: magic question...")
def c_magia(a):
    print(random.choice(["Sin duda.","No cuentes con ello.","Pregunta más tarde.",
                         "Mis fuentes dicen que no.","Concéntrate y pregunta de nuevo."]))

@comando("suerte", N("suerte","lucky","chance","gluck","sorte","fortuna"),
         es="Número de la suerte", en="Lucky number")
def c_suerte(a): print(random.randint(1, 100))

# ============================================================
# 136-150 · CONVERSIÓN
# ============================================================
@comando("c_f", N("c_f","c_f","c_f","c_f","c_f","c_f"),
         es="Celsius a Fahrenheit: c_f 25", en="Celsius to Fahrenheit: c_f 25")
def c_cf(a): print(float(a[0]) * 9/5 + 32)

@comando("f_c", N("f_c","f_c","f_c","f_c","f_c","f_c"),
         es="Fahrenheit a Celsius: f_c 77", en="Fahrenheit to Celsius: f_c 77")
def c_fc(a): print((float(a[0]) - 32) * 5/9)

@comando("km_mi", N("km_mi","km_mi","km_mi","km_mi","km_mi","km_mi"),
         es="Kilómetros a millas: km_mi 10", en="Km to miles: km_mi 10")
def c_km_mi(a): print(float(a[0]) * 0.621371)

@comando("mi_km", N("mi_km","mi_km","mi_km","mi_km","mi_km","mi_km"),
         es="Millas a kilómetros: mi_km 10", en="Miles to km: mi_km 10")
def c_mi_km(a): print(float(a[0]) / 0.621371)

@comando("kg_lb", N("kg_lb","kg_lb","kg_lb","kg_lb","kg_lb","kg_lb"),
         es="Kilogramos a libras: kg_lb 5", en="Kg to pounds: kg_lb 5")
def c_kg_lb(a): print(float(a[0]) * 2.20462)

@comando("lb_kg", N("lb_kg","lb_kg","lb_kg","lb_kg","lb_kg","lb_kg"),
         es="Libras a kilogramos: lb_kg 5", en="Pounds to kg: lb_kg 5")
def c_lb_kg(a): print(float(a[0]) / 2.20462)

@comando("m_pie", N("m_pie","m_ft","m_pied","m_fuss","m_pe","m_piedi"),
         es="Metros a pies: m_pie 2", en="Meters to feet: m_ft 2")
def c_m_pie(a): print(float(a[0]) * 3.28084)

@comando("pie_m", N("pie_m","ft_m","pied_m","fuss_m","pe_m","piedi_m"),
         es="Pies a metros: pie_m 10", en="Feet to meters: ft_m 10")
def c_pie_m(a): print(float(a[0]) / 3.28084)

@comando("seg_hora", N("seg_hora","sec_hour","sec_heure","sek_stunde","seg_hora","sec_ora"),
         es="Segundos a horas: seg_hora 3600", en="Seconds to hours: sec_hour 3600")
def c_sh(a): print(float(a[0]) / 3600)

@comando("hora_seg", N("hora_seg","hour_sec","heure_sec","stunde_sek","hora_seg","ora_sec"),
         es="Horas a segundos: hora_seg 1", en="Hours to seconds: hour_sec 1")
def c_hs(a): print(float(a[0]) * 3600)

@comando("dec_bin", N("dec_bin","dec_bin","dec_bin","dec_bin","dec_bin","dec_bin"),
         es="Decimal a binario: dec_bin 10", en="Decimal to binary: dec_bin 10")
def c_db(a): print(bin(int(a[0]))[2:])

@comando("bin_dec", N("bin_dec","bin_dec","bin_dec","bin_dec","bin_dec","bin_dec"),
         es="Binario a decimal: bin_dec 1010", en="Binary to decimal: bin_dec 1010")
def c_bd(a): print(int(a[0], 2))

@comando("dec_hex", N("dec_hex","dec_hex","dec_hex","dec_hex","dec_hex","dec_hex"),
         es="Decimal a hex: dec_hex 255", en="Decimal to hex: dec_hex 255")
def c_dh(a): print(hex(int(a[0]))[2:].upper())

@comando("hex_dec", N("hex_dec","hex_dec","hex_dec","hex_dec","hex_dec","hex_dec"),
         es="Hex a decimal: hex_dec FF", en="Hex to decimal: hex_dec FF")
def c_hd(a): print(int(a[0], 16))

@comando("romano", N("romano","roman","romain","romisch","romano","romano"),
         es="Número a romano: romano 2024", en="Number to roman: roman 2024")
def c_rom(a):
    n = int(a[0])
    vals = [(1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),(100,"C"),(90,"XC"),
            (50,"L"),(40,"XL"),(10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I")]
    r = ""
    for v, s in vals:
        while n >= v: r += s; n -= v
    print(r)

# ============================================================
# 151 · COMANDO ESPECIAL "url:"
# ============================================================
@comando("url", N("url:", "url:", "url:", "url:", "url:", "url:"),
         es="Abre una URL en el navegador: url: https://...",
         en="Open a URL in the browser: url: https://...")
def c_url(a):
    if not a:
        print(t("faltan_args", uso="url: https://ejemplo.com"))
        return
    url = " ".join(a).strip()
    # Añadir https:// si no se especificó protocolo
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.\-]*://", url):
        url = "https://" + url
    try:
        webbrowser.open(url, new=2)
        print(t("url_abriendo", url=url))
    except Exception as e:
        print(t("error", msg=str(e)))

# Construir índice tras registrar todos los comandos
build_index()

# ============================================================
# INTERFAZ GRÁFICA
# ============================================================
PLACEHOLDER = "Ingresa tu comando..."

class DavidConsole:
    def __init__(self, root):
        self.root = root
        root.title("davidconsole 1.2")
        root.configure(bg="black")
        root.geometry("1000x600")
        root.minsize(600, 400)

        top = tk.Frame(root, bg="black")
        top.pack(fill="x", padx=15, pady=(15, 5))

        logo = tk.Canvas(top, width=170, height=76, bg="black", highlightthickness=0)
        logo.pack(side="right")
        logo.create_rectangle(2, 2, 168, 74, outline="#cccccc", width=3)
        logo.create_rectangle(10, 10, 160, 66, outline="#555555", width=2, fill="#666666")
        logo.create_text(38, 38, text=">", fill="white", font=("Arial", 30, "bold"))
        logo.create_text(105, 27, text="david", fill="#FF6600", font=("Arial", 13, "bold"))
        logo.create_text(105, 49, text="console", fill="#3399FF", font=("Arial", 13, "bold"))

        self.text = tk.Text(root, bg="black", fg="#00FF00", font=("Consolas", 12),
                            wrap="word", insertbackground="white", bd=0,
                            padx=15, pady=5, selectbackground="#333333",
                            highlightthickness=0)
        self.text.pack(fill="both", expand=True, padx=15)

        self.text.tag_configure("green", foreground="#00FF00")
        self.text.tag_configure("white", foreground="#ffffff")
        self.text.tag_configure("gray", foreground="#888888")
        self.text.tag_configure("orange", foreground="#FF6600")

        self.text.bind("<Return>", self.on_enter)
        self.text.bind("<Key>", self.on_key)
        self.text.bind("<BackSpace>", self.on_backspace)

        self.input_start_index = "1.0"
        self.placeholder_active = False

        bottom = tk.Frame(root, bg="black")
        bottom.pack(fill="x", padx=15, pady=(0, 10))
        tk.Label(bottom, text="Hecho en Python", bg="black", fg="white",
                 font=("Arial", 9, "bold")).pack(side="right")

        sys.stdout = self

        self._write_tag(t("bienvenida") + "\n\n", "green")
        self.new_prompt()
        self.text.focus_set()

    def write(self, s):
        if s: self._write_tag(s, "green")
    def flush(self): pass

    def _write_tag(self, s, tag):
        self.text.insert("end", s, tag); self.text.see("end"); self.text.update_idletasks()

    def new_prompt(self):
        etiqueta = f"[{STATE['lang']}] "
        self.text.insert("end", etiqueta, "orange")
        self.text.insert("end", "> ", "white")
        self.input_start_index = self.text.index("end-1c")
        self.text.insert("end", PLACEHOLDER, "gray")
        self.placeholder_active = True
        self.text.mark_set("insert", self.input_start_index)
        self.text.see("end")

    def remove_placeholder(self):
        if self.placeholder_active:
            self.text.delete(self.input_start_index, "end-1c")
            self.placeholder_active = False

    def on_key(self, event):
        if event.keysym in ("Shift_L","Shift_R","Control_L","Control_R","Alt_L","Alt_R",
                            "Caps_Lock","Escape","Tab","Return","KP_Enter"):
            return
        if event.keysym in ("Left","Up","Home","Prior"):
            if self.text.compare("insert", "<=", self.input_start_index):
                return "break"
        if self.placeholder_active and event.char:
            self.remove_placeholder()

    def on_backspace(self, event):
        if self.placeholder_active: return "break"
        if self.text.compare("insert", "<=", self.input_start_index): return "break"

    def on_enter(self, event):
        cmd = "" if self.placeholder_active else self.text.get(self.input_start_index, "end-1c")
        self.placeholder_active = False
        self.text.insert("end", "\n")
        cmd = cmd.strip()
        if cmd:
            STATE["historial"].append(cmd)
            self.execute(cmd)
        if STATE["running"]:
            self.new_prompt()
        else:
            self.root.after(400, self.root.destroy)
        return "break"

    def execute(self, linea):
        linea = linea.strip()

        # --- Caso especial: "url: algo" o "url:algo" ---
        m = re.match(r"^url\s*:\s*(.+)$", linea, re.IGNORECASE)
        if m:
            canonical = resolver("url:")
            if canonical:
                try:
                    COMANDOS[canonical]["fn"]([m.group(1).strip()])
                except Exception as e:
                    print(t("error", msg=str(e)))
            return

        # --- Caso normal ---
        try:
            partes = shlex.split(linea)
        except ValueError:
            partes = linea.split()
        if not partes:
            return
        nombre = partes[0]
        args = partes[1:]

        if nombre.lower() in STATE["alias"]:
            partes = shlex.split(STATE["alias"][nombre.lower()]) + args
            nombre = partes[0]
            args = partes[1:]

        canonical = resolver(nombre)
        if canonical is None:
            print(t("desconocido", cmd=nombre))
            return
        try:
            COMANDOS[canonical]["fn"](args)
        except Exception as e:
            print(t("error", msg=str(e)))


def main():
    root = tk.Tk()
    DavidConsole(root)
    root.mainloop()

if __name__ == "__main__":
    main()
