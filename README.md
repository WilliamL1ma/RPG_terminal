## RPG de Terminal em Python

Projeto de RPG jogado pelo terminal, desenvolvido em Python. O jogador cria um personagem, escolhe uma classe e enfrenta monstros e chefes em batalhas por turnos.

## Funcionalidades

- Escolha entre 3 classes: `Guerreiro`, `Mago` e `Arqueiro`
- Sistema de batalha por turnos
- Ataque padrão, habilidade especial e habilidades de ascensão
- Sistema de vida, defesa, mana e stamina
- Ganho de experiência e evolução de nível
- Sistema de conquistas
- Encontros com monstros comuns e chefes
- Save e carregamento em JSON
- Menu pós-batalha com descanso, conquistas, contratos, save e encerramento de aventura

## Estrutura do projeto

```text
.
|-- rpg/
|   |-- __init__.py
|   |-- achievements.py
|   |-- battle_flow.py
|   |-- campaign.py
|   |-- combat.py
|   |-- engine.py
|   |-- entities.py
|   |-- interface.py
|   |-- market.py
|   |-- progression.py
|   |-- savegame.py
|   |-- session.py
|   `-- state.py
|-- rpg_v1.py
|-- README.md
`-- requirements.txt

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

Se preferir usar o pacote diretamente:

```bash
python -m rpg
```

O save é gravado em `data/savegame.json`.

## Como jogar

1. Informe o nome do personagem.
2. Escolha uma classe.
3. Durante a batalha, selecione uma ação:
   - `1` para ataque padrão
   - `2` para usar a habilidade especial
   - `3` para usar habilidade de ascensão
   - `4` para ver o status
   - `5` para tentar fugir
4. Entre batalhas, use o menu para continuar, descansar, ver conquistas, visitar o mercador sombrio, salvar e sair ou encerrar a aventura.

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
- A cada 10 vitórias, a rotação de contratos sombrios pode ser ativada.

## Autor

- William Gonçalves Cruz Ramos de Lima
