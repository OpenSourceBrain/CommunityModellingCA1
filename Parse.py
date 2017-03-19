import sys

ID = 'ID'
CELLTYPE = 'celltype'
ANCESTOR = 'ancestor'
AUTHOR = 'first author'
YEAR = 'year' 
URL = 'URL' 
COMMENT = 'comment'

if __name__ == '__main__':

    csv_file = 'CA1Models.csv'
    
    graphviz = '''# GraphViz compliant export of %s

digraph %s {
  fontsize=10;

'''%(csv_file,csv_file.replace('.','_'))
    
    entries = {}
    all_celltypes = []
    all_years = []
    output_mode = 'celltypes' #celltypes pr year
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
        for celltype in all_celltypes:
            print('===============  %s '%celltype)

            graphviz += '  subgraph cluster_%s {\n    style=filled;\n    color=lightgrey;\n'%(celltype)
            for id in entries.keys():
                entry = entries[id]
                if entry[CELLTYPE] == celltype:
                    print(celltype)
                    print("%s: %s -> %s"%(entry[YEAR], id, entry[AUTHOR]))
                    label = '%s'%(entry[COMMENT])
                    graphviz += '    node [style="rounded,filled",color=white,label="%s",width=1,height=3]; %s;\n'%(label, id)
                    all_nodes.append(id)
                    if entry[ANCESTOR] != '00' and entry[ANCESTOR] in all_nodes:
                        graphviz += '    %s -> %s [len=1.00, arrowhead=diamond]\n'%(entry[ANCESTOR],id)

            graphviz += '    label="%s";\n  }\n\n'%(celltype)
    
    if output_mode == 'years':
        for year in all_years:
            print('===============  %s '%year)

            graphviz += '  subgraph cluster_%s {\n    style=filled;\n    color=lightgrey;\n'%(year)
            for id in entries.keys():
                entry = entries[id]
                if entry[YEAR] == year:
                    print("%s: %s -> %s"%(entry[YEAR], id, entry[AUTHOR]))
                    label = '%s %s'%(entry[CELLTYPE],entry[COMMENT])
                    graphviz += '    node [style="rounded,filled",color=white,label="%s",width=1,height=3]; %s;\n'%(label, id)
                    all_nodes.append(id)
                    if entry[ANCESTOR] != '00' and entry[ANCESTOR] in all_nodes:
                        graphviz += '    %s -> %s [len=1.00, arrowhead=diamond]\n'%(entry[ANCESTOR],id)

            graphviz += '    label="%s";\n  }\n'%(year)
    
    else:
        "Invalid output mode. Please choose celltypes or years."
    
    graphviz += "\n}"
    graphviz = graphviz.replace('/', '')
    
    gv_file_name = csv_file.replace('.csv','.gv')
    gv_file = open(gv_file_name,'w')
    gv_file.write(graphviz)
    gv_file.close()
    
    print("\nGraphViz (http://www.graphviz.org/) file written to %s. Generate PNG file from this with:"%(gv_file_name))
    print("\n    dot -Tpng  %s -o %s\n"%(gv_file_name,csv_file.replace('.csv','.png')))

