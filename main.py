import pygame, os
from random import randint
from sys import exit
pygame.font.init()
pygame.mixer.init()

# typical to put contants in all CAPS
WIDTH, HEIGHT = 600,830
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake!")

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)

BORDER  = pygame.Rect(0,800,600,30)

SCORE_FONT = pygame.font.SysFont('comicsans', 18)

APPLE_WIDTH, APPLE_HEIGHT = 20,20
SNAKE_WIDTH, SNAKE_HEIGHT = 50,50

FPS = 60

EAT_APPLE = pygame.USEREVENT + 1

class Snake(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        # create snake head
        self.snake_head = pygame.image.load(os.path.join("graphics", 'head_right.png'))
        #self.snake_head_up = pygame.transform.scale(pygame.image.load(os.path.join("graphics", 'head_up.png')),(SNAKE_WIDTH,SNAKE_HEIGHT))
        #self.snake_head_right = pygame.transform.scale(pygame.image.load(os.path.join("graphics", 'head_right.png')),(SNAKE_WIDTH,SNAKE_HEIGHT))
        #self.snake_head_down = pygame.transform.scale(pygame.image.load(os.path.join("graphics", 'head_down.png')),(SNAKE_WIDTH,SNAKE_HEIGHT))
        #self.snake_head_left = pygame.transform.scale(pygame.image.load(os.path.join("graphics", 'head_left.png')),(SNAKE_WIDTH,SNAKE_HEIGHT))

        self.snake_direction = "right"

        self.image = self.snake_head
        self.rect = self.image.get_rect(midbottom = (100,400))

    def player_input(self):
       
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.snake_direction != "right": # left
            self.snake_direction = 'left'
            self.image = pygame.transform.rotate(self.snake_head,180)
            #self.rect.x -= VEL
        if keys[pygame.K_RIGHT] and self.snake_direction != "left": # Right
            self.snake_direction = 'right'
            self.image = self.snake_head
            #self.rect.x += VEL
        if keys[pygame.K_UP] and self.snake_direction != "down": # Up
            self.snake_direction = 'up'
            self.image = self.image = pygame.transform.rotate(self.snake_head,90)
            #self.rect.y -= VEL
        if keys[pygame.K_DOWN] and self.snake_direction != "up": # Down
            self.snake_direction = 'down'
            self.image = self.image = pygame.transform.rotate(self.snake_head,270)
            #self.rect.y += VEL

    def move_snake(self,score):
        if score > 3:
            velocity = score / 3
        else:
            velocity = 1


        if self.snake_direction == "left": # left
            self.rect.x -= velocity
        if self.snake_direction == "right": # Right
            self.rect.x += velocity
        if self.snake_direction == "up": # Up
            self.rect.y -= velocity
        if self.snake_direction == "down": # Down
            self.rect.y += velocity

    def update(self,score):
        self.player_input()
        self.move_snake(score)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,snake):
        super().__init__()

        # load snake body
        self.snake_body_bl = pygame.image.load(os.path.join("graphics", 'body_bl.png'))
        self.snake_body_br = pygame.image.load(os.path.join("graphics", 'body_br.png'))
        self.snake_body_horizontal = pygame.image.load(os.path.join("graphics", 'body_horizontal.png'))
        self.snake_body_tl = pygame.image.load(os.path.join("graphics", 'body_tl.png'))
        self.snake_body_tr = pygame.image.load(os.path.join("graphics", 'body_tr.png'))
        self.snake_body_vertical = pygame.image.load(os.path.join("graphics", 'body_vertical.png'))

        
        if snake.snake_direction == "right":
            self.image = self.snake_body_horizontal
            self.rect = self.image.get_rect(midright = snake.rect.midleft)

    
    """ def move_snake_body(self,snake):
        if snake.snake_direction == "left": # left
            self.rect.x -= VEL
        if snake.snake_direction == "right": # Right
            self.rect.x += VEL
        if snake.snake_direction == "up": # Up
            self.rect.y -= VEL
        if snake.snake_direction == "down": # Down
            self.rect.y += VEL """
    
    def update(self,snake):
        self.move_snake_body(snake)
        

pygame.init()

def collisions(snake):
        if snake.rect.left <= 0:
            return False # HIT LEFT WALL
        elif snake.rect.right >= 600:
            return False # HIT RIGHT WALL
        elif snake.rect.top <= 0:
            return False # HIT CEILING
        elif snake.rect.bottom >= 800:
            return False # HIT FLOOR
        else:
            return True #NO COLLISION

def collect_apple(apple,snake):
    if snake.colliderect(apple):
        pygame.event.post(pygame.event.Event(EAT_APPLE))

def display_score(score,start_time):
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = SCORE_FONT.render(f'Time: {current_time} | Apples: {score}', False, WHITE)
    score_rect = score_surf.get_rect(topleft = (20,800))
    WIN.blit(score_surf,score_rect)

def draw_window(apple_surf,apple_rect,snake,obstacle_group,score,start_time):
    # Draw all our elemnets
    WIN.fill("dark green")
    WIN.blit(apple_surf,apple_rect)
    snake.draw(WIN)
    snake.update(score)
    pygame.draw.rect(WIN, BLACK, BORDER)

    display_score(score,start_time)

    #obstacle_group.draw(WIN)
    #obstacle_group.update(snake.sprite)

    # update display
    pygame.display.update()

def main():

    # start time
    start_time = 0

    # score
    score = 0
    
    apple_surf = pygame.image.load(os.path.join("Graphics","apple.png"))
    apple_rect = apple_surf.get_rect(topleft = (randint(0,560),randint(0,760)))
    
    clock = pygame.time.Clock()

    # Groups
    snake = pygame.sprite.GroupSingle()
    snake.add(Snake())

    obstacle_group = pygame.sprite.Group()

    #obstacle_timer = pygame.USEREVENT + 1
    #pygame.time.set_timer(obstacle_timer, 500)

    run = True
    while run:
        # set frame rate
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == EAT_APPLE:
                # generate new apple
                score += 1
                apple_surf = pygame.image.load(os.path.join("Graphics","apple.png"))
                apple_rect = apple_surf.get_rect(topleft = (randint(0,560),randint(0,760)))
                print(f'score: {score}')

        # check for eating apple
        collect_apple(apple_rect,snake.sprite.rect)

        # check for wall collision
        run = collisions(snake.sprite)

        # Draw Window
        draw_window(apple_surf,apple_rect,snake,obstacle_group,score,start_time)

# only run this function if this file is ran directly
if __name__ == "__main__":
    main()