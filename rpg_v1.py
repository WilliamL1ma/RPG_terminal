# NOME COMPLETO: William Gonçalves Cruz Ramos de Lima
# R.E: 824143532
# Trabalho de RPG em Python para terminal.

import random


class SistemaConquistas:
    """Controla as conquistas desbloqueadas durante a aventura."""

    def __init__(self):
        self.desbloqueadas = []

    def desbloquear(self, nome_conquista: str):
        """Desbloqueia uma conquista se ela ainda não tiver sido obtida."""
        if nome_conquista not in self.desbloqueadas:
            self.desbloqueadas.append(nome_conquista)
            print(f"\n🏆 CONQUISTA DESBLOQUEADA: {nome_conquista}!\n")

    def checar_evento(self, evento: str, jogador=None, inimigo=None):
        """Verifica eventos importantes do jogo para liberar conquistas."""
        if evento == 'primeira_vitoria':
            self.desbloquear('Primeiro Sangue')

        elif evento == 'fugiu':
            self.desbloquear('Covardia Estratégica')

        elif evento == 'critico':
            self.desbloquear('Golpe de Mestre')

        elif evento == 'chefao_derrotado':
            self.desbloquear('Caçador de Chefões')

        elif evento == 'nivel_5' and jogador is not None and jogador.nivel >= 5:
            self.desbloquear('Herói Experiente')

        elif evento == 'sem_defesa' and jogador is not None and jogador.defesa == 0:
            self.desbloquear('Peito Aberto')

    def exibir(self):
        """Mostra todas as conquistas do jogador."""
        print('\n=== CONQUISTAS ===')
        if not self.desbloqueadas:
            print('Nenhuma conquista desbloqueada ainda.')
        else:
            for indice, conquista in enumerate(self.desbloqueadas, start=1):
                print(f'{indice}. {conquista}')


class Personagem:
    """Classe base dos personagens do jogo."""

    def __init__(
        self,
        nome: str = 'Steve',
        vida: int = 20,
        defesa: int = 5,
        ataque: int = 5,
        mana: int = 20,
        stamina: int = 30,
        xp: int = 0,
        nivel: int = 0,
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
        self.xp = xp
        self.nivel = nivel
        self.proximo_nivel = 100
        self.conquistas = SistemaConquistas()

    def esta_vivo(self):
        """Retorna True se o personagem ainda estiver vivo."""
        return self.vida > 0

    def receber_dano(self, dano):
        """Aplica dano primeiro na defesa e depois na vida."""
        dano_original = dano

        if self.defesa > 0:
            if dano <= self.defesa:
                self.defesa -= dano
                print(f'{self.nome} bloqueou o ataque! Defesa restante: {self.defesa}')
                dano = 0
            else:
                dano -= self.defesa
                print(f'{self.nome} perdeu toda a defesa!')
                self.defesa = 0

        self.vida -= dano
        if self.vida < 0:
            self.vida = 0

        if dano > 0:
            print(f'{self.nome} recebeu {dano} de dano!')
            print(f'Vida atual: {self.vida}/{self.vida_max}')
        elif dano_original > 0:
            print(f'{self.nome} não perdeu vida neste ataque.')

    def atacar(self, alvo):
        """Realiza um ataque comum com chance de golpe crítico."""
        dano = self.ataque
        critico = False

        if random.random() < 0.20:
            dano = int(dano * 1.8)
            critico = True
            print(f'💥 GOLPE CRÍTICO! {self.nome} causará {dano} de dano!')
            self.conquistas.checar_evento('critico')

        print(f'{self.nome} atacou {alvo.nome}!')
        alvo.receber_dano(dano)
        return critico

    def esquivar(self):
        """Permite ao jogador tentar se esquivar do ataque inimigo."""
        escolha = input('Deseja tentar esquivar do ataque? (S/N): ').strip().lower()

        if escolha == 's':
            if self.stamina >= 5:
                chance_esquiva = min(0.15 + (self.nivel * 0.03), 0.60)
                if random.random() < chance_esquiva:
                    self.stamina -= 5
                    print(f'{self.nome} esquivou do ataque!')
                    print(f'Stamina: {self.stamina}/{self.stamina_max}')
                    return True

                self.stamina = max(0, self.stamina - 10)
                print(f'{self.nome} tentou esquivar, mas falhou!')
                print(f'Stamina: {self.stamina}/{self.stamina_max}')
            else:
                print('Sem stamina suficiente para esquivar!')

        return False

    def fugir(self):
        """Permite ao jogador tentar fugir da batalha."""
        escolha = input('Deseja fugir? (S/N): ').strip().lower()

        if escolha == 's':
            if random.random() > 0.5:
                print(f'{self.nome} conseguiu fugir com sucesso!')
                print('Foi por pouco... você escapou quase sem forças!')
                self.vida = max(1, self.vida)
                self.defesa = max(0, self.defesa)
                self.mana = max(1, self.mana)
                self.stamina = max(1, self.stamina)
                self.conquistas.checar_evento('fugiu')
                return True

            print(f'{self.nome} tentou fugir, mas falhou!')
            print('Você tropeçou e ficou vulnerável ao inimigo!')
            self.receber_dano(10)

        return False

    def subir_nivel(self):
        """Aumenta os atributos do personagem ao subir de nível."""
        self.nivel += 1
        self.vida_max += 20
        self.defesa_max += 5
        self.ataque += 5
        self.mana_max += 5
        self.stamina_max += 5
        self.proximo_nivel += 20

        self.vida = self.vida_max
        self.defesa = self.defesa_max
        self.mana = self.mana_max
        self.stamina = self.stamina_max

        print('\n=== LEVEL UP! ===')
        print(f'{self.nome} subiu para o nível {self.nivel}!')
        print(f'Vida máxima: {self.vida_max}')
        print(f'Defesa máxima: {self.defesa_max}')
        print(f'Mana máxima: {self.mana_max}')
        print(f'Stamina máxima: {self.stamina_max}')
        print(f'Ataque: {self.ataque}')
        print(f'Próximo nível: {self.proximo_nivel} XP')
        print('Todos os atributos foram restaurados!\n')

        self.conquistas.checar_evento('nivel_5', jogador=self)

    def ganhar_xp(self, quantidade):
        """Adiciona XP e sobe de nível quando necessário."""
        self.xp += quantidade
        print(f'{self.nome} ganhou {quantidade} XP! ({self.xp}/{self.proximo_nivel})')

        while self.xp >= self.proximo_nivel:
            self.xp -= self.proximo_nivel
            self.subir_nivel()

    def descansar(self):
        """Recupera parte dos atributos do jogador."""
        curar_vida = 30
        curar_defesa = 10
        curar_mana = 10
        curar_stamina = 10

        vida_antes = self.vida
        defesa_antes = self.defesa
        mana_antes = self.mana
        stamina_antes = self.stamina

        self.vida = min(self.vida + curar_vida, self.vida_max)
        self.defesa = min(self.defesa + curar_defesa, self.defesa_max)
        self.mana = min(self.mana + curar_mana, self.mana_max)
        self.stamina = min(self.stamina + curar_stamina, self.stamina_max)

        print(f'\n{self.nome} descansou!')
        print(f'Vida: {vida_antes} -> {self.vida}/{self.vida_max}')
        print(f'Defesa: {defesa_antes} -> {self.defesa}/{self.defesa_max}')
        print(f'Mana: {mana_antes} -> {self.mana}/{self.mana_max}')
        print(f'Stamina: {stamina_antes} -> {self.stamina}/{self.stamina_max}')

    def mostrar_status(self):
        """Exibe os atributos atuais do personagem."""
        print(f'\n=== STATUS DE {self.nome.upper()} ===')
        print(f'Nível: {self.nivel}')
        print(f'Vida: {self.vida}/{self.vida_max}')
        print(f'Defesa: {self.defesa}/{self.defesa_max}')
        print(f'Ataque: {self.ataque}')
        print(f'Mana: {self.mana}/{self.mana_max}')
        print(f'Stamina: {self.stamina}/{self.stamina_max}')
        print(f'XP: {self.xp}/{self.proximo_nivel}')

    def exibir_conquistas(self):
        """Mostra as conquistas do personagem."""
        self.conquistas.exibir()


class Guerreiro(Personagem):
    """Classe de guerreiro, com mais vida e defesa."""

    def __init__(self, nome):
        super().__init__(nome, vida=25, ataque=10, defesa=15, mana=10, stamina=35)

    def habilidade_especial(self, alvo):
        """Golpe forte que consome stamina."""
        if self.stamina >= 10:
            dano = int(self.ataque * 2.5)
            print(f'{self.nome} usou Golpe Duplo!')
            alvo.receber_dano(dano)
            self.stamina -= 10
            print(f'Stamina: {self.stamina}/{self.stamina_max}')
        else:
            print('Stamina insuficiente!')


class Mago(Personagem):
    """Classe de mago, com foco em magia."""

    def __init__(self, nome):
        super().__init__(nome, vida=18, ataque=20, defesa=10, mana=35, stamina=20)

    def habilidade_especial(self, alvo):
        """Magia ofensiva que consome mana."""
        if self.mana >= 10:
            dano = self.ataque + 10
            print(f'{self.nome} lançou Bola de Fogo!')
            alvo.receber_dano(dano)
            self.mana -= 10
            print(f'Mana: {self.mana}/{self.mana_max}')
        else:
            print('Mana insuficiente!')


class Arqueiro(Personagem):
    """Classe de arqueiro, com alto ataque e menor defesa."""

    def __init__(self, nome):
        super().__init__(nome, vida=15, ataque=30, defesa=5, mana=10, stamina=35)

    def habilidade_especial(self, alvo):
        """Ataque preciso que consome stamina."""
        if self.stamina >= 10:
            dano = self.ataque + 5
            print(f'{self.nome} usou Flecha Precisa!')
            alvo.receber_dano(dano)
            self.stamina -= 10
            print(f'Stamina: {self.stamina}/{self.stamina_max}')
        else:
            print('Stamina insuficiente!')


class Monstro(Personagem):
    """Classe que gera inimigos comuns do jogo."""

    TIPOS = {
        'Orc': {'vida': 60, 'ataque': 10, 'defesa': 15, 'xp': 40},
        'Goblin': {'vida': 35, 'ataque': 10, 'defesa': 0, 'xp': 20},
        'Lobo': {'vida': 40, 'ataque': 20, 'defesa': 0, 'xp': 30},
        'Dragão Jovem': {'vida': 100, 'ataque': 40, 'defesa': 50, 'xp': 250},
    }

    def __init__(self, nome, vida, ataque, defesa, xp, nivel=1):
        super().__init__(nome=nome, vida=vida, defesa=defesa, ataque=ataque, xp=xp, nivel=nivel)

    @classmethod
    def gerar_monstro(cls):
        """Gera um monstro aleatório."""
        nome = random.choice(list(cls.TIPOS.keys()))
        atributos = cls.TIPOS[nome]
        return cls(
            nome,
            atributos['vida'],
            atributos['ataque'],
            atributos['defesa'],
            atributos['xp'],
        )


class Chefao(Personagem):
    """Classe que gera chefões do jogo."""

    TIPOS = {
        'Grommash, o Destruidor': {'vida': 120, 'ataque': 30, 'defesa': 30, 'xp': 100},
        'Gribbik, o Pestilento': {'vida': 70, 'ataque': 20, 'defesa': 10, 'xp': 60},
        'Garra Cinzenta': {'vida': 90, 'ataque': 35, 'defesa': 15, 'xp': 80},
        'Zarathek, o Imortal': {'vida': 250, 'ataque': 60, 'defesa': 100, 'xp': 500},
    }

    def __init__(self, nome, vida, ataque, defesa, xp, nivel=1):
        super().__init__(nome=nome, vida=vida, defesa=defesa, ataque=ataque, xp=xp, nivel=nivel)

    @classmethod
    def gerar_chefao(cls):
        """Gera um chefão aleatório."""
        nome = random.choice(list(cls.TIPOS.keys()))
        atributos = cls.TIPOS[nome]
        return cls(
            nome,
            atributos['vida'],
            atributos['ataque'],
            atributos['defesa'],
            atributos['xp'],
        )


def escolher_personagem():
    """Cria o personagem do jogador de acordo com a classe escolhida."""
    nome = input('Digite o nome do seu personagem: ').strip().title()

    while not nome:
        nome = input('Digite um nome válido para seu personagem: ').strip().title()

    classes = '''
|-=-=-=-=-=-=-=-=-=-=-=-=|
| Escolha sua classe     |
|-=-=-=-=-=-=-=-=-=-=-=-=|
|   1 - Guerreiro        |
|   2 - Mago             |
|   3 - Arqueiro         |
|-=-=-=-=-=-=-=-=-=-=-=-=|
'''

    while True:
        print(classes)
        entrada = input('Escolha o número que representa sua classe: ').strip()

        if not entrada.isdigit():
            print('Opção inválida. Tente novamente.')
            continue

        escolha_j = int(entrada)

        if escolha_j == 1:
            return Guerreiro(nome)
        if escolha_j == 2:
            return Mago(nome)
        if escolha_j == 3:
            return Arqueiro(nome)

        print('Opção inválida. Tente novamente.')


def turno_jogador(jogador, inimigo):
    """Executa a ação escolhida pelo jogador."""
    opcoes = '''
======================
|      Sua vez       |
======================
| 1 - Ataque padrão  |
| 2 - Ataque especial|
| 3 - Ver status     |
| 4 - Fugir          |
======================
'''

    while True:
        print(opcoes)
        entrada = input('Escolha uma ação: ').strip()

        if not entrada.isdigit():
            print('Opção inválida. Tente novamente.')
            continue

        acao = int(entrada)

        if acao == 1:
            jogador.atacar(inimigo)
            return 'ataque'

        if acao == 2:
            jogador.habilidade_especial(inimigo)
            return 'especial'

        if acao == 3:
            jogador.mostrar_status()
            inimigo.mostrar_status()
            continue

        if acao == 4:
            if jogador.fugir():
                return 'fuga'
            return 'falha_fuga'

        print('Opção inválida. Tente novamente.')


def turno_inimigo(inimigo, jogador):
    """Executa o turno do inimigo."""
    if inimigo.esta_vivo() and jogador.esta_vivo():
        print(f'\nVez de {inimigo.nome}!')
        esquivou = jogador.esquivar()

        if not esquivou:
            inimigo.atacar(jogador)
            if jogador.defesa == 0:
                jogador.conquistas.checar_evento('sem_defesa', jogador=jogador)


def batalha(jogador, inimigo):
    """Controla o loop de batalha até alguém vencer ou o jogador fugir."""
    print(f'\n=== Um {inimigo.nome} apareceu! ===')
    inimigo.mostrar_status()

    while jogador.esta_vivo() and inimigo.esta_vivo():
        resultado_acao = turno_jogador(jogador, inimigo)

        if resultado_acao == 'fuga':
            print(f'\n{jogador.nome} fugiu da batalha!')
            return 'fugiu'

        if inimigo.esta_vivo() and jogador.esta_vivo():
            turno_inimigo(inimigo, jogador)

    if jogador.esta_vivo() and not inimigo.esta_vivo():
        print(f'\n{jogador.nome} derrotou {inimigo.nome}!')
        jogador.ganhar_xp(inimigo.xp)
        return 'venceu'

    print('\nGame Over!')
    return 'derrota'


def menu_pos_batalha(jogador):
    """Exibe o menu entre uma batalha e outra."""
    menu = '''
==============================
|            MENU            |
==============================
| 1 - Enfrentar novo inimigo |
| 2 - Descansar              |
| 3 - Ver status             |
| 4 - Ver conquistas         |
| 5 - Encerrar aventura      |
==============================
'''

    while True:
        print(menu)
        entrada = input('Escolha uma opção: ').strip()

        if not entrada.isdigit():
            print('Opção inválida. Tente novamente.')
            continue

        escolha = int(entrada)

        if escolha == 1:
            return True
        if escolha == 2:
            jogador.descansar()
        elif escolha == 3:
            jogador.mostrar_status()
        elif escolha == 4:
            jogador.exibir_conquistas()
        elif escolha == 5:
            return False
        else:
            print('Opção inválida. Tente novamente.')


def jogar():
    """Função principal que inicia e organiza toda a aventura."""
    print('=== BEM-VINDO AO RPG ===')
    jogador = escolher_personagem()
    monstros_derrotados = 0

    print(f'\nSeu personagem {jogador.nome} foi criado com sucesso!')
    jogador.mostrar_status()

    while jogador.esta_vivo():
        if monstros_derrotados > 0 and monstros_derrotados % 10 == 0:
            print('\n!!! O CLIMA FICA TENSO... UM CHEFÃO SE APROXIMA !!!')
            inimigo = Chefao.gerar_chefao()
            eh_chefao = True
        else:
            inimigo = Monstro.gerar_monstro()
            eh_chefao = False

        resultado = batalha(jogador, inimigo)

        if resultado == 'venceu':
            monstros_derrotados += 1

            if monstros_derrotados == 1:
                jogador.conquistas.checar_evento('primeira_vitoria')

            if eh_chefao:
                jogador.conquistas.checar_evento('chefao_derrotado')

        elif resultado == 'derrota':
            break

        continuar = menu_pos_batalha(jogador)
        if not continuar:
            break

    print('\n=== FIM DA AVENTURA ===')
    if jogador.esta_vivo():
        print('Você decidiu se aposentar vivo e cheio de glórias!')
    else:
        print('Você lutou bravamente, mas sucumbiu aos perigos do mundo.')

    print(f'Inimigos derrotados no total: {monstros_derrotados}')
    jogador.mostrar_status()
    jogador.exibir_conquistas()


if __name__ == '__main__':
    jogar()