# Align Quest
Align Quest is an old-school adventure game created using concepts learnt in CS 5001 [2019]. The project uses functions, conditionals, loops, lists, dictionaries, tuples, exception handling, classes, and PyUnit unit test to provide a solution for the project.

Lists and dictionaries are mainly used in the project, while tuples are used for multiple returning purposes.

## Summary of Classes Defined
### Game
This class encapsulates all of the functionality of the game inside this class. The class has attributes such as: `self.name` (name of the game instance), `self.current_room` (the current room the player is virtually in), `self.inventory` (to store Item objects), `self.inventory_names` (to store Item objects' names), `self.inventory_weights` (to store the total weights of objects in the inventory) and `self.item_puzzle_count` (to check if any item puzzles have been solved).

The class has the following methods:

* `move`: To handle user's virtual movement in any of the four directions. The method checks if it is possible to move in that direction or if the room has an obstacle. If the mentioned checks are passed the method updates the self.current_room attribute to the new room.

* `look`: To handle user's inquiry to examine item in the current room. The method checks if the item inquired to be examined is in the room. If so, a description of the item is returned. If not, feedback that the current item doesn't exist in the room is returned.

* `take`: To handle user's inquiry to take an item in the current room. The method checks for the presence of the item. And if the item is present, the items in the current room are updated (item removed), the items in the inventory are updated, the weight of the inventory is updated, the score for storing items is updated, and feedback about the item's addition to the inventory is returned. If weight is beyond what can be handled, feedback that the item is too heavy is returned. If the inventory is full, feedback mentioning that is returned, and if the item is also not in the room, feedback about the absence of the item is returned.

* `drop`: To handle user's inquiry to drop an item in the current room. The method checks for the presence of the item in the inventory, then drops the item in the current room (i.e., updates the items in the current room, removes the item from the inventory, updates the inventory weight (reduces the weight), and also updates the score (reduces the score)). If the item isn't present, feedback mentioning just that is returned.

* `solve`: To handle user's inquiry to use an item to solve a puzzle or defeat a monster. The method has 3 options for where to apply the possible solution. They are:
    * A. A monster: If a monster is in the room, the item is used to defeat the monster, feedback of the successful solution is returned as feedback. If the item wasn't the right solution, feedback for that is returned. If no monster is in the room, the check proceeds to solve the puzzle.
    * B. A puzzle: If a puzzle is in the room, the item is used to solve the puzzle, feedback of the successful solution is returned as feedback. If the item wasn't the right solution, feedback for that is returned. If no puzzle is in the room, and no monster is in the room, the check proceeds to items.
    * C. An item with puzzles: If an item is present in the room, each item is checked for the presence of a puzzle. If a puzzle is present, the solution provided by the user is checked the same way as it would be checked for a room, and the same procedures follow. If none of these seem to be true, feedback that nothing happened is returned.

* `rank`: This method returns stored score for items in the inventory and 5 ratings based on the score.


### GameInterface
This class is where all GUI for the game is processed. The Game interface class has various attributes such as: self.window, self.image, self.room_name, self.room_items, self.description, self.north, self.south, self.east, self.west, self.take, self.look, self.use, self.drop, self.inventory, and self.quit. self.window is a Tk object, the rest are either buttons or texts that appear on the window.

The class has the following methods:

* `process_quit`: Handles the click of a quit button.
popupmsg: Handles pop windows and various types of information to be placed on the window.
* `update_popup`: Updates the display of the popup window based on which button is clicked.
* `look_handler`, `take_handler`, `use_handler`, `drop_handler`: All these methods handle what should happen behind a click on the look button, take button, use button, and drop button respectively.
update_items: Updates items displayed on the window upon a take or drop of an item.
* `move`: Handles Button clicks of the north, south, east, or west.
process_north, process_south, process_east, process_west: All these are bridge between a click on the north, south, east, and west buttons and the move method.
* `process_look`, `process_take`, `process_drop`, `process_use`: All these methods are bridges between the respective button clicks and their handlers.
process_inventory: Handles what is to be displayed upon the click of the inventory button.


## Summary of Non-Class Functions Defined
1. `Menu`: Displays question and options for possible answers. The function then checks for the validity of the user input constantly until a valid input is placed.
2. `get_file`: Opens any file, with the file name passed as a parameter, and stores each line of the file as a list. The function returns a tuple of 2 lists. The first list is the list with lines except the first line. The second list is a list of the metadata split using the '|' character.
3. `create_objects`: Creates objects of class Room, Item, Puzzle, and Monster. Checks which objects are to be created based on the metadata. If a Room object is to be created, every Room object is stored in a list to be accessed based on indices later on. If an Item Object is to be created, every Item object is stored in a dictionary as values, with Item names set as keys, so that the Item objects can be accessed using these keys later on. Finally, if a Puzzle or Monster object is to be created, each Monster or Puzzle object is stored in a dictionary. The name of the monster or puzzle is set as keys so that these objects can be easily accessed later on.


## Summary of Approach in Testing
The test was carried out for the Game class only. This is done because the non-class functions are bases for this class, the Game class can't work without the non-class functions working. The Game class's method move was tested for all 3 possibilities: A successful move, trial of movement in a direction not allowed, and trial of movement in a direction with an obstacle. The take, drop, and look methods were tested for a successful and unsuccessful take, drop, and look respectively.

