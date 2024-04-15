from buggy_code1 import LinkedList

""" vvv TEST CASES - DO NOT MODIFY vvv """

llist = LinkedList()
assert llist.getAsPythonList() == []
assert llist.sizeOfLL() == 0

llist.insertAtBegin(3)
assert llist.getAsPythonList() == [3]
assert llist.sizeOfLL() == 1
assert llist.at(0) == 3
index = False
try:
    llist.at(1)
except:
    index = True
assert index
llist.removeFirstNode()
assert llist.getAsPythonList() == []
assert llist.sizeOfLL() == 0
index = False
try:
    llist.at(1)
except:
    index = True
assert index

llist.insertAtEnd(3)
assert llist.getAsPythonList() == [3]
assert llist.sizeOfLL() == 1
assert llist.at(0) == 3
index = False
try:
    llist.at(1)
except:
    index = True
assert index
llist.removeLastNode()
assert llist.getAsPythonList() == []
assert llist.sizeOfLL() == 0
index = False
try:
    llist.at(1)
except:
    index = True
assert index

llist.insertAtIndex(3, 0)
assert llist.getAsPythonList() == [3]
assert llist.sizeOfLL() == 1
assert llist.at(0) == 3
index = False
try:
    llist.at(1)
except:
    index = True
assert index
llist.removeAtIndex(0)
assert llist.getAsPythonList() == []
assert llist.sizeOfLL() == 0
index = False
try:
    llist.at(1)
except:
    index = True
assert index

llist.insertAtBegin(3)
llist.removeNode(3)
assert llist.getAsPythonList() == []
assert llist.sizeOfLL() == 0
index = False
try:
    llist.at(1)
except:
    index = True
assert index

for i in range(10):
    llist.insertAtBegin(i)
assert llist.sizeOfLL() == 10
assert llist.getAsPythonList() == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
for i in range(10):
    assert llist.at(i) == 10-i-1
for i in range(10):
    assert llist.at(llist.sizeOfLL() - 1) == i
    llist.removeLastNode()
assert llist.getAsPythonList() == []
assert llist.sizeOfLL() == 0
index = False
try:
    llist.at(1)
except:
    index = True
assert index

for i in range(10):
    llist.insertAtEnd(i)
assert llist.sizeOfLL() == 10
assert llist.getAsPythonList() == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
for i in range(10):
    assert llist.at(i) == i
for i in range(10):
    assert llist.at(0) == i
    llist.removeFirstNode()
assert llist.getAsPythonList() == []
assert llist.sizeOfLL() == 0
index = False
try:
    llist.at(1)
except:
    index = True
assert index

for i in range(10):
    llist.insertAtIndex(i, i)
assert llist.sizeOfLL() == 10
assert llist.getAsPythonList() == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
for i in range(10):
    assert llist.at(i) == i
for i in range(10):
    assert llist.at(0) == i
    llist.removeAtIndex(0)
assert llist.getAsPythonList() == []
assert llist.sizeOfLL() == 0
index = False
try:
    llist.at(1)
except:
    index = True
assert index



print("All tests passed!")
""" ^^^ TEST CASES - DO NOT MODIFY ^^^ """