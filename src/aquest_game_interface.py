'''
aquest_game.py

CS 5001
Fall 2019
Homework 7/ Final Project

Student name: Samuel Engida

    CS 5001 HW 7 Problem 1: Using what has been acquired in CS 5001 to create
    an old_class adventure game. Using Tkinter to create a user interface for
    aquest_game.py
    '''
from room import *
from aquest_game import *
DIR_LABELS = ['N', 'S', 'E', 'W']
OPTIONS = DIR_LABELS + ['I', 'T', 'D', 'U', 'L', 'Q']
QUESTION = 'What do you want to do? '
from tkinter import *

# 
aquest_rooms_lst, acquest_rooms_keys = get_file('aquest_rooms.txt')
aquest_items_lst, acquest_items_keys = get_file('aquest_items.txt')
puzzles_n_monsters_lst, puzles_n_monsters_keys = get_file('puzzles_n_monsters.txt')

EMPTY = ''

items = create_objects(aquest_items_lst, acquest_items_keys)
rooms = create_objects(aquest_rooms_lst, acquest_rooms_keys, [], items)
puzzles_n_monsters = create_objects(puzzles_n_monsters_lst, puzles_n_monsters_keys, rooms, items)
    
game = Game(rooms)
'''
class: GameInterface
Description:
The class GameInterface instantiates various tkinter GUI objects to create a GUI for the
Align auest game. The class also interacts with classes/functions in room.py and aquest_game
to perform tasks Button objects demand. The class has various methods to handle the various
Button objects.
'''
class GameInterface:
    def __init__ (self):

        # Instantiation of the window and objects on the window
        self.window = Tk()
        self.window.title('Align Quest')
        courtyard_img = PhotoImage(file = game.current_room.picture)
        main_frame = Frame(self.window)
        main_frame.pack(side = LEFT, fill = BOTH)
        self.image = Label(main_frame)
        self.image['image'] = courtyard_img
        self.image.grid(row = 1, column = 1)
        text_frame = Frame(self.window)
        text_frame.pack(side = LEFT, fill = BOTH)
        buttons_frame = Frame(self.window)
        buttons_frame.pack(side = RIGHT)
        self.room_name = Label(text_frame, text = game.current_room.name, wraplength = 300,
                                font = 'Helvetica 12 bold')
        self.room_description = Label(text_frame, text = game.current_room.description,
                               wraplength = 300, font = 'Helvetica 10')        
        for each in game.current_room.items:
            self.room_items_text = each.name + ' here in the room.\n'
        self.room_items = Label(text_frame, text = each.name + ' here in the room', font = 'Helvetica 10',
                                    wraplength = 300)
        self.room_warning = Label(text_frame, text = '', font = 'Helvetica 10',
                                wraplength = 300)
        self.room_name.grid( row = 1 , column = 1, columnspan = 2)
        self.room_description.grid( row = 2, column = 1, columnspan = 2)
        self.room_items.grid( row = 3, column = 1, columnspan = 2)
        self.room_warning.grid( row = 4, column = 1, columnspan = 2)
        self.north = Button(buttons_frame, text = 'North', command = self.process_north)
        self.north.grid(row = 1, padx = 5, pady =5, column = 11, sticky = E)
        self.south = Button(buttons_frame, text = 'South', command = self.process_south)
        self.south.grid(row = 2, padx = 5, pady =5, column = 11, sticky = E)
        self.east = Button(buttons_frame, text = 'East', command = self.process_east)
        self.east.grid(row = 3, padx = 5, pady =5, column = 11, sticky = E)
        self.west = Button(buttons_frame, text = 'West', command = self.process_west)
        self.west.grid(row = 4, padx = 5, pady =5, column = 11, sticky = E)
        self.take = Button(buttons_frame, text = 'Take', command = self.process_take)
        self.take.grid(row = 5,padx = 5, pady =5, column = 11, sticky = E)
        self.look = Button(buttons_frame, text = 'Look', command = self.process_look)
        self.look.grid(row = 6, padx = 5, pady =5, column = 11, sticky = E)
        self.use = Button(buttons_frame, text = 'Use', command = self.process_use)
        self.use.grid(row = 7, padx = 5, pady =5, column = 11, sticky = E)
        self.drop = Button(buttons_frame, text = 'Drop', command = self.process_drop)
        self.drop.grid(row = 8, padx = 5, pady =5, column = 11, sticky = E)
        self.inventory = Button(buttons_frame, text = 'Inventory',
                                command = self.process_inventory)
        self.inventory.grid(row = 9, padx = 5, pady =5, column = 11, sticky = E)
        self.quit = Button(buttons_frame, text = 'Quit', command = self.process_quit)
        self.quit.grid(row = 10, rowspan = 2, padx = 5, pady = 5, column = 11, sticky = E)

        self.window.mainloop()
    def process_quit(self):
        # handles quit button.
        title = 'Quit'
        rank, score = game.rank()
        msg = ('Your Score is: ' + str(score) + '\n' +
               'You are a ' + rank + '\n' +
               'Good bye!')
        self.popupmsg(title, msg, '')
    def update_popup(self, feedback, msg):
        # updates popup message for all buttons that require a pop up
        self.label.configure(text = msg)
        self.label.text = msg
        self.examination.configure(text = feedback)
        self.examination.text = feedback
    def look_handler(self):
        # handles the look button
        to_be_examined = (self.entry.get()).upper()
        item_desc = game.look(to_be_examined)
        msg = 'Looking for ' + to_be_examined + '.........'
        self.update_popup(item_desc, msg)
    def take_handler(self):
        # handles the take button
        to_be_taken = (self.entry.get()).upper()
        take_feedback = game.take(to_be_taken)
        msg = 'Taking ' + to_be_taken + '........'
        self.update_popup(take_feedback, msg)
        self.update_items()
    def drop_handler(self):
        # handles the drop button 
        to_be_dropped = (self.entry.get()).upper()
        drop_feedback = game.drop(to_be_dropped)
        msg = 'Droping ' + to_be_dropped + '........'
        self.update_popup(drop_feedback, msg)
        self.update_items()
    def use_handler(self):
        # handles the use button
        solution = (self.entry.get()).upper()
        inventory_names = game.inventory_names
        msg = 'Using ' + solution + '........'
        if solution in game.inventory_names:
            if items[solution].has_use_remaining():
                items[solution].use()
                use_feedback = game.solve(solution, items)
                self.room_description.configure(text = game.current_room.contextual_description())
                self.room_description.text = game.current_room.contextual_description()
                self.room_warning.configure(text = '')
                self.room_warning.text = ''
                self.update_popup(use_feedback, msg)
                self.update_items()
            else:
                self.update_popup('You have no uses left for this item!', msg)
        else:
            self.update_popup('No such item in your inventory', msg)
    def update_items(self):
        # updates items displayed in current room
        self.room_items.configure(text = EMPTY)
        self.room_items_text = EMPTY
        if len(game.current_room.items) > 0:
            for each in game.current_room.items:
                self.room_items_text += each.name + ' here in the room.\n'
            self.room_items.configure(text = self.room_items_text)
            self.room_items.text = self.room_items_text
        else:
            self.room_items.configure(text = EMPTY)
            self.room_items.text = EMPTY
    def popupmsg(self, title, msg, handler):
        # creates a popup window and labels, entry fields, and buttons associated to it
        popup = Tk()
        popup.wm_title(title)
        popup.minsize(250, 200)
        self.label = Label(popup, text = msg, font = 'Helvetica 10')
        self.label.pack(side = 'top', fill = 'x', pady = 10)
        self.examination = Label(popup, text = EMPTY, font = 'Helvetica 10', wraplength = 500)
        self.examination.pack(side = 'top', fill = 'x', pady = 10)
        # makes sure Inventory popup has one button only
        if title == 'Inventory':
            okay_btn = Button(popup, text = 'Okay', command = popup.destroy)
            okay_btn.pack(side = BOTTOM)
        # makes sure the Quit popup has one button only and that, this button
        # makes sure the all windows are destoryed
        elif title == 'Quit':
            exit_btn = Button(popup, text = 'Exit', command =lambda:[
                             popup.destroy(),self.window.destroy()])
            exit_btn.pack(side = BOTTOM)
        else:
            self.entry = Entry(popup, width = 20)
            self.entry.pack()
            okay_btn = Button(popup, text = 'Okay', command = handler)
            okay_btn.pack(side = LEFT)
            cancel_btn = Button(popup, text = 'Go back', command = popup.destroy)
            cancel_btn.pack(side = RIGHT)
        popup.mainloop()
                          
    def move(self, movement, moved):
        # handles button clicks indicating movement in any of the 4 directions
        if moved:
            current_room_image = PhotoImage(file = game.current_room.picture)
            self.image.configure(image = current_room_image)
            self.image.image = current_room_image
            self.room_name.configure(text = game.current_room.name)
            self.room_name.text = game.current_room.name
            self.room_description.configure(text = game.current_room.contextual_description())
            self.room_description.text = game.current_room.contextual_description()
            self.update_items()
            self.room_warning.configure(text = EMPTY)
            self.room_warning.text = EMPTY
            
        else:
            self.room_warning.configure(text = movement)
            self.room_warning.text = movement
    def process_north(self):
        # bridge between the north button and the move method
        movement, moved = game.move(rooms,'N', puzzles_n_monsters)
        self.move(movement, moved)
    def process_south(self):
        # bridge between the south button and the move method
        movement, moved = game.move(rooms,'S', puzzles_n_monsters)
        self.move(movement, moved)
    def process_east(self):
        # bridge between the east button and the move method
        movement, moved = game.move(rooms,'E', puzzles_n_monsters)
        self.move(movement, moved)
    def process_west(self):
        # bridge between the west button and the move method
        movement, moved = game.move(rooms,'W', puzzles_n_monsters)
        self.move(movement, moved)
    def process_look(self):
        # bridge between the look button and the look_hanlder method
        title = 'Look'
        msg = 'What do you want to look at?'
        self.popupmsg(title, msg, self.look_handler)
    def process_take(self):
        # bridge between the look button and the look_hanlder method
        title = 'Take'
        msg = 'What do you want to take?'
        self.popupmsg(title, msg, self.take_handler)
    def process_drop(self):
        # bridge between the drop button and the drop_hanlder method
        title = 'Drop'
        msg = 'What do you want to drop?'
        self.popupmsg(title, msg, self.drop_handler)
    def process_use(self):
        # bridge between the use button and the use_hanlder method
        title = 'Use'
        msg = 'Which Item do you want to use?'
        self.popupmsg(title, msg, self.use_handler)
    def process_inventory(self):
        # bridge between the inventory button and the inventory_hanlder method
        title = 'Inventory'
        if len(game.inventory) == 0:
            msg = 'You have nothing in your inventory'
            self.popupmsg(title, msg, '')
        else:
            msg = 'Your Inventory has the following:\n'
            for each in game.inventory_names:
                msg += each + '\n'
            self.popupmsg(title, msg, '')

def main():
    GameInterface()

main()
