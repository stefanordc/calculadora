import tkinter as tk
import math
import threading
import pystray
from PIL import Image, ImageDraw

resultado_exibido = False
current_text = ""

WINDOW_WIDTH = 420
WINDOW_HEIGHT = 540

maximized = False
normal_geometry = ""
icon = None  # Para o ícone da bandeja

def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    win.geometry(f"{width}x{height}+{x}+{y}")

# Helper para checar se é operador
def is_operator(char):
    return char in '+-*/^'

def button_click(valor):
    global current_text, resultado_exibido
    # Se o resultado foi exibido e usuário digita número ou ponto, inicia nova expressão
    if resultado_exibido and (str(valor).isdigit() or valor in [".", ","]):
        current_text = ""
        resultado_exibido = False

    # Se o valor digitado é operador, verificar se o último caractere também é operador
    if is_operator(str(valor)):
        if current_text:
            if is_operator(current_text[-1]):
                # Substitui o último operador pelo novo
                current_text = current_text[:-1]
    current_text += str(valor)
    display.delete(0, tk.END)
    display.insert(0, current_text)

def clear():
    global current_text, resultado_exibido
    current_text = ""
    resultado_exibido = False
    display.delete(0, tk.END)

def equals():
    global current_text, resultado_exibido
    try:
        expr = current_text.replace(",", ".")
        expr = expr.replace("^", "**")

        def substituir_raiz(expr_in):
            i = 0
            resultado = ""
            while i < len(expr_in):
                if expr_in[i] == '√':
                    if i +1 < len(expr_in) and expr_in[i+1] == '(':
                        par_count = 1
                        raiz_exp = ""
                        i += 2
                        while i < len(expr_in) and par_count > 0:
                            if expr_in[i] == '(':
                                par_count += 1
                            elif expr_in[i] == ')':
                                par_count -= 1
                            if par_count > 0:
                                raiz_exp += expr_in[i]
                            i += 1
                        resultado += f"math.sqrt({raiz_exp})"
                        continue
                    else:
                        resultado += "√"
                        i += 1
                        continue
                else:
                    resultado += expr_in[i]
                    i += 1
            return resultado

        expr = substituir_raiz(expr)

        resultado = eval(expr)
        if isinstance(resultado, float) and resultado.is_integer():
            resultado = int(resultado)

        display.delete(0, tk.END)
        display.insert(0, str(resultado))
        current_text = str(resultado)
        resultado_exibido = True
    except Exception:
        display.delete(0, tk.END)
        display.insert(0, "Erro")
        current_text = ""
        resultado_exibido = False

def tecla_pressionada(event):
    global resultado_exibido, current_text
    tecla = event.char
    valid_chars = '0123456789+-*/.,^()√'
    if tecla in valid_chars:
        if resultado_exibido and (tecla.isdigit() or tecla in '.,'):
            clear()
        button_click(tecla)
    elif tecla == '\r':
        equals()
    elif tecla == '\x08':
        current_text = current_text[:-1]
        display.delete(0, tk.END)
        display.insert(0, current_text)
        resultado_exibido = False
    elif event.keysym == 'Escape':
        clear()

def move_window(event):
    root.geometry(f'+{event.x_root - offset_x}+{event.y_root - offset_y}')

def start_move(event):
    global offset_x, offset_y
    offset_x = event.x
    offset_y = event.y

def close_app(icon_obj=None, item=None):
    # Para o ícone da bandeja caso exista e fecha app
    global icon
    if icon:
        icon.stop()
    root.destroy()

def minimize_app():
    root.withdraw()  # Esconde janela
    if icon:
        icon.visible = True  # Mostra ícone da bandeja

def restore_app(icon_obj=None, item=None):
    if icon:
        icon.visible = False
    root.deiconify()  # Mostra janela

def create_image():
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), color='black')
    dc = ImageDraw.Draw(image)
    dc.rectangle((16, 16, 48, 48), fill='white')
    return image

def setup_tray_icon():
    global icon
    image = create_image()
    icon = pystray.Icon("calculadora", image, "Calculadora Financeira")
    icon.menu = pystray.Menu(
        pystray.MenuItem("Restaurar", restore_app),
        pystray.MenuItem("Sair", close_app)
    )
    icon.run()

def maximize_restore_app():
    global maximized, normal_geometry
    if not maximized:
        normal_geometry = root.geometry()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        maximized = True
    else:
        root.geometry(normal_geometry)
        maximized = False

root = tk.Tk()
root.overrideredirect(True)

root.update_idletasks()
center_window(root, WINDOW_WIDTH, WINDOW_HEIGHT)

title_bar = tk.Frame(root, bg='#2b2b2b', relief='raised', bd=0, height=30)
title_bar.pack(fill=tk.X)

button_close = tk.Canvas(title_bar, width=15, height=15, bg='#2b2b2b', highlightthickness=0)
button_close.pack(side=tk.LEFT, padx=6, pady=7)
button_close.create_oval(2, 2, 14, 14, fill='#ff5f57', outline='')
button_close.bind("<Button-1>", lambda e: close_app())

button_max = tk.Canvas(title_bar, width=15, height=15, bg='#2b2b2b', highlightthickness=0)
button_max.pack(side=tk.LEFT, padx=6, pady=7)
button_max.create_oval(2, 2, 14, 14, fill='#ffbd2e', outline='')
button_max.bind("<Button-1>", lambda e: maximize_restore_app())

button_min = tk.Canvas(title_bar, width=15, height=15, bg='#2b2b2b', highlightthickness=0)
button_min.pack(side=tk.LEFT, padx=6, pady=7)
button_min.create_oval(2, 2, 14, 14, fill='#27c93f', outline='')
button_min.bind("<Button-1>", lambda e: minimize_app())

title_bar.bind('<Button-1>', start_move)
title_bar.bind('<B1-Motion>', move_window)

root.bind("<Key>", tecla_pressionada)
root.protocol("WM_DELETE_WINDOW", close_app)

main_frame = tk.Frame(root, bg="#4B4B4B")
main_frame.pack(fill=tk.BOTH, expand=True)

display = tk.Entry(main_frame, width=20, font=("Consolas", 24, "bold"), bd=0,
                   bg="#1E1E1E", fg="#FFFFFF", justify='right', insertbackground='white')
display.grid(row=0, column=0, columnspan=4, padx=12, pady=(15, 5), ipady=45, sticky="we")

button_params = {
    "width": 5,
    "height": 2,
    "font": ("Consolas", 16, "bold"),
    "bd": 0,
    "fg": "#FFFFFF",
    "activebackground": "#6C6C6C",
    "activeforeground": "#FFFFFF",
}

colors = {
    "num": "#2E2E2E",
    "op": "#FF9500",
    "clear": "#FF3B30",
    "equals": "#34C759",
}

for col in range(4):
    main_frame.grid_columnconfigure(col, weight=1, uniform='col')

padx = 6
pady = 3

b1 = tk.Button(main_frame, text="1", bg=colors["num"], command=lambda: button_click(1), **button_params)
b1.grid(row=1, column=0, padx=padx, pady=pady, sticky="nsew")
b2 = tk.Button(main_frame, text="2", bg=colors["num"], command=lambda: button_click(2), **button_params)
b2.grid(row=1, column=1, padx=padx, pady=pady, sticky="nsew")
b3 = tk.Button(main_frame, text="3", bg=colors["num"], command=lambda: button_click(3), **button_params)
b3.grid(row=1, column=2, padx=padx, pady=pady, sticky="nsew")
b_plus = tk.Button(main_frame, text="+", bg=colors["op"], command=lambda: button_click("+"), **button_params)
b_plus.grid(row=1, column=3, padx=padx, pady=pady, sticky="nsew")

b4 = tk.Button(main_frame, text="4", bg=colors["num"], command=lambda: button_click(4), **button_params)
b4.grid(row=2, column=0, padx=padx, pady=pady, sticky="nsew")
b5 = tk.Button(main_frame, text="5", bg=colors["num"], command=lambda: button_click(5), **button_params)
b5.grid(row=2, column=1, padx=padx, pady=pady, sticky="nsew")
b6 = tk.Button(main_frame, text="6", bg=colors["num"], command=lambda: button_click(6), **button_params)
b6.grid(row=2, column=2, padx=padx, pady=pady, sticky="nsew")
b_minus = tk.Button(main_frame, text="-", bg=colors["op"], command=lambda: button_click("-"), **button_params)
b_minus.grid(row=2, column=3, padx=padx, pady=pady, sticky="nsew")

b7 = tk.Button(main_frame, text="7", bg=colors["num"], command=lambda: button_click(7), **button_params)
b7.grid(row=3, column=0, padx=padx, pady=pady, sticky="nsew")
b8 = tk.Button(main_frame, text="8", bg=colors["num"], command=lambda: button_click(8), **button_params)
b8.grid(row=3, column=1, padx=padx, pady=pady, sticky="nsew")
b9 = tk.Button(main_frame, text="9", bg=colors["num"], command=lambda: button_click(9), **button_params)
b9.grid(row=3, column=2, padx=padx, pady=pady, sticky="nsew")
b_multiply = tk.Button(main_frame, text="*", bg=colors["op"], command=lambda: button_click("*"), **button_params)
b_multiply.grid(row=3, column=3, padx=padx, pady=pady, sticky="nsew")

b0 = tk.Button(main_frame, text="0", bg=colors["num"], command=lambda: button_click(0), **button_params)
b0.grid(row=4, column=0, padx=padx, pady=pady, sticky="nsew")
b_clear = tk.Button(main_frame, text="C", bg=colors["clear"], command=clear, **button_params)
b_clear.grid(row=4, column=1, padx=padx, pady=pady, sticky="nsew")
b_equal = tk.Button(main_frame, text="=", bg=colors["equals"], command=equals, **button_params)
b_equal.grid(row=4, column=2, padx=padx, pady=pady, sticky="nsew")
b_divide = tk.Button(main_frame, text="/", bg=colors["op"], command=lambda: button_click("/"), **button_params)
b_divide.grid(row=4, column=3, padx=padx, pady=pady, sticky="nsew")

b_sqrt = tk.Button(main_frame, text="√", bg=colors["op"], command=lambda: button_click("√("), **button_params)
b_sqrt.grid(row=5, column=0, padx=padx, pady=(pady, 5), sticky="nsew")
b_open_paren = tk.Button(main_frame, text="(", bg=colors["op"], command=lambda: button_click("("), **button_params)
b_open_paren.grid(row=5, column=1, padx=padx, pady=(pady, 5), sticky="nsew")
b_close_paren = tk.Button(main_frame, text=")", bg=colors["op"], command=lambda: button_click(")"), **button_params)
b_close_paren.grid(row=5, column=2, padx=padx, pady=(pady, 5), sticky="nsew")
b_pow = tk.Button(main_frame, text="^", bg=colors["op"], command=lambda: button_click("^"), **button_params)
b_pow.grid(row=5, column=3, padx=padx, pady=(pady, 5), sticky="nsew")

# Inicia ícone da bandeja em thread separada para não travar app
threading.Thread(target=setup_tray_icon, daemon=True).start()

root.mainloop()
