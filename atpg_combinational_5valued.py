#!/usr/bin/env python
# This is just a new statement really
import matplotlib.pyplot as plt
import networkx as nx
from collections import OrderedDict

class MyOrderedDict(OrderedDict):
    def last(self):
        return list(self.items())[-1]
    def lastbutone(self):
        return list(self.items())[-2]

def output_val(val_non_faulty, val_faulty):
    return{
           '00':'0',
           '01':'D',
           '0x':'x',
           '10':'D_bar',
           '11':'1',
           '1x':'x',
           'x0':'x',
           'x1':'x',
           'xx':'x',
           
           }[val_non_faulty + val_faulty]
    

"This funtion is to calculate outputs of a gate out_node based on current values of its input. Returns output value"
def calc_output(G, out_node):
    def or_three_valued(a, b):
        return{
         '00': '0',
         '01': '1',
         '0x': 'x',
         '10': '1',
         '11': '1',
         '1x': '1',
         'x0': 'x',
         'x1': '1',
         'xx': 'x',
         }[a + b]
    
    def and_three_valued(a, b):
        return{
         '00': '0',
         '01': '0',
         '0x': '0',
         '10': '0',
         '11': '1',
         '1x': 'x',
         'x0': '0',
         'x1': 'x',
         'xx': 'x',
         }[a + b]
    
    def not_three_valued(a):
        return{
         '0': '1',
         '1': '0',
         'x': 'x',
         }[a]
    
    def nand_three_valued(a, b):
        return not_three_valued(and_three_valued(a, b))
        
    def nor_three_valued(a, b):
        return not_three_valued(or_three_valued(a, b))
    
    def xor_three_valued(a, b):
        return or_three_valued(and_three_valued(a, not_three_valued(b)), and_three_valued(b, not_three_valued(a)))
    
    def xnor_three_valued(a, b):
        return not_three_valued(xor_three_valued(a, b))
    
    def non_faulty(a):
        return{
               '0':'0',
               '1':'1',
               'x':'x',
               'D':'0',
               'D_bar':'1'
               }[a]
               
    def faulty(a):
        return{
               '0':'0',
               '1':'1',
               'x':'x',
               'D':'1',
               'D_bar':'0'
               }[a]
    def and_gate(a, b):
        a_non_faulty = non_faulty(a)
        b_non_faulty = non_faulty(a)
        val_non_faulty = and_three_valued(a_non_faulty, b_non_faulty)
        a_faulty = faulty(a)
        b_faulty = faulty(b)
        val_faulty = and_three_valued(a_faulty, b_faulty)
        return output_val(val_non_faulty, val_faulty)
    
    def or_gate(a, b):
        a_non_faulty = non_faulty(a)
        b_non_faulty = non_faulty(a)
        val_non_faulty = or_three_valued(a_non_faulty, b_non_faulty)
        a_faulty = faulty(a)
        b_faulty = faulty(b)
        val_faulty = or_three_valued(a_faulty, b_faulty)
        return output_val(val_non_faulty, val_faulty)
    
    def nand_gate(a, b):
        a_non_faulty = non_faulty(a)
        b_non_faulty = non_faulty(a)
        val_non_faulty = nand_three_valued(a_non_faulty, b_non_faulty)
        a_faulty = faulty(a)
        b_faulty = faulty(b)
        val_faulty = nand_three_valued(a_faulty, b_faulty)
        return output_val(val_non_faulty, val_faulty)
    
    def nor_gate(a, b):
        a_non_faulty = non_faulty(a)
        b_non_faulty = non_faulty(a)
        val_non_faulty = nor_three_valued(a_non_faulty, b_non_faulty)
        a_faulty = faulty(a)
        b_faulty = faulty(b)
        val_faulty = nor_three_valued(a_faulty, b_faulty)
        return output_val(val_non_faulty, val_faulty)
    
    def xor_gate(a, b):
        a_non_faulty = non_faulty(a)
        b_non_faulty = non_faulty(a)
        val_non_faulty = xor_three_valued(a_non_faulty, b_non_faulty)
        a_faulty = faulty(a)
        b_faulty = faulty(b)
        val_faulty = xor_three_valued(a_faulty, b_faulty)
        return output_val(val_non_faulty, val_faulty)
    
    def xnor_gate(a, b):
        a_non_faulty = non_faulty(a)
        b_non_faulty = non_faulty(a)
        val_non_faulty = xnor_three_valued(a_non_faulty, b_non_faulty)
        a_faulty = faulty(a)
        b_faulty = faulty(b)
        val_faulty = xnor_three_valued(a_faulty, b_faulty)
        return output_val(val_non_faulty, val_faulty)
    
    def not_gate(a):
        a_non_faulty = non_faulty(a)
        val_non_faulty = not_three_valued(a_non_faulty)
        a_faulty = faulty(a)
        val_faulty = not_three_valued(a_faulty)
        return output_val(val_non_faulty, val_faulty)

    gate_type = out_node[1]['gatetype']
    in_edge_list = G.in_edges(out_node[0], data=True)
    first_edge = in_edge_list[0]
    val = first_edge[2]['value']
    if(gate_type == 'not'):
        val = not_gate(val)
    for i in range (1, len(in_edge_list)):
        if(gate_type == 'or'):
            val = or_gate(val, in_edge_list[i][2]['value'])
        elif(gate_type == 'and'):
            val = and_gate(val, in_edge_list[i][2]['value'])     
        elif(gate_type == 'nand'):
            val = nand_gate(val, in_edge_list[i][2]['value'])
        elif(gate_type == 'nor'):
            val = nor_gate(val, in_edge_list[i][2]['value'])
        elif(gate_type == 'xnor'):
            val = xnor_gate(val, in_edge_list[i][2]['value'])
        elif(gate_type == 'xor'):
            val = xor_gate(val, in_edge_list[i][2]['value'])
        
        else:
            val = 'x'     
    return val            
        
"This is very helpful function. Gets the node whose number is given by num"
def get_node(G, num):
    node_iter = G.nodes_iter(True)
    for iter in node_iter:
        if (iter[0] == num):
            return iter
    return    

"Takes an edge and its value as input and finds the implications of this value on entire graph and modifies the edge values accordingly"
def imply_edge(G, edge, val, implications):
    if(edge[2]['fault'] == 'none'):
        edge[2]['value'] = val
    elif(edge[2]['fault'] == 'sa1'):
        edge[2]['value'] = output_val(val, '1')
    else:
        edge[2]['value'] = output_val(val, '0')

    if edge not in implications[implications.last()[0]]:
        implications[implications.last()[0]].append(edge)
    
    node_iter = G.nodes_iter(True)
    out_node = get_node(G, edge[1])
    out_edge_list = G.out_edges(edge[1], True)
            
    if(out_node[1]['type'] == 'output'):
        return
    if(out_node[1]['type'] == 'gate'):
        out_val = calc_output(G, out_node)
        
    if(out_val != 'x'):
        for out_edge in out_edge_list:
            imply_edge(G, out_edge, out_val, implications)
        return
    return
           
        
"This is the function to which call needs to be made in the main program. pi here stands for primary input. val stands for its new value ('0' or '1')"
def imply(G, pi, val, implications):
    out_edge_list = G.out_edges(pi, True)
    for out_edge in out_edge_list:
        imply_edge(G, out_edge, val, implications)
    return
    
def NOT(value):
    if (value == 0):
        return 1
    elif (value == 1):
        return 0

def ctrl_value(type):
    if (type == 'and' or type == 'nand'):
        return 0
    elif (type == 'or' or type == 'nor'):
        return 1
    else:
        return -1
    "-1 represents that a controlling value is not defined"

def get_po_list(G):
    l = []
    attr_list = nx.get_node_attributes(G, 'type')
    for key in attr_list.keys():
        if attr_list[key] == 'output':
            l.append(key)
    return l

def has_fault_propagated(G, po_list):
    for item in G.in_edges_iter(po_list, True):
         if item[2]['value'] == 'D' or item[2]['value'] == 'D_bar':
                return True
    return False

def get_d_frontier(G):
    l = []
    flag1 = 0
    flag2 = 0
    gate_attr_list = nx.get_node_attributes(G, 'type')
    edge_attr_list = nx.get_edge_attributes(G, 'value')
    for key1 in gate_attr_list.keys():
        flag1 = 0
        flag2 = 0
        "For every node which is a gate"
        if gate_attr_list[key1] == 'gate':
            for key2 in edge_attr_list.keys():
                if (key2[0] == key1):
                    "Checking if any of the output of the node is 'x'"
                    if (edge_attr_list[key2] == 'x'):
                        flag1 = 1
            for key2 in edge_attr_list.keys():
                if (key2[1] == key1):
                    "And checking if at least one of the input is D or D_bar"
                    if (edge_attr_list[key2] == 'D' or edge_attr_list[key2] == 'D_bar'):
                        flag2 = 1
            "If both conditions are satisfied, add this gate to the list of D-frontier"
            if((flag1 * flag2) == 1):
                l.append(key1)
            else:
                "Do nothing"
    return l

def x_path_check(l):
    if not l:
        return False
    else:
        return True

def IsUnassigned(G, node1, node2):
    for key in nx.get_edge_attributes(G, 'value').keys():
        if(key[0] == node1 and key[1] == node2):
            if (nx.get_edge_attributes(G, 'value')[key] == 'x'):
                return True
            else:
                "Do nothing"
        else:
            "Continue search"
    return False

    
"returns a tuple (input_edge,value) where input_edge is a 2-tuple and value is a number"
def Objective(G, node1, node2, fvalue): 
    "fvalue should be True or False"
    if(IsUnassigned(G, node1, node2)):
        return (node1, node2, NOT(fvalue))
    "Select a gate P from the D-frontier"
    D_frontier = get_d_frontier(G)
    node1 = D_frontier[0]
    for item in G.in_edges_iter(node1, 'x'):
        if (item[2]["value"] == 'x'):
            input_edge = (item[0], item[1])
            break
    "If gate g has controlling value"
    "Else if 0 value easier to get at input of XOR/EQUIV gate"
    "Else c=0"
    if (ctrl_value(nx.get_node_attributes(G, 'gatetype')[node1]) != -1):
        c = ctrl_value(nx.get_node_attributes(G, 'gatetype')[node1])
    elif ((G.node[node1]['type'] == 'xor' or G.node[node1]['type'] == 'xnor') and (G.node[item[0]]['cc0'] < G.node[item[0]]['cc1'])):
        c = 1
    else:
        c = 0
        
    return (input_edge, NOT(c))


"this function returns controllability values of node, where node is a number"
def get_controllability(G, node):
    if G.node[node]['type'] == 'output' :
       for predecessors in G.predecessors_iter(node):
           l0 = G.node[predecessors]['cc0']
           l1 = G.node[predecessors]['cc1']
       G.node[node]['cc0'] = l0
       G.node[node]['cc1'] = l1
    else : 
         for incoming in G.predecessors_iter(node):
             if G.node[incoming]['cc0'] == 1 and G.node[incoming]['cc1'] == 1 and G.node[incoming]['type'] != 'input':
                get_controllability(G, incoming)
         l0 = []
         l1 = []
         for predecessors in G.predecessors_iter(node):
             l0.append(G.node[predecessors]['cc0'])
             l1.append(G.node[predecessors]['cc1'])

         if G.node[node]['gatetype'] == 'and':
            G.node[node]['cc0'] = min(l0) + 1
            G.node[node]['cc1'] = sum(l1) + 1

         elif G.node[node]['gatetype'] == 'nand':
            G.node[node]['cc0'] = sum(l1) + 1
            G.node[node]['cc1'] = min(l0) + 1

         elif G.node[node]['gatetype'] == 'or':
            G.node[node]['cc0'] = sum(l0) + 1
            G.node[node]['cc1'] = min(l1) + 1

         elif G.node[node]['gatetype'] == 'nor':
            G.node[node]['cc0'] = min(l1) + 1
            G.node[node]['cc1'] = sum(l0) + 1

         elif G.node[node]['gatetype'] == 'not':    
            G.node[node]['cc0'] = sum(l1) + 1
            G.node[node]['cc1'] = sum(l0) + 1

         elif G.node[node]['gatetype'] == 'xor':
            l2 = []
            l3 = []
            i = 0
            for predecessors in G.predecessors_iter(node):
                if i % 2 == 0 :
                   l2.append(G.node[predecessors]['cc0'])
                   l3.append(G.node[predecessors]['cc1'])
                else :
                   l2.append(G.node[predecessors]['cc1'])
                   l3.append(G.node[predecessors]['cc0'])
                i += 1
            G.node[node]['cc0'] = min(sum(l0), sum(l1)) + 1
            G.node[node]['cc1'] = min(sum(l2), sum(l3)) + 1

         elif G.node[node]['gatetype'] == 'xnor':
            l2 = []
            l3 = []
            i = 0
            for predecessors in G.predecessors_iter(node):
                if i % 2 == 0 :
                   l2.append(G.node[predecessors]['cc0'])
                   l3.append(G.node[predecessors]['cc1'])
                else :
                   l2.append(G.node[predecessors]['cc1'])
                   l3.append(G.node[predecessors]['cc0'])
                i += 1
            G.node[node]['cc0'] = min(sum(l2), sum(l3)) + 1
            G.node[node]['cc1'] = min(sum(l0), sum(l1)) + 1


"nodes_iter returns 2-tuple (node(nbr), data-dict)"
def preprocess(G):
    for items in G.nodes_iter(data=True):
        if items[1]['type'] != 'input' and items[1]['cc0'] == 1 and items[1]['cc1'] == 1:
           get_controllability(G, items[0])

"checks if objective requires setting of all inputs"
def all_inputs_req(G, input_edge, vs) : 
    if G.node[input_edge[0]]['gatetype'] == 'and' and vs == 1 :
       return True
    elif G.node[input_edge[0]]['gatetype'] == 'or' and vs == 0 :
       return True
    elif G.node[input_edge[0]]['gatetype'] == 'nand' and vs == 0 :
       return True
    elif G.node[input_edge[0]]['gatetype'] == 'nor' and vs == 1 :
       return True
    elif G.node[input_edge[0]]['gatetype'] == 'not' :
       return True
    else :
       return False


"input_edge is a 2-tuple of nodes given in (source, dest) manner, where source and dest are numbers"
"takes in a tuple, returns list"
def Backtrace(G, input_edge, vs, implications):
 v = vs
 new_input_edge = list(input_edge)
 "tuple to list conversion is done as only lists, but not tuples can be updated"
 while G.node[new_input_edge[0]]['type'] == 'gate' :
   if G.node[new_input_edge[0]]['gatetype'] == 'nand' or G.node[new_input_edge[0]]['gatetype'] == 'not' or G.node[new_input_edge[0]]['gatetype'] == 'nor' :
    v = NOT(v)
   ls = [x for x in G.in_edges(new_input_edge[0], data=True) if x[2]['value'] == 'x']
   if all_inputs_req(G, new_input_edge, vs) : 
    if v :
     edge = max(ls, key=lambda x:G.node[x[0]]['cc1'])
    else :
     edge = max(ls, key=lambda x:G.node[x[0]]['cc0'])
   else :
    if v :
     edge = min(ls, key=lambda x:G.node[x[0]]['cc1'])
    else :
     edge = min(ls, key=lambda x:G.node[x[0]]['cc0'])
   new_input_edge[0] = edge[0]
 "add the objective at input to the implication stack"
 a = (new_input_edge[0], v)
 if len(implications) == 0 :
    implications[a]=[]
 elif (a[0] != implications.last()[0][0]) or (a[1] != implications.last()[0][1]) : 
    implications[a]=[]
 return a
 # objects returned are the primary input and its objective value 

"Backtrack returns a tuple (node,value), which is the new PI assignment OR an empty list"
def Backtrack(G, implications) : 
    if len(implications) == 0 :
       "do nothing"
    elif len(implications) == 1 :
        "remove all assignments due to the item implications[len(implications)-1], accessed from hash table"
        for edges in implications.last()[1] :
           edges[2]['value'] = 'x'
           
        item = (implications.last()[0][0],NOT(implications.last()[0][1]))
        implications[item]=[]
    elif implications.last()[0][0] == implications.lastbutone()[0][0] : 
       "remove all assignments due to the item implications[len(implications)-1], accessed from hash table"
       for edges in implications.last()[1] :
           edges[2]['value'] = 'x'
           
       del implications[implications.last()[0]]
       del implications[implications.lastbutone()[0]]
       Backtrack(G, implications)
    else :
       item = (implications.last()[0][0],NOT(implications.last()[0][1]))
       "remove all assignments due to the item implications[len(implications)-1], accessed from hash table"
       for edges in implications.last()[1] :
           edges[2]['value'] = 'x'
           
       implications[item]=[]
    if not implications :
       return ()
    else : 
       return implications.last()[0]


"PODEM algorithm"
"fault is stuck-at-fvalue on the edge node1->node2, implications is the global implication stack : it is also the test vector"
def podem_comb(G, implications, node1, node2, fvalue) :
    po_list = get_po_list(G) 
    while not has_fault_propagated(G, po_list) : 
          dfrontier = get_d_frontier(G)
          if x_path_check(dfrontier) :
             [l, vl] = Objective(G, node1, node2, fvalue)
             [pi, vpi] = Backtrace(G, l, vl, implications)
             "print [pi, vpi]"
             imply(G, pi, str(vpi),implications)
             if podem_comb(G, implications, node1, node2, fvalue) : 
                return True
             result = Backtrack(G, implications)  # Backtrack can return new PI assignmnet or an empty list
             if not result :  # implications list has been exhausted
                return False
             else : 
                pi = result[0]
                vpi = result[1]
             imply(G, pi, str(vpi),implications)
             if podem_comb(G, implications, node1, node2, fvalue) : 
                return True
             imply(G, pi, 'x',implications)
             return False
          elif not implications : 
             return False
          else :
             result = Backtrack(G, implications)
    return True
          

def fault_assign(G, node1, node2, fvalue) :
    if fvalue : 
       G[node1][node2]['value'] = 'D_bar'
    else : 
       G[node1][node2]['value'] = 'D'           


G = nx.DiGraph()
G.add_nodes_from([1, 2, 3], type='input', cc0=1, cc1=1)
G.add_node(4, type='gate', gatetype='and', cc0=1, cc1=1)
G.add_nodes_from([5, 6, 7], type='gate', gatetype='xnor', cc0=1, cc1=1)
G.add_nodes_from([8, 9], type='gate', gatetype='not', cc0=1, cc1=1)
G.add_nodes_from([10, 11], type='gate', gatetype='nand', cc0=1, cc1=1)
G.add_node(12, type='gate', gatetype='or', cc0=1, cc1=1)
G.add_nodes_from([13, 14, 15], type='output', cc0=1, cc1=1)
G.add_edges_from([(1, 4), (2, 4), (2, 6), (2, 7), (3, 11), (4, 10), (4, 5), (4, 6), (5, 8), (5, 10), (6, 5), (6, 9), (6, 11), (7, 11), (8, 7), (9, 12), (10, 13), (11, 15), (12, 14)], value='x', fault='none')
G.add_edge(8, 12, value='x', fault='sa1')
nx.draw_circular(G)
plt.savefig("samplegraph.png")
plt.ion()
plt.show()
preprocess(G)  # preprocess assigns all controllability values to nodes


"fault_assign(G,8,12,1)"
"test for podem_comb"
"implications is a derived subclass of OrderedDict which stores PI assignments with corresponding implications,"
"It also stores keys in the order in which they were added"
implications = MyOrderedDict()
fault_assign(G, 8, 12, 1)
fault_assign(G, 8, 7, 1)

a = podem_comb(G, implications, 8, 12, 1)
print '***'
print a
print implications
