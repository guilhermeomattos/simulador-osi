from simulador.dispositivos import Computador, Roteador
from simulador.rede import LeitorTopologia

class MotorSimulacao:
    def __init__(self):
        self.passo = 1
        self.eventos = []
        self.dispositivos = {}
        self.contador_quadros = 1
        self.octetos_transmitidos = 0
        self.octetos_dados = 0
        self.carregar_dados()

    def carregar_dados(self):
        dados = LeitorTopologia.carregar()
        for nome, i in dados["computadores"].items():
            self.dispositivos[nome] = Computador(self, nome, i["ip"], i["mac"], i["gateway"])
        for nome, i in dados["roteadores"].items():
            self.dispositivos[nome] = Roteador(self, nome, i["mac"], i["rotas"])

    def registrar(self, dispositivo, camada, acao, descricao, tamanho):
        linha = f"{self.passo:03d} | {dispositivo} | L{camada} | {acao} | {descricao} | {tamanho} B"
        self.eventos.append(linha)
        self.passo += 1

    def obter_novo_id_quadro(self):
        id_atual = self.contador_quadros
        self.contador_quadros += 1
        return id_atual

    def obter_disp_por_mac(self, mac):
        return next((d for d in self.dispositivos.values() if d.mac == mac), None)

    def obter_mac_por_ip(self, ip):
        return next((d.mac for d in self.dispositivos.values() if getattr(d, 'ip', None) == ip or (hasattr(d, 'rotas') and d.mac)), None)

    def iniciar_transmissao(self, origem_nome, destino_ip, p_origem, p_destino, texto):
        self.eventos.clear()
        self.passo = 1
        self.octetos_transmitidos = 0
        self.octetos_dados = len(texto)
        
        origem = self.dispositivos[origem_nome]
        origem.camadas[7].descer(texto, destino_ip, p_origem, p_destino)
        
        eficiencia = (self.octetos_dados / self.octetos_transmitidos) * 100 if self.octetos_transmitidos > 0 else 0
        self.eventos.append(f"--- | SISTEMA | -- | RESULTADO | Úteis: {self.octetos_dados}B, Total: {self.octetos_transmitidos}B, Eficiência: {eficiencia:.1f}% | --")