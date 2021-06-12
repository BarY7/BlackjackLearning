import blackjack as game
import numpy as np


# Parameters
gamma = 0.9

# Model
states = [(i+4, j+2)for i in range(19) for j in range(10)]
actions = ['h', 's']

card_game = game.CardGame()
approx_v = {}
num_visits = {}


def compute_action_default_policy(s):
    sum = s[0]
    if(sum >= 18):
        return 's'
    else:
        return 'h'


def get_obs():
    start_hands = card_game.get_game_state()
    state = (start_hands[1], card_game.total([start_hands[0]]))
    a = None
    if(state[0] >= 18):
        a = 's'
    else:
        a = 'h'
    dealer, player, reward, done = card_game.do_action(a)
    next_state = (player, card_game.total([dealer]))
    if(next_state[0] > 21):
        next_state = (22, next_state[1])
    return state, a, reward, next_state, done


def get_step_size(s, a):
    num_visits[s[0]][s[1]][a] += 1
    return 1/num_visits[s[0]][s[1]][a]


def run_td0():
    for state in states:
        if(state[0] not in approx_v):
            approx_v[state[0]] = {}
        approx_v[state[0]][state[1]] = 0
        if(state[0] not in num_visits):
            num_visits[state[0]] = {}
        num_visits[state[0]][state[1]] = {}
        for action in actions:
            num_visits[state[0]][state[1]][action] = 0

    for t in range(0, 10000):
        s, a, r, next_s, done = get_obs()
        step = get_step_size(s, a)
        temporal_diff = r + gamma * \
            approx_v[next_s[0]][next_s[1]] - approx_v[s[0]][s[1]]
        approx_v[s[0]][s[1]] = approx_v[s[0]][s[1]] + step * temporal_diff
        if(done):
            card_game.reset()
    for player_sum in approx_v.keys():
        array = np.array(list(approx_v[player_sum].values()))
        min = array.min()
        if(min < 0):
          array += min
        sum = array.sum()
        array /= sum
        for host_card in approx_v[2].keys():
          #try normalize minus values.
          print(
              f"{player_sum - host_card} : {approx_v[player_sum][host_card]}")


run_td0()
