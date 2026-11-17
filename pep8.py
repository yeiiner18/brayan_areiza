import tkinter as tk
import ast
import operator

# Configuración de la ventana
ventana = tk.Tk()
ventana.title("Mi Calculadora - Python")
ventana.geometry("340x430")
ventana.resizable(False, False)
ventana.configure(bg="#1E1E2E")

# Colores
color_fondo = "#1E1E2E"
color_pantalla = "#313244"
color_numero = "#45475A"
color_operacion = "#89B4FA"
color_borrar = "#F38BA8"
color_igual = "#A6E3A1"
color_texto = "#FFFFFF"

# Pantalla de la calculadora
entrada_texto = tk.Entry(
    ventana,
    font=("Calibri", 25),
    bg=color_pantalla,
    fg=color_texto,
    insertbackground=color_texto,
    justify="right",
    bd=0
)
entrada_texto.grid(
    row=0,
    column=0,
    columnspan=4,
    padx=10,
    pady=15,
    ipady=12,
    sticky="nsew"
)


# Insertar valores
def insertar_valor(valor):
    if entrada_texto.get() == "Error":
        entrada_texto.delete(0, tk.END)

    entrada_texto.insert(tk.END, str(valor))


# Borrar toda la pantalla
def borrar():
    entrada_texto.delete(0, tk.END)


# Borrar el último carácter
def borrar_ultimo():
    contenido = entrada_texto.get()

    if contenido:
        entrada_texto.delete(len(contenido) - 1, tk.END)


# Evaluar operaciones matemáticas de forma controlada
operaciones = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod
}


def evaluar(nodo):
    if isinstance(nodo, ast.Expression):
        return evaluar(nodo.body)

    if isinstance(nodo, ast.Constant) and type(nodo.value) in (int, float):
        return nodo.value

    if isinstance(nodo, ast.BinOp) and type(nodo.op) in operaciones:
        izquierda = evaluar(nodo.left)
        derecha = evaluar(nodo.right)
        return operaciones[type(nodo.op)](izquierda, derecha)

    if isinstance(nodo, ast.UnaryOp) and isinstance(
        nodo.op, (ast.UAdd, ast.USub)
    ):
        valor = evaluar(nodo.operand)
        return valor if isinstance(nodo.op, ast.UAdd) else -valor

    raise ValueError("Operación no permitida")


# Calcular resultado
def calcular():
    ecuacion = entrada_texto.get()

    try:
        arbol = ast.parse(ecuacion, mode="eval")
        resultado = evaluar(arbol)

        entrada_texto.delete(0, tk.END)
        entrada_texto.insert(0, str(resultado))

    except Exception:
        entrada_texto.delete(0, tk.END)
        entrada_texto.insert(0, "Error")


# Crear botones con diseño
def crear_boton(texto, fila, columna, comando,
                color=color_numero, columnas=1):

    boton = tk.Button(
        ventana,
        text=texto,
        font=("Calibri", 16, "bold"),
        width=5,
        height=2,
        bg=color,
        fg=color_texto,
        activebackground="#585B70",
        activeforeground=color_texto,
        bd=0,
        cursor="hand2",
        command=comando
    )

    boton.grid(
        row=fila,
        column=columna,
        columnspan=columnas,
        padx=5,
        pady=5,
        sticky="nsew"
    )

    return boton


# Primera fila: borrar y paréntesis
crear_boton("AC", 1, 0, borrar, color_borrar)
crear_boton("⌫", 1, 1, borrar_ultimo, color_borrar)
crear_boton("(", 1, 2, lambda: insertar_valor("("), color_operacion)
crear_boton(")", 1, 3, lambda: insertar_valor(")"), color_operacion)

# Segunda fila
crear_boton("7", 2, 0, lambda: insertar_valor(7))
crear_boton("8", 2, 1, lambda: insertar_valor(8))
crear_boton("9", 2, 2, lambda: insertar_valor(9))
crear_boton("/", 2, 3, lambda: insertar_valor("/"), color_operacion)

# Tercera fila
crear_boton("4", 3, 0, lambda: insertar_valor(4))
crear_boton("5", 3, 1, lambda: insertar_valor(5))
crear_boton("6", 3, 2, lambda: insertar_valor(6))
crear_boton("*", 3, 3, lambda: insertar_valor("*"), color_operacion)

# Cuarta fila
crear_boton("1", 4, 0, lambda: insertar_valor(1))
crear_boton("2", 4, 1, lambda: insertar_valor(2))
crear_boton("3", 4, 2, lambda: insertar_valor(3))
crear_boton("-", 4, 3, lambda: insertar_valor("-"), color_operacion)

# Quinta fila
crear_boton("0", 5, 0, lambda: insertar_valor(0), columnas=2)
crear_boton(".", 5, 2, lambda: insertar_valor("."))
crear_boton("%", 5, 3, lambda: insertar_valor("/100"), color_operacion)

# Sexta fila
crear_boton("+", 6, 0, lambda: insertar_valor("+"), color_operacion)
crear_boton("=", 6, 1, calcular, color_igual, columnas=3)

# Ajustar columnas
for columna in range(4):
    ventana.grid_columnconfigure(columna, weight=1)

ventana.mainloop()
