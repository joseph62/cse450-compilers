Name:
Sean Joseph
Resources:
A piazza post about handling adding a scope.
PLY Documentation.
Some production rules were taken from the Project 3 solution.
Most of those rules focused on the print statements arg list.
Comments:
This project was awesome. I had fun trying to add features and debug
the Bad code my compiler generated. Seeing code compile properly after
adding and debugging a new feature was so rewarding.
Some portions of my solution are very sub optimal. I have a separate
node for If and IfElse and the boolean operators. Those all have extremely
similar functionality so there is probably a way to cut back on the 
duplicate code through inheritance. Ditto the comparison and math nodes. 
I'm not super confident in my solution to the break statement problem.
I ended up using a closure passed into a Node class method that modifies 
only BreakNodes. That seems a little bit out there. I would really appreciate 
suggestions for solutions that are not as weird. 
This class is awesome by the way.
