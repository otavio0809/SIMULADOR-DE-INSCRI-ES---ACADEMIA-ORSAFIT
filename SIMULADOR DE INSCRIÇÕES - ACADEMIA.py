from abc import ABC, abstractmethod
from datetime import datetime




class Plano:
    def __init__(self, nome, valor_mensal, fidelidade=False):
        self.nome = nome
        self.valor_mensal = valor_mensal
        self.fidelidade = fidelidade

    def __str__(self):
        return f"{self.nome} - R${self.valor_mensal}/mês {'(Fidelidade)' if self.fidelidade else ''}"



class Aluno:
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email
    
    def __str__(self):
        return f"{self.nome} ({self.email})"



class Pagamento(ABC):
    def __init__(self, valor):
        self.valor = valor
        self.data = datetime.now()

    @abstractmethod
    def processar(self):
        pass


class PagamentoPix(Pagamento):
    def __init__(self, valor, chave):
        super().__init__(valor)
        self.chave = chave

    def processar(self):
        return f"Pagamento via PIX de R${self.valor} enviado para {self.chave}"


class PagamentoCartao(Pagamento):
    def __init__(self, valor, numero_cartao):
        super().__init__(valor)
        self.numero_cartao = numero_cartao

    def processar(self):
        return f"Pagamento no cartão final {self.numero_cartao[-4:]} no valor de R${self.valor}"



class Inscricao:
    def __init__(self, aluno, plano):
        self.aluno = aluno
        self.plano = plano
        self.data_inscricao = datetime.now()
        self.ativa = True
        self.historico_pagamentos = []

    def cancelar(self):
        self.ativa = False
    
    def registrar_pagamento(self, pagamento: Pagamento):
        self.historico_pagamentos.append(pagamento)
        print(pagamento.processar())

    def __str__(self):
        return f"Inscrição de {self.aluno.nome} no plano {self.plano.nome} - {'Ativa' if self.ativa else 'Inativa'}"

if __name__ == "__main__":
    plano1 = Plano("Smart Basic", 99.90)
    aluno1 = Aluno("João Silva", "joao@email.com")

    inscricao = Inscricao(aluno1, plano1)
    
    print(inscricao)
    
    pagamento1 = PagamentoPix(99.90, "joao@pix.com")
    inscricao.registrar_pagamento(pagamento1)
