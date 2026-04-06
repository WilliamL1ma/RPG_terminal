import random

from .combat import NarradorCombate, SistemaCombate
from .interface import InterfaceRPG


class SistemaProgressao:
    """Agrupa regras de XP, nível, recompensas e ascensão."""

    MARCOS_ASCENSAO = (25, 50, 75, 100)

    def __init__(self, personagem, conquistas, trilha_ascensao, classe_inicial):
        self.personagem = personagem
        self.conquistas = conquistas
        self.trilha_ascensao = trilha_ascensao

        self.xp = 0
        self.nivel = 1
        self.proximo_nivel = 100
        self.ouro = 0
        self.almas = 0
        self.almas_coletadas_run = 0
        self.multiplicador_xp = 1.0
        self.multiplicador_ouro = 1.0
        self.maldicao_ultimo_nivel_ativa = False
        self.ruptura_maldicao_realizada = False

        self.bonus_esquiva = 0.0
        self.usou_ascensao = False
        self.decisao_ascensao_tomada = False
        self.recusou_ascensao = False
        self.marcos_ascensao_aplicados = set()
        self.forma_ascensao_atual = classe_inicial
        self.habilidades_ascensao = []

    def aplicar_bonus_ascensao(self, bonus):
        # Aplica os bônus da ascensão sem quebrar limites mínimos dos atributos.
        vida_bonus = bonus.get("vida", 0)
        defesa_bonus = bonus.get("defesa", 0)
        ataque_bonus = bonus.get("ataque", 0)
        mana_bonus = bonus.get("mana", 0)
        stamina_bonus = bonus.get("stamina", 0)
        esquiva_bonus = bonus.get("esquiva", 0.0)

        self.personagem.vida_max += vida_bonus
        self.personagem.defesa_max += defesa_bonus
        self.personagem.ataque += ataque_bonus
        self.personagem.mana_max += mana_bonus
        self.personagem.stamina_max += stamina_bonus
        self.bonus_esquiva += esquiva_bonus

        self.personagem.vida_max = max(1, self.personagem.vida_max)
        self.personagem.defesa_max = max(0, self.personagem.defesa_max)
        self.personagem.mana_max = max(0, self.personagem.mana_max)
        self.personagem.stamina_max = max(0, self.personagem.stamina_max)

        self.personagem.vida = min(self.personagem.vida_max, self.personagem.vida + max(0, vida_bonus))
        self.personagem.defesa = min(self.personagem.defesa_max, self.personagem.defesa + max(0, defesa_bonus))
        self.personagem.mana = min(self.personagem.mana_max, self.personagem.mana + max(0, mana_bonus))
        self.personagem.stamina = min(self.personagem.stamina_max, self.personagem.stamina + max(0, stamina_bonus))

    def desbloquear_marco_ascensao(self, marco):
        etapa = self.trilha_ascensao.get(marco)
        if not etapa:
            return

        self.forma_ascensao_atual = etapa["titulo"]
        self.aplicar_bonus_ascensao(etapa["bonus"])
        self.habilidades_ascensao.append(etapa["habilidade"])
        self.marcos_ascensao_aplicados.add(marco)

        print("\n=== ASCENSÃO DESPERTA ===")
        print(f"Novo título: {etapa['titulo']} (Nível {marco})")

        bonus_txt = []
        for chave, valor in etapa["bonus"].items():
            if chave == "esquiva":
                bonus_txt.append(f"+{int(valor * 100)}% Esquiva")
            else:
                sinal = "+" if valor >= 0 else ""
                bonus_txt.append(f"{sinal}{valor} {chave.upper()}")
        print("Bônus: " + ", ".join(bonus_txt))

        print(f"Nova habilidade: {etapa['habilidade']['nome']}")

    def verificar_ascensao(self):
        # A decisão da ascensão acontece só uma vez quando o jogador chega no nível 25.
        if self.recusou_ascensao:
            return

        if not self.decisao_ascensao_tomada and self.nivel >= 25:
            while True:
                escolha = input(
                    "Deseja abraçar o Caminho da Ascensão e transcender os seus limites mortais? [S/N]: "
                ).strip().lower()
                if escolha in ("s", "n"):
                    break
                print("Digite apenas S ou N.")

            self.decisao_ascensao_tomada = True
            if escolha == "n":
                self.recusou_ascensao = True
                self.conquistas.processar_evento("ascensao_recusada")
                print("Você recusou a Ascensão. Não haverá nova oportunidade.")
                return

            self.usou_ascensao = True
            print("\nVocê aceitou o Caminho da Ascensão.")

        if not self.usou_ascensao:
            return

        for marco in self.MARCOS_ASCENSAO:
            if self.nivel >= marco and marco not in self.marcos_ascensao_aplicados:
                self.desbloquear_marco_ascensao(marco)

    def subir_nivel(self):
        # Regra de level up: evolui os atributos base e restaura recursos.
        self.nivel += 1
        self.personagem.vida_max += 20
        self.personagem.defesa_max += 5
        self.personagem.ataque += 5
        self.personagem.mana_max += 5
        self.personagem.stamina_max += 5
        self.proximo_nivel += 20

        self.personagem.vida = self.personagem.vida_max
        self.personagem.defesa = self.personagem.defesa_max
        self.personagem.mana = self.personagem.mana_max
        self.personagem.stamina = self.personagem.stamina_max

        print(InterfaceRPG.titulo("Level Up", "Seu poder acabou de subir mais um degrau", cor=InterfaceRPG.VERDE, icone="🆙"))
        print(f"{self.personagem.nome} subiu para o nível {self.nivel}.")
        print(f"Vida máxima: {self.personagem.vida_max}")
        print(f"Defesa máxima: {self.personagem.defesa_max}")
        print(f"Ataque: {self.personagem.ataque}")
        print(f"Mana máxima: {self.personagem.mana_max}")
        print(f"Stamina máxima: {self.personagem.stamina_max}")
        print(f"Próximo nível: {self.proximo_nivel} XP")

        self.conquistas.processar_evento("nivel_alcancado", nivel=self.nivel)
        self.verificar_quebra_automatica_maldicao()
        self.verificar_ascensao()

    def ganhar_xp(self, quantidade):
        # Enquanto tiver XP suficiente, sobe vários níveis em sequência.
        ganho_real = max(1, int(round(quantidade * self.multiplicador_xp)))
        self.xp += ganho_real
        print(
            f"{self.personagem.nome} ganhou {ganho_real} XP "
            f"(base {quantidade}). ({self.xp}/{self.proximo_nivel})"
        )

        while self.xp >= self.proximo_nivel:
            self.xp -= self.proximo_nivel
            self.subir_nivel()

    def calcular_ouro_drop(self, ouro_base):
        multiplicador_aleatorio = random.uniform(1.0, 3.0)
        ouro_bruto = ouro_base + (self.nivel * multiplicador_aleatorio)
        variacao = random.uniform(0.70, 1.30)
        ouro_final = int(round(ouro_bruto * variacao))
        return max(1, ouro_final)

    def ganhar_ouro(self, inimigo):
        # O ouro final mistura faixa do inimigo com variação aleatória.
        faixa_ouro = getattr(inimigo, "faixa_ouro", None)
        if faixa_ouro:
            ouro_base = random.randint(faixa_ouro[0], faixa_ouro[1])
        else:
            ouro_base = max(5, int(inimigo.xp * 0.5))
        ganho_bruto = self.calcular_ouro_drop(ouro_base)
        ganho = max(1, int(round(ganho_bruto * self.multiplicador_ouro)))
        self.ouro += ganho
        print(
            f"{self.personagem.nome} encontrou {ganho} de ouro "
            f"(base {ganho_bruto}). (Total: {self.ouro})"
        )
        self.conquistas.processar_evento("ouro_coletado", ganho=ganho, total_ouro=self.ouro)

    def adicionar_almas(self, quantidade):
        self.almas += quantidade
        if quantidade > 0:
            self.almas_coletadas_run += quantidade

    def descansar(self):
        custo_estalagem = 10 + (self.nivel * 5)
        if self.ouro < custo_estalagem:
            print("\nO estalajadeiro te expulsou: ouro insuficiente para hospedagem.")
            print(f"Custo: {custo_estalagem} | Seu ouro: {self.ouro}")
            return False

        self.ouro -= custo_estalagem
        # Escala de cura por atributo para continuar útil em níveis altos.
        curar_vida = max(30, int(self.personagem.vida_max * 0.35))
        curar_defesa = max(10, int(self.personagem.defesa_max * 0.35))
        curar_mana = max(10, int(self.personagem.mana_max * 0.30))
        curar_stamina = max(10, int(self.personagem.stamina_max * 0.30))

        if self.maldicao_ultimo_nivel_ativa and self.nivel < 101:
            # Maldição hardcore: descanso fica 30% menos eficiente.
            curar_vida = max(1, int(curar_vida * 0.70))
            curar_defesa = max(1, int(curar_defesa * 0.70))
            curar_mana = max(1, int(curar_mana * 0.70))
            curar_stamina = max(1, int(curar_stamina * 0.70))

        vida_antes = self.personagem.vida
        defesa_antes = self.personagem.defesa
        mana_antes = self.personagem.mana
        stamina_antes = self.personagem.stamina

        self.personagem.vida = min(self.personagem.vida + curar_vida, self.personagem.vida_max)
        self.personagem.defesa = min(self.personagem.defesa + curar_defesa, self.personagem.defesa_max)
        self.personagem.mana = min(self.personagem.mana + curar_mana, self.personagem.mana_max)
        self.personagem.stamina = min(self.personagem.stamina + curar_stamina, self.personagem.stamina_max)

        print(InterfaceRPG.destaque(f"{self.personagem.nome} descansou e recuperou as forças.", icone=InterfaceRPG.ICONES["descanso"], cor=InterfaceRPG.VERDE))
        print(f"Vida: {vida_antes} -> {self.personagem.vida}/{self.personagem.vida_max}")
        print(f"Defesa: {defesa_antes} -> {self.personagem.defesa}/{self.personagem.defesa_max}")
        print(f"Mana: {mana_antes} -> {self.personagem.mana}/{self.personagem.mana_max}")
        print(f"Stamina: {stamina_antes} -> {self.personagem.stamina}/{self.personagem.stamina_max}")
        print(f"Custo da estalagem: {custo_estalagem} | Ouro restante: {self.ouro}")
        self.conquistas.processar_evento("descanso_realizado")
        return True

    def verificar_quebra_automatica_maldicao(self):
        if self.maldicao_ultimo_nivel_ativa and self.nivel >= 101:
            self.maldicao_ultimo_nivel_ativa = False
            self.conquistas.processar_evento("maldicao_quebrada_nivel101")
            print(InterfaceRPG.destaque("A Maldição do Último Nível foi quebrada. Seu destino está livre.", icone="⛓️", cor=InterfaceRPG.VERDE))

    def aplicar_maldicao_ultimo_nivel(self):
        if self.maldicao_ultimo_nivel_ativa:
            return
        self.maldicao_ultimo_nivel_ativa = True
        self.ruptura_maldicao_realizada = False
        self.conquistas.processar_evento("maldicao_ativada")
        print(InterfaceRPG.destaque("MALDIÇÃO ATIVA: só é possível encerrar a campanha ao atingir o nível 101.", icone=InterfaceRPG.ICONES["maldicao"], cor=InterfaceRPG.VERMELHO))

    def tentar_ruptura_maldicao(self):
        if not self.maldicao_ultimo_nivel_ativa:
            print("Nenhuma maldição ativa para romper.")
            return False
        if self.nivel >= 101:
            print("Você já superou a maldição pelo nível.")
            self.maldicao_ultimo_nivel_ativa = False
            return False
        if self.ruptura_maldicao_realizada:
            print("A ruptura já foi realizada nesta vida.")
            return False

        vida_perdida = max(1, int(self.personagem.vida_max * 0.30))
        ataque_perdido = max(1, int(self.personagem.ataque * 0.20))
        mana_perdida = max(1, int(self.personagem.mana_max * 0.20))

        print(InterfaceRPG.titulo("Ruptura da Maldição", "Poder cobrado em carne e destino", cor=InterfaceRPG.VERMELHO, icone=InterfaceRPG.ICONES["maldicao"]))
        print(f"-{vida_perdida} VIDA_MAX | -{ataque_perdido} ATAQUE | -{mana_perdida} MANA_MAX")
        confirmar = input("Confirmar ruptura? (S/N): ").strip().lower()
        if confirmar != "s":
            print("Ruptura cancelada.")
            return False

        self.personagem.vida_max = max(1, self.personagem.vida_max - vida_perdida)
        self.personagem.ataque = max(1, self.personagem.ataque - ataque_perdido)
        self.personagem.mana_max = max(0, self.personagem.mana_max - mana_perdida)
        self.personagem.vida = min(self.personagem.vida, self.personagem.vida_max)
        self.personagem.mana = min(self.personagem.mana, self.personagem.mana_max)

        self.maldicao_ultimo_nivel_ativa = False
        self.ruptura_maldicao_realizada = True
        self.conquistas.processar_evento("ruptura_maldicao")
        print(InterfaceRPG.destaque("A ruptura foi concluída. A maldição foi quebrada à força.", icone="💔", cor=InterfaceRPG.VERMELHO))
        return True

    def usar_habilidade_ascensao(self, alvo):
        # Interface simples de skill: valida escolha, custo e só então aplica o dano.
        if not self.habilidades_ascensao:
            print("Nenhuma habilidade de ascensão desbloqueada.")
            return False

        print(InterfaceRPG.titulo("Habilidades de Ascensão", "Escolha como gastar seu poder transcendental", cor=InterfaceRPG.MAGENTA, icone="🌠"))
        for indice, habilidade in enumerate(self.habilidades_ascensao, start=1):
            custo = habilidade["custo"]
            recurso = habilidade["recurso"].upper()
            print(f"{indice} - {habilidade['nome']} (Custo: {custo} {recurso})")

        escolha = input("Escolha a habilidade: ").strip()
        if not escolha.isdigit():
            print("Opção inválida.")
            return False

        indice = int(escolha) - 1
        if indice < 0 or indice >= len(self.habilidades_ascensao):
            print("Opção inválida.")
            return False

        habilidade = self.habilidades_ascensao[indice]
        custo = habilidade["custo"]
        recurso = habilidade["recurso"]

        valor_recurso = getattr(self.personagem, recurso)
        if valor_recurso < custo:
            print(f"{recurso.title()} insuficiente para usar {habilidade['nome']}.")
            return False

        setattr(self.personagem, recurso, valor_recurso - custo)

        dano = int(self.personagem.ataque * habilidade["multiplicador"] + habilidade.get("bonus_dano", 0))
        print(
            InterfaceRPG.destaque(
                NarradorCombate.narrar_habilidade_ascensao(self.personagem, alvo, habilidade["nome"]),
                icone=InterfaceRPG.ICONES["magia"],
                cor=InterfaceRPG.MAGENTA,
            )
        )
        print(
            InterfaceRPG.destaque(
                f"{self.personagem.nome} usou {habilidade['nome']} e causou {dano} de dano.",
                icone="🌠",
                cor=InterfaceRPG.MAGENTA,
            )
        )
        SistemaCombate.aplicar_dano(alvo, dano)
        self.conquistas.processar_evento("habilidade_ascensao_usada")

        print(f"{recurso.title()}: {getattr(self.personagem, recurso)}/{getattr(self.personagem, recurso + '_max')}")
        return True

