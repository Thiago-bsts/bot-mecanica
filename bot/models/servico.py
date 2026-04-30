class Servico:
    def __init__(self, id_servico: str, nome: str, preco: float):
        self.id = id_servico
        self.nome = nome
        self.preco = preco

    def __str__(self):
        return f"{self.nome} (R$ {self.preco:.2f})"
