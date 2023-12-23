class Graph

  def initialize(adj={})
    @adj = adj
  end
  
  def get_neighbors(node)
    @adj[node] || []
  end
  
  def get_adjacency_list
    @adj.keys
  end
  
  def is_oriented
    matrix = get_matrix
    order = get_order
    order.times do |i|
      row = matrix[i]
      column = matrix.map {|line| line[i]}
      return true if row != column
    end
    false
  end

  
  def is_complete
    @adj.each_key do |node|
      return false if get_degree(node) != get_order - 1
    end
    true
  end
  
  def is_labeled
    @adj.each_value do |neighbors|
      neighbors.each do |neighbor|
        return true if neighbor.is_a?(String) && neighbor != ""
      end
    end
    false
  end
  
  def get_order
    @adj.size
  end
  
  def get_degree(node)
    @adj[node]&.size
  end
  
  def get_vertices
    vertices = []
    get_adjacency_list().each do |vertex|
      vertices << vertex
    end
    vertices
  end
  
  def get_matrix
    order = get_order
    m = Array.new(order) { Array.new(order, 0) }
    i = -1
    vl = get_vertices()
    vl.sort!
    
    vl.each do |node|
      i += 1
      @adj[node].each_with_index do |_, j|
        m[i][j] = 1
      end
    end
    m
  end
  
  def show_matrix
    if is_oriented
      puts "\nAdjacency matrix of predecessors"
      Graph.new(get_pred).get_matrix.each do |line|
        puts line.join(" ")
      end
      puts "\nAdjacency matrix of successors"
    else
      puts "\nAdjacency matrix of the graph"
    end
    get_matrix.each do |line|
      puts line.join(" ")
    end
  end
  
  def get_pred
    pred = {}
    vl = get_vertices()
    vl.sort!
    vl.each do |node|
      pred[node] ||= []
      @adj[node].each do |neighbor|
        pred[neighbor] ||= []
        pred[neighbor] << node
      end
    end
    pred
  end
  
  def set_neighbors(node, neighbor)
    @adj[node] = neighbor
  end
  
  ###################################################
  #     Graph Traversal Algorithms: DFS and BFS     #
  ###################################################
  def BFS(node)
    traversal, temp = [], [node]
    until temp.empty?
      x = temp.shift
      l = @adj[x].is_a?(Array) ? @adj[x] : [@adj[x]]
      traversal << x
      l.each do |neighbor|
        temp << neighbor if !temp.include?(neighbor) && !traversal.include?(neighbor)
      end
    end
    traversal
  end
  
  def DFS(start, visited=[])
    visited << start
    @adj[start].each do |neighbor|
      DFS(neighbor, visited) if !visited.include?(neighbor)
    end
    visited
  end
  
  def paths(departure, arrival)
    paths, visited, tmp_stack = [], [departure], [[departure]]
    until tmp_stack.empty?
      x = tmp_stack.shift
      neighbors = @adj[x[-1]].is_a?(Array) ? @adj[x[-1]] : [@adj[x[-1]]]
      neighbors.each do |neighbor|
        if neighbor == arrival
          paths << x + [neighbor]
        elsif !x.include?(neighbor)
          visited << neighbor if !visited.include?(neighbor)
          tmp_stack << x + [neighbor]
        end
      end
    end
    paths
  end
       
  def set_neighbors(node, neighbor)
    @adj[node] = neighbor
  end
    
  def BFS(node)
    traversal = []
    temp = [node]
      
    while !temp.empty?
      x = temp.shift
      
      if @adj[x].is_a?(Array)
        l = @adj[x].dup
      else
        l = [@adj[x]]
      end
        
      traversal << x
        
      l.each do |neighbor|
        if !temp.include?(neighbor) && !traversal.include?(neighbor)
          temp << neighbor
        end
      end
    end
     
    traversal
  end
    
  def DFS(start, visited=nil)
    visited ||= []
    visited << start
      
    @adj[start].each do |neighbor|
      if !visited.include?(neighbor)
        DFS(neighbor, visited)
      end
    end
     
    visited
  end
    
  def paths(departure, arrival)
    paths = []
    visited = [departure]
    tmp_stack = [[departure]]
      
    while !tmp_stack.empty?
      x = tmp_stack.shift
      neighbors = @adj[x[-1]].is_a?(Array) ? @adj[x[-1]] : [@adj[x[-1]]]
      
      neighbors.each do |neighbor|
        if neighbor == arrival
          paths << x + [neighbor]
        elsif !x.include?(neighbor)
          if !visited.include?(neighbor)
            visited << neighbor
          end
          tmp_stack << x + [neighbor]
        end
      end
    end
      
    paths
  end
    
  def get_shortest_path(paths)
    shortest_path = paths[0]
    
    paths[1..-1].each do |path|
      if path.length < shortest_path.length
        shortest_path = path
      end
    end
    
    shortest_path
  end
  
  def add_node(node, values)
    if !get_vertices.include?(node)
      set_neighbors(node, values)
    end
  end
end


###################################################
#               TESTING AND EXAMPLES              #
###################################################
def example
  # Undirected Graphs
  social_links = Graph.new(
    {
      "Jean" => ["Jade"],
      "Jade" => ["Paul"],
      "Paul" => ["Thomas", "René", "Pierre"],
      "Pierre" => [],
      "Thomas" => ["Jean"],
      "René" => ["Marie"],
      "Marie" => ["René"]
    }
  )
  
  # Undirected Graphs - defined with letters
  lower_example = Graph.new(
    {
      "a" => ["b", "c"],
      "b" => ["a", "d", "e"],
      "c" => ["a", "d"],
      "d" => ["b", "c", "e"],
      "e" => ["b", "d", "f", "g"],
      "f" => ["e", "g"],
      "g" => ["e", "f", "h"],
      "h" => ["g"]
    }
  )
  
  # Directed Graph, Successor List
  upper_example = Graph.new(
    {
      "A" => ["C"],
      "B" => ["A"],
      "C" => ["B", "D"],
      "D" => ["A", "B"],
      "E" => ["D"]
    }
  )
  
  ###################################################
  #                  ASSERTION TESTS                #
  ###################################################
  raise "Degree of C is not 2" unless upper_example.get_degree('C') == 2
  raise "Degree of Jean is not 1" unless social_links.get_degree('Jean') == 1
  raise "Graph is not labeled" unless social_links.is_labeled
  raise "Shortest path is incorrect" unless lower_example.get_shortest_path(lower_example.paths("g", "c")) == ['g', 'e', 'd', 'c']
  raise "Degree of Paul is not 3" unless social_links.get_degree('Paul') == 3
  
  ###################################################
  #                     SHOW CASES                  #
  ###################################################    
  puts "----------- social_links Graph --------------"
  puts "Nodes: #{social_links.get_vertices}, BFS search with node 'Jean': #{social_links.BFS('Jean')}"
  social_links.show_matrix
  puts
  
  puts "----------- upper_example Graph --------------"
  upper_example.show_matrix
  puts
  
  puts "----------- lower_example Graph --------------"
  puts "The list of paths to go from node 'a' to node 'g' is: #{lower_example.paths('a', 'g')}"
  puts "A breadth-first traversal of graph Gl from node 'g' is: #{lower_example.DFS('g')}"
  puts "DFS applied started from node 'a' is: #{lower_example.DFS('a')}"
  lower_example.show_matrix
end

if __FILE__ == $PROGRAM_NAME
  example
end