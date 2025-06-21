def pontuar(tipo, acertou):
    pontos = {
        "PRIMEIRA": (5, -5),
        "PASSA": (7, -5),
        "REPASSA": (10, -3)
    }
    return pontos[tipo][0] if acertou else pontos[tipo][1]

def calcular_placar(jogadores, scores):
    return f"Placar: " + " | ".join(
        [f"{jogadores[addr]}: {score}" for addr, score in scores.items()]
    )
