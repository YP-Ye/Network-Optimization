# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 19:39:12 2016

@author: YeYipeng
"""

####该函数用于确定有向图中路段-路径关系以及路径-OD关系
####ODs是OD起始点标号，edges是路段起始点标号
####该函数借用networkx工具包生成路径并标号
####进而生成link-path关系矩阵与path-OD关系矩阵

def incidence_matrix_generation(edges,ODs):
    import networkx as nx
    #表示有向图
    G=nx.DiGraph()
    routes = {}
    #给OD标号
    OD_indexs = {}
    index = 1
    for OD in ODs:
        OD_indexs[index] = list(OD)
        index = index + 1
#给路段标号
    edge_indexs = {}
    index = 1
    for edge in edges:
        edge_indexs[index] = list(edge)
        index = index + 1

#给网络增加路段
    for edge in edges:
        G.add_edge(edge[0],edge[1])
#枚举路径
    for (i,j) in ODs:
        paths = nx.all_simple_paths(G,source=i,target=j)
        routes[i,j] = list(paths)

#给路径标号
    route_indexs = {}
    index = 1
    for (i,j) in ODs:
        k = 0
        while k <= len(routes[i,j]) - 1:
            route_indexs[index] = routes[i,j][k]
            index = index + 1
            k = k + 1

#分解路径为路段 之后判断路段是否属于该路径
    route_indexs_decompose = {}
    for index in route_indexs:
        route_indexs_decompose[index] = []
        k = 1
        while k <= len(route_indexs[index]) - 1:
            route_indexs_decompose[index].append([route_indexs[index][k-1],route_indexs[index][k]])
            k = k + 1
#确定路段路径关系
    delta_a_k = {}
    a = 1
    while a <= len(edge_indexs):
        k = 1
        while k <= len(route_indexs_decompose):
            if edge_indexs[a] in route_indexs_decompose[k]:
                delta_a_k[a,k] = 1
            else:
                delta_a_k[a,k] = 0
            k = k + 1
        a = a + 1
#确定路径与OD关系
    delta_k_rs = {}
    k = 1
    while k <= len(route_indexs):
        rs = 1
        while rs <= len(OD_indexs):
            if route_indexs[k][0] == OD_indexs[rs][0] and route_indexs[k][len(route_indexs[k])-1] == OD_indexs[rs][len(OD_indexs[rs])-1]:
                delta_k_rs[k,rs] = 1
            else:
                delta_k_rs[k,rs] = 0
            rs = rs + 1
        k = k + 1
#给路段标号
    edgeindex = []
    i = 1
    while i <= len(edge_indexs):
        edgeindex.append(i)
        i = i + 1
#给路径标号
    routeindex = []
    i = 1
    while i <= len(route_indexs):
        routeindex.append(i)
        i = i + 1
#给OD标号
    ODindex = []
    i = 1
    while i <= len(OD_indexs):
        ODindex.append(i)
        i = i + 1

    return(delta_a_k,delta_k_rs,edgeindex,routeindex,ODindex)


