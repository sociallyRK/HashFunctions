# ---------------------
# Hash Function
# ---------------------
def basic_hash(key, table_size):
    return sum(ord(c) for c in key) % table_size

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
        print(f"Key '{key}' not found in chained list.")




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
    def __init__(self, table_size=11):
        self.table_size = table_size
        self.table = [None] * self.table_size

    def insert(self, key, value):
        index = basic_hash(key, self.table_size)
        self.table[index] = (key, value)

    def search(self, key):
        index = basic_hash(key, self.table_size)
        if self.table[index] and self.table[index][0] == key:
            return self.table[index][1]
        return None

    def delete(self, key):
        index = basic_hash(key, self.table_size)
        if self.table[index] and self.table[index][0] == key:
            self.table[index] = None
        else:
            print(f"Key '{key}' not found in direct table.")

# ---------------------
# Chaining with LinkedList (Version 2)
# ---------------------
class HashTableChaining(HashTableStrategy):
    def __init__(self, table_size=11):
        self.table_size = table_size
        self.table = [LinkedList() for _ in range(self.table_size)]

    def insert(self, key, value):
        self.table[basic_hash(key, self.table_size)].insert(key, value)

    def search(self, key):
        return self.table[basic_hash(key, self.table_size)].search(key)

    def delete(self, key):
        self.table[basic_hash(key, self.table_size)].delete(key)

class HashTableLinearProbing(HashTableStrategy):
    def __init__(self, table_size=11):
        self.table_size = table_size
        self.table = [None] * self.table_size

    def insert(self, key, value):
        # Get initial index from hash function
        index = basic_hash(key, self.table_size)
        start_index = index

        # Linear probing: move forward until empty or matching key found
        while self.table[index] is not None and self.table[index][0] != key:
            index = (index + 1) % self.table_size
            if index == start_index:
                print("HashTable is full")
                return

        # Insert new pair or update existing key
        self.table[index] = (key, value)

    def search(self, key):
        # Start at hashed index
        index = basic_hash(key, self.table_size)
        start_index = index

        # Linearly probe until key is found or wraparound completes
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.table_size
            if index == start_index:
                break
        return None  # Not found

    def delete(self, key):
        # Start at hashed index
        index = basic_hash(key, self.table_size)
        start_index = index

        # Probe until match or loop
        while self.table[index] is not None:
            if self.table[index][0] == key:
                self.table[index] = None
                return
            index = (index + 1) % self.table_size
            if index == start_index:
                break
        print(f"Key '{key}' not found in linear probing table.")


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
def main(): 
    print("Using Chaining Strategy")
    ht = HashTable(HashTableChaining(table_size=11))

    ht.insert("apple", "$4 Trillion")
    ht.insert("elppa", "reverse")  # hashes to a different index
    print("Search apple:", ht.search("apple"))     # $4 Trillion
    print("Search elppa:", ht.search("elppa"))     # reverse
    ht.delete("apple")
    print("Search apple after delete:", ht.search("apple"))  # None

    print("\nUsing Direct Strategy")
    ht2 = HashTable(HashTableDirect(table_size=11))

    ht2.insert("apple", "$4 Trillion")
    ht2.insert("elppa", "reverse")
    print("Search apple:", ht2.search("apple"))
    print("Search elppa:", ht2.search("elppa"))

    print("\nTesting collision in Direct Strategy")
    ht2.insert("papel", "overwrites apple")  # ✅ fixed
    print("Search apple:", ht2.search("apple"))   # ✅ fixed
    print("Search papel:", ht2.search("papel"))   # ✅ fixed

    print("papel hashes to:", basic_hash("papel", 11))  # 2
    print("apple hashes to:", basic_hash("apple", 11))  # 2
    print("elppa hashes to:", basic_hash("elppa", 11))  # 9


if __name__ == "__main__":
    main()

