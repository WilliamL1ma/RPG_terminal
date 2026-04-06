from .achievements import SistemaConquistas
from .entities import Arqueiro, Chefao, Guerreiro, Mago, Monstro
from .interface import InterfaceRPG
from .savegame import load_game, save_exists, save_game
from .state import EstadoRun


class SessaoJogoMixin:
    def criar_conquistas(self):
        return SistemaConquistas(
            catalogo_monstros=Monstro.TIPOS.keys(),
            catalogo_chefes=Chefao.TIPOS.keys(),
        )

    def iniciar_nova_run(self):
        self.estado_run = EstadoRun()

    def copiar_estado(self, outro_motor):
        self.estado_run = outro_motor.estado_run
        self.jogador = outro_motor.jogador
        self.inimigos_derrotados = outro_motor.inimigos_derrotados
        self.nemesis_strikes = outro_motor.nemesis_strikes
        self.maldicao_linhagem_ativa = outro_motor.maldicao_linhagem_ativa
        self.final_reflexo_tipo = outro_motor.final_reflexo_tipo
        self.epilogo_encerramento = outro_motor.epilogo_encerramento
        self.heranca_ouro = outro_motor.heranca_ouro
        self.heranca_almas = outro_motor.heranca_almas

    def salvar_progresso(self, silencioso=False):
        if not self.jogador:
            return False

        caminho = save_game(self)
        if not silencioso:
            print(f"\nProgresso salvo em: {caminho}")
        return True

    def tentar_carregar_save(self):
        if not save_exists():
            return False

        while True:
            print(
                InterfaceRPG.menu(
                    "Save Encontrado",
                    [
                        ("1", "Continuar do save"),
                        ("2", "Novo jogo"),
                    ],
                    rodape=(
                        "O save atual fica em data/savegame.json e sera sobrescrito "
                        "quando um novo progresso for salvo."
                    ),
                    cor=InterfaceRPG.MAGENTA,
                )
            )
            escolha = input("Escolha uma opcao: ").strip()

            if escolha == "2":
                return False

            if escolha == "1":
                try:
                    motor_carregado = load_game()
                except Exception as erro:
                    print(f"\nNao foi possivel carregar o save: {erro}")
                    return False

                if not motor_carregado or not motor_carregado.jogador:
                    print("\nO save encontrado esta vazio ou invalido.")
                    return False

                self.copiar_estado(motor_carregado)
                print(
                    f"\nSave carregado: {self.jogador.nome} "
                    f"(Nivel {self.jogador.nivel})."
                )
                return True

            print("Opcao invalida.")

    def escolher_personagem(self):
        print(
            InterfaceRPG.titulo(
                "Criacao de Heroi",
                "Escolha um nome, uma classe e aceite o caos",
                cor=InterfaceRPG.CIANO,
                icone="🧙",
            )
        )
        nome = input("Digite o nome do seu personagem: ").strip().title()

        while not nome:
            nome = input("Digite um nome valido: ").strip().title()

        conquistas = self.criar_conquistas()

        while True:
            print(
                InterfaceRPG.menu(
                    "🧬 Classes",
                    [
                        ("1", "Guerreiro | brutal, resistente, fisico"),
                        ("2", "Mago | explosivo, mana alta, arcano"),
                        ("3", "Arqueiro | agil, preciso, tecnico"),
                    ],
                    cor=InterfaceRPG.CIANO,
                )
            )
            entrada = input("Escolha o numero da classe: ").strip()

            if entrada == "1":
                return Guerreiro(nome, conquistas)
            if entrada == "2":
                return Mago(nome, conquistas)
            if entrada == "3":
                return Arqueiro(nome, conquistas)

            print("Opcao invalida. Tente novamente.")
