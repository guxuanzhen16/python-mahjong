import random, copy

class Tile(object):
	RANKS = (1, 2, 3, 4, 5, 6, 7, 8, 9)
	SUITS = ('B')

	def __init__(self, rank, suit):
		self.rank = rank
		self.suit= suit

	def __str__(self):
		return str(self.rank)
	
	def __eq__ (self, other):
		return (self.rank == other.rank)

	def __ne__ (self, other):
		return (self.rank != other.rank)

	def __lt__ (self, other):
		return (self.rank < other.rank)

	def __le__ (self, other):
		return (self.rank <= other.rank)

	def __gt__ (self, other):
		return (self.rank > other.rank)

	def __ge__ (self, other):
		return (self.rank >= other.rank)

	def is_Same_Suit(self, other):
		return (same.suit == other.suit)

	# checks if a given tile is higher than this tile by one
	# used in run checks
	def is_Higher_Tile(self, other):
		if self.rank == 9:
			return False
		elif self.rank + 1 == other.rank:
			return True
		else:
			return False


class Wall (object):
	def __init__(self):
		self.wall = []
		for i in range(4):
			for suit in Tile.SUITS:
				for rank in Tile.RANKS:
					tile = Tile(rank, suit)
					self.wall.append(tile)

	def shuffle(self):
		random.shuffle(self.wall)

	def deal(self):
		if len(self.wall) == 0:
			return None
		else:
			return self.wall.pop(0)

class Game (object):
	def __init__ (self, numHands):
		self.wall = Wall()
		self.wall.shuffle()
		self.hands = []
		numTiles_in_Hand = 8

		# create and sort hands
		for i in range(numHands):
			hand = []
			for j in range(numTiles_in_Hand):
				hand.append(self.wall.deal())
			sortedHand = sorted(hand, key=lambda tile: tile.rank)
			self.hands.append(sortedHand)

	# funny recursion moment theres probably a better way to do this
	@staticmethod
	def remove_Pairs(sus_hand, current_index):
		if current_index == len(sus_hand) - 1:
			# if no pairs were found at all then no winning hand
			return False
		# for each pair found, create a new hand without pair and remove melds
		# Saves where hand check left off and continues making new pairs until the end
		elif sus_hand[current_index] == sus_hand[current_index+1]:
			depaired_hand = copy.deepcopy(sus_hand)
			del depaired_hand[current_index : current_index + 2]
			# if a hand with this pair is not winnable, move on to next pair
			if Game.remove_Melds(depaired_hand):
				return True
			else:
				Game.remove_Pairs(sus_hand, current_index +1)
		else:
			Game.remove_Pairs(sus_hand, current_index +1)
	
	# yup, recursion time
	@staticmethod
	def remove_Melds(demelded_hand):
		# if hand has been removed to the point of nothing left, then all
		# tiles could form into valid melds and hand is won
		if len(demelded_hand) == 0:
			return True
		else:
			# is a set?
			# can just check consecutive sets because they're sorted
			if demelded_hand[0] == demelded_hand[1] == demelded_hand[2]:
				del demelded_hand[0:3]
				return Game.remove_Melds(demelded_hand)
			# is a run?
			# runs cannot be checked in consective order because a same tile might get in the way
			elif Game.is_Run(demelded_hand):
				del demelded_hand[0:3]
				return Game.remove_Melds(demelded_hand)

	@staticmethod
	def is_Run(demelded_hand):
		for i in range(1, len(demelded_hand)):
			if demelded_hand[0].is_Higher_Tile(demelded_hand[i]):
				for j in range(i, len(demelded_hand)):
					if demelded_hand[i].is_Higher_Tile(demelded_hand[j]):
						return True
		else:
			return False


	@staticmethod
	def is_Win(hand):
		sus_hand = copy.deepcopy(hand)
		# begin the pain
		# if the hand is winnable, returns true
		return Game.remove_Pairs(sus_hand, 0)

	@staticmethod
	# testing
	def make_Winning_Hand():
		hand = []
		hand.append(Tile(1, 'B'))
		hand.append(Tile(1, 'B'))
		hand.append(Tile(1, 'B'))
		hand.append(Tile(1, 'B'))
		hand.append(Tile(2, 'B'))
		hand.append(Tile(3, 'B'))
		hand.append(Tile(3, 'B'))
		hand.append(Tile(3, 'B'))

		if Game.is_Win(hand):
			print('Tsumo!')
		else:
			print('Something went wrong, should have been a win')

	def play(self):
		for i in range(len(self.hands)):
			hand = ''
			for tile in self.hands[i]:
				hand = hand + str(tile) + ' '
			print('Hand ' + str(i + 1) + ': ' + hand)
			if Game.is_Win(self.hands[i]):
				print('Tsumo!')

class main():
	for i in range(3):
		game = Game(1)
		game.play()

main()
print('Finish')