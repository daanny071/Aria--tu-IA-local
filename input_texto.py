import tkinter as tk
import threading

resultado = [None]

def pedir_texto():
    def _abrir():
        root = tk.Tk()
        root.title("Aria - Escribe tu mensaje")
        root.attributes("-topmost", True)
        root.configure(bg="#1e1e1e")
        root.resizable(False, False)

        ancho = 400
        alto = 100
        x = root.winfo_screenwidth() // 2 - ancho // 2
        y = root.winfo_screenheight() // 2 - alto // 2
        root.geometry(f"{ancho}x{alto}+{x}+{y}")

        label = tk.Label(root, text="¿Qué le dices a Aria?", bg="#1e1e1e", fg="#00c864",
                        font=("Segoe UI", 10, "bold"))
        label.pack(pady=(10, 0))

        entrada = tk.Entry(root, width=50, font=("Segoe UI", 10),
                          bg="#2d2d2d", fg="white", insertbackground="white")
        entrada.pack(pady=5, padx=10)
        entrada.focus()

        def enviar(event=None):
            resultado[0] = entrada.get()
            root.destroy()

        def cancelar(event=None):
            resultado[0] = None
            root.destroy()

        entrada.bind("<Return>", enviar)
        entrada.bind("<Escape>", cancelar)

        root.mainloop()

    hilo = threading.Thread(target=_abrir)
    hilo.start()
    hilo.join()
    return resultado[0]