class PDU:
    def __init__(self, conteudo, tamanho_cabecalho=0):
        self.conteudo = conteudo
        self.tamanho = (conteudo.tamanho if isinstance(conteudo, PDU) else len(str(conteudo))) + tamanho_cabecalho

class Mensagem(PDU):
    def __init__(self, texto): super().__init__(texto, 4)

class Segmento(PDU):
    def __init__(self, mensagem, p_origem, p_destino, seq=1, total=1):
        super().__init__(mensagem, 8) 
        self.porta_origem = p_origem
        self.porta_destino = p_destino
        self.seq = seq
        self.total = total

class Pacote(PDU):
    def __init__(self, segmento, ip_origem, ip_destino):
        super().__init__(segmento, 20) 
        self.ip_origem = ip_origem
        self.ip_destino = ip_destino

class Quadro(PDU):
    def __init__(self, pacote, mac_origem, mac_destino, id_quadro):
        super().__init__(pacote, 18) # 14 header + 4 trailer
        self.mac_origem = mac_origem
        self.mac_destino = mac_destino
        self.id_quadro = id_quadro
        self.verificacao_erro = True