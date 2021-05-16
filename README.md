# Team Orange
# Team members
1. Ryan Choy 014499316
2. William Su 013697658
3. Janaarthana Harri 015246205
4. Premchand

# Contributions
1. Ryan
 - Made base game
 - Added bullet projectile feature
 - Added screens (Home page, Controls page, Credits page, Game Page)
 - Added screen transitions
 - Made game turn based (Player 1 goes first, then Player 2 and vice versa)
 - Start screen background image
 - Bug fixes + minor QOL features 
2. William
 - Ensured clean code by moving utility functions into the classes that used them instead of just hanging around the main code
 - Optimized bullet physics for correctness and performance
 - Created system to rotate an image around its center
 - Used system to have active sprites follow cursor
 - Expanded Player class and Bullet class attributes for further functionality
 - Optimized game loop logic to be cleaner and less verbose (less conditionals using the active_player and dormant_player system)
 - Added fuel consumption feature
 - Logic for intelligent image import and process based on player1/player2
3. Janaarthana
 - ackground images and sound.
 - Player hit animation.
 - Screen transition after the game ends, continue to play again or quit.
 - Health bar created for both players.
 - Snowfall map created.
4. Premchand
 - Added the collision detection feature to detect collision between the object and projectile
 - Used the collision detection to reduce the hp to reduce the player's health.
 - Added multiple model images for the player and made the model random at the start of the game.


# Summary
Our project is a multiplayer turn based shooting game where 2 players try to hit each other with a physics projectile. This idea came about due to the recent EOLing of adobe flash player. Many of us had grown up playing adobe flash games with very similar premises - and with Flash's EOL just passed, we wanted to create a tribute to those somewhat crude 2D physics games of our childhoods. With that in mind, we included many hallmarks of that particular genre of game - stock art backgrounds, inconsistent sprite choices, and simplistic gameplay mechanics. While perhaps not as involved as we had originally intended, we believe our project reflects that experience rather well.

With regards to the physics: the projectile's movement speed and direction depends on the location of the mouse, the further away the mouse is from the player, the faster it will go. Players have a set amount of distance they can travel (energy) in a turn and uses the a and d key on the keyboard to move left and right respectively. The goal of this is to make it harder for the enemy to use the same shot on you two turns in a row. Players would take turns shooting the projectile and when their respective hp goes down to 0, the opponent will win the game. The game will then restart after a few moments.

# Architectural diagram
![]()

# Key Features
1. Speed and angle of projectile based on location of mouse
2. Different character models, including more complex multipart sprites
3. Dynamic hp bar visual that changes based on incoming damage
4. Dynamic pixel elements imitating snow fall
5. Characters model change its direction based on the position of the mouse

# Youtube Ad link

# Game demo link

# Team Kanban Board
![](img/kb1.png)
![](img/kb2.png)
![](img/kb3.png)
![](img/kb4.png)
![](img/kb5.png)
