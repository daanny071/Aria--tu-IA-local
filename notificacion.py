import tkinter as tk
import threading

def mostrar_notificacion(texto, duracion=None):
    def _mostrar():
        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.attributes("-alpha", 0.9)

        ancho_pantalla = root.winfo_screenwidth()
        alto_pantalla = root.winfo_screenheight()

        frame = tk.Frame(root, bg="#1e1e1e", padx=15, pady=10)
        frame.pack()

        titulo = tk.Label(frame, text="🤖 Aria", bg="#1e1e1e", fg="#00c864",
                         font=("Segoe UI", 10, "bold"))
        titulo.pack(anchor="w")

        # Limita el texto a 60 caracteres por línea
        palabras = texto.split()
        lineas = []
        linea_actual = ""
        for palabra in palabras:
            if len(linea_actual + " " + palabra) <= 60:
                linea_actual += " " + palabra if linea_actual else palabra
            else:
                lineas.append(linea_actual)
                linea_actual = palabra
        if linea_actual:
            lineas.append(linea_actual)
        texto_formateado = "\n".join(lineas)

        mensaje = tk.Label(frame, text=texto_formateado, bg="#1e1e1e", fg="white",
                          font=("Segoe UI", 10), justify="left", wraplength=300)
        mensaje.pack(anchor="w", pady=(5, 0))

        root.update_idletasks()
        ancho = root.winfo_width()
        alto = root.winfo_height()
        x = ancho_pantalla - ancho - 20
        y = alto_pantalla - alto - 60
        root.geometry(f"+{x}+{y}")

        if duracion:
            root.after(duracion * 1000, root.destroy)

        root.mainloop()

    hilo = threading.Thread(target=_mostrar, daemon=True)
    hilo.start()
    return hilo