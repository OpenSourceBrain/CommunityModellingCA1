import sys
import re

from subprocess import check_call

ID = 'ID'
CELLTYPE = 'celltypes'
ANCESTOR = 'ancestor'
AUTHOR = 'first author'
YEAR = 'year' 
URL = 'URL' 
COMMENT = 'comment'

if __name__ == '__main__':

    csv_file = 'CA1Models.csv'
    
    entries = {}
    all_celltypes = []
    all_years = []
    output_mode = 'celltypes' #celltypes or years
    max_lines = 148 # useful for testing
    
    for line in open(csv_file):
        if not line.startswith(ID) and max_lines>0:
            max_lines -= 1
            info = line.split(',')
            id = info[0]
            if id == 'x':
                id = info[5].strip().replace(':','_').replace('/','_').replace('.','_').replace('?','_') # URL.. unique
            entry = {}
            entries[id] = entry
            entry[CELLTYPE] = info[1].strip()
            if not entry[CELLTYPE] in all_celltypes:
                all_celltypes.append(entry[CELLTYPE])
            entry[ANCESTOR] = info[2].strip()
            entry[AUTHOR] = info[3].strip()
            entry[YEAR] = info[4].strip()
            entry[URL] = info[5].strip()
            entry[COMMENT] = info[6].strip()
            if not entry[YEAR] in all_years:
                all_years.append(entry[YEAR])
            
    all_celltypes.sort()
    all_years.sort()
    
    all_nodes = []
    
    if output_mode == 'celltypes':

        graphviz_PC = '''# GraphViz compliant export of %s

digraph %s {
  fontsize=10;\n  ranksep=2;\n  nodesep=0.06;

'''%(csv_file,csv_file.replace('.','_'))

        graphviz_IN = '''# GraphViz compliant export of %s

digraph %s {
  fontsize=10;\n  ranksep=2;\n  nodesep=0.06;

'''%(csv_file,csv_file.replace('.','_'))

        for celltype in all_celltypes:
            print('===============  %s '%celltype)

            if celltype == "PC":
                graphviz_PC += '  subgraph cluster_%s {\n    style=filled;\n    color=lightgrey;\n'%(celltype)
                for id in entries.keys():
                    entry = entries[id]
                    if entry[CELLTYPE] == celltype:
                        print(celltype)
                        print("%s: %s -> %s"%(entry[YEAR], id, entry[AUTHOR]))
                        label1 = re.sub('\d+','',str(entry[COMMENT]))
                        label1 = label1.rstrip()
                        label2 = re.sub('[.&\sA-Za-z]','',str(entry[COMMENT]))
                        label = label1 + '\\n' + label2
                        graphviz_PC += '    node [shape="rect",style="rounded,filled",color="black",fillcolor="white",label="%s"]; %s;\n'%(label, id)
                        all_nodes.append(id)
                        if entry[ANCESTOR] != '00' and entry[ANCESTOR] in all_nodes:
                            graphviz_PC += '    %s -> %s [len=1.0, arrowhead=normal]\n'%(entry[ANCESTOR],id)

                graphviz_PC += '    label="%s";\n  }\n\n'%(celltype)

            else:
                graphviz_IN += '  subgraph cluster_%s {\n    style=filled;\n    color=lightgrey;\n'%(celltype)
                for id in entries.keys():
                    entry = entries[id]
                    if entry[CELLTYPE] == celltype:
                        print(celltype)
                        print("%s: %s -> %s"%(entry[YEAR], id, entry[AUTHOR]))
                        label1 = re.sub('\d+','',str(entry[COMMENT]))
                        label1 = label1.rstrip()
                        label2 = re.sub('[.&\sA-Za-z]','',str(entry[COMMENT]))
                        label = label1 + '\\n' + label2
                        graphviz_IN += '    node [shape="rect",style="rounded,filled",color="black",fillcolor="white",label="%s"]; %s;\n'%(label, id)
                        all_nodes.append(id)
                        if entry[ANCESTOR] != '00' and entry[ANCESTOR] in all_nodes:
                            graphviz_IN += '    %s -> %s [len=1.0, arrowhead=normal]\n'%(entry[ANCESTOR],id)

                graphviz_IN += '    label="%s";\n  }\n\n'%(celltype)

        graphviz_PC += "\n}"
        graphviz_PC = graphviz_PC.replace('/', '')
    
        gv_file_name_PC = csv_file.replace('.csv','_PC.gv')
        gv_file_PC = open(gv_file_name_PC,'w')
        gv_file_PC.write(graphviz_PC)
        gv_file_PC.close()

        graphviz_IN += "\n}"
        graphviz_IN = graphviz_IN.replace('/', '')

        gv_file_name_IN = csv_file.replace('.csv','_IN.gv')
        gv_file_IN = open(gv_file_name_IN,'w')
        gv_file_IN.write(graphviz_IN)
        gv_file_IN.close()

        check_call(['dot','-Tpng','%s'%(gv_file_name_PC),'-o','%s'%(gv_file_name_PC.replace('.gv','.png'))])
        check_call(['dot','-Tpng','%s'%(gv_file_name_IN),'-o','%s'%(gv_file_name_IN.replace('.gv','.png'))])

        print("\nGraphViz (http://www.graphviz.org/) files written to %s, %s and PNG files written to %s, %s"%(gv_file_name_PC, gv_file_name_IN, gv_file_name_PC.replace('.gv','.png'), gv_file_name_IN.replace('.gv','.png')))

    if output_mode == 'years':

        graphviz = '''# GraphViz compliant export of %s

digraph %s {
  fontsize=10;\n  ranksep=2;\n  nodesep=0.06;

'''%(csv_file,csv_file.replace('.','_'))

        for year in all_years:
            print('===============  %s '%year)

            graphviz += '  subgraph cluster_%s {\n    style=filled;\n    color=lightgrey;\n'%(year)
            for id in entries.keys():
                entry = entries[id]
                if entry[YEAR] == year:
                    print("%s: %s -> %s"%(entry[YEAR], id, entry[AUTHOR]))
                    label1 = str(entry[CELLTYPE])
                    label2 = re.sub('\d+','',str(entry[COMMENT]))
                    label2 = label1.rstrip()
                    label3 = re.sub('[.&\sA-Za-z]','',str(entry[COMMENT]))
                    label = label1 + '\\n' + label2 + '\\n' + label3
                    graphviz += '    node [shape="rect",style="rounded,filled",color="black",fillcolor="white",label="%s",width=1,height=3]; %s;\n'%(label, id)
                    all_nodes.append(id)
                    if entry[ANCESTOR] != '00' and entry[ANCESTOR] in all_nodes:
                        graphviz += '    %s -> %s [len=1.00, arrowhead=diamond]\n'%(entry[ANCESTOR],id)

            graphviz += '    label="%s";\n  }\n'%(year)

        graphviz += "\n}"
        graphviz = graphviz.replace('/', '')

        gv_file_name = csv_file.replace('.csv','.gv')
        gv_file = open(gv_file_name,'w')
        gv_file.write(graphviz)
        gv_file.close()

        check_call(['dot','-Tpng','%s'%(gv_file_name),'-o','%s'%(gv_file_name.replace('.gv','.png'))])

        print("\nGraphViz (http://www.graphviz.org/) file written to %s and PNG file written to %s"%(gv_file_name, gv_file_name.replace('.gv','.png')))

    else:
        "Invalid output mode. Please choose celltypes or years."

#    print("\nGraphViz (http://www.graphviz.org/) file written to %s. Generate PNG file from this with:"%(gv_file_name))
#    print("\n    dot -Tpng  %s -o %s\n"%(gv_file_name,csv_file.replace('.csv','.png')))

