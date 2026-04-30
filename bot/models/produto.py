class Produto:
    def __init__(self, id_produto: int, nome: str, preco: float):
        self.id = id_produto
        self.nome = nome
        self.preco = preco

    def __str__(self):
        return f"{self.nome} (R$ {self.preco:.2f})"
