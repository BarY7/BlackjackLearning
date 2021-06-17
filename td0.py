import blackjack as game
import numpy as np
import random


# Parameters
gamma = 1

# Model
states = [i for i in range(23)]
actions = ['h', 's']

card_game = game.CardGame()
approx_V = {}
approx_Q = {}
num_visits = {}
num_visits_sarsa = {}


def compute_action_default_policy(s):
    sum = s
    if(sum >= 18):
        return 's'
    else:
        return 'h'


def get_current_state():
    start_hands = card_game.get_game_state()
    return start_hands[1]

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

def get_obs_sarsa(a):
    start_hands = card_game.get_game_state()
    state = start_hands[1]
    if(a == None):
        a = select_sarsa_action(state)
    dealer, player, reward, done = card_game.do_action(a)
    next_state = player
    if(done):
        next_state = 22
    if(next_state > 21):
        next_state = 22
    return state, a, reward, next_state, done

def select_sarsa_action(s):
    num_visits[s] += 1
    prob_for_random = 1/num_visits[s]    
    result = np.random.binomial(1, prob_for_random, 1)
    if(result == 1):
        return random.choice(actions)
    else:
        q_vals = np.array(list(map(lambda x: approx_Q[s][x], actions)))
        return actions[np.argmax(q_vals)]


def get_step_size(s, a):
    num_visits[s] += 1
    return 1/num_visits[s]
    # return 1

def get_step_size_sarsa(s, a):
    num_visits_sarsa[s][a] += 1
    return 1/num_visits_sarsa[s][a]
    # return 1




def run_td0():
    for state in states:
        if(state not in approx_V):
            approx_V[state] = {}
        approx_V[state] = 0
        num_visits[state] = 0

    for t in range(0, 10000):
        s, a, r, next_s, done = get_obs()
        step = get_step_size(s, a)
        temporal_diff = r + gamma * approx_V[next_s] - approx_V[s]
        approx_V[s] = approx_V[s] + step * temporal_diff
        if(done):
            card_game.reset()
    for player_sum in approx_V.keys():
        print(
            f"(Sum {player_sum}) : {approx_V[player_sum]}")
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
            num_visits_sarsa[state] = {}
            num_visits[state] = 0
        for action in actions:
            approx_Q[state][action] = 0
            num_visits_sarsa[state][action] = 0
    next_a = None
    for t in range(0, 80000):
        s = get_current_state()
        s, a, r, next_s, done = get_obs_sarsa(next_a)
        next_a = select_sarsa_action(s)
        step = get_step_size(s, a)
        sarsa_diff = r + gamma * \
            approx_Q[next_s][next_a] - approx_Q[s][a]
        approx_Q[s][a] = approx_Q[s][a] + step * sarsa_diff
        if(done):
            total_reward += r
            total_games += 1
            next_a = None
            card_game.reset()

    for player_sum in approx_Q.keys():
        action_values = np.array(list(map(lambda x: approx_Q[player_sum][x], actions)))
        best_action = actions[np.argmax(action_values)]
        print(
            f"(Action {player_sum}) : {best_action} , {approx_Q[player_sum]}")
    print(f'Probability to win: {total_reward/total_games}')


# run_td0()
run_sarsa()
