import random

# Define a Card class to represent individual playing cards
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value} of {self.suit}"

# Define a Deck class to represent a deck of cards
class Deck:
    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        # Create a deck by generating all possible cards and shuffling them
        self.cards = [Card(suit, value) for suit in suits for value in values]
        random.shuffle(self.cards)

    # Method to draw a card from the deck
    def draw(self):
        return self.cards.pop()

# Define a Hand class to represent a player's hand of cards
class Hand:
    def __init__(self):
        self.cards = []

    # Method to add a card to the hand
    def add_card(self, card):
        self.cards.append(card)

    # Method to compute the value of the hand in a game of blackjack
    def compute_value(self):
        value = 0
        aces = 0
        for card in self.cards:
            if card.value in ['Jack', 'Queen', 'King']:
                value += 10
            elif card.value == 'Ace':
                aces += 1
                value += 11
            else:
                value += int(card.value)

        while value > 21 and aces:
            value -= 10
            aces -= 1

        return value

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)

# Function to handle a player's turn in the game
def player_turn(deck, player_hand, player_name):
    while True:
        print(f"{player_name}'s cards:", player_hand)
        action = input(f"{player_name}, do you want to hit or stand? ").lower()
        if action == 'hit':
            player_hand.add_card(deck.draw())
            if player_hand.compute_value() > 21:
                print(f"{player_name} busts!")
                return False
        elif action == 'stand':
            break
    return True

# Function to get the bet amount from a player
def get_bet_amount(player_name, player_money):
    while True:
        try:
            bet = int(input(f"{player_name}, you have ${player_money}. How much would you like to bet? "))
            if 0 < bet <= player_money:
                return bet
            print(f"Please enter a valid amount between 1 and {player_money}.")
        except ValueError:
            print("Please enter a valid amount.")

# Main function to play the game of blackjack
def play_blackjack():
    player1_money = 100
    player2_money = 100

    while player1_money > 0 and player2_money > 0:
        deck = Deck()

        player1_hand = Hand()
        player2_hand = Hand()
        dealer_hand = Hand()

        # Deal initial cards to players and the dealer
        for _ in range(2):
            player1_hand.add_card(deck.draw())
            player2_hand.add_card(deck.draw())
            dealer_hand.add_card(deck.draw())

        player1_bet = get_bet_amount("Player 1", player1_money)
        player2_bet = get_bet_amount("Player 2", player2_money)

        # Allow players to take their turns
        player1_active = player_turn(deck, player1_hand, "Player 1")
        player2_active = player_turn(deck, player2_hand, "Player 2")

        # Dealer's turn
        print("Dealer's cards:", dealer_hand)
        while dealer_hand.compute_value() < 17:
            dealer_hand.add_card(deck.draw())
            print("Dealer draws a card. Dealer's cards:", dealer_hand)

        # Determine the outcomes and update player money
        player1_value = player1_hand.compute_value()
        player2_value = player2_hand.compute_value()
        dealer_value = dealer_hand.compute_value()

        if dealer_value > 21 or (player1_active and player1_value > dealer_value):
            print("Player 1 wins!")
            player1_money += player1_bet
        else:
            print("Player 1 loses!")
            player1_money -= player1_bet

        if dealer_value > 21 or (player2_active and player2_value > dealer_value):
            print("Player 2 wins!")
            player2_money += player2_bet
        else:
            print("Player 2 loses!")
            player2_money -= player2_bet

        print("Player 1's total money:", player1_money)
        print("Player 2's total money:", player2_money)

        play_again = input("Do you want to play another round? (yes/no): ").lower()
        if play_again != 'yes':
            break

if __name__ == "__main__":
    play_blackjack()