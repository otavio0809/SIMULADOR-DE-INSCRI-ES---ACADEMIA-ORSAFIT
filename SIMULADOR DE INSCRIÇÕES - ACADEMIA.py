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

# PADRÃO DE PROJETO FACTORY PARA PLANOS

class PlanoFactory:
    @staticmethod
    def criar_plano(tipo):
        if tipo == 1:
            return PlanoSimples("Básico", 150, 0, 1)
        elif tipo == 2:
            return PlanoPremium("Premium", 120.90, 0, 3)
        elif tipo == 3:
            return PlanoBlack("Black", 99.90, 12, 12)
        else:
            return None

class PlanoSimples(Plano):
    def beneficios(self):
        return "Acesso em horário comercial."


class PlanoPremium(Plano):
    def beneficios(self):
        return "Acesso total + musculação + aeróbico."


class PlanoBlack(Plano):
    def beneficios(self):
        return "Acesso total + personal + salas VIP."



# CLASSE ALUNO

class Aluno:
    def __init__(self, nome, cpf, telefone):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone






# PADRÃO DE PROJETO BIULDER PARA PAGAMENTO.

class Inscricao:
    def __init__(self, aluno, plano, data_inscricao, status, pagamento):
        self.aluno = aluno
        self.plano = plano
        self.data_inscricao = data_inscricao
        self.status = status
        self.pagamento = pagamento


class InscricaoBuilder:
    def __init__(self):
        self._aluno = None
        self._plano = None
        self._data = datetime.now()
        self._status = "ATIVA"
        self._pagamento = None

    def com_aluno(self, aluno):
        self._aluno = aluno
        return self

    def com_plano(self, plano):
        self._plano = plano
        return self

    def com_pagamento(self, pagamento):
        self._pagamento = pagamento
        return self

    def build(self):
        return Inscricao(self._aluno, self._plano, self._data, self._status, self._pagamento)


# CLASSE PAGAMENTO

class Pagamento:
    def __init__(self, valor, data_pagamento, metodo):
        self.valor = valor
        self.data_pagamento = data_pagamento
        self.metodo = metodo



# (USADNDO LISTA PARA ARMAZENAR DADOS DE PLANOS, ALUNOS E INSCRIÇÕES)

alunos = []
planos = []
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
    tipo = int(input("> "))

    plano = PlanoFactory.criar_plano(tipo)
    
    print(f"\nPlano selecionado: {plano.nome} - R${plano.preco}")
    
    metodo_pagamento = input("Forma de pagamento (PIX, cartão, dinheiro): ")
    pagamento = Pagamento(plano.preco, datetime.now(), metodo_pagamento)

    inscricao = (
        InscricaoBuilder()
        .com_aluno(aluno)
        .com_plano(plano)
        .com_pagamento(pagamento)
        .build()
    )

    inscricoes.append(inscricao)

    print("\n Inscrição concluída com sucesso!")
    print(f"Aluno: {aluno.nome} | Plano: {plano.nome} | Status: Ativa")


def listar_inscricoes():
    print("\n   Lista de Inscrições   ")
    for i, ins in enumerate(inscricoes):
        print(f"{i+1} - {ins.aluno.nome} | {ins.plano.nome} | {ins.status}")


def cancelar_inscricao():
    listar_inscricoes()
    escolha = int(input("\nDigite o número da inscrição para cancelar: ")) - 1
    inscricoes[escolha].status = "Inativa"
    print("\n   Inscrição cancelada com sucesso!   ")





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
            canceler = cancelar_inscricao()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")


main()
