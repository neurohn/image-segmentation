class Node:
    def __init__(self, parent, rank=0, size=1):
        self.parent = parent
        self.rank = rank # What is rank exactly -> Height function in the tree
        self.size = size

    def __repr__(self):
        # This returns a printable version of the object
        return '(parent=%s, rank=%s, size=%s)' % (self.parent, self.rank, self.size)

class Forest:
    def __init__(self, num_nodes):
        self.nodes = [Node(i) for i in xrange(num_nodes)]
        self.num_sets = num_nodes

    def size_of(self, i):
        # Returns the size of the ith node
        return self.nodes[i].size

    def find(self, n):
        # Finds the parent(godfather) of the nth node
        temp = n
        while temp != self.nodes[temp].parent:
            temp = self.nodes[temp].parent

        self.nodes[n].parent = temp
        return temp

    def merge(self, a, b):
        # Merge ath and bth nodes
        if self.nodes[a].rank > self.nodes[b].rank:
            self.nodes[b].parent = a
            self.nodes[a].size = self.nodes[a].size + self.nodes[b].size
        else:
            self.nodes[a].parent = b
            self.nodes[b].size = self.nodes[b].size + self.nodes[a].size

            if self.nodes[a].rank == self.nodes[b].rank:
                self.nodes[b].rank = self.nodes[b].rank + 1

        self.num_sets = self.num_sets - 1

    def print_nodes(self):
        for node in self.nodes:
            print node

def create_edge(img, height, x, y, x1, y1, diff):
    vertex_id = lambda x, y: y * height + x
    w = diff(img, x, y, x1, y1)
    return (vertex_id(x, y), vertex_id(x1, y1), w)

def build_graph(img, width, height, diff, neighborhood_8=False):
    graph = []
    for x in xrange(height):
        for y in xrange(width):
            if x > 0:
                graph.append(create_edge(img, height, x, y, x-1, y, diff))

            if y > 0:
                graph.append(create_edge(img, height, x, y, x, y-1, diff))

            if neighborhood_8:
                if x > 0 and y > 0:
                    graph.append(create_edge(img, height, x, y, x-1, y-1, diff))

                if x > 0 and y < height-1:
                    graph.append(create_edge(img, height, x, y, x-1, y+1, diff))

    return graph

def remove_small_components(forest, graph, min_size):
    for edge in graph:
        a = forest.find(edge[0])
        b = forest.find(edge[1])

        if a != b and (forest.size_of(a) < min_size or forest.size_of(b) < min_size):
            forest.merge(a, b)

    return  forest

def segment_graph(graph, num_nodes, const, min_size, threshold_func):
    weight = lambda edge: edge[2]
    forest = Forest(num_nodes)
    sorted_graph = sorted(graph, key=weight)
    # threshold is a list of length = num_nodes
    threshold = [threshold_func(1, const)] * num_nodes
    for edge in sorted_graph:
        parent_a = forest.find(edge[0])
        parent_b = forest.find(edge[1])
        a_condition = weight(edge) <= threshold[parent_a]
        b_condition = weight(edge) <= threshold[parent_b]

        if parent_a != parent_b and a_condition and b_condition:
            forest.merge(parent_a, parent_b)
            a = forest.find(parent_a)
            # Doing this instead of MST
            threshold[a] = weight(edge) + threshold_func(forest.nodes[a].size, const)

    return remove_small_components(forest, sorted_graph, min_size)
