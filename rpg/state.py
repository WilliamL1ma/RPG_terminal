from dataclasses import dataclass, field, fields


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
