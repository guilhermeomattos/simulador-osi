# Simulador do Modelo OSI

**Instituição:** Faculdade Engenheiro Salvador Arena (FESA)  
**Disciplina:** Comunicação de Dados  
**Professor:** Prof. Vinícius S. Borges  
**Semestre:** 7° Semestre  

**Autoria (Equipe):**
* Guilherme de Oliveira Mattos - RA: 082230009
* Luigi Guilherme Pereira Silva - RA: 082230025
* Paulo Henrique de Carvalho Santos - RA: 082230006
* Pedro Henrique de Holanda Carvalho - RA: 082230005
* Tayson Moises Costa do Carmo - RA: 082230008

## Descrição do Projeto
Este projeto consiste em um simulador visual do Modelo OSI de sete camadas. O sistema demonstra o transporte passo a passo de uma mensagem entre computadores (H1 a H5) através de uma rede com múltiplos roteadores (R1 a R4). O simulador evidencia os processos de encapsulamento, desencapsulamento, as decisões de roteamento da Camada 3 por prefixo de rede e a recriação do quadro físico (endereços MAC) a cada salto na Camada 2.

## Como Executar
Clique duas vezes no arquivo `SimuladorOSI.exe`. Não é necessário instalar o Python ou configurar qualquer ambiente de desenvolvimento na máquina.

## Requisitos de Ambiente
* O simulador foi desenvolvido em **Python 3**.
* Interface gráfica construída utilizando a biblioteca nativa **Tkinter**.
* Executável independente gerado via **PyInstaller** (não requer dependências externas para execução).

## Estrutura do Repositório

    simulador-osi/
    |-- .gitignore
    |-- main.py
    |-- README.md
    |-- README_GRUPO.md
    |-- SimuladorOSI.exe
    |-- topologia.json
    |-- docs/
    |   |-- documentacao_projeto.pdf
    |   |-- especificacao.pdf
    |   |-- guia_de_documentacao.pdf
    |   |-- tutorial_execucao.pdf
    |   `-- tutorial_uso.pdf
    `-- simulador/
        |-- camadas.py
        |-- dispositivos.py
        |-- motor.py
        |-- pdu.py
        |-- rede.py
        `-- visual.py

## Arquivos de Código
* `SimuladorOSI.exe`: Executável principal compilado e pronto para uso.
* `topologia.json`: Arquivo de configuração dinâmico lido no momento da execução, contendo redes, endereços lógicos/físicos e custos de enlace.
* `simulador/camadas.py`: Classes estritamente isoladas para as sete camadas de rede.
* `simulador/dispositivos.py`: Definição de Computadores (L1-L7) e Roteadores (L1-L3).
* `simulador/motor.py`: Relógio central, registro de eventos e resolução inteligente de rotas.
* `simulador/pdu.py`: Formatação da Unidade de Dados de Protocolo (PDU) e cabeçalhos.
* `simulador/rede.py`: Lógica de leitura e adaptação de caminhos para o ambiente empacotado.
* `simulador/visual.py`: Interface gráfica interativa desenhada em Tkinter.
* `main.py`: Ponto de entrada do sistema que interliga o motor à visualização.

## Funcionalidades
| O que faz | Onde está implementado |
| :--- | :--- |
| Interface gráfica, controles e mapa de rede | `simulador/visual.py` |
| Laço de simulação, log de eventos e cálculo de eficiência | `simulador/motor.py` |
| Criação e estruturação da unidade de dados (PDU) | `simulador/pdu.py` |
| Encapsulamento, desencapsulamento e segmentação | `simulador/camadas.py` |
| Encaminhamento e validação de rotas da Camada 3 | `simulador/motor.py` e `simulador/camadas.py` |
| Leitura da topologia dinâmica e adaptada para executável | `simulador/rede.py` |
| Isolamento restrito de escopo entre Computadores e Roteadores | `simulador/dispositivos.py` |

## Documentação Oficial
* [Tutorial de Execução](./docs/tutorial_execucao.pdf)
* [Tutorial de Uso](./docs/tutorial_uso.pdf)
* [Documentação Técnica](./docs/documentacao_projeto.pdf)

## Por onde começar
1. Abra o arquivo `SimuladorOSI.exe` e siga o **Tutorial de Execução** para validar a abertura do programa.
2. Reproduza os cenários interativos (como o Cenário C2) utilizando o **Tutorial de Uso**.
3. Consulte a **Documentação Técnica** para compreender as decisões de arquitetura e a separação restrita de camadas no código.