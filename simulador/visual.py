import tkinter as tk
from tkinter import ttk, filedialog

class InterfaceSimulador:
    def __init__(self, motor):
        self.motor = motor
        self.root = tk.Tk()
        self.root.title("Simulador OSI - Comunicação de Dados")
        self.root.geometry("1000x700")
        
        self.evento_atual = 0
        self.rodando = False
        self.velocidade_ms = 1000
        self.modo_tcp = False
        
        self.construir()
        self.desenhar_mapa()
        self.atualizar_pilha(None, None)

    def construir(self):
        frame_ctrl = tk.Frame(self.root, pady=10)
        frame_ctrl.pack(fill=tk.X)
        tk.Button(frame_ctrl, text="Executar C2 (H1->H4)", command=self.simular).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_ctrl, text="Passo a Passo", command=self.passo).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_ctrl, text="Contínuo", command=self.continuo).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_ctrl, text="Pausar", command=self.pausar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_ctrl, text="Alternar Pilha", command=self.alternar).pack(side=tk.LEFT, padx=15)
        
        frame_meio = tk.Frame(self.root)
        frame_meio.pack(fill=tk.BOTH, expand=True)
        
        self.canvas_mapa = tk.Canvas(frame_meio, bg="white", width=600)
        self.canvas_mapa.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.canvas_pilha = tk.Canvas(frame_meio, bg="#f9f9f9", width=300)
        self.canvas_pilha.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        frame_base = tk.Frame(self.root)
        frame_base.pack(fill=tk.BOTH, expand=True)
        
        frame_info = tk.Frame(frame_base)
        frame_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.lbl_logico = tk.Label(frame_info, text="Endereços Lógicos (Origem -> Destino): --", fg="blue", font=("Arial", 11, "bold"))
        self.lbl_logico.pack(anchor="w", pady=5)
        self.lbl_fisico = tk.Label(frame_info, text="Endereços Físicos (Salto Atual): --", fg="green", font=("Arial", 11, "bold"))
        self.lbl_fisico.pack(anchor="w", pady=5)
        
        self.log = tk.Text(frame_base, height=12, width=60)
        self.log.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def desenhar_mapa(self):
        self.canvas_mapa.delete("all")
        nodes = {"H1": (50, 50), "H2": (50, 150), "R1": (150, 100), "R4": (250, 50), 
                 "R2": (250, 150), "R3": (350, 100), "H4": (450, 50), "H5": (450, 150), "H3": (250, 250)}
        links = [("H1","R1"), ("H2","R1"), ("R1","R4"), ("R1","R2"), ("R4","R3"), ("R2","R3"), ("R2","H3"), ("R3","H4"), ("R3","H5")]
        
        for o, d in links:
            self.canvas_mapa.create_line(nodes[o][0], nodes[o][1], nodes[d][0], nodes[d][1], fill="gray", width=2)
        for n, (x, y) in nodes.items():
            cor = "lightblue" if "H" in n else "lightcoral"
            self.canvas_mapa.create_oval(x-20, y-20, x+20, y+20, fill=cor)
            self.canvas_mapa.create_text(x, y, text=n, font=("Arial", 10, "bold"))

    def atualizar_pilha(self, dispositivo, camada):
        self.canvas_pilha.delete("all")
        if not dispositivo: return
        
        self.canvas_pilha.create_text(150, 20, text=f"Pilha: {dispositivo}", font=("Arial", 12, "bold"))
        camadas = ["3 Rede", "2 Enlace", "1 Física"] if "R" in dispositivo else (
            ["Aplicação (L5-L7)", "4 Transporte", "3 Rede", "2 Enlace", "1 Física"] if self.modo_tcp else 
            ["7 Aplicação", "6 Apresentação", "5 Sessão", "4 Transporte", "3 Rede", "2 Enlace", "1 Física"])
        
        y = 50 if "H" in dispositivo else 150
        for c in camadas:
            num = int(c.split()[0]) if c[0].isdigit() else 7
            cor = "yellow" if num == camada or (self.modo_tcp and num==7 and camada in [5,6,7]) else "#e6e6fa"
            self.canvas_pilha.create_rectangle(50, y, 250, y+30, fill=cor)
            self.canvas_pilha.create_text(150, y+15, text=c)
            y += 35

    def simular(self):
        self.log.delete(1.0, tk.END)
        self.motor.iniciar_transmissao("H1", "10.0.3.10", 5210, 443, "Mensagem do navegador")
        self.evento_atual = 0
        self.rodando = False
        self.passo()

    def alternar(self):
        self.modo_tcp = not self.modo_tcp
        self.atualizar_pilha(None, None)

    def pausar(self): self.rodando = False
    def continuo(self): 
        self.rodando = True
        self.executar()
    def passo(self):
        self.rodando = False
        self.executar()

    def executar(self):
        if self.evento_atual < len(self.motor.eventos):
            evt = self.motor.eventos[self.evento_atual]
            self.log.insert(tk.END, evt + "\n")
            self.log.see(tk.END)
            
            if "SISTEMA" not in evt:
                partes = [p.strip() for p in evt.split('|')]
                disp, cam, acao, desc = partes[1], int(partes[2].replace('L','')), partes[3], partes[4]
                self.atualizar_pilha(disp, cam)
                
                if acao == "ENCAPSULA": self.lbl_logico.config(text=f"Endereços Lógicos (Origem -> Destino): {desc}")
                if acao == "ENQUADRA": self.lbl_fisico.config(text=f"Endereços Físicos (Salto Atual): {desc.split(',')[0]}")

            self.evento_atual += 1
            if self.rodando: self.root.after(self.velocidade_ms, self.executar)
        else: self.rodando = False