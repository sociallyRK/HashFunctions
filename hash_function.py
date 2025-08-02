TABLE_SIZE = 11

#basic hash function 
def basic_hash(key):
	return sum(ord(c) for c in key) % TABLE_SIZE

#initialize hash table
hash_table = [None] * TABLE_SIZE

#Insert key= value pair
def insert(key, value):
	global hash_table
	index = basic_hash(key)
	hash_table[index] = (key, value) #Overwrites if collision

#Search for a Key
def search(key):
	global hash_table
	index = basic_hash(key)
	if hash_table[index] and hash_table[index][0] == key:
		return hash_table[index][1]
	return None

#Delete a key
def delete(key):
	global hash_table
	index = basic_hash(key)
	if hash_table[index] and hash_table[index][0] == key:
		hash_table[index] = None

insert("apple", "$4 Trillion")
print("Hash index for 'apple':", basic_hash("apple"))
print("Hash table at that index:", hash_table[basic_hash("apple")])
insert("car", "vehicle")
print("searching apple")
print(search("apple"))
print("Apple does not show up due to a Hash Collision of car overwriting apple")
insert("apple", "$4 Trillion")
delete("apple")
print("searching apple")
print(search("apple"))
print("Apple does not show up due to it being deleted")
insert("apple", "$4 Trillion")
print(search("apple"))