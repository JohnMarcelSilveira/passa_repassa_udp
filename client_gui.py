import tkinter as tk
from tkinter import simpledialog, messagebox
import socket
import threading

HOST = 'localhost'
PORT = 10000

class GameClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Passa ou Repassa - Cliente")

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.nickname = simpledialog.askstring("Nickname", "Digite seu nickname:")
        if not self.nickname:
            self.root.destroy()
            return

        self.socket.sendto(self.nickname.encode(), (HOST, PORT))

        self.text_area = tk.Text(root, height=15, width=50, state='disabled', bg="lightyellow")
        self.text_area.pack(pady=10)

        self.input_frame = tk.Frame(root)
        self.input_frame.pack()

        self.option_var = tk.StringVar()
        self.option_entry = tk.Entry(self.input_frame, textvariable=self.option_var, width=5)
        self.option_entry.grid(row=0, column=0, padx=5)

        self.btn_responder = tk.Button(self.input_frame, text="RESPONDER", command=self.enviar_resposta)
        self.btn_responder.grid(row=0, column=1, padx=5)

        self.btn_passa = tk.Button(self.input_frame, text="PASSA", command=lambda: self.enviar_acao("PASSA"))
        self.btn_passa.grid(row=0, column=2, padx=5)

        self.btn_repassa = tk.Button(self.input_frame, text="REPASSA", command=lambda: self.enviar_acao("REPASSA"))
        self.btn_repassa.grid(row=0, column=3, padx=5)

        self.escutando = True
        threading.Thread(target=self.ouvir_servidor, daemon=True).start()

    def enviar_acao(self, acao):
        self.socket.sendto(acao.encode(), (HOST, PORT))

    def enviar_resposta(self):
        opcao = self.option_var.get().strip().upper()
        if opcao in ['A', 'B', 'C', 'D']:
            self.enviar_acao(f"RESPONDER - {opcao}")
            self.option_var.set("")
        else:
            messagebox.showerror("Erro", "Digite uma opção válida: A, B, C ou D.")

    def mostrar_mensagem(self, msg):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, msg + "\n")
        self.text_area.see(tk.END)
        self.text_area.configure(state='disabled')

    def ouvir_servidor(self):
        while self.escutando:
            try:
                msg, _ = self.socket.recvfrom(1024)
                self.mostrar_mensagem("[Servidor]: " + msg.decode())
            except:
                break

    def fechar(self):
        self.escutando = False
        self.socket.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GameClient(root)
    root.protocol("WM_DELETE_WINDOW", app.fechar)
    root.mainloop()
