class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

#notice that I am not storing the character in the node itself
#this is what I mean by it being implicit, because the dictionary  
# of children is already storing the parent in its key. 

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char]=TrieNode()
            node = node.children[char]
        node.is_end = True

    def query(self, x: str) -> bool:
        node = self.root

        for char in x:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

if __name__=="__main__":
    tr = Trie()
    tr.insert('Suhail')
    tr.insert('Felipe')
    print(tr.query('Felipe'))
    print(tr.query('suh'))
