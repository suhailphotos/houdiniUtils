class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next
    
def printlist(head):
    while head is not None:
        print(head.value)
        head = head.next

def insertAt(previous, newVal):
    newNode = Node(newVal)
    newNode.next = previous.next
    previous.next = newNode
    return newNode


head = Node(1)
middle = Node(2)
tail = Node(5)

head.next = middle
middle.next = tail
tail.next = None

print('original list')
printlist(head)
print('\n')
insertAt(middle, 4)
print('inserted list')
printlist(head)



