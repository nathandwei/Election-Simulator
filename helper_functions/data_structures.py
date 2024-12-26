from matplotlib.colors import CSS4_COLORS
import random
from faker import Faker

fake = Faker()

# Sets to track used names and colors
used_names = set()
used_colors = set()

# Node
class Node:
    def __init__(self, data):
        self.data = data
        self.color = self._generate_unique_color()
        self.name = self._generate_unique_name()
        self.prev = None
        self.next = None

    def _generate_unique_color(self):
        color = random.choice(list(CSS4_COLORS.values()))
        while color in used_colors:
            color = random.choice(list(CSS4_COLORS.values()))
        used_colors.add(color)
        return color

    def _generate_unique_name(self):
        name = fake.first_name()
        while name in used_names:
            name = fake.first_name()
        used_names.add(name)
        return name

    def __hash__(self):
        return hash(id(self))

    def __eq__(self, other):
        return self is other

    def __str__(self):
        return f"Node(data={self.data}, name={self.name}, color={self.color})"


# Doubly Linked List (for candidates)
class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def __str__(self):
        build = ""
        if not self.head:
            return "DoublyLinkedList()"
        
        current = self.head
        while current.next:
            build += str(current)+", "
            current = current.next
        build += str(current)+")"
        build = "DoublyLinkedList("+build
        return build

    def __iter__(self):
        current = self.head

        while current:
            yield current
            current = current.next

    def append(self, data):
        new_node = Node(data)
        if not self.head:  # If the list is empty
            self.head = new_node
            return
        current = self.head
        while current.next:  # Traverse to the end
            current = current.next
        current.next = new_node
        new_node.prev = current

    def prepend(self, data):
        new_node = Node(data)
        if not self.head:  # If the list is empty
            self.head = new_node
            return
        self.head.prev = new_node
        new_node.next = self.head
        self.head = new_node

    def delete(self, key):
        if not self.head:  # If the list is empty
            print("List is empty")
            return
        current = self.head
        while current:
            if current.data == key:  # Node to delete is found
                if current.prev:  # Update previous node's next pointer
                    current.prev.next = current.next
                else:  # If the node to delete is the head
                    self.head = current.next
                if current.next:  # Update next node's previous pointer
                    current.next.prev = current.prev
                return
            current = current.next
        return