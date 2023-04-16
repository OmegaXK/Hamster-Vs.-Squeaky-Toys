# Hamster Versus Squeaky Toys
# A game where you are a hamster being pelted with squeaky toys.
# By Collin Maryniak
# omegaxk314@gmail.com

"""
- - - Modules Used in File - - -

- - pathlib and json - -
-The Path class from pathlib is used to make Path objects to work with
so the game can work with files easier. Combined with the json module,
the high score can be saved even after closing the window in a file
using the json data format.

- - random - -
-The random module is used for the choice() funtion to choose random
squeaky toys to spawn in, as well as the randint() function for choosing 
random coordinates for the hamster and squeaky toys to spawn.

- - sys --
-sys is used for the exit() frunction to exit the window easily.

- - pygame and pygame.locals - -
-The pygame module provides the tools used to build the actual game.

-The pygame.locals module is used for the different events such as QUIT,
KEYDOWN, K_w, K_RIGHT, etc. I import the pygame.locals module as *
because it is easy to tell what a pygame.locals variable looks like and
it is tedious to type out pygame.locals.EVENTNAME every time I want
to check for an event.
"""

from pathlib import Path
import json, random, sys
import pygame
from pygame.locals import *

# Screen constants.
WINDOWWIDTH = 1200 # Default is 1200.
WINDOWHEIGHT = 900 # Default is 900
CENTERX = WINDOWWIDTH / 2
CENTERY = WINDOWHEIGHT / 2

# General constants.
FPS = 30 # FPS is 30 instead of 60 so the game doesn't lag as much.
MOVESPEED = 11 # Hamster move speed.
EXTRALIFETIME = 300 # The number of frames it takes for the extra life.

# Squeaky toy constants.
TOYMINSIZE = 100
TOYMAXSIZE = 150
TOYMINSPEED = 10
TOYMAXSPEED = 16
TOYSPAWNRATE = 20

# Colors.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def main():
    """Main code for the game."""
    global MAINCLOCK, BASICFONT, DISPLAYSURF, hamster_img, hamster_rect 
    global cage_img, high_score

    # Initialize pygame and set up a clock.
    pygame.init()
    MAINCLOCK = pygame.time.Clock()

    # Set up the window.
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Hamster')

    # Create the fonts.
    BASICFONT = make_font(40)
    TITLEFONT = make_font(80)

    # Load hamster.
    hamster_img = pygame.image.load('images/hamster.png').convert_alpha()
    hamster_img = pygame.transform.scale(hamster_img, (200, 180))
    hamster_rect = hamster_img.get_rect()
    hamster_rect.center = (CENTERX, CENTERY)

    # Load background.
    cage_img = pygame.image.load('images/cage.png').convert_alpha()
    cage_img = pygame.transform.scale(cage_img, (WINDOWWIDTH, WINDOWHEIGHT))

    # Load squeaky toys.
    load_squeaky_toys()

    # Set the high score to the current high score.
    high_score = get_high_score()

    # Load the main theme and play it.
    pygame.mixer.music.load('sounds/main_theme.wav')
    pygame.mixer.music.play(-1, 0.0)

    # Run the title screen.
    title_screen(TITLEFONT)

    # Overall game loop.
    while True:
        # Get score once run_game() returns.
        score = run_game()
        # Call game_over() with that score.
        game_over(score)


def game_over(score):
    """Run the game over code."""
    global high_score 

    # Fill the screen white.
    DISPLAYSURF.fill(WHITE)

    # Check if the new score is greater than the high score.
    if score >= high_score:
        high_score = score

    # Display the text.
    GAMEOVERFONT = make_font(100)
    gamesurf, gamerect = make_text('Game Over', GAMEOVERFONT, BLACK)
    gamerect.center = (CENTERX, CENTERY - 300)

    DISPLAYSURF.blit(gamesurf, gamerect)
    draw_press_key_text(CENTERX, WINDOWHEIGHT - 200)
    draw_score_text(score)
    draw_high_score_text(high_score)

    # Blit the hamster image on the screen.
    big_hamster = pygame.transform.scale(hamster_img, (400, 350))
    big_hamster_rect = big_hamster.get_rect()
    big_hamster_rect.center = (CENTERX, CENTERY)
    DISPLAYSURF.blit(big_hamster, big_hamster_rect)

    # Update and wait for better playibility.
    pygame.display.update()
    pygame.time.wait(1000)

    # Wait for the player to press a key and then return.
    wait_for_player_to_press_key()
    return


def load_squeaky_toys():
    """Load in the squeaky toys"""
    global bananna, carrot, eggplant, mushroom, strawberry, squeaky_toy_images

    # Load each toy, make it the correct size, and convert it to alpha.
    bananna = pygame.image.load('images/squeaky_toys/bananna.png')
    bananna = pygame.transform.scale(bananna, (200, 200))
    bananna.convert_alpha()

    carrot = pygame.image.load('images/squeaky_toys/carrot.png')
    carrot = pygame.transform.scale(carrot, (200, 200))
    carrot.convert_alpha()

    eggplant = pygame.image.load('images/squeaky_toys/eggplant.png')
    eggplant = pygame.transform.scale(eggplant, (200, 200))
    carrot.convert_alpha()

    mushroom = pygame.image.load('images/squeaky_toys/mushroom.png')
    mushroom = pygame.transform.scale(mushroom, (200, 200))
    mushroom.convert_alpha()

    strawberry = pygame.image.load('images/squeaky_toys/strawberry.png')
    strawberry = pygame.transform.scale(strawberry, (200, 200))
    strawberry.convert_alpha()
    
    # Set up a list with all of the squeaky toy images.
    squeaky_toy_images = [bananna, carrot, eggplant, mushroom, strawberry]


def run_game():
    """Run the game, and return when it is over."""
    global loaded_toys, squeaky_toy_frame

    # Reset the game variables.
    left = False 
    right = False
    up = False 
    down = False
    score = 0
    loaded_toys = []
    squeaky_toy_frame = 0
    lives = 1

    # Run game loop.
    while True:
        for event in pygame.event.get(): # Event handling loop.
            # Check for quit.
            if event.type == QUIT:
                terminate()
            
            # Check if a key is being pressed.
            if event.type == KEYDOWN:
                # Terminate if it is the ESCAPE key.
                if event.key == K_ESCAPE:
                    terminate()

                # Check if the player is holding a direction,
                if (event.key == K_RIGHT) or (event.key == K_d):
                    left = False
                    right = True 
                if (event.key == K_LEFT) or (event.key == K_a):
                    right = False 
                    left = True
                if (event.key == K_UP) or (event.key == K_w):
                    down = False 
                    up = True 
                if (event.key == K_DOWN) or (event.key == K_s):
                    up = False 
                    down = True 

            # Check if player has released a key.
            if event.type == KEYUP:
                # Check if the player has released a direction.
                if (event.key == K_RIGHT) or (event.key == K_d):
                    right = False
                if (event.key == K_LEFT) or (event.key == K_a):
                    left = False
                if (event.key == K_UP) or (event.key == K_w):
                    up = False
                if (event.key == K_DOWN) or (event.key == K_s):
                    down = False

        # Blit the background img, the cage on to the screen.
        DISPLAYSURF.blit(cage_img, (0, 0))

        # Increment the player's score and draw it on the screen.
        score += 1
        draw_score_text(score)

        # Draw the high score text.
        draw_high_score_text(high_score)

        # Update the squeaky toys and display them.
        create_squeaky_toys()

        # Check if a squeaky toy has hit the player.
        if update_squeaky_toys() == False:
            # If the player has ran out of lives, return.
            lives -= 1
            if lives == 0:
                return score
            
            # If the player lost a life, spawn them in the center.
            hamster_rect.center = (CENTERX, CENTERY)

            # Clear out the toys.
            loaded_toys.clear()

            # Wait for half a second.
            pygame.time.wait(500)

        # Check if the player gets an extra life yet.
        if score == EXTRALIFETIME:
            lives += 1

        # Draw the player's lives on the screen.
        draw_lives(lives)

        # Update the hamster and draw him.
        update_hamster(right, left, up, down)
        DISPLAYSURF.blit(hamster_img, hamster_rect)

        # Update the game.
        pygame.display.update()
        MAINCLOCK.tick(FPS)


def draw_lives(lives):
    """
    If the player has two lives, let them know with an extra hamster.
    """

    if lives == 2:
        # Make a small hamster.
        small_hamster = pygame.transform.scale(hamster_img, (70, 70))

        # Draw it on the top of the screen.
        width = small_hamster.get_rect().width
        DISPLAYSURF.blit(small_hamster, (CENTERX - width, 10))


def draw_high_score_text(high_score):
    """Draw the current high score on to the screen."""
    scoresurf, scorerect = make_text(f"High Score: {high_score}",
                                      BASICFONT, BLACK)
    scorerect.topright = (WINDOWWIDTH - 100, 10)
    DISPLAYSURF.blit(scoresurf, scorerect)


def update_squeaky_toys():
    """Update the squeaky toys and display them."""
    if loaded_toys: # Only execute if there are toys loaded.
        for toy in loaded_toys:
            # Depending on where they spawned, move them.
            if toy['spawn'] == 'yt': # Spawned on the top.
                toy['rect'].y += toy['speed']
            elif toy['spawn'] == 'yb': # Spawned on the bottom.
                toy['rect'].y -= toy['speed']
            elif toy['spawn'] == 'xl': # Spawned on the left.
                toy['rect'].x += toy['speed']
            elif toy['spawn'] == 'xr': # Spawned on the right.
                toy['rect'].x -= toy['speed']

            # Check if a toy is colliding with hamster.
            if toy['rect'].colliderect(hamster_rect):
                return False

            # Blit each toy on the screen.
            DISPLAYSURF.blit(toy['image'], toy['rect'])


def create_squeaky_toys():
    """Create a squeaky toy every few frames."""
    global squeaky_toy_frame

    # Increment squeaky toy frame.
    squeaky_toy_frame += 1
    # If the frame reaches the spawn rate, reset it and spawn a toy.
    if squeaky_toy_frame >= TOYSPAWNRATE:
        squeaky_toy_frame = 0
        spawn_squeaky_toy()


def spawn_squeaky_toy():
    """Create a new squeaky toy and add it to the list."""
    global loaded_toys

    # Define the attributes of the new toy.
    new_image = random.choice(squeaky_toy_images)
    size = random.randint(TOYMINSIZE, TOYMAXSIZE)
    new_image = pygame.transform.scale(new_image, (size, size))
    new_rect = new_image.get_rect()
    speed = random.randint(TOYMINSPEED, TOYMAXSPEED)

    # Side is a random int, either 1 or 2.
    side = random.randint(1, 2)

    # If it is 1, then the toy will spawn on the y axis.
    if side == 1:
        spawn = 'y'
        # Sets the x randomly across the entire x axis.
        new_rect.x = random.randint(0, WINDOWWIDTH - new_rect.width)

        # Decide if it spawns on the top or bottom.
        if random.randint(1, 2) == 1:
            # Spawn it on the top by setting y to above the screen.
            new_rect.y = -40
            spawn += 't'
        else:
            # Spawn it on the bottom with a value passed the bottom.
            new_rect.y = WINDOWHEIGHT + 40
            spawn += 'b'

    # If side is 2, then the toy will spawn on the x axis.
    elif side == 2:
        spawn = 'x'
        # Set the y randomly across the y axis.
        new_rect.y = random.randint(0, WINDOWHEIGHT - new_rect.height)

        # Decide if it spawns on the left or right side.
        if random.randint(1, 2) == 1:
            # Spawn it on the left.
            new_rect.x = -40
            spawn += 'l'
        else:
            # Spawn it on the right.
            new_rect.x = WINDOWWIDTH + 40
            spawn += 'r'

    # Add the new toy's info to a dictionary and add it to the list.
    loaded_toys.append({
        'image': new_image,
        'rect': new_rect,
        'spawn': spawn,
        'speed': speed
    })


def draw_score_text(score):
    """Draw the player's score on the screen."""
    scoresurf, scorerect = make_text(f"Score: {score}", BASICFONT, BLACK)
    scorerect.topleft = (10, 10)
    DISPLAYSURF.blit(scoresurf, scorerect)


def update_hamster(right, left, up, down):
    """Update the hamster's position based on the movement variables."""

    if right and hamster_rect.right < WINDOWWIDTH:
        # Hamster is allowed to move right.
        hamster_rect.x += MOVESPEED
    if left and hamster_rect.left > 0:
        # Hamster is allowed to move left.
        hamster_rect.x -= MOVESPEED 

    if up and hamster_rect.top > 0:
        # Hamster is allowed to move up.
        hamster_rect.y -= MOVESPEED 
    if down and hamster_rect.bottom < WINDOWHEIGHT:
        # Hamster is allowed to move down.
        hamster_rect.y += MOVESPEED


def title_screen(font):
    """Blit the title screen and wait for the player to press a key."""

    # Fill the screen white.
    DISPLAYSURF.fill(WHITE)

    # Create the text displaying the title screen and instructions.
    titlesurf, titlerect = make_text('Hamster Vs. Squeaky Toys', font, BLACK)
    titlerect.center = (CENTERX, CENTERY - 150)

    # Instrucs short for instructions.
    instrucs = 'Avoid the squeaky toys flying at you for as long as possible.'
    insurf, inrect = make_text(instrucs, BASICFONT, BLACK)
    inrect.center = (CENTERX, CENTERY)

    # Make text saying when you get an extra life.
    # lt is short for life_text so I could fit the string.
    lt = f'Once your score reaches {EXTRALIFETIME}, you get an extra life!'
    lifesurf, liferect = make_text(lt, BASICFONT, BLACK)
    liferect.center = (CENTERX, CENTERY + 75)

    # Put the text on the screen.
    DISPLAYSURF.blit(titlesurf, titlerect)
    DISPLAYSURF.blit(insurf, inrect)
    DISPLAYSURF.blit(lifesurf, liferect)

    # Draw all the squeaky toys on the top of the title screen.
    x = 100
    y = 20
    for toy_image in squeaky_toy_images:
        # Blit the toy's image at the correct position.
        DISPLAYSURF.blit(toy_image, (x, y))

        # Make a rect out of the image.
        toyrect = toy_image.get_rect()

        # Use the rect's width aspect to increase x by the right number.
        x += toyrect.width

    # Wait for the player to press a key and draw the message.
    draw_press_key_text(CENTERX, WINDOWHEIGHT - 250)
    wait_for_player_to_press_key()
    return


def draw_press_key_text(x, y):
    """Make text and blit it on to the screen."""
    playsurf, playrect = make_text('Press a key to play.', BASICFONT, BLACK)
    playrect.center = (x, y)
    DISPLAYSURF.blit(playsurf, playrect)


def make_font(size):
    """Return a font obj with the correct size."""
    return pygame.font.Font('freesansbold.ttf', int(size))


def make_text(text, font, color):
    """Make surf and rect objects and return them."""
    textsurf = font.render(text, True, color)
    textrect = textsurf.get_rect()
    return textsurf, textrect


def wait_for_player_to_press_key():
    """Wait for the player to press any key but escape."""
    while True:
        for event in pygame.event.get(): # Event handling loop.
            # Check for quit.
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                # If the player pressed escape, terminate.
                if event.key == K_ESCAPE:
                    terminate()
                # If player pressed a key that wasn't escape, return.
                return
        
        # Update.
        pygame.display.update()
        MAINCLOCK.tick(FPS)


def save_high_score(high_score):
    """Save the high score."""

    # Create a path object.
    path = Path('high_score.json')

    # Make sure the high score is a string.
    high_score = str(high_score)

    # Convert the high score to JSON format.
    json_score = json.dumps(high_score)

    # Write the score to the file.
    path.write_text(json_score)


def get_high_score():
    """Find the current high score and set it."""

    # Create a path object for the file.
    path = Path('high_score.json')

    # Check if the pathh exists.
    if path.exists():
        # If so, get the current high score.
        contents = path.read_text()
        high_score = json.loads(contents)
        high_score = int(high_score)
    else:
        # If not, set the high score to zero.
        high_score = 0

    # Return the high score.
    return high_score
              

def terminate():
    """Save the high score and quit out of the game.."""
    save_high_score(high_score)
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    # Run the game.
    main()