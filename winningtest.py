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

class Hand(object):
    def __init__(self):
        self.hand = []

    def add_Tile(self, tile: Tile):
        self.hand.append(tile)

    # sorts by rank and suit
    def sort_Hand(self):
        self.hand = sorted(self.hand, key=lambda tile: tile.suit)
        # sort within groups of suits then merge back into main hand
        # this way the hand is grouped into suits, which are then ranked in order
        sorted_Hand = []
        current_Suit = self.hand[0].suit
        suit_Group = []
        for tile in self.hand:
            if current_Suit == tile.suit:
                suit_Group.append(tile)
            else:
                suit_Group = sorted(suit_Group, key=lambda tile: tile.rank)
                sorted_Hand.extend(suit_Group)
                suit_Group =[]
                current_Suit = tile.suit
                suit_Group.append(tile)
        if len(suit_Group) > 0:
            suit_Group = sorted(suit_Group, key=lambda tile: tile.rank)
            sorted_Hand.extend(suit_Group)
        self.hand = sorted_Hand

    '''converts hand into a readable format, somewhat following riichi convention but
    accounting for Chinese mahjong variant tiles so honors are not collapsed into one notation (Z in riichi)'''
    def hand_To_String(self) -> str:
        if len(self.hand) == 0:
            print('Nothing in hand to print!')
        hand_String = ''
        self.sort_Hand()
        current_Suit = self.hand[0].suit # only print suit at end of a group of same suit
        for tile in self.hand:
            if current_Suit != tile.suit:
                hand_String = hand_String + current_Suit + ' '
                hand_String = hand_String + str(tile)
                current_Suit = tile.suit
            else:
                hand_String = hand_String + str(tile)
        if current_Suit == self.hand[-1].suit:
                hand_String = hand_String + self.hand[-1].suit
        hand_String = 'Hand: ' + hand_String
        return hand_String

    def check_Seven_Pairs(self) -> bool:
        if len(self.hand) % 2 != 0:
            return False
        half_hand = len(self.hand)/2
        num_pairs = int(half_hand)
        for i in range(num_pairs):
            if self.hand[2*i] != self.hand[2*i+1]:
                return False
        return True

    @staticmethod
    def is_Set(demelded_hand):
        if demelded_hand[0] == demelded_hand[1] == demelded_hand[2]:
            print('set detected, removing set')
            print(demelded_hand[0])
            print(demelded_hand[1])
            print(demelded_hand[2])
            Hand.remove_Set(demelded_hand)
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
                        Hand.remove_Run(demelded_hand, 0, i, j)
                        return True
        else:
            print('no valid meld found!')
            return False

    # yup, recursion time
    @staticmethod
    def remove_Melds(demelded_hand):
        # print('length left: ' + str(len(demelded_hand)))
        # if hand has been removed to the point of nothing left, then all
        # tiles could form into valid melds and hand is won
        if len(demelded_hand) == 0:
            print('melds are cleared!')
            return True
        else:
            # is a set?
            # can just check consecutive sets because they're sorted
            if Hand.is_Set(demelded_hand):
                return Hand.remove_Melds(demelded_hand)
            # is a run?
            # runs cannot be checked in consective order because a same tile might get in the way
            # is_Run also removes a run if detected
            elif Hand.is_Run(demelded_hand):
                return Hand.remove_Melds(demelded_hand)

    ''' finds all pairs in hand, removes them and starts removing melds'''
    def remove_Pairs(self) -> bool:
        checked_tiles = [] # check skips tiles already checked
        for i in range(len(self.hand)):
            # ends before the last tile
            if i == len(self.hand) - 2:
                return False # no pairs were found
            elif not (self.hand[i] in checked_tiles):
                if self.hand[i] == self.hand[i+1]:
                    depaired_hand = copy.deepcopy(self.hand)
                    del depaired_hand[i : i + 2]
                    # start removing melds with the hand without a pair
                    if Hand.remove_Melds(depaired_hand):
                        print('hand all removed!')
                        return True
                else:
                    checked_tiles.append(self.hand[i])


    # checks if hand is a complete winning hand
    def is_Win(self) -> bool:
        sus_hand = copy.deepcopy(self)
        # ensure hand is sorted properly
        sus_hand.sort_Hand()
        # check seven_pairs
        if self.check_Seven_Pairs():
            print('This is seven pairs!')
            return True
        # begin the pain
        # if the hand is winnable, returns true
        return Hand.remove_Pairs(sus_hand)

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

    def deal(self) -> Tile:
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
            hand = Hand()
            for j in range(numTiles_in_Hand):
                hand.add_Tile(self.wall.deal())
            hand.sort_Hand()
            self.hands.append(hand)


    @staticmethod
    # testing
    def make_Winning_Hand():
        # hand = Hand()
        # hand.add_Tile(Tile(1, 'S'))
        # hand.add_Tile(Tile(6, 'M'))
        # hand.add_Tile(Tile(1, 'S'))
        # hand.add_Tile(Tile(4, 'M'))
        # hand.add_Tile(Tile(5, 'M'))
        # hand.add_Tile(Tile(6, 'M'))
        # hand.add_Tile(Tile(1, 'S'))
        # hand.add_Tile(Tile(6, 'M'))
        # hand.add_Tile(Tile(7, 'P'))
        # hand.add_Tile(Tile(7, 'P'))
        # hand.add_Tile(Tile(7, 'P'))
        # hand.add_Tile(Tile(8, 'M'))
        # hand.add_Tile(Tile(8, 'M'))
        # hand.add_Tile(Tile(8, 'M'))

        # print ('1 Test: ' + hand.hand_To_String())

        # if hand.is_Win():
        #     print('1. Tsumo!')
        # else:
        #     print('1. Something went wrong, should have been a win')

       hand = Hand()
       hand.add_Tile(Tile(1, 'P'))
       hand.add_Tile(Tile(2, 'P'))
       hand.add_Tile(Tile(3, 'P'))
       hand.add_Tile(Tile(1, 'M'))
       hand.add_Tile(Tile(2, 'M'))
       hand.add_Tile(Tile(3, 'M'))
       hand.add_Tile(Tile(4, 'M'))
       hand.add_Tile(Tile(5, 'M'))
       hand.add_Tile(Tile(6, 'M'))
       hand.add_Tile(Tile(1, 'S'))
       hand.add_Tile(Tile(2, 'S'))
       hand.add_Tile(Tile(3, 'S'))
       hand.add_Tile(Tile(7, 'S'))
       hand.add_Tile(Tile(7, 'S'))

       if hand.is_Win():
           print('2. Tsumo!')
       else:
           print('2. Something went wrong, should have been a win')

    @staticmethod
    # testing
    def make_Wrong_Hand():
        hand = Hand()
        hand.add_Tile(Tile(1, 'M'))
        hand.add_Tile(Tile(2, 'M'))
        hand.add_Tile(Tile(3, 'S'))
        hand.add_Tile(Tile(3, 'S'))
        hand.add_Tile(Tile(3, 'S'))
        hand.add_Tile(Tile(3, 'M'))
        hand.add_Tile(Tile(4, 'S'))
        hand.add_Tile(Tile(4, 'S'))
        hand.add_Tile(Tile(5, 'S'))
        hand.add_Tile(Tile(8, 'P'))
        hand.add_Tile(Tile(7, 'M'))
        hand.add_Tile(Tile(7, 'P'))
        hand.add_Tile(Tile(6, 'P'))
        hand.add_Tile(Tile(9, 'P'))

        print ('2 Test: ' + hand.hand_To_String())

        if hand.is_Win():
            print('This shouldn\'t be a win!')
        else:
            print('Correctly not a win')
    
    @staticmethod
    def make_Seven_Pairs_Hand():
        hand = Hand()
        hand.add_Tile(Tile(4, 'M'))
        hand.add_Tile(Tile(1, 'S'))
        hand.add_Tile(Tile(1, 'M'))
        hand.add_Tile(Tile(2, 'P'))
        hand.add_Tile(Tile(2, 'P'))
        hand.add_Tile(Tile(3, 'P'))
        hand.add_Tile(Tile(3, 'P'))
        hand.add_Tile(Tile(1, 'M'))
        hand.add_Tile(Tile(4, 'M'))
        hand.add_Tile(Tile(6, 'S'))
        hand.add_Tile(Tile(1, 'S'))
        hand.add_Tile(Tile(6, 'M'))
        hand.add_Tile(Tile(6, 'M'))
        hand.add_Tile(Tile(6, 'S'))

        print ('3 Test: ' + hand.hand_To_String())

        if hand.is_Win():
            print('This is a win!')
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

def test(hand: str, winstatus: bool, ifsevenpairs: bool): #hand: in the format of 1m2m3s4p, etc., num must be even
    halfhand = int(len(hand)/2)
    sus_hand = Hand()
    
    for x in range(halfhand):
        sus_hand.add_Tile(Tile(hand[2*x], hand[2*x+1]))
        
    print('Judging ' + sus_hand.hand_To_String())

    if sus_hand.is_Win() and winstatus:
        print('The hand is correctly judged to be winning!')
    elif sus_hand.is_Win() == True and winstatus == False:
        print('The hand is incorrectly judged to be winning!')
    elif sus_hand.is_Win() == False and winstatus == True:
        print('The hand is incorrectly judged to be losing!')
    elif sus_hand.is_Win() == False and winstatus == False:
        print('The hand is correctly judged to be losing!')
    
Game.make_Winning_Hand()

test('1M2M3M1S2S3S1P2P3P4M6M5M7S7S', True, False)

print('Finish')

#Game.make_Wrong_Hand()
#Game.make_Seven_Pairs_Hand()

