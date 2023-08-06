import re
import io
import random

_authors_ = "Md Rezaur Rahman"
_copyright_ = "Copyright 2020, The Human Motion Synthesis Project"
_version_ = "0.1"
_maintainer_ = "Reza, Matthias"
_status_ = "Dev"


class LTLGraphCreation():
    def __init__(self, file_data):
        buf = io.StringIO(file_data)
        self.graph = {}  # Stores all node-edge information from the ltl graph
        self.graph_center = None
        self.parsing_buffer(buf)
        self.trv_ftime = None
        self.dead_nodes = []
        self.total_vertex = 0

    def parsing_buffer(self, buf):
        self.lines = buf.readlines()
        for line in self.lines:
            if ("->" in line) and ("[label=" in line):  # Contain edge info between nodes
                # print("Line: ", line)
                pattern = "\[label=(.*?)\]"
                edges = re.search(pattern, line).group(1)
                edges = edges.replace("&amp;", "&")
                edges = edges[1:-1]  # Remove "" or <> from the string
                nodes = list(map(int, re.findall(r'\d+', line)))
                print("Nodes: ", nodes)
                print("Edge: ", edges)
                self.store_graph_info(nodes, edges)

            elif "peripheries" in line:
                self.graph_center = int(re.search(r'\d+', line).group())  # Only take the first node info

        self.total_vertex = len(self.graph.keys())

    def store_graph_info(self, nodes, edge):
        # Source node is empty only
        if self.graph.get(nodes[0]) is None:
            temp = {}
            temp["incoming"] = []
            temp["outgoing"] = []
            temp["edge_info"] = {}  # dict for node -> edge info for tracing the action along the path
            self.graph[nodes[0]] = temp

        # Destination node is empty but source node already exists
        if self.graph.get(nodes[1]) is None:
            temp = {}
            temp["incoming"] = []
            temp["outgoing"] = []
            temp["edge_info"] = {}  # dict for node -> edge info for tracing the action along the path
            self.graph[nodes[1]] = temp

        self.graph.get(nodes[0])["outgoing"].append(nodes[1])
        self.graph.get(nodes[1])["incoming"].append(nodes[0])
        self.graph.get(nodes[0])["edge_info"][nodes[1]] = edge  # e.g., {0: {'edge_info':{1: 'action_str'}}}

    def graph_print(self):
        print(self.graph)
        print("Total nodes are : ", len(self.graph.keys()))
        print("The Graph center: ", self.graph_center)

    def get_action(self, src_node, dst_node):
        edge_str = self.graph.get(src_node)["edge_info"][dst_node] # edge_str: edge information as string
        print(edge_str)
        actn_strings = re.findall(r"[!A-Z\d]+", edge_str)  # only get the actions (uppercase chars) + digits
        actions = []
        reg_exp = re.compile(r'^[A-Z]+\d*')  # Always starts with alpha char, followed by 0 or more digits
        for atm in actn_strings:
            if '!' not in atm and reg_exp.match(atm):
                actions.append(atm)

        actions = list(set(actions))  # convert the list as a unique actions list
        # print("Actions: ", actions)
        return actions

    def check_dead_nodes(self):
        for k in self.graph.keys():
            sz = len(self.graph[k]["outgoing"])
            if (sz == 1) and (self.graph[k]["outgoing"][0] == k):
                self.dead_nodes.append(k)

        if len(self.dead_nodes) > 0:
            print("Dead nodes exist in the Graph.\nDead nodes are: ")
            for i in self.dead_nodes:
                print(i)

    def is_dead(self, u):
        for i in self.dead_nodes:
            if u == i:
                return True
        return False

    def recurse_traversal(self, cur_node, path, actions, p_len=20):
        if len(path) > p_len:
            print("Traversal : ", path)
            print("Actions taken: ", actions)
            return

        edges = self.graph[cur_node]["outgoing"]

        while True:
            next_node = random.choice(edges)
            # print("Current randomly chosen node: ", next_node)
            if self.is_dead(next_node) or cur_node == next_node:
                continue
            else:
                break

        path.append(next_node)
        actions.append(self.get_action(cur_node, next_node))
        self.recurse_traversal(next_node, path, actions)
