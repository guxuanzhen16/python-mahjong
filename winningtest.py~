import random, copy

class Tile(object):
    RANKS = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    SUITS = ('M', 'P', 'S') # Sou (bamboo), Pin (dots), Man (characters)

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit= suit

    def __str__(self):
        return str(self.rank)
    
    def __eq__ (self, other):
        return (self.rank == other.rank) and (self.suit == other.suit)

    def __ne__ (self, other):
        return (self.rank != other.rank) and (self.suit == other.suit)

    def __lt__ (self, other):
        return (self.rank < other.rank)

    def __le__ (self, other):
        return (self.rank <= other.rank)

    def __gt__ (self, other):
        return (self.rank > other.rank)

    def __ge__ (self, other):
        return (self.rank >= other.rank)

    def is_Same_Suit(self, other):
        return (self.suit == other.suit)

    # checks if a given tile is higher than this tile by one and is same suit
    # used in run checks
    def is_Higher_Tile(self, other):
        if self.rank + 1 == other.rank and self.is_Same_Suit(other):
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
            print('calling sort hand to initialize hands')
            sorted_Hand = Game.sort_Hand(hand)
            self.hands.append(sorted_Hand)

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
                        # print('hand all removed!')
                        return True
                else:
                    checked_tiles.append(sus_hand[i])

    # yup, recursion time
    @staticmethod
    def remove_Melds(demelded_hand):
        # print('length left: ' + str(len(demelded_hand)))
        # if hand has been removed to the point of nothing left, then all
        # tiles could form into valid melds and hand is won
        if len(demelded_hand) == 0:
            # print('melds are cleared!')
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
           # print('set detected, removing set')
           # print(demelded_hand[0])
           # print(demelded_hand[1])
           # print(demelded_hand[2])
            Game.remove_Set(demelded_hand)
            return True

    @staticmethod
    def remove_Set(demelded_hand):
        del demelded_hand[0:3]
    
    @staticmethod
    # removes three tiles in a run given the indexes
    def remove_Run(demelded_hand, first_tile_loc, second_tile_loc, third_tile_loc):
       # print('run removal')
       # print(demelded_hand[first_tile_loc])
       # print(demelded_hand[second_tile_loc])
       # print(demelded_hand[third_tile_loc])
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
            # print('no valid meld found!')
            return False

    @staticmethod
    def is_Win(hand):
        sus_hand = copy.deepcopy(hand)
        # ensure hand is sorted properly
        print('calling sort hand to check win')
        sus_hand = Game.sort_Hand(sus_hand)
        # begin the pain
        # if the hand is winnable, returns true
        return Game.remove_Pairs(sus_hand)

    '''converts hand into a readable format, somewhat following riichi convention but
    accounting for Chinese mahjong variant tiles so honors are not collapsed into one notation (Z in riichi)'''
    @staticmethod
    def hand_To_String(hand: list[Tile]) -> str:
        hand_String = ''
        print('calling sort hand to print')
        sorted_Hand = Game.sort_Hand(hand)
        current_Suit = sorted_Hand[0].suit # only print suit at end of a group of same suit
        for tile in sorted_Hand:
            if current_Suit != tile.suit:
                hand_String = hand_String + current_Suit + ' '
                hand_String = hand_String + str(tile)
                current_Suit = tile.suit
            else:
                hand_String = hand_String + str(tile)
        if current_Suit == sorted_Hand[-1].suit:
                hand_String = hand_String + sorted_Hand[-1].suit
        hand_String = 'Hand: ' + hand_String
        return hand_String

    # creates a deep copy of the hand that is sorted by rank and suit
    @staticmethod
    def sort_Hand(hand: list[Tile]) -> list[Tile]:
        suited_Hand = copy.deepcopy(hand)
        suited_Hand = sorted(suited_Hand, key=lambda tile: tile.suit)
        # sort within groups of suits then merge back into main hand
        # this way the hand is grouped into suits, which are then ranked in order
        sorted_Hand = []
        current_Suit = suited_Hand[0].suit
        suit_Group = []
        for tile in suited_Hand:
            if current_Suit == tile.suit:
                suit_Group.append(tile)
            else:
                suit_Group = sorted(suit_Group, key=lambda tile: tile.rank)
                sorted_Hand.extend(suit_Group)
                suit_Group =[]
                current_Suit = tile.suit
                suit_Group.append(tile)
        if len(suit_Group) > 0:
            sorted_Hand.extend(suit_Group)
        return sorted_Hand

    @staticmethod
    # testing
    def make_Winning_Hand():
        hand = []
        hand.append(Tile(1, 'S'))
        hand.append(Tile(6, 'M'))
        hand.append(Tile(1, 'S'))
        hand.append(Tile(4, 'M'))
        hand.append(Tile(5, 'M'))
        hand.append(Tile(6, 'M'))
        hand.append(Tile(1, 'S'))
        hand.append(Tile(6, 'M'))
        hand.append(Tile(7, 'P'))
        hand.append(Tile(7, 'P'))
        hand.append(Tile(7, 'P'))
        hand.append(Tile(8, 'M'))
        hand.append(Tile(8, 'M'))
        hand.append(Tile(8, 'M'))

        print ('1 Test: ' + Game.hand_To_String(hand))

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
        hand.append(Tile(1, 'M'))
        hand.append(Tile(2, 'M'))
        hand.append(Tile(3, 'S'))
        hand.append(Tile(3, 'S'))
        hand.append(Tile(3, 'S'))
        hand.append(Tile(3, 'M'))
        hand.append(Tile(4, 'S'))
        hand.append(Tile(4, 'S'))
        hand.append(Tile(5, 'S'))
        hand.append(Tile(8, 'P'))
        hand.append(Tile(7, 'M'))
        hand.append(Tile(7, 'P'))
        hand.append(Tile(6, 'P'))
        hand.append(Tile(9, 'P'))

        print ('2 Test: ' + Game.hand_To_String(hand))

        if Game.is_Win(hand):
            print('This shouldn\'t be a win!')
        else:
            print('Correctly not a win')

    def play(self):
        for hand in self.hands:
            print(Game.hand_To_String(hand))
            if Game.is_Win(hand):
                print('Tsumo!')

class main():
    for i in range(1):
        game = Game(1)
        #game.play()

print('Finish')
Game.make_Winning_Hand()
Game.make_Wrong_Hand()
