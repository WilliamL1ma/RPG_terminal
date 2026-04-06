import os
import shutil
import sys


class InterfaceRPG:
    """Utilitários visuais para dar identidade ao terminal sem mexer na lógica."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    VERMELHO = "\033[91m"
    VERDE = "\033[92m"
    AMARELO = "\033[93m"
    AZUL = "\033[94m"
    MAGENTA = "\033[95m"
    CIANO = "\033[96m"
    BRANCO = "\033[97m"

    ICONES = {
        "vida": "❤️",
        "defesa": "🛡️",
        "mana": "🔮",
        "stamina": "⚡",
        "ouro": "🪙",
        "almas": "👻",
        "nivel": "🏅",
        "xp": "📘",
        "critico": "💥",
        "conquista": "🏆",
        "chefe": "👑",
        "aviso": "⚠️",
        "menu": "🎮",
        "batalha": "⚔️",
        "fuga": "💨",
        "descanso": "🛏️",
        "vitoria": "🎉",
        "derrota": "☠️",
        "magia": "✨",
        "mercador": "🕯️",
        "maldicao": "🩸",
        "reflexo": "🪞",
        "classe": "🧬",
        "inimigo": "👹",
        "herdeiro": "🧭",
    }

    @classmethod
    def suporta_cor(cls):
        return sys.stdout.isatty() and os.getenv("NO_COLOR") is None

    @classmethod
    def cor(cls, texto, codigo, negrito=False):
        if not cls.suporta_cor():
            return texto
        prefixo = cls.BOLD if negrito else ""
        return f"{prefixo}{codigo}{texto}{cls.RESET}"

    @staticmethod
    def largura():
        return min(86, max(56, shutil.get_terminal_size((80, 24)).columns))

    @classmethod
    def separador(cls, char="="):
        return cls.cor(char * cls.largura(), cls.AZUL)

    @classmethod
    def titulo(cls, texto, subtitulo=None, cor=None, icone=">>"):
        cor = cor or cls.CIANO
        largura = cls.largura()
        cabecalho = f" {icone} {texto.upper()} "
        topo = cls.cor("╔" + "═" * (largura - 2) + "╗", cor, negrito=True)
        meio = cls.cor(cabecalho.center(largura), cor, negrito=True)
        base = cls.cor("╚" + "═" * (largura - 2) + "╝", cor, negrito=True)
        blocos = [f"\n{topo}", meio]
        if subtitulo:
            blocos.append(cls.cor(subtitulo.center(largura), cls.BRANCO))
        blocos.append(base)
        return "\n".join(blocos)

    @classmethod
    def caixa(cls, titulo, linhas, cor=None):
        cor = cor or cls.AZUL
        largura = cls.largura()
        internas = [linha[: largura - 6] for linha in linhas]
        topo = cls.cor("┌" + "─" * (largura - 2) + "┐", cor)
        rodape = cls.cor("└" + "─" * (largura - 2) + "┘", cor)
        corpo = [cls.cor(f"│ {titulo[:largura - 6].ljust(largura - 4)}│", cor, negrito=True)]
        corpo.extend(
            cls.cor(f"│ {linha.ljust(largura - 4)}│", cls.BRANCO) for linha in internas
        )
        return "\n".join(["", topo, *corpo, rodape])

    @classmethod
    def menu(cls, titulo, opcoes, rodape=None, cor=None):
        linhas = [f"{indice}. {descricao}" for indice, descricao in opcoes]
        if rodape:
            linhas.append("")
            linhas.append(rodape)
        return cls.caixa(titulo, linhas, cor=cor or cls.MAGENTA)

    @classmethod
    def destaque(cls, texto, icone="✨", cor=None):
        return cls.cor(f"{icone} {texto}", cor or cls.BRANCO, negrito=True)

    @classmethod
    def barra(cls, atual, maximo, largura=18, cheia="#", vazia="-"):
        maximo = max(1, maximo)
        preenchida = int((atual / maximo) * largura)
        return "[" + cheia * preenchida + vazia * (largura - preenchida) + "]"

    @classmethod
    def status_personagem(cls, personagem):
        linhas = [
            f"{cls.ICONES['nivel']} {personagem.nivel} | {cls.ICONES['classe']} Classe: {personagem.forma_ascensao_atual}",
            (
                f"{cls.ICONES['vida']} {personagem.vida}/{personagem.vida_max} {cls.barra(personagem.vida, personagem.vida_max)} | "
                f"{cls.ICONES['defesa']} {personagem.defesa}/{personagem.defesa_max}"
            ),
            (
                f"{cls.ICONES['mana']} {personagem.mana}/{personagem.mana_max} {cls.barra(personagem.mana, max(1, personagem.mana_max))} | "
                f"{cls.ICONES['stamina']} {personagem.stamina}/{personagem.stamina_max}"
            ),
            (
                f"⚔️ ATAQ {personagem.ataque} | {cls.ICONES['xp']} {personagem.xp}/{personagem.proximo_nivel} | "
                f"{cls.ICONES['ouro']} {personagem.ouro} | {cls.ICONES['almas']} {personagem.progressao.almas}"
            ),
            f"🌀 Esquiva bônus: +{int(personagem.bonus_esquiva * 100)}%",
        ]
        if personagem.progressao.maldicao_ultimo_nivel_ativa and personagem.nivel < 101:
            linhas.append(f"{cls.ICONES['maldicao']} Maldição do Último Nível: ativa até o nível 101.")
        return cls.caixa(f"Status de {personagem.nome.upper()}", linhas, cor=cls.CIANO)

    @classmethod
    def status_inimigo(cls, inimigo):
        linhas = [
            f"{cls.ICONES['nivel']} {inimigo.nivel}",
            f"{cls.ICONES['vida']} {inimigo.vida}/{inimigo.vida_max} {cls.barra(inimigo.vida, inimigo.vida_max)}",
            f"{cls.ICONES['defesa']} {inimigo.defesa}/{inimigo.defesa_max} | ⚔️ ATAQ {inimigo.ataque}",
        ]
        return cls.caixa(f"{cls.ICONES['inimigo']} Inimigo: {inimigo.nome.upper()}", linhas, cor=cls.VERMELHO)

