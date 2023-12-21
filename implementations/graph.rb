class Graph

    def initialize(adj={})    
        @adj = adj
    end

    def get_neighbors(node)
        return @adj[node] || []
    end

    def get_adjacency_list()
        return @adj
    end

    def is_oriented
        matrix = get_matrix()

        (0...get_order).each do |i|
            row = matrix[i]
            column = (0...get_order).map {|j| matrix[j][i]}
            return true if row != column
        end
        
        return false
    end

    def is_complete()
       @adj.keys.each do |node|
            if get_degree(node) != get_order()-1
                return false
            end
        end

        return true
    end

    def is_labeled()
        @adj.each do |node, neighbors|
            neighbors.each do |neighbor|
                if neighbor.is_a?(String) && neighbor != ""
                    return true
                end
            end
        return false
        end
    end

    def get_order()
        return @adj.keys.length
    end

    def get_degree(node)
        return @adj.key?(node) ? @adj[node].length : nil
    end

    def get_vertices()
        return @adj.keys.to_a
    end

    def get_matrix
        order = get_order()
        # m = (((0...order).each do |i|).each do |j|)
        m = Array.new(order) { Array.new(order, 0) }
        i = -1
        vl = get_vertices()
        vl.sort!
    
        vl.each do |node|
            i += 1
            adj[node].length do |j|
                m[i][j] = 1        
        end
        return m
    end
end


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

puts social_links.get_degree("Jean") end