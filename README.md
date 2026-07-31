# snake-game
Creating Snake game using pygame

# Logic of Snake Game
1. We create a grid (kind of)
2. some blocks are snake blocks

# Vector2: way to store 2d data
v = pygame.math.Vector2(5,4)        ls = [5,4]
v.x -> 5                ls[0] -> 5
v.y -> 4                ls[1] -> 4

Move right: 
r = Vector2(1,0)        ls[0] += 1
v += r
[5] + [1] = [6]
[4] + [0] = [4]

# Moving the snake
The head is moved to a new block
The block before the head gets the position where the head used to be.
Each block is moved to the position of the block that used to be before it
(this deletes the last block)

|-----list copy
|    [pos1,pos2,pos3][direction]
|------- new head position
image.png

# Drawing the snake body with images
We cycle through every block in snake.body
We check the block as well as the previous and next block
Depending on how they are laid we can display different graphics