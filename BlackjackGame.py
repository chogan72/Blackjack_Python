# INF360 - Programming in Python
# Chris Hogan
# Blackjack Game

"""
This is a fully functioning multiplayer blackjack game. The game starts off by
shuffling 6 decks together. The game then starts the process of adding players 
by asking how many players are at the table, and prompts each player to enter
their name. From there, each player is given 1000 chips to start the game.
Then the first round will start with each player being prompted to place
their bets for the hand. Once all the bets are placed each player and dealer
are dealt their cards. From there each player is prompted when it is there turn.
Next,  they can either hit, stand, surrender, or double down depending on their 
hand. From there the players chips are adjusted based on the outcome of the 
hand. At this point players that have 0 chips left are removed from the table.
If the deck of cards has less than 52 cards left it is reshuffled. The round
then starts over and goes until all the players are out of chips. Once all of
the players are removed from the table the game is over.

Table Rules:
Players: 1-4
Min Bet: 1
Max Bet: 1000
Blackjack pays 3 to 2
Dealer must draw to 16 and stand on 17
"""

import sys
import logging

logging.basicConfig(filename='GameLog.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#Import BlackjackFunctions module
try:
    import BlackjackFunctions
    logging.debug('BlackjackFunctions module loaded successfully.')
except:
    logging.critical('Missing BlackjackFunctions module. Check for installation.')
    logging.critical('Program will now close...')
    sys.exit


#Runs the game
def game():
    #Prints the table Rules
    BlackjackFunctions.rules()
    #Adds Players to the table
    playerNum = BlackjackFunctions.numPlayers()
    players = BlackjackFunctions.addPlayers(playerNum)
    #Gives each player there starting chips
    chips = BlackjackFunctions.firstChips(players)
    #Creates the full deck from 6 decks of cards
    BlackjackFunctions.shuffleDeck(6)
    while len(chips) > 0:
        #Each player places there bets
        bets = BlackjackFunctions.betChips(players,chips)
        #Deals starting cards and scores them
        dealtCards = BlackjackFunctions.dealCards(players)
        currentCards = BlackjackFunctions.scoreCards(dealtCards)
        #Prints the cards that were delt
        BlackjackFunctions.printCards(currentCards,bets,0)
        #Runs Turn Function suffling though each players turn
        cardStatus = BlackjackFunctions.turn(currentCards,bets,chips)
        #Changes players chip count
        chips = BlackjackFunctions.chipChange(currentCards,bets,chips,cardStatus)
        #Checks if players still has chips
        BlackjackFunctions.chipCheck(chips,players)
        #Checks if there are still players with chips
        if len(chips) == 0:
            print('All of the players have run out of chips. Better luck next time.')
            #Logs all players have ran out of chips
            logging.debug('All players have run out of chips.')
            break
        #Shuffles decks when there is less than 1 left
        if len(BlackjackFunctions.DeckData.deck) < 52:
            BlackjackFunctions.shuffleDeck(6)
            BlackjackFunctions.sleepPrint('The Deck has been shuffled.')


#Runs Main Game Funtion
game()
