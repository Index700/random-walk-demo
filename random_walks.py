import graph_tools
import sys
import random
import pathutil

# 遷移モデルの関数
# input:グラフg, 滞在ノード v, (その他)
# output: 遷移ノード u

def random_walk(g,v):
    # N : ノードvの隣接ノード集合
    N = g.neighbors(v)
    u = random.choice(N)        

    return u

def non_back_rw(g,v,p):
    # p: 前回に滞在したノード
    N = g.neighbors(v)
    # print(v,N,p)
    if len(N) == 1:
        return p
    N.remove(p)
    u = random.choice(N)
    return u


def coarsning_rw(g,v):
    # L 遷移候補ノード集合
    L = []
    N = g.neighbors(v)
    for n in N:
        # ノードvの隣接ノードの隣接ノードが候補ノード
        N_n = g.neighbors(n)
        L.extend(N_n)            
        while True:
            u = random.choice(L)
            if not u in N:
                break
    return n,u 


# 終了条件を返す
def hitting_time(v,t,end):
    # v: 訪問ノード
    # t: 目的ノード
    if v == t:
        end = False

    return end

def cover_time(v,V,end):
    # v: 訪問ノード
    # V: 未訪問ノード集合
    if v in V:
        V.remove(v)
    if len(V) == 0:
        end = False
    
    return end,V

def k_cover_time(v,V,k,end):
    # v: 訪問ノード
    # V: 未訪問ノード集合
    # k: 到達訪問数(ノード数 * pi)
    fin = int()
    if v in V:
        V.remove(v)
    if len(V) < k:
        end = False
    
    return end,V

def main():
    fname1, s  = sys.argv[1:3]    
    g = graph_tools.Graph(directed=False)
    g.import_dot(pathutil.Path(fname1).lines())

    v = int(s)
    P = [v]
    # P 訪問ノード集合

    # テストの変更はここから
    # for i in range(0,10):
    #    u = coarsning_rw(g,v)
    #    P.append(u)
    #    v = u

    end = True
    t = 10
    V = g.vertices().copy()
    k = int(len(g.vertices()) * 0.8)
    while end:
        u = random_walk(g,v)        
        end,V = k_cover_time(v,V,k,end)
        P.append(u)
        v = u
        print(len(V))
        
    # ここまで
    print(P)
    
if __name__ == "__main__":
    main()

            

