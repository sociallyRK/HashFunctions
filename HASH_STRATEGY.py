TABLE_SIZE = 11

# ---------------------
# Hash Function
# ---------------------
def basic_hash(key):
    return sum(ord(c) for c in key) % TABLE_SIZE

# ---------------------
# Linked List for Chaining
# ---------------------
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, key, value):
        current = self.head
        while current:
            if current.key == key:
                current.value = value
                return
            current = current.next
        new_node = Node(key, value)
        new_node.next = self.head
        self.head = new_node

    def search(self, key):
        current = self.head
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def delete(self, key):
        current = self.head
        prev = None
        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return
            prev = current
            current = current.next

# ---------------------
# Strategy Interface
# ---------------------
class HashTableStrategy:
    def insert(self, key, value): raise NotImplementedError
    def search(self, key): raise NotImplementedError
    def delete(self, key): raise NotImplementedError

# ---------------------
# Direct Addressing (Version 1)
# ---------------------
class HashTableDirect(HashTableStrategy):
    def __init__(self):
        self.table = [None] * TABLE_SIZE

    def insert(self, key, value):
        index = basic_hash(key)
        self.table[index] = (key, value)

    def search(self, key):
        index = basic_hash(key)
        if self.table[index] and self.table[index][0] == key:
            return self.table[index][1]
        return None

    def delete(self, key):
        index = basic_hash(key)
        if self.table[index] and self.table[index][0] == key:
            self.table[index] = None

# ---------------------
# Chaining with LinkedList (Version 2)
# ---------------------
class HashTableChaining(HashTableStrategy):
    def __init__(self):
        self.table = [LinkedList() for _ in range(TABLE_SIZE)]

    def insert(self, key, value):
        self.table[basic_hash(key)].insert(key, value)

    def search(self, key):
        return self.table[basic_hash(key)].search(key)

    def delete(self, key):
        self.table[basic_hash(key)].delete(key)

# ---------------------
# Unified HashTable Interface
# ---------------------
class HashTable:
    def __init__(self, strategy: HashTableStrategy):
        self.strategy = strategy

    def insert(self, key, value):
        self.strategy.insert(key, value)

    def search(self, key):
        return self.strategy.search(key)

    def delete(self, key):
        self.strategy.delete(key)

# ---------------------
# Demo (Test Code)
# ---------------------
print("Using Chaining Strategy")
ht = HashTable(HashTableChaining())
ht.insert("apple", "$4 Trillion")
ht.insert("elppa", "reverse")  # hashes to same index
print("Search apple:", ht.search("apple"))     # fruit
print("Search elppa:", ht.search("elppa"))     # reverse
ht.delete("apple")
print("Search apple after delete:", ht.search("apple"))  # None

print("\nUsing Direct Strategy")
ht2 = HashTable(HashTableDirect())
ht2.insert("apple", "$4 Trillion")
ht2.insert("elppa", "reverse")  # overwrites if same index
print("Search apple:", ht2.search("apple"))
print("Search elppa:", ht2.search("elppa"))
