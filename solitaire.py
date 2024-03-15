import pygame
import sys
import random
import math


class Card:
    """
    The class Card represents the game cards
    It has different methods for dealing with the cards
    """

    def __init__(self, number, symbol):
        """
        Card constructor

        Args:
            self: refer to the current instance
            number: number of the card (1,2,..,13)
            symbol: symbol of card (hearts,diamons,clubs,spades)

        Returns:
            None
        """
        self.number = number
        self.symbol = symbol
        self.face_up = False

    def flip(self):
        """
        Flips the card upwards or downwards depending of the original state.

        Args:
            self: refer to the current instance

        Returns:
            None
        """
        self.face_up = not self.face_up

    def draw(self, screen, x, y):
        """
        Draw this instance of the card on the screen.

        Args:
            self: refer to the current instance
            screen: the pygame screen
            x: the x coordinate of the card on the screen where the card will begin drawing
            y: the y coordinate of the card on the screen where the card will begin drawing

        Returns:
            None
        """
        card_image = pygame.image.load(
            f"Proiect Python/cards/clasic/{str(self.number)}_of_{self.symbol}.png"
        ).convert()
        card_back = pygame.image.load(
            "Proiect Python/cards/clasic/card_back.png"
        ).convert()

        # resize the card images
        new_width, new_height = 100, 150
        card_image = pygame.transform.scale(card_image, (new_width, new_height))
        card_back = pygame.transform.scale(card_back, (new_width, new_height))

        if self.face_up:
            screen.blit(card_image, (x, y))
        else:
            screen.blit(card_back, (x, y))

    def draw_top(self, screen, x, y):
        """
        Draw only the top size of the card. The first 30 pixels as height.

        Args:
            self: refer to the current instance
            screen: the pygame screen
            x: the x coordinate of the card on the screen where the card will begin drawing
            y: the y coordinate of the card on the screen where the card will begin drawing

        Returns:
            None
        """

        card_image = pygame.image.load(
            f"Proiect Python/cards/clasic/{str(self.number)}_of_{self.symbol}.png"
        ).convert()
        card_back = pygame.image.load(
            "Proiect Python/cards/clasic/card_back.png"
        ).convert()

        # resize the card images
        new_width, new_height = 100, 150
        card_image = pygame.transform.scale(card_image, (new_width, new_height))
        card_back = pygame.transform.scale(card_back, (new_width, new_height))

        # draw only the top 30 pixels of the card (space_tableau dimension)
        top_portion_rect = pygame.Rect(0, 0, new_width, 30)

        if self.face_up:
            screen.blit(card_image, (x, y), area=top_portion_rect)
        else:
            screen.blit(card_back, (x, y), area=top_portion_rect)

    def get_rect_at(self, x, y):
        """
        Get a rectangle at the location provided by (x,y) where the card is drawn.

        Args:
            self: refer to the current instance
            x: the x coordinate of the card on the screen where the card is
            y: the y coordinate of the card on the screen where the card is

        Returns:
            The rectangle shape that represents the card.
        """
        card_width, card_height = 100, 150
        return pygame.Rect(x, y, card_width, card_height)


# Card spacing (different constants for drawing and card positions):
card_width, card_height = 100, 150  # card dimension
space_width, space_height = 30, 15  # spacing from the left up corner
space_cards = 15  # space between cards
space_show, space_tableau = (
    25,
    30,
)  # space right between show_pile cards/ space down between cards in tableau
transparent_color = (20, 220, 50)  # (20,220,50,100)

# spacing from left top corner
stock_width, stock_height = space_width, space_height
show_width, show_height = card_width + space_width + space_cards, space_height
foundation_width, foundation_height = (
    space_width + (card_width + space_cards) * 3,
    space_height,
)
tableau_width, tableau_height = (
    space_width,
    card_height + space_height + space_cards * 2,
)

# Solitaire components (the five piles):
stock_pile = []  # cards to be drawn and used up-left, vector
show_pile = []  # the cards shown that can be used, vector 3 elements
waste_pile = []  # cards not chosen to be used and that will be reused later
foundation = [[], [], [], []]  # cards to be completed up-right, vector x4 each symbol
tableau = [[], [], [], [], [], [], []]  # cards to be used down, vector x7


# Methods that interact with the piles and the deck of cards
def generate_card_deck():
    """
    Generate a new deck of cards.

    Args:
        None

    Returns:
        The newly generated deck of cards
    """
    symbols = ["clubs", "diamonds", "hearts", "spades"]
    deck = []
    for number in range(1, 14):
        for symbol in symbols:
            card = Card(number, symbol)
            deck.append(card)

    return deck


def shuffle_deck(deck):
    """
    Shuffle the deck.

    Args:
        None

    Returns:
        The shuffled deck
    """
    random.shuffle(deck)


def split_deck_in_components(deck):
    """
    Splits the deck of cards in the different piles. Stock and tableau are the piles that
    are generated at the start of the game.

    Args:
        deck: the deck of cards

    Returns:
        The stock pile and the tableau at the start of a new game.
    """
    stock_pile = []
    tableau = [[], [], [], [], [], [], []]
    tableau_index = 1
    tableau_total = 1

    for index, card in enumerate(deck):
        if index < 28:
            if index < tableau_total:
                tableau[tableau_index - 1] = [card] + tableau[tableau_index - 1]
            else:
                tableau_index += 1
                tableau_total += tableau_index
                tableau[tableau_index - 1] = [card] + tableau[tableau_index - 1]
        else:
            stock_pile.append(card)

    # last cards in each tableau column need to be face up
    for i in range(7):
        tableau[i][i].flip()

    return stock_pile, tableau


def update_waste_pile(waste_pile):
    """
    Updates the waste pile with the cards not used from the show pile.

    Args:
        waste_pile: the waste pile that needs updating

    Returns:
        The updated waste_pile
    """

    show_cards = []

    if show_pile:
        for card in show_pile:
            show_cards += [card]

        waste_pile += show_cards[::-1]

        # waste_pile=waste_pile + [show_pile[2]]+ [show_pile[1]]+ [show_pile[0]]

    return waste_pile


def flip_show_pile(show_pile):
    """
    Flips the cards in the show pile if some are not already flipped

    Args:
        show_pile: the show pile

    Returns:
        The updated show pile
    """
    for card in show_pile:
        if card.face_up == False:
            card.flip()

    return show_pile


def stock_draw(stock_pile, show_pile, waste_pile):
    """
    Draw cards from the stock pile and update the stock,show and waste piles accordingly.

    Args:
        stock_pile: stock pile
        show_pile: show pile
        waste_pile: waste pile

    Returns:
        The updated stock,show and waste piles.
    """
    if (game_mode==3):
        if len(stock_pile) >= 3:
            waste_pile = update_waste_pile(waste_pile)
            show_pile = [stock_pile[2], stock_pile[1], stock_pile[0]]
            show_pile = flip_show_pile(show_pile)
            stock_pile = stock_pile[3:]

        elif len(stock_pile) == 2:
            waste_pile = update_waste_pile(waste_pile)
            if waste_pile:
                show_pile = [waste_pile[-1], stock_pile[1], stock_pile[0]]
            else:
                show_pile = [stock_pile[1], stock_pile[0]]
            show_pile = flip_show_pile(show_pile)
            stock_pile = []

        elif len(stock_pile) == 1:
            waste_pile = update_waste_pile(waste_pile)

            if len(waste_pile) >= 2:
                show_pile = [waste_pile[-1], waste_pile[-2], stock_pile[0]]
            elif waste_pile:
                show_pile = [waste_pile[-1], stock_pile[0]]
            else:
                show_pile = [stock_pile[0]]
            show_pile = flip_show_pile(show_pile)
            stock_pile = []

        else:
            waste_pile = update_waste_pile(waste_pile)

            # remove duplicates
            new_waste_pile = []
            seen_elements = set()
            for element in waste_pile:
                if element not in seen_elements:
                    new_waste_pile.append(element)
                    seen_elements.add(element)

            show_pile = []
            stock_pile = new_waste_pile
            waste_pile = []

            for card in stock_pile:
                card.flip()
    elif game_mode==1:
        waste_pile = update_waste_pile(waste_pile)
        if (stock_pile):
            show_pile=[stock_pile[0]]
            show_pile = flip_show_pile(show_pile)
            stock_pile=stock_pile[1:]
        else:
            show_pile = []
            stock_pile = waste_pile
            waste_pile = []

            for card in stock_pile:
                card.flip()


    return stock_pile, show_pile, waste_pile


def remove_card_start_location(screen, drawn_card_location, drawn_card_position):
    """
    Remove the moving card from where it was taken (if it is placed correctly).

    Args:
        screen: pygame screen
        drawn_card_location: which pile it is in (tableau-t, foundation-f, show-s)
        drawn_card_position: position in the pile

    Returns:
        The updated drawn_card_location, drawn_card_position.
    """

    if drawn_card_location == "s":
        del show_pile[drawn_card_position]
        pygame.draw.rect(
            screen,
            (20, 150, 50),
            (show_width, show_height, card_width + 2 * space_show, card_height),
        )
        draw_show(screen)

    elif drawn_card_location == "f":
        del foundation[drawn_card_position // 10][drawn_card_position % 10]
        pygame.draw.rect(
            screen,
            (20, 150, 50),
            (
                foundation_width,
                foundation_height,
                (card_width + space_cards) * 4,
                card_height,
            ),
        )
        draw_foundation(screen)

    elif drawn_card_location == "t":
        nr_tableau = drawn_card_position // 10
        length = len(tableau[nr_tableau])

        for index in range(
            len(tableau[drawn_card_position // 10]) - 1,
            drawn_card_position % 10 - 1,
            -1,
        ):
            del tableau[drawn_card_position // 10][index]

        # last card face up
        if tableau[nr_tableau]:
            if tableau[nr_tableau][-1].face_up == False:
                tableau[nr_tableau][-1].flip()

        pygame.draw.rect(
            screen,
            (20, 150, 50),
            (
                tableau_width + nr_tableau * (card_width + space_cards),
                tableau_height,
                card_width,
                card_height + space_tableau * length,
            ),
        )
        draw_tableau(screen, nr_tableau)

    drawn_card_location = None
    drawn_card_position = None

    return drawn_card_location, drawn_card_position


def place_card_foundation(placed_card, nr_foundation):
    """
    Verifies if the a card can be placed in foundation.

    Args:
        placed_card: the card that will be placed
        nr_foundation: which foundation pile

    Returns:
        True/False if the card can be placed in the foundation
    """
    if foundation[nr_foundation]:
        if (
            placed_card.number - 1 == foundation[nr_foundation][-1].number
            and placed_card.symbol == foundation[nr_foundation][-1].symbol
        ):
            return True

    elif placed_card.number == 1:
        return True

    return False


def opposed_color_symbol(symbol1, symbol2):
    """
    Verify if two cards symbols are the different colour (red-black)

    Args:
        symbol1: symbol of first card
        smymbol2: symbol of second card

    Returns:
        True/False if it is the opposed color or not.
    """
    if symbol1 == "clubs" or symbol1 == "spades":
        if symbol2 == "hearts" or symbol2 == "diamonds":
            return True
        else:
            return False

    elif symbol1 == "hearts" or symbol1 == "diamonds":
        if symbol2 == "clubs" or symbol2 == "spades":
            return True
        else:
            return False


def place_card_tableau(placed_card, nr_tableau):
    """
    Verifies if the a card can be placed in tableau.

    Args:
        placed_card: the card that will be placed
        nr_tableau: which tableau pile

    Returns:
        True/False if the card can be placed in the tableau
    """
    if tableau[nr_tableau]:
        if (
            placed_card.number + 1 == tableau[nr_tableau][-1].number
            and opposed_color_symbol(placed_card.symbol, tableau[nr_tableau][-1].symbol)
            == True
        ):
            return True

    elif placed_card.number == 13:
        return True

    return False


def end_game():
    """
    Verifies if the foundation pile is completed and the game is finished

    Args:
        None

    Returns:
        True/False if the game is finished
    """
    for columns in foundation:
        if len(columns) != 13:
            return False

    else:
        return True


# Methods for drawing piles/cards/buttons


def draw_rect_alpha(screen, color, rect):
    """
    Draw a rectangle (the ones on which the piles and cards will be placed)

    Args:
        screen: pygame screen
        color: color of the rectangle
        rect: rectangle object which will be drawn

    Returns:
        None
    """
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    screen.blit(shape_surf, rect)


def draw_stock(screen):
    """
    Draw the stock pile

    Args:
        screen: pygame screen

    Returns:
        None
    """
    draw_rect_alpha(
        screen, transparent_color, (stock_width, stock_height, card_width, card_height)
    )
    if stock_pile:
        stock_pile[0].draw(screen, stock_width, stock_height)


def draw_show(screen):
    """
    Draw the show pile

    Args:
        screen: pygame screen

    Returns:
        None
    """
    draw_rect_alpha(
        screen, transparent_color, (show_width, show_height, card_width, card_height)
    )
    if show_pile:
        for index, card in enumerate(show_pile):
            card.draw(screen, show_width + index * space_show, show_height)


def draw_foundation(screen):
    """
    Draw the foundation piles

    Args:
        screen: pygame screen

    Returns:
        None
    """
    for nr_foundation in range(4):
        draw_rect_alpha(
            screen,
            transparent_color,
            (
                foundation_width + (card_width + space_cards) * nr_foundation,
                foundation_height,
                card_width,
                card_height,
            ),
        )
        if foundation[nr_foundation]:
            foundation[nr_foundation][-1].draw(
                screen,
                foundation_width + (card_width + space_cards) * nr_foundation,
                foundation_height,
            )


def draw_tableau(screen, nr_tableau):
    """
    Draw the tableau pile with index nr_tableau

    Args:
        screen: pygame screen
        nr_tableau: tableau index

    Returns:
        None
    """
    draw_rect_alpha(
        screen,
        transparent_color,
        (
            tableau_width + (card_width + space_cards) * nr_tableau,
            tableau_height,
            card_width,
            card_height,
        ),
    )
    if tableau[nr_tableau]:
        for index, card in enumerate(tableau[nr_tableau]):
            card.draw(
                screen,
                tableau_width + (card_width + space_cards) * nr_tableau,
                tableau_height + space_tableau * index,
            )


def draw_tableau_specific(screen, nr_tableau, start_card_index, final_card_index):
    """
    Draw the tableau pile with index nr_tableau, but only some cards

    Args:
        screen: pygame screen
        nr_tableau: index of tableau pile
        start_card_index: starting index of cards
        final_card_index: ending index of cards

    Returns:
        None
    """
    if not tableau[nr_tableau]:
        draw_rect_alpha(
            screen,
            transparent_color,
            (
                tableau_width + (card_width + space_cards) * nr_tableau,
                tableau_height,
                card_width,
                card_height,
            ),
        )

    if tableau[nr_tableau] and (len(tableau[nr_tableau]) > final_card_index):
        for index in range(start_card_index, final_card_index + 1):
            tableau[nr_tableau][index].draw_top(
                screen,
                tableau_width + (card_width + space_cards) * nr_tableau,
                tableau_height + space_tableau * index,
            )

    if tableau[nr_tableau]:
        # if(final_card_index-4<=len(tableau[nr_tableau])-1):
        tableau[nr_tableau][len(tableau[nr_tableau]) - 1].draw(
            screen,
            tableau_width + (card_width + space_cards) * nr_tableau,
            tableau_height + space_tableau * (len(tableau[nr_tableau]) - 1),
        )


def draw_cards(screen):
    """
    Draw all card piles on the screen.

    Args:
        screen: pygame screen

    Returns:
        None
    """
    # green background
    screen.fill((20, 150, 50))

    # stock pile
    draw_stock(screen)
    # show pile
    draw_show(screen)

    # foundation
    draw_foundation(screen)

    # tableau
    for nr_tableau in range(7):
        draw_tableau(screen, nr_tableau)


# Measurments for draw_dirty_portion
xl_stock = stock_width
xr_stock = stock_width + card_width
yt_stock = stock_height
yb_stock = stock_height + card_height

xl_show = show_width
xr_show = show_width + card_width + 2 * space_show
yt_show = show_height
yb_show = show_height + card_height

xl_foundation = foundation_width
xr_foundation = foundation_width + card_width * 4 + space_cards * 3
yt_foundation = foundation_height
yb_foundation = foundation_height + card_height


def draw_dirty_portion(screen, x_topleft, y_topleft, x_bottomright, y_bottomright):
    """
    Draw the portion of the screen where the moving card was, so that
    it will not leave an empty space behind and the cards are still shown

    Args:
        screen: pygame screen
        x_topleft: x coordinate of the topleft corner of the dirty rectangle
        y_topleft: y coordinate of the topleft corner of the dirty rectangle
        x_bottomright: x coordinate of the bottomright corner of the dirty rectangle
        y_bottomright: y coordinate of the bottomright corner of the dirty rectangle

    Returns:
        None
    """
    # stock pile
    if (
        xl_stock <= x_topleft <= xr_stock or xl_stock <= x_bottomright <= xr_stock
    ) and (yt_stock <= y_topleft <= yb_stock or yt_stock <= y_bottomright <= yb_stock):
        draw_stock(screen)

    # show pile
    if (xl_show <= x_topleft <= xr_show or xl_show <= x_bottomright <= xr_show) and (
        yt_show <= y_topleft <= yb_show or yt_show <= y_bottomright <= yb_show
    ):
        draw_show(screen)

    # foundation
    if (
        xl_foundation <= x_topleft <= xr_foundation
        or xl_foundation <= x_bottomright <= xr_foundation
    ) and (
        yt_foundation <= y_topleft <= yb_foundation
        or yt_foundation <= y_bottomright <= yb_foundation
    ):
        draw_foundation(screen)

    # tableau
    if tableau_height < y_bottomright:
        counter_width = (x_bottomright - tableau_width) / (card_width + space_cards)
        counter_height_top = (y_topleft - tableau_height) / space_tableau
        counter_height_bottom = (y_bottomright - tableau_height) / space_tableau
        # momentan card_height=5*space_tableau

        if 1 <= counter_width < 7:
            s_index, f_index = adjust_counter_heights(
                counter_height_top, counter_height_bottom, math.ceil(counter_width - 1)
            )

            draw_tableau_specific(
                screen, math.ceil(counter_width - 1), s_index, f_index
            )

            s_index, f_index = adjust_counter_heights(
                counter_height_top, counter_height_bottom, math.floor(counter_width - 1)
            )
            draw_tableau_specific(
                screen, math.floor(counter_width - 1), s_index, f_index
            )

        elif 7 <= counter_width < 8:
            s_index, f_index = adjust_counter_heights(
                counter_height_top, counter_height_bottom, 6
            )
            draw_tableau_specific(screen, 6, s_index, f_index)

        elif 0 <= counter_width:
            s_index, f_index = adjust_counter_heights(
                counter_height_top, counter_height_bottom, 0
            )
            draw_tableau_specific(screen, 0, s_index, f_index)


def adjust_counter_heights(counter_height_top, counter_height_bottom, counter_width):
    """
    Determines the card indexes that need drawing

    Args:
        counter_height_top: counter of topleft corner of height
        counter_height_bottom: counter of bottomright corner of height
        counter_width: counter of width

    Returns:
        Starting and final indexes of the cards that need to be redrawn
    """
    nr_cards = len(tableau[counter_width])

    # moving card top under tableau or above tableau
    if counter_height_top > nr_cards + 4 or counter_height_bottom < 0:
        s_index, f_index = nr_cards, nr_cards

    # moving card top at last card
    elif counter_height_top >= nr_cards - 1:
        s_index, f_index = nr_cards - 1, nr_cards - 1

    else:
        s_index = math.floor(counter_height_top)
        f_index = math.floor(counter_height_bottom)
        if s_index < 0:
            s_index = 0
        if f_index >= nr_cards:
            f_index = nr_cards - 1

    return s_index, f_index


#  draw button
def draw_button(x, y, text_on_button):
    """
    Draw a button with text on it.

    Args:
        x: x coordinate on the screen
        y: y coordinate on the screen
        text_on_button: text to be drawn on the button

    Returns:
        None
    """
    button_width = 100
    button_height = 40

    pygame.draw.rect(screen, (169, 169, 169), (x, y, button_width, button_height))
    font = pygame.font.Font(None, 37)
    text = font.render(text_on_button, True, (0, 0, 0))

    text_width, text_height = font.size(text_on_button)
    text_x = x + (button_width - text_width) // 2
    text_y = y + (button_height - text_height) // 2
    screen.blit(text, (text_x, text_y))


# draw rules
def draw_rules(screen, filename):
    """
    Draw the rules on the screen.

    Args:
        screen: pygame screen
        filename: name of the txt file which will be used to get the rules from

    Returns:
        None
    """
    screen.fill((20, 150, 50), (0, 0, 900, 750))
    font = pygame.font.Font(None, 30)
    try:
        with open(filename, "r") as file:
            rules_text = file.read()
            lines = rules_text.splitlines()

            # Render each line separately
            y_offset = 50
            for line in lines:
                text = font.render(line, True, (0, 0, 0))
                screen.blit(text, (50, y_offset))
                y_offset += text.get_height() + 5
    except FileNotFoundError:
        print(f"File not found: {filename}")


def pick_card(card_x, card_y, position):
    """
    Update offsets for moving card

    Args:
        card_x: last x coordinate on the screen of the card
        card_y: last y coordinate on the screen of the card
        position: current card position

    Returns:
        The updated offsets
    """
    offset_x = card_x - position[0]
    offset_y = card_y - position[1]

    return offset_x, offset_y


def move_card(offset_x, offset_y, position):
    """
    Update the position coordinates  of the card.

    Args:
        offset_x: offset x of the card
        offset_y: offset y of the card
        position: current card position

    Returns:
        The updated coordinates of the card
    """
    card_x = position[0] + offset_x
    card_y = position[1] + offset_y

    return card_x, card_y


def set_moving(width, height, event):
    """
    Set the card as moving and update coordinates

    Args:
        width: current x of the card
        height: current y of the card
        event: the event (mouseclick)


    Returns:
        None
    """
    global moving, drawn_card_x, drawn_card_y, offset_x, offset_y
    moving = True
    drawn_card_x, drawn_card_y = width, height
    offset_x, offset_y = pick_card(width, height, event.pos)


# TEST
# card1=Card(7,"clubs")
# card2=Card(13,"hearts")
# card2.flip()

# for j in range(0,4):
#     for i in range(0,13):
#         foundation[j].append(card2)


# SOLITAIRE
# start pygame
pygame.init()

# window
width, height = 1000, 750
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Solitaire")

clock = pygame.time.Clock()
moving = False
drawn_card = None
game_mode=3

drawn_card_location = None  # s-show f-foundation t-tableau
drawn_card_position = None  # index in vector s-1,2,3 ; f,t- ab unde a->[nr_foundation/nr_tableau]; b-> pozitia in a

rules_drawn = False

font = pygame.font.Font(None, 36)

# deck preparation and draw the board
deck = generate_card_deck()
shuffle_deck(deck)
stock_pile, tableau = split_deck_in_components(deck)
draw_cards(screen)

dirty_rect = None

# main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            draw_cards(screen)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # click on stock_pile
                if (
                    stock_width < event.pos[0] < stock_width + card_width
                    and stock_height < event.pos[1] < stock_height + card_height
                ):
                    stock_pile, show_pile, waste_pile = stock_draw(
                        stock_pile, show_pile, waste_pile
                    )

                    # draw stock and show again
                    portion_rect = pygame.Rect(
                        stock_width,
                        stock_height,
                        show_width + card_width + space_show * 2,
                        card_height,
                    )
                    pygame.draw.rect(screen, (20, 150, 50), portion_rect)
                    draw_show(screen)
                    draw_stock(screen)

                # RESET BUTTON
                elif 900 <= event.pos[0] <= 1000 and 120 <= event.pos[1] <= 160:
                    deck = generate_card_deck()
                    shuffle_deck(deck)
                    stock_pile, tableau = split_deck_in_components(deck)
                    waste_pile = []
                    show_pile = []
                    foundation = [[], [], [], []]
                    draw_cards(screen)
                    rules_drawn = False

                # RULES BUTTON
                elif 900 <= event.pos[0] <= 1000 and 170 <= event.pos[1] <= 210:
                    if rules_drawn:
                        draw_cards(screen)
                        rules_drawn = False
                    else:
                        draw_rules(screen, "Proiect Python/rules.txt")
                        rules_drawn = True

                elif 900 <= event.pos[0] <= 1000 and 220 <= event.pos[1] <= 260:
                     
                    # change game mode
                    if game_mode==3:
                        game_mode=1
                    elif game_mode==1:
                        game_mode=3
                    
                    # reset game
                    deck = generate_card_deck()
                    shuffle_deck(deck)
                    stock_pile, tableau = split_deck_in_components(deck)
                    waste_pile = []
                    show_pile = []
                    foundation = [[], [], [], []]
                    draw_cards(screen)
                    rules_drawn = False

                # move card in show_pile
                if (
                    len(show_pile) == 3
                    and show_width + space_show * 2
                    < event.pos[0]
                    < show_width + space_show * 2 + card_width
                    and show_height < event.pos[1] < show_height + card_height
                ):
                    set_moving(show_width + space_show * 2, show_height, event)
                    drawn_card = show_pile[2]
                    drawn_card_location = "s"
                    drawn_card_position = 2

                elif (
                    len(show_pile) == 2
                    and show_width + space_show
                    < event.pos[0]
                    < show_width + space_show + card_width
                    and show_height < event.pos[1] < show_height + card_height
                ):
                    set_moving(show_width + space_show, show_height, event)
                    drawn_card = show_pile[1]
                    drawn_card_location = "s"
                    drawn_card_position = 1

                elif (
                    len(show_pile) == 1
                    and show_width < event.pos[0] < show_width + card_width
                    and show_height < event.pos[1] < show_height + card_height
                ):
                    set_moving(show_width, show_height, event)
                    drawn_card = show_pile[0]
                    drawn_card_location = "s"
                    drawn_card_position = 0

                # move card in foundation
                elif (
                    foundation[0]
                    and foundation_width < event.pos[0] < foundation_width + card_width
                    and foundation_height
                    < event.pos[1]
                    < foundation_height + card_height
                ):
                    set_moving(foundation_width, foundation_height, event)
                    drawn_card = foundation[0][-1]
                    drawn_card_location = "f"
                    drawn_card_position = len(foundation[0]) - 1

                elif (
                    foundation[1]
                    and foundation_width + (card_width + space_cards)
                    < event.pos[0]
                    < foundation_width + (card_width + space_cards) + card_width
                    and foundation_height
                    < event.pos[1]
                    < foundation_height + card_height
                ):
                    set_moving(
                        foundation_width + (card_width + space_cards),
                        foundation_height,
                        event,
                    )
                    drawn_card = foundation[1][-1]
                    drawn_card_location = "f"
                    drawn_card_position = 10 + len(foundation[1]) - 1

                elif (
                    foundation[2]
                    and foundation_width + (card_width + space_cards) * 2
                    < event.pos[0]
                    < foundation_width + (card_width + space_cards) * 2 + card_width
                    and foundation_height
                    < event.pos[1]
                    < foundation_height + card_height
                ):
                    set_moving(
                        foundation_width + (card_width + space_cards) * 2,
                        foundation_height,
                        event,
                    )
                    drawn_card = foundation[2][-1]
                    drawn_card_location = "f"
                    drawn_card_position = 20 + len(foundation[2]) - 1

                elif (
                    foundation[3]
                    and foundation_width + (card_width + space_cards) * 3
                    < event.pos[0]
                    < foundation_width + (card_width + space_cards) * 3 + card_width
                    and foundation_height
                    < event.pos[1]
                    < foundation_height + card_height
                ):
                    set_moving(
                        foundation_width + (card_width + space_cards) * 3,
                        foundation_height,
                        event,
                    )
                    drawn_card = foundation[3][-1]
                    drawn_card_location = "f"
                    drawn_card_position = 30 + len(foundation[3]) - 1

                # move card in foundation
                else:
                    counter_width_pos = (event.pos[0] - tableau_width) / (
                        card_width + space_cards
                    )
                    counter_height_pos = (event.pos[1] - tableau_height) / space_tableau
                    nr_tableau = math.floor(counter_width_pos)

                    if 0 <= nr_tableau <= 6:
                        if 0 <= counter_height_pos - len(tableau[nr_tableau]) + 1 <= 5:
                            set_moving(
                                tableau_width + (card_width + space_cards) * nr_tableau,
                                tableau_height
                                + space_tableau * (len(tableau[nr_tableau]) - 1),
                                event,
                            )
                            drawn_card = tableau[nr_tableau][-1]
                            drawn_card_location = "t"
                            drawn_card_position = (
                                10 * nr_tableau + len(tableau[nr_tableau]) - 1
                            )

                        elif (
                            0
                            <= math.floor(counter_height_pos)
                            < len(tableau[nr_tableau]) - 1
                            and tableau[nr_tableau][
                                math.floor(counter_height_pos)
                            ].face_up
                            == True
                        ):
                            set_moving(
                                tableau_width + (card_width + space_cards) * nr_tableau,
                                tableau_height
                                + space_tableau * math.floor(counter_height_pos),
                                event,
                            )
                            drawn_card = tableau[nr_tableau][
                                math.floor(counter_height_pos)
                            ]
                            drawn_card_location = "t"
                            drawn_card_position = 10 * nr_tableau + math.floor(
                                counter_height_pos
                            )

        elif event.type == pygame.MOUSEBUTTONUP:
            moving = False

            if drawn_card:
                middle_card_x = drawn_card_x + card_width / 2
                middle_card_y = drawn_card_y + card_height / 2

                # card placed in foundation
                if (
                    foundation_width
                    <= middle_card_x
                    <= foundation_width + (card_width + space_cards) * 4
                    and foundation_height
                    <= middle_card_y
                    <= foundation_height + card_height
                ):
                    middle_card_x = middle_card_x - foundation_width
                    nr_foundation = math.floor(
                        middle_card_x / (card_width + space_cards)
                    )

                    if place_card_foundation(drawn_card, nr_foundation) == True:
                        # cards in tableau need to be last in column to be placed in foundation
                        if drawn_card_location == "t":
                            if (
                                drawn_card_position % 10
                                == len(tableau[drawn_card_position // 10]) - 1
                            ):
                                foundation[nr_foundation].append(drawn_card)
                                (
                                    drawn_card_location,
                                    drawn_card_position,
                                ) = remove_card_start_location(
                                    screen, drawn_card_location, drawn_card_position
                                )

                        else:
                            foundation[nr_foundation].append(drawn_card)
                            (
                                drawn_card_location,
                                drawn_card_position,
                            ) = remove_card_start_location(
                                screen, drawn_card_location, drawn_card_position
                            )

                # card placed in tableau
                if (
                    tableau_width
                    <= middle_card_x
                    <= tableau_width + (card_width + space_cards) * 7
                    and tableau_height <= middle_card_y
                ):
                    middle_card_x = middle_card_x - tableau_width
                    middle_card_y = middle_card_y - tableau_height
                    nr_tableau = math.floor(middle_card_x / (card_width + space_cards))
                    position_column = math.floor(middle_card_y / space_tableau)
                    length_column = len(tableau[nr_tableau])

                    if length_column <= position_column <= length_column + 4:
                        if place_card_tableau(drawn_card, nr_tableau) == True:
                            if drawn_card_location == "t":
                                for index in range(
                                    drawn_card_position % 10,
                                    len(tableau[drawn_card_position // 10]),
                                ):
                                    tableau[nr_tableau].append(
                                        tableau[drawn_card_position // 10][index]
                                    )
                                (
                                    drawn_card_location,
                                    drawn_card_position,
                                ) = remove_card_start_location(
                                    screen, drawn_card_location, drawn_card_position
                                )
                            else:
                                tableau[nr_tableau].append(drawn_card)
                                (
                                    drawn_card_location,
                                    drawn_card_position,
                                ) = remove_card_start_location(
                                    screen, drawn_card_location, drawn_card_position
                                )

                # drawn_card will dissapear
                drawn_card = None

        elif event.type == pygame.MOUSEMOTION:
            if moving:
                drawn_card_x, drawn_card_y = move_card(offset_x, offset_y, event.pos)

    # Clear the screen only for dirty rect (the moving card)
    if dirty_rect:
        # coordiantes of dirty_rect
        x_topleft = dirty_rect.topleft[0]
        y_topleft = dirty_rect.topleft[1]
        x_bottomright = dirty_rect.bottomright[0]
        y_bottomright = dirty_rect.bottomright[1]

        screen.fill((20, 150, 50), dirty_rect)
        draw_dirty_portion(screen, x_topleft, y_topleft, x_bottomright, y_bottomright)
        dirty_rect = None

    # Draw the moving card if it exists
    if drawn_card:
        # Calculate the dirty rect for the drawn card
        dirty_rect = drawn_card.get_rect_at(drawn_card_x, drawn_card_y)
        drawn_card.draw(screen, drawn_card_x, drawn_card_y)

    # END GAME
    if end_game() == True:
        font2 = pygame.font.Font(None, 50)
        text_surface = font2.render("CONGRATULATIONS, YOU WON!", True, (255, 150, 0))
        screen.blit(text_surface, (220, 600))

    # RESET BUTTON
    draw_button(900, 120, "RESET")

    # RULES BUTTON
    draw_button(900, 170, "RULES")

    # RULES BUTTON
    draw_button(900, 220, "MODE")

    # FPS AND MS
    fps = int(clock.get_fps())
    ms_per_frame = clock.get_time()

    fps_text = font.render(f"FPS: {fps}", True, (0, 0, 0))
    ms_text = font.render(f"MS: {ms_per_frame}", True, (0, 0, 0))

    portion_rect = pygame.Rect(900, 0, 100, 100)
    pygame.draw.rect(screen, (20, 150, 50), portion_rect)
    screen.blit(fps_text, (900, 10))
    screen.blit(ms_text, (900, 50))

    pygame.display.update()
    clock.tick(60)
