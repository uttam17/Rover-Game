# Uttam Kumaran
# CSCI204 - Project 2
# 10/12/2015

""" Game to play 'Lost Rovers'. This is the file you edit.
To make more ppm files, open a gif or jpg in xv and save as ppm raw.
Put the three ADTs in their own files.
"""

from gameboard import *
from random import *

class Game:
    """ Holds all the methods that start and modify the game.

    Can get and set position as well as change the position 

    Attributes:
        self.gui: The gameboard with the given size
        self.rover: The rover object
        self.room: The room with the given size
    """
    SIZE = 15 # rooms are 15x15
    def __init__(self):
        # Creates the gameboard, rover, and room with the given size
        self.gui = GameBoard("Lost Rover", self, Game.SIZE)
        self.rover = Rover()
        self.room = Room(Game.SIZE)
        self.inventory = LinkedList()
        self.portal_stack = MyStack()
    
    def startGame(self):
        """ Starts the GUI.
         
          Returns:
            The graphical interface running
        """
        self.gui.run()

    def getRoverImage(self):
        """ Called by GUI when screen updates.
            Returns image name (as a string) of the rover. 
        (Likely 'rover.ppm') 

            Returns:
                The rover image
        """
        return 'rover.ppm'

    def getRoverLocation(self):
        """ Called by GUI when screen updates.
            Returns location (as a Point).

            Returns:
                The rover position          
             """
        return self.rover.get_position()

    def getImage(self, point):
        """ Called by GUI when screen updates.
            Returns image name (as a string) part, 
        ship component, or portal at the given 
        coordinates. ('engine.ppm' or 'cake.ppm' or 
        'portal.ppm', etc)

        Also handles linking portals and running the gui to
        load new rooms if the rover is on the portal 

            Args:
                point: A point object with coordinates
             
            Returns:
                The image at theat certain coordinate
        """
        x = point.getX()
        y = point.getY()
        item = self.room.get_object(x,y)

        if str(item) == "Part":
            return item.get_image()

        elif str(item) == 'Portal':
            if self._check_if_rover_on_item(item): # Rover on portal
                
                if item.linked_portal != None: # Portal is linked
                    self.room = item.linked_portal.get_room()
                    old_portal = self.portal_stack.pop()
                    old_portal.toggle_portal()

                else: 
                    new_room = Room(Game.SIZE) 
                    # Generates new room with given new_room and a newly generated portal
                    new_portal = Portal(item.x, item.y, new_room, item)
                    self.portal_stack.push(new_room)
                    self._generate_new_room(new_room, new_portal)

                self.gui.run()
            else:
                return item.get_image()

        elif str(item) == 'Ship Component':
            return item.get_image()

    def _check_if_rover_on_item(self, item):
        """ Returns true or false if the rover is on item passed to the function

            Args:
                item: item to check if the rover is on it

            Returns:
                True or false regarding whether the rover is on the item
        """
        return [self.rover.x, self.rover.y] == [item.x, item.y]

    def _generate_new_room(self, room, item):
        """ Generates a new room with the new linked portal added

            Args: 
                room: the room to set
                item: the portal to be added
        """
        self.room = room
        self.room.add_item(item)
        item.set_room(room)
        self.startGame()

    def goUp(self):
        """ Called by GUI when button clicked.
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. 
        """
        self.rover.move_up()

    def goDown(self):
        """ Called by GUI when button clicked. 
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. 
        """
        self.rover.move_down()

    def goLeft(self):
        """ Called by GUI when button clicked. 
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. 

        """
        self.rover.move_left()

    def goRight(self):
        """ Called by GUI when button clicked. 
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. 
        """
        self.rover.move_right()

    def showWayBack(self):
        """ Called by GUI when button clicked.
            Flash the portal leading towards home. 
        """
        if not self.portal_stack.isEmpty():
            self.portal_stack.peek().toggle_portal()

    def getInventory(self):
        """ Called by GUI when inventory updates.
            Returns entire inventory (as a nice string). 
        3 cake
        2 screws
        1 rug
        """
        return str(self.inventory)

    def pickUp(self):
        """ Called by GUI when button clicked. 
        If rover is standing on a part (not a portal 
        or ship component), pick it up and add it
        to the inventory. 

        Checks if the item isn't empty, a portal, or a ship comp. Then cuts off
        the .ppm from the image name. Then if it is in the inventory, increment the count
        up. Otherwise add it to the inventory. After remove it from the room.
        """
        x = self.rover.get_position().getX()
        y = self.rover.get_position().getY()
        item = self.room.get_object(x,y)        
        
        if str(item) not in ['Ship Component', 'Portal', '0']:
            item_name = item.get_image()[:-4].title()

            if self.inventory.check_if_in_list(item_name):
                self.inventory.increment_count(item_name)
            else:
                self.inventory.append(item_name)
            self.room.remove_item(item)
        
    def getCurrentTask(self):
        """ Called by GUI when task updates.
            Returns top task (as a string). 
        'Fix the engine using 2 cake, 3 rugs' or
        'You win!' 
        """
        pass # Your code goes here

    def performTask(self):
        """ Called by the GUI when button clicked.
            If necessary Part are in inventory, and rover
            is on the relevant broken ship piece, then fixes
            ship piece and removes Part from inventory. If
            we run out of tasks, we win. """
        pass # Your code goes here

class Rover:
    """Holds all the data for the rover and functions to apply to it.

    Can get and set position as well as change the position 

    Attributes:
        self.x: The x coord of the rover
        self.y: The y coord of the rover
        self.position: The position object representing the location of the rover
    """
    LOWER_BOUND = 1
    UPPER_BOUND = 14
    def __init__(self):
        self.x = randint(Rover.LOWER_BOUND,Rover.UPPER_BOUND)
        self.y = randint(Rover.LOWER_BOUND,Rover.UPPER_BOUND)
        self.position = Point(self.x, self.y)

    def _set_position(self,x,y):
        """ Sets the position of the rover
        """
        self.position = Point(x,y)

    def get_position(self):
        """ Returns the position of the rover

        """
        return self.position

    def move_up(self):
        """ Modifies the position of the rover to move up 1
        """
        if self.y not in [0]:
            self.y -= 1
        self._set_position(self.x, self.y)

    def move_down(self):
        """ Modifies the position of the rover to move down 1
        """
        if self.y not in [14]:
            self.y += 1
        self._set_position(self.x, self.y)

    def move_left(self):
        """ Modifies the position of the rover to move left 1
        """
        if self.x not in [0]:
            self.x -= 1
        self._set_position(self.x, self.y)

    def move_right(self):
        """ Modifies the position of the rover to move right 1
        """
        if self.x not in [14]:
            self.x += 1
        self._set_position(self.x, self.y)


class Room:
    """The room that is displayed. Holds all the objects.

    Can populate the room, set objects, and initialze the room. Room is populated as soon 
    as the method is called.

    Attributes:
        self.room_matrix: Holds a 2d list of lists that will hold all the objects in the room
    """
    def __init__(self, size):
        self.room_matrix= self._initalize_room(size)
        self._populate_room()
        self.linked_portal = None

    def _populate_room(self):
        """ Populates the room with objects 
          There is a count set for each type of item which represents the max number of that
          type of item allowed in the room. It goes through each position in the matrix and 
          and then randomly* chooses which item. It is not completely random because the case 
          of no item being places is the else. Therefore by setting the range of the choice variable
          greater, there will be a greater frequency of empty spaces.

          Returns:
            The updated matrix with objects
        """
        component_count = 10
        part_count = 9
        portal_count = 2
        max_x = 15
        max_y = 15
        for x in range(max_x):
            for y in range(max_y):
                choice = randint(1,21)

                if self._check_if_empty(x,y):   # IS EMPTY METHOD
                    back_portal_count = 0

                    if choice == 1 and portal_count != 0:
                        self._set_object(x,y, Portal(x,y, self, None))
                        portal_count -= 1

                    elif choice == 2 and part_count != 0:
                        self._set_object(x,y,Part(x,y))
                        part_count -= 1

                    elif choice == 3 and component_count != 0:
                        # Used to limit space for ship components as they must be in center
                        x_coord = randint(6,8)
                        y_coord = randint(6,8)
                        if self.room_matrix != 0:
                            self._set_object(x_coord,y_coord,ShipComponent(x_coord,y_coord))
                        component_count -= 1

                    else:
                        self._set_object(x,y,0)    

        return self.room_matrix

    def toggle_portal(self):
        if self.linked_portal.get_image() == 'portal_flashing.ppm':
            self.linked_portal.change_to_normal()
        else:
            self.linked_portal.change_to_flash()

    def _check_if_empty(self, x, y):
        """ Check if there isn't an object at that point in the room

            Args:
                x: the x coord to check
                y: the y coord to check
            Returns:
                True if space is empty. False otherwise
        """
        return self.room_matrix[x][y] == 0

    def add_item(self, item):
        """ Adds item to the room_matrix in a random empty space

            Args: 
                item: item being added to the room_matrix
        """

        if item.get_image() == 'portal.ppm':
            self.linked_portal = item
        # Only adds one portal
        empty_room_list = []
        count = 1
        for x in range(15):
            for y in range(15): 
                if self.room_matrix[x][y] == 0:
                    empty_room_list += [[x,y]]
        
        selected_coords = choice(empty_room_list)
        empty_x = selected_coords[0]
        empty_y = selected_coords[1]

        if count > 0:
            self._set_object(empty_x, empty_y, item)
            item.x = empty_x
            item.y = empty_y
            count -= 1

    def remove_item(self, item):
        """ Removes item from the room_matrix

            Args:
                item to be removed
        """
        x = item.get_position().getX()
        y = item.get_position().getY()

        self.room_matrix[x][y] = 0

    def get_object(self, x, y):
        """ Returns the object at the specified x and y coords
        """
        return self.room_matrix[x][y]

    def _set_object(self,x,y,object):
        self.room_matrix[x][y] = object

    def _initalize_room(self,size):
        """ Initalizes room with zeros. Size dependent on given input.
        """
        return [[0 for x in range(size)] for y in range(size)]

class Item:
    """Base class for all items

    Able to get position if needed. Image is set as soon as Item is created.

    Attributes:
        self.x: The x coord of the item
        self.y: The y coord of the item
        self.image: The image of the specific item
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = self._set_image()

    def get_position(self):
        """ Returns a Position object using the x an y coords of the item passed to it
        """
        return Point(self.x, self.y)
    def get_image(self):
        """ Gets image of part

        Returns:
            image of part
        """
        return self.image
 
class Portal(Item):
    """Portal class. Child of Item.

    Able to get images.  

    Attributes:
        self.x: The x coord of the item
        self.y: The y coord of the item
        self.image: The image of the specific item
        self.last_room = reference to room portal links to if at all
        self.linked_portal = reference to portal this item is linked to if at all
    """
    def __init__(self, x, y, room, Portal):
        self.x = x
        self.y = y
        self.image = self._set_image()
        self.last_room = room
        self.linked_portal = Portal
    
    def __repr__(self):
        return "Portal"

    def _set_image(self):
        return 'portal.ppm'

    def change_to_flash(self):
        self.image = 'portal-flashing.ppm'

    def change_to_normal(self):
        self.image = 'portal.ppm'

    def set_room(self, room):
        """ Sets the room variable to the given room

        Args:
            room: the room to be set
        """
        self.last_room = room

    def get_room(self):
        """ Gets the last_room reference in the Portal item. Used when traveling through portals
        """
        return self.last_room


class Part(Item): 
    """Part class. Child of Item.

        Able to get image.
    """

    def __repr__(self):
        return "Part"

    def _set_image(self):
        """ Sets the image of the different parts. Random in order to create variation

        Returns:
            The string of the image file needed to be added
        """
        choice = randint(1,5)
        if choice == 1:
            return 'cake.ppm'
        elif choice == 2:
            return 'lettuce.ppm'
        elif choice == 3:
            return 'screw.ppm'
        elif choice == 4:
            return 'bagel.ppm'
        elif choice == 5:
            return 'gear.ppm'


class ShipComponent(Item):
    """ShipComponent class. Child of Item.

        Able to get image.
    """ 

    def __repr__(self):
        return "Ship Component" 

    def _set_image(self):
        """ Sets the image of the different componenets, normal and broken. Random in order to create variation

        Returns:
            The string of the image file needed to be added
        """
        
        choice = randint(1,7)
        if choice == 1:
            return 'cabin.ppm'
        elif choice == 2:
            return 'engine.ppm'
        elif choice == 3:
            return 'exhaust.ppm'
        else:
            # Used to create broken comps as well
            broken_choice = randint(1,3)
            if broken_choice == 1:
                return 'cabinbroken.ppm'
            elif broken_choice == 2:
                return 'enginebroken.ppm'
            elif broken_choice == 3:
                return 'exhaustbroken.ppm'


class Node:
    """A simple Node class

    Data attributes:
        self.name: data of any type to be stored in the node
        self.next: a pointer to the next node. next will be None
            if there are no more nodes.
    """
    def __init__(self, name = None, count = 0, next = None):
        self.name = name
        self.count = count
        self.next = next


class LinkedList:
    """A basic Linked List data structure

    Data attributes:
        self.head: a reference to the first Node in the list.
                self.head will basice None if the list is empty
        self.size: Represents the size of the list. Updated when 
                list is appended
    """

    def __init__(self, python_list = None):
        """ Initializes a new linked list.

        If no arguments are provided, an empty list is created.
        Otherwise, a python
        """
        self.head = None
        self.size = 0

        if python_list is not None:
            self._create_list(python_list)

    def __repr__(self):
        """ Creates a visual representation of the list

        Returns:
            The count of the node then a space then the name of the
            current node. Also places each node on its own line
        """
        linked_list = ""
        curr_node = self.head
        while curr_node:
            linked_list += str(curr_node.count) + " " + str(curr_node.name) + '\n'
            curr_node = curr_node.next
        return linked_list

    def check_if_in_list(self, name):
        """ Checks and returns boolean representing whether or not the 
        given object is in the list by comparing the names of each node

        Args:
            name: the name being checked in the list
        Returns:
            in_list: a boolean representing whether the name is in the list
        """
        curr_node = self.head
        in_list = False

        while (self.head is not None and curr_node is not None): 
            if curr_node.name == str(name):
                in_list = True
            curr_node = curr_node.next
        return in_list

    def increment_count(self, item):
        """ Increments the count up by one for an item. Called when item already
        exists in the list.

            Args:
                item: item to increment count for
        """
        curr_node = self.head
        count = 0
        while count < self.size: 
            if curr_node.name == str(item):
                curr_node.count += 1
                return
            else:
                curr_node = curr_node.next
            count+=1

    def append(self, name):
        """ Appends a new node containing data at the end of the list.

        Args:
            name: the data that will be appended to the current list
        """
        new_node = Node(name, 1)
        if self.head is None:
            self.head = new_node
        else: 
            curr_node = self.head
            while curr_node.next is not None: 
                curr_node = curr_node.next
            curr_node.next = new_node
        self.size += 1


class MyStack:
    """ Implement this Stack ADT using a Python list to hold elements.
         
        Do NOT use the len() feature of lists.
    """
    CAPACITY = 4
    def __init__( self ):
        """ Initialize an empty stack. """

        self._capacity = MyStack.CAPACITY
        self._size = 0
        self._array = [''] * self._capacity

    def isEmpty( self ):
        """ Is the stack empty? 
        Returns True if the stack is empty; False otherwise. """
        return self._array == ['']*self._capacity

    def push( self, item ):
        """ Push the item onto the top of the stack. """
        self._double_if_needed()
        self._array[self._size] = item
        self._size += 1

    def pop( self ):
        """ Pop the top item off the stack and return it. """
        popped_item = self._array[self._size-1]
        self._array[self._size-1] = ''
        self._size -=1
        return popped_item

    def peek( self ):
        """ Return the top item on the stack (does not change the stack). """
        if self._size >=1:
            return self._array[self._size-1]

    def _double_if_needed(self):
        if self._capacity - 1 == self._size:
            self._array += ['']*self._capacity
            self._capacity = self._capacity*2
 

""" Launch the game. """
g = Game()
g.startGame() # This does not return until the game is over
