import json
from dataclasses import asdict
from pathlib import Path

from .achievements import SistemaConquistas
from .entities import Arqueiro, Guerreiro, Mago
from .state import EstadoRun


SAVE_VERSION = 1
SAVE_FILE = Path(__file__).resolve().parent.parent / "data" / "savegame.json"
CLASSES_JOGADOR = {
    "Guerreiro": Guerreiro,
    "Mago": Mago,
    "Arqueiro": Arqueiro,
}
CONJUNTOS_CONQUISTAS = {
    "monstros_unicos_derrotados",
    "chefes_unicos_derrotados",
    "monstros_sem_descanso",
    "chefes_sem_descanso",
    "catalogo_monstros",
    "catalogo_chefes",
}


def save_exists(path=SAVE_FILE):
    return Path(path).exists()


def delete_save(path=SAVE_FILE):
    caminho = Path(path)
    if caminho.exists():
        caminho.unlink()


def save_game(motor, path=SAVE_FILE):
    caminho = Path(path)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": SAVE_VERSION,
        "motor": _serialize_motor(motor),
    }
    caminho.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return caminho


def load_game(path=SAVE_FILE):
    caminho = Path(path)
    if not caminho.exists():
        return None

    payload = json.loads(caminho.read_text(encoding="utf-8"))
    if payload.get("version") != SAVE_VERSION:
        raise ValueError("Versao de save incompativel.")
    return _deserialize_motor(payload["motor"])


def _serialize_motor(motor):
    return {
        "jogador": _serialize_player(motor.jogador),
        "estado_run": _json_safe(asdict(motor.estado_run)),
        "inimigos_derrotados": motor.inimigos_derrotados,
        "nemesis_strikes": dict(motor.nemesis_strikes),
        "maldicao_linhagem_ativa": motor.maldicao_linhagem_ativa,
        "final_reflexo_tipo": motor.final_reflexo_tipo,
        "epilogo_encerramento": motor.epilogo_encerramento,
        "heranca_ouro": motor.heranca_ouro,
        "heranca_almas": motor.heranca_almas,
    }


def _deserialize_motor(data):
    from .engine import MotorJogo

    motor = MotorJogo()
    motor.jogador = _deserialize_player(data["jogador"])
    motor.estado_run = EstadoRun(**data.get("estado_run", {}))
    motor.inimigos_derrotados = data.get("inimigos_derrotados", 0)
    motor.nemesis_strikes = dict(data.get("nemesis_strikes", {}))
    motor.maldicao_linhagem_ativa = data.get("maldicao_linhagem_ativa", False)
    motor.final_reflexo_tipo = data.get("final_reflexo_tipo")
    motor.epilogo_encerramento = data.get("epilogo_encerramento")
    motor.heranca_ouro = data.get("heranca_ouro", 0)
    motor.heranca_almas = data.get("heranca_almas", 0)
    return motor


def _serialize_player(jogador):
    if jogador is None:
        return None

    progressao = jogador.progressao
    return {
        "classe": jogador.__class__.__name__,
        "nome": jogador.nome,
        "vida": jogador.vida,
        "vida_max": jogador.vida_max,
        "defesa": jogador.defesa,
        "defesa_max": jogador.defesa_max,
        "ataque": jogador.ataque,
        "mana": jogador.mana,
        "mana_max": jogador.mana_max,
        "stamina": jogador.stamina,
        "stamina_max": jogador.stamina_max,
        "atributos_base_classe": dict(jogador.atributos_base_classe),
        "tomou_dano_na_batalha": jogador.tomou_dano_na_batalha,
        "progressao": {
            "xp": progressao.xp,
            "nivel": progressao.nivel,
            "proximo_nivel": progressao.proximo_nivel,
            "ouro": progressao.ouro,
            "almas": progressao.almas,
            "almas_coletadas_run": progressao.almas_coletadas_run,
            "multiplicador_xp": progressao.multiplicador_xp,
            "multiplicador_ouro": progressao.multiplicador_ouro,
            "maldicao_ultimo_nivel_ativa": progressao.maldicao_ultimo_nivel_ativa,
            "ruptura_maldicao_realizada": progressao.ruptura_maldicao_realizada,
            "bonus_esquiva": progressao.bonus_esquiva,
            "usou_ascensao": progressao.usou_ascensao,
            "decisao_ascensao_tomada": progressao.decisao_ascensao_tomada,
            "recusou_ascensao": progressao.recusou_ascensao,
            "marcos_ascensao_aplicados": sorted(progressao.marcos_ascensao_aplicados),
            "forma_ascensao_atual": progressao.forma_ascensao_atual,
            "habilidades_ascensao": _json_safe(progressao.habilidades_ascensao),
        },
        "conquistas": _serialize_achievements(jogador.conquistas),
    }


def _deserialize_player(data):
    if not data:
        return None

    classe_nome = data["classe"]
    classe = CLASSES_JOGADOR.get(classe_nome)
    if classe is None:
        raise ValueError(f"Classe de save desconhecida: {classe_nome}")

    conquistas = _deserialize_achievements(data.get("conquistas", {}))
    jogador = classe(data["nome"], conquistas)

    for atributo in (
        "vida",
        "vida_max",
        "defesa",
        "defesa_max",
        "ataque",
        "mana",
        "mana_max",
        "stamina",
        "stamina_max",
    ):
        setattr(jogador, atributo, data[atributo])

    jogador.atributos_base_classe = dict(
        data.get("atributos_base_classe", jogador.atributos_base_classe)
    )
    jogador.tomou_dano_na_batalha = data.get("tomou_dano_na_batalha", False)

    _restore_progression(jogador, data.get("progressao", {}))
    return jogador


def _serialize_achievements(conquistas):
    return _json_safe(asdict(conquistas.estado))


def _deserialize_achievements(data):
    catalogo_monstros = data.get("catalogo_monstros", [])
    catalogo_chefes = data.get("catalogo_chefes", [])
    conquistas = SistemaConquistas(
        catalogo_monstros=catalogo_monstros,
        catalogo_chefes=catalogo_chefes,
    )

    for campo, valor in data.items():
        if campo in CONJUNTOS_CONQUISTAS:
            setattr(conquistas.estado, campo, set(valor))
        else:
            setattr(conquistas.estado, campo, valor)
    return conquistas


def _restore_progression(jogador, data):
    progressao = jogador.progressao
    for atributo in (
        "xp",
        "nivel",
        "proximo_nivel",
        "ouro",
        "almas",
        "almas_coletadas_run",
        "multiplicador_xp",
        "multiplicador_ouro",
        "maldicao_ultimo_nivel_ativa",
        "ruptura_maldicao_realizada",
        "bonus_esquiva",
        "usou_ascensao",
        "decisao_ascensao_tomada",
        "recusou_ascensao",
        "forma_ascensao_atual",
    ):
        if atributo in data:
            setattr(progressao, atributo, data[atributo])

    progressao.marcos_ascensao_aplicados = set(
        data.get("marcos_ascensao_aplicados", [])
    )
    progressao.habilidades_ascensao = data.get("habilidades_ascensao", [])


def _json_safe(value):
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, set):
        return sorted(_json_safe(item) for item in value)
    return value
