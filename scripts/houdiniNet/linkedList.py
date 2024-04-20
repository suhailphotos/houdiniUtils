import hou

class HoudiniNode:
    def __init__(self, node: hou.Node):
        if not isinstance(node, hou.Node):
            raise TypeError('node must be a Houdini Node')
        self.node = node
        self.next = None

    def __getattr__(self, attr):
        return getattr(self.node, attr)

class LinkedList:
    def __init__(self, parent_node=None, head=None):
        if head:
            if len(head.inputs())>0:
                print('head provided is not a head')
                self.head = None
            else:
                self.parent_node = head.parent()
                self.head = HoudiniNode(head)
                current_node = self.head
                while len(current_node.outputs())>0:
                    current_node.next = HoudiniNode(current_node.outputs()[0])
                    current_node = current_node.next
        elif parent_node and not head:
            self.parent_node = parent_node
            self.head = None


    def print_list(self):
        current_node = self.head
        while current_node:
            print(current_node.name())
            current_node = current_node.next

    def print_tail(self):
        if not self.head:
            return
        tail_node = self.head
        while tail_node.next:
            tail_node = tail_node.next
        print(f'tail node: {tail_node.name()}')

    def append(self, node_type, node_name=None):
        new_node = HoudiniNode(self.parent_node.createNode(node_type, node_name))
        if self.head is None:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node
        new_node.setInput(0, last_node)
        pos = hou.Vector2((last_node.position()[0], last_node.position()[1]-1.1954))
        new_node.setPosition(pos)

    def prepend(self, node_type, node_name=None):
        new_node = HoudiniNode(self.parent_node.createNode(node_type, node_name))
        self.head.setInput(0, new_node)
        pos = hou.Vector2((self.head.position()[0], self.head.position()[1]+1.1954))
        new_node.setPosition(pos)
        new_node.next = self.head
        self.head = new_node
   
    def _find_node(self, node_name: str) -> hou.Node:
        current_node = self.head
        while current_node:
            if current_node.name()==node_name:
                return current_node
            current_node = current_node.next
        return None
        


    def insert_after_node(self, previous_node_name, node_type, node_name):
        previous_node = self._find_node(previous_node_name)
        if not previous_node:
            print('Previous node is not in the network')
            return
        new_node = HoudiniNode(self.parent_node.createNode(node_type, node_name))
        previous_node.next.setInput(0, new_node)
        new_node.setInput(0, previous_node)
        pos = hou.Vector2((previous_node.position()[0], previous_node.position()[1]-1.1954))
        new_node.setPosition(pos)
        new_node.next = previous_node.next
        previous_node.next = new_node
        current_node = new_node.next
        while current_node:
            pos = hou.Vector2((current_node.position()[0], current_node.position()[1]-1.1954))
            current_node.setPosition(pos)
            current_node = current_node.next

if __name__ == '__main__':
    #following code builds a linked list houdini network 
    # and inserts a transfrom node after null3
    # the LinkedList clas should also work if the linked list is already provided by passing a head when initializing
    parent_node=hou.node('/obj').createNode('geo', 'rebelGeo')
    llist = LinkedList(parent_node)
    llist.append('null', 'null1')
    llist.append('null', 'null2')
    llist.append('null', 'null3')
    llist.append('null', 'null4')
    llist.append('output', 'rebel_Output')
    llist.prepend('file', 'head')
    llist.insert_after_node('null3', 'xform', 'mytransfrom')
    llist.print_list()

    #following code coud be used to test if this works with existing network
    #--------------------------------------------
    selected_nodes = hou.selectedNodes()
    if not selected_nodes:
        print('no nodes are selected')
    else:
         existing_head = selected_nodes[0]
         llist_existing = LinkedList(head=existing_head)
         llist_existing.print_list()
         llist_existing.print_tail()

    #following code could be used to test if this could insert a new node
    #Please comment previous section and uncomment to test the below code
    #-------------------------------------------------------------------
    #selected_nodes = hou.selectedNodes()
    #if not selected_nodes:
    #    print('no nodes are selected')
    #else:
    #    existing_head = selected_nodes[0]
    #    llist_existing = LinkedList(head=existing_head)
    #    llist_existing.insert_after_node('null4', 'xform', 'mytransform2')
