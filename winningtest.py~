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
        if self.rank + 1 == other.rank:
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
        numTiles_in_Hand = 14

        # create and sort hands
        for i in range(numHands):
            hand = []
            for j in range(numTiles_in_Hand):
                hand.append(self.wall.deal())
            sortedHand = sorted(hand, key=lambda tile: tile.rank)
            self.hands.append(sortedHand)

    ''' finds all pairs in hand, removes them and starts removing melds'''
    @staticmethod
    def remove_Pairs(sus_hand: list[Tile]) -> bool:
        checked_tiles = [] # check skips tiles already checked
        for i in range(len(sus_hand)):
            # ends before the last tile
            if i == len(sus_hand) - 2:
                return False # no pairs were found
            elif not (sus_hand[i] in checked_tiles):
                if sus_hand[i] == sus_hand[i+1]:
                    depaired_hand = copy.deepcopy(sus_hand)
                    del depaired_hand[i : i + 2]
                    # start removing melds with the hand without a pair
                    if Game.remove_Melds(depaired_hand):
                        print('hand all removed!')
                        return True
                else:
                    checked_tiles.append(sus_hand[i])

    # yup, recursion time
    @staticmethod
    def remove_Melds(demelded_hand):
        print('length left: ' + str(len(demelded_hand)))
        # if hand has been removed to the point of nothing left, then all
        # tiles could form into valid melds and hand is won
        if len(demelded_hand) == 0:
            print('melds are cleared!')
            return True
        else:
            # is a set?
            # can just check consecutive sets because they're sorted
            if Game.is_Set(demelded_hand):
                return Game.remove_Melds(demelded_hand)
            # is a run?
            # runs cannot be checked in consective order because a same tile might get in the way
            # is_Run also removes a run if detected
            elif Game.is_Run(demelded_hand):
                return Game.remove_Melds(demelded_hand)

    @staticmethod
    def is_Set(demelded_hand):
        if demelded_hand[0] == demelded_hand[1] == demelded_hand[2]:
            print('set detected, removing set')
            print(demelded_hand[0])
            print(demelded_hand[1])
            print(demelded_hand[2])
            Game.remove_Set(demelded_hand)
            return True

    @staticmethod
    def remove_Set(demelded_hand):
        del demelded_hand[0:3]
    
    @staticmethod
    # removes three tiles in a run given the indexes
    def remove_Run(demelded_hand, first_tile_loc, second_tile_loc, third_tile_loc):
        print('run removal')
        print(demelded_hand[first_tile_loc])
        print(demelded_hand[second_tile_loc])
        print(demelded_hand[third_tile_loc])
        demelded_hand.pop(third_tile_loc)
        demelded_hand.pop(second_tile_loc)
        demelded_hand.pop(first_tile_loc)

    @staticmethod
    # detects a run and removes it
    def is_Run(demelded_hand):
        for i in range(1, len(demelded_hand)):
            if demelded_hand[0].is_Higher_Tile(demelded_hand[i]):
                for j in range(i + 1, len(demelded_hand)):
                    if demelded_hand[i].is_Higher_Tile(demelded_hand[j]):
                        Game.remove_Run(demelded_hand, 0, i, j)
                        return True
        else:
            print('no valid meld found!')
            return False

    @staticmethod
    def is_Win(hand):
        sus_hand = copy.deepcopy(hand)
        # ensure hand is sorted properly
        sus_hand = sorted(sus_hand, key=lambda tile: tile.rank)
        # begin the pain
        # if the hand is winnable, returns true
        return Game.remove_Pairs(sus_hand)

    @staticmethod
    # testing
    def make_Winning_Hand():
        hand = []
        hand.append(Tile(1, 'B'))
        hand.append(Tile(1, 'B'))
        hand.append(Tile(1, 'B'))
        hand.append(Tile(4, 'B'))
        hand.append(Tile(5, 'B'))
        hand.append(Tile(6, 'B'))
        hand.append(Tile(6, 'B'))
        hand.append(Tile(6, 'B'))
        hand.append(Tile(7, 'B'))
        hand.append(Tile(7, 'B'))
        hand.append(Tile(7, 'B'))
        hand.append(Tile(8, 'B'))
        hand.append(Tile(8, 'B'))
        hand.append(Tile(8, 'B'))

        if Game.is_Win(hand):
            print('1. Tsumo!')
        else:
            print('1. Something went wrong, should have been a win')

       # hand = []
       # hand.append(Tile(1, 'B'))
       # hand.append(Tile(2, 'B'))
       # hand.append(Tile(3, 'B'))
       # hand.append(Tile(2, 'B'))
       # hand.append(Tile(3, 'B'))
       # hand.append(Tile(4, 'B'))
       # hand.append(Tile(5, 'B'))
       # hand.append(Tile(6, 'B'))
       # hand.append(Tile(7, 'B'))
       # hand.append(Tile(7, 'B'))
       # hand.append(Tile(8, 'B'))
       # hand.append(Tile(9, 'B'))
       # hand.append(Tile(9, 'B'))
       # hand.append(Tile(9, 'B'))

       # if Game.is_Win(hand):
       #     print('2. Tsumo!')
       # else:
       #     print('2. Something went wrong, should have been a win')

    @staticmethod
    # testing
    def make_Wrong_Hand():
        hand = []
        hand.append(Tile(1, 'B'))
        hand.append(Tile(1, 'B'))
        hand.append(Tile(2, 'B'))
        hand.append(Tile(3, 'B'))
        hand.append(Tile(3, 'B'))
        hand.append(Tile(3, 'B'))
        hand.append(Tile(4, 'B'))
        hand.append(Tile(4, 'B'))
        hand.append(Tile(5, 'B'))
        hand.append(Tile(6, 'B'))
        hand.append(Tile(6, 'B'))
        hand.append(Tile(7, 'B'))
        hand.append(Tile(8, 'B'))
        hand.append(Tile(9, 'B'))

        if Game.is_Win(hand):
            print('This shouldn\'t be a win!')
        else:
            print('Correctly not a win')

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
        #game.play()

print('Finish')
Game.make_Winning_Hand()
#Game.make_Wrong_Hand()
