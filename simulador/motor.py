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
        self.flag_erro_c6 = False
        self.carregar_dados()

    def carregar_dados(self):
        self.dispositivos.clear()
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
        for d in self.dispositivos.values():
            if getattr(d, 'ip', None) == ip:
                return d.mac
                
        prefixo = ip.rsplit('.', 1)[0]
        if prefixo == "10.0.1": return self.dispositivos["R1"].mac
        if prefixo == "10.0.2": return self.dispositivos["R2"].mac
        if prefixo == "10.0.3": return self.dispositivos["R3"].mac
        
        return None

    def simular_cenario(self, cenario):
        self.eventos.clear()
        self.passo = 1
        self.octetos_transmitidos = 0
        self.octetos_dados = 0
        self.flag_erro_c6 = False
        self.carregar_dados() # Restaura topologia limpa

        if "C1" in cenario:
            self.iniciar_transmissao("H1", "10.0.1.11", 5000, 80, "Entrega Local")
        elif "C2" in cenario:
            self.iniciar_transmissao("H1", "10.0.3.10", 5210, 443, "Mensagem do navegador")
        elif "C3" in cenario:
            self.iniciar_transmissao("H1", "10.0.3.10", 5001, 80, "Req1")
            self.iniciar_transmissao("H2", "10.0.3.10", 5002, 80, "Req2")
        elif "C4" in cenario:
            del self.dispositivos["R1"].rotas["10.0.3.0/24"]
            self.dispositivos["R1"].rotas["10.0.3.0/24"] = {"prox_salto": "R2", "ip_prox": "10.0.12.2", "mac_prox": "BB:00:00:00:02:00"}
            self.eventos.append(f"--- | SISTEMA | -- | AVISO | Enlace R1-R4 caiu! Nova rota via R2 inserida. | --")
            self.passo += 1
            self.iniciar_transmissao("H1", "10.0.3.10", 5210, 443, "Mensagem")
        elif "C5" in cenario:
            self.iniciar_transmissao("H1", "10.0.9.10", 5210, 443, "Para IP Inexistente")
        elif "C6" in cenario:
            self.flag_erro_c6 = True
            self.iniciar_transmissao("H1", "10.0.3.10", 5210, 443, "Msg com erro CRC")
        elif "C7" in cenario:
            self.iniciar_transmissao("H1", "10.0.3.10", 5210, 443, "Esta_mensagem_e_muito_longa_e_vai_ser_fragmentada_obrigatoriamente")
            
        eficiencia = (self.octetos_dados / self.octetos_transmitidos) * 100 if self.octetos_transmitidos > 0 else 0
        self.eventos.append(f"--- | SISTEMA | -- | RESULTADO | Úteis: {self.octetos_dados}B, Total: {self.octetos_transmitidos}B, Eficiência: {eficiencia:.1f}% | --")

    def iniciar_transmissao(self, origem_nome, destino_ip, p_origem, p_destino, texto):
        self.octetos_dados += len(texto)
        origem = self.dispositivos[origem_nome]
        origem.camadas[7].descer(texto, destino_ip, p_origem, p_destino)