import pygame
import sys
from game import *
import pygame_textinput
from time import sleep

white = (255, 255, 255)
grey = (180, 180, 180)
list_of_rect_card = []
red = (245, 100, 98)
blue = (0, 195, 229)
green = (47, 226, 155)
yellow = (247, 227, 89)
black = [150, 150, 150]
# light shade of the button
button_hover_color = (170, 170, 170)

# dark shade of the button
button_color = (100, 100, 100)
# defining a font
tiny_font = pygame.font.SysFont('Corbel', 25)
small_font = pygame.font.SysFont('Corbel', 35)
name_font = pygame.font.SysFont('Corbel', 25, True)
table = pygame.image.load('NaturalOak.jpg')
table = pygame.transform.rotate(table, 90)
table = pygame.transform.scale(table, (1200, 800))


def game_engine():
    pygame.init()
    screen_size = (1200, 800)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('UNO!')
    screen.fill(black)

    # rendering a text written in
    # this font
    text_quit = small_font.render('Quit', True, white)
    text_new_game = tiny_font.render('New Game', True, white)
    text_rules = small_font.render('Rules', True, white)
    background = pygame.image.load("background.png")

    win = False

    game_over = True
    show_menu = True
    show_rules = False
    show_results = False

    # menu screen

    while show_menu:
        # stores the (x,y) coordinates into
        # the variable as a tuple
        mouse = pygame.mouse.get_pos()
        width = screen.get_width()
        height = screen.get_height()
        button_width = 140
        button_height = 40
        new_game_button_x = (width * .5) - (button_width / 2)
        quit_button_x = (width * .75) - (button_width / 2)
        rules_button_x = (width * .25) - (button_width / 2)
        button_y = (height * .75) + (button_height / 2)

        # background
        screen.fill(white)
        screen.blit(background, (screen.get_width() / 2 - 450, 100))
        pygame.draw.rect(screen, blue, [0, 0, 20, 800])
        pygame.draw.rect(screen, green, [1180, 0, 20, 800])
        pygame.draw.rect(screen, red, [0, 0, 1200, 20])
        pygame.draw.rect(screen, yellow, [0, 780, 1200, 20])

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

                # checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                # if the mouse is clicked on the
                # button the game is terminated
                if quit_button_x <= mouse[0] <= quit_button_x + button_width and button_y <= mouse[
                        1] <= button_y + button_height:
                    pygame.quit()
                    sys.exit()

                if new_game_button_x <= mouse[0] <= new_game_button_x + button_width and button_y <= mouse[
                        1] <= button_y + button_height:
                    game_over = False

                if rules_button_x <= mouse[0] <= rules_button_x + button_width and button_y <= mouse[
                        1] <= button_y + button_height:
                    show_rules = True

        if new_game_button_x <= mouse[0] <= new_game_button_x + button_width and button_y <= mouse[
                1] <= button_y + button_height:
            pygame.draw.rect(screen, button_hover_color, [new_game_button_x, button_y, 140, 40])
        else:
            pygame.draw.rect(screen, button_color, [new_game_button_x, button_y, 140, 40])

        if quit_button_x <= mouse[0] <= quit_button_x + button_width and button_y <= mouse[
                1] <= button_y + button_height:
            pygame.draw.rect(screen, button_hover_color, [quit_button_x, button_y, 140, 40])
        else:
            pygame.draw.rect(screen, button_color, [quit_button_x, button_y, 140, 40])

        if rules_button_x <= mouse[0] <= rules_button_x + button_width and button_y <= mouse[
                1] <= button_y + button_height:
            pygame.draw.rect(screen, button_hover_color, [rules_button_x, button_y, 140, 40])
        else:
            pygame.draw.rect(screen, button_color, [rules_button_x, button_y, 140, 40])

        # superimposing the text onto our buttons
        screen.blit(text_quit, (quit_button_x + 40, button_y + 3))
        screen.blit(text_new_game, (new_game_button_x + 15, button_y + 7))
        screen.blit(text_rules, (rules_button_x + 30, button_y + 3))

        # updates the frames of the game
        pygame.display.update()

        if show_rules or not game_over:
            show_menu = False

    # show rules screen
    if show_rules:
        print_rules(screen)

    # game screen
    if not game_over:
        text_input = pygame_textinput.TextInput('', font_family='Corbel')
        text = True
        while text:
            screen.fill((225, 225, 225))
            text_enter = small_font.render('Enter Name', True, black)
            screen.blit(text_enter, (screen.get_width() / 2 - 70, 300))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    text = False
            # Feed it with events every frame
            text_input.update(events)
            # Blit its surface onto the screen
            screen.blit(text_input.get_surface(), (screen.get_width() / 2 - (len(text_input.get_text()) * 18) / 2,
                                                   screen.get_height() / 2))
            pygame.display.update()

        screen = pygame.display.set_mode(screen_size)
        screen.fill((0, 0, 0))
        cpu1 = CPU("Mark", 1)
        cpu2 = CPU("Mira", 2)
        cpu3 = CPU("Julia", 3)
        name = text_input
        player = Player(name, 0)
        game = Game(cpu1, cpu2, cpu3, player)
        for player in game.players:  # creates starting hands
            game.fill_hand(player)
        screen = pygame.display.set_mode(screen_size)
        screen.fill(black)
        print_top_card(game, screen)

        while not game_over:  # game engine

            player = game.players[game.current_player]
            print_game(game, screen)
            pygame.display.update()
            picked_card = choose_card(screen, game)
            if type(player) == CPU:
                print_game(game, screen)
                pygame.display.update()
                sleep(random.random() + .25)
            if not picked_card:
                pass
            elif type(picked_card) == Card:  # handles changing the game variables when a card is played
                if game.last_played.get_type() == Type.WILD or game.last_played.get_type() == Type.DRAW4:
                    game.last_played.set_wild(Color.NONE)  # resets wilds and draw fours from the previous turn, so
                    # they don't have a color after shuffling
                game.last_played = picked_card  # updates the last played card and adds it to the discard
                game.played_deck.append(game.last_played)

                # handles wilds
                if type(player) == Player and (
                        game.last_played.get_type() == Type.WILD or game.last_played.get_type() == Type.DRAW4):
                    color = set_wild(screen)
                    game.last_played.set_wild(color)
                    print_game(game, screen)
                elif type(player) == CPU and (
                        game.last_played.get_type() == Type.WILD or game.last_played.get_type() == Type.DRAW4):
                    game.last_played.set_wild(player.cpu_wilds())  # sets the color of the wild with cpu choice
                game.apply_power()
            # handles all non wild power cards
            if not player.get_hand() or (len(game.played_deck) == 0):
                game_over = True
                # referring to the actual user, not a CPU
                if type(player) == Player and not player.get_hand():
                    win = True
                show_results = True

            if type(player) == CPU:
                print_game(game, screen)
                pygame.display.update()

            elif type(player) == Player:
                print_game(game, screen)
                pygame.display.update()

            game.change_turn()

    if show_results:
        screen = pygame.display.set_mode(screen_size)
        win_text = small_font.render('You Win!', True, [0, 0, 0])
        lose_text = small_font.render('You lost, better luck next round', True, white)

        if win:
            screen.fill(white)
            screen.blit(win_text, (screen.get_width() / 2 - 50, 400))
        else:
            screen.fill(black)
            screen.blit(lose_text, ((screen.get_width() / 2) - 150, 400))
        pygame.draw.rect(screen, blue, [0, 0, 20, 800])
        pygame.draw.rect(screen, green, [1180, 0, 20, 800])
        pygame.draw.rect(screen, red, [0, 0, 1200, 20])
        pygame.draw.rect(screen, yellow, [0, 780, 1200, 20])
        text_back = tiny_font.render('     Menu', True, black)
        while show_results:
            button_width = 140
            button_height = 40
            width = screen.get_width()
            height = screen.get_height()
            menu_back_x = (width * .1) - (button_width / 2)
            button_y = (height * .85) + (button_height / 2)
            mouse = pygame.mouse.get_pos()

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:

                    if menu_back_x <= mouse[0] <= menu_back_x + button_width and button_y <= mouse[1] <= button_y + \
                            button_height:
                        show_results = False
                        game_engine()

            # if the mouse is clicked on the
            # button the game is terminated
            if menu_back_x <= mouse[0] <= menu_back_x + button_width and button_y <= mouse[1] <= button_y + \
                    button_height:
                pygame.draw.rect(screen, button_hover_color, [menu_back_x, button_y, 140, 40])
            else:
                pygame.draw.rect(screen, button_color, [menu_back_x, button_y, 140, 40])

            screen.blit(text_back, (menu_back_x + 15, button_y + 10))

            # updates the frames of the game
            pygame.display.update()


# prints CPU hand to screen
def print_cpu_hands(game, screen):
    cpus = [game.cpu1, game.cpu2, game.cpu3]

    # iterates through each CPU in game to print
    for i in range(len(cpus)):
        cpu = cpus[i]
        hand_size = len(cpu.get_hand())

        # first CPU prints to left side of screen
        if i == 0:
            hand_start = 0
            hand_height = screen.get_height() * (1 / 6)  # starts printing 1/6th from top of screen

            # if the hand size is less than three, no overlapping of cards, center hand
            if hand_size <= 3:
                card_offset = hand_height - 30 + (.5 * (3 - hand_size) * 120)  # space in between each card
                for _ in cpu.get_hand():
                    card_face = pygame.image.load('cards/card_back.png')

                    # transforms to default size
                    card_face = pygame.transform.scale(card_face, (100, 140))

                    # rotate image
                    card_face = pygame.transform.rotate(card_face, -90)
                    card_rect = card_face.get_rect()

                    # set x and y coordinates of card
                    card_rect.y = hand_height + card_offset
                    card_rect.x = hand_start + 30
                    screen.blit(card_face, card_rect)  # print to screen
                    card_offset += 120  # card size plus space between cards

            else:
                # multiple cards left in hand, calculates overlap of each card
                card_offset = 30  # space in between each card
                max_size = screen.get_height() * 2 / 3 - 120  # maximum size of space hand can take up on screen
                hand_width = 120 * hand_size
                overlap = 0

                # the max size of screen is less than hand width, begin overlapping cards
                while max_size < hand_width:
                    overlap += 1
                    hand_width = (120 - overlap) * hand_size  # determines width of entire hand with overlap

                for _ in cpu.get_hand():
                    card_face = pygame.image.load('cards/card_back.png')

                    # transforms to default size
                    card_face = pygame.transform.scale(card_face, (100, 140))

                    # rotate image
                    card_face = pygame.transform.rotate(card_face, -90)
                    card_rect = card_face.get_rect()

                    # set x and y coordinates of card
                    card_rect.y = hand_height + card_offset
                    card_rect.x = hand_start + 30
                    screen.blit(card_face, card_rect)  # print to screen

                    # change width of rectangle to only include part of card not covered for event handling
                    card_rect.width = card_rect.width - overlap
                    card_offset += 120 - overlap  # card size plus space between cards minus overlap of cards

        # if cpu is on top of screen
        elif i == 1:
            hand_height = 0

            # starts printing 1/6th from top of screen
            hand_start = screen.get_width() * (1 / 6)

            # if the hand size is less than six, no overlapping of cards, center hand
            if hand_size <= 6:
                card_offset = hand_start + 30 + (.5 * (6 - hand_size) * 120)  # space in between each card
                for _ in cpu.get_hand():
                    card_face = pygame.image.load('cards/card_back.png')

                    # transforms to default size
                    card_face = pygame.transform.scale(card_face, (100, 140))

                    # rotate image
                    card_face = pygame.transform.rotate(card_face, 180)
                    card_rect = card_face.get_rect()

                    # set x and y coordinates of card
                    card_rect.y = hand_height + 30
                    card_rect.x = card_offset
                    screen.blit(card_face, card_rect)  # print to screen
                    card_offset += 120  # card size plus space between cards

            else:
                card_offset = hand_start + 30  # space in between each card
                max_size = screen.get_width() * 2 / 3 - 60  # maximum size of space hand can take up on screen
                hand_width = 120 * hand_size  # width of entire hand
                overlap = 0

                # the max size of screen is less than width of entire hand, begin overlapping cards
                while max_size < hand_width:
                    overlap += 1
                    hand_width = (120 - overlap) * hand_size  # determines width of entire hand with overlap

                for _ in cpu.get_hand():
                    card_face = pygame.image.load('cards/card_back.png')

                    # transforms to default size
                    card_face = pygame.transform.scale(card_face, (100, 140))

                    # rotate image
                    card_face = pygame.transform.rotate(card_face, 180)
                    card_rect = card_face.get_rect()

                    # set x and y coordinates of card
                    card_rect.y = hand_height + 30
                    card_rect.x = card_offset
                    screen.blit(card_face, card_rect)  # print to screen

                    # change width of rectangle to only include part of card not covered for event handling
                    card_rect.width = card_rect.width - overlap
                    card_offset += 120 - overlap  # card size plus space between cards minus overlap of cards

        # CPU on right side of screen
        else:
            hand_start = screen.get_width() - 200  # starts printing cards 200 from right side of screen
            hand_height = screen.get_height() * (1 / 6)  # starts printing hand 1/6th from top of screen

            # if the hand size is less than three, no overlapping of cards, center hand
            if hand_size <= 3:

                card_offset = hand_height - 30 + (.5 * (3 - hand_size) * 120)  # space in between each card
                for _ in cpu.get_hand():
                    card_face = pygame.image.load('cards/card_back.png')

                    # transforms to default size
                    card_face = pygame.transform.scale(card_face, (100, 140))

                    # rotate image
                    card_face = pygame.transform.rotate(card_face, 90)
                    card_rect = card_face.get_rect()

                    # set x and y coordinates of card
                    card_rect.y = hand_height + card_offset
                    card_rect.x = hand_start + 30
                    screen.blit(card_face, card_rect)  # print to screen

                    card_offset += 120  # card size plus space between cards

            else:
                card_offset = 30  # space in between each card
                max_size = screen.get_height() * 2 / 3 - 120  # maximum size of space hand can take up on screen
                hand_width = 120 * hand_size  # width of entire hand
                overlap = 0

                # the max size of screen is less than width of entire hand, begin overlapping cards
                while max_size < hand_width:
                    overlap += 1
                    hand_width = (120 - overlap) * hand_size  # determines width of entire hand with overlap
                for _ in cpu.get_hand():
                    card_face = pygame.image.load('cards/card_back.png')

                    # transforms to default size
                    card_face = pygame.transform.scale(card_face, (100, 140))

                    # rotate image
                    card_face = pygame.transform.rotate(card_face, 90)
                    card_rect = card_face.get_rect()

                    # set x and y coordinates of card
                    card_rect.y = hand_height + card_offset
                    card_rect.x = hand_start + 30
                    screen.blit(card_face, card_rect)  # print to screen

                    # change width of rectangle to only include part of card not covered for event handling
                    card_rect.width = card_rect.width - overlap
                    card_offset += 120 - overlap  # card size plus space between cards minus overlap of cards


# prints player hand to screen
def print_player_hand(game, screen: pygame.Surface):
    list_of_rect_card.clear()
    player = game.player
    hand_size = len(player.get_hand())
    hand_height = screen.get_height() - 200  # begin printing hand 200 from bottom
    hand_start = screen.get_width() * (1 / 6)  # begin printing hand 1/6th from left side of screen

    # if the hand size is less than six, no overlapping of cards, center hand
    if hand_size <= 6:

        card_offset = hand_start + 30 + (.5 * (6 - hand_size) * 120)  # space in between each card
        for card in player.get_hand():
            card_face = pygame.image.load(card.get_path())  # get path of card image

            # transforms to default size
            card_face = pygame.transform.scale(card_face, (100, 140))
            card_rect = card_face.get_rect()

            # set x and y coordinates of card
            card_rect.y = hand_height + 30
            card_rect.x = card_offset
            screen.blit(card_face, card_rect)  # print to screen

            # add to list of user rectangle cards for event handling
            list_of_rect_card.append(card_rect)
            card_offset += 120  # card size plus space between cards

    else:
        card_offset = hand_start + 30  # space in between each card
        max_size = screen.get_width() * 2 / 3 - 60  # maximum width of hand space on screen
        hand_width = 120 * hand_size  # width of entire hand
        overlap = 0

        # the max size of screen is less than width of entire hand, begin overlapping cards
        while max_size < hand_width:
            overlap += 1
            hand_width = (120 - overlap) * hand_size  # determines width of entire hand with overlap

        for card in player.get_hand():
            card_face = pygame.image.load(card.get_path())  # get path of card image

            # transforms to default size
            card_face = pygame.transform.scale(card_face, (100, 140))
            card_rect = card_face.get_rect()

            # set x and y coordinates of card
            card_rect.y = hand_height + 30
            card_rect.x = card_offset

            screen.blit(card_face, card_rect)  # print to screen

            # change width of rectangle to only include part of card not covered for event handling
            card_rect.width = card_rect.width - overlap

            # add to list of user rectangle cards for event handling
            list_of_rect_card.append(card_rect)
            card_offset += 120 - overlap  # card size plus space between cards minus overlap of cards


# prints card last played and deck of cards
def print_top_card(game, screen):
    # gets image of last card played
    top_card = print_card(game.last_played)
    deck_cover = pygame.image.load('cards/card_back.png')
    deck_cover = pygame.transform.scale(deck_cover, (100, 140))  # transforms to default size

    # print to screen
    screen.blit(top_card, (((screen.get_width() / 2) - 120), (screen.get_height() / 2) - 70))
    screen.blit(deck_cover, (((screen.get_width() / 2) + 20), (screen.get_height() / 2) - 70))


# gets image of card to load to screen, returns card image
def print_card(card):
    graphics_card = pygame.image.load(card.get_path())
    graphics_card = pygame.transform.scale(graphics_card, (100, 140))  # transforms to default size
    return graphics_card


# allows the user to choose the card through event handlers and also contains calls to the cpu card choosing algorithm
def choose_card(screen, game):
    current_player = game.players[game.current_player]

    # creates a rectangle for the draw card event and blits an image onto it
    deck_cover = pygame.image.load('cards/card_back.png')
    deck_cover = pygame.transform.scale(deck_cover, (100, 140))
    deck_rect = deck_cover.get_rect()
    deck_rect.x = (screen.get_width() / 2) + 20
    deck_rect.y = (screen.get_height() / 2) - 70
    screen.blit(deck_cover, deck_rect)
    user_answer = False

    # while user has not played or drawn a card from the deck
    while user_answer is False and type(game.players[game.current_player]) == Player:

        while True:  # handles events
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:

                    # handles player event for drawing a card
                    if deck_rect.collidepoint(ev.pos):
                        card = game.draw_card()
                        deck_cover = pygame.image.load('cards/card_back.png')
                        deck_cover = pygame.transform.scale(deck_cover, (100, 140))
                        deck_cover_rect = deck_cover.get_rect()
                        deck_cover_rect.x = (screen.get_width() / 2) + 20
                        deck_cover_rect.y = (screen.get_height() / 2) - 70
                        for x in range(20):
                            # re-update screen every time card moves up # of pixels
                            print_game(game, screen)
                            # move card object up 10 pixels at a time
                            deck_cover_rect = deck_cover_rect.move(0, 10)
                            screen.blit(deck_cover, deck_cover_rect)  # blit it to the new position
                            pygame.display.update()
                            pygame.time.delay(10)

                        # re-update screen once card animation is over
                        print_game(game, screen)

                        if game.validate_move(card):  # checks if drawn card can be played and allows user to if so
                            card_face = pygame.image.load(card.get_path())
                            card_face = pygame.transform.scale(card_face, (100, 140))
                            card_rect = card_face.get_rect()

                            # confirm if user wants to play drawn card
                            result = confirm_user_card(card, card_rect, screen)

                            # update screen after user confirmation
                            print_game(game, screen)

                            # if the user wants to play it, play card
                            if result:
                                card_rect.x = (screen.get_width() / 2) - 50
                                card_rect.y = screen.get_height() - 170
                                for x in range(20):
                                    # re-update screen every time card moves up # of pixels
                                    print_game(game, screen)

                                    # move card object up 10 pixels at a time
                                    card_rect = card_rect.move(0, -10)
                                    screen.blit(card_face, card_rect)  # blit it to the new position
                                    pygame.time.delay(10)  # add time delay so it doesn't happen all at once
                                    pygame.display.update()
                                return card

                            # otherwise add to user hand
                            else:
                                current_player.add_card(card)
                                return False
                        else:  # adds to hand if the card wouldn't be a valid move
                            current_player.add_card(card)
                            return False

                    # checks to see which card user clicked on
                    for i in range(len(list_of_rect_card)):
                        if list_of_rect_card[i].collidepoint(ev.pos):
                            rect_position = list_of_rect_card[i]  # gets rectangle card object user clicked on

                            # calls to confirm card to confirm user selection of card played
                            user_answer = confirm_user_card(current_player.get_hand()[i], rect_position, screen)

                            # if user wants to play their card, update screen and play card
                            if user_answer:

                                # updates screen
                                print_game(game, screen)

                                if game.validate_move(current_player.get_hand()[i]):  # validates choice
                                    position = list_of_rect_card.pop(i)
                                    pygame.display.update()
                                    card_played = pygame.image.load(current_player.get_hand()[i].get_path())
                                    card_selected = current_player.get_hand().pop(i)
                                    # re-update screen once card animation is over

                                    # animation
                                    for x in range(20):
                                        # re-update screen every time card moves up # of pixels
                                        print_game(game, screen)

                                        # move card object up 10 pixels at a time
                                        position = position.move(0, -10)
                                        screen.blit(card_played, position)  # blit it to the new position
                                        pygame.time.delay(10)  # add time delay so it doesn't happen all at once
                                        pygame.display.update()

                                    # re-update screen once card animation is over
                                    print_game(game, screen)
                                    return card_selected
                                pygame.display.update()
                            # if the user does not want to play the selected card, re-update screen
                            # and let them select again
                            elif user_answer is False:

                                print_game(game, screen)
                                pygame.display.update()

    for ev in pygame.event.get():  # allows user to exit during cpu turn
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    card_face = pygame.image.load('cards/card_back.png')
    card_face = pygame.transform.scale(card_face, (100, 140))

    if current_player.get_number() == 1:  # handles first cpu move
        card_face = pygame.transform.rotate(card_face, -90)
        card_rect = card_face.get_rect()
        card_rect.x = 30
        card_rect.y = (screen.get_height() / 2) - 50
        direction = (10, 0)
        card = current_player.play_card(game.player, game.cpu3, game.cpu2, game.last_played)  # calls cpu choice alg
        pygame.display.update()

    elif current_player.get_number() == 2:  # handles second cpu move
        card_face = pygame.transform.rotate(card_face, 180)
        card_rect = card_face.get_rect()
        card_rect.x = (screen.get_width() / 2) - 50
        card_rect.y = 30
        direction = (0, 10)
        card = current_player.play_card(game.player, game.cpu1, game.cpu3, game.last_played)  # calls cpu choice alg
        pygame.display.update()

    else:  # handles third cpu move
        card_face = pygame.transform.rotate(card_face, 90)
        card_rect = card_face.get_rect()
        card_rect.x = screen.get_width() - 170
        card_rect.y = (screen.get_height() / 2) - 50
        direction = (-10, 0)
        card = current_player.play_card(game.player, game.cpu1, game.cpu2, game.last_played)  # calls cpu choice alg
        pygame.display.update()

    if not card:  # draws card for cpu
        current_player.add_card(game.draw_card())

        # handles animation if card is valid
        if game.validate_move(current_player.get_hand()[len(current_player.get_hand()) - 1]):
            print_game(game, screen)
            # move card object up 10 pixels at a time
            for x in range(20):
                print_game(game, screen)
                deck_rect = deck_rect.move(-5, 0)
                screen.blit(card_face, deck_rect)  # blit it to the new position
                pygame.time.delay(10)
                pygame.display.update()
            print_game(game, screen)
            return current_player.get_hand().pop(len(current_player.get_hand()) - 1)

        else:  # adds to hand
            for x in range(20):
                # re-update screen every time card moves up # of pixels
                print_game(game, screen)

                # move card object up 10 pixels at a time
                deck_rect = deck_rect.move(-(direction[0]), -(direction[1]))
                screen.blit(card_face, deck_rect)  # blit it to the new position
                pygame.time.delay(10)  # add time delay so it doesn't happen all at once
                pygame.display.update()
            print_game(game, screen)
            return False  # returns false if no valid card is found
    else:  # adds to hand

        for x in range(20):
            # re-update screen every time card moves up # of pixels
            # screen.fill(black)
            print_game(game, screen)

            # move card object up 10 pixels at a time
            card_rect = card_rect.move(direction)
            screen.blit(card_face, card_rect)  # blit it to the new position
            pygame.time.delay(10)  # add time delay so it doesn't happen all at once
            pygame.display.update()
        print_game(game, screen)

        return card  # returns card if one is found


# function for handling the user confirming a chosen or valid card
def confirm_user_card(card_selected, rectangle, screen):
    screen.fill(black)  # clear the screen
    button_height = 100
    button_width = 150

    pygame.display.update()
    card_played = pygame.image.load(card_selected.get_path())
    rectangle.x = screen.get_width() / 2 - 75
    rectangle.y = screen.get_height() / 2 - 75

    # blit the card selected by user to screen
    screen.blit(card_played, rectangle)

    # yes or no buttons for user selection
    yes_button = pygame.draw.rect(screen, blue,
                                  [screen.get_width() / 2 - 165, screen.get_height() / 2 + 200, button_width,
                                   button_height])
    no_button = pygame.draw.rect(screen, red,
                                 [screen.get_width() / 2 - 165 + 160, screen.get_height() / 2 + 200, button_width,
                                  button_height])
    yes = small_font.render('Yes', True, black)
    no = small_font.render('No', True, black)

    # blit buttons and text description to screen
    description = small_font.render("Would you like to play this card?", True, white)
    screen.blit(yes, (screen.get_width() / 2 - 110, screen.get_height() / 2 + 235))
    screen.blit(no, (screen.get_width() / 2 - 110 + 160, screen.get_height() / 2 + 235))
    screen.blit(description, (screen.get_width() / 2 - 200, screen.get_height() / 2 - 150))
    pygame.display.update()

    while True:  # handles events for if the player clicks yes or no
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mouse = pygame.mouse.get_pos()
                # if yes button is clicked on
                if yes_button.x <= mouse[0] <= yes_button.x + button_width and yes_button.y <= mouse[
                        1] <= yes_button.y + button_height:
                    return True
                # if no button is clicked on
                if no_button.x <= mouse[0] <= no_button.x + button_width and no_button.y <= mouse[
                        1] <= no_button.y + button_height:
                    return False


# handles choosing the wild card color for the player
def set_wild(screen):
    button_size = 150
    blue_button = pygame.draw.rect(screen, blue,
                                   [(screen.get_width() / 2) - button_size - 75, (screen.get_height() / 2) - 75,
                                    button_size, button_size])
    yellow_button = pygame.draw.rect(screen, yellow,
                                     [(screen.get_width() / 2) + button_size - 75, (screen.get_height() / 2) - 75,
                                      button_size, button_size])
    red_button = pygame.draw.rect(screen, red,
                                  [(screen.get_width() / 2) - 75, (screen.get_height() / 2) - button_size - 75,
                                   button_size, button_size])
    green_button = pygame.draw.rect(screen, green,
                                    [(screen.get_width() / 2) - 75, (screen.get_height() / 2) + button_size - 75,
                                     button_size, button_size])

    pygame.display.update()

    while True:  # event handler
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mouse = pygame.mouse.get_pos()

                # handles return the color corresponding to the button clicked on
                if blue_button.x <= mouse[0] <= blue_button.x + button_size and blue_button.y <= mouse[
                        1] <= blue_button.y + button_size:
                    return Color.BLUE
                elif red_button.x <= mouse[0] <= red_button.x + button_size and red_button.y <= mouse[
                        1] <= red_button.y + button_size:
                    return Color.RED
                elif green_button.x <= mouse[0] <= green_button.x + button_size and green_button.y <= mouse[
                        1] <= green_button.y + button_size:
                    return Color.GREEN
                elif yellow_button.x <= mouse[0] <= yellow_button.x + button_size and yellow_button.y <= mouse[
                        1] <= yellow_button.y + button_size:
                    return Color.YELLOW


def print_arrows(game, screen):
    # set the x position for the arrow that will correspond to the player
    arrow_player_x = (screen.get_width() / 2) - 75
    # set the y position for the arrow that will correspond to the player
    arrow_player_y = (screen.get_height() / 2) + 100
    # load the 4 different player arrow images and assign each to a variable
    arrow_highlight_player = pygame.image.load('arrows/light_arrow_player.png')
    arrow_highlight_reverse_player = pygame.image.load('arrows/light_arrow_reverse_player.png')
    arrow_dark_player = pygame.image.load('arrows/dark_arrow_player.png')
    arrow_dark_reverse_player = pygame.image.load('arrows/dark_arrow_reverse_player.png')
    # if the game is not reversed and it is the player turn show the highlighted arrow
    if not game.reversed and game.current_player == 0:
        arrow_player_rect = arrow_highlight_player.get_rect()
        arrow_player_rect.x = arrow_player_x
        arrow_player_rect.y = arrow_player_y
        screen.blit(arrow_highlight_player, arrow_player_rect)
    # if the game is not reversed and it is not the players turn show the dark arrow
    elif not game.reversed and game.current_player != 0:
        arrow_player_rect = arrow_dark_player.get_rect()
        arrow_player_rect.x = arrow_player_x
        arrow_player_rect.y = arrow_player_y
        screen.blit(arrow_dark_player, arrow_player_rect)
    # if the game is reversed and it is the players turn show the reversed highlighted arrow
    elif game.reversed and game.current_player == 0:
        arrow_player_rect = arrow_highlight_reverse_player.get_rect()
        arrow_player_rect.x = arrow_player_x
        arrow_player_rect.y = arrow_player_y
        screen.blit(arrow_highlight_reverse_player, arrow_player_rect)
    # if the game is not reversed and it is not the players turn show the reversed dark arrow
    elif game.reversed and game.current_player != 0:
        arrow_player_rect = arrow_dark_reverse_player.get_rect()
        arrow_player_rect.x = arrow_player_x
        arrow_player_rect.y = arrow_player_y
        screen.blit(arrow_dark_reverse_player, arrow_player_rect)
    # set the x position for the arrow that will correspond to the CPU on the left
    arrow_cpu1_x = (screen.get_width() / 2) - 200
    # set the y position for the arrow that will correspond to the CPU on the left
    arrow_cpu1_y = (screen.get_height() / 2) - 75
    # load the 4 different CPU1 arrow images and assign each to a variable
    arrow_highlight_cpu1 = pygame.image.load('arrows/light_arrow_cpu1.png')
    arrow_highlight_reverse_cpu1 = pygame.image.load('arrows/light_arrow_reverse_cpu1.png')
    arrow_dark_cpu1 = pygame.image.load('arrows/dark_arrow_cpu1.png')
    arrow_dark_reverse_cpu1 = pygame.image.load('arrows/dark_arrow_reverse_cpu1.png')
    # if the game is not reversed and it is the CPU1 turn show the highlighted arrow
    if not game.reversed and game.current_player == 1:
        arrow_cpu1_rect = arrow_highlight_cpu1.get_rect()
        arrow_cpu1_rect.x = arrow_cpu1_x
        arrow_cpu1_rect.y = arrow_cpu1_y
        screen.blit(arrow_highlight_cpu1, arrow_cpu1_rect)
    # if the game is not reversed and it is not the CPU1 turn show the dark arrow
    elif not game.reversed and game.current_player != 1:
        arrow_cpu1_rect = arrow_dark_cpu1.get_rect()
        arrow_cpu1_rect.x = arrow_cpu1_x
        arrow_cpu1_rect.y = arrow_cpu1_y
        screen.blit(arrow_dark_cpu1, arrow_cpu1_rect)
    # if the game is reversed and it is the CPU1 turn show the reversed highlighted arrow
    elif game.reversed and game.current_player == 1:
        arrow_cpu1_rect = arrow_highlight_reverse_cpu1.get_rect()
        arrow_cpu1_rect.x = arrow_cpu1_x
        arrow_cpu1_rect.y = arrow_cpu1_y
        screen.blit(arrow_highlight_reverse_cpu1, arrow_cpu1_rect)
    # if the game is not reversed and it is not the CPU1 turn show the reversed dark arrow
    elif game.reversed and game.current_player != 1:
        arrow_cpu1_rect = arrow_dark_reverse_cpu1.get_rect()
        arrow_cpu1_rect.x = arrow_cpu1_x
        arrow_cpu1_rect.y = arrow_cpu1_y
        screen.blit(arrow_dark_reverse_cpu1, arrow_cpu1_rect)
    # set the x position for the arrow that will correspond to the CPU above the player
    arrow_cpu2_x = (screen.get_width() / 2) - 75
    # set the y position for the arrow that will correspond to the CPU above the player
    arrow_cpu2_y = (screen.get_height() / 2) - 160
    # load the 4 different CPU2 arrow images and assign each to a variable
    arrow_highlight_cpu2 = pygame.image.load('arrows/light_arrow_cpu2.png')
    arrow_highlight_reverse_cpu2 = pygame.image.load('arrows/light_arrow_reverse_cpu2.png')
    arrow_dark_cpu2 = pygame.image.load('arrows/dark_arrow_cpu2.png')
    arrow_dark_reverse_cpu2 = pygame.image.load('arrows/dark_arrow_reverse_cpu2.png')
    # if the game is not reversed and it is the CPU2 turn show the highlighted arrow
    if not game.reversed and game.current_player == 2:
        arrow_cpu2_rect = arrow_highlight_cpu2.get_rect()
        arrow_cpu2_rect.x = arrow_cpu2_x
        arrow_cpu2_rect.y = arrow_cpu2_y
        screen.blit(arrow_highlight_cpu2, arrow_cpu2_rect)
    # if the game is not reversed and it is not the CPU2 turn show the dark arrow
    elif not game.reversed and game.current_player != 2:
        arrow_cpu2_rect = arrow_dark_cpu2.get_rect()
        arrow_cpu2_rect.x = arrow_cpu2_x
        arrow_cpu2_rect.y = arrow_cpu2_y
        screen.blit(arrow_dark_cpu2, arrow_cpu2_rect)
    # if the game is reversed and it is the CPU2 turn show the reversed highlighted arrow
    elif game.reversed and game.current_player == 2:
        arrow_cpu2_rect = arrow_highlight_reverse_cpu2.get_rect()
        arrow_cpu2_rect.x = arrow_cpu2_x
        arrow_cpu2_rect.y = arrow_cpu2_y
        screen.blit(arrow_highlight_reverse_cpu2, arrow_cpu2_rect)
    # if the game is not reversed and it is not the CPU2 turn show the reversed dark arrow
    elif game.reversed and game.current_player != 2:
        arrow_cpu2_rect = arrow_dark_reverse_cpu2.get_rect()
        arrow_cpu2_rect.x = arrow_cpu2_x
        arrow_cpu2_rect.y = arrow_cpu2_y
        screen.blit(arrow_dark_reverse_cpu2, arrow_cpu2_rect)
    # set the x position for the arrow that will correspond to the CPU on the right
    arrow_cpu3_x = (screen.get_width() / 2) + 140
    # set the y position for the arrow that will correspond to the CPU on the right
    arrow_cpu3_y = (screen.get_height() / 2) - 75
    # load the 4 different CPU3 arrow images and assign each to a variable
    arrow_highlight_cpu3 = pygame.image.load('arrows/light_arrow_cpu3.png')
    arrow_highlight_reverse_cpu3 = pygame.image.load('arrows/light_arrow_reverse_cpu3.png')
    arrow_dark_cpu3 = pygame.image.load('arrows/dark_arrow_cpu3.png')
    arrow_dark_reverse_cpu3 = pygame.image.load('arrows/dark_arrow_reverse_cpu3.png')
    # if the game is not reversed and it is the CPU3 turn show the highlighted arrow
    if not game.reversed and game.current_player == 3:
        arrow_cpu3_rect = arrow_highlight_cpu3.get_rect()
        arrow_cpu3_rect.x = arrow_cpu3_x
        arrow_cpu3_rect.y = arrow_cpu3_y
        screen.blit(arrow_highlight_cpu3, arrow_cpu3_rect)
    # if the game is not reversed and it is not the CPU3 turn show the dark arrow
    elif not game.reversed and game.current_player != 3:
        arrow_cpu3_rect = arrow_dark_cpu3.get_rect()
        arrow_cpu3_rect.x = arrow_cpu3_x
        arrow_cpu3_rect.y = arrow_cpu3_y
        screen.blit(arrow_dark_cpu3, arrow_cpu3_rect)
    # if the game is reversed and it is the CPU3 turn show the reversed highlighted arrow
    elif game.reversed and game.current_player == 3:
        arrow_cpu3_rect = arrow_highlight_reverse_cpu3.get_rect()
        arrow_cpu3_rect.x = arrow_cpu3_x
        arrow_cpu3_rect.y = arrow_cpu3_y
        screen.blit(arrow_highlight_reverse_cpu3, arrow_cpu3_rect)
    # if the game is not reversed and it is not the CPU3 turn show the reversed dark arrow
    elif game.reversed and game.current_player != 3:
        arrow_cpu3_rect = arrow_dark_reverse_cpu3.get_rect()
        arrow_cpu3_rect.x = arrow_cpu3_x
        arrow_cpu3_rect.y = arrow_cpu3_y
        screen.blit(arrow_dark_reverse_cpu3, arrow_cpu3_rect)


def print_names(game, screen):
    # get the player name from the user text input
    player_name = name_font.render(game.players[0].get_name().get_text(), True, white)
    # get each of the pre-defined computer names from the game
    cpu1_name = name_font.render(game.players[1].get_name(), True, white)
    cpu2_name = name_font.render(game.players[2].get_name(), True, white)
    cpu3_name = name_font.render(game.players[3].get_name(), True, white)
    # print the names out to the corresponding players so the user can see which hand belongs to which player
    screen.blit(player_name, ((screen.get_width() / 2) - len(game.players[0].get_name().get_text()) * 6, 570))
    screen.blit(cpu2_name, ((screen.get_width() / 2) - len(game.players[1].get_name()) * 6, 205))
    screen.blit(cpu1_name, (205, (screen.get_height() / 2) - 10))
    screen.blit(cpu3_name, (1000 - len(game.players[1].get_name()) * 12, (screen.get_height() / 2) - 10))


def draw_uno(screen):
    # load and print the uno logo onto the screen
    uno = pygame.image.load('background.png')
    uno = pygame.transform.scale(uno, (135, 95))
    screen.blit(uno, (screen.get_width() - 165, screen.get_height() - 138))


def print_rules(screen):
    # load the image with the rules into a variable
    rules_png = pygame.image.load('rules.PNG')
    # create a new screen from the size of the previous screen
    screen = pygame.display.set_mode(screen.get_size())
    # set the text for the Menu button
    text_back = tiny_font.render('     Menu', True, black)
    # fill the new screen with a white background
    screen.fill(white)
    # show the picture with the rules
    screen.blit(rules_png, (20, 20))
    # create a boarder of rectangles in the uno colors
    pygame.draw.rect(screen, blue, [0, 0, 20, 800])
    pygame.draw.rect(screen, green, [1180, 0, 20, 800])
    pygame.draw.rect(screen, red, [0, 0, 1200, 20])
    pygame.draw.rect(screen, yellow, [0, 780, 1200, 20])
    show_rules = True
    # continue to show the rules until the user clicks the menu button
    while show_rules:
        # button dimensions
        button_width = 140
        button_height = 40
        width = screen.get_width()
        height = screen.get_height()
        # assign the starting position for the menu button
        menu_back_x = (width * .1) - (button_width / 2)
        button_y = (height * .85) + (button_height / 2)
        mouse = pygame.mouse.get_pos()
        # handles events
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # checks if a mouse button is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                # if the mouse button was clicked over the button then return to the main menu
                if menu_back_x <= mouse[0] <= menu_back_x + button_width and button_y <= mouse[
                        1] <= button_y + button_height:
                    show_rules = False
                    game_engine()

        # if the mouse is hovering over the button change the color to show the user it is highlighted
        if menu_back_x <= mouse[0] <= menu_back_x + button_width and button_y <= mouse[
                1] <= button_y + button_height:
            pygame.draw.rect(screen, button_hover_color, [menu_back_x, button_y, 140, 40])
        # if the mouse is not over the button change it back to the original color
        else:
            pygame.draw.rect(screen, button_color, [menu_back_x, button_y, 140, 40])
        screen.blit(text_back, (menu_back_x + 15, button_y + 10))

        # updates the frames of the game
        pygame.display.update()


def print_game(game, screen):
    # call all the print functions all at once
    screen.blit(table, (0, 0))
    print_arrows(game, screen)
    print_cpu_hands(game, screen)
    print_top_card(game, screen)
    print_player_hand(game, screen)
    print_names(game, screen)
    draw_uno(screen)


if __name__ == '__main__':
    game_engine()
