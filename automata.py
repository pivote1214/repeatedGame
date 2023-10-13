import numpy as np
import itertools
from graphviz import Digraph

# 有限オートマトンを定義
class FiniteAutomaton:
    def __init__(self, states, initial_state, action_function, transition_function):
        self.states = states
        self.initial_state = initial_state
        self.action_function = action_function
        self.transition_function = transition_function


# 有限オートマトンを描画
def draw_automaton(fa: FiniteAutomaton, machine_num):
    """有限オートマトンを描画する

    Args:
        fa (FiniteAutomaton): 有限オートマトン
        machine_num (int): 有限オートマトンの番号

    Returns:
        None
    """
    act = ['C', 'D']

    # Create a new Graphviz graph
    graph = Digraph(graph_attr={'rankdir': 'LR', 'size': '4,2'}, 
                    node_attr={'shape': 'circle', 'fixedsize': 'true'})

    # Set the resolution of the graph
    graph.attr(dpi='300')

    # Add the states to the graph
    for state, action in fa.action_function.items():
        if state == fa.initial_state:
            graph.node(str(state), label=action, width='0.4', height='0.4', fillcolor='gray', style='filled')
        else:
            graph.node(str(state), label=action, width='0.4', height='0.4')

    # 状態遷移を追加
    for state, action in fa.action_function.items():
        # g, bの遷移先が同じ場合
        if fa.transition_function[(state, 'g')] == fa.transition_function[(state, 'b')]:
            graph.edge(str(state), str(fa.transition_function[(state, 'g')]), label='g, b')
        # g, bの遷移先が異なる場合
        else:
            graph.edge(str(state), str(fa.transition_function[(state, 'g')]), label='g')
            graph.edge(str(state), str(fa.transition_function[(state, 'b')]), label='b')
    
    # Save the graph to a file
    graph.render(f"automaton/automata_{machine_num}", format='png')


# 1状態の有限オートマトンを作成
def make_one_state_automaton() -> FiniteAutomaton:
    one_state_automaton = []
    for action in ["C", "D"]:
        automaton = FiniteAutomaton((1,), 1, {1: action}, {(1, "g"): 1, (1, "b"): 1})
        one_state_automaton.append(automaton)

    return one_state_automaton


# 2状態の有限オートマトンを作成
def make_two_state_automaton() -> FiniteAutomaton:
    two_state_automaton = []
    state_signal_pair = [(1, "g"), (1, "b"), (2, "g"), (2, "b")]
    for action1, action2 in [('C', 'D'), ('D', 'C')]:
        action_function = {1: action1, 2: action2}
        for i in range(1 << 4):
            trasition_function = {}
            for j in range(4):
                if (i & (1 << j)):
                    trasition_function[state_signal_pair[j]] = 1
                else:
                    trasition_function[state_signal_pair[j]] = 2

            if trasition_function[(1, "g")] == 1 and trasition_function[(1, "b")] == 1:
                continue
            automaton = FiniteAutomaton((1, 2), 1, action_function, trasition_function)
            two_state_automaton.append(automaton)

    return two_state_automaton


# 3状態の有限オートマトンを作成
def make_three_state_automaton() -> FiniteAutomaton:
    three_state_automaton = []
    state_signal_pair = [(1, "g"), (1, "b"), (2, "g"), (2, "b"), (3, "g"), (3, "b")]
    transition_combinations = list(itertools.product([1, 2, 3], repeat=6))

    # ('C', 'C', 'D') or ('D', 'D', 'C') の場合
    for action1, action2, action3 in [('C', 'C', 'D'), ('D', 'D', 'C')]:
        action_function = {1: action1, 2: action2, 3: action3}
        for combination in transition_combinations:
            # 初期状態しか使わないものを除く
            if combination[0] == 1 and combination[1] == 1:
                continue
            # 状態1と状態2しか使わないものを除く
            elif 3 not in combination[:4]:
                continue
            # 状態1と状態3しか使わないものを除く
            elif 2 not in combination[:2] + combination[4:]:
                continue
            # 実質的に2状態と同じ動きをするものを除く
            elif action_function[combination[0]] == action_function[combination[2]] and \
                action_function[combination[1]] == action_function[combination[3]]:
                continue
            transition_function = {}
            for i in range(6):
                transition_function[state_signal_pair[i]] = combination[i]

            automaton = FiniteAutomaton((1, 2, 3), 1, action_function, transition_function)
            three_state_automaton.append(automaton)

    # ('C', 'D', 'D') or ('D', 'C', 'C') の場合
    for action1, action2, action3 in [('C', 'D', 'D'), ('D', 'C', 'C')]:
        action_function = {1: action1, 2: action2, 3: action3}
        for combination in transition_combinations:
            prohibited = [(1, 1), (1, 3), (3, 1), (3, 2), (3, 3)]
            # 初期状態しか使わないもの, 同じパターンのものを取り除く
            if (combination[0], combination[1]) in prohibited:
                continue
            # 状態1と状態2しか使わないものを除く
            elif 3 not in combination[:4]:
                continue
            # 状態1と状態3しか使わないものを除く
            elif 2 not in combination[:2] + combination[4:]:
                continue
            # 実質的に2状態と同じ動きをするものを除く
            elif action_function[combination[2]] == action_function[combination[4]] and \
                action_function[combination[3]] == action_function[combination[5]]:
                continue
            transition_function = {}
            for i in range(6):
                transition_function[state_signal_pair[i]] = combination[i]

            automaton = FiniteAutomaton((1, 2, 3), 1, action_function, transition_function)
            three_state_automaton.append(automaton)

    return three_state_automaton


# 3状態以下の有限オートマトンを作成
def make_automaton() -> FiniteAutomaton:
    automaton = []
    automaton.extend(make_one_state_automaton())
    # print(len(automaton))
    automaton.extend(make_two_state_automaton())
    # print(len(automaton))
    automaton.extend(make_three_state_automaton())
    # print(len(automaton))

    return automaton

# 積有限オートマトンを計算
def make_product_automaton(fa1: FiniteAutomaton, fa2: FiniteAutomaton) -> FiniteAutomaton:
    # 積オートマトンの状態集合を生成
    product_states = tuple([(s1, s2) for s1 in fa1.states for s2 in fa2.states])
    
    # 積オートマトンの初期状態を生成
    product_initial_state = (fa1.initial_state, fa2.initial_state)
    
    # 積オートマトンの行動決定関数を生成
    product_action_function = {(s1, s2): (fa1.action_function[s1], fa2.action_function[s2]) for (s1, s2) in product_states}
    
    # 積オートマトンの状態遷移関数を生成
    product_transition_function = {}
    for (s1, a1), next_s1 in fa1.transition_function.items():
        for (s2, a2), next_s2 in fa2.transition_function.items():
            product_transition_function[((s1, s2), (a1, a2))] = (next_s1, next_s2)

    # 積オートマトンを生成して返す
    return FiniteAutomaton(product_states, product_initial_state, product_action_function, product_transition_function)


# 2つのオートマトンが与えられたときに遷移を表す行列を返す
def transition_matrix(fa1: FiniteAutomaton, fa2: FiniteAutomaton, signals) -> list:
    fa1_action_function = fa1.action_function
    fa2_action_function = fa2.action_function
    
    product_fa = make_product_automaton(fa1, fa2)
    
    states = list(product_fa.states)
    transition_matrix = [[0 for _ in range(len(states))] for _ in range(len(states))]

    for row, state in enumerate(states):
        for signal_pair in [("g", "g"), ("g", "b"), ("b", "g"), ("b", "b")]:
            next_state = product_fa.transition_function[(state, signal_pair)]
            transition_matrix[row][states.index(next_state)] += signals[((fa1_action_function[state[0]], fa2_action_function[state[1]]), signal_pair)]

    return transition_matrix


# 2つのオートマトンが与えられたときに、2プレイヤーの利得を計算する
def calculate_payoff(fa1: FiniteAutomaton, fa2: FiniteAutomaton, signals, delta, payoff_table) -> float:
    """
    Args:
        fa1: FiniteAutomaton
        fa2: FiniteAutomaton
        signals: dict
        delta: float
        payoff_table: np.array

    Returns:
        payoff_1: float
    """

    product_automaton = make_product_automaton(fa1, fa2)
    
    # 遷移行列を計算
    transition = np.array(transition_matrix(fa1, fa2, signals))

    # 利得ベクトルを計算
    payoff_vector_1 = np.array([payoff_table[(fa1.action_function[state[0]], fa2.action_function[state[1]])] 
                                for state in product_automaton.states])
    payoff_vector_2 = np.array([payoff_table[(fa2.action_function[state[1]], fa1.action_function[state[0]])]
                                for state in product_automaton.states])
    
    # 単位行列 I を定義
    I = np.identity(len(product_automaton.states))
    
    # (I - δB) の逆行列を計算
    inv = np.linalg.inv(I - delta * transition)
    
    # X = (I - δB)^{-1} A を計算
    X_1 = np.dot(inv, payoff_vector_1)
    X_2 = np.dot(inv, payoff_vector_2)

    # 利得を計算
    # TODO: 初期状態に合わせて変更する
    payoff_1 = X_1[0]
    payoff_2 = X_2[0]
    
    return payoff_1, payoff_2
