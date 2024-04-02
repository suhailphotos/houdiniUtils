class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.value = key

class BinaryTree:
    def __init__(self):
        self.root = None

    def find_node(self, node, key):
        if node is None or node.value == key:
            return node
        elif key < node.value:
            return self.find_node(node.left, key)
        else:
            return self.find_node(node.right, key)

    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert_recursively(self.root, key)

    def _insert_recursively(self, node, key):
        if key < node.value:
            if node.left is None:
                node.left = Node(key)
            else:
                self._insert_recursively(node.left, key)
        else:
            if node.right is None:
                node.right = Node(key)
            else:
                self._insert_recursively(node.right, key)

    def insert_at_node(self, parent_key, key, to_left):
        parent_node = self.find_node(self.root, parent_key)
        if parent_node is not None:
            if to_left:
                if parent_node.left is None:
                    parent_node.left = Node(key)
                else:
                    print("left child already exists")
            else:
                if parent_node.right is None:
                    parent_node.right = Node(key)
                else:
                    print("right child already exists")
        else:
            print('Parent node not found')

    def inorder_traversal(self, node):
        if node:
            self.inorder_traversal(node.left)
            print(node.value, end=' ')
            self.inorder_traversal(node.right)
    
if __name__ == '__main__':
    bt = BinaryTree()
    bt.insert(3)
    bt.insert(2)
    bt.insert(4)

    bt.insert_at_node(2, 1, to_left=True)
    bt.insert_at_node(4, 5, to_left=False)

    bt.inorder_traversal(bt.root)
            

