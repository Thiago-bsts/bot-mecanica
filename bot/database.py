# ESTRUTURA DE DADOS: HashMap (Dicionário / dict)

SERVICOS_PRECOS = {
    "1": {"nome": "Troca de óleo", "preco": 150.0},
    "2": {"nome": "Revisão geral", "preco": 300.0},
    "3": {"nome": "Alinhamento", "preco": 80.0},
    "4": {"nome": "Balanceamento", "preco": 100.0},
    "5": {"nome": "Troca de freio", "preco": 250.0},
    "6": {"nome": "Diagnóstico de motor", "preco": 200.0}
}

DIAGNOSTICOS = {
    "1": {
        "problema": "Carro não liga",
        "causas": ["Bateria descarregada", "Motor de arranque com defeito", "Problema no alternador"],
        "servicos_sugeridos": ["Diagnóstico de motor", "Troca de bateria"],
        "urgente": True
    },
    "2": {
        "problema": "Barulho no motor",
        "causas": ["Falta de óleo", "Correia dentada gasta", "Válvulas desreguladas"],
        "servicos_sugeridos": ["Revisão geral", "Troca de óleo", "Diagnóstico de motor"],
        "urgente": True
    },
    "3": {
        "problema": "Freio falhando",
        "causas": ["Pastilhas gastas", "Vazamento de fluido", "Disco empenado"],
        "servicos_sugeridos": ["Troca de freio", "Revisão geral"],
        "urgente": True
    },
    "4": {
        "problema": "Superaquecimento",
        "causas": ["Falta de água", "Vazamento no radiador", "Válvula termostática travada"],
        "servicos_sugeridos": ["Revisão geral", "Diagnóstico de motor"],
        "urgente": True
    },
    "5": {
        "problema": "Luz do óleo acesa",
        "causas": ["Baixo nível de óleo", "Bomba de óleo com defeito", "Sensor de pressão danificado"],
        "servicos_sugeridos": ["Troca de óleo", "Diagnóstico de motor"],
        "urgente": False
    }
}
