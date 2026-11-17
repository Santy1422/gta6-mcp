# Guía de instalación (español, paso a paso)

Para que Claude juegue en tu PS5 necesitas tres cosas en la misma red Wi-Fi/Ethernet:
tu **Mac/PC**, tu **PS5**, y tu **cuenta PSN**. Nada de USB: todo va por la red.

## 1. Preparar la PS5 (2 minutos, con el mando)

En la consola:

1. **Ajustes → Sistema → Uso a distancia** → activa **"Activar uso a distancia"**.
2. (Opcional pero recomendado) **Ajustes → Sistema → Ahorro de energía → Funciones disponibles en modo de reposo** → activa **"Seguir conectado a Internet"** y **"Permitir encender la PS5 desde la red"**. Con esto el MCP puede despertar la consola con `wake()`.
3. Apunta la **IP de la consola**: **Ajustes → Red → Estado de conexión → Ver estado de conexión** → `Dirección IPv4` (algo tipo `192.168.1.42`).

## 2. Instalar el servidor (1 comando)

En tu Mac/PC:

```bash
git clone https://github.com/Santy1422/gta6-mcp.git
cd gta6-mcp
./setup.sh
```

El script crea el entorno, instala todo y te deja escritos los pasos siguientes.

## 3. Vincular tu cuenta PSN (una sola vez)

Este es el único paso "raro". Son dos partes:

```bash
.venv/bin/pyremoteplay 192.168.1.42 --register   # usa TU IP del paso 1
```

**Parte A — login en el navegador:**
- La terminal te muestra una URL de Sony. Ábrela e inicia sesión con tu cuenta PSN.
- Al terminar te redirige a una **página en blanco**. Es normal.
- Copia la **URL completa** de esa página en blanco (empieza por `https://remoteplay.dl.playstation.net/...`) y pégala en la terminal.

**Parte B — PIN de la consola:**
- En la PS5: **Ajustes → Sistema → Uso a distancia → Vincular dispositivo** → aparece un **PIN de 8 dígitos**.
- Escríbelo en la terminal.

Listo: las credenciales quedan guardadas en `~/.pyremoteplay/` y no se repite nunca más.

> **Si algo falla aquí:** el flujo de login de Sony cambia de vez en cuando. El plan B
> es [chiaki-ng](https://github.com/streetpea/chiaki-ng), que registra la consola con
> interfaz gráfica. Abre un issue si te pasa.

## 4. Conectar con Claude Code

```bash
claude mcp add gta6 -- "$(pwd)/.venv/bin/gta6-mcp"
```

(Si usas otro cliente MCP: el comando a registrar es la ruta absoluta a `.venv/bin/gta6-mcp`, transporte stdio.)

## 5. Probar

Abre Claude Code y dile:

> Conéctate a la PS5 en 192.168.1.42 y saca un screenshot.

Si ves un frame de la consola: **funciona**. A partir de ahí: `drive()`, `walk()`, `cheat()`…

## Problemas típicos

| Síntoma | Causa probable | Arreglo |
|---|---|---|
| `No response from <IP>` | PS5 apagada del todo, u otra red | Enciéndela o revisa la IP; `wake()` solo funciona desde reposo, no desde apagado total |
| `No registered PSN users` | Falta el paso 3 | `.venv/bin/pyremoteplay <IP> --register` |
| `Session refused` | Otro cliente Remote Play ya conectado | Cierra la app oficial de Remote Play / chiaki |
| Conecta pero sin vídeo | Códec/resolución | Prueba `connect(host, resolution="540p")` |
| El login de Sony no da la URL | Flujo OAuth cambiado | Plan B: chiaki-ng (ver arriba) |
