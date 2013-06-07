# Mini-project #6 - Blackjack
# It works with codesculptor http://www.codeskulptor.org/

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = True
outcome = ""
score = 1

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

class Card:
    def __init__(self, suit, rank, reveal = True):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
            self.reveal = reveal
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank
    
    def draw(self, canvas, pos):
        if self.reveal == True:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        else:
                canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                              [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
     
class Hand:
    def __init__(self):
        self.cards_in_hand = []

    def __str__(self):
        total = "Hand contains"
        for item in self.cards_in_hand:
            total += " " + item.suit + item.rank
        return total    # return a string representation of a hand

    def add_card(self, card):
        self.cards_in_hand.append(card)    # add a card object to a hand
            
    def get_value(self):
        self.value = 0   # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        is_aces = False
        for item in self.cards_in_hand:	# compute the value of the hand, see Blackjack video
            self.value += VALUES[item.get_rank()]
            if item.get_rank() == 'A':
                is_aces = True        
        if is_aces and self.value <= 11:
            self.value += 10
        return self.value
    
    def draw(self, canvas, pos):
        for item in self.cards_in_hand:
            item.draw(canvas, pos)
            pos[0] += 80
           
   
class Deck:
    def __init__(self):
        self.cards_in_deck = []	# create a Deck object
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit,rank)
                self.cards_in_deck.append(Card(suit, rank))
    def shuffle(self):
        random.shuffle(self.cards_in_deck)	# use random.shuffle() to shuffle the deck

    def deal_card(self):
        dealed_card = self.cards_in_deck[-1]
        self.cards_in_deck.remove(dealed_card)
        return dealed_card 
    
    def __str__(self):
        total = "Deck contains"  # return a string representing the deck
        for item in self.cards_in_deck:
            total += " " + item.suit + item.rank
        return total    
 
#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, bj_deck, dealer_value, score
    player_hand = Hand()
    dealer_hand = Hand()
    bj_deck = Deck()
    bj_deck.shuffle()
    outcome = "Hit or stand?"
    dealer_value = "?"
    for i in range(2):
        player_hand.add_card(bj_deck.deal_card())
        dealer_hand.add_card(bj_deck.deal_card())
        dealer_hand.cards_in_hand[0].reveal = False
    if in_play:
        score -= 1
    in_play = True

def hit():
    global in_play
    if in_play:
        if player_hand.get_value() < 21:
            player_hand.add_card(bj_deck.deal_card())
            if player_hand.get_value() > 21:
                lose()
           
def stand():
    global in_play, dealer_value 
    if not in_play:
        lose()
    else:
        dealer_hand.cards_in_hand[0].reveal = True
        dealer_value = dealer_hand.get_value()
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(bj_deck.deal_card())
            dealer_value = dealer_hand.get_value()
        if dealer_hand.get_value() > 21:
            win() 
        elif player_hand.get_value() > dealer_hand.get_value():
            win()
        else:
            lose()
    
def win():
    global score, outcome, in_play
    if in_play:
        score += 1
        outcome = "You win! New deal?"
        in_play = False
    
def lose():
    global score, outcome, in_play
    if in_play:
        score -= 1
        outcome = "You lost! New deal?"            
        in_play = False
        
deal()
# draw handler    
def draw(canvas):
    
    canvas.draw_text("BlackJack", (180, 60), 50, "Black")
    dealer_hand.draw(canvas, [100, 100])
    player_hand.draw(canvas, [100, 400])
    canvas.draw_text(str(player_hand.get_value()), (30, 460), 30, "White")
    canvas.draw_text(str(dealer_value), (30, 160), 30, "White")
    canvas.draw_text(outcome, (110, 370), 25, "White")
    canvas.draw_text("Scores: " + str(score), (450, 60), 25, "White")
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
frame.start()
