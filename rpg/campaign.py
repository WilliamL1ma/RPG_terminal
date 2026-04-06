import random

from .combat import SistemaCombate
from .entities import Chefao
from .interface import InterfaceRPG


class CampanhaMixin:
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
        if jogador.progressao.maldicao_ultimo_nivel_ativa:
            return
        if jogador.nivel >= 50 and self.descansos_na_run == 0:
            print(
                InterfaceRPG.destaque(
                    "Seu corpo venceu a fadiga, mas perdeu a liberdade.",
                    icone="🥀",
                    cor=InterfaceRPG.VERMELHO,
                )
            )
            print(
                InterfaceRPG.destaque(
                    "O Juramento do Sem Descanso desperta a Maldição do Último Nível.",
                    icone=InterfaceRPG.ICONES["maldicao"],
                    cor=InterfaceRPG.VERMELHO,
                )
            )
            jogador.progressao.aplicar_maldicao_ultimo_nivel()

    def definir_epilogo_encerramento(self, jogador):
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
        print(
            InterfaceRPG.titulo(
                "Reflexo Final",
                "O ultimo espelho nao devolve piedade",
                cor=InterfaceRPG.MAGENTA,
                icone=InterfaceRPG.ICONES["reflexo"],
            )
        )
        print("No limiar do fim, uma copia sua surge das sombras.")
        print('"Chegou até aqui... mas o que exatamente você se tornou?"')

        while True:
            print(
                InterfaceRPG.menu(
                    "Escolha do Reflexo",
                    [
                        ("1", "Eu faria tudo de novo"),
                        ("2", "Nao tenho certeza"),
                        ("3", "Eu me arrependo"),
                    ],
                    cor=InterfaceRPG.MAGENTA,
                )
            )
            resposta = input("Sua resposta: ").strip()
            if resposta in ("1", "2", "3"):
                break
            print("Opcao invalida.")

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

        print(f"\nNEMESIS: {inimigo.nome} retornou mais forte (+{bonus_nivel} niveis).")
        if strikes >= 3:
            print("Regra dos 3 Strikes ativa: fuga bloqueada contra este inimigo.")

    def registrar_fuga_nemesis(self, nome_inimigo):
        if not nome_inimigo:
            return

        atual = self.nemesis_strikes.get(nome_inimigo, 0)
        novo = min(3, atual + 1)
        self.nemesis_strikes[nome_inimigo] = novo

        print(f"NEMESIS atualizado para {nome_inimigo}: Strike {novo}/3.")
        if self.jogador:
            self.jogador.conquistas.processar_evento(
                "nemesis_strike",
                strike=novo,
                nome_inimigo=nome_inimigo,
            )

    def tentar_dominar_alma(self, jogador, inimigo):
        if jogador.nivel < 50:
            return

        if jogador.vida <= 1:
            print("Seu estado atual nao permite tentar dominar uma alma.")
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
                jogador.conquistas.processar_evento(
                    "dominio_alma_sucesso",
                    ganho=ganho,
                    eh_chefao=isinstance(inimigo, Chefao),
                )
            else:
                print("A alma resistiu ao dominio e se dispersou no vazio.")
            return

        dano = max(1, int(jogador.vida * 0.20))
        jogador.vida = max(0, jogador.vida - dano)
        print(f"Falha no dominio. Reacao espiritual: -{dano} de vida.")
        print(f"Vida atual: {jogador.vida}/{jogador.vida_max}")
        jogador.conquistas.processar_evento(
            "dominio_alma_falha",
            eh_chefao=isinstance(inimigo, Chefao),
        )
        if not jogador.esta_vivo():
            print("Seu corpo nao suportou o choque espiritual.")
