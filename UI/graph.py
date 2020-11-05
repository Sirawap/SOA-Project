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

plt.ion()
fig = plt.figure()
G = nx.Graph()

def run():
    while(1):
        #Getting data
        r = requests.get('http://localhost:8000/graph')
        #print(r.json())
        
        dataJson = r.text
        data = json.loads(dataJson)
        
        
        #Nodes, list of people
        nodes = []
        print("\nNodes")
        for i in data["nodes"]:
            nodes.append(i)
            print(nodes)
        
        for i in nodes:
            G.add_node(i, node_size=600, color = 'green')
        #######################################    
        
        #Normal Edges, contact with people at safe distance
        print("\nNormal edges")
        for i in data["normalEdges"]:
            print(i)
            
        for i in data["normalEdges"]:
            G.add_edge(i[0],i[1], color = 'b')
        ####################################### 
          
        
        #Covid edges, contact with people at unsafe distance
        print("\nCovid edges")
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
        plt.clf()
        fig.canvas.draw()
        t.sleep(5)
    
        print("-----------------------------\n")
            

if __name__ == "__main__":
    run()


