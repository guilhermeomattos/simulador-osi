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

    