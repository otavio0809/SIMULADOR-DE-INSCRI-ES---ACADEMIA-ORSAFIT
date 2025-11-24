from datetime import datetime
from abc import ABC, abstractmethod


# CLASSES DE PLANO

class Plano(ABC):
    def __init__(self, nome, preco, fidelidade_meses, duracao_meses):
        self.nome = nome
        self.preco = preco
        self.fidelidade_meses = fidelidade_meses
        self.duracao_meses = duracao_meses

    @abstractmethod
    def beneficios(self):   
        pass
    

    @abstractmethod
    def calcular_multa_cancelamento(self):
        """Calcula a multa a ser paga em caso de cancelamento prematuro."""
        pass

# PADRÃO DE PROJETO FACTORY PARA PLANOS

class PlanoFactory:
    @staticmethod
    def criar_plano(tipo):
        if tipo == 1:
            return PlanoSimples("Básico", 150.00, 0, 1)
        elif tipo == 2:
            return PlanoPremium("Premium", 120.90, 0, 3)
        elif tipo == 3:
            return PlanoBlack("Black", 99.90, 12, 12)
        else:
            return None

class PlanoSimples(Plano):
    def beneficios(self):
        return "Acesso em horário comercial."

    def calcular_multa_cancelamento(self):
        return 0.0

class PlanoPremium(Plano):
    def beneficios(self):
        return "Acesso total + musculação + aeróbico."


    def calcular_multa_cancelamento(self):
        return 0.0

class PlanoBlack(Plano):
    def beneficios(self):
        return "Acesso total + personal + salas VIP."
    

    def calcular_multa_cancelamento(self):
        if self.fidelidade_meses > 0:
            return self.preco
        return 0.0


# CLASSE ALUNO

class Aluno:
    def __init__(self, nome, cpf, telefone):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone



#Inscrição
class Inscricao:
    def __init__(self, aluno, plano, data_inscricao, status, processador_pagamento):
        self.aluno = aluno
        self.plano = plano
        self.data_inscricao = data_inscricao
        self._status = status
        self.processador = processador_pagamento 

    @property
    def status(self):
        return self._status

    def processar_cobranca_inicial(self):
        """Usa a estratégia de pagamento associada para processar o valor do plano."""
        print(f"\nTentando cobrar R${self.plano.preco:.2f}...")
        self.processador.processar(self.plano.preco)


# PADRÃO DE PROJETO BIULDER

class InscricaoBuilder:
    def __init__(self):
        self._aluno = None
        self._plano = None
        self._data = datetime.now()
        self._status = "ATIVA"

        self._processador_pagamento = None 

    def com_aluno(self, aluno):
        self._aluno = aluno
        return self

    def com_plano(self, plano):
        self._plano = plano
        return self

    def com_processador(self, processador):
        self._processador_pagamento = processador
        return self

    def build(self):
        return Inscricao(
            self._aluno, 
            self._plano, 
            self._data, 
            self._status, 
            self._processador_pagamento
        )


class EstrategiaPagamento(ABC):
    @abstractmethod
    def processar(self, valor):
        """Define o método de processamento de pagamento."""
        pass


class ProcessadorPix(EstrategiaPagamento):
    def processar(self, valor):
        desconto = valor * 0.05  # 5% de desconto para PIX
        valor_final = valor - desconto
        print(f"✅ Pagamento via PIX. Desconto de R${desconto:.2f} aplicado.")
        print(f"   Valor final cobrado: R${valor_final:.2f}")

class ProcessadorCartao(EstrategiaPagamento):
    def processar(self, valor):
        taxa = valor * 0.03  # 3% de taxa para Cartão
        valor_final = valor + taxa
        print(f"💳 Pagamento via Cartão. Taxa de R${taxa:.2f} adicionada.")
        print(f"   Valor final cobrado: R${valor_final:.2f}")

#USANDO LISTA PARA ARMAZENAR DADOS DE PLANOS, ALUNOS E INSCRIÇÕES

alunos = []
inscricoes = []


# FUNÇÕES DO MENU


def criar_inscricao():
    print("\n     Criar Inscrição     ")
    nome = input("Nome do aluno: ")
    cpf = input("CPF: ")
    telefone = input("Telefone: ")

    aluno = Aluno(nome, cpf, telefone)
    alunos.append(aluno)

    print("\nEscolha o plano:")
    print("1 - Básico")
    print("2 - Premium")
    print("3 - Black")
    try:
        tipo = int(input("> "))
    except ValueError:
        print("Opção de plano inválida.")
        return

    plano = PlanoFactory.criar_plano(tipo)
    if not plano:
        print("Plano não encontrado.")
        return

    
    print(f"\nPlano selecionado: {plano.nome} - R${plano.preco:.2f}")
    
    print("\nEscolha o Processador de Pagamento (Strategy):")
    print("1 - PIX (5% Desconto)")
    print("2 - Cartão (3% Taxa)")
    metodo_escolhido = input("> ")

    if metodo_escolhido == '1':
        processador = ProcessadorPix()
        metodo_nome = "PIX"
    elif metodo_escolhido == '2':
        processador = ProcessadorCartao()
        metodo_nome = "Cartão"
    else:
        print("Método de pagamento inválido.")
        return


    inscricao = (
        InscricaoBuilder()
        .com_aluno(aluno)
        .com_plano(plano)

        .com_processador(processador) 
        .build()
    )

    inscricao.processar_cobranca_inicial()

    inscricoes.append(inscricao)

    print("\n Inscrição concluída com sucesso!")
    print(f"Aluno: {aluno.nome} | Plano: {plano.nome} | Status: {inscricao.status}")


def listar_inscricoes():
    print("\n   Lista de Inscrições   ")
    for i, ins in enumerate(inscricoes):

        print(f"{i+1} - {ins.aluno.nome} | {ins.plano.nome} | Status: {ins.status}")


def cancelar_inscricao():
    listar_inscricoes()
    try:
        escolha = int(input("\nDigite o número da inscrição para cancelar: ")) - 1
        
        if 0 <= escolha < len(inscricoes):
            ins = inscricoes[escolha]
            

            multa = ins.plano.calcular_multa_cancelamento()
            
            if ins.plano.fidelidade_meses > 0 and multa > 0:
                print(f"\n⚠️ Plano com fidelidade. Multa de R${multa:.2f} aplicada.")


            ins._status = "CANCELADA"
            print("\n   Inscrição cancelada com sucesso!   ")
        else:
            print("Número de inscrição inválido.")
    except ValueError:
        print("Entrada inválida. Digite um número.")


# MENU

def main():
    while True:
        print("\n     SISTEMA ACADEMIA     ")
        print("1 - Criar inscrição")
        print("2 - Listar inscrições")
        print("3 - Cancelar inscrição")
        print("0 - Sair")

        opcao = input("> ")

        if opcao == "1":
            criar_inscricao()
        elif opcao == "2":
            listar_inscricoes()
        elif opcao == "3":
            cancelar_inscricao()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()