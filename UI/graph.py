# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 13:27:40 2020

@author: Ricky
"""

import networkx as nx
import matplotlib.pyplot as plt
import time as t
import requests
import json

G = nx.Graph()

while(1):
    print()
    r = requests.get('http://localhost:8000/graph')
    print(r.json())
    
    dataJson = r.text
    data = json.loads(dataJson)
    
    print("Humans: ", data["nodes"])
    print("Safe distance: ", data["normalEdges"])
    print("Covid edges: ", data["covidEdges"])
    print()
    
    ############# Nodes
    nodes = []
    print("Nodes")
    for i in data["nodes"]:
        nodes.append(i)
        print(nodes)
    
    print()
    for i in nodes:
        G.add_node(i, node_size=600, color = 'green')
    #######################################    
    
    ############# Normal Edges
    print("Normal edges")
    for i in data["normalEdges"]:
        print(i)
        
    for i in data["normalEdges"]:
        G.add_edge(i[0],i[1], color = 'b')
    ####################################### 
      
    
    ############# Covid edges
    print("Covid edges")
    for i in data["covidEdges"]:
        print(i)
    
    for i in data["covidEdges"]:
        G.add_edge(i[0],i[1], color = 'r')
    ####################################### 
    
    
    print("\nAll edges:")
    print(G.edges())
    
    
    colors = nx.get_edge_attributes(G,'color').values()
    ncolors = nx.get_node_attributes(G, 'color').values()
    weights = nx.get_edge_attributes(G,'weight').values()
    
    
    nx.draw(G, with_labels = True, edge_color = colors, node_size = 600, node_color = ncolors)
    plt.show()
    t.sleep(10)


