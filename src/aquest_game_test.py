'''
aquest_game_test.py

CS 5001
Fall 2019
Homework 7/ Final Project

Student name: Samuel Engida

    CS 5001 HW 7 Problem 1: Using Python's Unittest to test the Game class.

'''
import unittest
from aquest_game import*
aquest_rooms_lst, acquest_rooms_keys = get_file('aquest_rooms.txt')
aquest_items_lst, acquest_items_keys = get_file('aquest_items.txt')
puzzles_n_monsters_lst, puzles_n_monsters_keys = get_file('puzzles_n_monsters.txt')

items = create_objects(aquest_items_lst, acquest_items_keys)
rooms = create_objects(aquest_rooms_lst, acquest_rooms_keys, [], items)
puzzles_n_monsters = create_objects(puzzles_n_monsters_lst, puzles_n_monsters_keys, rooms, items)

class AquestGameTest(unittest.TestCase):
    ''' class to test all the methods of the Game class
        imports from TestCase

        Compares inputs and expected outputs with all Game methods:
         * __init__, all initializations
         * move, movement in possible direction, direction with obstacles
         and impossible direction
         * look a successful and unsuccessful look
         * take successul and unsuccessful takes
         * drop successul and unsuccessful drops
         * solve successul and unsuccessful use of items
         * rank Correct display of ratings and scores
         * __eq__, checking the == operator
    '''

    def test_init(self):
        self.game = Game(rooms)
        self.assertEqual(self.game.name, 'game')
        self.assertEqual(self.game.current_room.name, 'Courtyard')
        self.assertEqual(len(self.game.inventory), 0)
        self.assertEqual(len(self.game.inventory_names), 0)
        self.assertEqual(self.game.inventory_weights, 0)
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.item_puzzle_count, 0)
    def test_move(self):
        self.game =Game(rooms)
        expected_output = 'Mansion Entrance'
        feedback, validity = self.game.move(rooms, 'N', puzzles_n_monsters)
        self.assertEqual(feedback.name, expected_output)
        self.assertEqual(validity, True)
        expected_output = 'Foyer'
        feedback, validity = self.game.move(rooms, 'N', puzzles_n_monsters)
        self.assertEqual(feedback.name, expected_output)
        self.assertEqual(validity, True)
        expected_output = '>>>>>>>You can\'t go in this direction.<<<<<<<<'
        feedback, validity = self.game.move(rooms, 'N', puzzles_n_monsters)
        self.assertEqual(feedback, expected_output)
        self.assertEqual(validity, False)
        feedback, validity = self.game.move(rooms, 'E', puzzles_n_monsters)
        feedback, validity = self.game.move(rooms, 'E', puzzles_n_monsters)
        expected_output = ('An spooky, eerie library. You walked into this eerie '
                           +'library FROM the west. Another room is north. Books are '+
                           'rustling by themselves on the bookshelf. You hear a voice '+
                           'whisper: "~Find Even Numbers Only~". Yikes. That\'s ' +
                           'creepy. Maybe we should leave?' +
                           '\nThe room has an obstacle')
        
        self.assertEqual(feedback, expected_output)
        self.assertEqual(validity, False)
    def test_look(self):
        self.game = Game(rooms)
        expected_output = ('Cordless Wahl hair clippers for pets or humans. '+
                            'The battery low light is blinking')
        feedback = self.game.look('HAIR CLIPPERS')
        self.assertEqual(feedback, expected_output)
        feedback, validity = self.game.move(rooms, 'N', puzzles_n_monsters)
        expected_output = '><><><><>< NO SUCH ITEM IN THIS ROOM ><><><><><'
        feedback = self.game.look('HAIR CLIPPERS')
        self.assertEqual(feedback, expected_output)
        
    def test_take(self):
        self.game = Game(rooms)
        expected_output = 'HAIR CLIPPERS added to your inventory'
        feedback = self.game.take('HAIR CLIPPERS')
        self.assertEqual(feedback, expected_output)
        hidden_chamber_room_index = 4
        self.game = Game(rooms[hidden_chamber_room_index:])
        expected_output = 'Item too heavy, can\'t carry it'
        feedback = self.game.take('DESK')
        self.assertEqual(feedback, expected_output)
        self.game.inventory_weights = 10
        feedback = self.game.take('ALGORITHMS BOOK')
        expected_output = 'The inventory is full, please drop some items'
        self.assertEqual(feedback, expected_output)
        
    def test_drop(self):
        self.game = Game(rooms[1:])
        self.game.take('THUMB DRIVE')
        self.game.move(rooms, 'N', puzzles_n_monsters)
        feedback = self.game.drop('THUMB DRIVE')
        expected_output = 'THUMB DRIVE dropped in Foyer'
        self.assertEqual(feedback, expected_output)
        feedback = self.game.drop('THUMB DRIVE')
        expected_output = '><><><><>< NO SUCH ITEM IN YOUR INVENTORY ><><><><><'
        self.assertEqual(feedback, expected_output)
        item_no_in_room = len(self.game.current_room.items)
        expected_output = 2
        self.assertEqual(item_no_in_room, expected_output)
    def test_solve(self):
        self.game = Game(rooms[2:])
        feedback = self.game.solve('HAIR CLIPPERS', items)
        expected_output = ('Woohoo! You have used the ' +
                           'HAIR CLIPPERS' + ' on the ' +
                           'Teddy Bear' +'\n' + 'The ' +
                           'Teddy Bear' + ' has been defeated. It is not moving.')
        self.assertEqual(feedback, expected_output)
        
        self.game.move(rooms, 'E', puzzles_n_monsters)
        feedback = self.game.solve('MOD_2', items)
        expected_output = ('You have successfully passed the ' +
                           'Mod_Spooky_Voice')
        self.assertEqual(feedback, expected_output)
        
        feedback = self.game.solve('HAIR CLIPPERS', items)
        expected_output = ('HAIR CLIPPERS' +  ' didn\'t work on '
                           + 'Mod_Spooky_Voice')
        self.assertEqual(feedback, expected_output)

        self.game.move(rooms, 'W', puzzles_n_monsters)
        current_room, va =self.game.move(rooms, 'S', puzzles_n_monsters)
        feedback = self.game.solve('MOD_2', items)
        expected_output = ('Nothing happened')
        self.assertEqual(feedback, expected_output)
    def test_rank(self):
        # No need to check scores since scores are assigned here.
        self.game = Game(rooms)
        self.game.score = 4
        feedback, score = self.game.rank()
        expected_output = 'Begineer'
        self.assertEqual(feedback, expected_output)

        self.game.score = 190
        feedback, score = self.game.rank()
        expected_output = 'Amateur'
        self.assertEqual(feedback, expected_output)

        self.game.score = 700
        feedback, score = self.game.rank()
        expected_output = 'Professional'
        self.assertEqual(feedback, expected_output)

        self.game.score = 1005
        feedback, score = self.game.rank()
        expected_output = 'World Class'
        self.assertEqual(feedback, expected_output)

        self.game.score = 10000
        feedback, score = self.game.rank()
        expected_output = 'Legend'
        self.assertEqual(feedback, expected_output)
              
def main():
    unittest.main(verbosity = 3) # 1 - 3, 3 being most verbose

main()
