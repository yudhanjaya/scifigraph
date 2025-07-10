'''
1. Add a node per book. Ignore authors for now.
2. Go through the list of concepts. Add each concept as a node, 
   and add an edge for each of the books it connects to.
'''
# Powered by Python 3.9
# To cancel the modifications performed by the script
# on the current graph, click on the undo button.
# Some useful keyboard shortcuts:
#   * Ctrl + D: comment selected lines.
#   * Ctrl + Shift + D: uncomment selected lines.
#   * Ctrl + I: indent selected lines.
#   * Ctrl + Shift + I: unindent selected lines.
#   * Ctrl + Return: run script.
#   * Ctrl + F: find selected text.
#   * Ctrl + R: replace selected text.
#   * Ctrl + Space: show auto-completion dialog.
from tulip import tlp
import json

def main(graph):
    prop_viewBorderColor = graph['viewBorderColor']
    prop_viewBorderWidth = graph['viewBorderWidth']
    prop_viewColor = graph['viewColor']
    prop_viewFont = graph['viewFont']
    prop_viewFontSize = graph['viewFontSize']
    prop_viewIcon = graph['viewIcon']
    prop_viewLabel = graph['viewLabel']
    prop_viewLabelBorderColor = graph['viewLabelBorderColor']
    prop_viewLabelBorderWidth = graph['viewLabelBorderWidth']
    prop_viewLabelColor = graph['viewLabelColor']
    prop_viewLabelPosition = graph['viewLabelPosition']
    prop_viewLayout = graph['viewLayout']
    prop_viewMetric = graph['viewMetric']
    prop_viewRotation = graph['viewRotation']
    prop_viewSelection = graph['viewSelection']
    prop_viewShape = graph['viewShape']
    prop_viewSize = graph['viewSize']
    prop_viewSrcAnchorShape = graph['viewSrcAnchorShape']
    prop_viewSrcAnchorSize = graph['viewSrcAnchorSize']
    prop_viewTexture = graph['viewTexture']
    prop_viewTgtAnchorShape = graph['viewTgtAnchorShape']
    prop_viewTgtAnchorSize = graph['viewTgtAnchorSize']

    # for n in graph.getNodes():
    #     print(n)

    dirPath = '/Users/albertocottica/Documents/GitHub/scifigraph/'
    dataFile = dirPath + 'scifi_concepts_clean.json'
    with open (dataFile) as f:
        data = json.load(f)
    
    titles = {} # a map from titles to nodes
    for book in data['books']:
        title = book['title']
        author = book['author']
        n = graph.addNode()
        titles[title] = n
        graph.setNodePropertiesValues(n, {'title': title, 'author': author })
        
    for concept in data['concepts']:
        name = concept['name']
        n = graph.addNode()
        graph.setNodePropertiesValues(n, {'name': name})
        for book in concept['books']:
            e = graph.addEdge(n, titles[book])
            
    print(graph.numberOfNodes(), graph.numberOfEdges())
        
        
        

    
  
