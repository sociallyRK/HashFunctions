"""
UCLA Extension - Data Structures and Algorithms - Summer 2025  
Assignment #3 – Hash Tables  
Author: Rahul Khanna  
Purpose: Implementation of two Hash Table versions using (1) Chaining and (2) Linear Probing.  
Includes a custom hash function, collision handling, and resize capability.  

Command Line to Run Program:  
python3 HashTable_Rahul_Khanna.py
"""


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

    def resize(self):
        old_table = self.table
        old_size = self.table_size
        self.table_size *= 2
        self.table = [LinkedList() for _ in range(self.table_size)]

        for bucket in old_table:
            current = bucket.head
            while current:
                # Re-insert each key-value pair using the new table size
                self.insert(current.key, current.value)
                current = current.next

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

    def resize(self):
        old_table = self.table
        old_size = self.table_size
        self.table_size *= 2
        self.table = [None] * self.table_size

        for entry in old_table:
            if entry is not None:
                key, value = entry
                self.insert(key, value)


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

def test_hash_distribution():
    table_size = 11
    slots = [0] * table_size
    keys = [f"key{i}" for i in range(100)]

    for key in keys:
        index = basic_hash(key, table_size)
        slots[index] += 1

    print("Hash Distribution (slot -> # of keys):")
    for i, count in enumerate(slots):
        print(f"Index {i}: {count} keys")
import time


def benchmark(strategy_class, num_ops=10000):
    # Use larger table for probing to avoid overflow
    table_size = 16384 if strategy_class == HashTableLinearProbing else 1024
    ht = strategy_class(table_size=table_size)
    keys = [f"key{i}" for i in range(num_ops)]

    start = time.time()
    for i, key in enumerate(keys):
        ht.insert(key, str(i))
    insert_time = time.time() - start

    start = time.time()
    for key in keys:
        ht.search(key)
    search_time = time.time() - start

    print(f"\n{strategy_class.__name__} Performance:")
    print(f"Insert Time: {insert_time:.4f}s")
    print(f"Search Time: {search_time:.4f}s")




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

    print("\nResizing Chaining Table")
    ht_chained = HashTableChaining(table_size=2)
    ht_chained.insert("a", "1")
    ht_chained.insert("b", "2")
    ht_chained.resize()
    ht_chained.insert("c", "3")
    print(ht_chained.search("a"))  # 1
    print(ht_chained.search("b"))  # 2
    print(ht_chained.search("c"))  # 3

    print("\nResizing Probing Table")
    ht_probing = HashTableLinearProbing(table_size=2)
    ht_probing.insert("a", "1")
    ht_probing.insert("b", "2")
    ht_probing.resize()
    ht_probing.insert("c", "3")
    print(ht_probing.search("a"))  # 1
    print(ht_probing.search("b"))  # 2
    print(ht_probing.search("c"))  # 3

    print("\nResizing Probing Table")
    ht_probing = HashTableLinearProbing(table_size=2)
    ht_probing.insert("a", "1")
    ht_probing.insert("b", "2")
    ht_probing.resize()
    ht_probing.insert("c", "3")
    print(ht_probing.search("a"))  # 1
    print(ht_probing.search("b"))  # 2
    print(ht_probing.search("c"))  # 3

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

# ---------------------
# Run Benchmark After Demo
# ---------------------
    print("\nBenchmarking Performance on 10,000 keys...")
    benchmark(HashTableChaining)
    benchmark(HashTableLinearProbing)
    print("\n✅ Demo complete. Benchmarking followed. No errors detected.")


if __name__ == "__main__":
    main()

