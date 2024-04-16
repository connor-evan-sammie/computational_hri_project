from buggy_code1 import LinkedList

""" vvv TEST CASES - DO NOT MODIFY vvv """

print("Empty List Tests")
llist = LinkedList()
print(f"\tCurrent list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == []
print(f"\tSize: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 0

print("Test suite 1: insertAtBegin and removeFirstNode")
llist.insertAtBegin(3)
print(f"\tCurrent list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == [3] # Error line!
print(f"\tSize: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 1 # Error line!
print(f"\tList at idx 0: {llist.at(0)}")
assert llist.at(0) == 3
index = False
try:
    llist.at(1)
except:
    index = True
assert index
llist.removeFirstNode()
print(f"\tCurrent list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == [] # Error line!
print(f"\tSize: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 0
index = False
try:
    llist.at(1)
except:
    index = True
assert index

print("Test suite 2: insertAtEnd and removeFirstNode")
llist.insertAtEnd(3) # Error line!
print(f"\tCurrent list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == [3]
print(f"\tSize: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 1
print(f"\tList at idx 0: {llist.at(0)}")
assert llist.at(0) == 3
index = False
try:
    llist.at(1)
except:
    index = True
assert index
llist.removeLastNode()
print(f"\tCurrent list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == []
print(f"\tSize: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 0
index = False
try:
    llist.at(1)
except:
    index = True
assert index

print("Test suite 3: insertAtIndex and removeAtIndex")
llist.insertAtIndex(3, 0)
print(f"\tCurrent list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == [3]
index = False
try:
    llist.insertAtIndex(5, 3)
except:
    index = True
assert index
print(f"\tSize: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 1
print(f"\tList at idx 0: {llist.at(0)}")
assert llist.at(0) == 3
index = False
try:
    llist.at(1)
except:
    index = True
assert index
llist.removeAtIndex(0)
print(f"\tCurrent list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == []
print(f"\tSize: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 0
index = False
try:
    llist.at(1)
except:
    index = True
assert index

print("Test suite 4: insertAtBegin and removeNode")
llist.insertAtBegin(3)
llist.removeNode(3)
print(f"\tCurrent list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == []
print(f"\tSize: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 0
index = False
try:
    llist.at(1)
except:
    index = True
assert index

print("Test suite 5: adding and removing multiple 1")
for i in range(10):
    llist.insertAtBegin(i)
print(f"\tSize: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 10
print(f"\tCurrent list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
for i in range(10):
    print(f"\tList at idx {i}: {llist.at(i)}")
    assert llist.at(i) == 10-i-1
for i in range(10):
    print(f"\tList at idx {llist.at(llist.sizeOfLL() - 1)}: {llist.at(llist.sizeOfLL() - 1)}")
    assert llist.at(llist.sizeOfLL() - 1) == i
    llist.removeLastNode() # Error line!
print(f"\tCurrent list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == []
print(f"\tSize: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 0
index = False
try:
    llist.at(1)
except:
    index = True
assert index

print("Test suite 6: adding and removing multiple 2")
for i in range(10):
    llist.insertAtEnd(i)
print(f"\tSize: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 10
print(f"\tCurrent list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
for i in range(10):
    print(f"\tList at idx {i}: {llist.at(i)}")
    assert llist.at(i) == i
for i in range(10):
    print(f"\tList at idx 0: {llist.at(0)}")
    assert llist.at(0) == i
    llist.removeFirstNode()
print(f"\tCurrent list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == []
print(f"\tSize: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 0
index = False
try:
    llist.at(1)
except:
    index = True
assert index

print("Test suite 7: adding and removing multiple 3")
for i in range(10):
    llist.insertAtIndex(i, i)
print(f"\tSize: {llist.sizeOfLL()}") # Error is thrown here!
assert llist.sizeOfLL() == 10
print(f"\tCurrent list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
for i in range(10):
    print(f"\tList at idx {i}: {llist.at(i)}")
    assert llist.at(i) == i
for i in range(10):
    print(f"\tList at idx 0: {llist.at(0)}")
    assert llist.at(0) == i
    llist.removeAtIndex(0)
print(f"\tCurrent list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == []
print(f"\tSize: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 0
index = False
try:
    llist.at(1)
except:
    index = True
assert index

print("Test suite 8: adding and removing with removeNode 1")
for i in range(10):
    llist.insertAtIndex(i, i)
print(f"\tSize: {llist.sizeOfLL()}") # Error is thrown here!
assert llist.sizeOfLL() == 10
print(f"\tCurrent list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
for i in range(10):
    print(f"\tList at idx {i}: {llist.at(i)}")
    assert llist.at(i) == i
for i in range(10):
    print(f"\tList at idx 0: {llist.at(0)}")
    assert llist.at(0) == i
    llist.removeNode(i)
print(f"\tCurrent list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == []
print(f"\tSize: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 0
index = False
try:
    llist.at(1)
except:
    index = True
assert index

print("Test suite 8: adding and removing with removeNode 2")
for i in range(10):
    llist.insertAtIndex(i, i)
print(f"\tSize: {llist.sizeOfLL()}") # Error is thrown here!
assert llist.sizeOfLL() == 10
print(f"\tCurrent list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
for i in range(10):
    print(f"\tList at idx {i}: {llist.at(i)}")
    assert llist.at(i) == i
for i in range(10):
    print(f"\tList at idx {10-i-1}: {llist.at(10-i-1)}")
    assert llist.at(10-i-1) == 10-i-1
    llist.removeNode(10-i-1)
print(f"\tCurrent list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == []
print(f"\tSize: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 0
index = False
try:
    llist.at(1)
except:
    index = True
assert index

print("All tests passed!")
""" ^^^ TEST CASES - DO NOT MODIFY ^^^ """