#  davidconsole v1.2

> Terminal gráfica con **151 comandos** y soporte **multi-idioma** (español, inglés, francés, alemán, portugués e italiano), escrita en Python puro con Tkinter.
> Hecho en Python  — sin dependencias externas obligatorias.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Estable-brightgreen)
![Commands](https://img.shields.io/badge/Commands-151-orange)
![Idiomas](https://img.shields.io/badge/Idiomas-6-purple)

---

##  Índice

1. [Descripción](#-descripción)
2. [Características](#-características)
3. [Captura de pantalla](#-captura-de-pantalla)
4. [Instalación de Python](#-instalación-de-python)
5. [Instalación de davidconsole](#-instalación-de-davidconsole)
6. [Uso](#-uso)
7. [Los 151 comandos](#-los-151-comandos)
8. [Multi-idioma](#-multi-idioma)
9. [Comando especial `url:`](#-comando-especial-url)
10. [Ejemplos prácticos](#-ejemplos-prácticos)
11. [Solución de problemas](#-solución-de-problemas)
12. [Personalización](#-personalización)
13. [Licencia](#-licencia)

---

##  Descripción

**davidconsole** es una terminal interactiva con interfaz gráfica construida con **Tkinter** (incluido en la biblioteca estándar de Python). Reproduce el aspecto clásico de una terminal (fondo negro, texto verde, prompt `>`) pero con un toque moderno: un logo *david console*, firma "Hecho en Python" y **soporte para 6 idiomas** que traduce tanto los mensajes como los **nombres de los comandos**.

No requiere instalar `pip` ni paquetes externos. Todo funciona con la biblioteca estándar de Python.

---

##  Características

- ✅ **151 comandos** organizados en 9 categorías.
- ✅ **6 idiomas**: español, inglés, francés, alemán, portugués, italiano.
- ✅ **Traducción dinámica**: cambia el idioma en caliente con `idioma [código]`.
- ✅ **Los nombres de los comandos cambian** con el idioma (`ayuda` ↔ `help` ↔ `aide` ↔ `hilfe`).
- ✅ **Fallback automático**: si escribes en otro idioma, se entiende igual.
- ✅ **Comando `url:`** para abrir páginas web en tu navegador.
- ✅ Interfaz **gráfica oscura** estilo terminal.
- ✅ **Historial** de comandos.
- ✅ **Alias** personalizables.
- ✅ Sin dependencias externas (todo es biblioteca estándar).

---

##  Captura de pantalla


<img width="991" height="597" alt="Captura de pantalla 2026-09-23 201116" src="https://github.com/user-attachments/assets/d910ae89-494f-4b82-a54e-b8e4d108d239" />


---

##  Instalación de Python

Si **no tienes Python instalado**, sigue los pasos según tu sistema operativo. Necesitas **Python 3.10 o superior** (recomendado 3.12+; idealmente 3.14 como usas en IDLE).

###  Windows

#### Opción A: Instalador oficial (recomendado)

1. Ve a la página oficial: **https://www.python.org/downloads/**
2. Haz clic en el botón grande **Download Python 3.14.x** (o la versión más reciente).
3. Ejecuta el instalador descargado (`.exe`).
4.  **MUY IMPORTANTE**: en la primera pantalla, marca la casilla **"Add python.exe to PATH"** antes de continuar.
5. Haz clic en **"Install Now"**.
6. Espera a que termine y haz clic en **"Close"**.

#### Verificar la instalación

Abre **Símbolo del sistema** (`Win + R` → escribe `cmd` → Enter) y escribe:

```bash
python --version
```

Debe mostrar algo como:

```
Python 3.14.0
```

Si en su lugar aparece la **Microsoft Store** o un error, revisa que hayas marcado *"Add python.exe to PATH"*. Si no, reinstala Python marcando esa opción.

#### Opción B: Microsoft Store

1. Abre **Microsoft Store**.
2. Busca **"Python 3.14"**.
3. Haz clic en **Instalar**.

>  La versión de la Store a veces no incluye `tkinter` completo. Si tienes problemas con la ventana gráfica, usa la Opción A.

---

###  macOS

#### Opción A: Instalador oficial

1. Ve a **https://www.python.org/downloads/macos/**
2. Descarga el instalador `.pkg` de la versión más reciente.
3. Ábrelo y sigue el asistente (siguiente → siguiente → instalar).
4. Introduce tu contraseña de administrador cuando lo pida.

#### Opción B: Homebrew (si ya usas Homebrew)

Abre **Terminal** y ejecuta:

```bash
brew install python@3.14
```

#### Verificar la instalación

Abre **Terminal** (`Cmd + Espacio` → escribe "Terminal") y ejecuta:

```bash
python3 --version
```

Debe mostrar `Python 3.14.x`.

>  En macOS el comando suele ser `python3`, no `python`.

---

###  Linux

#### Ubuntu / Debian / Linux Mint

Abre una terminal y ejecuta:

```bash
sudo apt update
sudo apt install python3 python3-tk python3-pip
```

#### Fedora / Red Hat

```bash
sudo dnf install python3 python3-tkinter
```

#### Arch Linux / Manjaro

```bash
sudo pacman -S python tk
```

#### Verificar la instalación

```bash
python3 --version
```

Debe mostrar `Python 3.x.x`.

>  En muchas distros, `tkinter` viene en un paquete aparte llamado `python3-tk` o `python3-tkinter`. **Instálalo**, porque davidconsole lo necesita.

---

###  Otros sistemas

| Sistema | Cómo instalar Python |
|---|---|
| **Android** | Instala [Pydroid 3](https://play.google.com/store/apps/details?id=ru.iiec.pydroid3) desde Play Store. |
| **iOS / iPadOS** | Instala [Pythonista](https://apps.apple.com/app/pythonista-3/id1085978097) (de pago). |
| **ChromeOS** | Activa Linux (Crostini) y sigue los pasos de Linux. |
| **Termux (Android)** | `pkg install python` (ojo: sin Tkinter, davidconsole no funcionará). |

---

##  Instalación de davidconsole

### Paso 1 — Descarga el archivo

Descarga o copia el archivo **`davidconsole.py`** a una carpeta, por ejemplo:

- Windows: `C:\Users\TuUsuario\davidconsole\`
- macOS/Linux: `~/davidconsole/`

### Paso 2 — Verifica que tienes Tkinter

Tkinter viene **incluido con Python en Windows y macOS**, pero en Linux a veces hay que instalarlo por separado (ver sección anterior).

Para comprobar que funciona, abre una terminal y ejecuta:

```bash
python -c "import tkinter; print('Tkinter OK')"
```

Debe imprimir `Tkinter OK`. Si da error en Linux, instala `python3-tk`.

### Paso 3 — No hay Paso 3 

**No necesitas instalar nada más.** davidconsole solo usa la biblioteca estándar.

---

##  Uso

### Método 1: Desde IDLE (recomendado para principiantes)

1. Abre **IDLE** (viene con Python).
2. `File` → `Open...` → selecciona `davidconsole.py`.
3. Presiona **`F5`** (o `Run` → `Run Module`).
4. Se abrirá la ventana gráfica de davidconsole.

### Método 2: Desde la terminal

Abre una terminal, navega a la carpeta donde está el archivo y ejecuta:

**Windows:**

```bash
python davidconsole.py
```

**macOS / Linux:**

```bash
python3 davidconsole.py
```

### Método 3: Doble clic (Windows)

Haz doble clic sobre `davidconsole.py`. Si no se abre, asegúrate de que los archivos `.py` estén asociados a Python.

---

##  Los 151 comandos

###  Terminal (10)

| Comando (es) | Descripción |
|---|---|
| `ayuda` | Lista todos los comandos |
| `salir` | Sale de la terminal |
| `limpiar` | Limpia la pantalla |
| `historial` | Muestra el historial |
| `repetir N` | Repite el último comando N veces |
| `alias n cmd` | Crea un alias |
| `version` | Versión de davidconsole |
| `hola` | Saludo |
| `gracias` | Agradecimiento |
| `quien_eres` | Información del programa |

###  Idioma (5)

| Comando | Descripción |
|---|---|
| `idioma [code]` | Cambia el idioma |
| `idiomas` | Lista idiomas disponibles |
| `traduccion clave` | Traduce una clave |
| `reiniciar` | Reinicia historial y alias |
| `sobre` | Acerca de davidconsole |

###  Sistema (15)

`info`, `sistema`, `usuario`, `hostname`, `plataforma`, `python`, `cwd`, `hora`, `fecha`, `fecha_hora`, `uptime`, `memoria`, `cpu`, `entorno`, `timestamp`

###  Archivos (20)

`ls`, `listar`, `cd`, `cat`, `mkdir`, `rmdir`, `rm`, `touch`, `cp`, `mv`, `existe`, `tamanio`, `escribir`, `append`, `buscar`, `arbol`, `cabecera`, `cola`, `archivos`, `pausa`

###  Matemáticas (20)

`suma`, `resta`, `mult`, `div`, `potencia`, `raiz`, `modulo`, `abs`, `redondeo`, `techo`, `piso`, `seno`, `coseno`, `tangente`, `log`, `log10`, `exp`, `factorial`, `primo`, `aleatorio`

###  Texto (25)

`mayus`, `minus`, `titulo`, `invertir`, `longitud`, `repetir_txt`, `reemplazar`, `dividir`, `unir`, `contiene`, `empezar`, `terminar`, `contar`, `indice`, `limpiar_txt`, `ascii`, `char`, `binario`, `hexa`, `octal`, `base64`, `md5`, `sha256`, `uuid`, `utc`

###  Utilidades (20)

`eco`, `dormir`, `contar_letras`, `contar_palabras`, `palindromo`, `reverso`, `suma_digitos`, `par`, `impar`, `fibonacci`, `tabla`, `promedio`, `maximo`, `minimo`, `ordenar`, `unicos`, `lista_aleatoria`, `contrasena`, `rango`, `ip_local`

###  Entretenimiento (20)

`dado`, `moneda`, `ppt`, `chiste`, `frase`, `dato`, `color`, `emoji`, `arte`, `banner`, `cuenta_atras`, `temporizador`, `calendario`, `loteria`, `bingo`, `carta`, `ruleta`, `oraculo`, `magia`, `suerte`

### 🔄 Conversión (15)

`c_f`, `f_c`, `km_mi`, `mi_km`, `kg_lb`, `lb_kg`, `m_pie`, `pie_m`, `seg_hora`, `hora_seg`, `dec_bin`, `bin_dec`, `dec_hex`, `hex_dec`, `romano`

###  Especial (1)

| Comando | Descripción |
|---|---|
| `url: https://...` | Abre una URL en el navegador predeterminado |

**Total: 151 comandos**

---

##  Multi-idioma

davidconsole soporta **6 idiomas**. Al cambiar de idioma, se traducen:

1. Los **mensajes del sistema** (bienvenida, errores, ayuda…).
2. Los **nombres de los 151 comandos**.

### Idiomas disponibles

| Código | Idioma    | Ejemplo: "help" se llama… |
|--------|-----------|---------------------------|
| `es`   | Español   | `ayuda`                   |
| `en`   | English   | `help`                    |
| `fr`   | Français  | `aide`                    |
| `de`   | Deutsch   | `hilfe`                   |
| `pt`   | Português | `ajuda`                   |
| `it`   | Italiano  | `aiuto`                   |

### Cambiar el idioma

```text
[es] > idioma en
Idioma cambiado a English. Los comandos ahora están en English.

[en] > help                # ahora 'ayuda' se llama 'help'
[en] > sum 3 4             # ahora 'suma' se llama 'sum'
[en] > time                # ahora 'hora' se llama 'time'
[en] > user                # ahora 'usuario' se llama 'user'
```

### Fallback

Si estás en inglés y escribes `suma` (en español), **también funciona**. El intérprete busca en el idioma activo, luego en español, luego en inglés.

---

##  Comando especial `url:`

El comando `url:` abre cualquier enlace en tu **navegador predeterminado** (Chrome, Firefox, Edge, Safari, Brave…).

### Sintaxis

```text
url: [espacio] URL
url:URL
url : URL
URL: URL       # también acepta mayúsculas
```

### Ejemplos

```text
[es] > url: google.com
🌐 Abriendo: https://google.com

[es] > url: https://github.com
🌐 Abriendo: https://github.com

[en] > url: python.org
🌐 Opening: https://python.org

[fr] > url: fr.wikipedia.org
🌐 Ouverture : https://fr.wikipedia.org
```

Si omites `http://` o `https://`, davidconsole **añade `https://` automáticamente**.

---

## 🧪 Ejemplos prácticos

```text
# Matemáticas
[es] > suma 10 20 30
60.0
[es] > raiz 144
12.0
[es] > factorial 10
3628800
[es] > romano 2024
MMXXIV

# Archivos
[es] > ls
[es] > mkdir pruebas
[es] > escribir notas.txt Hola davidconsole
[es] > cat notas.txt
Hola davidconsole

# Texto
[es] > mayus hola mundo
HOLA MUNDO
[es] > palindromo anita lava la tina
True
[es] > sha256 contraseña
...

# Entretenimiento
[es] > ppt piedra
Tú: piedra  Máquina: tijera
¡Ganaste!
[es] > contrasena 20
kA9#mP2$xLq7!vB3nR8w

# Sistema
[es] > hora
14:32:08
[es] > usuario
David
[es] > ip_local
192.168.1.42

# Web
[es] > url: youtube.com
🌐 Abriendo: https://youtube.com
```

---

## ❓ Solución de problemas

### Error: `ModuleNotFoundError: No module named 'tkinter'`

**Linux**: instala el paquete Tkinter según tu distro.

```bash
sudo apt install python3-tk        # Debian / Ubuntu
sudo dnf install python3-tkinter   # Fedora
sudo pacman -S tk                  # Arch
```

**Windows / macOS**: reinstala Python desde el instalador oficial y asegúrate de marcar **"tcl/tk and IDLE"** durante la instalación (viene marcado por defecto).

---

### La ventana se abre pero no responde a los comandos

Asegúrate de hacer clic **dentro del área de texto** (la zona negra). El foco debe estar en la caja de texto. Si no, presiona la tecla `Tab` o haz clic sobre ella.

---

### El comando `url:` no abre el navegador

- Verifica que el navegador predeterminado esté bien configurado en tu sistema.
- Prueba con `https://` explícito: `url: https://google.com`.
- En Linux sin entorno gráfico (servidores), `webbrowser` no funciona.

---

### `python: command not found` (macOS / Linux)

Usa `python3` en lugar de `python`:

```bash
python3 davidconsole.py
```

---

### `"python" no se reconoce como un comando` (Windows)

Olvidaste marcar **"Add python.exe to PATH"** durante la instalación. Soluciones:

1. Reinstala Python marcando esa casilla.
2. O usa la ruta completa, por ejemplo:
   ```bash
   C:\Users\TuUsuario\AppData\Local\Programs\Python\Python314\python.exe davidconsole.py
   ```

---

## 🎨 Personalización

### Cambiar los colores

Busca en `DavidConsole.__init__`:

```python
root.configure(bg="black")                        # fondo de la ventana
self.text = tk.Text(..., bg="black", fg="#00FF00")  # fondo y texto del área
```

Prueba con:

| Elemento | Valor |
|---|---|
| Fondo negro | `"#000000"` |
| Texto verde clásico | `"#00FF00"` |
| Texto ámbar (más retro) | `"#FFB000"` |
| Texto Matrix | `"#39FF14"` |
| Fondo azul oscuro | `"#0A0E27"` |

### Añadir un comando nuevo

```python
@comando("saludo", N("saludo","greet","saluer","grussen","cumprimento","saluto"),
         es="Saluda a alguien: saludo nombre", en="Greet someone: greet name")
def c_saludo(a):
    nombre = " ".join(a) if a else "mundo"
    print(f"¡Hola, {nombre}!")
```

### Añadir un idioma nuevo (ejemplo: japonés `ja`)

1. Añade `"ja": "日本語"` a `IDIOMAS`.
2. Añade una entrada `"ja": {...}` a `T` con las traducciones de los mensajes del sistema.
3. Añade el nombre japonés a cada `N(...)` de los comandos que quieras traducir. Los que no traduzcas caerán al español automáticamente.


```
MIT License

Copyright (c) 2026 David

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

##  Créditos

- **Autor:** David
- **Hecho en:** Python  + Tkinter
- **Versión:** 1.2
- **Última actualización:** 2026

---

<p align="center">
  <strong>Hecho en Python </strong><br>
  Si te gusta davidconsole, dale una ⭐ en GitHub.
</p>
