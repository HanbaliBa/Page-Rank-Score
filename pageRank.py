import numpy as np
import networkx as nx
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from datetime import datetime
from pyvis.network import Network

class PageRank:

    def __init__(self):
            pass
    
    def page_rank_matrix(self, matrix, alpha=0.85, threshold=0.00001):
        pr_graph = PR_matrix()
        return pr_graph.page_rank(matrix, alpha, threshold)

    def page_rank_graph(self, Graph, alpha=0.85, threshold=0.00001):
       pr_graph = PR_graph()
       return pr_graph.page_rank(Graph, alpha, threshold)
    
    def page_rank_xml(self, txtxml, alpha=0.85, threshold=0.00001):
       pr_graph = PR_xml()
       return pr_graph.page_rank(txtxml, alpha, threshold)
    
    def page_rank_python(self, G):
        page_rank = nx.pagerank(G, alpha=0.85)
        return page_rank

# Class page rank for adjacency matrix
class PR_matrix:

    def __init__(self):
            pass

    # calculating the random surfing probabilities
    def surfing_probabilities(self, matrix, alpha):
        N = len(matrix)
        P = [[0] * N for _ in range(N)]
        for i in range(N):
            sm = sum(matrix[i])
            for j in range(N):
                if sm != 0:
                    P[i][j] = ( (alpha * ( matrix[i][j] / sm )) + (( 1 - alpha ) * 1 / N ))
                else:
                    P[i][j] = 1 / N
           
        return P

    # calculating the pageRank vector
    def page_rank(self, matrix, alpha = 0.85, threshold = 0.000001):
        print(matrix)
        N = len(matrix)
        R = np.full(N, 1/N)
        P = np.array(self.surfing_probabilities(matrix, alpha))
        R_new = np.dot( R , P )
        t = max(abs( R - R_new ))
        i = 0
        while t > threshold and i < 1000: 
            i += 1
            R = np.copy(R_new)
            R_new = np.matmul(R , P)
            t = max(  abs( R_new - R ) )
       
        
        path = self.create_network(matrix,R_new)

        return R_new, path
    
    # method to create and save the Graph with the page rank score in html format
    def create_network(self, matrix, R_new):


        R_new = np.array(["{:.2f}".format(x * 100) for x in R_new])
        net = Network(height="750px", width="100%", bgcolor="#000000", font_color="white" , directed=True)
        num_nodes = len(R_new)

        for i in range(1, num_nodes + 1):
            net.add_node(i, label = str(i)+"\nPg_score : "+str(R_new[i - 1])+"%", font={'size': R_new[i - 1], 'color': '#ffffff'})

        for i in range(num_nodes):
            for j in range(num_nodes):
                if matrix[i][j] == 1:
                    net.add_edge(i+1, j+1)
        
        net.toggle_physics(True)
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")  
        path = f"{current_time}_network.html"
        net.save_graph("static/"+path)
        return path

    
# Class page rank for Graphs
class PR_graph:

    def __init__(self):
            pass
    
    # function to extract the adjacency matrix from the Graph 
    def graph_To_AdjMatrix(self, Graph):
        length = len(Graph.nodes())
        m = [ [0] * length for _ in range(length) ]
        for i, j in Graph.edges():
            m[i-1][j-1] = 1
        return m
    
    # calculating the pageRank vector
    def page_rank(self, Graph, alpha=0.85, threshold=0.00001):
        pr_matrix = PR_matrix()
        matrix = self.graph_To_AdjMatrix(Graph)
        return pr_matrix.page_rank(matrix, alpha, threshold)


# Class page rank for xml files
class PR_xml:

    def __init__(self):
        pass

    # Parse the XML structure
    def XML_parser(self, path):
        try:
            tree = ET.parse(path)
            root = tree.getroot()
            return root
        except ET.ParseError as e:
            print(f"Error parsing XML file: {e}")
        except FileNotFoundError:
            print(f"File not found: {path}")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    # function to extract the adjacency matrix from the xml file
    def XML_To_AdjMatrix(self, txtxml):

        root = ET.fromstring(txtxml)
        nodes = []

        # Extarcting the nodes
        for node in root.find('nodes').findall('node'):
            nodes.append( int(node.get('id')) )
        edges = []
        # Extarcting the edges 
        for edge in root.find('edges').findall('edge'):
            edges.append( ( int(edge.get('source')), int(edge.get('target'))) )
        
        length = len(nodes)
        m = [ [0] * length for _ in range(length) ]
        for i, j in edges:
            m[i-1][j-1] = 1
        return m
    
    # calculating the pageRank vector
    def page_rank(self, xml_file, alpha=0.85, threshold=0.00001):
        pr_matrix = PR_matrix()
        matrix = self.XML_To_AdjMatrix(xml_file)
        return pr_matrix.page_rank(matrix, alpha, threshold)






            

# The xml file will be represeted as follow : 
xml_data = """<?xml version="1.0" encoding="UTF-8"?>
<graph>
    <!-- nœuds Representation -->
    <nodes>
        <node id="1" label="Node 1" />
        <node id="2" label="Node 2" />
        <node id="3" label="Node 3" />
        <node id="4" label="Node 4" />
        
    </nodes>

    <!-- Edges representation -->
    <edges>
        <edge source="1" target="2"/>
        <edge source="2" target="3" />
        <edge source="4" target="1"/>
        <edge source="3" target="2"/>
        <edge source="1" target="4"/>
        <edge source="1" target="2"/>
    </edges>
</graph>
"""







# G = nx.DiGraph()  # directed graph
# G.add_edges_from([(1, 2), (2, 3), (3, 4), (2, 4), (1, 4)]) # Adding edges
# print(G.nodes())  # Printing the nodes
# print(G.edges())  # Printing the edges
# print(G)
# pgr = PageRank()
# print(len(G.nodes()))
# pgr.page_rank_graph(G)

    # A  B  C  D  E  F  G  H  I  L  M
m = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
     [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
     [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
     [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
     [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
     [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]]

# pgr.page_rank_matrix(m)
# print(pgr.page_rank_xml(xml_data))
# xml = PR_xml()
# m = xml.XML_To_AdjMatrix(r"C:\Users\HP\Desktop\pyt\PageRank\xmlFile.xml")
# print(m)

