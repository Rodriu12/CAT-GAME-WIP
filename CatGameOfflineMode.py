# Este es el modo offline para usarlo sin internet. Está hecho de la misma manera que el online sin la conexión al exterior.
# Versión liviana al no traer las funcionalidades del modo online.
# También pueden modificar a gusto los colores y tamaños de los botones y letras.

from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import time

# Algoritmo MINIMAX para jugar contra la máquina usando esta IA de búsqueda adversaria
def minimax(board, depth, is_maximizing):
    # Verificar si hay ganador usando la misma lógica del método verificar() del modo 2 jugadores
    ganador = None
    if (board[0]=="X" and board[1]=="X" and board[2]=="X") or (board[3]=="X" and board[4]=="X" and board[5]=="X") or (board[6]=="X" and board[7]=="X" and board[8]=="X"):
        ganador = "X"
    elif (board[0]=="X" and board[3]=="X" and board[6]=="X") or (board[1]=="X" and board[4]=="X" and board[7]=="X") or (board[2]=="X" and board[5]=="X" and board[8]=="X"):
        ganador = "X"
    elif (board[0]=="X" and board[4]=="X" and board[8]=="X") or (board[2]=="X" and board[4]=="X" and board[6]=="X"):
        ganador = "X"
    elif (board[0]=="O" and board[1]=="O" and board[2]=="O") or (board[3]=="O" and board[4]=="O" and board[5]=="O") or (board[6]=="O" and board[7]=="O" and board[8]=="O"):
        ganador = "O"
    elif (board[0]=="O" and board[3]=="O" and board[6]=="O") or (board[1]=="O" and board[4]=="O" and board[7]=="O") or (board[2]=="O" and board[5]=="O" and board[8]=="O"):
        ganador = "O"
    elif (board[0]=="O" and board[4]=="O" and board[8]=="O") or (board[2]=="O" and board[4]=="O" and board[6]=="O"):
        ganador = "O"

    if ganador == "O":   
        return 10 - depth
    elif ganador == "X":
        return depth - 10
    elif "N" not in board:
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == "N":
                board[i] = "O"
                score = minimax(board, depth+1, False)
                board[i] = "N"
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == "N":
                board[i] = "X"
                score = minimax(board, depth+1, True)
                board[i] = "N"
                best_score = min(score, best_score)
        return best_score

def mejor_movimiento_ia(board):
    mejor_puntaje = -float('inf')
    mejor_mov = None
    for i in range(9):
        if board[i] == "N":
            board[i] = "O"
            puntaje = minimax(board, 0, False)
            board[i] = "N"
            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
                mejor_mov = i
    return mejor_mov

# Funciones adaptadas al nuevo modo de 1 solo jugador contra la máquina
def bloquear():
    for i in range(0,9):
        listaBotones[i].config(state="disable")

def desbloquear():
    for i in range(0,9):
        listaBotones[i].config(state="normal")

def resetear_tablero():
    for i in range(0,9):
        listaBotones[i].config(state="normal")
        listaBotones[i].config(bg="lightgray")
        listaBotones[i].config(text="")
        t[i] = "N"
    bloquear()

def iniciarJ():
    global nombreJugador1, nombreJugador2, modo_maquina, turno
    modo_maquina = False
    resetear_tablero()
    nombreJugador1 = simpledialog.askstring("Jugador", "Escribe el nombre del jugador 1: ")
    nombreJugador2 = simpledialog.askstring("Jugador", "Escribe el nombre del jugador 2: ")
    if not nombreJugador1 or not nombreJugador2:
        return
    turno = 0
    turnoJugador.set("Turno: " + nombreJugador1)
    desbloquear()

def iniciarJ1():
    global nombreJugador1, nombreJugador2, modo_maquina, turno
    modo_maquina = True
    resetear_tablero()
    nombreJugador1 = simpledialog.askstring("Jugador", "Escribe tu nombre (tú eres X): ")
    if not nombreJugador1:
        return
    nombreJugador2 = "Máquina"
    turno = 0
    turnoJugador.set("Turno: " + nombreJugador1)
    desbloquear()

def cambiar(num):
    global turno, nombreJugador1, nombreJugador2, modo_maquina
    if t[num] != "N":
        return

    if t[num]=="N" and turno==0:
        listaBotones[num].config(text="X")
        listaBotones[num].config(bg="white")
        t[num] = "X"
        turno = 1
        if modo_maquina:
            turnoJugador.set("Turno: " + nombreJugador2 + " (O)")
        else:
            turnoJugador.set("Turno: " + nombreJugador2)
        listaBotones[num].config(state="disable")
        if verificar():
            return

        if modo_maquina:
            ventana.after(500, movimiento_ia)
    elif t[num]=="N" and turno==1:
        
        listaBotones[num].config(text="O")
        listaBotones[num].config(bg="lightblue")
        t[num] = "O"
        turno = 0
        turnoJugador.set("Turno: " + nombreJugador1)
        listaBotones[num].config(state="disable")
        verificar()

def movimiento_ia():
    global turno
    if modo_maquina and turno == 1:
        mov = mejor_movimiento_ia(t)
        if mov is not None:
            t[mov] = "O"
            listaBotones[mov].config(text="O")
            listaBotones[mov].config(bg="lightblue")
            listaBotones[mov].config(state="disable")
            turno = 0
            turnoJugador.set("Turno: " + nombreJugador1)
            verificar()

def verificar():
    
    if (t[0]=="X" and t[1]=="X" and t[2]=="X") or (t[3]=="X" and t[4]=="X" and t[5]=="X") or (t[6]=="X" and t[7]=="X" and t[8]=="X"):
        bloquear()
        messagebox.showinfo("¡Ganador!", "Ganaste Jugador " + nombreJugador1)
        return True
    elif (t[0]=="X" and t[3]=="X" and t[6]=="X") or (t[1]=="X" and t[4]=="X" and t[7]=="X") or (t[2]=="X" and t[5]=="X" and t[8]=="X"):
        bloquear()
        messagebox.showinfo("¡Ganador!", "Ganaste Jugador " + nombreJugador1)
        return True
    elif (t[0]=="X" and t[4]=="X" and t[8]=="X") or (t[2]=="X" and t[4]=="X" and t[6]=="X"):
        bloquear()
        messagebox.showinfo("¡Ganador!", "Ganaste Jugador " + nombreJugador1)
        return True
    elif (t[0]=="O" and t[1]=="O" and t[2]=="O") or (t[3]=="O" and t[4]=="O" and t[5]=="O") or (t[6]=="O" and t[7]=="O" and t[8]=="O"):
        bloquear()
        if modo_maquina:
            messagebox.showinfo("¡Ganador!", "Ganó la máquina (O)")
        else:
            messagebox.showinfo("¡Ganador!", "Ganaste Jugador " + nombreJugador2)
        return True
    elif (t[0]=="O" and t[3]=="O" and t[6]=="O") or (t[1]=="O" and t[4]=="O" and t[7]=="O") or (t[2]=="O" and t[5]=="O" and t[8]=="O"):
        bloquear()
        if modo_maquina:
            messagebox.showinfo("¡Ganador!", "Ganó la máquina (O)")
        else:
            messagebox.showinfo("¡Ganador!", "Ganaste Jugador " + nombreJugador2)
        return True
    elif (t[0]=="O" and t[4]=="O" and t[8]=="O") or (t[2]=="O" and t[4]=="O" and t[6]=="O"):
        bloquear()
        if modo_maquina:
            messagebox.showinfo("¡Ganador!", "Ganó la máquina (O)")
        else:
            messagebox.showinfo("¡Ganador!", "Ganaste Jugador " + nombreJugador2)
        return True
    elif "N" not in t:
        bloquear()
        messagebox.showinfo("Empate", "¡Empate!")
        return True
    return False

# ---------- Interfaz del juego del gato ----------
ventana = Tk()
ventana.title("Cat Game")
ventana.geometry("400x500")

turno = 0
nombreJugador1 = ""
nombreJugador2 = ""
modo_maquina = False

listaBotones = []
t = ["N"] * 9
turnoJugador = StringVar()

posiciones = [(50,50), (150,50), (250,50),
              (50,150), (150,150), (250,150),
              (50,250), (150,250), (250,250)]

for i, (x,y) in enumerate(posiciones):
    btn = Button(ventana, width=10, height=5, command=lambda idx=i: cambiar(idx))
    btn.place(x=x, y=y)
    listaBotones.append(btn)

turnoEtiqueta = Label(ventana, textvariable=turnoJugador)
turnoEtiqueta.place(x=120, y=20)
turnoJugador.set("Presiona 'Iniciar'")

iniciar = Button(ventana, bg="#006", fg="white", text="INICIAR EL JUEGO", width=15, height=3, command=iniciarJ)
iniciar.place(x=50, y=350)

iniciar_maq = Button(ventana, bg="#060", fg="white", text="VS MÁQUINA", width=15, height=3, command=iniciarJ1)
iniciar_maq.place(x=200, y=350)

bloquear()

ventana.mainloop()