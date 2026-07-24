# Este es el modo offline para usarlo sin internet. Está hecho de la misma manera que el online sin la conexión al exterior.
# Versión liviana al no traer las funcionalidades del modo online.
# También pueden modificar a gusto los colores y tamaños de los botones y letras.

from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

def bloquear():
    for i in range(0,9):
        listaBotones[i].config(state="disable")
        
def iniciarJ():
    for i in range(0,9):
        listaBotones[i].config(state="normal")
        listaBotones[i].config(bg="lightgray")
        listaBotones[i].config(text="")
        t[i] = "N"
    global nombreJugador1, nombreJugador2
    nombreJugador1 = simpledialog.askstring("Jugador", "Escribe el nombre del jugador 1: ")
    nombreJugador2 = simpledialog.askstring("Jugador", "Escribe el nombre del jugador 2: ")
    turnoJugador.set("Turno: " + nombreJugador1)
    
def cambiar(num):
    global turno, nombreJugador1, nombreJugador2
    if t[num]=="N" and turno==0:
        listaBotones[num].config(text="X")
        listaBotones[num].config(bg="white")
        t[num] = "X"
        turno = 1
        turnoJugador.set("Turno: " + nombreJugador2)
    elif t[num]=="N" and turno==1:
        listaBotones[num].config(text="O")
        listaBotones[num].config(bg="lightblue")
        t[num] = "O"
        turno = 0
        turnoJugador.set("Turno: " + nombreJugador1)
    listaBotones[num].config(state="disable")
    verificar()

def verificar():
    if (t[0]=="X" and t[1]=="X" and t[2]=="X") or (t[3]=="X" and t[4]=="X" and t[5]=="X") or (t[6]=="X" and t[7]=="X" and t[8]=="X"):
        bloquear()
        messagebox.showinfo("¡Ganador!", "Ganaste Jugador " + nombreJugador1)
    elif (t[0]=="X" and t[3]=="X" and t[6]=="X") or (t[1]=="X" and t[4]=="X" and t[7]=="X") or (t[2]=="X" and t[5]=="X" and t[8]=="X"):
        bloquear()
        messagebox.showinfo("¡Ganador!", "Ganaste Jugador " + nombreJugador1)
    elif (t[0]=="X" and t[4]=="X" and t[8]=="X") or (t[2]=="X" and t[4]=="X" and t[6]=="X"):
        bloquear()
        messagebox.showinfo("¡Ganador!", "Ganaste Jugador " + nombreJugador1)
    elif (t[0]=="O" and t[1]=="O" and t[2]=="O") or (t[3]=="O" and t[4]=="O" and t[5]=="O") or (t[6]=="O" and t[7]=="O" and t[8]=="O"):
        bloquear()
        messagebox.showinfo("¡Ganador!", "Ganaste Jugador " + nombreJugador2)
    elif (t[0]=="O" and t[3]=="O" and t[6]=="O") or (t[1]=="O" and t[4]=="O" and t[7]=="O") or (t[2]=="O" and t[5]=="O" and t[8]=="O"):
        bloquear()
        messagebox.showinfo("¡Ganador!", "Ganaste Jugador " + nombreJugador2)
    elif (t[0]=="O" and t[4]=="O" and t[8]=="O") or (t[2]=="O" and t[4]=="O" and t[6]=="O"):
        bloquear()
        messagebox.showinfo("¡Ganador!", "Ganaste Jugador " + nombreJugador2)
        
ventana = Tk()
ventana.title("Cat Game")
ventana.geometry("400x500")

turno = 0
nombreJugador1 = ""
nombreJugador2 = ""

listaBotones = []
t = [] # X O N
turnoJugador = StringVar()

for i in range(0,9):
    t.append("N")

boton0 = Button(ventana, width=10, height=5, command=lambda: cambiar(0))
listaBotones.append(boton0)
boton0.place(x=50, y=50)

boton1 = Button(ventana, width=10, height=5, command=lambda: cambiar(1))
listaBotones.append(boton1)
boton1.place(x=150, y=50)

boton2 = Button(ventana, width=10, height=5, command=lambda: cambiar(2))
listaBotones.append(boton2)
boton2.place(x=250, y=50)

boton3 = Button(ventana, width=10, height=5, command=lambda: cambiar(3))
listaBotones.append(boton3)
boton3.place(x=50, y=150)

boton4 = Button(ventana, width=10, height=5, command=lambda: cambiar(4))
listaBotones.append(boton4)
boton4.place(x=150, y=150)

boton5 = Button(ventana, width=10, height=5, command=lambda: cambiar(5))
listaBotones.append(boton5)
boton5.place(x=250, y=150)

boton6 = Button(ventana, width=10, height=5, command=lambda: cambiar(6))
listaBotones.append(boton6)
boton6.place(x=50, y=250)

boton7 = Button(ventana, width=10, height=5, command=lambda: cambiar(7))
listaBotones.append(boton7)
boton7.place(x=150, y=250)

boton8 = Button(ventana, width=10, height=5, command=lambda: cambiar(8))
listaBotones.append(boton8)
boton8.place(x=250, y=250)

turnoEtiqueta = Label(ventana, textvariable=turnoJugador).place(x=120, y=20)
iniciar = Button(ventana, bg="#006", fg="white", text="INICIAR EL JUEGO", width=15, height=3, command=iniciarJ).place(x=130, y=350)
bloquear()

ventana.mainloop()
