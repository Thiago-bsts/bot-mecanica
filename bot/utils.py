def formatar_telefone(numero: str) -> str:
    """Remove espaços e formatações indesejadas de um telefone."""
    return numero.replace(" ", "").replace("-", "")

def log_sistema(acao: str, detalhes: str):
    print(f"[SYSTEM LOG] {acao} - {detalhes}")
