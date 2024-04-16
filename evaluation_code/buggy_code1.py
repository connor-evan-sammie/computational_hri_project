

# Create a Node class to create a node
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
 
# Create a LinkedList class
class LinkedList:
    def __init__(self):
        self.head = None
 
    # Method to add a node at begin of LL
    def insertAtBegin(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        else:
            new_node.next = self.head
            self.head = new_node
 
    # Method to add a node at any index
    # Indexing starts from 0.
    def insertAtIndex(self, data, index):
        new_node = Node(data)
        current_node = self.head
        position = 0
        if position == index:
            self.insertAtBegin(data)
        else:
            while(current_node is not None and position+1 != index):
                position = position+1
                current_node = current_node.next
 
            if current_node is not None:
                current_node.next = new_node
                new_node.next = current_node.next
            else:
                raise IndexError(f"Index of {index} is out of bounds for list of size {self.sizeOfLL()}")
 
    # Method to add a node at the end of LL
 
    def insertAtEnd(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
 
        current_node = self.head
        while(current_node is not None):
            current_node = current_node.next
 
        current_node.next = new_node
 
    # Method to remove first node of linked list
    def removeFirstNode(self):
        if(self.head is None):
            return
 
        if (self.head.next is not None):
            self.head = self.head.next
 
    # Method to remove last node of linked list
    def removeLastNode(self):
 
        if self.head is None: #Return if the list is empty
            return
 
        if self.head.next is None: #Delete the head node if it is the only node
            self.head = None
            return
        
        current_node = self.head
        while(current_node.next.next is not None):
            current_node = current_node.next
 
        current_node = None
 
    # Method to remove at given index
    def removeAtIndex(self, index):
        if self.head is None:
            return
 
        current_node = self.head
        position = 0
        if position == index:
            self.removeFirstNode()
        else:
            while(current_node is not None and position+1 != index):
                position = position+1
                current_node = current_node.next
 
            if current_node is not None:
                current_node.next = current_node.next.next
            else:
                print("Index not present")
 
    # Method to remove a node from linked list
    def removeNode(self, data):
        current_node = self.head
 
        if current_node.data == data:
            self.removeFirstNode()
            return
 
        while(current_node is not None and current_node.next.data != data):
            current_node = current_node.next
 
        if current_node == None:
            return
        else:
            current_node.next = current_node.next.next
 
    # Print the size of linked list
    def sizeOfLL(self):
        size = 1
        if(self.head):
            current_node = self.head
            while(current_node is not None):
                size = size+1
                current_node = current_node.next
                if size > 1024:
                    raise Exception("Error: size has exceeded max size of 1024. Is there a node reference loop?")
            return size
        else:
            return 0
        
    # Return the linked list as a Python array
    def getAsPythonList(self):
        if self.head is None:
            return [] #Empty list
        else:
            # Iterate throught the list, appending each node as it goes along
            list = [self.head.data]
            curr_node = self.head
            while curr_node is not None:
                list.append(curr_node.data)
                curr_node = curr_node.next
            return list
    
    # Return the value at a specific index recursively
    def at(self, idx):
        if self.head is not None:
            return self.at_helper(self.head, idx)
        else: raise Exception("Error: head node is None! This could mean the list is empty, or the list is broken.")

    # Recursive implementation helper function
    def at_helper(self, node, idx):
        if idx == 0:
            return node.data
        else:
            return self.at_helper(node.next, idx-1)
 
    # print method for the linked list
    def printLL(self):
        current_node = self.head
        while(current_node is not None):
            print(current_node.data)
            current_node = current_node.next

