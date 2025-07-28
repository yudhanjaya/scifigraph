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
# The updateVisualization(centerViews = True) function can be called
# during script execution to update the opened views
# The pauseScript() function can be called to pause the script execution.
# To resume the script execution, you will have to click on the
# "Run script " button.
# The runGraphScript(scriptFile, graph) function can be called to launch
# another edited script on a tlp.Graph object.
# The scriptFile parameter defines the script name to call
# (in the form [a-zA-Z0-9_]+.py)
# The main(graph) function must be defined
# to run the script on the current graph
def main(graph):
    prop_author = graph['author']
    prop_name = graph['name']
    prop_title = graph['title']
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

    for n in graph.getNodes():
        name_node = prop_name[n]
        if name_node != '':
            prop_viewLabel[n] = name_node
        else:
            prop_viewLabel[n] = prop_title[n]
    
    print('all done.')
