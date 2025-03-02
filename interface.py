"""
Commands for user interaction and interface.
Handles request for user input, and different CLI results.
"""
import os
import numpy as np
from game_elements import *

def show_stats(players:list[player], team1:list[monster], team2:list[monster]):
    # os.system('clear')
    print(f'PLAYER 1:\n{players[0].stats}')

    print(f'{'team1':8} {'health':>8} {'damage':>8} {'speed':>8}')
    for m in team1:
        print(f'{'Monster':8} {m.health:>8} {m.damage:>8} {m.speed:>8}')

    print(f'\nBOT 1:\n{players[1].stats}')

    print(f'{'team2':8} {'health':>8} {'damage':>8} {'speed':>8}')
    for m in team2:
        print(f'{'Monster':8} {m.health:>8} {m.damage:>8} {m.speed:>8}')

# NOTE: Game Stage Flags
def user_interface (
        player:player, team:pygame.sprite.Group, 
        cap_points:pygame.sprite.Group
):
    print('\nAll input must be an int.')
    prompts = {
        'health':'How much health should each monster have?\n',
        'damage':'How much damage should each monster have?\n',
        'speed':'How much speed should each monster have?\n',
        'capture':'Which capture point do you want to capture? 0 or 1?\n',
    }
    user_responses = {
        'health' : 0,
        'damage' : 0,
        'speed' : 0,
        'capture': 0,
    }
    valid_score = False
    while not valid_score:
        for key in user_responses.keys():
            userInput = input(prompts[key]) # get user input
            
            # check if want to quit
            if userInput == 'q': 
                print('quiting game')
                return False

            # check that input is integer
            valid_input = True if userInput.isdigit() else False
            while(not valid_input):
                print('What was entered was not a valid integer, please try again.')
                userInput = input(prompts[key])
                if userInput.isdigit():
                    valid_input = True
                    print('WHAT')

            valid_input = True if key == 'capture' and int(userInput) > 1 else False
            while(not valid_input and key == 'capture'):
                userInput = input(prompts[key])
                print('Choose a valid capture point.')
                userInput = input(prompts[key])
                valid_input = True if key == 'capture' and int(userInput) > 1 else False

            user_responses[key] = int(userInput)

        user_selection = int(user_responses['capture'])
        captureThis = cap_points.sprites()[user_selection]

        # check if monster is balanced, i.e. stats no greater than maxMonsterScore
        monster_strength = (user_responses['health'] + 
                            user_responses['damage'] + 
                            user_responses['speed'])
        if monster_strength > player.resources:
            print(f'Stats sum greater than {player.resources}, please try again')
            valid_score = False
        else:
            valid_score = True


    # Add monsters to team
    # print('added monster')
    team.add(monster(
        player.position, 'blue', user_responses,
        captureThis.vector
    ))
    
    return True


def bot_interface (
        player:player, team:pygame.sprite.Group, 
        cap_points:pygame.sprite.Group
):

    bot_responses = {
        'health' : 0,
        'damage' : 1,
        'speed' : 1,
    }
    maximum_score = 3
    for i in range(maximum_score):
        i_stat = np.random.randint(0, 3) # select random stat
        keys = list(bot_responses.keys())
        bot_responses[keys[i_stat]] += 1

    #NOTE: redundancy 
    bot_responses_capture = np.random.randint(0, 2)

    # Add monsters to team
    # print('added monster')
    captureThis = cap_points.sprites()[bot_responses_capture]
    team.add(monster(
        player.position, 'red', bot_responses,
        captureThis.vector
    ))
    
    return True