import random

from .combat import NarradorCombate, SistemaCombate
from .interface import InterfaceRPG
from .progression import SistemaProgressao


class Personagem:
    """Mantém identidade e estado base do herói."""

    def __init__(
        self,
        nome,
        vida,
        defesa,
        ataque,
        mana,
        stamina,
        classe_inicial,
        trilha_ascensao,
        conquistas,
    ):
        self.nome = nome
        self.vida = vida
        self.vida_max = vida
        self.defesa = defesa
        self.defesa_max = defesa
        self.mana = mana
        self.mana_max = mana
        self.stamina = stamina
        self.stamina_max = stamina
        self.ataque = ataque
        self.atributos_base_classe = {
            "vida": vida,
            "defesa": defesa,
            "ataque": ataque,
            "mana": mana,
            "stamina": stamina,
        }

        self.conquistas = conquistas
        self.progressao = SistemaProgressao(self, conquistas, trilha_ascensao, classe_inicial)
        self.tomou_dano_na_batalha = False

    def iniciar_batalha(self):
        self.tomou_dano_na_batalha = False

    def registrar_dano_batalha(self):
        self.tomou_dano_na_batalha = True

    @property
    def nivel(self):
        return self.progressao.nivel

    @property
    def xp(self):
        return self.progressao.xp

    @property
    def proximo_nivel(self):
        return self.progressao.proximo_nivel

    @property
    def ouro(self):
        return self.progressao.ouro

    @property
    def bonus_esquiva(self):
        return self.progressao.bonus_esquiva

    @property
    def forma_ascensao_atual(self):
        return self.progressao.forma_ascensao_atual

    def esta_vivo(self):
        return self.vida > 0

    def mostrar_status(self):
        # Status resumido para o jogador entender rápido como está o personagem.
        print(InterfaceRPG.status_personagem(self))

    def exibir_conquistas(self):
        self.conquistas.exibir()

    def resetar_para_base_classe(self):
        # Usado no julgamento final: volta os atributos ao ponto inicial da classe.
        base = self.atributos_base_classe
        self.vida_max = base["vida"]
        self.defesa_max = base["defesa"]
        self.ataque = base["ataque"]
        self.mana_max = base["mana"]
        self.stamina_max = base["stamina"]
        self.vida = self.vida_max
        self.defesa = self.defesa_max
        self.mana = self.mana_max
        self.stamina = self.stamina_max

class Guerreiro(Personagem):
    TRILHA_ASCENSAO = {
        25: {
            "titulo": "Gladiador",
            "bonus": {"vida": 20, "ataque": 10},
            "habilidade": {
                "nome": "Investida do Colosso",
                "recurso": "stamina",
                "custo": 14,
                "multiplicador": 2.8
            },
        },
        
        50: {
            "titulo": "Cavaleiro Rúnico",
            "bonus": {"defesa": 30, "mana": 15},
            "habilidade": {
                "nome": "Runa de Ruptura",
                "recurso": "mana",
                "custo": 12,
                "multiplicador": 2.6,
                "bonus_dano": 12,
            },
        },

        75: {
            "titulo": "Senhor da Guerra",
            "bonus": {"vida": 50, "stamina": 20},
            "habilidade": {
                "nome": "Comando Bélico", 
                "recurso": "stamina", 
                "custo": 22, 
                "multiplicador": 3.4
            },
        },

        100: {
            "titulo": "Titã Colossal",
            "bonus": {"vida": 100, "defesa": 40},
            "habilidade": {
                "nome": "Esmagamento Titânico", 
                "recurso": "stamina", 
                "custo": 30, 
                "multiplicador": 4.3
            },
        },
    }

    def __init__(self, nome, conquistas):
        super().__init__(
            nome=nome,
            vida=25,
            ataque=10,
            defesa=15,
            mana=10,
            stamina=35,
            classe_inicial="Guerreiro",
            trilha_ascensao=self.TRILHA_ASCENSAO,
            conquistas=conquistas,
        )

    def habilidade_especial(self, alvo):
        if self.stamina >= 10:
            dano = int(self.ataque * 2.5)
            print(
                InterfaceRPG.destaque(
                    NarradorCombate.narrar_habilidade_especial(self, alvo, "Golpe Duplo"),
                    icone="🗡️",
                    cor=InterfaceRPG.VERMELHO,
                )
            )
            SistemaCombate.aplicar_dano(alvo, dano)
            self.conquistas.processar_evento("habilidade_especial_usada")
            self.stamina -= 10
            print(f"Stamina: {self.stamina}/{self.stamina_max}")
            return True

        print("Stamina insuficiente.")
        return False


class Mago(Personagem):
    TRILHA_ASCENSAO = {
        25: {
            "titulo": "Feiticeiro",
            "bonus": {"mana": 20, "ataque": 15},
            "habilidade": {
                "nome": "Raio Arcano", 
                "recurso": "mana", 
                "custo": 14, 
                "multiplicador": 2.4
            },
        },

        50: {
            "titulo": "Arquimago",
            "bonus": {"mana": 30, "ataque": 20},
            "habilidade": {
                "nome": "Nova Etérea", 
                "recurso": "mana", 
                "custo": 22, 
                "multiplicador": 3.1
            },
        },

        75: {
            "titulo": "Tecelão do Vazio",
            "bonus": {"ataque": 40, "vida": -10},
            "habilidade": {
                "nome": "Fenda do Vazio",
                "recurso": "mana",
                "custo": 28,
                "multiplicador": 3.8,
                "bonus_dano": 20,
            },
        },

        100: {
            "titulo": "Avatar Cósmico",
            "bonus": {"mana": 80, "ataque": 50},
            "habilidade": {
                "nome": "Supernova Cósmica", 
                "recurso": "mana", 
                "custo": 36, 
                "multiplicador": 4.7
            },
        },
    }

    def __init__(self, nome, conquistas):
        super().__init__(
            nome=nome,
            vida=18,
            ataque=20,
            defesa=10,
            mana=35,
            stamina=20,
            classe_inicial="Mago",
            trilha_ascensao=self.TRILHA_ASCENSAO,
            conquistas=conquistas,
        )

    def habilidade_especial(self, alvo):
        if self.mana >= 10:
            dano = self.ataque + 10
            print(
                InterfaceRPG.destaque(
                    NarradorCombate.narrar_habilidade_especial(self, alvo, "Bola de Fogo"),
                    icone="🔥",
                    cor=InterfaceRPG.VERMELHO,
                )
            )
            SistemaCombate.aplicar_dano(alvo, dano)
            self.conquistas.processar_evento("habilidade_especial_usada")
            self.mana -= 10
            print(f"Mana: {self.mana}/{self.mana_max}")
            return True

        print("Mana insuficiente.")
        return False


class Arqueiro(Personagem):
    TRILHA_ASCENSAO = {
        25: {
            "titulo": "Caçador",
            "bonus": {"stamina": 20, "ataque": 15},
            "habilidade": {
                "nome": "Rajada Predadora", 
                "recurso": "stamina", 
                "custo": 14, 
                "multiplicador": 2.5
            },
        },

        50: {
            "titulo": "Patrulheiro",
            "bonus": {"ataque": 25, "esquiva": 0.10},
            "habilidade": {
                "nome": "Passo Fantasma", 
                "recurso": "stamina", 
                "custo": 18, 
                "multiplicador": 3.0
            },
        },

        75: {
            "titulo": "Sniper",
            "bonus": {"stamina": 40, "ataque": 30},
            "habilidade": {
                "nome": "Disparo Perfurante", 
                "recurso": "stamina", 
                "custo": 24, 
                "multiplicador": 3.9
            },
        },

        100: {
            "titulo": "Espectro dos Ventos",
            "bonus": {"ataque": 50, "stamina": 40},
            "habilidade": {
                "nome": "Tempestade de Flechas", 
                "recurso": "stamina", 
                "custo": 30, 
                "multiplicador": 4.8
            },
        },
    }

    def __init__(self, nome, conquistas):
        super().__init__(
            nome=nome,
            vida=15,
            ataque=30,
            defesa=5,
            mana=10,
            stamina=35,
            classe_inicial="Arqueiro",
            trilha_ascensao=self.TRILHA_ASCENSAO,
            conquistas=conquistas,
        )

    def habilidade_especial(self, alvo):
        if self.stamina >= 10:
            dano = self.ataque + 5
            print(
                InterfaceRPG.destaque(
                    NarradorCombate.narrar_habilidade_especial(self, alvo, "Flecha Precisa"),
                    icone="🏹",
                    cor=InterfaceRPG.VERDE,
                )
            )
            SistemaCombate.aplicar_dano(alvo, dano)
            self.conquistas.processar_evento("habilidade_especial_usada")
            self.stamina -= 10
            print(f"Stamina: {self.stamina}/{self.stamina_max}")
            return True

        print("Stamina insuficiente.")
        return False


class Inimigo:
    """Classe base para monstros e chefões."""

    def __init__(self, nome, vida, ataque, defesa, xp, faixa_ouro, nivel=1):
        self.nome = nome
        self.vida = vida
        self.vida_max = vida
        self.ataque = ataque
        self.defesa = defesa
        self.defesa_max = defesa
        self.xp = xp
        self.nivel = nivel
        self.faixa_ouro = faixa_ouro

    def esta_vivo(self):
        return self.vida > 0

    def mostrar_status(self):
        print(InterfaceRPG.status_inimigo(self))

class Monstro(Inimigo):
    TIPOS = {
        "Rato de Porão": {"vida": 10, "ataque": 3, "defesa": 0, "xp": 8, "ouro_min": 1, "ouro_max": 4},
        "Morcego Perdido": {"vida": 12, "ataque": 4, "defesa": 0, "xp": 9, "ouro_min": 1, "ouro_max": 4},
        "Slime Pequeno": {"vida": 34, "ataque": 13, "defesa": 1, "xp": 10, "ouro_min": 2, "ouro_max": 5},
        "Esqueleto Frágil": {"vida": 36, "ataque": 15, "defesa": 1, "xp": 12, "ouro_min": 2, "ouro_max": 6},
        "Duende Desarmado": {"vida": 25, "ataque": 14, "defesa": 0, "xp": 10, "ouro_min": 2, "ouro_max": 5},
        "Aranha de Caverna": {"vida": 23, "ataque": 15, "defesa": 0, "xp": 11, "ouro_min": 1, "ouro_max": 5},
        "Lodo Sonolento": {"vida": 28, "ataque": 12, "defesa": 2, "xp": 11, "ouro_min": 2, "ouro_max": 5},
        "Corvo Agressivo": {"vida": 21, "ataque": 14, "defesa": 0, "xp": 9, "ouro_min": 1, "ouro_max": 4},
        "Bandido Novato": {"vida": 30, "ataque": 10, "defesa": 1, "xp": 13, "ouro_min": 2, "ouro_max": 6},
        "Lacrau Cinzento": {"vida": 22, "ataque": 10, "defesa": 0, "xp": 10, "ouro_min": 1, "ouro_max": 5},
        "Goblin Sonolento": {"vida": 17, "ataque": 12, "defesa": 1, "xp": 12, "ouro_min": 2, "ouro_max": 6},
        "Orc": {"vida": 60, "ataque": 10, "defesa": 15, "xp": 40, "ouro_min": 16, "ouro_max": 28},
        "Goblinoide": {"vida": 35, "ataque": 10, "defesa": 0, "xp": 20, "ouro_min": 8, "ouro_max": 16},
        "Lobo Terrível": {"vida": 40, "ataque": 20, "defesa": 0, "xp": 30, "ouro_min": 12, "ouro_max": 22},
        "Dragão Vermelho Jovem": {"vida": 100,"ataque": 40,"defesa": 50,"xp": 250,"ouro_min": 90,"ouro_max": 150,},
        "Esqueleto": {"vida": 55, "ataque": 18, "defesa": 8, "xp": 35, "ouro_min": 14, "ouro_max": 24},
        "Slime": {"vida": 65, "ataque": 22, "defesa": 10, "xp": 45, "ouro_min": 20, "ouro_max": 34},
        "Bandido da Estrada": {"vida": 48, "ataque": 14, "defesa": 8, "xp": 28, "ouro_min": 10, "ouro_max": 20},
        "Espadachim Mercenário": {"vida": 62, "ataque": 18, "defesa": 12, "xp": 42, "ouro_min": 15, "ouro_max": 28},
        "Aspirante Arcano": {"vida": 38, "ataque": 24, "defesa": 4, "xp": 36, "ouro_min": 12, "ouro_max": 24},
        "Batedor Élfico Sombrio": {"vida": 50, "ataque": 20, "defesa": 7, "xp": 40, "ouro_min": 14, "ouro_max": 26},
        "Guardião da Cripta": {"vida": 78, "ataque": 16, "defesa": 18, "xp": 52, "ouro_min": 18, "ouro_max": 32},
        "Duelista Mascarado": {"vida": 55, "ataque": 22, "defesa": 10, "xp": 46, "ouro_min": 16, "ouro_max": 30},
        "Acólito Corrompido": {"vida": 44, "ataque": 19, "defesa": 6, "xp": 34, "ouro_min": 11, "ouro_max": 22},
        "Cavaleiro Errante": {"vida": 88, "ataque": 21, "defesa": 20, "xp": 65, "ouro_min": 22, "ouro_max": 38},
        "Atirador de Besta": {"vida": 52, "ataque": 23, "defesa": 5, "xp": 43, "ouro_min": 14, "ouro_max": 27},
        "Bruxo das Cinzas": {"vida": 68, "ataque": 28, "defesa": 9, "xp": 72, "ouro_min": 24, "ouro_max": 45},
        "Gelatina Ocre": {"vida": 80, "ataque": 15, "defesa": 20, "xp": 50, "ouro_min": 18, "ouro_max": 32},
        "Harpia": {"vida": 70, "ataque": 28, "defesa": 12, "xp": 60, "ouro_min": 22, "ouro_max": 38},
        "Trol": {"vida": 140, "ataque": 32, "defesa": 30, "xp": 95, "ouro_min": 35, "ouro_max": 58},
        "Golem de Pedra": {"vida": 180, "ataque": 26, "defesa": 55, "xp": 120, "ouro_min": 40, "ouro_max": 70},
        "Espectro": {"vida": 90, "ataque": 34, "defesa": 18, "xp": 85, "ouro_min": 30, "ouro_max": 50},
        "Minotauro": {"vida": 100, "ataque": 38, "defesa": 25, "xp": 80, "ouro_min": 45, "ouro_max": 78},
        "Aranha Gigante": {"vida": 90, "ataque": 30, "defesa": 14, "xp": 75, "ouro_min": 28, "ouro_max": 46},
        "Orc Olho de Gruumsh": {"vida": 95,"ataque": 36,"defesa": 16,"xp": 90,"ouro_min": 32,"ouro_max": 54},
    }

    @staticmethod
    def escalar_atributos(atributos_base, nivel_jogador):
        nivel_efetivo = max(1, nivel_jogador + random.randint(-1, 1))
        fator_vida = 1.0 + (nivel_efetivo - 1) * 0.09
        fator_ataque = 1.0 + (nivel_efetivo - 1) * 0.06
        fator_defesa = 1.0 + (nivel_efetivo - 1) * 0.07
        fator_recompensa = 1.0 + (nivel_efetivo - 1) * 0.09

        if nivel_jogador <= 5:
            amortecedor_inicio = 0.80 + (nivel_jogador * 0.04)
            fator_vida *= amortecedor_inicio
            fator_ataque *= amortecedor_inicio
            fator_defesa *= amortecedor_inicio

        vida = max(20, int(atributos_base["vida"] * fator_vida * random.uniform(0.90, 1.10)))
        ataque = max(5, int(atributos_base["ataque"] * fator_ataque * random.uniform(0.92, 1.08)))
        defesa = max(0, int(atributos_base["defesa"] * fator_defesa * random.uniform(0.90, 1.10)))
        xp = max(10, int(atributos_base["xp"] * fator_recompensa))
        ouro_min = max(1, int(atributos_base["ouro_min"] * fator_recompensa))
        ouro_max = max(ouro_min + 1, int(atributos_base["ouro_max"] * fator_recompensa))
        return nivel_efetivo, vida, ataque, defesa, xp, (ouro_min, ouro_max)

    @staticmethod
    def indice_ameaca(atributos_base):
        return (
            atributos_base["vida"] * 0.30
            + atributos_base["ataque"] * 2.1
            + atributos_base["defesa"] * 1.2
        )

    @classmethod
    def gerar_monstro(cls, nivel_jogador=1):
        # Mantém uma faixa base, mas aceita encontros mais perigosos para deixar a run tensa.
        ameaca_maxima = 60 + (nivel_jogador * 24)
        candidatos_normais = [
            (nome, atributos)
            for nome, atributos in cls.TIPOS.items()
            if cls.indice_ameaca(atributos) <= ameaca_maxima
        ]

        candidatos_perigosos = [
            (nome, atributos)
            for nome, atributos in cls.TIPOS.items()
            if ameaca_maxima < cls.indice_ameaca(atributos) <= (ameaca_maxima * 1.85)
        ]

        chance_encontro_perigoso = min(0.18 + (nivel_jogador * 0.015), 0.42)
        if candidatos_perigosos and random.random() < chance_encontro_perigoso:
            candidatos = candidatos_perigosos
        else:
            candidatos = candidatos_normais

        if not candidatos:
            candidatos = sorted(
                cls.TIPOS.items(),
                key=lambda item: cls.indice_ameaca(item[1]),
            )[:8]

        nome, atributos = random.choice(candidatos)
        nivel_efetivo, vida, ataque, defesa, xp, faixa_ouro = cls.escalar_atributos(atributos, nivel_jogador)
        return cls(nome, vida, ataque, defesa, xp, faixa_ouro, nivel=nivel_efetivo)


class Chefao(Inimigo):
    TIPOS = {
        "Ogro": {"vida": 120, "ataque": 30, "defesa": 30, "xp": 100, "ouro_min": 50, "ouro_max": 90},
        "Basilisco": {"vida": 70, "ataque": 20, "defesa": 10, "xp": 60, "ouro_min": 30, "ouro_max": 60},
        "Verme Alado": {"vida": 90, "ataque": 35, "defesa": 15, "xp": 80, "ouro_min": 40, "ouro_max": 70},
        "Hidra de Três Cabeças": {"vida": 260, "ataque": 66, "defesa": 72, "xp": 510, "ouro_min": 200, "ouro_max": 310},
        "Manticora Régia": {"vida": 210, "ataque": 74, "defesa": 38, "xp": 430, "ouro_min": 165, "ouro_max": 255},
        "General Orc de Gruumsh": {"vida": 280, "ataque": 62, "defesa": 90, "xp": 520, "ouro_min": 210, "ouro_max": 320},
        "Quimera Infernal": {"vida": 235, "ataque": 80, "defesa": 42, "xp": 470, "ouro_min": 180, "ouro_max": 285},
        "Arquidruida Corrompido": {"vida": 220, "ataque": 69, "defesa": 64, "xp": 455, "ouro_min": 175, "ouro_max": 272},
        "Colosso de Obsidiana": {"vida": 360, "ataque": 55, "defesa": 150, "xp": 610, "ouro_min": 250, "ouro_max": 380},
        "Lorde Vampiro": {"vida": 240, "ataque": 76, "defesa": 68, "xp": 500, "ouro_min": 195, "ouro_max": 300},
        "Kraken Abissal Menor": {"vida": 320, "ataque": 72, "defesa": 95, "xp": 590, "ouro_min": 235, "ouro_max": 360},
        "Arcanjo Caído": {"vida": 275, "ataque": 84, "defesa": 88, "xp": 640, "ouro_min": 265, "ouro_max": 400},
        "Lich Rei das Catacumbas": {"vida": 300, "ataque": 79, "defesa": 102, "xp": 670, "ouro_min": 275, "ouro_max": 410},
        "Dragão Vermelho Ancião": {"vida": 250,"ataque": 60,"defesa": 100,"xp": 500,"ouro_min": 180,"ouro_max": 280,},
        "Liche": {"vida": 220, "ataque": 58, "defesa": 70, "xp": 420, "ouro_min": 160, "ouro_max": 250},
        "Espectador": {"vida": 180, "ataque": 72, "defesa": 35, "xp": 390, "ouro_min": 150, "ouro_max": 235},
        "Diabo das Fossas": {"vida": 300,"ataque": 52,"defesa": 120,"xp": 520,"ouro_min": 210,"ouro_max": 320},
        "Balor": {"vida": 170, "ataque": 78, "defesa": 28, "xp": 400, "ouro_min": 155, "ouro_max": 245},
        "Dragão Azul Adulto": {"vida": 240,"ataque": 64,"defesa": 85,"xp": 470,"ouro_min": 185,"ouro_max": 290},
        "Cavaleiro da Morte": {"vida": 260,"ataque": 70,"defesa": 75,"xp": 490,"ouro_min": 195,"ouro_max": 305},
        "Devorador de Mentes Arcanista": {"vida": 210,"ataque": 82,"defesa": 40,"xp": 460,"ouro_min": 180,"ouro_max": 285},
        "Yuan-ti Anatema": {"vida": 230,"ataque": 68,"defesa": 55,"xp": 440,"ouro_min": 170,"ouro_max": 270},
        "Golem de Ferro": {"vida": 340,"ataque": 48,"defesa": 140,"xp": 560,"ouro_min": 230,"ouro_max": 350},
        "Tarrasque": {"vida": 380, "ataque": 88, "defesa": 110, "xp": 700, "ouro_min": 280, "ouro_max": 420},
    }

    @staticmethod
    def indice_ameaca(atributos_base):
        return (
            atributos_base["vida"] * 0.35
            + atributos_base["ataque"] * 2.5
            + atributos_base["defesa"] * 1.4
        )

    @staticmethod
    def escalar_atributos(atributos_base, nivel_jogador):
        nivel_efetivo = max(3, nivel_jogador + random.randint(1, 3))
        fator_vida = 1.0 + (nivel_efetivo - 1) * 0.22
        fator_ataque = 1.0 + (nivel_efetivo - 1) * 0.16
        fator_defesa = 1.0 + (nivel_efetivo - 1) * 0.18
        fator_recompensa = 1.0 + (nivel_efetivo - 1) * 0.20

        vida = max(80, int(atributos_base["vida"] * fator_vida * random.uniform(0.95, 1.12)))
        ataque = max(20, int(atributos_base["ataque"] * fator_ataque * random.uniform(0.95, 1.10)))
        defesa = max(10, int(atributos_base["defesa"] * fator_defesa * random.uniform(0.95, 1.12)))
        xp = max(60, int(atributos_base["xp"] * fator_recompensa))
        ouro_min = max(10, int(atributos_base["ouro_min"] * fator_recompensa))
        ouro_max = max(ouro_min + 1, int(atributos_base["ouro_max"] * fator_recompensa))
        return nivel_efetivo, vida, ataque, defesa, xp, (ouro_min, ouro_max)

    @classmethod
    def gerar_chefao(cls, nivel_jogador=3):
        # Chefões continuam escalados, mas agora há chance de aparecer um encontro acima da curva.
        ameaca_maxima = 260 + (nivel_jogador * 55)
        candidatos_normais = [
            (nome, atributos)
            for nome, atributos in cls.TIPOS.items()
            if cls.indice_ameaca(atributos) <= ameaca_maxima
        ]

        candidatos_perigosos = [
            (nome, atributos)
            for nome, atributos in cls.TIPOS.items()
            if ameaca_maxima < cls.indice_ameaca(atributos) <= (ameaca_maxima * 1.55)
        ]

        chance_chefao_brutal = min(0.12 + (nivel_jogador * 0.01), 0.28)
        if candidatos_perigosos and random.random() < chance_chefao_brutal:
            candidatos = candidatos_perigosos
        else:
            candidatos = candidatos_normais

        if not candidatos:
            candidatos = sorted(
                cls.TIPOS.items(),
                key=lambda item: cls.indice_ameaca(item[1]),
            )[:8]

        nome, atributos = random.choice(candidatos)
        nivel_efetivo, vida, ataque, defesa, xp, faixa_ouro = cls.escalar_atributos(atributos, nivel_jogador)
        return cls(nome, vida, ataque, defesa, xp, faixa_ouro, nivel=nivel_efetivo)

