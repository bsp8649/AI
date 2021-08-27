class TreeMapNode:
    __slots__ = 'key', 'val', 'left', 'right'

    def __init__(self, key, val=None, left=None, right=None):
        self.key = key
        self.val = val
        self.left = left
        self.right = right

    def __iter__(self):
        if self:
            if self.left:
                for elem in self.left: yield elem
            yield self.key
            if self.right:
                for elem in self.right: yield elem

class TreeMap:
    __slots__ = 'root', 'size'

    def __init__(self):
        self.root = None
        self.size = 0

    def __len__(self):
        return self.size

    def __put(self, key, val, node):
        if key == node.key:
            node.val = val
        elif key < node.key:
            if not node.left: node.left = TreeMapNode(key, val)
            else: self.__put(key, val, node.left)
        else:
            if not node.right: node.right = TreeMapNode(key, val)
            else: self.__put(key, val, node.right)

    def put(self, key, val=None):
        if not self.root: self.root = TreeMapNode(key, val)
        else: self.__put(key, val, self.root)
        self.size += 1

    def __setitem__(self, key, val=None):
        self.put(key, val)

    def __get(self, key, node):
        if node == None: return None
        elif key == node.key: return node.val
        elif key < node.key: return self.__get(key, node.left)
        else: return self.__get(key, node.right)

    def get(self, key):
        if not self.root: raise KeyError(key)
        else:
            val = self.__get(key, self.root)
            if val: return val
            else: raise KeyError(key)

    def __getitem__(self,key):
        return self.get(key)

    def __contains__(self,key):
        return self.__get(key, self.root)

    def __iter__(self):
        return self.root.__iter__()

    def __str__(self):
        if not self.root: return '{}'
        result = '{'
        for key in self.root:
            result += repr(key) + ': ' + repr(self[key]) + ', '
        result = result[:-2]
        result += '}'
        return result

def testTreeMap():
    t0 = TreeMap()
    print('t0:', t0)
    print('t0 size (0):', len(t0))
    print('a in t0 (False)?', 'a' in t0)
    print()

    t1 = TreeMap()
    t1['a'] = 1
    print('t1:', t1)
    print('t1 size (1):', len(t1))
    print('t1["a"] (1):', t1['a'])
    print('a in t1 (True)?', 'a' in t1)
    print('b in t1 (False)?', 'b' in t1)
    t1['a'] = 2
    print('t1["a"]=2, t1:', t1)
    print()

    t2 = TreeMap()
    for key,val in zip(('c','a','b'), (3, 1, 2)):
        t2[key] = val
    print('t2:', t2)
    print('t2 size (3):', len(t2))
    print('t1["c"] (2):', t2['c'])
    print('c in t2 (True)?', 'c' in t2)
    print('z in t2 (False)?', 'z' in t2)
    t2['c'] = 3
    print('t2["c"]=3, t2:', t2)
    print()

    t3 = TreeMap()
    for key in ('q','w','e','r','t','y','a','s','d'):
        t3[key] = ord(key)
    print('t3:', t3)
    print('t3 size (9): t3')
    print('t3["y"] (121):', t3['y'])
    print('t in t3 (True):', 't' in t3)
    print('z in t3 (False):', 'z' in t3)
    t3['t'] = 99
    print('t3["t"]=99, t3:', t3)

if __name__ == '__main__':
    testTreeMap()