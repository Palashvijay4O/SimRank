#!/usr/bin/env python

import itertools
import numpy
import logging
import argparse
import networkx as nx
import multiprocessing as mp
import traceback
import ctypes
import json
import sqlite3
import copy
import sys
from collections import defaultdict



le=[]


def simrank(G, flag,c=0.8, iterations=3):
  # Used to maintain the count of top 20 pairs of research papers which
  # are most similiar and their simranks.
  max_list=[]

  for i in xrange(20):
    max_list.append((-1,-1,0))
  
  # Initialize the sim and sim_old dictionaries with default values.
  sim_old = defaultdict(list)
  sim = defaultdict(list)
  for n in G.nodes():
    sim[n] = defaultdict(int)
    sim[n][n] = 1
    sim_old[n] = defaultdict(int)
    sim_old[n][n] = 1 
  
  

  for iter_ctr in range(iterations):
    sim_old = copy.deepcopy(sim)
    for v in G.nodes():
        l=[]
        '''  
        for n_u in G.successors(v):
                l.append(n_u)
   
        for n_u in G.successors(v):
            for n_x in G.successors(n_u):
                l.append(n_x)
        '''
        ### DEPTH 3
        for n_u in G.successors(v):
            l.append(n_u)
            for n_x in G.successors(n_u):
               l.append(n_x)
               for t in G.successors(n_x):  
                  l.append(t) 

        '''
        for n_u in G.successors(v):
            l.append(n_u)
            for n_x in G.predecessors(n_u):
               l.append(n_x)
               for t in G.successors(n_x):  
                  l.append(t)

        for n_u in G.successors(v):
            l.append(n_u)
            for n_x in G.successors(n_u):
               l.append(n_x)
               for t in G.predecessors(n_x):  
                  l.append(t)

        for n_u in G.successors(v):
            l.append(n_u)
            for n_x in G.predecessors(n_u):
               l.append(n_x)
               for t in G.predecessors(n_x):  
                  l.append(t)         
        '''
        '''
        for n_u in G.predecessors(v):
                l.append(n_u)
   
        for n_u in G.predecessors(v):
            for n_x in G.predecessors(n_u):
                l.append(n_x)
        '''
        for n_u in G.predecessors(v):
            l.append(n_u)
            for n_x in G.predecessors(n_u):
               l.append(n_x)
               for t in G.predecessors(n_x):  
                  l.append(t) 
        '''
        for n_u in G.predecessors(v):
            l.append(n_u)
            for n_x in G.successors(n_u):
               l.append(n_x)
               for t in G.predecessors(n_x):  
                  l.append(t) 

        for n_u in G.predecessors(v):
            l.append(n_u)
            for n_x in G.predecessors(n_u):
               l.append(n_x)
               for t in G.successors(n_x):  
                  l.append(t)
        for n_u in G.predecessors(v):
            l.append(n_u)
            for n_x in G.successors(n_u):
               l.append(n_x)
               for t in G.successors(n_x):  
                  l.append(t)  
        
        '''
        '''
        le = nx.algorithms.traversal.depth_first_search.dfs_predecessors(G,v)
        ke = nx.algorithms.traversal.depth_first_search.dfs_successors(G,v)
        ne = list(le.keys())
        se = list(ke.keys())
        ze = ne + se
        '''
        neighbors = list(set(l))
        for i in neighbors:
            if v == i :
               sim[v][i]=1
            else:   
              s_uv = 0.0
              for n_u in G.predecessors(v):
                  for n_v in G.predecessors(i):
                      s_uv += sim_old[n_u][n_v]
              if len(G.predecessors(i)) * len(G.predecessors(v)) > 0:     
                  sim[v][i] = (c * s_uv / (len(G.predecessors(v)) * len(G.predecessors(i))))
                  if sim[v][i] > max_list[0][2] and sim[v][i] != 1 and iter_ctr==iterations-1:
                    if(v>i):
                      max_list[0]=(v,i,sim[v][i]) 
                      max_list = sorted(max_list,key=lambda v:v[2])
              else:
  		sim[v][i]=0
  if flag == 0:
    print sorted(list(set(max_list)),key=lambda j:j[2])

  return sim

def dfs_back(G,h,node,l1):

  if h == 0:
     return l1  
  for i in G.predecessors(node):
      l1.append(i)
      dfs(G,h-1,i,l1)
  


def dfs_front(G,h,node,l2):
  #print "a"
  if h == 0:
     return l2
  for i in G.neighbors(node):
      l2.append(i)
      dfsa(G,h-1,i,l2)



if __name__ == '__main__':
  arguments = sys.argv[1:]
  #print arguments
  symbol = int(arguments[0])
  conn = sqlite3.connect('Paper_db')
  connection = conn.cursor()
  row_of_row=[]
 
  for row in connection.execute("SELECT ref_id,ref_num FROM papers limit '%s'" % symbol):
  	y=[]
  	y.append(str(row[0]))
  	y.append(row[1])
  	row_of_row.append(y)
  	#print str(row)
  #print x
  l=[]
  temp=''
  node=0
  for i in row_of_row:
  	for j in i[0]:
  		if j != ';':
  		   temp=temp+j
  		else:
  		   tup=(int(temp),node)
  		   l.append(tup)		
  		   temp=''
  	if temp !='':
  	   l.append((int(temp),node))
  	   temp=''	   
  	node=node+1
  #print l
  G=nx.DiGraph()
  G.add_edges_from(l)
  #s = simrank(G)
  mylist = list(xrange(symbol)) 
  G.add_nodes_from(mylist)

  #G.add_edges_from(l)
  #l=[(1,2),(2,3),(1,3)]
  #G.add_edges_from(l)
  #G = nx.DiGraph()
  #G.add_edges_from([('a','b'), ('b','c'), ('a','c'), ('c','d'),('b','d')])
  if arguments[1] == '0':
    flag = 0
    s = simrank(G,0)
  elif arguments[1] == '1' and len(arguments) == 4:
    flag = 1
    s = simrank(G,1)
    print s[int(arguments[2])][int(arguments[3])]


    '''
    for i in range(symbol):
       for j in range(symbol):
           if s[i][j] > 0 and s[i][j]!=1:
             temp= []
             temp.append(s[i][j])
             temp.append((i,j))
             print temp
    '''

#print sorted(list(set(max_list)),key=lambda j:j[2])


