import tkinter as tk
from tkinter import ttk, filedialog

class InterfaceSimulador:
    def __init__(self, motor):
        self.motor = motor
        self.root = tk.Tk()
        self.root.title("Simulador OSI - Comunicação de Dados")
        self.root.state('zoomed')
        
        self.evento_atual = 0
        self.rodando = False
        self.modo_tcp = False
        self.velocidade_ms = 1000
        
        self.dispositivo_recente = "H1"
        self.camada_recente = 7
        
        self.construir()
        self.desenhar_mapa(None)
        self.atualizar_pilha("H1", 7)

    def construir(self):
        frame_ctrl = tk.Frame(self.root, pady=5)
        frame_ctrl.pack(fill=tk.X, padx=10)
        
        tk.Label(frame_ctrl, text="Cenário:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.combo_cenario = ttk.Combobox(frame_ctrl, state="readonly", width=35)
        self.combo_cenario['values'] = [
            "C1. Entrega Direta (H1->H2)", "C2. Caso Central (H1->H4)", 
            "C3. Demultiplexação (H1 e H2 -> H4)", "C4. Falha de Enlace (R1-R4 Caiu)",
            "C5. Destino Inalcançável (Sem rota)", "C6. Erro de Transmissão (CRC)", 
            "C7. Mensagem Longa (Segmentação)"
        ]
        self.combo_cenario.current(1)
        self.combo_cenario.pack(side=tk.LEFT, padx=5)
        tk.Button(frame_ctrl, text="Executar Cenário", command=self.simular_cenario, bg="lightblue").pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_ctrl, text="  |  Velocidade:").pack(side=tk.LEFT)
        self.combo_vel = ttk.Combobox(frame_ctrl, values=["Lento", "Normal", "Rápido"], state="readonly", width=8)
        self.combo_vel.current(1)
        self.combo_vel.bind("<<ComboboxSelected>>", self.mudar_velocidade)
        self.combo_vel.pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_ctrl, text="Passo a Passo", command=self.passo).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_ctrl, text="Contínuo", command=self.continuo).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_ctrl, text="Pausar", command=self.pausar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_ctrl, text="Alternar Pilha OSI/TCP", command=self.alternar).pack(side=tk.LEFT, padx=15)
        tk.Button(frame_ctrl, text="Salvar Registo", command=self.salvar_log, bg="lightgreen").pack(side=tk.RIGHT, padx=10)

        frame_manual = tk.Frame(self.root, pady=5)
        frame_manual.pack(fill=tk.X, padx=10)
        
        tk.Label(frame_manual, text="Envio Personalizado:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_manual, text="Origem:").pack(side=tk.LEFT, padx=2)
        self.combo_origem = ttk.Combobox(frame_manual, state="readonly", width=5)
        self.combo_origem['values'] = ["H1", "H2", "H3", "H4", "H5"]
        self.combo_origem.current(0)
        self.combo_origem.pack(side=tk.LEFT, padx=2)
        
        tk.Label(frame_manual, text="Destino:").pack(side=tk.LEFT, padx=2)
        self.combo_destino = ttk.Combobox(frame_manual, state="readonly", width=5)
        self.combo_destino['values'] = ["H1", "H2", "H3", "H4", "H5"]
        self.combo_destino.current(3)
        self.combo_destino.pack(side=tk.LEFT, padx=2)
        
        tk.Label(frame_manual, text="Mensagem:").pack(side=tk.LEFT, padx=2)
        self.entry_msg = tk.Entry(frame_manual, width=35)
        self.entry_msg.insert(0, "Escreva a sua mensagem aqui")
        self.entry_msg.pack(side=tk.LEFT, padx=2)
        
        tk.Button(frame_manual, text="Enviar Manualmente", command=self.simular_manual, bg="#ffebcd").pack(side=tk.LEFT, padx=10)

        frame_meio = tk.Frame(self.root)
        frame_meio.pack(fill=tk.BOTH, expand=True)
        
        self.canvas_mapa = tk.Canvas(frame_meio, bg="white", width=600)
        self.canvas_mapa.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.canvas_pilha = tk.Canvas(frame_meio, bg="#f9f9f9", width=300)
        self.canvas_pilha.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        frame_base = tk.Frame(self.root)
        frame_base.pack(fill=tk.BOTH, expand=True)
        
        frame_info = tk.Frame(frame_base)
        frame_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        self.lbl_logico = tk.Label(frame_info, text="Endereços Lógicos (Origem -> Destino): --", fg="blue", font=("Arial", 11, "bold"))
        self.lbl_logico.pack(anchor="w", pady=5)
        self.lbl_fisico = tk.Label(frame_info, text="Endereços Físicos (Salto Atual): --", fg="green", font=("Arial", 11, "bold"))
        self.lbl_fisico.pack(anchor="w", pady=5)
        
        tk.Label(frame_info, text="Unidade de Dados Corrente (V3):", font=("Arial", 9, "italic")).pack(anchor="w", pady=(10, 0))
        self.canvas_pdu = tk.Canvas(frame_info, height=80, bg="#eaeaea")
        self.canvas_pdu.pack(fill=tk.X, pady=5)
        
        self.log = tk.Text(frame_base, height=12, width=65)
        self.log.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def desenhar_mapa(self, dispositivo_ativo):
        self.canvas_mapa.delete("all")
        nodes = {"H1": (50, 50), "H2": (50, 150), "R1": (150, 100), "R4": (250, 50), 
                 "R2": (250, 150), "R3": (350, 100), "H4": (450, 50), "H5": (450, 150), "H3": (250, 250)}
        links = [("H1","R1"), ("H2","R1"), ("R1","R4"), ("R1","R2"), ("R4","R3"), ("R2","R3"), ("R2","H3"), ("R3","H4"), ("R3","H5")]
        
        for o, d in links:
            self.canvas_mapa.create_line(nodes[o][0], nodes[o][1], nodes[d][0], nodes[d][1], fill="gray", width=2)
            
        for n, (x, y) in nodes.items():
            if n == dispositivo_ativo:
                cor = "yellow"
                borda = 3
            else:
                cor = "lightblue" if "H" in n else "lightcoral"
                borda = 1
                
            self.canvas_mapa.create_oval(x-20, y-20, x+20, y+20, fill=cor, width=borda)
            self.canvas_mapa.create_text(x, y, text=n, font=("Arial", 10, "bold"))

    def atualizar_pilha(self, dispositivo, camada):
        if dispositivo:
            self.dispositivo_recente = dispositivo
            self.camada_recente = camada
        else:
            dispositivo = self.dispositivo_recente
            camada = self.camada_recente

        self.canvas_pilha.delete("all")
        if not dispositivo: return
        
        modelo_str = "TCP/IP" if self.modo_tcp and "H" in dispositivo else "OSI"
        titulo_texto = f"Pilha: {dispositivo} [{modelo_str}]" if "H" in dispositivo else f"Pilha: {dispositivo}"
        self.canvas_pilha.create_text(150, 20, text=titulo_texto, font=("Arial", 11, "bold"))
        
        camadas = ["3 Rede", "2 Enlace", "1 Física"] if "R" in dispositivo else (
            ["Aplicação (L5-L7)", "4 Transporte", "3 Rede", "2 Enlace", "1 Física"] if self.modo_tcp else 
            ["7 Aplicação", "6 Apresentação", "5 Sessão", "4 Transporte", "3 Rede", "2 Enlace", "1 Física"])
        
        y = 50 if "H" in dispositivo else 150
        for c in camadas:
            num = int(c.split()[0]) if c.split()[0].isdigit() else 7
            destacada = False
            if camada is not None:
                if num == camada or (self.modo_tcp and num == 7 and camada in [5, 6, 7]):
                    destacada = True
            cor = "yellow" if destacada else "#e6e6fa"
            
            self.canvas_pilha.create_rectangle(50, y, 250, y+30, fill=cor)
            self.canvas_pilha.create_text(150, y+15, text=c)
            y += 35

    def desenhar_pdu(self, camada_atual):
        self.canvas_pdu.delete("all")
        if not camada_atual: return
        
        x, y, w, h = 10, 20, 60, 40
        cores = {2: "#ffd700", 3: "#87ceeb", 4: "#98fb98", "Dados": "#d3d3d3"}
        
        if camada_atual <= 2:
            self.canvas_pdu.create_rectangle(x, y, x+w, y+h, fill=cores[2])
            self.canvas_pdu.create_text(x+w/2, y+h/2, text="L2 Hdr")
            x += w
        if camada_atual <= 3:
            self.canvas_pdu.create_rectangle(x, y, x+w, y+h, fill=cores[3])
            self.canvas_pdu.create_text(x+w/2, y+h/2, text="L3 Hdr")
            x += w
        if camada_atual <= 4:
            self.canvas_pdu.create_rectangle(x, y, x+w, y+h, fill=cores[4])
            self.canvas_pdu.create_text(x+w/2, y+h/2, text="L4 Hdr")
            x += w
            
        self.canvas_pdu.create_rectangle(x, y, x+w*2, y+h, fill=cores["Dados"])
        self.canvas_pdu.create_text(x+w, y+h/2, text="Dados (Payload)")
        x += w*2
        
        if camada_atual <= 2:
            self.canvas_pdu.create_rectangle(x, y, x+w, y+h, fill=cores[2])
            self.canvas_pdu.create_text(x+w/2, y+h/2, text="L2 FCS")

    def simular_cenario(self):
        self.log.delete(1.0, tk.END)
        cenario = self.combo_cenario.get()
        self.motor.simular_cenario(cenario)
        self.iniciar_ciclo_animacao()

    def simular_manual(self):
        self.log.delete(1.0, tk.END)
        self.motor.eventos.clear()
        self.motor.passo = 1
        self.motor.octetos_transmitidos = 0
        self.motor.octetos_dados = 0
        self.motor.flag_erro_c6 = False
        self.motor.carregar_dados()
        
        origem_nome = self.combo_origem.get()
        destino_nome = self.combo_destino.get()
        texto = self.entry_msg.get()
        
        ip_destino = self.motor.dispositivos[destino_nome].ip
        self.motor.iniciar_transmissao(origem_nome, ip_destino, 5000, 80, texto)
        
        eficiencia = (self.motor.octetos_dados / self.motor.octetos_transmitidos) * 100 if self.motor.octetos_transmitidos > 0 else 0
        self.motor.eventos.append(f"--- | SISTEMA | -- | RESULTADO | Úteis: {self.motor.octetos_dados}B, Total: {self.motor.octetos_transmitidos}B, Eficiência: {eficiencia:.1f}% | --")
        
        self.iniciar_ciclo_animacao()

    def iniciar_ciclo_animacao(self):
        self.evento_atual = 0
        self.rodando = False
        self.passo()

    def alternar(self):
        self.modo_tcp = not self.modo_tcp
        self.atualizar_pilha(None, None)

    def mudar_velocidade(self, event):
        v = self.combo_vel.get()
        self.velocidade_ms = 2000 if v == "Lento" else 500 if v == "Rápido" else 1000

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
                self.desenhar_pdu(cam)
                self.desenhar_mapa(disp)
                
                if acao == "ENCAPSULA": self.lbl_logico.config(text=f"Endereços Lógicos (Origem -> Destino): {desc}")
                if acao == "ENQUADRA": self.lbl_fisico.config(text=f"Endereços Físicos (Salto Atual): {desc.split(',')[0]}")

            self.evento_atual += 1
            if self.rodando: self.root.after(self.velocidade_ms, self.executar)
        else: 
            self.rodando = False
            self.desenhar_mapa(None)

    def salvar_log(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if caminho:
            with open(caminho, 'w', encoding='utf-8') as f:
                f.write(self.log.get(1.0, tk.END))