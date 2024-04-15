from queue import PriorityQueue
from utils import FindPath
from UpperClasses import Problem

def UniformCostSearch(P: Problem):
    """Implementation of the Uniform Cost Search"""
    # Initialization
    distance = {}
    predecessor = {}
    Q = PriorityQueue()
    source = P.initialState()
    distance[source] = 0.0
    #an element in the priority queue is the accumulated probability t and the state u
    Q.put((0, source))
    visited_states = 0
    max_size_queue = 0
    while not Q.empty():
        visited_states += 1
        (t, u) = Q.get()
        if P.isGoal(u):
            print(f"Found the goal state after visiting {visited_states} states, its log-probability is {t}. The queue ended with {Q.qsize()} elements and its maximum size was {max_size_queue}.") 
            return FindPath(predecessor, source, u)
        for a in P.actions(u):
            v = P.result(u,a)
            alt = t + P.cost(u,a,v)
            if v not in distance or alt < distance[v]: 
                distance[v] = alt
                predecessor[v] = (u,a) 
                Q.put((alt,v))
        max_size_queue = max(max_size_queue, Q.qsize())
    return None #Não chegou em lugar nenhum


def LimitedDepthSearch(P: Problem, max_depth: int, initialState, return_value=False):
    """
    DFS bounded by the depth parameter. The priority in this search is set by the state's depth and ties are decided by the state's probabilities.
    Depending on return_value, this function either returns the path [if false] or the value from initialState to a goal [if true].
    """
    distance = {}
    predecessor = {}
    Q = PriorityQueue()
    source = initialState
    distance[source] = 0.0
    #an state is an the inverse of the depth [counting from depth to 0], the probability t of the state, the depth d, the state u, and the accumulated probability
    Q.put((max_depth, 0, 0, source, 0))
    visited_states = 0
    best_probability = 10000
    max_size_queue = -1
    while not Q.empty():
        (inverse_depth, t, d, u, accumulated_probability) = Q.get()
        visited_states += 1
        if P.isGoal(u):
            print(f"Found the goal state after visiting {visited_states} states, its log-probability is {accumulated_probability}. The queue ended with {Q.qsize()} elements and its maximum size was {max_size_queue}.")
            if not return_value:
                return FindPath(predecessor, source, u)
            else:
                return accumulated_probability
        else:
            if d == max_depth:
                if accumulated_probability < best_probability: #Found a better solution at the max depth
                    best_probability = accumulated_probability
            else:
                for a in P.actions(u):
                    v = P.result(u,a)
                    alt = d + 1
                    current_cost = P.cost(u, a, v)
                    total_cost = accumulated_probability + current_cost
                    if v not in distance or alt < distance[v]: # found improving path to v
                        distance[v] = alt
                        predecessor[v] = (u,a) # so that we can backtrack to source
                        Q.put( (inverse_depth-1, current_cost, alt, v, total_cost )  )
        max_size_queue = max(max_size_queue, Q.qsize())
    if not return_value:
        return None # Failure: Could not reach target
    else:
        return best_probability

def BeamSearch(P: Problem, Beam: int):
    """Runs the Beam Search always keeping Beam elements.  """
    # Initialization
    Q = []
    solutions = []
    source = P.initialState()
    #an element in queue is accumulated probability t, perplexity p, the state u, u's predecessors h.
    Q.append( (0, 0, source, [source]) )
    iteration = 0
    while len(solutions) < Beam:
        iteration += 1
        aux_list = []
        for (t, p, u, h) in Q: #2
            for a in P.actions(u):
                v = P.result(u,a)
                alt = t + P.cost(u, a, v)
                new_per = alt / (len(h) + 1)
                new_history = h + [v]
                aux_list.append( (alt, new_per, v, new_history) ) 
        aux_list.sort()
        aux_list = aux_list[:Beam]
        for (t, p, u, h) in aux_list:
            if P.isGoal(u):
                print(f"One goal found, there are {Beam-len(solutions)-1} left")
                solutions.append([h, t, p])
                aux_list.remove( (t, p, u, h) )
        if iteration %10 == 0:
            print("Iteracao ", iteration)
        if iteration == 30:
            break
        Q = aux_list
    return solutions

def run_search(search_name: str, model: Problem, *params):
    if search_name == "UniformCost":
        S = UniformCostSearch(model)
    elif search_name ==  "LimitedDepthSearch":
        S = LimitedDepthSearch(model, params[0], model.initialState(), return_value=False)
    elif search_name ==  "BeamSearch":
         S = BeamSearch(model, params[0])
    else:
        print(f"The word {search_name} does not match any implemented search.")
        S = None
    if S is not None:
        S = list(S)
    return S



