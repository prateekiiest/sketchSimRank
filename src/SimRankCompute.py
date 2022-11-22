import numpy as np
from Similarity import Similarity
from utilities.GraphUtility import hash_graph, init_graph


def SimRank_one_iter_approx(nodeList, sim, cur_count):
    for node1 in nodeList:
        for node2 in nodeList:
            new_SimRank = sim.calculate_simrank_approximate(
                node1, node2, cur_count)
            sim.update_sim_value_approx(node1, node2, new_SimRank)
            # print(node1.label, node2.label, new_SimRank)


    sim.replace_sim()


def SimRank_one_iter(graph, sim):
    for node1 in graph.nodes:
        for node2 in graph.nodes:
            new_SimRank = sim.calculate_SimRank(node1, node2)
            sim.update_sim_value(node1, node2, new_SimRank)
            # print(node1.label, node2.label, new_SimRank)

    sim.replace_sim()


def SimRankApprox(nodeList, sim, cur_count, iteration=100):
    for i in range(iteration):
        SimRank_one_iter_approx(nodeList, sim, cur_count)
        # ans = sim.get_sim_matrix()
        # print(ans)
        # print()


def SimRank(graph, sim, iteration=100):
    for i in range(iteration):
        SimRank_one_iter(graph, sim)
        # ans = sim.get_sim_matrix()
        # print(ans)
        # print()


if __name__ == '__main__':

    decay_factor = 0.9
    iteration = 100

    graph = init_graph('graph.txt')
    cur_count, nodeList = hash_graph('graph.txt')
    sim = Similarity(graph, decay_factor)

    sim2 = Similarity(graph, decay_factor)

    SimRank(graph, sim, iteration)
    ans = sim.get_sim_matrix()
    print('True simrank', ans)

    SimRankApprox(nodeList, sim2, cur_count, iteration)
    ans2 = sim2.get_sim_matrix()
    print('Approx simrank ', ans2)


    print(np.linalg.norm(np.subtract(ans, ans2)))
    
    '''
 
    for node in graph.nodes:
        print(node.name, len(node.parents), [nodep.name for nodep in node.parents])

    print('Approx simrank neighbors\n ')
    for node in nodeList:
        print(node, len(sim2.compute_approximate_neighbors(node, cur_count)), sim2.compute_approximate_neighbors(node, cur_count))
    '''
  
    #print(len(graph.nodes))
    #print(len(nodeList))