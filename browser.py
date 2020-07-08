"""
browser
Author: Neil Balaskandarajah
Created on: 20/06/2020
Play the browser version of Hoop Stack
"""
import pyautogui as pag
from time import sleep
import cv2
import image_filtering
import os.path

def _pair_click(stack_locations, pair):
    """
    Click between two pairs
    """
    delay = 0.2
    moveTime = 0.001
    x, y = stack_locations[pair[0]]; pag.moveTo(x, y, moveTime); pag.click()
    sleep(delay)
    x, y = stack_locations[pair[1]]; pag.moveTo(x, y, moveTime); pag.click()
    sleep(delay)

def _take_screenshots():
    """
    Take screenshots of stacks for testing
    """
    pag.alert('Hit ENTER when mouse is at the top left of the stacks bound')
    x1, y1 = pag.position()
    pag.alert('Hit ENTER when mouse is at the bottom right of the stacks bound')
    x2, y2 = pag.position()

    i = 0; done = False
    while not done:
        file = 'tests\\lvl{}.png'.format(i)
        sleep(0.25)
        pag.screenshot(file, region=(x1, y1, x2-x1, y2-y1))
        i += 1
        done = pag.confirm('Press OK if done, Cancel if continuing') == 'OK'
        if not done:
            pag.alert('Press OK when next level is open')

def get_game_bounds():
    """
    Get the bounds of the game from the user
    """
    filename = 'coords.crd'
    if os.path.isfile(filename):
        with open(filename, 'r') as file:
            for line in file:
                coords = [int(elem) for elem in line.split(' ')]
        return coords

    else:
        pag.alert('Hit ENTER when mouse is at the top left of the stacks bound')
        x1, y1 = pag.position()
        pag.alert('Hit ENTER when mouse is at the bottom right of the stacks bound')
        x2, y2 = pag.position()
        pag.alert('Hit ENTER when mouse is at the Next Level button')
        s_x, s_y = pag.position()

        # Write to file
        file = open(filename, 'w')
        file.write('{} {} {} {} {} {}'.format(x1, y1, x2, y2, s_x, s_y))

    return x1,y1,x2,y2,s_x,s_y

def screenshot_game(coords, filename):
    """
    Take a screenshot of the game given its coords and the name of the file to write to
    """
    sleep(0.25)
    x1,y1,x2,y2 = coords
    pag.screenshot(filename, region=(x1, y1, x2-x1, y2-y1))

def play_moves(moves, locations):
    """
    Play the game given the moves that need to be done and the location of each stack
    """
    sleep(0.5)
    for move in moves:
        _pair_click(locations, move)

def play_game():
    """
    Play the game in the browser

    PROCESS
    (debugging)

    get_game_bounds
        Get the image bounds
            store the x,y point of the top left

    play_level
        screenshot_game
            Take a screenshot of the image
                (show the image with cv2)
                - save to a global file name so it can be accessed within play_level

        create_game
            Create the Game object with the image
                Create all the stacks
                (print each stack)
            Set num_pieces
                Loop through all the stacks, return the first hoop
                Loop through all the stacks and count how many of that color hoop there is
                That number is num_pieces
                    ie. level 1, three cyan hoops, total stack height is three

        get_click_locations
            Center of the stack bounds of the image
            (show the image with the click locations drawn on for each stack)
            Offset with the top left of the x,y to get the screen position

        play_game
            Solve the game
            (Print with display_moves)
            (display_history)
            Play the game
                For each pair in move history, go to those locations

        next_level
            # need to get next_level button location
            Click the next level button
            Wait 1-2s for the screen to load

    Write settings to file when exiting? (ie. image bounds, next button location)
    Press X to exit
    """
    #Get the image
    filename = 'game.png'
    ans = pag.confirm('Press OK to start playing, or SET to start setting mouse locations', buttons=['OK', 'SET'])
    if ans == 'SET': os.remove('coords.crd')
    coords = get_game_bounds()

    sleep(3)
    playing = True
    while playing:
        screenshot_game(coords[:4], filename)
        img = cv2.imread(filename, cv2.IMREAD_COLOR)
        s = 0.5; scale = 1/s
        img = image_filtering.scale_image(img, s)
        # cv2.imshow('img', img); cv2.waitKey(0); cv2.destroyAllWindows()

        # Create the game instance and solve it
        game, clicks = image_filtering.game_from_image(img)
        game.display()

        # Calculate the click locations (offset stack locations in image by where image is in screen)
        for letter in clicks:
            # cv2.circle(img, clicks[letter], 5, 255, -1)  #Draw circle to image
            x, y = clicks[letter]
            clicks[letter] = (int(x*scale + coords[0]), int(y*scale + coords[1]))

        # Play the game
        game.solve(debug=False)
        play_moves(game.history, clicks)

        # Press the next level button
        sleep(1.75)
        pag.click(coords[4], coords[5])
        sleep(0.5)


"""
Levels 49 and 65 no longer get stuck
"""
play_game()