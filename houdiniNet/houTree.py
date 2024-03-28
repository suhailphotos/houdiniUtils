import hou

class NodeNetwork:
    def __init__(self):
        self.root = None

    def networkTraversal(self, root):
        self.root = root
        visited = set()
        self._bfs_printnode(root, visited)

    # find node using recursive method. But works only for 
    # Binary Trees. For this assigment I haven't used this method. 
    # Question: How to extend this to multiple branches 
    # such as when a merge node is present in 
    # the tree which has multiple inputs?

    def find_node(self, node, key):
        if node is None or node.name()==key:
            return node
        elif len(node.inputs())==1:
            return self.find_node(node.inputs()[0], key)
        else:
            return self.find_node(node.inputs()[1], key)
    # I tried to use a for loop here to tackle multiple inputs
    # for example:
    # for current_node in node.inputs():
    #   return self.find_node(current_node, key)
    # this however did not work. 

    def _networkSearch(self, root, key):
        self.root = root
        visited = set()
        return self._bfs_search(root, visited, key)

    def _bfs_printnode(self, root, visited):
        queue = [root]
        while len(queue)>0:
            current = queue.pop(0)
            if current is visited:
                pass
            else:
                print(current.name())
            visited.add(current)
            for node in current.inputs():
                queue.append(node)

    def _bfs_search(self, root, visited, key):
        queue = [root]
        while len(queue)>0:
            current = queue.pop(0)
            if current is visited or current.name()!=key:
                pass
            else:
                return current
            visited.add(current)
            for node in current.inputs():
                queue.append(node)

    def set_root_node(self):
        self.root = hou.node(hou.ui.selectNode(title='Please select output node'))
        return self.root

    def insert_at_node(self, parent_key, key, insert_at=0):
        parent_node = self._networkSearch(self.root, parent_key)
        if parent_node is not None and len(parent_node.inputs())>0:
            current_input_node = parent_node.inputs()[insert_at]
            new_node = parent_node.createInputNode(insert_at, key)
            new_node.setInput(0, current_input_node, 0)
            return new_node
        else:
            print("Node not found or its the head")
        

if __name__ == "__main__":
    geo_tree = NodeNetwork()
    root = geo_tree.set_root_node()
    geo_tree.networkTraversal(root)
    new_node = geo_tree.insert_at_node(parent_key="copytopoints1", key="xform", insert_at=1)
    print(new_node)
