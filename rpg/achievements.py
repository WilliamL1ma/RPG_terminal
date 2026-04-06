from .interface import InterfaceRPG
from .state import ESTADO_CONQUISTAS_ATRIBUTOS, EstadoConquistas


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
