"""
A rudimentary Story Time Generator Video Game :)
"""
from pprint import pprint
import numpy as np
import pygame
import pygame.sprite as sprite
from mlx_lm import load, generate
import os


from game_elements import *
from interface import *

# llm setup:
model_name = 'meta-llama/Llama-3.2-1B-Instruct'
model, tokenizer = load(model_name)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
running = True
dt = 0
maxRoundTime = 1
allow_model = True

player_pos = pygame.Vector2(screen.get_width() / 4, screen.get_height() / 4 * 3)
capture_points_pos = pygame.Vector2(screen.get_width() / 4, screen.get_height() / 4)

player1 = player(player_pos.x, player_pos.y, 'green')
player2 = player(player_pos.y, player_pos.x, 'purple')

team1 = pygame.sprite.Group()
team2 = pygame.sprite.Group()

capture1 = capture_point(capture_points_pos.y, capture_points_pos.x, 'orange')
capture2 = capture_point(capture_points_pos.y * 3, capture_points_pos.x * 3, 'orange')
cap_points = pygame.sprite.Group((capture1, capture2))


eventsTable = []
storyTable = [
    '', '', ''
]
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # === Handle Attacking Player1 ===
    attackPlayer = sprite.spritecollide(player1, team2, 0)
    if attackPlayer != []:
        for enemyAttacks in attackPlayer:
            player1.health -= enemyAttacks.damage
            eventsTable.append('Monsters attack Player1')
        if player1.health <= 0:
            print('Player1 has been slain! You lose :(')
            running = False

    # === Handle Attacking Player2 ===
    attackPlayer = sprite.spritecollide(player2, team1, 0)
    if attackPlayer != []:
        for monsterAttack in attackPlayer:
            player2.health -= monsterAttack.damage
            eventsTable.append('Knights attack Player2')
        if player2.health <= 0:
            print('Player2 has been slain! You Win :)')
            running = False

    # === Handle monster fight ===
    # NOTE: This Section handles conflict from the perspective of the player. We only select the first enemy encountered, so player all monsters can attack and freeze on first monster encountered, which can be the same one. However, this has the effect of allowing the enemy to by pass a conflict, due to the fact that player monsters only engage with first enemy in the group, by enemyContact[0]. If we want to be equal reimplement through enemy encounter.
    fight_collision = sprite.groupcollide(team1, team2, 0, 0)
    if fight_collision != {}:
        for oneMonster in fight_collision.keys():
            enemyContact = fight_collision[oneMonster]

            # Freeze combatants when in meeting
            oneMonster.moving = False
            enemyContact[0].moving = False

            # First calculate ally attack result
            enemyContact[0].health -= oneMonster.damage

            # Then calculate enemy damage
            oneMonster.health -= enemyContact[0].damage

            # Resume movement if kill successfull
            if oneMonster.health <= 0:
                if oneMonster.addStory_attack:
                    eventsTable.append("Player1's knight was killed by Player2's monster")
                    oneMonster.addStory_attack = False
                enemyContact[0].moving = True
            if enemyContact[0].health <= 0:
                if enemyContact[0].addStory_attack:
                    eventsTable.append("Player2's monster was slain by Player1's knight")
                    enemyContact[0].addStory_attack = False
                oneMonster.moving = True

            # Remove killed entity
            if oneMonster.health <= 0: 
                team1.remove(oneMonster)
            if enemyContact[0].health <= 0:
                team2.remove(enemyContact[0])

    # === Change player movement if at capture point ===
    player_capture = sprite.groupcollide(team1, cap_points, 0, 0)
    if player_capture != {}:
        for oneMonster in player_capture.keys():
            if oneMonster.addStory_capture:
                eventsTable.append("Player1's knights enters the village.")
                oneMonster.addStory_capture = False
            oneMonster.destination = player2.vector


    # === Change bot movement if at capture point ===
    bot_capture = sprite.groupcollide(team2, cap_points, 0, 0)
    if bot_capture != {}:
        for oneMonster in bot_capture.keys():
            if oneMonster.addStory_capture:
                eventsTable.append("Player2's monsters enters the village.")
                oneMonster.addStory_capture = False
            oneMonster.destination = player1.vector

    # ==== Request user/bot  input / interface, game stage flags ====
    if maxRoundTime == 0:
        os.system('clear')
        # ==== Show Stats ====
        show_stats([player1, player2], team1, team2)
        # ==== Generate Story Events ====
        if allow_model and running and (len(eventsTable) > 0): 
            storyTable.pop(0)
            storyTable.append(
                eventsTable[np.random.
                    randint(0, len(eventsTable))]
            )
            seedPrompt = np.random.random()
            print('INSIDE STORY TABLE:', storyTable)

            prompt = f"Write a short description about the follow events in a video game. The description should be no longer than 5 sentences. Describe the events briefly.:\n{'\n'.join(storyTable)} + {seedPrompt}"
            
            messages = [
                    {"role": "system", "content": "You are a description generating chatbot that describes events. Response should be no longer than 5 sentences. Describe the events briefly."},
                    {"role": "user", "content": prompt}
            ]
            prompt = tokenizer.apply_chat_template(
                    messages, add_generation_prompt=True
                )
            text = generate(model, tokenizer, prompt=prompt, verbose=False, max_tokens=150)
            print(text, '\n')

        eventsTable.clear()
        running = user_interface(player1, team1, cap_points)
        if running: bot_interface(player2, team2, cap_points) 
        maxRoundTime = 1_00

    maxRoundTime -= 1

    # ==== Render Players / Capture Points ====
    player1.update()
    player2.update()
    cap_points.update()

    # === Update team movements ===
    team1.update()
    team2.update()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
