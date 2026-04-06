import random

from .combat import SistemaCombate
from .entities import Chefao, Monstro
from .interface import InterfaceRPG
from .savegame import SAVE_FILE, delete_save


class FluxoBatalhaMixin:
    def turno_jogador(self, jogador, inimigo):
        fuga_bloqueada = self.nemesis_strikes.get(inimigo.nome, 0) >= 3
        while True:
            print(
                InterfaceRPG.menu(
                    "🎮 Sua Vez",
                    [
                        ("1", "Ataque padrao"),
                        ("2", "Ataque especial"),
                        ("3", "Habilidade de ascensao"),
                        ("4", "Ver status"),
                        ("5", "Fugir"),
                    ],
                    rodape=f"Adversario: {inimigo.nome} | Fuga bloqueada: {'SIM' if fuga_bloqueada else 'NAO'}",
                    cor=InterfaceRPG.VERDE,
                )
            )
            entrada = input("Escolha uma acao: ").strip()

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
                    print("Fuga bloqueada pela Regra dos 3 Strikes deste Nemesis.")
                    jogador.conquistas.processar_evento("fuga_bloqueada_nemesis")
                    continue
                if SistemaCombate.tentar_fuga(jogador):
                    return "fuga"
                return "falha_fuga"

            print("Opcao invalida.")

    def turno_inimigo(self, inimigo, jogador):
        if inimigo.esta_vivo() and jogador.esta_vivo():
            print(f"\nVez de {inimigo.nome}.")
            if not SistemaCombate.tentar_esquiva(jogador):
                SistemaCombate.atacar(inimigo, jogador)

    def batalha(self, jogador, inimigo):
        tipo_encontro = "👑 Chefao" if isinstance(inimigo, Chefao) else "👹 Inimigo"
        cor_titulo = InterfaceRPG.VERMELHO if isinstance(inimigo, Chefao) else InterfaceRPG.AMARELO
        print(
            InterfaceRPG.titulo(
                f"{tipo_encontro}: {inimigo.nome}",
                "Prepare sua acao. O proximo erro custa caro.",
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
                jogador.conquistas.processar_evento(
                    "vitoria_perfeita",
                    eh_chefao=isinstance(inimigo, Chefao),
                )
            else:
                jogador.conquistas.processar_evento("quebrou_perfeita")
            self.tentar_dominar_alma(jogador, inimigo)
            if not jogador.esta_vivo():
                jogador.conquistas.processar_evento("quebrou_perfeita")
                print("\nVoce sucumbiu ao choque espiritual apos a vitoria.")
                return "derrota"
            return "venceu"

        jogador.conquistas.processar_evento("quebrou_perfeita")
        print("\nGame Over.")
        return "derrota"

    def menu_pos_batalha(self, jogador):
        while True:
            print(
                InterfaceRPG.menu(
                    "Entre Batalhas",
                    [
                        ("1", "Enfrentar novo inimigo"),
                        ("2", "Descansar"),
                        ("3", "Ver status"),
                        ("4", "Ver conquistas"),
                        ("5", "Mercador Sombrio"),
                        ("6", "Encerrar aventura"),
                        ("7", "Ruptura da Maldicao"),
                        ("8", "Salvar e sair"),
                    ],
                    rodape=f"Nivel {jogador.nivel} | Ouro {jogador.progressao.ouro} | Almas {jogador.progressao.almas}",
                    cor=InterfaceRPG.AZUL,
                )
            )
            entrada = input("Escolha uma opcao: ").strip()

            if entrada == "1":
                return "continuar"
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
                    print("A Maldicao do Ultimo Nivel impede encerrar antes do nivel 101.")
                    print("Voce pode continuar, chegar ao nivel 101 ou tentar a ruptura da maldicao.")
                    jogador.conquistas.processar_evento("encerramento_bloqueado_maldicao")
                    continue
                if jogador.progressao.maldicao_ultimo_nivel_ativa and jogador.nivel >= 101:
                    self.executar_julgamento_reflexo_final(jogador)
                    return "encerrar"
                self.definir_epilogo_encerramento(jogador)
                return "encerrar"
            elif entrada == "7":
                jogador.progressao.tentar_ruptura_maldicao()
            elif entrada == "8":
                self.salvar_progresso()
                return "salvar_sair"
            else:
                print("Opcao invalida.")

    def executar(self):
        print(
            InterfaceRPG.titulo(
                "Cronicas do Abismo",
                "ASCII, cor e sangue suficiente para uma run memoravel",
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

        save_carregado = self.tentar_carregar_save()
        if not save_carregado:
            self.jogador = self.escolher_personagem()
            self.aplicar_heranca_inicial(self.jogador)
            self.iniciar_nova_run()

            print(f"\nSeu personagem {self.jogador.nome} foi criado com sucesso.")
            self.jogador.mostrar_status()
            self.salvar_progresso(silencioso=True)
        else:
            self.jogador.mostrar_status()

        aposentou = False
        salvou_e_saiu = False
        while True:
            while self.jogador.esta_vivo():
                self.salvar_progresso(silencioso=True)
                chance_chefao = 0.20
                if self.vitorias_na_run >= 20 and self.jogador.nivel >= 3 and random.random() < chance_chefao:
                    print(
                        InterfaceRPG.cor(
                            f"\n{InterfaceRPG.ICONES['aviso']} O clima fica tenso... um chefao se aproxima.",
                            InterfaceRPG.VERMELHO,
                            negrito=True,
                        )
                    )
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

                resultado_menu = self.menu_pos_batalha(self.jogador)
                if resultado_menu == "encerrar":
                    self.registrar_evento_fim_run(morreu=False)
                    aposentou = True
                    break
                if resultado_menu == "salvar_sair":
                    salvou_e_saiu = True
                    break

            if aposentou:
                break
            if salvou_e_saiu:
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
                self.salvar_progresso(silencioso=True)
                continue

            break

        if salvou_e_saiu:
            print(
                InterfaceRPG.titulo(
                    "Progresso Salvo",
                    "Sua aventura foi registrada para continuar depois",
                    cor=InterfaceRPG.VERDE,
                    icone="💾",
                )
            )
            print(f"Arquivo de save: {SAVE_FILE}")
            return

        delete_save()
        print(
            InterfaceRPG.titulo(
                "Fim da Aventura",
                "Toda run deixa uma cicatriz diferente",
                cor=InterfaceRPG.AMARELO,
                icone="🌙",
            )
        )
        if self.final_reflexo_tipo == "integro":
            print("FINAL: JULGAMENTO DA ORIGEM.")
            print("Voce venceu o mundo, mas nao venceu a pergunta final.")
        elif self.final_reflexo_tipo == "corrompido":
            print("FINAL: INVENTARIO DO VAZIO.")
            print("Voce conquistou poder, mas hipotecou o proprio sentido.")
        elif self.epilogo_encerramento:
            print("FINAL: EPILOGO DE APOSENTADORIA.")
            print(self.epilogo_encerramento)
        elif self.jogador.esta_vivo():
            print("Voce decidiu se aposentar vivo e cheio de glorias.")
        else:
            print("Voce lutou bravamente, mas sucumbiu aos perigos do mundo.")

        print(f"Inimigos derrotados no total: {self.inimigos_derrotados}")
        self.jogador.mostrar_status()
        self.jogador.exibir_conquistas()
