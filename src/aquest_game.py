'''
aquest_game.py

CS 5001
Fall 2019
Homework 7/ Final Project

Student name: Samuel Engida

    CS 5001 HW 7 Problem 1: Using what has been acquired in CS 5001 to create
    an old_class adventure game.
    '''
from room import *
DIR_LABELS = ['N', 'S', 'E', 'W']
OPTIONS = DIR_LABELS + ['I', 'T', 'D', 'U', 'L', 'Q']
QUESTION = 'What do you want to do? '
def menu(question):
    ''' Function: menu
        Parameter: string, recieves question to be displayed to player
        Returns: string, answer from the player
        Does: Continously asks player for the inputs: N, S, E, W, I, T
              D, U, L, Q until user has typed in one of those.
              If so, the player's answer is returned'''
    while True:
        print('\nPlease enter one of the following commands: ')
        print(' N, S, E, W to go (North, South, East, West) \n' +
              ' I - Print current inventory of Items the player has collected\n' +
              ' T - Take an item from the current room\n' +
              ' D - Drop an item they are carrying in their inventory \n' +
              ' U - Use an item to solve a puzzle or defeat a monster\n' +
              ' L - Look at (examine) an item in the current room\n' +
              ' Q - Quit and exit game')
        answer = input(question).upper()
        if answer in OPTIONS:
            return answer
        else:
            print('Error!, please try again')


def get_file(file_name):
    ''' Function: get_file
        Parameters: string, the name of the file to be opened
        Returns: list, all the lines in the file as elements of a list
        Does: Opens a text file, reads each line of the text file
        and stores each line as elements of a list'''
    infile = open(file_name, 'r')
    info = infile.readlines()
    sorted_info = []
    for each in info:
        sorted_info.append(each)
    infile.close()
    return sorted_info[1:], sorted_info[0][:-1].split('|')

def create_objects(lst, keys, rooms = [], items = {}):
    ''' Funciton: create_objects
        Parameters: lst(list), keys(list), rooms(list), items(dictionary)
                    lst: is the specific list created using get info, it could
                    be a list of lists of each attributes from the
                    aquest_rooms.txt, aquest_items.txt, or puzzles_n_monsters.txt
                    keys: is a list of each labels in the first line of
                    aquest_rooms.txt, aquest_items.txt, or puzzles_n_monsters.txt
                    rooms: is an optional paramter with list carrying the
                    objects of room
                    items: is a dictionary with item name as a list and item objects
                    as a values.
        Returns: puzzles_n_mosnters(dict), rooms(list), items(dictionary)
        Does: creates objects of the classes Room, Item, Puzzle and Monster.
              and then stores the room objects in a list, the item objects in
              a dictionary with the Item's names as keys, the Puzzle and Monster
              objects in a dictionary with the puzzle's and monster's name as
              keys. Finally returns the above created data depending on the
              data requested.
    
    '''
    dictionary = {}

    puzzles_n_monsters = {}
    for i in range(len(lst)):
        temp = lst[i].split('|')
        j = 0
        
        if 'METADATA' in keys:
            keys.remove('METADATA') # stripping off 'METADATA'
        for each in keys:
            if temp[j] == 'T':
                dictionary[each] = True # replacing the T's with True
            elif temp[j] == '*':
                dictionary[each] = False # replacing the *'s with False(consistency)
            else:
                dictionary[each] = temp[j]
            j += 1
            
        if keys[1] == 'Room Name':
            # creating Room objects and storing them
            adjacent_rooms = dictionary['Adjacent Rooms (N S E W)'].split(' ')
            adjacent_room_numbers = []
            for each in adjacent_rooms:
                adjacent_room_numbers.append(int(each))
            rooms.append(Room(int(dictionary['0']), dictionary['Room Name'],
                     dictionary['Description'],
                     adjacent_room_numbers,
                     dictionary['Pictures'][:-1]))
            
            # adding items to rooms
            for each in dictionary['Items'].split(','):
                if each != 'None':
                    rooms[i].add_item(items[each.upper()])
           
        elif keys[0] == 'name':
            # creating Monster objects
            if dictionary['can attack']:
                puzzles_n_monsters[dictionary['name'].upper()] =(Monster(dictionary['name'],
                                                  dictionary['description'],
                                                  dictionary['target'],
                                                  dictionary['active'],
                                                  dictionary['affects target'],
                                                  dictionary['solution'],
                                                  dictionary['effect'],
                                                  dictionary['can attack'],
                                                  dictionary['attack']))
                # adding monster to rooms                
                rooms[int(dictionary['target'][5:])-1].add_monster(puzzles_n_monsters[dictionary['name'].upper()])

              
            else:
                # Creating Puzzle objects
                puzzles_n_monsters[dictionary['name'].upper()] = (Puzzle(dictionary['name'],
                                                  dictionary['description'],
                                                  dictionary['target'],
                                                  dictionary['active'],
                                                  dictionary['affects target'],
                                                  dictionary['solution'],
                                                  dictionary['effect']))
                try:
                    # adding puzzle to rooms
                    rooms[int(dictionary['target'][5:])-1].add_puzzle(puzzles_n_monsters[dictionary['name'].upper()])
                    
                except:
                    # if puzzle doesn't affect rooms adding puzzle to items
                    items[dictionary['target'].upper()].add_puzzle(puzzles_n_monsters[dictionary['name'].upper()])
                    
        elif keys[1] == 'Item Name':
            # creating Item objects
            items[(dictionary['Item Name']).upper()] = (Item(int(dictionary['Item Number']),
                              dictionary['Item Name'].upper(),
                              dictionary['Description'],
                              int(dictionary['Weight']),
                              int(dictionary['Value']),
                              int(dictionary['Uses use_remaining'])))
            

    if len(puzzles_n_monsters) > 0:
        return puzzles_n_monsters
    if len(rooms) > 0:
        return rooms
    if len(items) > 0:
        return items

'''
class: Game
Description:
This class encapsulates all of the behaviours of playing the game. The class
has methods such as: move (makes movement in any of the four directions if
it is possible to move in that direction), look (examine item in current room)
take (take current item in room if inventory requirements are met). drop (drop
items in the current room). solve (use item in inventory to solve puzzles and
defeat monsters). inventory (to have a look at the items in the inventory.) and
rank ( to return scores and ratings).

'''
class Game:
    def __init__(self, rooms):
        self.name = 'game'
        self.current_room = rooms[0]
        self.inventory = []
        self.inventory_names = []
        self.inventory_weights = 0
        self.score = 0
        self.item_puzzle_count = 0
    def move(self, rooms, direction, puzzles_n_monsters):
        directions = self.current_room.adjacent_rooms
        directions_dict = {}
        i = 0
        for each in DIR_LABELS:
            directions_dict[each] = directions[i]
            i += 1
        move_to_room = int(directions_dict[direction])
        if move_to_room > 0:
            self.current_room = rooms[move_to_room-1]
            return self.current_room, True
        elif move_to_room < 0:
            return (self.current_room.contextual_description() +
                    '\nThe room has an obstacle', False)
        else:
            return '>>>>>>>You can\'t go in this direction.<<<<<<<<', False
    
    def look(self, key):
        both_inventory_n_room = self.current_room.items + self.inventory
        for each in both_inventory_n_room:
            if each.name == key:
                return each.contextual_description()
            
        return '><><><><>< NO SUCH ITEM IN THIS ROOM ><><><><><'
    def take(self, item):
        for each in self.current_room.items:
            if (each.name == item):
                if self.inventory_weights + each.weight <= 10:
                    self.inventory.append(each)
                    self.inventory_names.append(each.name)
                    self.current_room.remove_item(each)
                    self.inventory_weights += each.weight
                    self.score += each.value
                    return(each.name + ' added to your inventory')
                elif each.weight >= 10:
                    return('Item too heavy, can\'t carry it')
                elif self.inventory_weights + each.weight > 10:
                    return('The inventory is full, please drop some items')

        return('><><><><>< NO SUCH ITEM IN THIS ROOM ><><><><><')
    def drop(self, item):
        for each in self.inventory:
            if each.name == item:
                self.current_room.add_item(each)
                self.inventory.remove(each)
                self.inventory_names.remove(each.name)
                self.inventory_weights -= each.weight
                self.score -= each.value
                return (item + ' dropped in ' + self.current_room.name)
        return '><><><><>< NO SUCH ITEM IN YOUR INVENTORY ><><><><><'
    def solve(self, solution, items):
        if self.current_room.has_monsters():
            for each in self.current_room.monsters:
                monster_pass_check = each.try_to_solve(solution)
                if monster_pass_check:
                    return_statement = ('Woohoo! You have used the ' +
                                        solution + ' on the ' + each.name +'\n' + each.defeated())
                    self.current_room.reverse_effects()
                    return return_statement
                else:
                    return solution + ' didn\'t work on ' + each.name
        if self.current_room.has_puzzle():
            for each in self.current_room.puzzles:
                puzzle_pass_check = each.try_to_solve(solution)
                if puzzle_pass_check:
                    return_statement = 'You have successfully passed the ' + each.name
                    self.current_room.reverse_effects()
                    return return_statement
                else:
                    return solution +  ' didn\'t work on ' + each.name 
        if self.current_room.has_items():
            for each in self.current_room.items:
                if each.has_puzzle():
                    self.item_puzzle_count += 1
                    for puzzle in each.puzzle:
                        puzzle_pass_check = puzzle.try_to_solve(solution)
                        if puzzle_pass_check:
                            self.current_room.reverse_effects()
                            return 'You have successfully passed the ' + puzzle.name
                        else:
                            return solution + ' didn\'t work on ' + each.name
            return 'Nothing happened'
                    
        if (not self.current_room.has_monsters() and not self.current_room.has_puzzle() and
            self.item_puzzle_count == 0):
            return 'Nothing happened'
               
    def rank(self):
        if self.score <=5:
            return 'Begineer', self.score
        elif self.score <= 200 and self.score > 5:
            return 'Amateur', self.score
        elif self.score > 200 and self.score <= 700:
            return 'Professional', self.score
        elif self.score > 700 and self.score <= 2000:
            return 'World Class', self.score
        elif self.score > 2000:
            return 'Legend', self.score
