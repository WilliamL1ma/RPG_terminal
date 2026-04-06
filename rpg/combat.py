import random

from .interface import InterfaceRPG


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
        classe = atacante.__class__.__name__
        if classe in {"Guerreiro", "Mago", "Arqueiro"}:
            return classe
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

