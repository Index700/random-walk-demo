#!/usr/bin/env python3

import fileinput
import itertools
import random
from collections import defaultdict
import crw

import graph_tools
from perlcompat import getopts, warn

import random_walks as rw
import crw

# p = 0.2  # influence propagation probability
# K = 20   # the number of seed nodes
# M = 50  # the number of sampled nodes

move1 = "0.5 0.4 0.8"
move2 = "0.1 0.8 0.1"
move3 = "0.8 0.1 0.1"

def change_color_node(g,v,model,t):
    d_w = g.get_vertex_weight(v)
    d_w = d_w + 0.05
    g.set_vertex_weight(v,d_w)
    print(f"priority v{v} 3")
    print(f"palette c{v}-{t} {model} {d_w}")
    print(f"color v{v} c{v}-{t}")

    return 0

def change_color_edge(g,u,v,model,t):
    e_w = g.get_edge_weight(u,v)
    e_w += 0.05
    g.set_edge_weight(u,v,e_w)
    print(f"priority e{u}-{v} 3")
    print(f"palette c{u}{v}-{t} {model} {e_w}")
    print(f"color e{u}-{v} c{u}{v}-{t}")
    return 0

def main():
    opt = getopts('t:k:')
    T = int(opt.t) if opt.t else 100
    k = int(opt.k) if opt.k else 1

    g = graph_tools.Graph(directed=False)
    g.import_dot(list(fileinput.input()))
    print("palette node 0.2 0.2 0.2 0.8")
    print("palette edge 0.2 0.2 0.2 0.8")
    print(f"palette move1 {move1} 0.8")
    print(f"palette move2 {move2} 0.8")
    print(f"palette move3 {move3} 0.8")
    
    # # random sampling
    # V = random.sample(g.vertices(), M)

    # # choose K seed nodes from randomly-sampled nodes
    # V = sorted(V, key=lambda v: g.degree(v), reverse=True)
    # A[0] = V[:K]

    # dump graph
    for v in g.vertices():
        print(f"define v{v} ellipse 5 5 node")
        g.set_vertex_weight(v,0.2)
    for e in g.edges():
        print(f"define e{e[0]}-{e[1]} link v{e[0]} v{e[1]} 1 edge")
        g.set_edge_weight(e[0],e[1],0.2)
    print("spring /./")
    print("display")
    print("wait")
    V = g.vertices()

    # # # # rw
    t = 0
    v = random.choice(V)

    print(f"define model text -l RW 15 move3 20 50")
    
    while t < int(T):
        u = rw.random_walk(g,v)
        print(f"color v{u} white")
        U = sorted([v,u])
        change_color_node(g,u,move2,t)
        change_color_edge(g,U[0],U[1],move2,t)
        v = u
        t = t + 1
        print(f"define step text steps:__{t} 10 white 50 580")
        print("display")
        print("kill /i./")

    # # # # nonback rw
    # v = random.choice(V)
    # u = rw.random_walk(g,v)
    # print(f"color v{v} red")
    # t = 0
    # print(f"define model text -l Self__avoiding__RW: 15 move1 20 20")
    # while t < int(T):
    #     u = rw.non_back_rw(g,v,u)
    #     print(f"color v{u} white")
    #     U = sorted([v,u])
    #     change_color_node(g,u,move1,t)
    #     change_color_edge(g,U[0],U[1],move1,t)

    #     # for w in g.neighbors(u):
    #     #     U = sorted([w,u])
    #     #     print(f"color v{w} move2")
    #     #     change_color_edge(g,U[0],U[1],move2,t)
    #     tmp = v
    #     v = u
    #     u = tmp
    #     t = t + 1
    #     print(f"define step text steps:__{t} 10 white 50 580")
    #     print("display")
    #     print("kill /i./")

    # coarsening rw
    # s = random.choice(V)
    # t = 0
    # v = s
    # L = [s]
    # print(f"color v{v} red")    
    # while t < int(T):
    #     p = v
    #     v,L = crw.k_crw(g,v,L,k)
    #     t += 1
    #     change_color_node(g,v,move3,t)
    #     U = sorted([v,p])
    #     change_color_edge(g,U[0],U[1],move3,t)
    #     # for w in g.neighbors(u):
    #     #     U = sorted([w,u])
    #     #     print(f"color v{w} move3")
    #     #     change_color_edge(g,U[0],U[1],move3,t)
        
    #     print("display")
    #     print("kill /i./")
    #     # print("wait")
            
            

    # print(f"color v{v} white")



    # x = random.choice(V)
    # print(f"color v{x} red")
    # end=True
    # while end:
    #     u = rw.random_walk(g,v)
    #     print(f"color v{u} white")
    #     for w in g.neighbors(u):
    #         U = sorted([w,u])
    #         print(f"color v{w} move2")
    #         change_color_edge(g,U[0],U[1],move3,t)
    #         if w == x:
    #             end=False
    #     v = u
    #     t = t + 1
    #     print("display")
    #     print("kill /i./")

    print("display")
    print("wait")

if __name__ == "__main__":
    main()
