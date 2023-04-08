from optparse import Option
import random
from re import T
import time
from typing import Dict, List, NamedTuple


#######################################################
# Class / constant definitions 
#######################################################

"""
Use 14 to represent aces so that when we do comparisons
aces will have the largest numeric value
"""
VALUES: List[int] = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
SUITS: List[str] = ["spade", "diamond", "heart", "club"]
POSITIONS: List[str] = ["UTG", "HJ", "CO", "BTN", "SB", "BB"]
ACTIONS: List[str] = ["Allin", "Call", "Fold", "Raise"]

class Card(NamedTuple):
    suit: str   
    value: int 

    def toString(self) -> str:
        output: str = ""
        if self.value == 14:
            output += "A"
        elif self.value == 13:
            output += "K"
        elif self.value == 12: 
            output += "Q"
        elif self.value == 11: 
            output += "J"
        elif self.value == 10:
            output += "T"
        else:
            output += self.value
        
        return output + " of " + self.suit


class Hand(NamedTuple):
    card1: Card
    card2: Card

class Player:
    def __init__(self, pos: str, isUser: bool, stackSize: int, hasFolded: bool) -> None:
        self.position = pos
        self.isUser = isUser
        self.stackSize = stackSize
        self.hasFolded = hasFolded
 
class Game:
    def __init__(self) -> None:
        self.players: List[Player] = Game.generatePlayers()
        self.deck: List[Card] = Game.generateDeck()
        self.hasAllined: bool = False
        self.moves: List[str] = []

    #########################
    # Class(static) methods # 
    #########################
    def generatePlayers() -> List[Player]:
        userPos: str = random.choice(POSITIONS)
        players: List[Player] = []

        for pos in POSITIONS:
            players.append(Player(pos, userPos == pos, 100, False))
        
        return players
    
    def generateDeck() -> List[Card]:
        # Generates a deck (52 cards)
        deck: List[Card] = []

        for suit in SUITS:
            for val in VALUES:
                deck.append(Card(
                    suit=suit,
                    value=val
                ))

        return deck

    ####################
    # Instance methods # 
    ####################
    def numPlayersLeft(self) -> int:
        activePlayerCount = 0

        for player in self.players:
            if not player.hasFolded:
                activePlayerCount += 1
        
        return activePlayerCount
      
    def recordMove(self, move: str) -> None: 
        # records a move
        if not move:
            self.moves.append('0')
        elif move == "raise":
            self.moves.append('r')
        elif move == 'call':
            self.moves.append('c')
        elif move == 'fold':
            self.moves.append('f')
        elif move == 'allin':
            self.moves.append('a')
        else:
            print("Wrong move provided")
    
    def getOptimalStrategy(self) -> str:
        # TODO: instead of random actions, return optimal strategy based on historical moves (game.moves)
        return random.choice(ACTIONS).lower().strip()
        


#######################################################
# Game starts here
#######################################################
def play():
    game: Game = Game()

    # Keep going around the table when there are >1 players that haven't folded
    while game.numPlayersLeft() > 1:
        playerIndex = len(game.moves) % len(game.players)
        currentPlayer = game.players[playerIndex]
        optimalStrategy = game.getOptimalStrategy()
        
        # If the current player has folded, record a "0" and skip to the next player
        # Note that we'll only encounter AI players that have folded here, as the game 
        # would have ended if the user folds.
        if currentPlayer.hasFolded:
            game.recordMove("")
        else:
            if currentPlayer.isUser:
                print("Your position is {} ...\n".format(currentPlayer.position))

                # Get a valid user input action. 
                # Will keep probing user for input if the given action is not valid.
                userAction = input("Please choose an action (Raise, Call, Fold, Allin)...\n")
                while userAction.strip().capitalize() not in ACTIONS:
                    userAction = input("You've chosen an incorrect action - please choose from these actions (Raise, Call, Fold, Allin) and try again: \n")
                print("Your chose to {} ... \n".format(userAction.lower()))

                game.recordMove(userAction.strip().lower())
                
                # Exit game if user folded or all-in'ed.
                # TODO: Tell user tell user whether or not they folded / allin'ed correctly according 
                # to returned optimalStrategy here.
                if userAction == 'fold':
                    print("You have folded. Game over! :) \n")
                    break
                elif userAction == 'allin':
                    print("Oooh hoo - you've all-in'ed. Game over! \n")
                    break
            else:
                print("{} is currently deciding... ".format(currentPlayer.position))

                # Give each AI player 1 second delay for making a move
                time.sleep(1)

                # Use random to simulate an AI user action here
                game.recordMove(optimalStrategy)
                print("Ok, {} decided to {}.\n".format(currentPlayer.position, optimalStrategy))

                # Add more active users to the round after action
                if optimalStrategy == "fold":
                    currentPlayer.hasFolded = True
            
        print("{}\n\n".format(game.moves))

play()