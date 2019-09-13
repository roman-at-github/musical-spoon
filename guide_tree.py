# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 13:57:44 2019

@author: Christopher
"""

import numpy as np
from vertex import Vertex
from edge import Edge
from graph import Graph
from bronk_pivot import find_mcis_without_prompt

class guide_tree:
    
    
    def call_subgraph_algorithm(self, g1, g2):
        
        #This is a placeholder right now, but this function handles the pipeline to the 
        #actual alignment algorithms later on.
        return find_mcis_without_prompt(g1, g2)
    
    
    def score_similarity(self, g1, g2):
        #This will of course need to be reworked to include a function to judge the relative
        #similarityof two graphs...
        return (len(g1.edges) - len(g2.edges))
    
    def __init__(self, graph_list: [] = None):
        
        newick = []
        score_matrix = []
        for n in range(0, len(graph_list)):
            vec = []
            score_matrix.append(vec) #just make enough entries in the matrix
            for b in range(0, len(graph_list)):
                if n != b:
                    score_matrix[n].append(self.score_similarity(graph_list[n], graph_list[b]))
                    
                else:
                    score_matrix[n].append(999)
        #---------------------------------------------------          
        pairs = []
        hold_last = None

        for n in range(0, len(score_matrix)):
            minimal = 999
            minimal_pos = []
            if graph_list[n] != None:
                X = 0
                if len(pairs) * 2 + 1 == len(graph_list):
                    hold_last = graph_list[n]
                    
                #Just a cleanup, in case we have an uneven number ...

                for x in range(0, len(score_matrix[n])):
                    if score_matrix[n][x] < minimal and graph_list[x] != None:
                        minimal = score_matrix[n][x]
                        minimal_pos = []
                        minimal_pos.append(graph_list[n])
                        minimal_pos.append(graph_list[x])
                        X = x
                pairs.append((minimal_pos))
                graph_list[X] = None
                
        #Just a cleanup, in case we have an uneven number ...
        l = len(pairs)

        while l > 1 or hold_last != None:
            tmp = []
            for n in range(0, len(pairs)):
                tmp.append(self.call_subgraph_algorithm(pairs[n][0], pairs[n][1]))
                newick.append([pairs[n][0], pairs[n][1]])
            pairs = []
            
            #The following handles the situation of an uneven number of inputs - the remainder gets prioritized 
            #and aligned with one of the already induced subgraphs
            if hold_last != None:
                m = 999
                for n in range(0, len(tmp)):
                    hold_similarity = self.score_similarity(tmp[n], hold_last)
                    print(str(hold_similarity))
                    if  hold_similarity < m:
                            m = hold_similarity
                            m_hold_index = n
                        
                tmp[m_hold_index] = self.call_subgraph_algorithm(tmp[m_hold_index], hold_last)
                hold_last = None
            
            if len(tmp) == 1:
                pairs = tmp
                break
            #Basically we have to find the next two best pairs and repeat this ad infinium until our tree is done
            for n in range(0, len(tmp)):
                m_hold = tmp[n]
                m = 999
                for b in range(n, len(tmp)):
                    if tmp[b] != None:
                        hold_similarity = self.score_similarity(tmp[n], tmp[b])
                        if  hold_similarity < m:
                            m = hold_similarity
                            m_hold = tmp[b]
                
                if m_hold != tmp[n]:
                    pairs.append([tmp[n], m_hold])
                else:
                    hold_last = m_hold
            
            l = len(pairs)
                
        self.result = self.call_subgraph_algorithm(pairs[0][0], pairs[0][1])

        #-------------------------------------------------
    
    #The following section is incomplete, as there is currently no working way to parse this mess
    #into Newick format.    
        
    def create_Newick(self):
        return ""

def count_input(string):
    s = string.replace(')', '')
    s = s.replace('(','')
    s_cut = s.split(',')
    return len(s_cut)    

#The following function just aligns given list of preordered graphs in linear fashion.
def traverse_linear_tree(ordered_graphs):
        
    tmp = []
    for n in range(0, len(ordered_graphs)):
        tmp = guide_tree.call_subgraph_algorithm(tmp, ordered_graphs[n])
        
    return tmp
        