import socket
import random
from question_bank import QuestionBank
from game_logic import pontuar, calcular_placar

HOST = 'localhost'
PORT = 10000
MAX_POINTS = 30

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))
print("Servidor aguardando jogadores...")

jogadores = {}       # {endereco: nome}
enderecos = []       # [endereco1, endereco2]
scores = {}          # {endereco: pontuacao}
quest = QuestionBank("perguntas.csv")

def receber_jogadores():
    while len(enderecos) < 2:
        msg, addr = server.recvfrom(1024)
        nome = msg.decode().strip()
        if addr not in enderecos:
            enderecos.append(addr)
            jogadores[addr] = nome
            scores[addr] = 0
            print(f"{nome} entrou no jogo.")
            server.sendto("Bem-vindo ao PASSA ou REPASSA!".encode(), addr)

def enviar_todos(msg):
    for addr in enderecos:
        server.sendto(msg.encode(), addr)

def receber_resposta(autorizado):
    while True:
        msg, addr = server.recvfrom(1024)
        if addr == autorizado:
            return msg.decode().strip().upper()
        else:
            server.sendto("⚠️ Não é sua vez!".encode(), addr)

def jogo():
    jogador_atual = random.choice(enderecos)
    outro = [e for e in enderecos if e != jogador_atual][0]

    while quest.get_question() and max(scores.values()) < MAX_POINTS:
        pergunta, correta = quest.get_question()
        enviar_todos(f"\nPERGUNTA:\n{pergunta}")
        server.sendto("Você deve RESPONDER ou PASSAR?".encode(), jogador_atual)

        resposta = receber_resposta(jogador_atual)
        if resposta.startswith("RESPONDER"):
            letra = resposta[-1]
            pontos = pontuar("PRIMEIRA", letra == correta)
            scores[jogador_atual] += pontos
            enviar_todos(f"{jogadores[jogador_atual]} respondeu {letra} — {'ACERTOU' if letra == correta else 'ERROU'} ({pontos} pontos)")

        elif resposta == "PASSA":
            # Agora sim pode perguntar ao outro jogador
            server.sendto("RESPONDA ou REPASSA?".encode(), outro)
            resposta2 = receber_resposta(outro)

            if resposta2.startswith("RESPONDER"):
                letra = resposta2[-1]
                pontos = pontuar("PASSA", letra == correta)
                scores[outro] += pontos
                enviar_todos(f"{jogadores[outro]} respondeu {letra} — {'ACERTOU' if letra == correta else 'ERROU'} ({pontos} pontos)")

            elif resposta2 == "REPASSA":
                # Volta para o primeiro jogador, que deve responder
                server.sendto("ADVERSÁRIO REPASSOU — Você deve responder!".encode(), jogador_atual)
                resposta3 = receber_resposta(jogador_atual)

                if resposta3.startswith("RESPONDER"):
                    letra = resposta3[-1]
                else:
                    letra = resposta3.split()[-1]

                pontos = pontuar("REPASSA", letra == correta)
                scores[jogador_atual] += pontos
                enviar_todos(f"{jogadores[jogador_atual]} respondeu {letra} — {'ACERTOU' if letra == correta else 'ERROU'} ({pontos} pontos)")


        enviar_todos(calcular_placar(jogadores, scores))
        jogador_atual, outro = outro, jogador_atual

    fim_jogo()

def fim_jogo():
    vencedor = max(scores, key=scores.get)
    enviar_todos(f"\n🏆 FIM DE JOGO! Vencedor: {jogadores[vencedor]} com {scores[vencedor]} pontos.")
    server.close()

# Execução principal
receber_jogadores()
receber_jogadores()
jogo()
