import random

#Create a class for a Card
class Card:
	def __init__(self, value, suit):
		self.value = value
		self.suit = suit


#Create a class for a Deck
class Deck:
	values = [str(i) for i in range(2, 11)] + ["J", "Q", "K", "A"]
	suits = ["C", "D", "H", "S"]

	def __init__(self):
		self.deck = [Card(value, suit) for value in self.values for suit in self.suits]

	def __len__(self):
		return len(self.deck)

	def __getitem__(self, position):
		return self.deck[position]

	def shuffleDeck(self):
		random.shuffle(self.deck)

	def printDeck(self):
		for card in self:
			print(card.value + card.suit)

#Create a class for a Player
class Player:
	def __init__(self, name):
		self.name = name
		self.hand = []
		self.score = 0

	def printHand(self):
		for card in self.hand:
			print(card.value + card.suit)


def setupPlayers():
	name = input('Hi Player, Welcome to Hearts!\nPlease enter your name: ')
	print("\n\n")

	Player1 = Player(name)
	Player2 = Player('Computer1')
	Player3 = Player('Computer2')
	Player4 = Player('Computer3')

	return [Player1, Player2, Player3, Player4]


def dealDeck(players):
	deck = Deck()
	deck.shuffleDeck()
	for number, player in enumerate(players):
		for card in deck[13*number:13*(number+1)]:
			player.hand.append(card)


def printScores(players):
	for player in players:
		print(player.name + "\n" + str(player.score))


def findTwoClubs(players):
	for number, player in enumerate(players):
		for card in player.hand:
			if card.value == '2' and card.suit == 'C':
				return number


def playCard(player, hearts_broken, suit=None):
	#Check for 2 of clubs first
	for card in player.hand:
		if card.value == '2' and card.suit == 'C':
			player.hand.remove(card)
			return card

	#Case in which actual player must play
	if player.name != 'Computer1' and player.name != 'Computer2' and player.name != 'Computer3':
		print("\n\nYour Hand:")
		player.printHand()
		print("\n")

		#check if there is a card that can follow suit
		follow_suit = False
		if suit is not None:
			for card in player.hand:
				if card.suit == suit:
					follow_suit = True

		#keep asking for input until card entered exists, card follows suit, or hearts is allowed to be played
		matched = False
		while not matched:	
			card = input("Please select a card from your hand you would like to play\n")
			print("\n")
			if card[0] == '1' and card[1] == '0':
				card_value = '10'
			else:
				card_value = card[0]
			card_suit = card[-1]
			
			for p_card in player.hand:
				if p_card.value == card_value and p_card.suit==card_suit:
					matched = True
					if suit is not None and follow_suit:
						if card_suit != suit:
							print("Please select a card that matches the suit that was led")
							matched = False
					if not hearts_broken:
						if card_suit == "H":
							if not hearts_broken and suit is not None and not follow_suit:
								break
							print("You cannot play a Hearts at this point")
							matched = False

			
		play_card = Card(card_value,card_suit)
		
		for card in player.hand:
			if card.value == play_card.value and card.suit==play_card.suit:
				player.hand.remove(card)
		return play_card


	#case for computers to play acceptable cards
	playable_cards = []
	if suit is None:
		if hearts_broken:
			playable_cards = player.hand
		else:
			for card in player.hand:
				if card.suit != 'H':
					playable_cards.append(card)
	else:
		for card in player.hand:
			if card.suit == suit:
				playable_cards.append(card)
		#can break hearts in this case
		if not playable_cards:
			playable_cards = player.hand

	play_card = random.choice(playable_cards)
	player.hand.remove(play_card)
	return play_card




	
def main():
	magnitude = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

	players = setupPlayers()

	#play 10 rounds total
	for round in range(1, 3):

		print("ROUND " + str(round) + ":")

		dealDeck(players)

		to_go_first = findTwoClubs(players)
		hearts_broken = False

		#13 tricks per round
		for i in range(13):
			suit = None
			played_cards = []

			#loop through each player
			for turn in range(4):
				card = playCard(players[(to_go_first + turn) % 4], hearts_broken, suit)
				if turn == 0:
					suit = card.suit
				played_cards.append(card)
				print(players[(to_go_first + turn) % 4].name + " " + card.value + card.suit)

			num_hearts = 0
			queen_spades = 0

			#determines who wins each trick
			largest = 0
			winner = None
			for idx, card in enumerate(played_cards):
				if card.suit == suit:
					if magnitude[card.value] > largest:
						largest = magnitude[card.value]
						winner = (to_go_first + idx) % 4
				if card.suit == 'H':
					num_hearts += 1
					hearts_broken = True
				if card.value == 'Q' and card.suit == 'S':
					queen_spades = 1

			#determine number of points winner of trick gets, and will go first
			players[winner].score += num_hearts + queen_spades * 13
			to_go_first = winner

			print("\n\n\n\n")
			printScores(players)
			print("\n\n\n\n")

		print("Round " + str(round) + " Scores:\n")
		printScores(players)
		print("\n\n\n\n")

	your_score = players[0].score
	place = 1
	for player in players[1:]:
		if your_score > player.score:
			place += 1

	print("Congrats for playing Hearts!")
	print("Your Place: " + str(place))



if __name__ == "__main__":
	main()









