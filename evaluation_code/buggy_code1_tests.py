from buggy_code1 import LinkedList

""" vvv TEST CASES - DO NOT MODIFY vvv """

llist = LinkedList()
print(f"Current list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == []
print(f"Size: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 0

llist.insertAtBegin(3)
print(f"Current list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == [3]
print(f"Size: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 1
print(f"List at idx 0: {llist.at(0)}")
assert llist.at(0) == 3
index = False
try:
    llist.at(1)
except:
    index = True
assert index
llist.removeFirstNode()
print(f"Current list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == []
print(f"Size: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 0
index = False
try:
    llist.at(1)
except:
    index = True
assert index

llist.insertAtEnd(3)
print(f"Current list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == [3]
print(f"Size: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 1
print(f"List at idx 0: {llist.at(0)}")
assert llist.at(0) == 3
index = False
try:
    llist.at(1)
except:
    index = True
assert index
llist.removeLastNode()
print(f"Current list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == []
print(f"Size: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 0
index = False
try:
    llist.at(1)
except:
    index = True
assert index

llist.insertAtIndex(3, 0)
print(f"Current list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == [3]
print(f"Size: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 1
print(f"List at idx 0: {llist.at(0)}")
assert llist.at(0) == 3
index = False
try:
    llist.at(1)
except:
    index = True
assert index
llist.removeAtIndex(0)
print(f"Current list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == []
print(f"Size: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 0
index = False
try:
    llist.at(1)
except:
    index = True
assert index

llist.insertAtBegin(3)
llist.removeNode(3)
print(f"Current list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == []
print(f"Size: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 0
index = False
try:
    llist.at(1)
except:
    index = True
assert index

for i in range(10):
    llist.insertAtBegin(i)
print(f"Size: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 10
print(f"Current list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
for i in range(10):
    print(f"List at idx {i}: {llist.at(i)}")
    assert llist.at(i) == 10-i-1
for i in range(10):
    print(f"List at idx {llist.at(llist.sizeOfLL() - 1)}: {llist.at(llist.sizeOfLL() - 1)}")
    assert llist.at(llist.sizeOfLL() - 1) == i
    llist.removeLastNode()
print(f"Current list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == []
print(f"Size: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 0
index = False
try:
    llist.at(1)
except:
    index = True
assert index

for i in range(10):
    llist.insertAtEnd(i)
print(f"Size: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 10
print(f"Current list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
for i in range(10):
    print(f"List at idx {i}: {llist.at(i)}")
    assert llist.at(i) == i
for i in range(10):
    print(f"List at idx 0: {llist.at(0)}")
    assert llist.at(0) == i
    llist.removeFirstNode()
print(f"Current list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == []
print(f"Size: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 0
index = False
try:
    llist.at(1)
except:
    index = True
assert index

for i in range(10):
    llist.insertAtIndex(i, i)
print(f"Size: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 10
print(f"Current list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
for i in range(10):
    print(f"List at idx {i}: {llist.at(i)}")
    assert llist.at(i) == i
for i in range(10):
    print(f"List at idx 0: {llist.at(0)}")
    assert llist.at(0) == i
    llist.removeAtIndex(0)
print(f"Current list: {llist.getAsPythonList()}")
assert llist.getAsPythonList() == []
print(f"Size: {llist.sizeOfLL()}")
assert llist.sizeOfLL() == 0
index = False
try:
    llist.at(1)
except:
    index = True
assert index



print("All tests passed!")
""" ^^^ TEST CASES - DO NOT MODIFY ^^^ """