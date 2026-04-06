# NOME COMPLETO: William Gonçalves Cruz Ramos de Lima
# R.E: 824143532
# Trabalho de RPG em Python para terminal.


import os
import random
import shutil
import sys
from dataclasses import dataclass, field, fields


class InterfaceRPG:
    """Utilitários visuais para dar identidade ao terminal sem mexer na lógica."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    VERMELHO = "\033[91m"
    VERDE = "\033[92m"
    AMARELO = "\033[93m"
    AZUL = "\033[94m"
    MAGENTA = "\033[95m"
    CIANO = "\033[96m"
    BRANCO = "\033[97m"

    ICONES = {
        "vida": "❤️",
        "defesa": "🛡️",
        "mana": "🔮",
        "stamina": "⚡",
        "ouro": "🪙",
        "almas": "👻",
        "nivel": "🏅",
        "xp": "📘",
        "critico": "💥",
        "conquista": "🏆",
        "chefe": "👑",
        "aviso": "⚠️",
        "menu": "🎮",
        "batalha": "⚔️",
        "fuga": "💨",
        "descanso": "🛏️",
        "vitoria": "🎉",
        "derrota": "☠️",
        "magia": "✨",
        "mercador": "🕯️",
        "maldicao": "🩸",
        "reflexo": "🪞",
        "classe": "🧬",
        "inimigo": "👹",
        "herdeiro": "🧭",
    }

    @classmethod
    def suporta_cor(cls):
        return sys.stdout.isatty() and os.getenv("NO_COLOR") is None

    @classmethod
    def cor(cls, texto, codigo, negrito=False):
        if not cls.suporta_cor():
            return texto
        prefixo = cls.BOLD if negrito else ""
        return f"{prefixo}{codigo}{texto}{cls.RESET}"

    @staticmethod
    def largura():
        return min(86, max(56, shutil.get_terminal_size((80, 24)).columns))

    @classmethod
    def separador(cls, char="="):
        return cls.cor(char * cls.largura(), cls.AZUL)

    @classmethod
    def titulo(cls, texto, subtitulo=None, cor=None, icone=">>"):
        cor = cor or cls.CIANO
        largura = cls.largura()
        cabecalho = f" {icone} {texto.upper()} "
        topo = cls.cor("╔" + "═" * (largura - 2) + "╗", cor, negrito=True)
        meio = cls.cor(cabecalho.center(largura), cor, negrito=True)
        base = cls.cor("╚" + "═" * (largura - 2) + "╝", cor, negrito=True)
        blocos = [f"\n{topo}", meio]
        if subtitulo:
            blocos.append(cls.cor(subtitulo.center(largura), cls.BRANCO))
        blocos.append(base)
        return "\n".join(blocos)

    @classmethod
    def caixa(cls, titulo, linhas, cor=None):
        cor = cor or cls.AZUL
        largura = cls.largura()
        internas = [linha[: largura - 6] for linha in linhas]
        topo = cls.cor("┌" + "─" * (largura - 2) + "┐", cor)
        rodape = cls.cor("└" + "─" * (largura - 2) + "┘", cor)
        corpo = [cls.cor(f"│ {titulo[:largura - 6].ljust(largura - 4)}│", cor, negrito=True)]
        corpo.extend(
            cls.cor(f"│ {linha.ljust(largura - 4)}│", cls.BRANCO) for linha in internas
        )
        return "\n".join(["", topo, *corpo, rodape])

    @classmethod
    def menu(cls, titulo, opcoes, rodape=None, cor=None):
        linhas = [f"{indice}. {descricao}" for indice, descricao in opcoes]
        if rodape:
            linhas.append("")
            linhas.append(rodape)
        return cls.caixa(titulo, linhas, cor=cor or cls.MAGENTA)

    @classmethod
    def destaque(cls, texto, icone="✨", cor=None):
        return cls.cor(f"{icone} {texto}", cor or cls.BRANCO, negrito=True)

    @classmethod
    def barra(cls, atual, maximo, largura=18, cheia="#", vazia="-"):
        maximo = max(1, maximo)
        preenchida = int((atual / maximo) * largura)
        return "[" + cheia * preenchida + vazia * (largura - preenchida) + "]"

    @classmethod
    def status_personagem(cls, personagem):
        linhas = [
            f"{cls.ICONES['nivel']} {personagem.nivel} | {cls.ICONES['classe']} Classe: {personagem.forma_ascensao_atual}",
            (
                f"{cls.ICONES['vida']} {personagem.vida}/{personagem.vida_max} {cls.barra(personagem.vida, personagem.vida_max)} | "
                f"{cls.ICONES['defesa']} {personagem.defesa}/{personagem.defesa_max}"
            ),
            (
                f"{cls.ICONES['mana']} {personagem.mana}/{personagem.mana_max} {cls.barra(personagem.mana, max(1, personagem.mana_max))} | "
                f"{cls.ICONES['stamina']} {personagem.stamina}/{personagem.stamina_max}"
            ),
            (
                f"⚔️ ATAQ {personagem.ataque} | {cls.ICONES['xp']} {personagem.xp}/{personagem.proximo_nivel} | "
                f"{cls.ICONES['ouro']} {personagem.ouro} | {cls.ICONES['almas']} {personagem.progressao.almas}"
            ),
            f"🌀 Esquiva bônus: +{int(personagem.bonus_esquiva * 100)}%",
        ]
        if personagem.progressao.maldicao_ultimo_nivel_ativa and personagem.nivel < 101:
            linhas.append(f"{cls.ICONES['maldicao']} Maldição do Último Nível: ativa até o nível 101.")
        return cls.caixa(f"Status de {personagem.nome.upper()}", linhas, cor=cls.CIANO)

    @classmethod
    def status_inimigo(cls, inimigo):
        linhas = [
            f"{cls.ICONES['nivel']} {inimigo.nivel}",
            f"{cls.ICONES['vida']} {inimigo.vida}/{inimigo.vida_max} {cls.barra(inimigo.vida, inimigo.vida_max)}",
            f"{cls.ICONES['defesa']} {inimigo.defesa}/{inimigo.defesa_max} | ⚔️ ATAQ {inimigo.ataque}",
        ]
        return cls.caixa(f"{cls.ICONES['inimigo']} Inimigo: {inimigo.nome.upper()}", linhas, cor=cls.VERMELHO)


class EventosConquista:
    """Constantes dos eventos aceitos pelo sistema de conquistas."""

    BATALHA_VENCIDA = "batalha_vencida"
    ASCENSAO_RECUSADA = "ascensao_recusada"
    DESCANSO_REALIZADO = "descanso_realizado"
    FUGA_REALIZADA = "fuga_realizada"
    ESQUIVA_BEM_SUCEDIDA = "esquiva_bem_sucedida"
    NIVEL_ALCANCADO = "nivel_alcancado"
    OURO_COLETADO = "ouro_coletado"
    CRITICO_APLICADO = "critico_aplicado"
    HABILIDADE_ESPECIAL_USADA = "habilidade_especial_usada"
    HABILIDADE_ASCENSAO_USADA = "habilidade_ascensao_usada"
    FUGA_FALHADA = "fuga_falhada"
    VITORIA_PERFEITA = "vitoria_perfeita"
    QUEBROU_PERFEITA = "quebrou_perfeita"
    PACTO_SOMBRIO_COMPRADO = "pacto_sombrio_comprado"
    CONTRATO_SOMBRIO_FECHADO = "contrato_sombrio_fechado"
    DOMINIO_ALMA_SUCESSO = "dominio_alma_sucesso"
    DOMINIO_ALMA_FALHA = "dominio_alma_falha"
    NEMESIS_STRIKE = "nemesis_strike"
    FUGA_BLOQUEADA_NEMESIS = "fuga_bloqueada_nemesis"
    HERANCA_AMALDICOADA = "heranca_amaldicoada"
    MORTE_HEROI = "morte_heroi"
    FIM_RUN = "fim_run"
    MALDICAO_ATIVADA = "maldicao_ativada"
    ENCERRAMENTO_BLOQUEADO_MALDICAO = "encerramento_bloqueado_maldicao"
    RUPTURA_MALDICAO = "ruptura_maldicao"
    MALDICAO_QUEBRADA_NIVEL101 = "maldicao_quebrada_nivel101"
    JULGAMENTO_REFLEXO = "julgamento_reflexo"


@dataclass
class EstadoConquistas:
    """Estado mutável do sistema de conquistas."""

    desbloqueadas: list = field(default_factory=list)

    vitorias: int = 0
    monstros_derrotados: int = 0
    chefes_derrotados: int = 0
    descansos_realizados: int = 0
    abates_sem_descanso: int = 0
    fugas_realizadas: int = 0
    esquivas_bem_sucedidas: int = 0
    criticos_aplicados: int = 0
    especiais_usados: int = 0
    habilidades_ascensao_usadas: int = 0
    fugas_falhadas: int = 0
    vitorias_perfeitas: int = 0
    chefes_perfeitos: int = 0
    maior_sequencia_perfeita: int = 0
    sequencia_perfeita_atual: int = 0
    ouro_total_coletado: int = 0
    maior_ouro_unico: int = 0
    pactos_sombrios_comprados: int = 0
    contratos_sombrios_fechados: int = 0
    sucessos_dominar_alma: int = 0
    falhas_dominar_alma: int = 0
    nemesis_criados: int = 0
    nemesis_supremos: int = 0
    fugas_bloqueadas_nemesis: int = 0
    runs_amaldicoadas: int = 0
    mortes_totais: int = 0
    runs_finalizadas: int = 0
    runs_aposentadas: int = 0
    runs_encerradas_sem_descanso: int = 0
    maldicoes_ativadas: int = 0
    bloqueios_encerrar_maldicao: int = 0
    rupturas_maldicao: int = 0
    quebras_maldicao_nivel101: int = 0
    mortes_amaldicoadas: int = 0
    julgamentos_reflexo: int = 0
    finais_reflexo_integro: int = 0
    finais_reflexo_corrompido: int = 0

    kills_monstros_por_tipo: dict = field(default_factory=dict)
    kills_chefes_por_tipo: dict = field(default_factory=dict)
    monstros_unicos_derrotados: set = field(default_factory=set)
    chefes_unicos_derrotados: set = field(default_factory=set)
    monstros_sem_descanso: set = field(default_factory=set)
    chefes_sem_descanso: set = field(default_factory=set)

    catalogo_monstros: set = field(default_factory=set)
    catalogo_chefes: set = field(default_factory=set)


ESTADO_CONQUISTAS_ATRIBUTOS = {campo.name for campo in fields(EstadoConquistas)}


@dataclass
class EstadoRun:
    """Estado temporário de uma run específica."""

    ultimo_inimigo_fugido: str | None = None
    compras_sombrias_na_run: int = 0
    bonus_nivel_monstros: int = 0
    bonus_nivel_chefes: int = 0
    usou_mercador_sombrio_run: bool = False
    vitorias_na_run: int = 0
    rotacao_contratos_ativa: bool = False
    contratos_rotacao: list = field(default_factory=list)
    contrato_comprado_no_ciclo: bool = False
    contratos_sombrios_na_run: int = 0
    descansos_na_run: int = 0
    fugas_na_run: int = 0


ESTADO_RUN_ATRIBUTOS = {campo.name for campo in fields(EstadoRun)}


class ExibidorConquistas:
    """Camada de apresentação textual das conquistas."""

    @staticmethod
    def anunciar_desbloqueio(nome_conquista: str):
        print(
            InterfaceRPG.caixa(
                f"{InterfaceRPG.ICONES['conquista']} Conquista Desbloqueada",
                [f"✨ {nome_conquista}"],
                cor=InterfaceRPG.AMARELO,
            )
        )

    @staticmethod
    def exibir(desbloqueadas):
        print(InterfaceRPG.titulo("Conquistas", "Seu mural de feitos e insanidades", cor=InterfaceRPG.AMARELO, icone="[+]"))
        if not desbloqueadas:
            print("Nenhuma conquista desbloqueada ainda.")
            return

        for indice, conquista in enumerate(desbloqueadas, start=1):
            print(f"{InterfaceRPG.cor(f'{indice:02d}.', InterfaceRPG.AMARELO, negrito=True)} {conquista}")


class SistemaConquistas:
    """Coordena estado, regras e apresentação das conquistas."""

    MARCOS_GERAIS_VITORIAS = {
        1: "Primeira Vitória",
        10: "Gladiador da Estrada (10 vitórias)",
        25: "Veterano de Campanha (25 vitórias)",
        50: "Lenda das Masmorras (50 vitórias)",
        100: "Dominador das Eras (100 vitórias)",
        150: "Comandante da Ruína (150 vitórias)",
        250: "Conquistador dos Milênios (250 vitórias)",
    }
    MARCOS_GERAIS_CHEFOES = {
        1: "Caçador de Chefão",
        5: "Quebra-Coroas (5 chefões)",
        10: "Carrasco de Titãs (10 chefões)",
        20: "Ruína dos Imortais (20 chefões)",
        35: "Executor dos Tronos (35 chefões)",
        50: "Imperador dos Chefões (50 chefões)",
    }
    MARCOS_GERAIS_SEM_DESCANSO = {
        10: "Fôlego de Ferro (10 sem descansar)",
        25: "Marcha Incansável (25 sem descansar)",
        50: "Frenesi de Guerra (50 sem descansar)",
        80: "Vigília de Ferro (80 sem descansar)",
        120: "Legião Ininterrupta (120 sem descansar)",
    }
    MARCOS_DESCANSO = {
        1: ("Pouso Estratégico (primeiro descanso)", "Retirada Tática (já foi descansar)"),
        5: "Disciplina de Quartel (5 descansos)",
        10: ("Hóspede de Elite (10 descansos)", "Recomposição Bélica (10 descansos)"),
        20: "Mestre da Recuperação (20 descansos)",
        25: "Lorde da Estalagem (25 descansos)",
        40: "Senhor das Estalagens (40 descansos)",
        60: "Trono do Repouso (60 descansos)",
        100: "Soberano do Santuário (100 descansos)",
    }
    MARCOS_FUGA = {
        1: "Retirada Estratégica (primeira fuga)",
        5: "Corredor de Masmorra (5 fugas)",
        10: "Passo Fantasma (10 fugas)",
        20: "Lenda da Retirada (20 fugas)",
        35: "Usain Bolt da Covardia(35 fugas)",
        50: "Estratégia de Sobrevivência Absoluta (50 fugas)",
    }
    MARCOS_ESQUIVA = {
        10: "Reflexo de Aço (10 esquivas)",
        25: "Dança da Tempestade (25 esquivas)",
        50: "Mestre da Intangibilidade (50 esquivas)",
        100: "Fantasma da Linha de Frente (100 esquivas)",
        150: "Arquétipo da Esquiva (150 esquivas)",
        250: "Sombra da Guerra (250 esquivas)",
    }
    MARCOS_NIVEL = {
        5: "Calouro Sobrevivente (nível 5)",
        10: "Veterano da Guilda (nível 10)",
        25: "Lenda em Formação (nível 25)",
        50: "Semideus da Taverna (nível 50)",
        100: "Mito Imortal (nível 100)",
        150: "Arquétipo Supremo (nível 150)",
    }
    MARCOS_OURO_TOTAL = [
        (20000, "Trono Dourado Eterno (20000 de ouro coletado)"),
        (10000, "Imperador das Fortunas (10000 de ouro coletado)"),
        (5000, "Soberano do Tesouro (5000 de ouro coletado)"),
        (2000, "Cofre Ambulante (2000 de ouro coletado)"),
        (500, "Barão das Campanhas (500 de ouro coletado)"),
        (100, "Tesoureiro de Guerra (100 de ouro coletado)"),
    ]
    MARCOS_OURO_DROP = [
        (75, "Pilhagem de Elite (drop de 75+ ouro)"),
        (150, "Espólio Monumental (drop de 150+ ouro)"),
        (250, "Herança dos Reis (drop de 250+ ouro)"),
        (400, "Fortuna Ancestral (drop de 400+ ouro)"),
    ]
    MARCOS_OURO_GUARDADO = [
        (1000, "Magnata das Guildas (1000 de ouro guardado)"),
        (2000, "Arquiteto de Impérios (2000 de ouro guardado)"),
        (5000, "Tesouro Inexpugnável (5000 de ouro guardado)"),
    ]
    MARCOS_CRITICO = {
        1: "Primeiro Sangue Crítico",
        10: "Cirurgião de Batalha (10 críticos)",
        30: "Precisão Implacável (30 críticos)",
        75: "Olhar do Destino (75 críticos)",
        120: "Sentença Perfeita (120 críticos)",
        200: "Martelo do Destino (200 críticos)",
    }
    MARCOS_HABILIDADE_ESPECIAL = {
        10: "Técnica de Assinatura (10 especiais)",
        30: "Doutrina de Combate (30 especiais)",
        75: "Codex do Conquistador (75 especiais)",
        120: "Arsenal Supremo (120 especiais)",
        200: "Doutrina Inquebrável (200 especiais)",
    }
    MARCOS_HABILIDADE_ASCENSAO = {
        1: "Toque do Infinito (primeira habilidade de ascensão)",
        15: "Canalizador de Éter (15 habilidades de ascensão)",
        40: "Arsenal Divino (40 habilidades de ascensão)",
        80: "Avatar da Ascensão (80 habilidades de ascensão)",
        150: "Vontade Transcendente (150 habilidades de ascensão)",
    }
    MARCOS_FUGA_FALHADA = {
        1: "Cálculo Imperfeito (primeira fuga falhada)",
        5: "Peso da Consequência (5 fugas falhadas)",
        15: "Provação do Aço (15 fugas falhadas)",
        30: "Juramento da Resistência (30 fugas falhadas)",
    }
    MARCOS_VITORIA_PERFEITA = {
        1: "Intocável (primeira vitória sem perder vida)",
        5: "Lâmina Inviolada (5 vitórias perfeitas)",
        15: "Zero Arranhões (15 vitórias perfeitas)",
        30: "Égide Absoluta (30 vitórias perfeitas)",
        60: "Inquebrável (60 vitórias perfeitas)",
    }
    MARCOS_SEQUENCIA_PERFEITA = {
        3: "Sequência Limpa (3 perfeitas seguidas)",
        7: "Postura Inabalável (7 perfeitas seguidas)",
        12: "Conquista Impecável (12 perfeitas seguidas)",
        20: "Linha Imortal (20 perfeitas seguidas)",
    }
    MARCOS_CHEFE_PERFEITO = {
        1: "Regicida Intocado (chefão sem perder vida)",
        3: "Colecionador de Coroas Perfeitas (3 chefões perfeitos)",
        7: "Coroa Incontestável (7 chefões perfeitos)",
    }
    MARCOS_PACTO = {
        1: "Primeiro Selo das Sombras",
        5: "Acordo com o Abismo (5 pactos)",
        15: "Arquiteto de Pactos (15 pactos)",
    }
    MARCOS_CONTRATO = {
        1: "Contrato Assinado com Sangue",
        5: "Colecionador de Cláusulas (5 contratos)",
        12: "Biblioteca da Ruína (12 contratos)",
    }
    MARCOS_DOMINIO_ALMA = {
        1: "Sussurro Aprisionado",
        10: "Pastor de Almas (10 sucessos)",
        30: "Carcereiro do Além (30 sucessos)",
    }
    MARCOS_FALHA_ALMA = {
        1: "Eco Rejeitado",
        8: "Ritual Instável (8 falhas)",
        20: "Mártir Espiritual (20 falhas)",
    }
    MARCOS_NEMESIS_CRIADOS = {
        1: "Inimizade Nascente",
        10: "Semeador de Rivais (10 nêmesis)",
    }
    MARCOS_NEMESIS_SUPREMOS = {
        1: "Nêmesis Supremo Desperto",
        5: "Dinastia da Vingança (5 strikes finais)",
    }
    MARCOS_FUGA_BLOQUEADA = {
        1: "Sem Porta de Saída",
        10: "Paredes se Fecham (10 bloqueios de fuga)",
    }
    MARCOS_RUNS_AMALDICOADAS = {
        1: "Sangue Endividado",
        3: "Linhagem Maculada",
    }
    MARCOS_MORTE = {
        1: "Primeira Queda",
        5: "Cemitério de Heróis (5 mortes)",
    }
    MARCOS_MALDICAO_ATIVADA = {
        1: "Juramento do Último Nível",
        3: "Corrente da Linhagem (3 maldições ativas)",
    }
    MARCOS_BLOQUEIO_MALDICAO = {
        1: "Não Há Aposentadoria",
        5: "Porta Trancada (5 bloqueios)",
        15: "Prisão do Destino (15 bloqueios)",
    }
    MARCOS_RUPTURA_MALDICAO = {
        1: "Liberdade por Sangue",
        3: "Quebra-Runas da Linhagem (3 rupturas)",
    }
    MARCOS_QUEBRA_MALDICAO_101 = {
        1: "Fim do Juramento (nível 101)",
        3: "Mestre do Nível 101 (3 quebras)",
    }
    MARCOS_RUN_FINALIZADA = {
        1: "Capítulo Encerrado",
        5: "Saga Persistente (5 runs)",
        15: "Crônicas Inesgotáveis (15 runs)",
    }
    MARCOS_RUN_SEM_DESCANSO = {
        1: "Juramento de Vigília",
        5: "Voto sem Travesseiro (5 runs sem descanso)",
    }
    MARCOS_RUN_APOSENTADA = {
        1: "Retirada com Honra",
        5: "Veterano Aposentado (5 aposentadorias)",
    }
    MARCOS_MORTE_AMALDICOADA = {
        1: "Tombo Antes do 101",
        5: "Cemitério do Juramento (5 mortes amaldiçoadas)",
    }
    _eventos_que_alteram_combos = {
        EventosConquista.BATALHA_VENCIDA,
        EventosConquista.DESCANSO_REALIZADO,
        EventosConquista.FUGA_REALIZADA,
        EventosConquista.ESQUIVA_BEM_SUCEDIDA,
        EventosConquista.OURO_COLETADO,
        EventosConquista.CRITICO_APLICADO,
        EventosConquista.HABILIDADE_ESPECIAL_USADA,
        EventosConquista.HABILIDADE_ASCENSAO_USADA,
        EventosConquista.FUGA_FALHADA,
        EventosConquista.VITORIA_PERFEITA,
        EventosConquista.PACTO_SOMBRIO_COMPRADO,
        EventosConquista.CONTRATO_SOMBRIO_FECHADO,
        EventosConquista.DOMINIO_ALMA_SUCESSO,
        EventosConquista.DOMINIO_ALMA_FALHA,
        EventosConquista.NEMESIS_STRIKE,
        EventosConquista.FUGA_BLOQUEADA_NEMESIS,
        EventosConquista.HERANCA_AMALDICOADA,
        EventosConquista.MORTE_HEROI,
        EventosConquista.FIM_RUN,
        EventosConquista.RUPTURA_MALDICAO,
        EventosConquista.MALDICAO_QUEBRADA_NIVEL101,
    }

    def __init__(self, catalogo_monstros=None, catalogo_chefes=None):
        super().__setattr__("estado", EstadoConquistas())
        super().__setattr__("_exibidor", ExibidorConquistas())
        self.catalogo_monstros = set(catalogo_monstros or [])
        self.catalogo_chefes = set(catalogo_chefes or [])
        super().__setattr__("_handlers_evento", self._criar_handlers_evento())

    def __getattr__(self, nome):
        if nome in ESTADO_CONQUISTAS_ATRIBUTOS:
            return getattr(self.estado, nome)
        raise AttributeError(nome)

    def __setattr__(self, nome, valor):
        if nome in ESTADO_CONQUISTAS_ATRIBUTOS and "estado" in self.__dict__:
            setattr(self.estado, nome, valor)
            return
        super().__setattr__(nome, valor)

    def _criar_handlers_evento(self):
        return {
            EventosConquista.BATALHA_VENCIDA: lambda contexto: self._registrar_vitoria(
                contexto.get("nome_inimigo", "Inimigo Desconhecido"),
                contexto.get("eh_chefao", False),
            ),
            EventosConquista.ASCENSAO_RECUSADA: lambda contexto: self._registrar_ascensao_recusada(),
            EventosConquista.DESCANSO_REALIZADO: lambda contexto: self._registrar_descanso(),
            EventosConquista.FUGA_REALIZADA: lambda contexto: self._registrar_fuga(),
            EventosConquista.ESQUIVA_BEM_SUCEDIDA: lambda contexto: self._registrar_esquiva(),
            EventosConquista.NIVEL_ALCANCADO: lambda contexto: self._registrar_nivel_alcancado(contexto.get("nivel", 0)),
            EventosConquista.OURO_COLETADO: lambda contexto: self._registrar_ouro_coletado(
                contexto.get("ganho", 0),
                contexto.get("total_ouro", 0),
            ),
            EventosConquista.CRITICO_APLICADO: lambda contexto: self._registrar_critico(),
            EventosConquista.HABILIDADE_ESPECIAL_USADA: lambda contexto: self._registrar_habilidade_especial(),
            EventosConquista.HABILIDADE_ASCENSAO_USADA: lambda contexto: self._registrar_habilidade_ascensao(),
            EventosConquista.FUGA_FALHADA: lambda contexto: self._registrar_fuga_falhada(),
            EventosConquista.VITORIA_PERFEITA: lambda contexto: self._registrar_vitoria_perfeita(
                contexto.get("eh_chefao", False)
            ),
            EventosConquista.QUEBROU_PERFEITA: lambda contexto: self._quebrar_sequencia_perfeita(),
            EventosConquista.PACTO_SOMBRIO_COMPRADO: lambda contexto: self._registrar_pacto_sombrio(),
            EventosConquista.CONTRATO_SOMBRIO_FECHADO: lambda contexto: self._registrar_contrato_sombrio(),
            EventosConquista.DOMINIO_ALMA_SUCESSO: lambda contexto: self._registrar_dominio_alma(contexto.get("ganho", 0)),
            EventosConquista.DOMINIO_ALMA_FALHA: lambda contexto: self._registrar_falha_alma(),
            EventosConquista.NEMESIS_STRIKE: lambda contexto: self._registrar_nemesis(contexto.get("strike", 0)),
            EventosConquista.FUGA_BLOQUEADA_NEMESIS: lambda contexto: self._registrar_fuga_bloqueada(),
            EventosConquista.HERANCA_AMALDICOADA: lambda contexto: self._registrar_heranca_amaldicoada(),
            EventosConquista.MORTE_HEROI: lambda contexto: self._registrar_morte_heroi(
                contexto.get("contratos_na_run", 0),
                contexto.get("pactos_na_run", 0),
            ),
            EventosConquista.FIM_RUN: lambda contexto: self._registrar_fim_run(**contexto),
            EventosConquista.MALDICAO_ATIVADA: lambda contexto: self._registrar_maldicao_ativada(),
            EventosConquista.ENCERRAMENTO_BLOQUEADO_MALDICAO: lambda contexto: self._registrar_encerramento_bloqueado(),
            EventosConquista.RUPTURA_MALDICAO: lambda contexto: self._registrar_ruptura_maldicao(),
            EventosConquista.MALDICAO_QUEBRADA_NIVEL101: lambda contexto: self._registrar_quebra_maldicao_nivel101(),
            EventosConquista.JULGAMENTO_REFLEXO: lambda contexto: self._registrar_julgamento_reflexo(
                contexto.get("tipo", "integro")
            ),
        }

    def _desbloquear_marco_exato(self, valor, marcos):
        recompensa = marcos.get(valor)
        if not recompensa:
            return
        if isinstance(recompensa, str):
            self.desbloquear(recompensa)
            return
        for conquista in recompensa:
            self.desbloquear(conquista)

    def _desbloquear_primeiro_marco_atingido(self, valor, marcos):
        for limite, conquista in marcos:
            if valor >= limite:
                self.desbloquear(conquista)
                return

    def _desbloquear_todos_os_marcos_atingidos(self, valor, marcos):
        for limite, conquista in marcos:
            if valor >= limite:
                self.desbloquear(conquista)

    @staticmethod
    def _nome_especialista(nome_inimigo: str, marco: int, eh_chefao: bool):
        if eh_chefao:
            if marco == 5:
                return f"Algoz de {nome_inimigo} (5)"
            if marco == 10:
                return f"Nêmesis de {nome_inimigo} (10)"
            return f"Flagelo de {nome_inimigo} (20)"
        if marco == 5:
            return f"Caçador de {nome_inimigo} (5)"
        if marco == 10:
            return f"Especialista em {nome_inimigo} (10)"
        return f"Exterminador de {nome_inimigo} (20)"

    def desbloquear(self, nome_conquista: str):
        if nome_conquista not in self.desbloqueadas:
            self.desbloqueadas.append(nome_conquista)
            self._exibidor.anunciar_desbloqueio(nome_conquista)

    def _registrar_marcos_gerais(self):
        self._desbloquear_marco_exato(self.vitorias, self.MARCOS_GERAIS_VITORIAS)
        self._desbloquear_marco_exato(self.chefes_derrotados, self.MARCOS_GERAIS_CHEFOES)
        self._desbloquear_marco_exato(self.abates_sem_descanso, self.MARCOS_GERAIS_SEM_DESCANSO)

    def _registrar_especialista(self, nome_inimigo: str, eh_chefao: bool):
        tabela = self.kills_chefes_por_tipo if eh_chefao else self.kills_monstros_por_tipo
        tabela[nome_inimigo] = tabela.get(nome_inimigo, 0) + 1
        kills = tabela[nome_inimigo]

        if kills in (5, 10, 20):
            self.desbloquear(self._nome_especialista(nome_inimigo, kills, eh_chefao))

        if eh_chefao:
            if kills == 1:
                self.desbloquear(f"Executor de {nome_inimigo} (1)")
            elif kills == 5:
                self.desbloquear(f"Açoite de {nome_inimigo} (5)")
            elif kills == 10:
                self.desbloquear(f"Suserano de {nome_inimigo} (10)")
                if self.catalogo_chefes and all(
                    self.kills_chefes_por_tipo.get(nome_chefao, 0) >= 10
                    for nome_chefao in self.catalogo_chefes
                ):
                    self.desbloquear("Lord entre os Lords")

    def _registrar_colecao(self, eh_chefao: bool):
        total_monstros = len(self.catalogo_monstros)
        total_chefes = len(self.catalogo_chefes)

        if eh_chefao:
            if total_chefes and len(self.chefes_unicos_derrotados) == total_chefes:
                self.desbloquear("Conselho dos Reis Caídos (todos os chefões)")
            if total_chefes and len(self.chefes_sem_descanso) == total_chefes:
                self.desbloquear("Trono Quebrado sem Descanso (todos os chefões sem descansar)")
        else:
            if total_monstros and len(self.monstros_unicos_derrotados) == total_monstros:
                self.desbloquear("Bestiário Conquistado (todos os monstros)")
            if total_monstros and len(self.monstros_sem_descanso) == total_monstros:
                self.desbloquear("Predador Implacável (todos os monstros sem descansar)")

        todos_monstros = total_monstros and len(self.monstros_unicos_derrotados) == total_monstros
        todos_chefes = total_chefes and len(self.chefes_unicos_derrotados) == total_chefes
        if todos_monstros and todos_chefes:
            self.desbloquear("Cronista da Guerra Total (com descanso)")

        todos_monstros_hard = total_monstros and len(self.monstros_sem_descanso) == total_monstros
        todos_chefes_hard = total_chefes and len(self.chefes_sem_descanso) == total_chefes
        if todos_monstros_hard and todos_chefes_hard:
            self.desbloquear("Apocalipse Ambulante (sem descansar)")

    def _registrar_vitoria(self, nome_inimigo: str, eh_chefao: bool):
        self.vitorias += 1
        self.abates_sem_descanso += 1

        if eh_chefao:
            self.chefes_derrotados += 1
            self.chefes_unicos_derrotados.add(nome_inimigo)
            self.chefes_sem_descanso.add(nome_inimigo)
        else:
            self.monstros_derrotados += 1
            self.monstros_unicos_derrotados.add(nome_inimigo)
            self.monstros_sem_descanso.add(nome_inimigo)

        self._registrar_marcos_gerais()
        self._registrar_especialista(nome_inimigo, eh_chefao)
        self._registrar_colecao(eh_chefao)

    def _registrar_descanso(self):
        self.descansos_realizados += 1
        self.abates_sem_descanso = 0
        self.monstros_sem_descanso.clear()
        self.chefes_sem_descanso.clear()
        self._desbloquear_marco_exato(self.descansos_realizados, self.MARCOS_DESCANSO)

    def _registrar_fuga(self):
        self.fugas_realizadas += 1
        self._desbloquear_marco_exato(self.fugas_realizadas, self.MARCOS_FUGA)

    def _registrar_esquiva(self):
        self.esquivas_bem_sucedidas += 1
        self._desbloquear_marco_exato(self.esquivas_bem_sucedidas, self.MARCOS_ESQUIVA)

    def _registrar_ascensao_recusada(self):
        self.desbloquear("Humildade Mortal")

    def _registrar_nivel_alcancado(self, nivel: int):
        self._desbloquear_marco_exato(nivel, self.MARCOS_NIVEL)

    def _registrar_ouro_coletado(self, ganho: int, total: int):
        self.ouro_total_coletado += ganho
        if ganho > self.maior_ouro_unico:
            self.maior_ouro_unico = ganho
        self._desbloquear_primeiro_marco_atingido(self.ouro_total_coletado, self.MARCOS_OURO_TOTAL)
        self._desbloquear_todos_os_marcos_atingidos(ganho, self.MARCOS_OURO_DROP)
        self._desbloquear_todos_os_marcos_atingidos(total, self.MARCOS_OURO_GUARDADO)

    def _registrar_critico(self):
        self.criticos_aplicados += 1
        self._desbloquear_marco_exato(self.criticos_aplicados, self.MARCOS_CRITICO)

    def _registrar_habilidade_especial(self):
        self.especiais_usados += 1
        self._desbloquear_marco_exato(self.especiais_usados, self.MARCOS_HABILIDADE_ESPECIAL)

    def _registrar_habilidade_ascensao(self):
        self.habilidades_ascensao_usadas += 1
        self._desbloquear_marco_exato(self.habilidades_ascensao_usadas, self.MARCOS_HABILIDADE_ASCENSAO)

    def _registrar_fuga_falhada(self):
        self.fugas_falhadas += 1
        self._desbloquear_marco_exato(self.fugas_falhadas, self.MARCOS_FUGA_FALHADA)

    def _registrar_vitoria_perfeita(self, eh_chefao: bool):
        self.vitorias_perfeitas += 1
        self.sequencia_perfeita_atual += 1
        self.maior_sequencia_perfeita = max(self.maior_sequencia_perfeita, self.sequencia_perfeita_atual)

        self._desbloquear_marco_exato(self.vitorias_perfeitas, self.MARCOS_VITORIA_PERFEITA)
        self._desbloquear_marco_exato(self.maior_sequencia_perfeita, self.MARCOS_SEQUENCIA_PERFEITA)

        if eh_chefao:
            self.chefes_perfeitos += 1
            self._desbloquear_marco_exato(self.chefes_perfeitos, self.MARCOS_CHEFE_PERFEITO)

    def _quebrar_sequencia_perfeita(self):
        self.sequencia_perfeita_atual = 0

    def _registrar_pacto_sombrio(self):
        self.pactos_sombrios_comprados += 1
        self._desbloquear_marco_exato(self.pactos_sombrios_comprados, self.MARCOS_PACTO)

    def _registrar_contrato_sombrio(self):
        self.contratos_sombrios_fechados += 1
        self._desbloquear_marco_exato(self.contratos_sombrios_fechados, self.MARCOS_CONTRATO)

    def _registrar_dominio_alma(self, ganho: int):
        if ganho > 0:
            self.sucessos_dominar_alma += 1
            self._desbloquear_marco_exato(self.sucessos_dominar_alma, self.MARCOS_DOMINIO_ALMA)

    def _registrar_falha_alma(self):
        self.falhas_dominar_alma += 1
        self._desbloquear_marco_exato(self.falhas_dominar_alma, self.MARCOS_FALHA_ALMA)

    def _registrar_nemesis(self, strike: int):
        if strike == 1:
            self.nemesis_criados += 1
            self._desbloquear_marco_exato(self.nemesis_criados, self.MARCOS_NEMESIS_CRIADOS)
        elif strike >= 3:
            self.nemesis_supremos += 1
            self._desbloquear_marco_exato(self.nemesis_supremos, self.MARCOS_NEMESIS_SUPREMOS)

    def _registrar_fuga_bloqueada(self):
        self.fugas_bloqueadas_nemesis += 1
        self._desbloquear_marco_exato(self.fugas_bloqueadas_nemesis, self.MARCOS_FUGA_BLOQUEADA)

    def _registrar_heranca_amaldicoada(self):
        self.runs_amaldicoadas += 1
        self._desbloquear_marco_exato(self.runs_amaldicoadas, self.MARCOS_RUNS_AMALDICOADAS)

    def _registrar_morte_heroi(self, contratos_na_run: int, pactos_na_run: int):
        self.mortes_totais += 1
        self._desbloquear_marco_exato(self.mortes_totais, self.MARCOS_MORTE)

        if contratos_na_run >= 2:
            self.desbloquear("Caiu com as Cláusulas Assinadas (2 contratos e morte)")
        if pactos_na_run >= 2:
            self.desbloquear("Apostador do Abismo (2 pactos e morte)")
        if contratos_na_run >= 2 and pactos_na_run >= 2:
            self.desbloquear("Falência da Alma (2 contratos + 2 pactos + morte)")

    def _registrar_maldicao_ativada(self):
        self.maldicoes_ativadas += 1
        self._desbloquear_marco_exato(self.maldicoes_ativadas, self.MARCOS_MALDICAO_ATIVADA)

    def _registrar_encerramento_bloqueado(self):
        self.bloqueios_encerrar_maldicao += 1
        self._desbloquear_marco_exato(self.bloqueios_encerrar_maldicao, self.MARCOS_BLOQUEIO_MALDICAO)

    def _registrar_ruptura_maldicao(self):
        self.rupturas_maldicao += 1
        self._desbloquear_marco_exato(self.rupturas_maldicao, self.MARCOS_RUPTURA_MALDICAO)

    def _registrar_quebra_maldicao_nivel101(self):
        self.quebras_maldicao_nivel101 += 1
        self._desbloquear_marco_exato(self.quebras_maldicao_nivel101, self.MARCOS_QUEBRA_MALDICAO_101)

    def _registrar_julgamento_reflexo(self, tipo: str):
        self.julgamentos_reflexo += 1
        if self.julgamentos_reflexo == 1:
            self.desbloquear("Encontro com o Reflexo Final")

        if tipo == "integro":
            self.finais_reflexo_integro += 1
            if self.finais_reflexo_integro == 1:
                self.desbloquear("Julgamento da Origem")
        elif tipo == "corrompido":
            self.finais_reflexo_corrompido += 1
            if self.finais_reflexo_corrompido == 1:
                self.desbloquear("Inventário do Vazio")

        if self.finais_reflexo_integro >= 1 and self.finais_reflexo_corrompido >= 1:
            self.desbloquear("As Duas Faces do Fim")

    def _registrar_fim_run(self, **contexto):
        self.runs_finalizadas += 1
        self._desbloquear_marco_exato(self.runs_finalizadas, self.MARCOS_RUN_FINALIZADA)

        morreu = contexto.get("morreu", False)
        nivel_final = contexto.get("nivel_final", 1)
        descansos_run = contexto.get("descansos_na_run", 0)
        contratos_run = contexto.get("contratos_na_run", 0)
        pactos_run = contexto.get("pactos_na_run", 0)
        fugas_run = contexto.get("fugas_na_run", 0)
        vitorias_run = contexto.get("vitorias_na_run", 0)
        ouro_final = contexto.get("ouro_final", 0)
        divida_herdeiro = contexto.get("divida_herdeiro", 0)
        almas_run = contexto.get("almas_coletadas_run", 0)
        maldicao_ativa_final = contexto.get("maldicao_ativa_final", False)
        ruptura_maldicao_run = contexto.get("ruptura_maldicao_run", False)

        if descansos_run == 0:
            self.runs_encerradas_sem_descanso += 1
            self._desbloquear_marco_exato(self.runs_encerradas_sem_descanso, self.MARCOS_RUN_SEM_DESCANSO)

        if not morreu:
            self.runs_aposentadas += 1
            self._desbloquear_marco_exato(self.runs_aposentadas, self.MARCOS_RUN_APOSENTADA)

            if nivel_final >= 80 and descansos_run <= 1 and contratos_run >= 1:
                self.desbloquear("Aposentadoria do Asceta Sombrio")
            if ouro_final >= 8000 and pactos_run == 0 and contratos_run == 0:
                self.desbloquear("Fortuna Sem Pacto")
            if vitorias_run >= 25 and fugas_run == 0 and descansos_run == 0:
                self.desbloquear("Campanha de Ferro Puro")
            if nivel_final >= 101 and descansos_run == 0 and pactos_run >= 1:
                self.desbloquear("Asceta do Centésimo Primeiro")
            if nivel_final >= 101 and contratos_run >= 2 and pactos_run >= 2:
                self.desbloquear("Trono do 101 com Cláusulas")
            if ruptura_maldicao_run and nivel_final >= 100:
                self.desbloquear("Quebrou o Pacto e Ainda Reinou")
            return

        # Abaixo: conquistas para run encerrada em morte.
        if maldicao_ativa_final and nivel_final < 101:
            self.mortes_amaldicoadas += 1
            self._desbloquear_marco_exato(self.mortes_amaldicoadas, self.MARCOS_MORTE_AMALDICOADA)

        if nivel_final >= 100 and descansos_run == 0 and divida_herdeiro <= -1000:
            self.desbloquear("Rei Sem Trono, Herdeiro em Ruínas")

        if nivel_final >= 120 and descansos_run == 0 and divida_herdeiro <= -2000:
            self.desbloquear("Dinastia da Dívida Eterna")

        if contratos_run >= 2 and pactos_run >= 2 and descansos_run == 0 and morreu:
            self.desbloquear("Tudo por Poder, Nada por Amanhã")

        if fugas_run >= 10 and morreu and divida_herdeiro < 0:
            self.desbloquear("Fuga do Presente, Cobrança do Futuro")

        if vitorias_run >= 30 and morreu and ouro_final < 0:
            self.desbloquear("General Falido")

        if almas_run >= 20 and morreu and divida_herdeiro < 0:
            self.desbloquear("Credor de Almas, Devedor de Sangue")

        if contratos_run >= 3 and morreu and nivel_final >= 70:
            self.desbloquear("Cláusula Final Irrevogável")

        if pactos_run >= 2 and fugas_run == 0 and morreu:
            self.desbloquear("Coragem Imprudente")

        if maldicao_ativa_final and contratos_run >= 2 and pactos_run >= 2:
            self.desbloquear("Ruinado Pelo Próprio Juramento")
        if maldicao_ativa_final and divida_herdeiro < 0 and nivel_final >= 90:
            self.desbloquear("Dívida do Centésimo Nível")
        if not ruptura_maldicao_run and maldicao_ativa_final and fugas_run >= 10:
            self.desbloquear("Acorrentado e Em Retirada")

    def _registrar_meta_combos(self):
        self._registrar_combos_pactos()
        self._registrar_combos_contratos()
        self._registrar_combos_universais()
        self._registrar_lendarias()

        # Combos globais que misturam sistemas diferentes da run.
        if self.pactos_sombrios_comprados >= 2 and self.contratos_sombrios_fechados >= 2:
            self.desbloquear("Diplomata do Abismo (2 pactos + 2 contratos)")

        if self.pactos_sombrios_comprados >= 5 and self.contratos_sombrios_fechados >= 5:
            self.desbloquear("Conselheiro das Trevas (5 pactos + 5 contratos)")

        if self.pactos_sombrios_comprados >= 10 and self.contratos_sombrios_fechados >= 10:
            self.desbloquear("Imperador dos Termos Sombrios (10 + 10)")

        if self.sucessos_dominar_alma >= 10 and self.habilidades_ascensao_usadas >= 15:
            self.desbloquear("Canal Arcano do Além (almas + ascensão)")

        if self.sucessos_dominar_alma >= 25 and self.ouro_total_coletado >= 5000:
            self.desbloquear("Banco de Almas e Ouro")

        if self.sucessos_dominar_alma >= 10 and self.falhas_dominar_alma >= 10:
            self.desbloquear("Equilíbrio Profano (10 sucessos + 10 falhas)")

        if self.nemesis_supremos >= 1 and self.vitorias_perfeitas >= 10:
            self.desbloquear("Duelo Contra o Destino")

        if self.nemesis_supremos >= 3 and self.chefes_perfeitos >= 3:
            self.desbloquear("Rei dos Rivais Caídos")

        if self.fugas_bloqueadas_nemesis >= 5 and self.fugas_falhadas >= 10:
            self.desbloquear("Sem Saída, Sem Medo")

        if self.fugas_realizadas >= 20 and self.chefes_derrotados >= 10:
            self.desbloquear("Covardia Calculada, Vitória Absoluta")

        if self.esquivas_bem_sucedidas >= 100 and self.criticos_aplicados >= 75:
            self.desbloquear("Fantasma da Lâmina Crítica")

        if self.vitorias_perfeitas >= 20 and self.abates_sem_descanso >= 80:
            self.desbloquear("Campanha Impecável e Incansável")

        if self.runs_amaldicoadas >= 1 and self.vitorias >= 50:
            self.desbloquear("Triunfo da Linhagem Amaldiçoada")

        if self.runs_amaldicoadas >= 3 and self.mortes_totais >= 3:
            self.desbloquear("Saga da Herança Maldita")

        if self.mortes_totais == 0 and self.vitorias >= 40 and self.pactos_sombrios_comprados >= 3:
            self.desbloquear("Pacto Sem Queda")

        if self.habilidades_ascensao_usadas >= 40 and self.especiais_usados >= 75:
            self.desbloquear("Doutrina da Ascensão Total")

        if self.ouro_total_coletado >= 10000 and self.chefes_derrotados >= 20:
            self.desbloquear("Tesouro Forjado em Sangue de Titãs")

        if self.contratos_sombrios_fechados >= 8 and self.nemesis_criados >= 8:
            self.desbloquear("Advogado do Caos (contratos + nêmesis)")

        if self.pactos_sombrios_comprados >= 12 and self.sucessos_dominar_alma >= 20:
            self.desbloquear("Arquiduque das Sombras Vivas")

        if self.vitorias >= 100 and self.chefes_perfeitos >= 5 and self.nemesis_supremos >= 2:
            self.desbloquear("Crônica do Conquistador Impossível")

        if self.maldicoes_ativadas >= 1 and self.quebras_maldicao_nivel101 >= 1:
            self.desbloquear("Linhagem que Superou o Juramento")
        if self.bloqueios_encerrar_maldicao >= 10 and self.vitorias >= 60:
            self.desbloquear("Recusa em Morrer no Comando")
        if self.rupturas_maldicao >= 2 and self.runs_amaldicoadas >= 2:
            self.desbloquear("Ferreiro de Destinos Quebrados")
        if self.quebras_maldicao_nivel101 >= 2 and self.mortes_amaldicoadas >= 2:
            self.desbloquear("Entre a Coroa e a Cova")

    def _registrar_combos_universais(self):
        combos_universais = [
            # Combos triplos
            (
                self.monstros_derrotados >= 80
                and self.chefes_derrotados >= 8
                and self.vitorias_perfeitas >= 12,
                "Carnificina de Elite (monstros + chefes + perfeitas)",
            ),
            (
                self.descansos_realizados >= 20
                and self.fugas_realizadas >= 10
                and self.esquivas_bem_sucedidas >= 40,
                "Mestre da Sobrevivência Tática",
            ),
            (
                self.maior_ouro_unico >= 150
                and self.ouro_total_coletado >= 3000
                and self.criticos_aplicados >= 50,
                "Pilhagem Cirúrgica",
            ),
            (
                self.especiais_usados >= 60
                and self.habilidades_ascensao_usadas >= 20
                and self.vitorias >= 50,
                "Doutor em Execução Arcana",
            ),
            (
                self.fugas_falhadas >= 12
                and self.nemesis_supremos >= 2
                and self.fugas_bloqueadas_nemesis >= 4,
                "Paradoxo da Retirada",
            ),
            (
                self.runs_amaldicoadas >= 2
                and self.mortes_totais >= 4
                and self.vitorias >= 70,
                "Herdeiro da Ruína",
            ),
            (
                self.sucessos_dominar_alma >= 20
                and self.falhas_dominar_alma >= 12
                and self.contratos_sombrios_fechados >= 8,
                "Médium do Caos Controlado",
            ),
            (
                len(self.monstros_unicos_derrotados) >= 15
                and len(self.chefes_unicos_derrotados) >= 8
                and self.abates_sem_descanso >= 40,
                "Cartógrafo das Guerras Vivas",
            ),
            (
                self.chefes_perfeitos >= 2
                and self.vitorias_perfeitas >= 25
                and self.esquivas_bem_sucedidas >= 80,
                "Coroa da Intocabilidade",
            ),
            (
                self.pactos_sombrios_comprados >= 8
                and self.fugas_realizadas >= 15
                and self.fugas_falhadas >= 10,
                "Diplomacia com o Desespero",
            ),
            (
                self.ouro_total_coletado >= 5000
                and self.descansos_realizados >= 30
                and self.vitorias >= 80,
                "Império Logístico de Guerra",
            ),
            (
                self.nemesis_criados >= 12
                and self.chefes_derrotados >= 15
                and self.criticos_aplicados >= 75,
                "Forjador de Rivais Lendários",
            ),

            # Combos quádruplos
            (
                self.vitorias >= 120
                and self.chefes_derrotados >= 20
                and self.vitorias_perfeitas >= 30
                and self.nemesis_supremos >= 3,
                "Tratado da Guerra Impossível",
            ),
            (
                self.especiais_usados >= 100
                and self.habilidades_ascensao_usadas >= 40
                and self.criticos_aplicados >= 90
                and self.esquivas_bem_sucedidas >= 120,
                "Física Aplicada ao Extermínio",
            ),
            (
                self.pactos_sombrios_comprados >= 10
                and self.contratos_sombrios_fechados >= 10
                and self.sucessos_dominar_alma >= 25
                and self.runs_amaldicoadas >= 1,
                "Ministro do Abismo Administrativo",
            ),
            (
                self.descansos_realizados >= 40
                and self.abates_sem_descanso >= 80
                and self.fugas_realizadas >= 20
                and self.fugas_falhadas >= 15,
                "Doutrina Completa de Campanha",
            ),
            (
                self.maior_ouro_unico >= 250
                and self.ouro_total_coletado >= 10000
                and self.pactos_sombrios_comprados >= 12
                and self.contratos_sombrios_fechados >= 12,
                "Tesouro com Firma no Sangue",
            ),
            (
                self.sucessos_dominar_alma >= 30
                and self.falhas_dominar_alma >= 20
                and self.mortes_totais >= 3
                and self.vitorias >= 90,
                "Teoria Geral da Transcendência Forçada",
            ),
            (
                self.nemesis_criados >= 15
                and self.nemesis_supremos >= 5
                and self.fugas_bloqueadas_nemesis >= 10
                and self.chefes_perfeitos >= 3,
                "Código Penal dos Nêmesis",
            ),
            (
                self.monstros_derrotados >= 150
                and self.chefes_derrotados >= 25
                and len(self.monstros_unicos_derrotados) >= 20
                and len(self.chefes_unicos_derrotados) >= 12,
                "Atlas do Extermínio Total",
            ),
            (
                self.vitorias_perfeitas >= 40
                and self.maior_sequencia_perfeita >= 12
                and self.esquivas_bem_sucedidas >= 150
                and self.criticos_aplicados >= 120,
                "Ópera da Lâmina Invencível",
            ),
            (
                self.runs_amaldicoadas >= 3
                and self.mortes_totais >= 6
                and self.vitorias >= 120
                and self.chefes_derrotados >= 20,
                "Dinastia da Herança Devastada",
            ),
            (
                self.pactos_sombrios_comprados >= 15
                and self.contratos_sombrios_fechados >= 15
                and self.habilidades_ascensao_usadas >= 60
                and self.vitorias >= 130,
                "Conselho Superior do Cataclismo",
            ),
            (
                self.fugas_realizadas >= 35
                and self.fugas_falhadas >= 20
                and self.nemesis_supremos >= 4
                and self.vitorias >= 100,
                "Geometria da Retirada Impossível",
            ),
        ]

        for condicao, nome in combos_universais:
            if condicao:
                self.desbloquear(nome)

    def _registrar_lendarias(self):
        # Conquistas lendárias: condições extremas e altamente específicas.
        lendarias = [
            (
                self.vitorias >= 300
                and self.chefes_derrotados >= 60
                and self.chefes_perfeitos >= 10
                and self.nemesis_supremos >= 8,
                "LENDA: Trono do Fim dos Tronos",
            ),
            (
                self.vitorias_perfeitas >= 120
                and self.maior_sequencia_perfeita >= 40
                and self.esquivas_bem_sucedidas >= 400
                and self.criticos_aplicados >= 260,
                "LENDA: Geometria Impossível da Guerra",
            ),
            (
                self.pactos_sombrios_comprados >= 30
                and self.contratos_sombrios_fechados >= 30
                and self.sucessos_dominar_alma >= 60
                and self.falhas_dominar_alma >= 35,
                "LENDA: Cartório da Eternidade Profana",
            ),
            (
                self.ouro_total_coletado >= 40000
                and self.maior_ouro_unico >= 380
                and self.chefes_derrotados >= 40
                and self.habilidades_ascensao_usadas >= 120,
                "LENDA: Tesouro Juramentado ao Vazio",
            ),
            (
                self.monstros_derrotados >= 400
                and self.chefes_derrotados >= 50
                and len(self.monstros_unicos_derrotados) >= 25
                and len(self.chefes_unicos_derrotados) >= 20,
                "LENDA: Atlas Vivo da Extinção",
            ),
            (
                self.fugas_realizadas >= 80
                and self.fugas_falhadas >= 50
                and self.fugas_bloqueadas_nemesis >= 25
                and self.nemesis_criados >= 35,
                "LENDA: Labirinto Sem Saída",
            ),
            (
                self.runs_amaldicoadas >= 8
                and self.mortes_totais >= 15
                and self.vitorias >= 220
                and self.vitorias_perfeitas >= 70,
                "LENDA: Dinastia Maldita Inquebrável",
            ),
            (
                self.abates_sem_descanso >= 200
                and self.descansos_realizados >= 120
                and self.ouro_total_coletado >= 20000
                and self.especiais_usados >= 200,
                "LENDA: Disciplina do Cataclismo",
            ),
            (
                self.sucessos_dominar_alma >= 75
                and self.habilidades_ascensao_usadas >= 150
                and self.chefes_perfeitos >= 12
                and self.nemesis_supremos >= 6,
                "LENDA: Arconte das Almas Ascendidas",
            ),
            (
                self.vitorias >= 333
                and self.chefes_derrotados >= 33
                and self.criticos_aplicados >= 333
                and self.esquivas_bem_sucedidas >= 333,
                "LENDA: O Número da Guerra",
            ),
            (
                self.pactos_sombrios_comprados >= 22
                and self.contratos_sombrios_fechados >= 22
                and self.nemesis_supremos >= 5
                and self.chefes_perfeitos >= 5
                and self.vitorias_perfeitas >= 55,
                "LENDA: Pentagrama da Coroa Negra",
            ),
            (
                self.vitorias >= 500
                and self.monstros_derrotados >= 700
                and self.chefes_derrotados >= 80
                and self.ouro_total_coletado >= 60000
                and self.sucessos_dominar_alma >= 100,
                "LENDA: Imperador do Último Ciclo",
            ),
        ]

        for condicao, nome in lendarias:
            if condicao:
                self.desbloquear(nome)

    def _registrar_combos_pactos(self):
        combos_pactos = [
            (self.pactos_sombrios_comprados >= 2, "Duas Velas no Abismo"),
            (self.pactos_sombrios_comprados >= 3 and self.vitorias >= 10, "Três Selos, Dez Tumbas"),
            (self.pactos_sombrios_comprados >= 4 and self.fugas_realizadas >= 5, "Pacto e Retirada Estratégica"),
            (self.pactos_sombrios_comprados >= 5 and self.criticos_aplicados >= 30, "Condenação de Precisão"),
            (self.pactos_sombrios_comprados >= 6 and self.esquivas_bem_sucedidas >= 25, "Juramento do Reflexo"),
            (self.pactos_sombrios_comprados >= 7 and self.sucessos_dominar_alma >= 5, "Colecionador de Sussurros"),
            (self.pactos_sombrios_comprados >= 8 and self.contratos_sombrios_fechados >= 3, "Tratado de Duas Mãos"),
            (self.pactos_sombrios_comprados >= 9 and self.nemesis_criados >= 3, "Diplomacia da Vingança"),
            (self.pactos_sombrios_comprados >= 10 and self.chefes_derrotados >= 5, "Coroas por Contrato"),
            (self.pactos_sombrios_comprados >= 12 and self.vitorias_perfeitas >= 10, "Pacto sem Mancha"),
            (self.pactos_sombrios_comprados >= 14 and self.abates_sem_descanso >= 25, "Marcha do Cartório Infernal"),
            (self.pactos_sombrios_comprados >= 16 and self.habilidades_ascensao_usadas >= 15, "Ascensão Contratada"),
            (self.pactos_sombrios_comprados >= 18 and self.ouro_total_coletado >= 2000, "Tesouro Juramentado"),
            (self.pactos_sombrios_comprados >= 20 and self.runs_amaldicoadas >= 1, "Herança com Firma Reconhecida"),
            (self.pactos_sombrios_comprados >= 22 and self.mortes_totais >= 2, "Termos Finais"),
            (self.pactos_sombrios_comprados >= 24 and self.nemesis_supremos >= 2, "Pacto com a Vingança Suprema"),
            (self.pactos_sombrios_comprados >= 26 and self.contratos_sombrios_fechados >= 8, "Consórcio das Trevas"),
            (self.pactos_sombrios_comprados >= 28 and self.chefes_perfeitos >= 2, "Assinatura Régia"),
            (self.pactos_sombrios_comprados >= 30 and self.vitorias >= 120, "Pactário da Guerra Eterna"),
            (
                self.pactos_sombrios_comprados >= 35
                and self.contratos_sombrios_fechados >= 12
                and self.sucessos_dominar_alma >= 20,
                "Tabela Periódica do Pecado",
            ),
        ]
        for condicao, nome in combos_pactos:
            if condicao:
                self.desbloquear(nome)

    def _registrar_combos_contratos(self):
        combos_contratos = [
            (self.contratos_sombrios_fechados >= 2, "Cláusula de Sangue"),
            (self.contratos_sombrios_fechados >= 3 and self.vitorias >= 10, "Ata Notarial de Batalha"),
            (self.contratos_sombrios_fechados >= 4 and self.fugas_falhadas >= 5, "Multa por Desistência"),
            (self.contratos_sombrios_fechados >= 5 and self.criticos_aplicados >= 20, "Parágrafo da Precisão"),
            (self.contratos_sombrios_fechados >= 6 and self.esquivas_bem_sucedidas >= 25, "Anexo do Vento"),
            (self.contratos_sombrios_fechados >= 7 and self.pactos_sombrios_comprados >= 3, "Dupla Rubrica"),
            (self.contratos_sombrios_fechados >= 8 and self.sucessos_dominar_alma >= 5, "Procuração Espiritual"),
            (self.contratos_sombrios_fechados >= 9 and self.nemesis_criados >= 3, "Foro da Vingança"),
            (self.contratos_sombrios_fechados >= 10 and self.chefes_derrotados >= 5, "Jurisdição das Coroas"),
            (self.contratos_sombrios_fechados >= 12 and self.vitorias_perfeitas >= 10, "Ato Sem Contestação"),
            (self.contratos_sombrios_fechados >= 14 and self.habilidades_ascensao_usadas >= 15, "Cláusula Ascendente"),
            (self.contratos_sombrios_fechados >= 16 and self.ouro_total_coletado >= 3000, "Emolumentos do Caos"),
            (self.contratos_sombrios_fechados >= 18 and self.abates_sem_descanso >= 25, "Regime de Urgência Bélica"),
            (self.contratos_sombrios_fechados >= 20 and self.runs_amaldicoadas >= 1, "Contrato de Herança Maldita"),
            (self.contratos_sombrios_fechados >= 22 and self.mortes_totais >= 2, "Termo de Queda Reincidente"),
            (self.contratos_sombrios_fechados >= 24 and self.nemesis_supremos >= 2, "Cláusula de Nêmesis Final"),
            (self.contratos_sombrios_fechados >= 26 and self.pactos_sombrios_comprados >= 8, "Aliança Cartorial Profana"),
            (self.contratos_sombrios_fechados >= 28 and self.chefes_perfeitos >= 2, "Despacho da Coroa Íntegra"),
            (self.contratos_sombrios_fechados >= 30 and self.vitorias >= 140, "Código Bélico Absoluto"),
            (
                self.contratos_sombrios_fechados >= 35
                and self.pactos_sombrios_comprados >= 12
                and self.sucessos_dominar_alma >= 20,
                "Constituição do Abismo",
            ),
        ]
        for condicao, nome in combos_contratos:
            if condicao:
                self.desbloquear(nome)

    def processar_evento(self, evento: str, **contexto):
        # Centraliza os gatilhos de conquista: o jogo só envia "o que aconteceu".
        handler = self._handlers_evento.get(evento)
        if handler:
            handler(contexto)

        if evento in self._eventos_que_alteram_combos:
            self._registrar_meta_combos()

    def exibir(self):
        self._exibidor.exibir(self.desbloqueadas)

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


class NarradorCombate:
    """Gera descrições aleatórias para deixar os golpes mais cinematográficos."""

    FRASES_ATAQUE_BASICO = {
        "Guerreiro": [
            "{atacante} avança com disciplina de arma marcial e quebra a postura de {alvo} num só golpe.",
            "{atacante} gira a lâmina como veterano de campanha e arranca {alvo} da própria linha de defesa.",
            "{atacante} entra no alcance de {alvo} com a calma de quem já sobreviveu a muitas masmorras.",
            "{atacante} transforma treino em impacto e faz {alvo} sentir o peso de um duelo de taverna virado guerra.",
            "{atacante} abaixa o centro de gravidade, mede a distância e desce o aço sobre {alvo} com precisão de soldado.",
            "{atacante} usa o escudo para abrir espaço e a espada para cobrar o erro de {alvo}.",
            "{atacante} luta como quem conhece cada palmo de uma linha de frente e corta {alvo} sem hesitar.",
            "{atacante} bate a arma contra a guarda de {alvo} e responde com um segundo movimento impossível de ignorar.",
            "{atacante} prende {alvo} no ritmo do combate e o castiga com um corte limpo de especialista em armas.",
            "{atacante} avança como campeão de arena e deixa {alvo} entender tarde demais o que é combate marcial.",
        ],
        "Mago": [
            "{atacante} recita uma fórmula curta e faz a própria trama arcana colidir contra {alvo}.",
            "{atacante} move dois dedos, reorganiza o ar e atinge {alvo} com força de estudo proibido.",
            "{atacante} abre o grimório invisível da memória e envia um lampejo de poder direto em {alvo}.",
            "{atacante} molda energia crua como um evocador paciente e despeja o resultado sobre {alvo}.",
            "{atacante} distorce a realidade por um instante e deixa {alvo} no ponto exato da ruptura.",
            "{atacante} traça um sigilo no vazio e a runa explode em {alvo} como resposta inevitável.",
            "{atacante} convoca um dardo arcano disciplinado, sem desperdício, e o entrega ao peito de {alvo}.",
            "{atacante} faz o espaço estremecer ao redor de {alvo} com a confiança de quem estudou além do razoável.",
            "{atacante} empilha vontade, cálculo e mana numa única descarga e marca {alvo} com puro arcano.",
            "{atacante} pronuncia uma sílaba de poder e obriga {alvo} a enfrentar a estrutura invisível da magia.",
        ],
        "Arqueiro": [
            "{atacante} trata {alvo} como presa marcada e solta a flecha no exato erro do movimento inimigo.",
            "{atacante} dispara com frieza de patrulheiro e acha a fenda que a armadura de {alvo} jurava esconder.",
            "{atacante} se move como caçador da fronteira e converte distância em sentença para {alvo}.",
            "{atacante} lê o terreno, encontra o ângulo e castiga {alvo} com precisão de vigia das matas.",
            "{atacante} acompanha a respiração de {alvo} por um instante e manda a seta no fim do compasso.",
            "{atacante} atira como quem já perseguiu monstros por dias e não pretende deixar {alvo} escapar agora.",
            "{atacante} faz do campo aberto sua vantagem e perfura {alvo} com técnica de caçador experiente.",
            "{atacante} espera a menor abertura de {alvo} e responde com um disparo digno de um matador de dragões.",
            "{atacante} encontra a trilha do golpe no próprio vento e deixa {alvo} no centro do disparo.",
            "{atacante} age com a paciência letal de quem protege as bordas da civilização e pune {alvo} à distância.",
        ],
    }

    FRASES_HABILIDADE_ESPECIAL = {
        "Golpe Duplo": [
            "{atacante} abre a guarda de {alvo} com a primeira passada e faz a segunda parecer uma execução de manual.",
            "{atacante} combina dois cortes de escola marcial e desmonta {alvo} antes da reação chegar.",
            "{atacante} entra num ritmo de guerra curta e carimba {alvo} com dois impactos quase simultâneos.",
            "{atacante} trata a própria espada como extensão do treino e varre {alvo} em dois tempos perfeitos.",
            "{atacante} esmaga a postura de {alvo} no primeiro golpe e cobra o segundo como veterano implacável.",
        ],
        "Bola de Fogo": [
            "{atacante} reúne fogo arcano em órbita na palma e arremessa a explosão inteira contra {alvo}.",
            "{atacante} evoca uma esfera rubra de energia e faz {alvo} desaparecer atrás das labaredas.",
            "{atacante} condensa calor, vontade e fórmula num projétil flamejante que desaba sobre {alvo}.",
            "{atacante} usa magia de evocação sem cerimônia e transforma {alvo} no centro do clarão.",
            "{atacante} acende o próprio ar diante de {alvo} e fecha a distância com uma bola de fogo devastadora.",
        ],
        "Flecha Precisa": [
            "{atacante} encontra a junta exata da defesa de {alvo} como se estivesse rastreando a presa há dias.",
            "{atacante} segura a corda até o último instante e atravessa o único ponto vulnerável de {alvo}.",
            "{atacante} responde ao menor vacilo de {alvo} com uma seta de precisão cruel e calculada.",
            "{atacante} faz do disparo uma técnica de caçador consumado e perfura a confiança de {alvo}.",
            "{atacante} escolhe o vão certo entre placa, couro e arrogância, e pune {alvo} sem desperdício.",
        ],
    }

    FRASES_ASCENSAO = {
        "Guerreiro": [
            "{atacante} libera uma técnica digna de campeão marcial e faz {alvo} suportar o peso de uma companhia inteira.",
            "{atacante} rompe os próprios limites como herói de campanha épica e transforma {alvo} em alvo de cerco.",
            "{atacante} ergue a arma com autoridade de senhor da guerra e abate {alvo} como se estivesse tomando uma fortaleza.",
            "{atacante} descarrega {habilidade} com a força de um confronto contra gigantes e deixa {alvo} sem chão.",
            "{atacante} conduz {habilidade} como veterano lendário, e {alvo} recebe o impacto de uma saga inteira.",
        ],
        "Mago": [
            "{atacante} ultrapassa a magia comum e faz {alvo} encarar uma distorção real nas leis do mundo.",
            "{atacante} dobra a estrutura da realidade em volta de {alvo} e despeja {habilidade} como cataclismo arcano.",
            "{atacante} convoca poder de alto círculo e transforma {alvo} no centro de uma anomalia perfeita.",
            "{atacante} lança {habilidade} com rigor de arquimago, e o campo inteiro vacila antes de atingir {alvo}.",
            "{atacante} faz a própria teoria arcana ruir sobre {alvo} numa explosão de poder disciplinado.",
        ],
        "Arqueiro": [
            "{atacante} some do ritmo do confronto como caçador sobrenatural e reaparece no ângulo fatal de {alvo}.",
            "{atacante} conduz {habilidade} como predador de monstros lendários e escolhe {alvo} como a presa do dia.",
            "{atacante} transforma alcance, terreno e paciência em uma sentença perfeita para {alvo}.",
            "{atacante} deixa o vento fechar a trilha do disparo e faz {alvo} receber a flecha como decreto inevitável.",
            "{atacante} usa {habilidade} com a frieza de quem já enfrentou dragões, e {alvo} paga o preço inteiro.",
        ],
    }

    @staticmethod
    def _classe(atacante):
        if isinstance(atacante, Guerreiro):
            return "Guerreiro"
        if isinstance(atacante, Mago):
            return "Mago"
        if isinstance(atacante, Arqueiro):
            return "Arqueiro"
        return "Inimigo"

    @classmethod
    def narrar_ataque_basico(cls, atacante, alvo):
        classe = cls._classe(atacante)
        frases = cls.FRASES_ATAQUE_BASICO.get(classe)
        if not frases:
            return f"{atacante.nome} atacou {alvo.nome}."
        return random.choice(frases).format(atacante=atacante.nome, alvo=alvo.nome)

    @classmethod
    def narrar_habilidade_especial(cls, atacante, alvo, habilidade):
        frases = cls.FRASES_HABILIDADE_ESPECIAL.get(habilidade)
        if not frases:
            return f"{atacante.nome} usou {habilidade} contra {alvo.nome}."
        return random.choice(frases).format(atacante=atacante.nome, alvo=alvo.nome, habilidade=habilidade)

    @classmethod
    def narrar_habilidade_ascensao(cls, atacante, alvo, habilidade):
        classe = cls._classe(atacante)
        frases = cls.FRASES_ASCENSAO.get(classe)
        if not frases:
            return f"{atacante.nome} usou {habilidade} contra {alvo.nome}."
        return random.choice(frases).format(atacante=atacante.nome, alvo=alvo.nome, habilidade=habilidade)


class SistemaCombate:
    """Agrupa regras de dano, ataque, esquiva e fuga."""

    @staticmethod
    def aplicar_dano(alvo, dano):
        # Primeiro consome defesa, depois vida. É o coração do cálculo de combate.
        dano_original = dano

        if alvo.defesa > 0:
            if dano <= alvo.defesa:
                alvo.defesa -= dano
                print(InterfaceRPG.destaque(f"{alvo.nome} bloqueou o ataque. Defesa restante: {alvo.defesa}", icone="🧱", cor=InterfaceRPG.AZUL))
                dano = 0
            else:
                dano -= alvo.defesa
                print(InterfaceRPG.destaque(f"{alvo.nome} perdeu toda a defesa.", icone="🛡️", cor=InterfaceRPG.AMARELO))
                alvo.defesa = 0

        alvo.vida -= dano
        if alvo.vida < 0:
            alvo.vida = 0

        if dano > 0:
            if hasattr(alvo, "registrar_dano_batalha"):
                alvo.registrar_dano_batalha()
            print(InterfaceRPG.destaque(f"{alvo.nome} recebeu {dano} de dano.", icone="💢", cor=InterfaceRPG.VERMELHO))
            print(f"Vida atual: {alvo.vida}/{alvo.vida_max}")
        elif dano_original > 0:
            print(InterfaceRPG.destaque(f"{alvo.nome} não perdeu vida neste ataque.", icone="😮‍💨", cor=InterfaceRPG.BRANCO))

    @staticmethod
    def atacar(atacante, alvo):
        # Ataque padrão com chance de crítico para deixar cada turno menos previsível.
        dano = atacante.ataque
        critico = False

        if random.random() < 0.20:
            dano = int(dano * 1.8)
            critico = True
            print(InterfaceRPG.destaque(f"CRÍTICO! {atacante.nome} causará {dano} de dano.", icone=InterfaceRPG.ICONES["critico"], cor=InterfaceRPG.AMARELO))

        print(
            InterfaceRPG.destaque(
                NarradorCombate.narrar_ataque_basico(atacante, alvo),
                icone=InterfaceRPG.ICONES["batalha"],
                cor=InterfaceRPG.BRANCO,
            )
        )
        SistemaCombate.aplicar_dano(alvo, dano)
        return critico

    @staticmethod
    def tentar_esquiva(jogador):
        # Esquiva é escolha do jogador e custa stamina (acertando ou errando).
        escolha = input("Deseja tentar esquivar do ataque? (S/N): ").strip().lower()

        if escolha != "s":
            return False

        if jogador.stamina < 5:
            print("Sem stamina suficiente para esquivar.")
            return False

        chance_esquiva = min(0.10 + (jogador.nivel * 0.05) + jogador.bonus_esquiva, 0.75)
        if random.random() < chance_esquiva:
            jogador.stamina -= 5
            print(InterfaceRPG.destaque(f"{jogador.nome} esquivou do ataque.", icone="🌀", cor=InterfaceRPG.VERDE))
            print(f"Stamina: {jogador.stamina}/{jogador.stamina_max}")
            jogador.conquistas.processar_evento("esquiva_bem_sucedida")
            return True

        jogador.stamina = max(0, jogador.stamina - 10)
        print(InterfaceRPG.destaque(f"{jogador.nome} tentou esquivar, mas falhou.", icone="💫", cor=InterfaceRPG.AMARELO))
        print(f"Stamina: {jogador.stamina}/{jogador.stamina_max}")
        return False

    @staticmethod
    def tentar_fuga(jogador):
        # Fuga é uma aposta: pode salvar a run ou punir com dano.
        escolha = input("Deseja mesmo fugir? (S/N): ").strip().lower()

        if escolha != "s":
            return False

        if random.random() > 0.5:
            penalidade_xp = 10 + (jogador.nivel * 2)
            penalidade_ouro = 5 + (jogador.nivel * 3)
            if jogador.progressao.maldicao_ultimo_nivel_ativa and jogador.nivel < 101:
                # Maldição hardcore: fugir fica bem mais caro.
                penalidade_xp *= 2
                penalidade_ouro *= 2

            perda_xp = min(jogador.progressao.xp, penalidade_xp)
            perda_ouro = min(jogador.progressao.ouro, penalidade_ouro)
            jogador.progressao.xp -= perda_xp
            jogador.progressao.ouro -= perda_ouro

            print(InterfaceRPG.destaque(f"{jogador.nome} conseguiu fugir com sucesso.", icone=InterfaceRPG.ICONES["fuga"], cor=InterfaceRPG.VERDE))
            print("Foi por pouco.")
            print(f"Penalidade da retirada: -{perda_xp} XP e -{perda_ouro} ouro.")
            jogador.vida = max(1, jogador.vida)
            jogador.defesa = max(0, jogador.defesa)
            jogador.mana = max(0, jogador.mana)
            jogador.stamina = max(0, jogador.stamina)
            jogador.conquistas.processar_evento("fuga_realizada")
            return True

        print(InterfaceRPG.destaque(f"{jogador.nome} tentou fugir, mas falhou.", icone="🪤", cor=InterfaceRPG.VERMELHO))
        print("Você tropeçou e ficou vulnerável.")
        jogador.vida = max(0, jogador.vida - 15)
        jogador.conquistas.processar_evento("fuga_falhada")
        return False


class MotorJogo:
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

    def criar_conquistas(self):
        return SistemaConquistas(
            catalogo_monstros=Monstro.TIPOS.keys(),
            catalogo_chefes=Chefao.TIPOS.keys(),
        )

    def iniciar_nova_run(self):
        self.estado_run = EstadoRun()

    def aplicar_heranca_inicial(self, jogador):
        jogador.progressao.ouro += self.heranca_ouro
        jogador.progressao.almas += self.heranca_almas
        if self.maldicao_linhagem_ativa:
            jogador.progressao.aplicar_maldicao_ultimo_nivel()
        if self.heranca_ouro != 0 or self.heranca_almas != 0:
            print(
                f"\nLegado recebido: Ouro {self.heranca_ouro:+} | "
                f"Almas {self.heranca_almas:+}"
            )
        self.heranca_ouro = 0
        self.heranca_almas = 0

    def verificar_gatilho_juramento_sem_descanso(self, jogador):
        # Gatilho da maldição hardcore: nível 50 sem nenhum descanso na run atual.
        if jogador.progressao.maldicao_ultimo_nivel_ativa:
            return
        if jogador.nivel >= 50 and self.descansos_na_run == 0:
            print(InterfaceRPG.destaque("Seu corpo venceu a fadiga, mas perdeu a liberdade.", icone="🥀", cor=InterfaceRPG.VERMELHO))
            print(InterfaceRPG.destaque("O Juramento do Sem Descanso desperta a Maldição do Último Nível.", icone=InterfaceRPG.ICONES["maldicao"], cor=InterfaceRPG.VERMELHO))
            jogador.progressao.aplicar_maldicao_ultimo_nivel()

    def definir_epilogo_encerramento(self, jogador):
        # Escolhe um epílogo de aposentadoria conforme o estilo da run.
        epilogos_honrados = [
            "Você pendurou a arma na parede da taverna.\n"
            "Não foi covardia. Foi escolha.\n"
            "Alguns chamaram de fim cedo; você chamou de vida longa.",
            "Sem atalhos, sem barganhas, sem dívida com o abismo.\n"
            "Você encerrou a aventura com as mãos limpas e a consciência firme.",
            "Na última fogueira da campanha, você escolheu não avançar.\n"
            "Nem toda vitória está em continuar.\n"
            "Às vezes, vencer é simplesmente voltar.",
        ]
        epilogos_pragmaticos = [
            "Você deixou o campo antes da última página.\n"
            "Não há vergonha nisso.\n"
            "Toda lenda que sobrevive é uma história que escolheu parar.",
            "Você cedeu quando precisou, atacou quando deu, recuou quando era certo.\n"
            "Não foi bonito o tempo todo, mas foi humano.",
            "Os vilarejos ainda sussurram seu nome quando anoitece.\n"
            "Você não voltou para o front, mas o front nunca saiu de você.",
        ]
        epilogos_sombrios = [
            "Você saiu vivo, mas não saiu sozinho.\n"
            "Cada pacto ficou atrás dos seus passos, como pegadas que nunca secam.",
            "Você trocou glória por dias comuns.\n"
            "No mercado, vendem pão; na memória, você compra paz que não vem.",
            "Você venceu reis e monstros, mas aprendeu cedo:\n"
            "trono nenhum devolve os mortos.",
        ]
        epilogos_lendarios = [
            "Quando você partiu, o mundo ficou menor.\n"
            "Não por falta de monstros,\n"
            "mas por falta de alguém capaz de encará-los sem piscar.",
            "Seu nome virou canção de guerra e aviso de prudência.\n"
            "A campanha terminou; o legado, não.",
        ]

        usou_artimanhas = self.usou_artimanhas_na_run(jogador)
        estilo_honrado = (not usou_artimanhas) and self.fugas_na_run <= 2
        estilo_lendario = jogador.nivel >= 100 or self.vitorias_na_run >= 45
        estilo_sombrio = usou_artimanhas or jogador.progressao.almas_coletadas_run >= 10

        if estilo_lendario:
            texto = random.choice(epilogos_lendarios)
        elif estilo_honrado:
            texto = random.choice(epilogos_honrados)
        elif estilo_sombrio:
            texto = random.choice(epilogos_sombrios)
        else:
            texto = random.choice(epilogos_pragmaticos)

        self.epilogo_encerramento = texto + "\n\nA aventura acabou. A consequência, não."

    def usou_artimanhas_na_run(self, jogador):
        return (
            self.compras_sombrias_na_run > 0
            or self.contratos_sombrios_na_run > 0
            or jogador.progressao.ruptura_maldicao_realizada
        )

    def executar_julgamento_reflexo_final(self, jogador):
        print(InterfaceRPG.titulo("Reflexo Final", "O último espelho não devolve piedade", cor=InterfaceRPG.MAGENTA, icone=InterfaceRPG.ICONES["reflexo"]))
        print("No limiar do fim, uma cópia sua surge das sombras.")
        print('"Chegou até aqui... mas o que exatamente você se tornou?"')

        while True:
            print(
                InterfaceRPG.menu(
                    "Escolha do Reflexo",
                    [
                        ("1", "Eu faria tudo de novo"),
                        ("2", "Não tenho certeza"),
                        ("3", "Eu me arrependo"),
                    ],
                    cor=InterfaceRPG.MAGENTA,
                )
            )
            resposta = input("Sua resposta: ").strip()
            if resposta in ("1", "2", "3"):
                break
            print("Opção inválida.")

        usou_artimanhas = self.usou_artimanhas_na_run(jogador)
        if not usou_artimanhas:
            self.final_reflexo_tipo = "integro"
            jogador.conquistas.processar_evento("julgamento_reflexo", tipo="integro")
            print("\nReflexo: 'Sem atalhos... ainda assim deixou um rastro de sangue.'")
            print("Reflexo: 'Agora, sem força, você chamaria isso de justiça?'")
            jogador.resetar_para_base_classe()
            jogador.mostrar_status()
            print("\nO Reflexo sorri e desfere o golpe final.")
            SistemaCombate.aplicar_dano(jogador, jogador.vida_max)
        else:
            self.final_reflexo_tipo = "corrompido"
            jogador.conquistas.processar_evento("julgamento_reflexo", tipo="corrompido")
            print("\nReflexo: 'Você não subiu. Você negociou cada degrau.'")
            print("O Reflexo começa a arrancar suas conquistas uma a uma...")
            while jogador.conquistas.desbloqueadas:
                conquista = jogador.conquistas.desbloqueadas.pop()
                print(f"Conquista perdida: {conquista}")
            print("Reflexo: 'Agora que está perdendo tudo... valeu a pena?'")
            print("Sem resposta, você é executado pelo próprio espelho.")
            jogador.vida = 0

    def registrar_heranca_pos_morte(self, jogador):
        ouro_final = jogador.progressao.ouro
        if ouro_final > 0:
            self.heranca_ouro = int(ouro_final * 0.10)
        else:
            self.heranca_ouro = ouro_final

        if self.usou_mercador_sombrio_run and jogador.progressao.almas_coletadas_run > 0:
            self.heranca_almas = -jogador.progressao.almas_coletadas_run
            print(
                "\nMaldição Sombria herdada: o herdeiro inicia com "
                f"{self.heranca_almas} almas."
            )
            jogador.conquistas.processar_evento("heranca_amaldicoada")
        else:
            self.heranca_almas = jogador.progressao.almas

        # Se morreu ainda amaldiçoado antes do 101, a linhagem continua amaldiçoada.
        self.maldicao_linhagem_ativa = (
            jogador.progressao.maldicao_ultimo_nivel_ativa and jogador.nivel < 101
        )

    def registrar_evento_fim_run(self, morreu: bool):
        divida_herdeiro = self.heranca_ouro if self.heranca_ouro < 0 else 0
        self.jogador.conquistas.processar_evento(
            "fim_run",
            morreu=morreu,
            nivel_final=self.jogador.nivel,
            descansos_na_run=self.descansos_na_run,
            contratos_na_run=self.contratos_sombrios_na_run,
            pactos_na_run=self.compras_sombrias_na_run,
            fugas_na_run=self.fugas_na_run,
            vitorias_na_run=self.vitorias_na_run,
            ouro_final=self.jogador.progressao.ouro,
            divida_herdeiro=divida_herdeiro,
            almas_coletadas_run=self.jogador.progressao.almas_coletadas_run,
            maldicao_ativa_final=self.jogador.progressao.maldicao_ultimo_nivel_ativa,
            ruptura_maldicao_run=self.jogador.progressao.ruptura_maldicao_realizada,
        )

    def escalar_inimigo_por_niveis(self, inimigo, niveis_extra):
        if niveis_extra <= 0:
            return

        if isinstance(inimigo, Chefao):
            fator_vida = 1.0 + (niveis_extra * 0.22)
            fator_ataque = 1.0 + (niveis_extra * 0.16)
            fator_defesa = 1.0 + (niveis_extra * 0.18)
            fator_recompensa = 1.0 + (niveis_extra * 0.20)
        else:
            fator_vida = 1.0 + (niveis_extra * 0.09)
            fator_ataque = 1.0 + (niveis_extra * 0.06)
            fator_defesa = 1.0 + (niveis_extra * 0.07)
            fator_recompensa = 1.0 + (niveis_extra * 0.09)

        inimigo.nivel += niveis_extra
        inimigo.vida_max = max(1, int(inimigo.vida_max * fator_vida))
        inimigo.vida = inimigo.vida_max
        inimigo.ataque = max(1, int(inimigo.ataque * fator_ataque))
        inimigo.defesa_max = max(0, int(inimigo.defesa_max * fator_defesa))
        inimigo.defesa = inimigo.defesa_max
        inimigo.xp = max(1, int(inimigo.xp * fator_recompensa))
        ouro_min = max(1, int(inimigo.faixa_ouro[0] * fator_recompensa))
        ouro_max = max(ouro_min + 1, int(inimigo.faixa_ouro[1] * fator_recompensa))
        inimigo.faixa_ouro = (ouro_min, ouro_max)

    def aplicar_nemesis(self, inimigo):
        strikes = self.nemesis_strikes.get(inimigo.nome, 0)
        if strikes <= 0:
            return

        bonus_nivel = 5 if strikes == 1 else 10 if strikes == 2 else 15
        self.escalar_inimigo_por_niveis(inimigo, bonus_nivel)

        print(f"\nNÊMESIS: {inimigo.nome} retornou mais forte (+{bonus_nivel} níveis).")
        if strikes >= 3:
            print("Regra dos 3 Strikes ativa: fuga bloqueada contra este inimigo.")

    def registrar_fuga_nemesis(self, nome_inimigo):
        if not nome_inimigo:
            return

        atual = self.nemesis_strikes.get(nome_inimigo, 0)
        novo = min(3, atual + 1)
        self.nemesis_strikes[nome_inimigo] = novo

        print(f"NÊMESIS atualizado para {nome_inimigo}: Strike {novo}/3.")
        if self.jogador:
            self.jogador.conquistas.processar_evento("nemesis_strike", strike=novo, nome_inimigo=nome_inimigo)

    def tentar_dominar_alma(self, jogador, inimigo):
        if jogador.nivel < 50:
            return

        if jogador.vida <= 1:
            print("Seu estado atual não permite tentar dominar uma alma.")
            return

        escolha = input("Deseja tentar dominar a alma do inimigo derrotado? (S/N): ").strip().lower()
        if escolha != "s":
            return

        chance_dominar = min(0.15 + (jogador.nivel * 0.01), 0.85)
        if random.random() < chance_dominar:
            if isinstance(inimigo, Chefao):
                ganho = random.choice([0, 2, 3])
            else:
                ganho = random.choice([0, 1, 2])

            if ganho > 0:
                jogador.progressao.adicionar_almas(ganho)
                print(
                    f"{jogador.nome} dominou almas com sucesso: +{ganho} "
                    f"(Total: {jogador.progressao.almas})"
                )
                jogador.conquistas.processar_evento("dominio_alma_sucesso", ganho=ganho, eh_chefao=isinstance(inimigo, Chefao))
            else:
                print("A alma resistiu ao domínio e se dispersou no vazio.")
            return

        dano = max(1, int(jogador.vida * 0.20))
        jogador.vida = max(0, jogador.vida - dano)
        print(f"Falha no domínio. Reação espiritual: -{dano} de vida.")
        print(f"Vida atual: {jogador.vida}/{jogador.vida_max}")
        jogador.conquistas.processar_evento("dominio_alma_falha", eh_chefao=isinstance(inimigo, Chefao))
        if not jogador.esta_vivo():
            print("Seu corpo não suportou o choque espiritual.")

    def menu_mercador_sombrio(self, jogador):
        if jogador.nivel < 50:
            print("\nO Mercador Sombrio só negocia com aventureiros de nível 50 ou mais.")
            return

        opcoes_pactos = {
            "1": {
                "nome": "Pacto da Vitalidade",
                "custo": 40,
                "bonus": {"vida": 80, "defesa": 10},
            },
            "2": {
                "nome": "Pacto da Carnificina",
                "custo": 55,
                "bonus": {"ataque": 18},
            },
            "3": {
                "nome": "Pacto da Muralha",
                "custo": 50,
                "bonus": {"defesa": 35, "vida": 30},
            },
            "4": {
                "nome": "Pacto Arcano",
                "custo": 65,
                "bonus": {"mana": 40, "stamina": 35, "ataque": 8},
            },
        }

        while True:
            print(
                InterfaceRPG.menu(
                f"{InterfaceRPG.ICONES['mercador']} Mercador Sombrio",
                    [
                        ("1", "Comprar Pacto Sombrio"),
                        ("2", "Ver Contratos Sombrios"),
                        ("3", "Voltar"),
                    ],
                    rodape=(
                        f"Almas: {jogador.progressao.almas} | "
                        f"Compras restantes: {max(0, 2 - self.compras_sombrias_na_run)}"
                    ),
                    cor=InterfaceRPG.MAGENTA,
                )
            )

            escolha_menu = input("Escolha uma opção: ").strip()
            if escolha_menu == "3":
                return

            if escolha_menu == "2":
                self.exibir_contratos_sombrios(jogador)
                continue

            if escolha_menu != "1":
                print("Opção inválida.")
                continue

            if self.compras_sombrias_na_run >= 2:
                print("\nLimite da run atingido: máximo de 2 compras sombrias.")
                continue

            print(
                InterfaceRPG.caixa(
                    "📜 Pactos Disponíveis",
                    [
                        *(f"{chave}. {opcao['nome']} | Custo: {opcao['custo']} almas" for chave, opcao in opcoes_pactos.items()),
                        "5. Cancelar",
                    ],
                    cor=InterfaceRPG.VERMELHO,
                )
            )

            escolha = input("Escolha um pacto: ").strip()
            if escolha == "5":
                continue
            if escolha not in opcoes_pactos:
                print("Opção inválida.")
                continue

            opcao = opcoes_pactos[escolha]
            custo = opcao["custo"]
            if jogador.progressao.almas < custo:
                print("Almas insuficientes para selar esse pacto.")
                continue

            jogador.progressao.almas -= custo
            jogador.progressao.aplicar_bonus_ascensao(opcao["bonus"])
            self.compras_sombrias_na_run += 1
            self.usou_mercador_sombrio_run = True
            self.bonus_nivel_monstros += 2
            self.bonus_nivel_chefes += 5
            jogador.conquistas.processar_evento("pacto_sombrio_comprado")

            print(f"\nPacto selado: {opcao['nome']}.")
            print(
                "O mundo reagiu ao pacto: "
                f"Monstros +{self.bonus_nivel_monstros} níveis globais | "
                f"Chefões +{self.bonus_nivel_chefes} níveis globais."
            )

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

    def ativar_rotacao_contratos(self):
        self.contratos_rotacao = random.sample(
            self.CATALOGO_CONTRATOS,
            k=min(3, len(self.CATALOGO_CONTRATOS)),
        )
        self.rotacao_contratos_ativa = True
        self.contrato_comprado_no_ciclo = False
        print(
            InterfaceRPG.caixa(
                "📜 Novos Contratos Sombrios",
                [f"{contrato['nome']}: {contrato['descricao']}" for contrato in self.contratos_rotacao],
                cor=InterfaceRPG.MAGENTA,
            )
        )

    def _reduzir_atributo(self, jogador, atributo, valor):
        if atributo == "ataque":
            jogador.ataque = max(1, jogador.ataque - valor)
            return

        limites_min = {
            "vida_max": 1,
            "defesa_max": 0,
            "mana_max": 0,
            "stamina_max": 1,
        }
        if atributo in limites_min:
            novo_valor = max(limites_min[atributo], getattr(jogador, atributo) - valor)
            setattr(jogador, atributo, novo_valor)
            atual = atributo.replace("_max", "")
            setattr(jogador, atual, min(getattr(jogador, atual), novo_valor))

    def aplicar_contrato_sombrio(self, jogador, contrato):
        bonus = contrato.get("bonus", {})
        if bonus:
            jogador.progressao.aplicar_bonus_ascensao(bonus)

        penalidade = contrato.get("penalidade", {})

        perda_vida_pct = penalidade.get("vida_atual_pct_loss")
        if perda_vida_pct:
            dano = max(1, int(jogador.vida * perda_vida_pct))
            jogador.vida = max(1, jogador.vida - dano)

        for atributo, valor in penalidade.get("reduzir_atributo_flat", {}).items():
            self._reduzir_atributo(jogador, atributo, valor)

        for atributo, percentual in penalidade.get("reduzir_max_pct", {}).items():
            valor_reducao = int(getattr(jogador, atributo) * percentual)
            self._reduzir_atributo(jogador, atributo, max(1, valor_reducao))

        if "multiplicador_xp" in penalidade:
            jogador.progressao.multiplicador_xp *= penalidade["multiplicador_xp"]

        if "multiplicador_ouro" in penalidade:
            jogador.progressao.multiplicador_ouro *= penalidade["multiplicador_ouro"]

        if "reduzir_bonus_monstros" in penalidade:
            self.bonus_nivel_monstros = max(
                0,
                self.bonus_nivel_monstros - penalidade["reduzir_bonus_monstros"],
            )

    def calcular_custo_contrato(self, contrato):
        """Escala custo pela potência real: ganhos altos ficam muito caros."""
        base = contrato["custo"]
        bonus = contrato.get("bonus", {})
        penalidade = contrato.get("penalidade", {})

        score_bonus = (
            bonus.get("vida", 0) / 20.0
            + bonus.get("defesa", 0) / 15.0
            + bonus.get("ataque", 0) / 4.0
            + bonus.get("mana", 0) / 20.0
            + bonus.get("stamina", 0) / 18.0
            + bonus.get("esquiva", 0.0) * 120.0
        )

        score_bonus += max(0.0, (penalidade.get("multiplicador_xp", 1.0) - 1.0) * 120.0)
        score_bonus += max(0.0, (penalidade.get("multiplicador_ouro", 1.0) - 1.0) * 100.0)

        # Penalidades reduzem um pouco o score, mas sem anular ganhos absurdos.
        reducao = 0.0
        reducao += penalidade.get("vida_atual_pct_loss", 0.0) * 30.0
        for valor in penalidade.get("reduzir_atributo_flat", {}).values():
            reducao += valor / 12.0
        for pct in penalidade.get("reduzir_max_pct", {}).values():
            reducao += pct * 35.0
        if penalidade.get("multiplicador_xp", 1.0) < 1.0:
            reducao += (1.0 - penalidade["multiplicador_xp"]) * 60.0
        if penalidade.get("multiplicador_ouro", 1.0) < 1.0:
            reducao += (1.0 - penalidade["multiplicador_ouro"]) * 50.0
        if penalidade.get("reduzir_bonus_monstros", 0) > 0:
            reducao += penalidade["reduzir_bonus_monstros"] * 5.0

        score_liquido = max(0.0, score_bonus - (reducao * 0.55))
        custo = base + int(score_liquido * 7.5)

        # Faixas de custo agressivas para contratos muito fortes.
        if score_liquido >= 32:
            custo = int(custo * 1.80)
        elif score_liquido >= 24:
            custo = int(custo * 1.55)
        elif score_liquido >= 16:
            custo = int(custo * 1.30)

        # Evita valores inviáveis para a economia atual de almas.
        return min(320, max(base, custo))

    def exibir_contratos_sombrios(self, jogador):
        if not self.rotacao_contratos_ativa:
            print("\nNenhuma rotação de contratos disponível agora.")
            return

        if self.contrato_comprado_no_ciclo:
            print("\nVocê já fechou um contrato nesta rotação.")
            return

        linhas = [f"Almas: {jogador.progressao.almas}", ""]
        for idx, contrato in enumerate(self.contratos_rotacao, start=1):
            custo_real = self.calcular_custo_contrato(contrato)
            linhas.append(f"{idx}. {contrato['nome']} | Custo: {custo_real} almas")
            linhas.append(f"   {contrato['descricao']}")
        linhas.append("")
        linhas.append(f"{len(self.contratos_rotacao) + 1}. Voltar")
        print(InterfaceRPG.caixa("📜 Contratos Sombrios", linhas, cor=InterfaceRPG.MAGENTA))

        escolha = input("Escolha um contrato: ").strip()
        if not escolha.isdigit():
            print("Opção inválida.")
            return

        indice = int(escolha) - 1
        if indice == len(self.contratos_rotacao):
            return
        if indice < 0 or indice >= len(self.contratos_rotacao):
            print("Opção inválida.")
            return

        contrato = self.contratos_rotacao[indice]
        custo_real = self.calcular_custo_contrato(contrato)
        if jogador.progressao.almas < custo_real:
            print("Almas insuficientes para esse contrato.")
            return

        jogador.progressao.almas -= custo_real
        self.aplicar_contrato_sombrio(jogador, contrato)
        self.contrato_comprado_no_ciclo = True
        self.contratos_sombrios_na_run += 1
        jogador.conquistas.processar_evento("contrato_sombrio_fechado")
        print(f"\nContrato selado: {contrato['nome']}.")

    def escolher_personagem(self):
        # Etapa inicial do jogo: nome + classe, sem complicar muito a entrada.
        print(
            InterfaceRPG.titulo(
                "Criação de Herói",
                "Escolha um nome, uma classe e aceite o caos",
                cor=InterfaceRPG.CIANO,
                icone="🧙",
            )
        )
        nome = input("Digite o nome do seu personagem: ").strip().title()

        while not nome:
            nome = input("Digite um nome válido: ").strip().title()

        conquistas = self.criar_conquistas()

        while True:
            print(
                InterfaceRPG.menu(
                    "🧬 Classes",
                    [
                        ("1", "Guerreiro | brutal, resistente, físico"),
                        ("2", "Mago | explosivo, mana alta, arcano"),
                        ("3", "Arqueiro | ágil, preciso, técnico"),
                    ],
                    cor=InterfaceRPG.CIANO,
                )
            )
            entrada = input("Escolha o número da classe: ").strip()

            if entrada == "1":
                return Guerreiro(nome, conquistas)
            if entrada == "2":
                return Mago(nome, conquistas)
            if entrada == "3":
                return Arqueiro(nome, conquistas)

            print("Opção inválida. Tente novamente.")

    def turno_jogador(self, jogador, inimigo):
        # Loop do turno do player até ele executar uma ação válida.
        fuga_bloqueada = self.nemesis_strikes.get(inimigo.nome, 0) >= 3
        while True:
            print(
                InterfaceRPG.menu(
                    "🎮 Sua Vez",
                    [
                        ("1", "Ataque padrão"),
                        ("2", "Ataque especial"),
                        ("3", "Habilidade de ascensão"),
                        ("4", "Ver status"),
                        ("5", "Fugir"),
                    ],
                    rodape=f"Adversário: {inimigo.nome} | Fuga bloqueada: {'SIM' if fuga_bloqueada else 'NÃO'}",
                    cor=InterfaceRPG.VERDE,
                )
            )
            entrada = input("Escolha uma ação: ").strip()

            if entrada == "1":
                critico = SistemaCombate.atacar(jogador, inimigo)
                if critico:
                    jogador.conquistas.processar_evento("critico_aplicado")
                return "ataque"

            if entrada == "2":
                if jogador.habilidade_especial(inimigo):
                    return "especial"
                continue

            if entrada == "3":
                if jogador.progressao.usar_habilidade_ascensao(inimigo):
                    return "ascensao"
                continue

            if entrada == "4":
                jogador.mostrar_status()
                inimigo.mostrar_status()
                continue

            if entrada == "5":
                if fuga_bloqueada:
                    print("Fuga bloqueada pela Regra dos 3 Strikes deste Nêmesis.")
                    jogador.conquistas.processar_evento("fuga_bloqueada_nemesis")
                    continue
                if SistemaCombate.tentar_fuga(jogador):
                    return "fuga"
                return "falha_fuga"

            print("Opção inválida.")

    def turno_inimigo(self, inimigo, jogador):
        if inimigo.esta_vivo() and jogador.esta_vivo():
            print(f"\nVez de {inimigo.nome}.")
            if not SistemaCombate.tentar_esquiva(jogador):
                SistemaCombate.atacar(inimigo, jogador)

    def batalha(self, jogador, inimigo):
        # Loop principal da luta: alterna turno do jogador e turno do inimigo.
        tipo_encontro = "👑 Chefão" if isinstance(inimigo, Chefao) else "👹 Inimigo"
        cor_titulo = InterfaceRPG.VERMELHO if isinstance(inimigo, Chefao) else InterfaceRPG.AMARELO
        print(
            InterfaceRPG.titulo(
                f"{tipo_encontro}: {inimigo.nome}",
                "Prepare sua ação. O próximo erro custa caro.",
                cor=cor_titulo,
                icone=InterfaceRPG.ICONES["chefe"] if isinstance(inimigo, Chefao) else InterfaceRPG.ICONES["batalha"],
            )
        )
        inimigo.mostrar_status()
        jogador.iniciar_batalha()
        self.ultimo_inimigo_fugido = None

        while jogador.esta_vivo() and inimigo.esta_vivo():
            if self.turno_jogador(jogador, inimigo) == "fuga":
                print(f"\n{jogador.nome} fugiu da batalha.")
                self.ultimo_inimigo_fugido = inimigo.nome
                return "fugiu"

            if inimigo.esta_vivo():
                self.turno_inimigo(inimigo, jogador)

        if jogador.esta_vivo():
            print(f"\n{jogador.nome} derrotou {inimigo.nome}.")
            jogador.progressao.ganhar_xp(inimigo.xp)
            jogador.progressao.ganhar_ouro(inimigo)
            if not jogador.tomou_dano_na_batalha:
                jogador.conquistas.processar_evento("vitoria_perfeita", eh_chefao=isinstance(inimigo, Chefao))
            else:
                jogador.conquistas.processar_evento("quebrou_perfeita")
            self.tentar_dominar_alma(jogador, inimigo)
            if not jogador.esta_vivo():
                jogador.conquistas.processar_evento("quebrou_perfeita")
                print("\nVocê sucumbiu ao choque espiritual após a vitória.")
                return "derrota"
            return "venceu"

        jogador.conquistas.processar_evento("quebrou_perfeita")
        print("\nGame Over.")
        return "derrota"

    def menu_pos_batalha(self, jogador):
        while True:
            print(
                InterfaceRPG.menu(
                    "🗺️ Entre Batalhas",
                    [
                        ("1", "Enfrentar novo inimigo"),
                        ("2", "Descansar"),
                        ("3", "Ver status"),
                        ("4", "Ver conquistas"),
                        ("5", "Mercador Sombrio"),
                        ("6", "Encerrar aventura"),
                        ("7", "Ruptura da Maldição"),
                    ],
                    rodape=f"Nível {jogador.nivel} | Ouro {jogador.progressao.ouro} | Almas {jogador.progressao.almas}",
                    cor=InterfaceRPG.AZUL,
                )
            )
            entrada = input("Escolha uma opção: ").strip()

            if entrada == "1":
                return True
            if entrada == "2":
                if jogador.progressao.descansar():
                    self.descansos_na_run += 1
            elif entrada == "3":
                jogador.mostrar_status()
            elif entrada == "4":
                jogador.exibir_conquistas()
            elif entrada == "5":
                self.menu_mercador_sombrio(jogador)
            elif entrada == "6":
                if jogador.progressao.maldicao_ultimo_nivel_ativa and jogador.nivel < 101:
                    print("A Maldição do Último Nível impede encerrar antes do nível 101.")
                    print("Você pode continuar, chegar ao nível 101 ou tentar a ruptura da maldição.")
                    jogador.conquistas.processar_evento("encerramento_bloqueado_maldicao")
                    continue
                if jogador.progressao.maldicao_ultimo_nivel_ativa and jogador.nivel >= 101:
                    self.executar_julgamento_reflexo_final(jogador)
                    return False
                self.definir_epilogo_encerramento(jogador)
                return False
            elif entrada == "7":
                jogador.progressao.tentar_ruptura_maldicao()
            else:
                print("Opção inválida.")

    def executar(self):
        # Orquestra a aventura inteira: combate, progresso e encerramento.
        print(
            InterfaceRPG.titulo(
                "Crônicas do Abismo",
                "ASCII, cor e sangue suficiente para uma run memorável",
                cor=InterfaceRPG.CIANO,
                icone="🐉",
            )
        )
        montanha = [
            "        /\\",
            "   /\\  /  \\",
            "  /  \\/ /\\ \\",
            " / /\\  /  \\ \\",
            "/_/  \\/_/\\_\\",
        ]
        logo = [
            "__        _______ _     _          ____    _    __  __ _____ ____ ",
            "\\ \\      / /_ _| | |   | |        / ___|  / \\  |  \\/  | ____/ ___|",
            " \\ \\ /\\ / / | || | |   | |       | |  _  / _ \\ | |\\/| |  _| \\___ \\",
            "  \\ V  V /  | || | |___| |___    | |_| |/ ___ \\| |  | | |___ ___) |",
            "   \\_/\\_/  |___|_|_____|_____|    \\____/_/   \\_\\_|  |_|_____|____/ ",
        ]
        for linha_montanha, linha_logo in zip(montanha, logo):
            print(
                InterfaceRPG.cor(linha_montanha.ljust(24), InterfaceRPG.CIANO, negrito=True)
                + "  "
                + InterfaceRPG.cor(linha_logo, InterfaceRPG.CIANO, negrito=True)
            )
        self.jogador = self.escolher_personagem()
        self.aplicar_heranca_inicial(self.jogador)
        self.iniciar_nova_run()

        print(f"\nSeu personagem {self.jogador.nome} foi criado com sucesso.")
        self.jogador.mostrar_status()

        aposentou = False
        while True:
            while self.jogador.esta_vivo():
                chance_chefao = 0.20
                if self.vitorias_na_run >= 20 and self.jogador.nivel >= 3 and random.random() < chance_chefao:
                    print(InterfaceRPG.cor(f"\n{InterfaceRPG.ICONES['aviso']} O clima fica tenso... um chefão se aproxima.", InterfaceRPG.VERMELHO, negrito=True))
                    nivel_base = self.jogador.nivel + self.bonus_nivel_chefes
                    inimigo = Chefao.gerar_chefao(nivel_base)
                    eh_chefao = True
                else:
                    nivel_base = self.jogador.nivel + self.bonus_nivel_monstros
                    inimigo = Monstro.gerar_monstro(nivel_base)
                    eh_chefao = False

                self.aplicar_nemesis(inimigo)
                resultado = self.batalha(self.jogador, inimigo)

                if resultado == "venceu":
                    self.inimigos_derrotados += 1
                    self.vitorias_na_run += 1
                    self.jogador.conquistas.processar_evento(
                        "batalha_vencida",
                        eh_chefao=eh_chefao,
                        nome_inimigo=inimigo.nome,
                    )
                    self.verificar_gatilho_juramento_sem_descanso(self.jogador)
                    if self.vitorias_na_run % 10 == 0:
                        self.ativar_rotacao_contratos()
                        self.exibir_contratos_sombrios(self.jogador)
                elif resultado == "fugiu":
                    self.fugas_na_run += 1
                    self.registrar_fuga_nemesis(self.ultimo_inimigo_fugido)
                elif resultado == "derrota":
                    self.jogador.conquistas.processar_evento(
                        "morte_heroi",
                        contratos_na_run=self.contratos_sombrios_na_run,
                        pactos_na_run=self.compras_sombrias_na_run,
                    )
                    break

                if not self.jogador.esta_vivo():
                    break
                if not self.menu_pos_batalha(self.jogador):
                    self.registrar_evento_fim_run(morreu=False)
                    aposentou = True
                    break

            if aposentou:
                break

            if not self.jogador.esta_vivo():
                self.registrar_heranca_pos_morte(self.jogador)
                self.registrar_evento_fim_run(morreu=True)
                escolha = input("\nDeseja que um herdeiro continue o legado? (S/N): ").strip().lower()
                if escolha != "s":
                    break

                self.jogador = self.escolher_personagem()
                self.aplicar_heranca_inicial(self.jogador)
                self.iniciar_nova_run()
                print(f"\nO herdeiro {self.jogador.nome} inicia uma nova run.")
                self.jogador.mostrar_status()
                continue

            break

        print(InterfaceRPG.titulo("Fim da Aventura", "Toda run deixa uma cicatriz diferente", cor=InterfaceRPG.AMARELO, icone="🌙"))
        if self.final_reflexo_tipo == "integro":
            print("FINAL: JULGAMENTO DA ORIGEM.")
            print("Você venceu o mundo, mas não venceu a pergunta final.")
        elif self.final_reflexo_tipo == "corrompido":
            print("FINAL: INVENTÁRIO DO VAZIO.")
            print("Você conquistou poder, mas hipotecou o próprio sentido.")
        elif self.epilogo_encerramento:
            print("FINAL: EPÍLOGO DE APOSENTADORIA.")
            print(self.epilogo_encerramento)
        elif self.jogador.esta_vivo():
            print("Você decidiu se aposentar vivo e cheio de glórias.")
        else:
            print("Você lutou bravamente, mas sucumbiu aos perigos do mundo.")

        print(f"Inimigos derrotados no total: {self.inimigos_derrotados}")
        self.jogador.mostrar_status()
        self.jogador.exibir_conquistas()


def jogar():
    MotorJogo().executar()


if __name__ == "__main__":
    jogar()
