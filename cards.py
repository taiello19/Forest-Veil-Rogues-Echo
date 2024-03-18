import random

class Card:
    def __init__(self, card_type, value, mana_cost):
        self.type = card_type
        self.value = value
        self.mana_cost = mana_cost
        self.rect = None  # Placeholder for card position, adjust as needed

# Define a function to create your initial set of cards
def create_initial_deck():
    cards = [
        Card('Attack', 5, 1),
        Card('Attack', 5, 1),
        Card('Attack', 5, 1),
        Card('Attack', 5, 1),
        Card('Attack', 5, 1),
        Card('Attack', 5, 1),
        Card('Attack', 5, 1),
        Card('Attack', 5, 1),
        Card('Defend', 5, 1),
        Card('Defend', 5, 1),
        Card('Defend', 5, 1),
        Card('Defend', 5, 1),
        Card('Defend', 5, 1),
        Card('Defend', 5, 1),
    ]
    return cards

# Function to draw a hand from the deck
def draw_hand(deck, discard_pile, hand_size=4):
    hand = []
    for _ in range(hand_size):
        if not deck:
            deck.extend(discard_pile)
            discard_pile.clear()
            random.shuffle(deck)
        card = deck.pop()
        hand.append(card)
    return hand, deck, discard_pile