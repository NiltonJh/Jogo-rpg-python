import random

# Lista para armazenar NPCs
lista_npcs = []

# Dicionário para armazenar informações do jogador
player = {
    "nome": "",
    "level": 1,
    "dano": 10,
    "hp": 100,
    "hp_max": 100,
    "exp": 0,
    "exp_max": 100,
    "inventario": [],
    "arma": None,
    "armadura": None
}

# Definição de itens
itens = {
    "armas": [
        {"nome": "Espada de Ferro", "dano": 5},
        {"nome": "Machado de Guerra", "dano": 10},
        {"nome": "Lança Longa", "dano": 7},
        {"nome": "Espada de Ouro", "dano": 15},
        {"nome": "Machado de Diamante", "dano": 20}
    ],
    "armaduras": [
        {"nome": "Armadura de Couro", "hp": 20},
        {"nome": "Armadura de Ferro", "hp": 40},
        {"nome": "Armadura de Aço", "hp": 60},
        {"nome": "Armadura de Ouro", "hp": 80},
        {"nome": "Armadura de Diamante", "hp": 100}
    ],
    "poções": [
        {"nome": "Poção de Cura", "cura": lambda hp_max: hp_max // 2}
    ]
}

# Função para criar um NPC
def criar_npc(level, tipo):
    if tipo == "Goblin":
        dano_base = random.randint(1, 5)
        hp_base = random.randint(10, 30)
    else:
        dano_base = random.randint(5, 15)
        hp_base = random.randint(20, 50)
    
    return {
        "nome": f"{tipo} #{level}" if level < 100 else "Rei do Inferno",
        "level": level,
        "dano": dano_base + level,
        "hp": hp_base + level * 2,
        "hp_max": hp_base + level * 2,
        "exp": level * 10,
        "drop": random.choice(itens["armas"] + itens["armaduras"] + itens["poções"])
    }

# Função para gerar NPCs
def gerar_npcs(n_npcs, tipo, level_range):
    for x in range(n_npcs):
        level = random.randint(level_range[0], level_range[1])
        npc = criar_npc(level, tipo)
        lista_npcs.append(npc)

# Função para exibir NPCs
def exibir_npcs():
    for npc in lista_npcs:
        exibir_npc(npc)

# Função para exibir um NPC
def exibir_npc(npc):
    print(
        f"Nome: {npc['nome']} // Level: {npc['level']} // Dano: {npc['dano']} // HP: {npc['hp']} // EXP: {npc['exp']} // Drop: {npc['drop']['nome']} (Atributos: {npc['drop']})"
    )

# Função para exibir informações do jogador
def exibir_player():
    print(
        f"Nome: {player['nome']} // Level: {player['level']} // Dano: {player['dano']} // HP: {player['hp']}/{player['hp_max']} // EXP: {player['exp']}/{player['exp_max']}"
    )
    if player["arma"]:
        print(f"Arma equipada: {player['arma']['nome']} (Dano: {player['arma']['dano']})")
    if player["armadura"]:
        print(f"Armadura equipada: {player['armadura']['nome']} (HP: {player['armadura']['hp']})")

# Função para resetar o HP do jogador
def reset_player():
    player["hp"] = player["hp_max"]

# Função para resetar o HP de um NPC
def reset_npc(npc):
    npc["hp"] = npc["hp_max"]

# Função para aumentar o nível do jogador
def level_up():
    player["level"] += 1
    player["exp"] = 0
    player["exp_max"] = player["exp_max"] * 2
    player["hp_max"] += 20
    player["hp"] = player["hp_max"]
    player["dano"] += 5  # Incrementa o dano do jogador a cada nível
    print(f"{player['nome']} subiu para o nível {player['level']}!")
    print(f"HP máximo aumentado para {player['hp_max']} e dano aumentado para {player['dano']}.")

# Função para escolher um caminho
def escolher_caminho():
    caminhos = ["Floresta", "Caverna", "Montanha", "Hell"]
    print("Escolha um caminho:")
    for i, caminho in enumerate(caminhos):
        print(f"{i + 1}. {caminho}")
    escolha = int(input("Digite o número do caminho escolhido: ")) - 1
    if escolha < 0 or escolha >= len(caminhos):
        print("Escolha inválida!")
        return escolher_caminho()
    return caminhos[escolha]

# Função para atacar um NPC
def atacar_npc(npc):
    npc["hp"] -= player["dano"]
    if npc["hp"] <= 0:
        print(f"Você derrotou {npc['nome']}!")
        player["exp"] += npc["exp"]
        if player["exp"] >= player["exp_max"]:
            level_up()
        drop_item(npc["drop"])
        reset_npc(npc)
    else:
        print(f"{npc['nome']} tem {npc['hp']} HP restante.")

# Função para dropar um item
def drop_item(item):
    print(f"Você encontrou um item: {item['nome']} (Atributos: {item})")
    player["inventario"].append(item)

# Função para tomar um banho em uma fonte termal
def tomar_banho():
    player["hp"] = player["hp_max"]
    print("Você tomou um banho na fonte termal e recuperou todo o seu HP!")
    print("Vida restaurada com sucesso.")

# Função para usar uma poção de cura
def usar_pocao():
    for item in player["inventario"]:
        if item["nome"] == "Poção de Cura":
            cura = item["cura"](player["hp_max"])
            player["hp"] = min(player["hp"] + cura, player["hp_max"])
            player["inventario"].remove(item)
            print(f"Você usou uma {item['nome']} e recuperou {cura} HP!")
            return
    print("Você não tem nenhuma Poção de Cura!")

# Função para exibir o inventário
def exibir_inventario():
    print("Inventário:")
    for item in player["inventario"]:
        print(f"- {item['nome']}")

# Função para reiniciar o jogo
def reiniciar_jogo():
    player["hp"] = player["hp_max"]
    player["inventario"] = []
    player["arma"] = None
    player["armadura"] = None
    lista_npcs.clear()

# Função principal do jogo
def main():
    player["nome"] = input("Digite o nome do seu personagem: ")
    while True:
        exibir_player()
        print("1. Escolher caminho")
        print("2. Tomar banho na fonte termal")
        print("3. Usar poção de cura")
        print("4. Exibir inventário")
        escolha = int(input("Digite a sua escolha: "))
        if escolha == 1:
            caminho = escolher_caminho()
            print(f"Você escolheu o caminho: {caminho}")
            if caminho == "Floresta":
                gerar_npcs(10, "Goblin", (1, 20))
            elif caminho == "Caverna":
                gerar_npcs(10, "Troll", (21, 50))
            elif caminho == "Montanha":
                gerar_npcs(10, "Dragão", (51, 80))
            elif caminho == "Hell":
                gerar_npcs(10, "Demônio", (81, 100))
            npc = random.choice(lista_npcs)
            print("Você encontrou um inimigo!")
            exibir_npc(npc)
            while npc["hp"] > 0 and player["hp"] > 0:
                atacar_npc(npc)
                if npc["hp"] > 0:
                    player["hp"] -= npc["dano"]
                    print(f"{npc['nome']} atacou você! Você tem {player['hp']} HP restante.")
                if player["hp"] <= 0:
                    print("Você morreu! Game Over.")
                    reiniciar_jogo()
                    break
            reset_player()
        elif escolha == 2:
            tomar_banho()
        elif escolha == 3:
            usar_pocao()
        elif escolha == 4:
            exibir_inventario()
        else:
            print("Escolha inválida!")

if __name__ == "__main__":
    main()