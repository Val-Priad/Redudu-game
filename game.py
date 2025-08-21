from random import randint, shuffle
from itertools import permutations, combinations

full_deck = [
    f"{value}{suit}"
    for value in [
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "0",
        "J",
        "Q",
        "K",
        "A",
    ]
    for suit in ["C", "D", "H", "S"]
] + ["X1", "X2"]

deck = [
    "2C",
    "2D",
    "2H",
    "2S",
    "3C",
    "3D",
    "3H",
    "3S",
    "4C",
    "4D",
    "4H",
    "4S",
    "5C",
    "5D",
    "5H",
    "5S",
    "6C",
    "6D",
    "6H",
    "6S",
    "7C",
    "7D",
    "7H",
    "7S",
    "8C",
    "8D",
    "8H",
    "8S",
    "9C",
    "9D",
    "9H",
    "9S",
    "0C",
    "0D",
    "0H",
    "0S",
    "JC",
    "JD",
    "JH",
    "JS",
    "QC",
    "QD",
    "QH",
    "QS",
    "KC",
    "KD",
    "KH",
    "KS",
    "AC",
    "AD",
    "AH",
    "AS",
    "X1",
    "X2",
]

gifs = [
    "girl_1",
    "girl_2",
    "girl_3",
    "girl_4",
    "girl_5",
    "girl_6",
    "girl_7",
    "girl_8",
    "girl_9",
    "girl_10",
    "boy_1",
    "boy_2",
    "boy_3",
    "boy_4",
    "boy_5",
    "boy_6",
    "boy_7",
    "boy_8",
    "boy_9",
    "boy_10",
]

ukrainian_female_names = [
    "Сивашка",
    "Модрина",
    "Живослава",
    "Вишеня",
    "Берегиня",
    "Гайовина",
    "Златоуста",
    "Мар'яна",
    "Лелія",
    "Яворина",
]

kozacki_imena = [
    "Сагайдачний",
    "Богдан",
    "Тарас",
    "Григорій",
    "Іван",
    "Михайло",
    "Семен",
    "Данило",
    "Остап",
    "Петро",
]


def shuffle_cards():
    croupier = randint(1, 3)
    cards = full_deck[:]
    shuffle(cards)

    num_players = 3
    hands = {
        f"Player {i + 1}": cards[i * 7 : (i + 1) * 7]
        for i in range(num_players)
    }
    remaining_deck = cards[num_players * 7 :]

    common_trump = remaining_deck.pop(0)
    remaining_deck.append(common_trump)

    piles = [remaining_deck[i::4] for i in range(4)]
    common_pile = []
    for i in range(4):
        if len(piles[i]) > 8:
            common_pile = piles[i]
            piles.pop(i)
            break

    player_piles = {f"Player {i + 1}": piles[i] for i in range(3)}

    player_trumps = {key: value[-1] for key, value in player_piles.items()}

    enemy_gifs = gifs.copy()
    shuffle(enemy_gifs)
    gifs_dict = {}
    for i in range(3):
        gifs_dict[f"enemy_{i + 1}_gif"] = enemy_gifs.pop(
            randint(0, len(enemy_gifs) - 1)
        )

    man = kozacki_imena.copy()
    woman = ukrainian_female_names.copy()
    player_name_dict = {}
    for key, value in gifs_dict.items():
        man_name = man[randint(0, len(man) - 1)]
        woman_name = woman[randint(0, len(woman) - 1)]
        man.remove(man_name)
        woman.remove(woman_name)
        key = key.replace("gif", "name")
        if "boy" in value:
            player_name_dict[key] = f"Козак {man_name}"
        if "girl" in value:
            player_name_dict[key] = f"Пані {woman_name}"
    player_name_dict["enemy_3_name"] = "ШІ гравець"
    return {
        "croupier": croupier,
        "current_player": croupier,
        "discards": [],
        "cards_in_game": [],
        "what_was_done": "",
        "hands": hands,
        "common_trump": common_trump,
        "player_piles": player_piles,
        "common_pile": common_pile,
        "gifs_dict": gifs_dict,
        "player_name_dict": player_name_dict,
        "player_trumps": player_trumps,
        "cards_was_moved": -1,
    }


MOVE_TO_ANOTHER = 1
BEAT_THE_CARDS = 2
TAKE = 3
NOTHING = -1
X2_BEAT = 3
X1_BEAT = 2
USUAL_BEAT = 1

VALUES = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "0": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
    "X1": 31,
    "X2": 32,
}

DECK = {
    "2C": "Двійка треф",
    "2D": "Двійка бубна",
    "2H": "Двійка чирва",
    "2S": "Двійка піка",
    "3C": "Трійка треф",
    "3D": "Трійка бубна",
    "3H": "Трійка чирва",
    "3S": "Трійка піка",
    "4C": "Четвірка треф",
    "4D": "Четвірка бубна",
    "4H": "Четвірка чирва",
    "4S": "Четвірка піка",
    "5C": "П'ятірка треф",
    "5D": "П'ятірка бубна",
    "5H": "П'ятірка чирва",
    "5S": "П'ятірка піка",
    "6C": "Шістка треф",
    "6D": "Шістка бубна",
    "6H": "Шістка чирва",
    "6S": "Шістка піка",
    "7C": "Сімка треф",
    "7D": "Сімка бубна",
    "7H": "Сімка чирва",
    "7S": "Сімка піка",
    "8C": "Вісімка треф",
    "8D": "Вісімка бубна",
    "8H": "Вісімка чирва",
    "8S": "Вісімка піка",
    "9C": "Дев'ятка треф",
    "9D": "Дев'ятка бубна",
    "9H": "Дев'ятка чирва",
    "9S": "Дев'ятка піка",
    "0C": "Десятка треф",
    "0D": "Десятка бубна",
    "0H": "Десятка чирва",
    "0S": "Десятка піка",
    "JC": "Валет треф",
    "JD": "Валет бубна",
    "JH": "Валет чирва",
    "JS": "Валет піка",
    "QC": "Дама треф",
    "QD": "Дама бубна",
    "QH": "Дама чирва",
    "QS": "Дама піка",
    "KC": "Король треф",
    "KD": "Король бубна",
    "KH": "Король чирва",
    "KS": "Король піка",
    "AC": "Туз треф",
    "AD": "Туз бубна",
    "AH": "Туз чирва",
    "AS": "Туз піка",
    "X1": "Чорна редуда",
    "X2": "Червона редуда",
}

example = {
    "croupier": int,
    "current_player": int,
    "discards": [],
    "cards_in_game": [{}, {}],
    "what_was_done": "",
    "hands": [{}, {}, {}],
    "common_trump": str,
    "player_piles": [[], [], []],
    "common_pile": [],
    "gifs_dict": {},
    "player_name_dict": {},
    "player_trumps": {},
}


def get_value_cards(game_state) -> dict:
    res_values = {}
    player_key = f"Player {game_state['current_player']}"
    player_hand = game_state["hands"][player_key]
    for card in player_hand:
        res_values[card] = VALUES.get(card[0], 0)

    user_trump = game_state["player_trumps"][player_key]
    if user_trump in game_state["hands"][player_key]:
        res_values[user_trump] = 29

    trump = game_state["common_trump"]
    if trump in game_state["hands"][player_key]:
        res_values[trump] = 30

    if "X1" in player_hand:
        res_values["X1"] = 31

    if "X2" in player_hand:
        res_values["X2"] = 32

    return res_values


def make_a_move(game_state) -> dict:
    values = get_value_cards(game_state)

    values = sorted(values.items(), key=lambda x: x[1])
    the_smallest_card = values[0][0]

    player_num = game_state["current_player"]
    player_key = f"Player {player_num}"
    player_hand = game_state["hands"][player_key]
    idx = player_hand.index(the_smallest_card)

    game_state["cards_in_game"] = [(f"{player_hand.pop(idx)}", player_key, "")]
    name = game_state["player_name_dict"][f"enemy_{player_num}_name"]
    game_state["what_was_done"] = (
        f"{name} походив/ла картою {DECK[f'{the_smallest_card}'].lower()}."
    )
    game_state["current_player"] = player_num % 3 + 1
    return game_state


def nominal_is_unique(cards):
    nominal = cards[0][0][0]
    for card in cards:
        if nominal != card[0][0] or nominal == "X":
            return False
    return True


def parse_card(card):
    rank = card[0]
    suit = card[1]
    return VALUES[f"{rank}"], suit


def can_beat(card_to_beat, defender, common_trump, player_trump):
    rank_to_beat, suit_to_beat = parse_card(card_to_beat)
    rank_defender, suit_defender = parse_card(defender)

    if suit_defender == suit_to_beat:
        return rank_defender > rank_to_beat
    elif defender == common_trump and rank_to_beat < 29:
        return True
    elif defender == player_trump and rank_to_beat < 20:
        return True
    return False


def check_lasting_qty_to_bit(
    clear_cards_in_game, player_hand, common_trump, player_trump, qty_to_beat
):
    counter = 0
    for card_to_beat in clear_cards_in_game:
        for card_defender in player_hand:
            if card_defender in ["X1", "X2"] or card_to_beat in ["X1", "X2"]:
                continue
            if can_beat(
                card_to_beat, card_defender, common_trump, player_trump
            ):
                counter += 1
                player_hand.remove(card_defender)
                break
        if counter >= qty_to_beat:
            return True
    return False


def what_to_do(game_state) -> tuple[int, int]:
    player_key = f"Player {game_state['current_player']}"
    player_hand = game_state["hands"][player_key].copy()
    cards_in_game = game_state["cards_in_game"]

    nominal = cards_in_game[0][0][0]
    exist_opportunity = nominal_is_unique(cards_in_game) and (
        nominal in [card[0] for card in player_hand]
        or "X1" in player_hand
        or "X2" in player_hand
    )
    cards_in_game_nominals = [card[0][0] for card in cards_in_game]
    next_player = game_state["current_player"] % 3 + 1
    next_player_key = f"Player {next_player}"
    next_player_hand = game_state["hands"][next_player_key].copy()
    avoided_first_obstacle = not (
        cards_in_game_nominals.count(nominal) > 3
        and len(next_player_hand) == 1
    )
    avoided_2_nd_obstacle = not (
        cards_in_game_nominals.count(nominal) > 4
        and len(next_player_hand) <= 2
    )
    avoided_3_rd_obstacle = not (
        len(cards_in_game) == 5 and "X2" not in next_player_hand
    )
    avoided_4th_obstacle = not (cards_in_game_nominals.count("X") == 2)
    if (
        exist_opportunity
        and avoided_first_obstacle
        and avoided_2_nd_obstacle
        and avoided_3_rd_obstacle
        and avoided_4th_obstacle
    ):
        return MOVE_TO_ANOTHER, NOTHING

    common_trump = game_state["common_trump"]
    player_trump = game_state["player_trumps"][
        f"Player {game_state['current_player']}"
    ]

    clear_cards_in_game = [card[0] for card in cards_in_game]
    can_beat_with_usual_cards = True
    for card_to_beat in clear_cards_in_game:
        beaten = False
        for card_defender in player_hand:
            if card_defender in ["X1", "X2"] or card_to_beat in ["X1", "X2"]:
                continue
            if can_beat(
                card_to_beat, card_defender, common_trump, player_trump
            ):
                beaten = True
                player_hand.remove(card_defender)
                break
        if not beaten:
            can_beat_with_usual_cards = False
            break

    player_hand = game_state["hands"][player_key].copy()

    can_beat_with_x2 = False
    if "X2" in player_hand:
        x1_not_in_attack = "X1" not in clear_cards_in_game

        qty_to_beat = len(clear_cards_in_game) - 3
        if "X2" in player_hand:
            player_hand.remove("X2")
        can_beat_qty_to_beat = check_lasting_qty_to_bit(
            clear_cards_in_game,
            player_hand,
            common_trump,
            player_trump,
            qty_to_beat,
        )

        player_hand = game_state["hands"][player_key].copy()

        x1_in_attack = "X1" in clear_cards_in_game
        clear_cards_in_game_copy = [card[0] for card in cards_in_game]
        if x1_in_attack:
            clear_cards_in_game_copy.remove("X1")
        qty_to_beat = len(clear_cards_in_game_copy)
        counter = 0
        can_beat_qty_to_beat2 = False
        for card_to_beat in clear_cards_in_game_copy:
            for card_defender in player_hand:
                if card_defender in ["X1", "X2"] or card_to_beat in [
                    "X1",
                    "X2",
                ]:
                    continue
                if can_beat(
                    card_to_beat, card_defender, common_trump, player_trump
                ):
                    counter += 1
                    player_hand.remove(card_defender)
                    break
            if counter + 1 >= qty_to_beat:
                can_beat_qty_to_beat2 = True
                break

        len(clear_cards_in_game_copy)

        can_beat_with_x2 = (can_beat_qty_to_beat and x1_not_in_attack) or (
            x1_in_attack and can_beat_qty_to_beat2
        )

    player_hand = game_state["hands"][player_key].copy()
    can_beat_with_x1 = False
    if "X1" in player_hand:
        x2_in_attack = "X2" in clear_cards_in_game
        common_trump_in_hand = common_trump in player_hand
        qty_to_beat = len(clear_cards_in_game) - 1
        can_beat_qty_to_beat = False

        player_hand.remove("X1")
        if common_trump_in_hand:
            player_hand.remove(common_trump)
        counter = 0
        for card_to_beat in clear_cards_in_game:
            for card_defender in player_hand:
                if card_defender in ["X1", "X2"] or card_to_beat in [
                    "X1",
                    "X2",
                ]:
                    continue
                if can_beat(
                    card_to_beat, card_defender, common_trump, player_trump
                ):
                    counter += 1
                    player_hand.remove(card_defender)
                    break
            if counter >= qty_to_beat:
                can_beat_qty_to_beat = True
                break

        player_hand = game_state["hands"][player_key].copy()

        x2_not_in_attack = "X2" not in clear_cards_in_game

        qty_to_beat = len(clear_cards_in_game) - 2
        if "X1" in player_hand:
            player_hand.remove("X1")
        can_beat_qty_to_beat2 = check_lasting_qty_to_bit(
            clear_cards_in_game,
            player_hand,
            common_trump,
            player_trump,
            qty_to_beat,
        )

        can_beat_with_x1 = (
            x2_in_attack and common_trump_in_hand and can_beat_qty_to_beat
        ) or (x2_not_in_attack and can_beat_qty_to_beat2)
    if can_beat_with_usual_cards:
        return BEAT_THE_CARDS, USUAL_BEAT
    elif can_beat_with_x1:
        return BEAT_THE_CARDS, X1_BEAT
    elif can_beat_with_x2:
        return BEAT_THE_CARDS, X2_BEAT
    return TAKE, NOTHING


def move_to_another(game_state):
    player_key = f"Player {game_state['current_player']}"
    player_num = game_state["current_player"]
    player_hand = game_state["hands"][player_key].copy()
    cards_in_game = game_state["cards_in_game"].copy()
    nominal = cards_in_game[0][0][0]

    nominal_is_in_player_hand = (
        True if nominal in [card[0] for card in player_hand] else False
    )
    remove_list = []
    if nominal_is_in_player_hand:
        for card in player_hand:
            if nominal == card[0]:
                remove_list.append(card)
                cards_in_game.append((card, player_key, "moved"))
    else:
        for card in player_hand:
            if card[0] == "X":
                remove_list.append(card)
                cards_in_game.append((card, player_key, "moved"))
                break

    for card in remove_list:
        player_hand.remove(card)

    attacker_num = (player_num - 2) % 3 + 1

    for i in range(len(cards_in_game)):
        card = cards_in_game[i]
        if card[1] == f"Player {attacker_num}":
            cards_in_game[i] = (card[0], player_key, card[2])

    transferred_with = " ".join([DECK[card].lower() for card in remove_list])
    game_state["what_was_done"] = (
        f"{game_state['player_name_dict'][f'enemy_{player_num}_name']} "
        f"перевів/ла карти/ту картою/ами {transferred_with}."
    )
    game_state["hands"][player_key] = player_hand
    game_state["cards_in_game"] = cards_in_game
    game_state["current_player"] = player_num % 3 + 1
    if game_state["cards_was_moved"] == -1:
        game_state["cards_was_moved"] = attacker_num

    return game_state


def take_cards(attackers_hand, common_pile, attackers_pile):
    if len(attackers_hand) < 7:
        if common_pile:
            while len(attackers_hand) != 7 and common_pile:
                attackers_hand.append((common_pile.pop(0)))
        elif attackers_pile:
            while len(attackers_hand) != 7 and attackers_pile:
                attackers_hand.append((attackers_pile.pop(0)))
        else:
            pass


def take_cards_from_piles(game_state):
    player_num = game_state["current_player"]
    common_pile = game_state["common_pile"]

    attacker_num = (player_num - 2) % 3 + 1

    if game_state["cards_was_moved"] != -1:
        attacker_num = game_state["cards_was_moved"]

    attackers_hand = game_state["hands"][f"Player {attacker_num}"]
    attackers_pile = game_state["player_piles"][f"Player {attacker_num}"]

    player_hand = game_state["hands"][f"Player {attacker_num % 3 + 1}"]
    players_pile = (game_state)["player_piles"][
        f"Player {attacker_num % 3 + 1}"
    ]

    last_players_hand = (game_state)["hands"][
        f"Player {(attacker_num % 3 + 1) % 3 + 1}"
    ]
    last_players_pile = (game_state)["player_piles"][
        (f"Player {(attacker_num % 3 + 1) % 3 + 1}")
    ]

    take_cards(attackers_hand, common_pile, attackers_pile)
    take_cards(player_hand, common_pile, players_pile)
    take_cards(last_players_hand, common_pile, last_players_pile)
    game_state["cards_was_moved"] = -1
    game_state["what_was_done"] += "Гравці добирають карти."
    return game_state


def usual_beat(game_state, limit=1000):
    player_key = f"Player {game_state['current_player']}"
    player_hand = game_state["hands"][player_key].copy()
    cards_in_game = game_state["cards_in_game"].copy()
    what_was_done = ""
    player_num = game_state["current_player"]
    common_trump = game_state["common_trump"]
    player_trump = game_state["player_trumps"][player_key]
    player_name = game_state["player_name_dict"][f"enemy_{player_num}_name"]
    counter = 0
    if counter < limit:
        for idx, card_data in enumerate(cards_in_game):
            card_to_beat, whose, explanation = card_data
            for card_defender in player_hand:
                if card_defender in ["X1", "X2"] or card_to_beat in [
                    "X1",
                    "X2",
                ]:
                    continue
                if can_beat(
                    card_to_beat, card_defender, common_trump, player_trump
                ):
                    cards_in_game[idx] = (card_to_beat, whose, card_defender)
                    what_was_done += (
                        f"{player_name} "
                        f"побив/ла карту {DECK[card_to_beat].lower()} "
                        f"картою {DECK[card_defender].lower()}\n"
                    )

                    player_hand.remove(card_defender)
                    counter += 1
                    break
                if counter >= limit:
                    break
    return what_was_done, player_hand, cards_in_game


def redudas_beat(game_state, what_to_remove, qty_to_substract):
    player_key = f"Player {game_state['current_player']}"
    player_hand = game_state["hands"][player_key].copy()
    cards_in_game = game_state["cards_in_game"].copy()
    what_was_done = ""

    player_hand.remove(what_to_remove)
    qty_to_beat = len(cards_in_game) - qty_to_substract
    message, player_hand, cards_in_game = usual_beat(game_state, qty_to_beat)
    what_was_done += message
    for idx, card_data in enumerate(cards_in_game):
        card_to_beat, whose, explanation = card_data
        if explanation == "":
            cards_in_game[idx] = (card_to_beat, whose, what_to_remove)
    if what_to_remove == "X1":
        what_was_done += "Карти, що залишилися побиті чорною редудою\n"
    else:
        what_was_done += "Карти, що залишилися побиті червоною редудою\n"
    return what_was_done, player_hand, cards_in_game


def beat_the_cards(game_state, how_to_beat: int) -> dict:
    player_key = f"Player {game_state['current_player']}"
    player_num = game_state["current_player"]
    player_hand = game_state["hands"][player_key].copy()
    cards_in_game = game_state["cards_in_game"].copy()
    common_trump = game_state["common_trump"]
    player_name = game_state["player_name_dict"][f"enemy_{player_num}_name"]
    what_was_done = ""
    clear_cards_in_game = [card[0] for card in cards_in_game]

    if how_to_beat == USUAL_BEAT:
        what_was_done, player_hand, cards_in_game = usual_beat(game_state)
    elif how_to_beat == X1_BEAT:
        x2_in_attack = "X2" in clear_cards_in_game
        common_trump_in_hand = common_trump in player_hand
        if x2_in_attack and common_trump_in_hand:
            for idx, card_data in enumerate(cards_in_game):
                card_to_beat, whose, explanation = card_data
                if card_to_beat == "X2":
                    player_hand.remove("X1")
                    player_hand.remove(common_trump)
                    cards_in_game[idx] = (
                        card_to_beat,
                        whose,
                        f"X1 + {common_trump}",
                    )
                    game_state["cards_in_game"] = cards_in_game
                    what_was_done += (
                        f"{player_name} "
                        f"побив/ла карту червона редуда "
                        f"комбінацією карт чорна редуда та "
                        f"{DECK[common_trump].lower()}\n"
                    )
                    break
            message, player_hand, cards_in_game = usual_beat(game_state)
            what_was_done += message
        else:
            message, player_hand, cards_in_game = redudas_beat(
                game_state, "X1", 2
            )
            what_was_done += message
    elif how_to_beat == X2_BEAT:
        x1_in_attack = "X1" in clear_cards_in_game
        if x1_in_attack:
            message, player_hand, cards_in_game = redudas_beat(
                game_state, "X2", 1
            )
            what_was_done += message
        else:
            message, player_hand, cards_in_game = redudas_beat(
                game_state, "X2", 3
            )
            what_was_done += message
    else:
        pass

    game_state["discards"].extend(cards_in_game)
    game_state["cards_in_game"] = []
    game_state["hands"][player_key] = player_hand
    game_state["what_was_done"] = what_was_done
    take_cards_from_piles(game_state)
    return game_state


def take(game_state, who=0):
    player_key = f"Player {game_state['current_player']}"
    player_num = game_state["current_player"]
    player_hand = game_state["hands"][player_key].copy()
    cards_in_game = game_state["cards_in_game"].copy()
    player_name = game_state["player_name_dict"][f"enemy_{player_num}_name"]

    player_hand.extend([card[0] for card in cards_in_game])
    cards_in_game = []
    if who == 0:
        what_was_done = (
            f"{player_name} забирає карти, бо не зміг/змогла побити.\n"
        )
    else:
        what_was_done = "Гравець забирає карти, бо не зміг побити.\n"

    game_state["hands"][player_key] = player_hand
    game_state["what_was_done"] = what_was_done
    game_state["cards_in_game"] = cards_in_game
    take_cards_from_piles(game_state)
    game_state["current_player"] = player_num % 3 + 1
    return game_state


def ai_move(game_state):
    if not game_state["cards_in_game"]:
        return make_a_move(game_state)

    do, beating_type = what_to_do(game_state)
    state = None
    if do == MOVE_TO_ANOTHER:
        state = move_to_another(game_state)
    elif do == BEAT_THE_CARDS:
        state = beat_the_cards(game_state, beating_type)
    elif do == TAKE:
        state = take(game_state)

    return state


def user_takes_cards(game_state):
    return take(game_state, 1)


def user_makes_a_move(
    game_state: dict, player_cards: list
) -> tuple[bool, dict]:
    list_of_nominals = [card[0] for card in player_cards]
    first_nominal = list_of_nominals[0]
    for nominal in list_of_nominals:
        if nominal != first_nominal:
            return False, {}
    current_player = game_state.get("current_player")
    player_key = f"Player {current_player}"
    game_state["cards_in_game"] = [
        (card, player_key, "") for card in player_cards
    ]
    for card in player_cards:
        game_state["hands"][player_key].remove(card)
    game_state["what_was_done"] = (
        f"Ви ходите картою/ми "
        f"{' '.join([DECK[card].lower() for card in player_cards])}\n"
    )
    game_state["current_player"] = current_player % 3 + 1
    return True, game_state


def qty_is_equal(player_cards, attacker_cards, qty_cards_to_ignore=0):
    return len(player_cards) == len(attacker_cards) - qty_cards_to_ignore


def find_defense_combination(
    attacker_cards, player_cards, common_trump, player_trump, ignore_limit=0
):
    for ignore_count in range(ignore_limit + 1):
        for ignored_cards in combinations(attacker_cards, ignore_count):
            remaining_attacker_cards = [
                card for card in attacker_cards if card not in ignored_cards
            ]

            for defender_combination in permutations(
                player_cards, len(remaining_attacker_cards)
            ):
                if all(
                    can_beat(
                        remaining_attacker_cards[i],
                        defender_combination[i],
                        common_trump,
                        player_trump,
                    )
                    for i in range(len(remaining_attacker_cards))
                ):
                    return list(defender_combination), list(ignored_cards)

    return None, None


def user_beat_lasting_cards(
    cards_in_game, player_hand, common_trump, player_trump
):
    what_was_done = ""
    for idx, card_data in enumerate(cards_in_game):
        card_to_beat, whose, explanation = card_data
        for card_defender in player_hand:
            if card_defender in ["X1", "X2"] or card_to_beat in ["X1", "X2"]:
                continue
            if can_beat(
                card_to_beat, card_defender, common_trump, player_trump
            ):
                cards_in_game[idx] = (card_to_beat, whose, card_defender)
                what_was_done += (
                    f"Гравець "
                    f"побив карту {DECK[card_to_beat].lower()} "
                    f"картою {DECK[card_defender].lower()}\n"
                )

                player_hand.remove(card_defender)
                break
    return cards_in_game, what_was_done


def remove_card_from_cards_in_game(cards_in_game, card_to_remove):
    cards_in_game_copy = cards_in_game.copy()
    for card in cards_in_game_copy:
        if card[0] == card_to_remove:
            cards_in_game_copy.remove(card)
    return cards_in_game_copy


def user_beats_the_cards(game_state: dict, player_cards: list):
    cards_in_game = game_state["cards_in_game"].copy()
    common_trump = game_state["common_trump"]
    player_num = game_state["current_player"]
    player_key = f"Player {player_num}"
    player_trump = game_state["player_trumps"][player_key]
    attack_cards = [card[0] for card in cards_in_game]
    player_hand = game_state["hands"][player_key]

    common_trump_is_in_player_cards = common_trump in player_cards

    x2_is_in_player_cards = "X2" in player_cards
    x1_is_in_player_cards = "X1" in player_cards

    x2_is_in_attack = "X2" in attack_cards
    x1_is_in_attack = "X1" in attack_cards

    can_t_beat = x2_is_in_attack and (
        not x1_is_in_player_cards or not common_trump_is_in_player_cards
    )
    if can_t_beat:
        return False, {}

    can_t_beat = x1_is_in_attack and not x2_is_in_player_cards
    if can_t_beat:
        return False, {}

    what_was_done = ""
    qty_cards_to_ignore = 0
    beaten_with = ""
    if x2_is_in_player_cards and x1_is_in_attack:
        attack_cards.remove("X1")
        cards_in_game = remove_card_from_cards_in_game(cards_in_game, "X1")
        player_cards.remove("X2")
        player_hand.remove("X2")
        beaten_with = "X2"
        game_state["discards"].append(
            ("X1", f"Player {(player_num - 2) % 3 + 1}", "X2")
        )
        what_was_done = "Гравець б'є чорну редуду червоною\n"
        qty_cards_to_ignore = 1
    elif x2_is_in_player_cards and not x1_is_in_attack:
        player_cards.remove("X2")
        player_hand.remove("X2")
        beaten_with = "X2"
        qty_cards_to_ignore = 3
    elif (
        x1_is_in_player_cards
        and x2_is_in_attack
        and common_trump_is_in_player_cards
    ):
        player_cards.remove("X1")
        player_hand.remove("X1")
        player_cards.remove(common_trump)
        player_hand.remove(common_trump)
        attack_cards.remove("X2")
        beaten_with = "X1"
        game_state["discards"].append(
            (
                "X2",
                f"Player {(player_num - 2) % 3 + 1}",
                f"X1 + {common_trump}",
            )
        )
        cards_in_game = remove_card_from_cards_in_game(cards_in_game, "X2")
        what_was_done = (
            "Гравець б'є червону редуду чорною з загальним козирем\n"
        )
    elif x1_is_in_player_cards and not x2_is_in_attack:
        player_cards.remove("X1")
        player_hand.remove("X1")
        beaten_with = "X1"
        qty_cards_to_ignore = 2

    if qty_cards_to_ignore > len(cards_in_game) and player_cards:
        return False, {}

    if qty_cards_to_ignore > len(cards_in_game):
        what_was_done = (
            f"Гравець б'є усі карти на полі картою "
            f"{DECK[beaten_with].lower()}.\n"
        )
        for idx, card_data in enumerate(cards_in_game):
            card, player, explanation = card_data
            cards_in_game[idx] = (card, player, beaten_with)
    else:
        if not qty_is_equal(player_cards, attack_cards, qty_cards_to_ignore):
            return False, {}

        (res_combination, ignored_cards) = find_defense_combination(
            attack_cards,
            player_cards,
            common_trump,
            player_trump,
            qty_cards_to_ignore,
        )
        if not res_combination:
            return False, {}
        for ignored_card in ignored_cards:
            cards_in_game = remove_card_from_cards_in_game(
                cards_in_game, ignored_card
            )
        cards_in_game, message = user_beat_lasting_cards(
            cards_in_game, player_cards, common_trump, player_trump
        )
        message2 = ""
        if ignored_cards:
            for card in ignored_cards:
                message2 += (
                    f"Гравець побив карту "
                    f"{DECK[card].lower()} картою "
                    f"{DECK[beaten_with].lower()}\n"
                )
                cards_in_game.append(
                    (card, f"Player {(player_num - 2) % 3 + 1}", beaten_with)
                )
        what_was_done += message + message2

        for card in res_combination:
            player_hand.remove(card)
    game_state["what_was_done"] = what_was_done
    game_state["cards_in_game"] = []
    game_state["discards"].extend(cards_in_game)
    take_cards_from_piles(game_state)
    return True, game_state


def user_moves_the_cards(game_state, selected_player_cards):
    player_key = f"Player {game_state['current_player']}"
    player_num = game_state["current_player"]
    selected_player_cards_nominals = [
        card[0] for card in selected_player_cards
    ]
    first_card_nominal = selected_player_cards_nominals[0]
    for nominal in selected_player_cards_nominals:
        if first_card_nominal != nominal:
            return False, {}
    cards_in_game = game_state["cards_in_game"].copy()
    cards_in_game_nominals = [card[0][0] for card in cards_in_game]
    if (
        cards_in_game_nominals[0] != first_card_nominal
        and first_card_nominal != "X"
    ):
        return False, {}

    for card in selected_player_cards:
        game_state["hands"][player_key].remove(card)
        cards_in_game.append((card, player_key, "moved"))

    attacker_num = (player_num - 2) % 3 + 1

    for i in range(len(cards_in_game)):
        card = cards_in_game[i]
        if card[1] == f"Player {attacker_num}":
            cards_in_game[i] = (card[0], player_key, card[2])
    deck_to_print = [DECK[card].lower() for card in selected_player_cards]
    fin_deck = " ".join(deck_to_print)
    what_was_done = f"Гравець перевів карти картою/ами {fin_deck}.\n"
    game_state["current_player"] = player_num % 3 + 1
    game_state["what_was_done"] = what_was_done
    game_state["cards_in_game"] = cards_in_game
    return True, game_state


if __name__ == "__main__":
    print(DECK.keys())
