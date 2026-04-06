## RPG de Terminal em Python

Projeto de RPG jogado pelo terminal, desenvolvido em Python. O jogador cria um personagem, escolhe uma classe e enfrenta monstros e chefes em batalhas por turnos.

## Funcionalidades

- Escolha entre 3 classes: `Guerreiro`, `Mago` e `Arqueiro`
- Sistema de batalha por turnos
- Ataque padrão e habilidade especial por classe
- Sistema de vida, defesa, mana e stamina
- Ganho de experiência e evolução de nível
- Sistema de conquistas
- Encontros com monstros comuns e chefões
- Menu pós-batalha para descansar, ver status e encerrar a aventura

## Estrutura do projeto

```text
.
|-- rpg_v1.py
|-- README.md
|-- requirements.txt
```

## Requisitos

- Python 3.10 ou superior

## Instalação

Como o projeto usa apenas módulos nativos do Python, não há dependências externas obrigatórias.

Ainda assim, se quiser seguir o fluxo padrão:

```bash
pip install -r requirements.txt
```

## Como executar

No terminal, dentro da pasta do projeto:

```bash
python rpg_v1.py
```

Se o seu sistema usar `python3`, execute:

```bash
python3 rpg_v1.py
```

## Como jogar

1. Informe o nome do personagem.
2. Escolha uma classe.
3. Durante a batalha, selecione uma ação:
   - `1` para ataque padrão
   - `2` para usar a habilidade especial
   - `3` para ver o status
   - `4` para tentar fugir
4. Entre batalhas, use o menu para continuar, descansar ou ver conquistas.

## Classes disponíveis

### Guerreiro

- Mais vida e defesa
- Habilidade especial: `Golpe Duplo`

### Mago

- Maior foco em dano mágico e mana
- Habilidade especial: `Bola de Fogo`

### Arqueiro

- Alto ataque e menor defesa
- Habilidade especial: `Flecha Precisa`

## Observações

- O jogo é totalmente interativo via terminal.
- Os inimigos são gerados aleatoriamente.
- A cada 10 inimigos derrotados, um chefão aparece.

## Autor

- William Gonçalves Cruz Ramos de Lima
