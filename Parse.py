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
    all_years = []
    max_lines = 35 # useful for testing
    
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
            entry[ANCESTOR] = info[2].strip()
            entry[AUTHOR] = info[3].strip()
            entry[YEAR] = info[4].strip()
            entry[URL] = info[5].strip()
            entry[COMMENT] = info[6].strip()
            if not entry[YEAR] in all_years:
                all_years.append(entry[YEAR])
            
    all_years.sort()
    
    all_nodes = []
    
    for year in all_years:
        print('===============  %s '%year)
        
        graphviz += '  subgraph cluster_%s {\n    style=filled;\n    color=lightgrey;\n'%(year)
        for id in entries.keys():
            entry = entries[id]
            if entry[YEAR] == year:
                print("%s: %s -> %s"%(entry[YEAR], id, entry[AUTHOR]))
                label = '%s %s'%(entry[CELLTYPE],entry[COMMENT])
                graphviz += '    node [style="rounded,filled",color=white,label="%s"]; %s;\n'%(label, id)
                all_nodes.append(id)
                if entry[ANCESTOR] != '00' and entry[ANCESTOR] in all_nodes:
                    graphviz += '    %s -> %s [len=1.00, arrowhead=diamond]\n'%(entry[ANCESTOR],id)
                
        
        graphviz += '    label="%s";\n  }\n'%(year)

            
    graphviz += "\n}"
    
    gv_file_name = csv_file.replace('.csv','.gv')
    gv_file = open(gv_file_name,'w')
    gv_file.write(graphviz)
    gv_file.close()
    
    print("\nGraphViz (http://www.graphviz.org/) file written to %s. Generate PNG file from this with:"%(gv_file_name))
    print("\n    dot -Tpng  %s -o %s\n"%(gv_file_name,csv_file.replace('.csv','.png')))
            

	
