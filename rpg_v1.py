# NOME COMPLETO: William Gonçalves Cruz Ramos de Lima
# R.E: 824143532
# Trabalho de RPG em Python para terminal.

"""Entry point compatível e camada de reexportação do jogo."""

from rpg.achievements import EventosConquista, ExibidorConquistas, SistemaConquistas
from rpg.combat import NarradorCombate, SistemaCombate
from rpg.engine import MotorJogo, jogar
from rpg.entities import Arqueiro, Chefao, Guerreiro, Inimigo, Mago, Monstro, Personagem
from rpg.interface import InterfaceRPG
from rpg.progression import SistemaProgressao
from rpg.state import (
    ESTADO_CONQUISTAS_ATRIBUTOS,
    ESTADO_RUN_ATRIBUTOS,
    EstadoConquistas,
    EstadoRun,
)

__all__ = [
    "Arqueiro",
    "Chefao",
    "ESTADO_CONQUISTAS_ATRIBUTOS",
    "ESTADO_RUN_ATRIBUTOS",
    "EstadoConquistas",
    "EstadoRun",
    "EventosConquista",
    "ExibidorConquistas",
    "Guerreiro",
    "Inimigo",
    "InterfaceRPG",
    "Mago",
    "Monstro",
    "MotorJogo",
    "NarradorCombate",
    "Personagem",
    "SistemaCombate",
    "SistemaConquistas",
    "SistemaProgressao",
    "jogar",
]


if __name__ == "__main__":
    jogar()
