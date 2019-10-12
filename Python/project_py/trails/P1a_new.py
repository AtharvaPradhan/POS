def dfs(graph, start, visited=None):
    if visited is None:
        #print(visited)
        visited = set()
        #print(visited)
    visited.add(start)
    print(start)
    for next in graph[start] - visited:
        #(graph[start]," ",visited)
        #print(graph," ",next," ",visited,"\n\n")
        dfs(graph, next, visited)
        #print(graph," ",next," ",visited,"\n\n")  
    return visited

graph = {'1': set(['2','3']),
         '2': set(['4', '5']),
         '3': set(['6','7']),
         '4': set(['2']),
         '5': set(['6']),
         '6':set(['3','5']),
         '7':set(['3'])}
dfs(graph,'1')