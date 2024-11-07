from flask import Flask,render_template,request,url_for
from pageRank import PageRank
import networkx as nx
import json

app=Flask(__name__)
@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':

        pgr = PageRank()

        if request.form['type'] == "XML":
            textxml = request.form['xmltext']
            selected_option = "XML"
            try:
                pagescore, path = pgr.page_rank_xml(str(textxml))
                f_path = url_for('static', filename = path)
            except:
                f_path = 'error'
            return render_template('index.html', text1 = request.form['xmltext'], file_path = f_path , selected_option=selected_option)
        
        elif request.form['type'] == "graph":
            selected_option = "graph"
            jsonGraph = request.form['defaultinput']
            data_str = jsonGraph
            data = json.loads(data_str)
            G = nx.DiGraph()
            nodes = [int(node[1:]) for node in data["nodes"]]
            G.add_nodes_from(nodes)
            edges = [ ( int(edge["source"][1:]) , int(edge["target"][1:]) )  for edge in data["edges"]]
            G.add_edges_from(edges)
            try :
                pagescore, path = pgr.page_rank_graph(G)
                f_path = url_for('static', filename = path)
            except:
                f_path='error_graph'
            return render_template('index.html', text1 = jsonGraph, file_path = f_path , selected_option=selected_option)
            
        elif request.form['type'] == "adjacencyMatrix":
            selected_option = "adjacencyMatrix"
            adjmatrix = request.form['defaultinput']
            data_str =json.loads(adjmatrix)
            matrix = data_str["matrix"]
           
            pagescore, path = pgr.page_rank_matrix(matrix)
            f_path = url_for('static', filename = path)
            
            st = ""
            for i in matrix:
                for j in i :
                    st += str(j) + " "
                st +="\n"
            return render_template('index.html', text1 = st, file_path = f_path, selected_option=selected_option)
        else: 
            return render_template('index.html')
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)