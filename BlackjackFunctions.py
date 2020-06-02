# INF360 - Programming in Python
# Chris Hogan
# Blackjack Functions

import time
import random
import re
import math
import logging 

logging.basicConfig(filename='GameLog.log',level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class DeckData(object):
    def __init__(self,deck):
        self.deck = deck


""" Print Functions """
#Adds 1 second to a print statement to make them easier to read
def sleepPrint(myString):
    print(myString)
    time.sleep(1)

#Prints the table rules at the beginning of the game
def rules():
    #Logs rules attempting to be displayed
    logging.debug('Attempting to display rules to players.')
    rulesList = [' Table Rules: ',' Players: 1-4 ',' Min Bet: 1 ',' Max Bet: 1000 ',' Blackjack pays 3 to 2 ',' Dealer must draw to 16 and stand on 17 ']
    print('*'*50)
    for row in rulesList:
        print(row.center(50))
    sleepPrint('*'*50)
    #Logs rules have been displayed
    logging.debug('Rules have been displayed to players.')

#Prints the cahips that have been given out
def printChips(tableChips):
    #Logs Attempting display chip count to players
    logging.debug('Attempting display chip counts to players.')
    #Finds the longest players name
    maxLen = 0
    for player in tableChips:
        if len(player) > maxLen:
            maxLen = len(player)
    #Prints the players name and chips
    header = 'Name'.ljust(maxLen) + '  ' + 'Chips'
    print(header)
    for playerName,playerChips in tableChips.items():
        if playerName == 'Dealer':
            pass
        else:
            #Adds Name to row
            row = playerName.rjust(maxLen) + ': '
            #Adds Chips to row
            row = row + str(playerChips)
            print(row)
    sleepPrint('')
    #Logs Chip counts displayed to players
    logging.debug('Chip counts displayed to players.')  

#Prints the cards that have been dealt
def printCards(tableCards,tableChips,final):
    #Logs Attempts to print cards on the table
    logging.debug('Attempting to print cards on the table.')
    #Finds the longest players name
    maxLen = 0
    for player in tableCards:
        if len(player) > maxLen:
            maxLen = len(player)
    #Prints the players name, bets, score, and cards
    header = 'Name'.ljust(maxLen) + '  ' + 'Bet'.ljust(5) + 'Score'.ljust(6) + 'Cards'
    print(header)
    for playerName,playerCards in tableCards.items():
        #Adds Name to row
        row = playerName.rjust(maxLen) + ': '
        #Adds Bet to row
        if playerName == 'Dealer':
            row = row + ' '*5
        else:
            row = row + str(tableChips[playerName]).ljust(5)
        #Adds Score to row
        if playerName == 'Dealer' and final == 0:
            row = row + str(playerCards[2]).ljust(6)
        else:
            row = row + str(playerCards[1]).ljust(6)
        #Adds Cards to row
        firstCard = 0
        for card in playerCards[0]:
            if playerName == 'Dealer' and final == 0 and firstCard == 0:
                row = row + '--  '
                firstCard = 1
            else:
                row = row + card.ljust(4)
        print(row)
    #Logs cards on table printed
    logging.debug('All cards on the table have been printed.')
    sleepPrint('')


""" Player Functions """
#Asks how many players are at the table
def numPlayers():
    #Logs attepting to add players
    logging.debug('Attempting to add players to game.')
    #Asks how many players are playing
    while True:
        sleepPrint('There can be between 1 and 4 players at this table.')
        try:
            playerNum = int(input('How many players do you have? '))
        #Check if an integer was given
        except ValueError:
            sleepPrint("That's not a valid number of players!")
        else:
            #Checks if number is between 1-4
            if int(playerNum) < 1 or int(playerNum) > 4:
                sleepPrint("That's not a valid number of players!")
            else:
                break
    sleepPrint('')
    #Logs Number of players at table succefully determined
    logging.debug('Number of players at table succefully determined.')
    return playerNum 

#Asks each player for their name
def addPlayers(playerNum):
    #Logs attepting to add player names
    logging.debug('Attempting to add players names to game.')
    players = ['Dealer']
    for num in range(1,int(playerNum) + 1):
        unique = 0
        while unique == 0:
            unique = 1
            playerName = input('What is your name player ' + str(num) +'? ')
            #Verifies that the name is unique
            for name in players:
                if playerName.lower() == name.lower():
                    unique = 0
                    sleepPrint('Someone already has that name! Please choose a different name.')
            #Checks if players name is to long or short
            if len(playerName) > 15:
                unique = 0
                sleepPrint('That name is to long! Please choose a different name.')
            elif len(playerName) < 1:
                unique = 0
                sleepPrint('That name is to short! Please choose a different name.')
            #Adds name to players list
            if unique == 1:
                players.insert(len(players) - 1, playerName)
                #Logs players NAME added to game
                logging.debug(playerName + ' has been added to the game.')
    sleepPrint('')
    #Logs players successfully added to game
    logging.debug('All players successfully added to game')
    return players


""" Card Functions """
#Creates multiple decks and shuffles them together
def shuffleDeck(numOfDecks):
    #Logs deck Shuffling
    logging.debug('Deck is being shuffled.')
    #Defines suits and numbers to create deck
    deck = []
    suits = {'Clubs':'♣', 'Diamonds':'♦', 'Hearts':'♥', 'Spades':'♠'}
    numbers = {'Ace':'A', 'Two':'2', 'Three':'3', 'Four':'4', 'Five':'5',
            'Six':'6', 'Seven':'7','Eight':'8', 'Nine':'9', 'Ten':'10',
            'Jack':'J', 'Queen':'Q', 'King':'K'}
    #Creates the number of desired decks
    for num in range(0,int(numOfDecks)):
        for suit in suits:
            for number in numbers:
                deck.append(suits[suit] + numbers[number])
    #Shuffles all decks together
    random.shuffle(deck)
    #Logs when deck is shuffled
    DeckData.deck = deck
    logging.debug('Deck has been shuffled.')

#Deal cards to all players and dealer
def dealCards(tablePlayers):
    #Logs attempting to deal cards to players
    logging.debug('Attempting to deal cards to players.')
    cardsDealt = {}
    firstCard = 0
    #Deals cards to all of the players and dealer one at a time
    for player in tablePlayers:
        cards = [DeckData.deck[firstCard], DeckData.deck[len(tablePlayers) + firstCard]]
        cardsDealt[player] = cards
        firstCard += 1
        #Logs player dealt cards
        logging.debug(player + ' has been dealt cards.')
    #Removes dealt cards from deck
    DeckData.deck = DeckData.deck[firstCard * 2:]
    #Logs all players dealt cards
    logging.debug('All players have been dealt cards.')
    return cardsDealt

#Scores players cards on the table
def scoreCards(tableCards):
    #Logs attempting to record players score
    logging.debug('Attempting to record score.')
    tableScore = {}
    for player in tableCards:
        #Defines score card variables
        playerScore = 0
        playerScore2 = 0
        dealerHide = 0
        firstCard = 0
        for cards in tableCards[player]:
            #Checks if card is a face card
            if re.search('[B-Zb-z]', cards):
                playerScore += 10
            #Checls if card has a number
            elif re.search('[0-9]', cards):
                playerScore += int(cards[1:])
            #Checks if card is an ace
            elif re.search('[Aa]', cards):
                playerScore += 11
                playerScore2 += 1
            if firstCard == 0:
                dealerHide = playerScore
            firstCard = 1
        #Adds two scores to hands with aces if needed
        if playerScore2 >= 1 and playerScore != 21:
            first = playerScore - 10 * playerScore2
            newScore = playerScore - 10 * (playerScore2 - 1)
            playerScore = str(first) + '/' + str(newScore)
            if newScore > 21:
                playerScore = first
        #Adds Dealers hidden score
        if player == 'Dealer':
            if '/' in str(playerScore):
                playerScore = playerScore.split('/')
                playerScore = int(playerScore[1])
            tableScore[player] = [tableCards[player],playerScore,playerScore - dealerHide]
            if 'A' in tableScore[player][0][1]:
                tableScore[player][2] = '1/11'
        #Adds players cards and score to the table score
        else:
            tableScore[player] = [tableCards[player],playerScore]
    #Logs scores have been updated
    logging.debug('Scores have been updated.')
    return tableScore


""" Chip Functions """
#Gives players there starting chips
def firstChips(tablePlayers):
    #Logs Attempting to give players there starting chips
    logging.debug('Attempting to give players there starting chips.')
    tableChips = {}
    #Gives every player 1000 chips to start the game
    for player in tablePlayers:
        if player.lower() != 'dealer':
            tableChips[player] = 1000
            #Logs players starting chip count
            logging.debug(player + ' has been given 1000 chips to start the game.')
    #Logs all players given chips
    logging.debug('All players have been given there starting chips.')
    #Prints players starting chips
    printChips(tableChips)
    return tableChips

#Players place there bet on each hand
def betChips(tablePlayers,tableChips):
    #Logs attempting to get bet size from each player
    logging.debug('Attempting to get bet size from each player.')
    betChips = {}
    for player in tablePlayers:
        if player.lower() != 'dealer':
            #Displays players current chips
            sleepPrint(player + ' you have ' + str(tableChips[player]) + ' chips.')
            while True:
                #Asks players for bets
                try:
                    bet = int(input('How much would you like to bet? '))
                #Check is an integer was given
                except ValueError:
                    sleepPrint("That's not a valid number!")
                else:
                    #Check if player has enough chips
                    if int(bet) > tableChips[player]:
                        sleepPrint(player + ', you do not have that many chips!')
                    #Makes sure bet is greater than 1
                    elif int(bet) < 1:
                        sleepPrint(player + ', bets can not be less than 1!')
                    #Makes sure bet is less than 1000
                    elif int(bet) > 1000:
                        sleepPrint(player + ', bets can not be greater than 1000!')
                    else:
                        break
            betChips[player] = bet
            #Logs players bet was accepted
            logging.debug(player + "'s bet of " + str(bet) + " was accepted.")
    sleepPrint('')
    #Logs all players bets accepted
    logging.debug('All players bets were accepted.')
    return betChips

#Adjusts chips that each player has to bet
def chipChange(tableCards,tableBets,tableChips,status):
    #Logs attempting to change players chip counts
    logging.debug('Attempting to change chip counts.')
    for player in tableCards:
        if player in status:
            tableChips[player] = int(tableChips[player]) - int(tableBets[player])
        elif player != 'Dealer':
            #Checks players score for aces
            tableCards[player][1] = aceCheck(str(tableCards[player][1]))
            #Checks if player busted
            if int(tableCards[player][1]) > 21:
                tableChips[player] = int(tableChips[player]) - int(tableBets[player])
            #Checks if players Chips are the same as the dealers
            elif int(tableCards[player][1]) == int(tableCards['Dealer'][1]):
                pass
            #Checks if player had a blackjack
            elif int(tableCards[player][1]) == 21:
                if len(tableCards[player][0]) == 2:
                    tableChips[player] = int(tableChips[player]) + round(int(tableBets[player])*1.5)
                else:
                    tableChips[player] = int(tableChips[player]) + int(tableBets[player])
            #Checks if dealer is below 21
            elif int(tableCards['Dealer'][1]) <= 21:
                if int(tableCards[player][1]) < int(tableCards['Dealer'][1]):
                    tableChips[player] = int(tableChips[player]) - int(tableBets[player])
                elif int(tableCards[player][1]) > int(tableCards['Dealer'][1]) and int(tableCards[player][1]) < 21:
                    tableChips[player] = int(tableChips[player]) + int(tableBets[player])
            #Checks if dealer is above 21
            elif int(tableCards['Dealer'][1]) > 21:
                if int(tableCards[player][1]) < 21:
                    tableChips[player] = int(tableChips[player]) + int(tableBets[player])
    #Prints players updated chip count
    #Logs chip counts changed
    logging.debug('All players chip counts have been changed.')
    printChips(tableChips)
    return tableChips

#Checks if players have chips left
def chipCheck(tableChips,tablePlayers):
    #Logs Checking if player has chips for next turn
    logging.debug('Checking if players have enough chips for next turn.')
    global chips
    global players
    #Creates variable for starting chips
    startingChips = tableChips.copy()
    for playerChips in startingChips:
        #Checks if players chips equal 0
        if int(tableChips[playerChips]) == 0:
            sleepPrint(playerChips + ', you have lost all of your chips! Better luck next time.\n')
            #Logs player has lost all there chips
            logging.debug(playerChips + ' has lost all there chips.')
            #Removes Player from players list and chips dictionaries
            del tableChips[playerChips]
            chips = tableChips
            tablePlayers.remove(playerChips)
            players = tablePlayers
        else:
            #Logs players who still have chips
            logging.debug(playerChips + ' still has chips.')


""" Turn Functions """
#Checks for Ace and pulls highest score
def aceCheck(playerCards):
    scoreTest = 0
    if '/' in playerCards:
        scoreTest = playerCards.split('/')
        scoreTest = int(scoreTest[1])
    else:
        scoreTest = int(playerCards)
    return scoreTest

#Adds a card to players hand and updates score
def hit(playerCards, playerTurn):
    hitCards = {}
    #Adds card to hand and removes card from deck
    for playerKey, playerValue in playerCards.items():
        if playerKey == playerTurn:
            playerValue[0].append(DeckData.deck[0])
            DeckData.deck = DeckData.deck[1:]
            hitCards[playerKey] = playerValue[0]
    #Adds new card to score and returns new score
    return scoreCards(hitCards)

#Takes player input to complete turn
def turn(tableCards,tableBets,tableChips):
    #Logs running player turns
    logging.debug('Attempting to run players turns.')
    #Checks if the Dealer has Blackjack
    surrenderList = []
    if int(tableCards['Dealer'][1]) == 21:
        sleepPrint('The Dealer has 21!\n')
    else:
        for player,cards in tableCards.items():
            #Runs dealers turn
            if player == 'Dealer':
                sleepPrint('It is the Dealers turn.\n')
                printCards(tableCards,tableBets,1)
                while tableCards[player][1] < 17:
                    tableCards[player] = hit(tableCards,player).get(player)
                    printCards(tableCards,tableBets,1)
            #Runs players turn
            elif player != 'Dealer':
                #Checks if player has a Blackjack
                if cards[1] == 21:
                    sleepPrint(player + ' it is your turn. You have a blackjack!\n')
                #Checks for an Ace
                scoreTest = aceCheck(str(tableCards[player][1]))
                #Sets player number variable for first turn
                playerNum = 0
                while scoreTest < 21:
                    #Asks the player what they would like to do
                    sleepPrint(player + ' it is your turn. You have ' + str(tableCards[player][1]) + '.')
                    if playerNum == 0:
                        playerTurn = input('What do you want to do? (Hit, Stand, Double, Surrender) ')
                    elif playerNum != 0:
                        playerTurn = input('What do you want to do? (Hit, Stand) ')
                        
                    #Executes stand command
                    if playerTurn.lower() == 'stand':
                        print('')
                        printCards(tableCards,tableBets,0)
                        break
                    #Executes hit function
                    elif playerTurn.lower() == 'hit':
                        print('')
                        tableCards[player] = hit(tableCards,player).get(player)
                        printCards(tableCards,tableBets,0)
                    #Doubles players bet size and runs hit function
                    elif playerTurn.lower() == 'double' and playerNum == 0:
                        #Checks if they have enough chips to double
                        if int(tableChips[player]) >= int(tableBets.get(player))*2:
                            tableBets[player] = int(tableBets.get(player))*2
                            tableCards[player] = hit(tableCards,player).get(player)
                            print('')
                            printCards(tableCards,tableBets,0)
                            break
                        #Runs if there is not enough chips to double down
                        else:
                            sleepPrint('You do not have enough chips to double down!')
                            playerNum -= 1
                    #Executes surrender command
                    elif playerTurn.lower() == 'surrender' and playerNum == 0:
                        surrenderList.append(player)
                        tableBets[player] = math.ceil(int(tableBets[player]) / 2)
                        tableCards[player][1] = 'SUR'
                        print('')
                        printCards(tableCards,tableBets,0)
                        break
                    #Runs if a valid command was not given
                    else:
                        sleepPrint('That is not a valid command')
                        playerNum -= 1

                    #Adds number to run for players next turn
                    playerNum += 1
                    #Updates Score for loop
                    scoreTest = aceCheck(str(tableCards[player][1]))
                    #Prints status of your cards
                    if int(scoreTest) == 21:
                        sleepPrint(player + ' you have ' + str(tableCards[player][1]) + '.\n')
                    elif int(scoreTest) > 21:
                        sleepPrint(player + ' you busted with ' + str(tableCards[player][1]) + '.\n')
            #Logs player has compled turn
            logging.debug(player + ' has completed there turn')
    #Logs all players completed turns
    logging.debug('All players have completed turns.')
    return surrenderList
