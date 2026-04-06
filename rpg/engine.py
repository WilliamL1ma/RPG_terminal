from .battle_flow import FluxoBatalhaMixin
from .campaign import CampanhaMixin
from .market import MercadoSombrioMixin
from .session import SessaoJogoMixin
from .state import ESTADO_RUN_ATRIBUTOS, EstadoRun


class MotorJogo(
    FluxoBatalhaMixin,
    MercadoSombrioMixin,
    CampanhaMixin,
    SessaoJogoMixin,
):
    """Controla o fluxo principal da aventura no console."""

    def __init__(self):
        super().__setattr__("estado_run", EstadoRun())
        self.jogador = None
        self.inimigos_derrotados = 0
        self.nemesis_strikes = {}
        self.maldicao_linhagem_ativa = False
        self.final_reflexo_tipo = None
        self.epilogo_encerramento = None

        self.heranca_ouro = 0
        self.heranca_almas = 0

    def __getattr__(self, nome):
        if nome in ESTADO_RUN_ATRIBUTOS:
            return getattr(self.estado_run, nome)
        raise AttributeError(nome)

    def __setattr__(self, nome, valor):
        if nome in ESTADO_RUN_ATRIBUTOS and "estado_run" in self.__dict__:
            setattr(self.estado_run, nome, valor)
            return
        super().__setattr__(nome, valor)

    CATALOGO_CONTRATOS = [
        {
            "id": "colosso_rubro",
            "nome": "Contrato do Colosso Rubro",
            "custo": 55,
            "descricao": "+90 VIDA_MAX, +18 ATAQUE; perde 30% da vida atual.",
            "bonus": {"vida": 90, "ataque": 18},
            "penalidade": {"vida_atual_pct_loss": 0.30},
        },
        {
            "id": "alma_runica",
            "nome": "Pacto da Alma Rúnica",
            "custo": 60,
            "descricao": "+80 MANA_MAX, +12 ATAQUE; -25 STAMINA_MAX.",
            "bonus": {"mana": 80, "ataque": 12},
            "penalidade": {"reduzir_atributo_flat": {"stamina_max": 25}},
        },
        {
            "id": "pacto_ferreo",
            "nome": "Juramento da Muralha Eterna",
            "custo": 62,
            "descricao": "+60 DEFESA_MAX, +70 VIDA_MAX; -30 MANA_MAX.",
            "bonus": {"defesa": 60, "vida": 70},
            "penalidade": {"reduzir_atributo_flat": {"mana_max": 30}},
        },
        {
            "id": "predador_silencioso",
            "nome": "Tratado do Predador Silencioso",
            "custo": 68,
            "descricao": "+28 ATAQUE, +8% ESQUIVA; -20 DEFESA_MAX.",
            "bonus": {"ataque": 28, "esquiva": 0.08},
            "penalidade": {"reduzir_atributo_flat": {"defesa_max": 20}},
        },
        {
            "id": "sangue_voraz",
            "nome": "Selo do Sangue Voraz",
            "custo": 57,
            "descricao": "+22 ATAQUE, +45 STAMINA_MAX; perde 20% da vida atual.",
            "bonus": {"ataque": 22, "stamina": 45},
            "penalidade": {"vida_atual_pct_loss": 0.20},
        },
        {
            "id": "tempestade_arcana",
            "nome": "Contrato da Tempestade Arcana",
            "custo": 72,
            "descricao": "+95 MANA_MAX, +10% ESQUIVA; -35 VIDA_MAX.",
            "bonus": {"mana": 95, "esquiva": 0.10},
            "penalidade": {"reduzir_atributo_flat": {"vida_max": 35}},
        },
        {
            "id": "senhor_ferro",
            "nome": "Pacto do Senhor de Ferro",
            "custo": 70,
            "descricao": "+75 DEFESA_MAX, +15 ATAQUE; -35 STAMINA_MAX.",
            "bonus": {"defesa": 75, "ataque": 15},
            "penalidade": {"reduzir_atributo_flat": {"stamina_max": 35}},
        },
        {
            "id": "cacador_noturno",
            "nome": "Juramento do Caçador Noturno",
            "custo": 58,
            "descricao": "+20 ATAQUE, +60 STAMINA_MAX; XP x0.85.",
            "bonus": {"ataque": 20, "stamina": 60},
            "penalidade": {"multiplicador_xp": 0.85},
        },
        {
            "id": "trono_espectral",
            "nome": "Tratado do Trono Espectral",
            "custo": 74,
            "descricao": "+70 VIDA_MAX, +70 MANA_MAX; -15 ATAQUE.",
            "bonus": {"vida": 70, "mana": 70},
            "penalidade": {"reduzir_atributo_flat": {"ataque": 15}},
        },
        {
            "id": "coracao_obsidiana",
            "nome": "Selo do Coração de Obsidiana",
            "custo": 80,
            "descricao": "+110 VIDA_MAX, +40 DEFESA_MAX; ouro x0.80.",
            "bonus": {"vida": 110, "defesa": 40},
            "penalidade": {"multiplicador_ouro": 0.80},
        },
        {
            "id": "cometa_negro",
            "nome": "Pacto do Cometa Negro",
            "custo": 75,
            "descricao": "+35 ATAQUE; -50 DEFESA_MAX.",
            "bonus": {"ataque": 35},
            "penalidade": {"reduzir_atributo_flat": {"defesa_max": 50}},
        },
        {
            "id": "pulso_draconico",
            "nome": "Contrato do Pulso Dracônico",
            "custo": 95,
            "descricao": "+120 VIDA_MAX, +20 ATAQUE, +25 DEFESA_MAX; -40 MANA_MAX e -40 STAMINA_MAX.",
            "bonus": {"vida": 120, "ataque": 20, "defesa": 25},
            "penalidade": {"reduzir_atributo_flat": {"mana_max": 40, "stamina_max": 40}},
        },
        {
            "id": "lamina_fria",
            "nome": "Juramento da Lâmina Fria",
            "custo": 60,
            "descricao": "+26 ATAQUE, +6% ESQUIVA; -25 VIDA_MAX.",
            "bonus": {"ataque": 26, "esquiva": 0.06},
            "penalidade": {"reduzir_atributo_flat": {"vida_max": 25}},
        },
        {
            "id": "arquimartir",
            "nome": "Pacto do Arquimártir",
            "custo": 92,
            "descricao": "+130 VIDA_MAX, +90 MANA_MAX; perde 35% da vida atual.",
            "bonus": {"vida": 130, "mana": 90},
            "penalidade": {"vida_atual_pct_loss": 0.35},
        },
        {
            "id": "coroa_quebrada",
            "nome": "Selo da Coroa Quebrada",
            "custo": 78,
            "descricao": "+50 DEFESA_MAX, +12% ESQUIVA; -18 ATAQUE.",
            "bonus": {"defesa": 50, "esquiva": 0.12},
            "penalidade": {"reduzir_atributo_flat": {"ataque": 18}},
        },
        {
            "id": "fome_astral",
            "nome": "Contrato da Fome Astral",
            "custo": 88,
            "descricao": "XP x1.45 e +15 ATAQUE; -20% VIDA_MAX e -20% MANA_MAX.",
            "bonus": {"ataque": 15},
            "penalidade": {
                "multiplicador_xp": 1.45,
                "reduzir_max_pct": {"vida_max": 0.20, "mana_max": 0.20},
            },
        },
        {
            "id": "eco_guerra",
            "nome": "Pacto do Eco de Guerra",
            "custo": 67,
            "descricao": "+22 ATAQUE, +22 DEFESA_MAX, +40 VIDA_MAX; -30 STAMINA_MAX.",
            "bonus": {"ataque": 22, "defesa": 22, "vida": 40},
            "penalidade": {"reduzir_atributo_flat": {"stamina_max": 30}},
        },
        {
            "id": "serpente_antiga",
            "nome": "Tratado da Serpente Antiga",
            "custo": 70,
            "descricao": "+75 MANA_MAX, +55 STAMINA_MAX; -20 DEFESA_MAX.",
            "bonus": {"mana": 75, "stamina": 55},
            "penalidade": {"reduzir_atributo_flat": {"defesa_max": 20}},
        },
        {
            "id": "vigilia_eterna",
            "nome": "Juramento da Vigília Eterna",
            "custo": 85,
            "descricao": "+95 DEFESA_MAX; XP x0.80.",
            "bonus": {"defesa": 95},
            "penalidade": {"multiplicador_xp": 0.80},
        },
        {
            "id": "aurora_profana",
            "nome": "Pacto da Aurora Profana",
            "custo": 73,
            "descricao": "+18 ATAQUE, +65 MANA_MAX, +7% ESQUIVA; -35 VIDA_MAX.",
            "bonus": {"ataque": 18, "mana": 65, "esquiva": 0.07},
            "penalidade": {"reduzir_atributo_flat": {"vida_max": 35}},
        },
        {
            "id": "leviata_ferido",
            "nome": "Contrato do Leviatã Ferido",
            "custo": 90,
            "descricao": "+160 VIDA_MAX; -25 ATAQUE.",
            "bonus": {"vida": 160},
            "penalidade": {"reduzir_atributo_flat": {"ataque": 25}},
        },
        {
            "id": "chama_azul",
            "nome": "Selo da Chama Azul",
            "custo": 82,
            "descricao": "+105 MANA_MAX, +20 ATAQUE; -25 DEFESA_MAX.",
            "bonus": {"mana": 105, "ataque": 20},
            "penalidade": {"reduzir_atributo_flat": {"defesa_max": 25}},
        },
        {
            "id": "executor_carmesim",
            "nome": "Pacto do Executor Carmesim",
            "custo": 79,
            "descricao": "+32 ATAQUE, +30 STAMINA_MAX; perde 25% da vida atual.",
            "bonus": {"ataque": 32, "stamina": 30},
            "penalidade": {"vida_atual_pct_loss": 0.25},
        },
        {
            "id": "nevoa_real",
            "nome": "Contrato da Névoa Real",
            "custo": 86,
            "descricao": "+14% ESQUIVA, +40 DEFESA_MAX; -22 ATAQUE.",
            "bonus": {"esquiva": 0.14, "defesa": 40},
            "penalidade": {"reduzir_atributo_flat": {"ataque": 22}},
        },
        {
            "id": "ultimo_imperador",
            "nome": "Juramento do Último Imperador",
            "custo": 140,
            "descricao": "+45 ATAQUE, +120 VIDA_MAX, +70 DEFESA_MAX, +100 MANA_MAX; XP x0.70, ouro x0.70 e perde 40% da vida atual.",
            "bonus": {"ataque": 45, "vida": 120, "defesa": 70, "mana": 100},
            "penalidade": {"multiplicador_xp": 0.70, "multiplicador_ouro": 0.70, "vida_atual_pct_loss": 0.40},
        },
        {
            "id": "juramento_penitente",
            "nome": "Juramento Penitente",
            "custo": 60,
            "descricao": "Monstros enfraquecem 3 níveis globais, mas XP x0.70.",
            "bonus": {},
            "penalidade": {"multiplicador_xp": 0.70, "reduzir_bonus_monstros": 3},
        },
        {
            "id": "aprendizado_profano",
            "nome": "Aprendizado Profano",
            "custo": 58,
            "descricao": "XP x1.40, mas -15% VIDA_MAX e -20% MANA_MAX.",
            "bonus": {},
            "penalidade": {"multiplicador_xp": 1.40, "reduzir_max_pct": {"vida_max": 0.15, "mana_max": 0.20}},
        },
    ]


def jogar():
    MotorJogo().executar()
