from tkinter import *
from tkinter import messagebox, simpledialog
import socket
import threading
import time

ventana = Tk()
ventana.title("Cat Game - LAN")
ventana.geometry("400x500")

# Variables globales para no tener errores de "nombrevariable is not defined" y acceder más fácilmente sin volver a declararlas
turno = 0
listaBotones = []
t = []  # "N", "X", "O"
turnoJugador = StringVar()

is_server = False
is_client = False
connected = False
game_started = False
local_name = ""
opponent_name = ""
local_symbol = ""
server_socket = None
client_socket = None
receiver_thread = None


def bloquear():
    for btn in listaBotones:
        btn.config(state="disable")

def desbloquear():
    for btn in listaBotones:
        btn.config(state="normal")

def actualizar_turno():
    if not game_started:
        turnoJugador.set("Esperando...")
        return
    if turno == 0:  # Turno de X
        if is_server:
            turnoJugador.set("Turno: " + local_name + " (X)")
        else:
            turnoJugador.set("Turno: " + opponent_name + " (X)")
    else:           # Turno de O
        if is_client:
            turnoJugador.set("Turno: " + local_name + " (O)")
        else:
            turnoJugador.set("Turno: " + opponent_name + " (O)")

def mostrar_ganador(ganador):
    bloquear()
    messagebox.showinfo("¡Ganador!", "¡" + ganador + " ha ganado!")
    mostrar_botones_post_partida()

def mostrar_empate():
    bloquear()
    messagebox.showinfo("Empate", "¡Empate!")
    mostrar_botones_post_partida()

def mostrar_botones_post_partida():
    btn_reiniciar.place(x=100, y=380)
    btn_salir.place(x=220, y=380)

def ocultar_botones_post_partida():
    btn_reiniciar.place_forget()
    btn_salir.place_forget()

# ---------- Funciones de red para el correcto funcionamiento del juego----------
def send_message(sock, msg):
    try:
        sock.sendall((msg + "\n").encode())
        print("[ENVIADO]", msg)
    except Exception as e:
        print("[ERROR al enviar]", e)

def process_message(msg):
    global turno, game_started, connected, opponent_name
    print("[RECIBIDO]", msg)  # Depuración
    parts = msg.strip().split()
    if not parts:
        return
    cmd = parts[0]

    if cmd == "NAME":
        if len(parts) >= 2:
            opponent_name = " ".join(parts[1:])
            if game_started:
                actualizar_turno()
    elif cmd == "START":
        game_started = True
        desbloquear()
        actualizar_turno()
        ocultar_botones_post_partida()
    elif cmd == "MOVE":
        if len(parts) >= 3:
            try:
                idx = int(parts[1])
                simbolo = parts[2]
                if t[idx] == "N":
                    t[idx] = simbolo
                    if simbolo == "X":
                        listaBotones[idx].config(text="X", bg="white", state="disable")
                    else:
                        listaBotones[idx].config(text="O", bg="lightblue", state="disable")
                    turno = 1 if simbolo == "X" else 0
                    actualizar_turno()
                    if verificar_ganador(simbolo):
                        ganador = local_name if simbolo == local_symbol else opponent_name
                        mostrar_ganador(ganador)
                        game_started = False
                    elif verificar_empate():
                        mostrar_empate()
                        game_started = False
            except:
                pass
    elif cmd == "WIN":
        if len(parts) >= 2:
            ganador = " ".join(parts[1:])
            mostrar_ganador(ganador)
            game_started = False
    elif cmd == "DRAW":
        mostrar_empate()
        game_started = False
    elif cmd == "REINICIAR":
        print("REINICIANDO por orden del otro jugador")
        reiniciar_tablero()
        game_started = True
        desbloquear()
        actualizar_turno()
        ocultar_botones_post_partida()
    elif cmd == "ERROR":
        messagebox.showerror("Error", "Movimiento inválido")

def receive_messages(sock):
    global connected
    while connected:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            lines = data.split("\n")
            for line in lines:
                if line.strip():
                    ventana.after(0, lambda l=line: process_message(l))
        except:
            break
    connected = False
    ventana.after(0, lambda: messagebox.showerror("Conexión perdida", "Se ha perdido la conexión."))
    ventana.after(0, bloquear)

# ---------- Funciones de inicio del que va a actuar de HOST----------
def host_game():
    global is_server, is_client, connected, server_socket, client_socket, receiver_thread
    global local_name, opponent_name, local_symbol, game_started, turno
    try:
        port = int(entry_port.get())
        ip = entry_ip.get()
    except:
        messagebox.showerror("Error", "Puerto inválido")
        return

    local_name = simpledialog.askstring("Nombre", "Ingresa tu nombre (servidor):")
    if not local_name:
        return

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((ip, port))
        server_socket.listen(1)
        messagebox.showinfo("Esperando", "Esperando conexión del cliente...")
        client_socket, addr = server_socket.accept()
        connected = True
        is_server = True
        is_client = False
        local_symbol = "X"
        turno = 0
        send_message(client_socket, "NAME " + local_name)
        receiver_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
        receiver_thread.start()
        time.sleep(0.5)
        send_message(client_socket, "START")
        game_started = True
        desbloquear()
        actualizar_turno()
        btn_host.config(state="disabled")
        btn_join.config(state="disabled")
        entry_ip.config(state="disabled")
        entry_port.config(state="disabled")
        ocultar_botones_post_partida()
    except Exception as e:
        messagebox.showerror("Error", "No se pudo iniciar: " + str(e))
        if server_socket:
            server_socket.close()
        connected = False

def join_game():
    global is_server, is_client, connected, client_socket, receiver_thread
    global local_name, opponent_name, local_symbol, game_started, turno
    try:
        port = int(entry_port.get())
        ip = entry_ip.get()
    except:
        messagebox.showerror("Error", "Puerto inválido")
        return

    local_name = simpledialog.askstring("Nombre", "Ingresa tu nombre (cliente):")
    if not local_name:
        return

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, port))
        connected = True
        is_client = True
        is_server = False
        local_symbol = "O"
        turno = 1
        send_message(client_socket, "NAME " + local_name)
        receiver_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
        receiver_thread.start()
        btn_host.config(state="disabled")
        btn_join.config(state="disabled")
        entry_ip.config(state="disabled")
        entry_port.config(state="disabled")
        bloquear()
        turnoJugador.set("Conectado, esperando inicio...")
        ocultar_botones_post_partida()
    except Exception as e:
        messagebox.showerror("Error", "No se pudo conectar: " + str(e))
        if client_socket:
            client_socket.close()
        connected = False

# ---------- Funcion de los clic que hacen los jugadores----------
def cambiar(num):
    global turno, t, game_started, connected
    if not game_started or not connected:
        return
    if t[num] != "N":
        return

    if is_server and turno == 0 and local_symbol == "X":
        simbolo = "X"
        nuevo_turno = 1
    elif is_client and turno == 1 and local_symbol == "O":
        simbolo = "O"
        nuevo_turno = 0
    else:
        return

    t[num] = simbolo
    if simbolo == "X":
        listaBotones[num].config(text="X", bg="white", state="disable")
    else:
        listaBotones[num].config(text="O", bg="lightblue", state="disable")
    turno = nuevo_turno
    actualizar_turno()

    send_message(client_socket, "MOVE " + str(num) + " " + simbolo)

    if verificar_ganador(simbolo):
        ganador = local_name if simbolo == local_symbol else opponent_name
        mostrar_ganador(ganador)
        send_message(client_socket, "WIN " + ganador)
        game_started = False
    elif verificar_empate():
        mostrar_empate()
        send_message(client_socket, "DRAW")
        game_started = False

# ---------- Funciones de reinicio para jugar otra vez ----------
def reiniciar_tablero():
    global t, turno
    for i in range(9):
        t[i] = "N"
        listaBotones[i].config(text="", bg="lightgray", state="normal")
    # El servidor siempre empieza (X), el cliente espera (O)
    if is_server:
        turno = 0
    else:
        turno = 1
    bloquear()

def jugar_de_nuevo():
    global game_started, connected
    if not connected:
        messagebox.showerror("Error", "No hay conexión con el otro jugador.")
        return
    print("JUGAR DE NUEVO (local)")
    # Enviar el mensaje de reinicio al cliente o servidor dependiendo quién envíe primero el mensaje
    send_message(client_socket, "REINICIAR")
    # Reinicia localmente el tablero al confirmarse el reinicio
    reiniciar_tablero()
    game_started = True
    desbloquear()
    actualizar_turno()
    ocultar_botones_post_partida()

def salir():
    ventana.destroy()

# ---------- Funciones que verifican en cuál posición ganó el jugador 1 o 2 ----------
def verificar_ganador(simbolo):
    if (t[0] == simbolo and t[1] == simbolo and t[2] == simbolo) or \
       (t[3] == simbolo and t[4] == simbolo and t[5] == simbolo) or \
       (t[6] == simbolo and t[7] == simbolo and t[8] == simbolo):
        return True
    if (t[0] == simbolo and t[3] == simbolo and t[6] == simbolo) or \
       (t[1] == simbolo and t[4] == simbolo and t[7] == simbolo) or \
       (t[2] == simbolo and t[5] == simbolo and t[8] == simbolo):
        return True
    if (t[0] == simbolo and t[4] == simbolo and t[8] == simbolo) or \
       (t[2] == simbolo and t[4] == simbolo and t[6] == simbolo):
        return True
    return False

def verificar_empate():
    for i in range(9):
        if t[i] == "N":
            return False
    return True

# ---------- Interfaz gráfica del videojuego (pueden modificarla a su gusto :) )----------
Label(ventana, text="IP:").place(x=50, y=10)
entry_ip = Entry(ventana, width=15)
entry_ip.insert(0, "127.0.0.1")
entry_ip.place(x=80, y=8)

Label(ventana, text="Puerto:").place(x=200, y=10)
entry_port = Entry(ventana, width=5)
entry_port.insert(0, "5000")
entry_port.place(x=260, y=8)

btn_host = Button(ventana, text="Host", width=8, command=host_game)
btn_host.place(x=310, y=6)
btn_join = Button(ventana, text="Join", width=8, command=join_game)
btn_join.place(x=310, y=30)

Label(ventana, textvariable=turnoJugador).place(x=120, y=60)
turnoJugador.set("Esperando...")

for i in range(9):
    t.append("N")

posiciones = [(50, 100), (150, 100), (250, 100),
              (50, 200), (150, 200), (250, 200),
              (50, 300), (150, 300), (250, 300)]

for i, (x, y) in enumerate(posiciones):
    btn = Button(ventana, width=10, height=5, command=lambda idx=i: cambiar(idx))
    btn.place(x=x, y=y)
    listaBotones.append(btn)

bloquear()

# Botones post-partida (inicialmente ocultos mientras espera la conexión del cliente)
btn_reiniciar = Button(ventana, bg="#006", fg="white", text="Jugar de nuevo", width=15, height=2, command=jugar_de_nuevo)
btn_salir = Button(ventana, bg="#006", fg="white", text="Salir", width=10, height=2, command=salir)

def on_closing():
    global connected
    connected = False
    if client_socket:
        try:
            client_socket.close()
        except:
            pass
    if server_socket:
        try:
            server_socket.close()
        except:
            pass
    ventana.destroy()

ventana.protocol("WM_DELETE_WINDOW", on_closing)
ventana.mainloop()