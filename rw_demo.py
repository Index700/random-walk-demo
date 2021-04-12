#!/usr/bin/env python3

import fileinput
import itertools
import random
from collections import defaultdict

import graph_tools
from perlcompat import getopts, warn

import random_walks as rw

# p = 0.2  # influence propagation probability
# K = 20   # the number of seed nodes
# M = 50  # the number of sampled nodes

move1 = "0.1 0.1 0.8"
move2 = "0.1 0.8 0.1"
move3 = "0.8 0.1 0.1"

def change_color_node(g,v,model):
    d_w = g.get_vertex_weight(v)
    d_w = d_w + 0.1
    g.set_vertex_weight(v,d_w)
    print(f"color v{v} {model} {d_w}")

    return 0

def change_color_edge(g,u,v,model,t):
    e_w = g.get_edge_weight(u,v)
    e_w += 0.1
    g.set_edge_weight(u,v,e_w)
    print(f"palette c{u}{v}-{t} {model} {e_w}")
    print(f"color e{u}-{v} c{u}{v}-{t}")

    return 0

def main():
    opt = getopts('t:')
    T = int(opt.t) if opt.t else 100

    g = graph_tools.Graph(directed=False)
    g.import_dot(list(fileinput.input()))
    print("palette node 0.2 0.2 0.2 0.2")
    print("palette edge 0.2 0.2 0.2 0.2")
    print("palette move1 0.1 0.1 0.8 0.2")
    print("palette move2 0.1 0.8 0.1 0.2")
    print("palette move3 0.8 0.1 0.1 0.2")
    
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


    # # nonback rw
    v = random.choice(V)
    u = rw.random_walk(g,v)
    print(f"color v{v} red")
    t = 0
    while t < int(T):
        u = rw.non_back_rw(g,v,u)
        print(f"color v{u} white")
        for w in g.neighbors(u):
            U = sorted([w,u])
            print(f"color v{w} move1")
            change_color_edge(g,U[0],U[1],move1,t)
        tmp = v
        v = u
        u = tmp
        t = t + 1
        print("display")
        print("kill /i./")

    # # coarsening rw
    # v = random.choice(V)
    # t = 0
    # while t < int(T) / 2:
    #     n,u = rw.coarsning_rw(g,v)
    #     print(f"color v{u} white")
    #     print(f"color v{n} white")
    #     for w in g.neighbors(n):
    #         U = sorted([w,n])
    #         print(f"color v{w} move3")
    #         change_color_edge(g,U[0],U[1],move3,t)

    #     for w in g.neighbors(u):
    #         U = sorted([w,u])
    #         print(f"color v{w} move3")
    #         change_color_edge(g,U[0],U[1],move3,t)

    #     tmp = v
    #     v = u
    #     u = tmp
    #     t = t + 1
        
    #     print("display")
    #     print("kill /i./")
    #     print(f"color v{n} move3")
    #     print(f"color v{u} move3")
    # print(f"color v{n} white")


    # # # # rw
    t = 0
    v = random.choice(V)
    
    # while t < int(T):
    #     u = rw.random_walk(g,v)
    #     print(f"color v{u} white")
    #     for w in g.neighbors(u):
    #         U = sorted([w,u])
    #         print(f"color v{w} move2")
    #         change_color_edge(g,U[0],U[1],move3,t)
    #     v = u
    #     t = t + 1
    #     print("display")
    #     print("kill /i./")

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
