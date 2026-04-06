import random

from .interface import InterfaceRPG


class MercadoSombrioMixin:
    def menu_mercador_sombrio(self, jogador):
        if jogador.nivel < 50:
            print("\nO Mercador Sombrio so negocia com aventureiros de nivel 50 ou mais.")
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

            escolha_menu = input("Escolha uma opcao: ").strip()
            if escolha_menu == "3":
                return

            if escolha_menu == "2":
                self.exibir_contratos_sombrios(jogador)
                continue

            if escolha_menu != "1":
                print("Opcao invalida.")
                continue

            if self.compras_sombrias_na_run >= 2:
                print("\nLimite da run atingido: maximo de 2 compras sombrias.")
                continue

            print(
                InterfaceRPG.caixa(
                    "📜 Pactos Disponiveis",
                    [
                        *(
                            f"{chave}. {opcao['nome']} | Custo: {opcao['custo']} almas"
                            for chave, opcao in opcoes_pactos.items()
                        ),
                        "5. Cancelar",
                    ],
                    cor=InterfaceRPG.VERMELHO,
                )
            )

            escolha = input("Escolha um pacto: ").strip()
            if escolha == "5":
                continue
            if escolha not in opcoes_pactos:
                print("Opcao invalida.")
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
                f"Monstros +{self.bonus_nivel_monstros} niveis globais | "
                f"Chefes +{self.bonus_nivel_chefes} niveis globais."
            )

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

        if score_liquido >= 32:
            custo = int(custo * 1.80)
        elif score_liquido >= 24:
            custo = int(custo * 1.55)
        elif score_liquido >= 16:
            custo = int(custo * 1.30)

        return min(320, max(base, custo))

    def exibir_contratos_sombrios(self, jogador):
        if not self.rotacao_contratos_ativa:
            print("\nNenhuma rotacao de contratos disponivel agora.")
            return

        if self.contrato_comprado_no_ciclo:
            print("\nVoce ja fechou um contrato nesta rotacao.")
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
            print("Opcao invalida.")
            return

        indice = int(escolha) - 1
        if indice == len(self.contratos_rotacao):
            return
        if indice < 0 or indice >= len(self.contratos_rotacao):
            print("Opcao invalida.")
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
