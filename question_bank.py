import csv
import random

class QuestionBank:
    def __init__(self, arquivo_csv):
        self.perguntas = []
        self._carregar_csv(arquivo_csv)

    def _carregar_csv(self, arquivo_csv):
        with open(arquivo_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                enunciado = f"{row['pergunta']}\nA) {row['a']}\nB) {row['b']}\nC) {row['c']}\nD) {row['d']}"
                self.perguntas.append((enunciado, row['correta'].strip().upper()))
        random.shuffle(self.perguntas)

    def get_question(self):
        if self.perguntas:
            return self.perguntas.pop(0)
        return None
