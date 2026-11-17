# MCP para que Claude juegue GTA 6 en PS5: investigación y plan

Fecha: 17 nov 2026. GTA 6 sale el jueves 19 nov 2026 en PS5 y Xbox Series X|S.

## Resumen

- **GTA 6 no está en el mercado todavía**, pero ya hay MCPs de Claude jugando a otros GTA y a juegos de PC.
- **Lo que existe es casi todo PC**: GTA 4, GTA V (mod), San Andreas, juegos de Windows en general.
- **No he encontrado nada que controle una PS5**, ni nada para GTA 6. El hueco es "Claude + PS5 + GTA 6 en el día de lanzamiento".
- **Se puede llegar primero, pero con poco margen.** Ya hay un artículo en XDA sobre Claude jugando GTA 4 "justo antes de GTA 6", así que otros van a intentar lo mismo.
- Mi búsqueda fue limitada (web y directorios MCP). No puedo garantizar que no exista algo privado o publicado hoy.

## Qué ya existe

| Proyecto | Qué hace | Plataforma |
|---|---|---|
| Claude jugando GTA 4 (post de r/ClaudeAI, cubierto por XDA) | MCP con teclado, ratón, mando y pantalla propios; el juego corre en segundo plano | PC |
| "LLM Game Automation MCP" (vídeo de YouTube) | MCP gratis para que Claude Code o Codex jueguen juegos de PC en segundo plano, GTA incluido | PC |
| GTAV-CLAUDE-MCP (TabbedScamper) | Claude dentro de GTA V: spawnear coches, clima, llamar nativas, chat en el juego (F10) | PC, con mod |
| gta-sa-mcp (Rams25) y sa-mcp (dntAtMe) | Observar, pilotar y editar GTA San Andreas con screenshots | PC |
| local-game-mcp | Input a nivel HID + captura + OCR para juegos locales | Windows |
| MCPs de emuladores (GameBoy, SNES, DOS, Sega) | Botones + screenshot | Emuladores |
| claude-ps5-mcp | Descubrir, registrar y despertar la PS5 | PS5, sin mando |
| ps5-mcp (leolobato) | Ver y controlar una PS5 con jailbreak, vídeo y audio HDMI | PS5 con jailbreak, solo macOS |
| Claude Plays Pokémon / Gemini Plays Pokémon | Streams en Twitch de IA jugando | Game Boy |

Lo importante: **la idea de "Claude juega un juego" ya es conocida y viral** (Pokémon), y la de "Claude juega GTA" ya existe en PC. Lo nuevo sería PS5 + GTA 6.

## El hueco

1. **Consola real, no PC.** Nadie parece haberlo hecho sobre PS5 sin jailbreak.
2. **GTA 6 el día 1.** Rockstar confirmó que GTA 6 soporta Remote Play en PlayStation y Xbox, así que el camino existe sin tocar la consola.
3. **Narrativa**: "Claude juega GTA 6 en una PS5 normal, sin mods".

## Cómo hacerlo (de más rápido a más propio)

### Opción A: reutilizar lo que ya hay (la más rápida)
- Cliente Remote Play en tu PC (chiaki-ng, activamente mantenido; v1.10.0 salió en abril 2026).
- Un MCP de juegos para PC que mande input virtual (mando) y capture la ventana, apuntando a la ventana de chiaki-ng.
- Ventaja: horas, no días. Desventaja: no es tuyo, así que el diferenciador es solo el montaje.

### Opción B: MCP propio sobre pyremoteplay
- pyremoteplay permite registrar la consola, controlar el host, sacar el stream de vídeo/audio y emular un DualShock.
- Tools: `screenshot()`, `press(button, ms)`, `stick(side, x, y, ms)`, y macros (`drive(throttle, steer, seconds)`, `enter_vehicle()`, `open_phone()`).
- Riesgo: no he podido confirmar que siga funcionando con el firmware actual de PS5. Probar **primero** que conecta y que llega vídeo.

### Opción C: híbrido
- Probar B; si falla, caer a A. El MCP propio es lo que se puede vender; A es el plan de rescate.

## Plan de 48 horas

1. **Hoy:** confirmar firmware de la PS5, activar Remote Play, registrar con pyremoteplay y ver si llega un frame. Si no, pasar a A.
2. **Mañana:** MCP mínimo (`screenshot`, `press`, `stick`) funcionando con otro juego, antes de GTA 6.
3. **Jueves 19:** probar con GTA 6 apenas arranque. Empezar con el personaje en un coche, calle despejada, macros de 1 a 3 s.
4. **Grabar:** pantalla de juego + log de tool calls al lado.

## Riesgos

- **Latencia**: el bucle screenshot → modelo → acción tarda segundos. GTA 6 va a 30 FPS en todas las consolas, y Remote Play añade compresión. Funciona conducir y explorar, no combate.
- **Firmware**: Sony sube firmware a menudo (14.x en sept/oct 2026). Las librerías no oficiales pueden romperse.
- **Rockstar/Sony**: no sé si limitan captura o Remote Play en las primeras horas. Probar antes de prometer nada.
- **Competencia**: lo del GTA 4 ya salió; habrá más intentos el día del estreno.
- **Cuenta PSN**: usar una cuenta propia; es una automatización no oficial.

## Cómo venderlo sin que se rompa

- Decir qué es: Claude controla la consola con macros y visión. Es igual de llamativo y aguanta cuando alguien lo pruebe.
- Enseñar el log de tool calls: es lo que convence a gente técnica.
- Evitar prometer "Claude se pasa el juego" o "juega como un humano": no va a pasar.

## Fuentes

- XDA: Claude jugando GTA 4 con un MCP: https://www.xda-developers.com/someone-got-claude-to-play-gta-4-just-ahead-of-gta6s-release/
- GTAV-CLAUDE-MCP: https://glama.ai/mcp/servers/TabbedScamper/GTAV-CLAUDE-MCP
- gta-sa-mcp: https://github.com/Rams25/gta-sa-mcp
- sa-mcp: https://github.com/dntAtMe/sa-mcp
- LLM Game Automation MCP (vídeo): https://www.youtube.com/watch?v=0ss1R0WnfWc
- local-game-mcp: https://glama.ai/mcp/servers/uxx02eftgl
- ps5-mcp (leolobato): https://glama.ai/mcp/servers/leolobato/ps5-mcp
- claude-ps5-mcp: https://www.pkgstats.com/pkg:claude-ps5-mcp
- pyremoteplay: https://pyremoteplay.readthedocs.io/en/latest/readme.html
- chiaki-ng v1.10.0: https://www.pulse.bot/gaming/news/chiaki-ng-the-open-source-playstation-remote-play-app-gets-better-streaming-quality-and-stability-a3a9807f-5b16-43e4-8a27-05c4e43eafa8
- Rockstar: Remote Play en GTA 6: https://www.dexerto.com/gta/gta-6-confirms-xbox-cloud-gaming-support-but-pc-players-face-a-catch-3427015/
- GTA 6, 30 FPS y fecha: https://playday.one/2026/11/10/gta-6-confirms-ps5-pro-enhancements-and-xbox-cloud-gaming-availability/
- Claude Plays Pokémon: https://latent.space/reading/claude-plays-pokemon/