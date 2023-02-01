#BlackJack3.0
#current blackjack project

import random
import itertools
import time

def slow_print(delay, end, *args):
    new_str = ""
    for arg in args:
        string = str(arg)
        for i in range(len(string)):
            new_str += string[i]
    for i in range(len(new_str)):
        print(new_str[i], end="")
        time.sleep(delay)
    if end == "\n":
        print("")

class Deck:
    suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    def __init__(self):
        self.cards = []

    def __len__(self):
        return len(self.cards)

    def fill(self):
        random.seed()
        for i in range(6):
            for suits, values in itertools.product(self.suits, self.values):
                self.cards.append(Card(values, suits))

    def shuffle(self):
        for i in range(random.randrange(15)):
            random.seed()
            random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

    def clear(self):
        for x in range(len(self.cards)):
            self.cards.pop(x)

class Card:

    def __init__(self, value, suit):
        self.suit = suit
        self.value = value

    def print_name(self):
        return f"{self.value} of {self.suit}"

    @property
    def cardscore(self):
        if self.value in ["Jack", "Queen", "King"]:
            return 10
        elif self.value in["Ace"]:
            return 1
        elif self.value in ["2", "3", "4", "5", "6", "7", "8", "9", "10"]:
             return int(self.value)

class Player:
    def __init__(self):
        self.hand = []

    def draw_card(self, card):
        self.hand.append(card)

    def clear_hand(self):
        self.hand = []

    def handscore(self):
        return sum([card.cardscore for card in self.hand])

    def ace_hand_score(self):
        ace_count = 0
        for x in range(len(self.hand)):
            if self.hand[x].value == "Ace":
                ace_count += 1
         
        ace_handscore = self.handscore()
        for ace in range(ace_count):
            if self.handscore() < 12 and ace_handscore < 12:
                ace_handscore += 10
        return ace_handscore

    @property
    def isBust(self):
        if self.ace_hand_score() > 21:
            return True
        else: return False

    def print_cards(self):
        for x in range(len(self.hand)):
            if x == len(self.hand)-2:
                slow_print(0.05, "", f"{self.hand[x].print_name()} and ")
            else:
                slow_print(0.05, "", f"{self.hand[x].print_name()}, ")
   

class Human(Player):

    min_bet = 20

    def __init__(self, chips):
        super().__init__()
        self.chips = chips

    def print_score(self):
        slow_print(0.05, "", "You have: ")
        self.print_cards()
        slow_print(0.05, "\n", f"for a score of {self.ace_hand_score()}.")

    def is_broke(self):
        if self.chips < 20:
            slow_print(0.05, "\n", "You are broke and don't have enough chips to play, come again next time. Closing game...")
            time.sleep(5)
            return exit()
        else: return False

    def place_bet(self):
        if not self.is_broke():
            try:
                slow_print(0.03, "\n", "How many chips would you like to bet? Minimum bet of 20 will be applied by default.")
                bet = int(input())
                if bet > self.chips:
                    slow_print(0.05, "\n", f"You only have {self.chips} chips, enter a lower amount")
                    return self.place_bet()
                elif bet == self.chips:
                    slow_print(0.05, "\n", f"Going all in! Betting {self.chips} chips")
                    self.chips = 0
                    return bet
                else:
                    if bet < 20:
                        self.is_broke()
                        bet = 20
                        slow_print(0.04, "\n", "Your bet amount was below the minimum of 20. Bet amount was set to 20.")
                    self.chips -= bet
                    slow_print(0.05, "\n", f"Betting {bet} chips. You have {self.chips} chips left.")
                    return bet
            except ValueError:
                slow_print(0.05, "\n", "That was not a valid entry, please try again")
                return self.place_bet()

    def hit(self):
        slow_print(0.03, "\n", "Enter 'h' to hit, or any other key to stand")
        if input() == "h":
            return True
        else: 
            slow_print(0.03, "\n", "Standing")
            return False

    def print_balance(self):
        return slow_print(0.05, "\n", f"You currently have {self.chips} chips.")


class Dealer(Player):
    def __init__(self):
        super().__init__()


    def show_hand(self, all):
        if all == True:
            slow_print(0.05, "", "Dealer has: ")
            self.print_cards()
            slow_print(0.05, "\n", f"total points are {self.ace_hand_score()}.")
        else: slow_print(0.05, "", f"Dealer has: {self.hand[0].print_name()}, at least {self.hand[0].cardscore} points. ")

   
class Game:
    def __init__(self):
        slow_print(0.03, "\n", "\n\n--------------Welcome to BlackJack--------------\n\n\n"
        "Press enter after typing your response to the dealer. \nBe sure to read each prompt carefully. \nThe game is case sensitive, so don't use uppercase characters.\n\n"
        "You start with 100 chips.")
        self.player = Human(100)
        self.dealer = Dealer()
        self.deck = Deck()
        self.bet_amt = 0
        self.deck.fill()
        self.deck.shuffle()

    def winner(self):
        if self.player.ace_hand_score() > self.dealer.ace_hand_score():
            return "Player"
        elif self.player.ace_hand_score() < self.dealer.ace_hand_score():
            return "Dealer"
        else: return "Pass"

    def reset_deck(self):
        slow_print(0.05, "\n", "Not enough cards left in the shoe, reshuffling 6 decks...")
        self.deck.clear()
        self.deck.fill()
        self.deck.shuffle()
        time.sleep(5)

    def init_round(self):
        self.deck.shuffle()
        self.player.is_broke()
        self.dealer.clear_hand()
        self.player.clear_hand()
        for i in range(2):  #deal two cards to both dealer and player
            self.deck.deal() # burn one card every time a card has been dealt to all players
            self.player.draw_card(self.deck.deal())
            self.dealer.draw_card(self.deck.deal())
        self.playing_round()

    def playing_round(self):
        if len(self.deck.cards) < 104:
            self.reset_deck()
        self.bet_amt = self.player.place_bet()
        self.dealer.show_hand(False)
        self.player.print_score()

        while self.player.hit() == True:
            self.player.draw_card(self.deck.deal())
            if self.player.isBust == True:
                slow_print(0.05, "\n", "You went over 21!")
                self.player.print_score()
                return self.player_loss()
            self.player.print_score()

        while self.dealer.ace_hand_score() < 17:
            self.dealer.draw_card(self.deck.deal())
            slow_print(0.1, "\n", "Dealer draws...")
            self.dealer.show_hand(True)
            if self.dealer.isBust == True:
                slow_print(0.05, "\n", "Dealer Busts!")
                return self.player_wins()

        if self.winner() == "Player":
            self.player_wins()
            time.sleep(3)

        elif self.winner() == "Pass":
            self.player_pass()
            time.sleep(3)


        elif self.winner() == "Dealer":
            self.player_loss()
            time.sleep(3)
       

    def end_screen(self):
        self.player.is_broke()
        slow_print(0.03, "\n", "Press 'e' to exit the game, or any key to play again\n\n")
        if input() == "e":
            exit()
        else:
            for i in range(15):
                print("\n") 
            self.init_round()

    def player_wins(self):
        slow_print(0.03, "\n", f"You win this round! You had a score of {self.player.ace_hand_score()}, beating the Dealer's score of {self.dealer.ace_hand_score()}. You gained {self.bet_amt} chips.")
        self.player.chips += 2*self.bet_amt
        self.player.print_balance()
        self.end_screen()

    def player_pass(self):
        self.dealer.show_hand(True)
        slow_print(0.03, "\n", f"You had the same score as the dealer: {self.player.ace_hand_score()}. No chips lost")
        self.player.chips += self.bet_amt
        self.player.print_balance()
        self.end_screen()
   
    def player_loss(self):
        if not self.player.isBust:
            slow_print(0.04, "\n", f"You lost this round. You had a score of {self.player.ace_hand_score()}, worse than the Dealer's score of {self.dealer.ace_hand_score()}. You lost {self.bet_amt} chips.")
        self.bet_amt = 0
        self.player.print_balance()
        self.end_screen()
       
def main():
    game = Game()
    game.init_round()

main()
