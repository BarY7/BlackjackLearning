import blackjack as game
import numpy as np
import random


# Parameters
gamma = 1

# Model
states = [i for i in range(23)]
actions = ['h', 's']

card_game = game.CardGame()
approx_Q = {}
approx_Q = {}
num_visits = {}


def compute_action_default_policy(s):
    sum = s
    if(sum >= 18):
        return 's'
    else:
        return 'h'


def get_obs():
    start_hands = card_game.get_game_state()
    state = start_hands[1]
    a = None
    if(state >= 18):
        a = 's'
    else:
        a = 'h'
    dealer, player, reward, done = card_game.do_action(a)
    next_state = player
    if(done):
        next_state = 22
    if(next_state > 21):
        next_state = 22
    return state, a, reward, next_state, done


def get_step_size(s, a):
    num_visits[s] += 1
    return 1/num_visits[s]
    # return 1


def select_sarsa_action(s):
    if(num_visits[s] == 0):
        prob_for_random = 1
    else:
        prob_for_random = 1/num_visits[s]
    result = np.random.binomial(1, prob_for_random, 1)
    if(result == 1):
        return random.choice(actions)
    else:
        q_vals = np.array(list(map(lambda x: approx_Q[s][x], actions)))
        return actions[np.argmax(q_vals)]


def run_td0():
    for state in states:
        if(state not in approx_Q):
            approx_Q[state] = {}
        approx_Q[state] = 0
        num_visits[state] = 0

    for t in range(0, 80000):
        s, a, r, next_s, done = get_obs()
        step = get_step_size(s, a)
        temporal_diff = r + gamma * approx_Q[next_s] - approx_Q[s]
        approx_Q[s] = approx_Q[s] + step * temporal_diff
        if(approx_Q[s]  > 1):
            print('here')
        if(done):
            card_game.reset()
    for player_sum in approx_Q.keys():
        print(
            f"(Sum {player_sum}) : {approx_Q[player_sum]}")
        # array = np.array(list(approx_v[player_sum].values()))
        # min = array.min()
        # if(min < 0):
        #   array += min
        # sum = array.sum()
        # if(sum>0):
        #     array /= sum
        # for host_card in approx_v[4].keys():
        #   #try normalize minus values.
        #   print(
        #       f"({player_sum} - {host_card}) : {approx_v[player_sum][host_card]}")


def run_sarsa():
    total_reward = 0 
    total_games = 0
    for state in states:
        if(state not in approx_Q):
            approx_Q[state] = {}
        for action in actions:
            approx_Q[state][action] = 0
            num_visits[state] = 0
    for t in range(0, 10000):
        s, a, r, next_s, done = get_obs()
        next_a = select_sarsa_action(s)
        step = get_step_size(s, a)
        sarsa_diff = r + gamma * \
            approx_Q[next_s][next_a] - approx_Q[s][a]
        approx_Q[s][a] = approx_Q[s][a] + step * sarsa_diff
        if(done):
            total_reward += r
            total_games += 1
            card_game.reset()

    for player_sum in approx_Q.keys():
        print(
            f"(Sum {player_sum}) : {approx_Q[player_sum]}")
    print(f'Probability to win: {total_reward/total_games}')


#run_td0()
run_sarsa()
