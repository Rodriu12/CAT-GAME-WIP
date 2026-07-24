# CAT-GAME-WIP (Modo Offline y Modo Online (Puedes jugar en LAN usando la misma red o con tu amigo nacional o internacional))

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Un clásico juego del "Gato" (Tic-Tac-Toe) con soporte para partidas multijugador en red local (LAN) y a través de Internet (con herramientas externas como ngrok). El juego cuenta con una interfaz gráfica simple e intuitiva, desarrollada con `tkinter`.


## Características

*   **Multijugador en Red:** Juega contra un amigo en tu misma red local (LAN) o a través de Internet.
*   **Interfaz Gráfica:** Ventana de juego limpia y fácil de usar con `tkinter`.
*   **Roles Definidos:** Un jugador actúa como **Servidor (X)** y el otro como **Cliente (O)**.
*   **Sincronización en Tiempo Real:** Los movimientos se sincronizan instantáneamente entre ambos jugadores.
*   **Sistema de Turnos:** Indica claramente de quién es el turno.
*   **Detección de Fin de Partida:** Detecta automáticamente victorias y empates, mostrando un mensaje al ganador.
*   **Jugar de Nuevo:** Permite reiniciar la partida sin necesidad de reconectar.
*   **Portátil:** Funciona tanto en Windows, macOS como en Linux.

## Requisitos Obligatorios Para Modo LAN
* Si quieres jugar de manera online y en modo LAN (usando la misma red) siendo host, ejecuta en la terminal WindowsPowershell o Símbolo del sistema "ipconfig" y busca tu dirección IP en Dirección IPV4 en Adaptador de LAN Inalámbrica de Wi-Fi y el puerto dejalo por defecto en 5000. Después de esto aprieta "Host" y selecciona aceptar para esperar al otro jugador. (Ej.: IP: 127.0.0.1(dependiendo cuál tenga asignada tu computadora) y el puerto dejalo por defecto en 5000).
  
* Para el jugador que se va a conectar (cliente) anota la ip junto con el puerto del host y aprieta "Join". (LOS DATOS DEBEN SER LO MISMOS ej.: IP: 127.0.0.1(dependiendo cuál tenga asignada el host) puerto: 5000 por defecto).

## Requisitos Opcionales
* Si quieres jugar de manera online y no desde tu misma red utiliza la herramienta ngrok como túnel entre tu computadora y la otra que vayan a utilizar de manera remota.

* Para usarla usa los siguientes comandos:
  1. Instala ngrok en tu pc desde su página oficial. (Necesitas una cuenta registrada para usarlo).
  2. Escribe "ngrok authtoken TU_TOKEN_AQUI" en la terminal de WindowsPowershell o Símbolo del sistema y en TU_TOKEN_AQUI usa el token que te dió ngrok para conectar tu cuenta. Va salir un mensaje tipo: "Authtoken saved to configuration file" o parecido.
  3. Escribe "ngrok tcp 5000" en la terminal de WindowsPowershell o Símbolo del sistema.
  4. Anota la ip que te asigna ngrok "ej.: 0.tcp.ngrok.io" y el puerto que asigne ngrok "ej.: 12345".
  5. Aprieta Join y se deberían de conectar automáticamente. (Si no llegara a funcionar es porque tu firewall bloquea las conexiones exteriores y para eso necesitas configurar la regla de que permita usar el puerto asignado por ngrok especialmente al archivo .exe).

##  Instalación

Sigue estos pasos para tener el juego funcionando en tu pc:

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/TU_USUARIO/gato-online.git

    O descarga el archivo .zip apretando "<> Code", selecciona "Download ZIP" y descomprimelo en donde tú quieras usando tu herramienta preferida.

2. **Ejecuta el archivo .exe que tú quieras ejecutar**
3. **Disfruta jugando en tu mismo pc con tu familia o amigos :)**

## Tecnologías Utilizadas
Python: Lenguaje de programación principal.

Tkinter: Biblioteca estándar para la interfaz gráfica de usuario (GUI).

Sockets: Para la comunicación en red entre el servidor y el cliente.

## ¿Cómo Contribuir?
¡Las contribuciones son bienvenidas! Si deseas mejorar el proyecto, por favor:
* Abre un ISSUE en el repositorio y deja tus sugerencias o ideas de cómo puedo mejorarlo.

##  Licencia y Derechos de Autor
Este proyecto está bajo la Licencia MIT. Puedes usarlo para tu proyecto educativo en tu universidad o instituto en el que estudies. Esto significa que eres libre de usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar y/o vender copias del software, siempre y cuando se cumplan las siguientes condiciones:

El aviso de derechos de autor y este permiso deben incluirse en todas las copias o partes sustanciales del software.

**Copyright (c) 2026 Rodriu12**
