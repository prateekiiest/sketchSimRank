import numpy as np
from Similarity import Similarity
from utilities.GraphUtility import hash_graph, init_graph
import plotly.express as px
import pandas as pd
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.io as pio
from sklearn.metrics import jaccard_score


def SimRank_one_iter_approx(nodeList, sim, cur_count):
    for node1 in nodeList:
        for node2 in nodeList:
            new_SimRank = sim.calculate_simrank_approximate(
                node1, node2, cur_count)
            sim.update_sim_value_approx(node1, node2, new_SimRank)

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


def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(set(list1)) + len(set(list2))) - intersection
    return float(intersection) / union

def jaccard(nodeList, graph, sim, cur_count):
    jacDic = dict()
    for node in nodeList:
        for nodegraph in graph.nodes:
            if int(nodegraph.name) == node:
                jacDic[node] = jaccard_similarity(sim.compute_approximate_neighbors(
                    node, cur_count), [int(i.name) for i in nodegraph.parents])
                
    return jacDic


if __name__ == '__main__':

    decay_factor = 0.9
    iteration = 100

    num_buckets = [80, 100, 120, 180]
    count_current = []
    count_original_current = []
    nodeL = []
    for num_bucket in num_buckets:
        graph = init_graph('graph-2.txt')
        cur_count, nodeList = hash_graph('graph-2.txt', num_bucket)
        sim = Similarity(graph, decay_factor)

        sim2 = Similarity(graph, decay_factor)

        SimRank(graph, sim, iteration)
        ans = sim.get_sim_matrix()
        #print('True simrank', ans)

        SimRankApprox(nodeList, sim2, cur_count, iteration)
        ans2 = sim2.get_sim_matrix()
        #print('Approx simrank ', ans2)

        print(np.linalg.norm(np.subtract(ans, ans2)))

        '''
        for node in graph.nodes:
            print(node.name, len(node.parents), [nodep.name for nodep in node.parents])

        print('Approx simrank neighbors\n ')
        for node in nodeList:
            print(node, len(sim2.compute_approximate_neighbors(node, cur_count)), sim2.compute_approximate_neighbors(node, cur_count))
    
        print(len(graph.nodes))
        print(len(nodeList))
        '''
        count_current.append(jaccard(nodeList, graph, sim2, cur_count))

    #df = pd.DataFrame({'node': nodeL, 'count_80': count_current[0], 'countOriginal_80': count_original_current[0], 'count_100': count_current[1], 'countOriginal_100': count_original_current[1],
     #                 'count_120': count_current[2], 'countOriginal_120': count_original_current[2], 'count_140': count_current[3], 'countOriginal_140': count_original_current[3]})
    
    df2 = pd.DataFrame({'node': list(count_current[0].keys()), 'count_80': list(count_current[0].values()), 'count_100': list(count_current[1].values()),'count_120': list(count_current[1].values()),'count_180': list(count_current[1].values())})
    
      
    pd.options.plotting.backend = "plotly"
    fig = df2.plot.bar(x='node', y=['count_80', 'count_180'], barmode='group', title='Jaccard index of approximate estimate of inlinks w.r.t original inlinks for w= 80 and w=180')
    plot(fig)
    # plot(fig2)
    #pio.write_image(fig, 'errorMatchInlinks.svg', width=1000, height=575)
