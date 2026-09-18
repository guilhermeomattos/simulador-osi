import json
import os
import sys
 
class LeitorTopologia:
    @staticmethod
    def carregar(arquivo="topologia.json"):
        if getattr(sys, 'frozen', False):
            diretorio_base = os.path.dirname(sys.executable)
        else:
            diretorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
           
        caminho = os.path.join(diretorio_base, arquivo)
       
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)