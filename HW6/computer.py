from perm import *
from wordgames import *

#
# Problem A: Computer chooses a word
#
def comp_choose_word(hand, words):
    """
    Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
    This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    words: list of strings
    """
    # TO DO...

#
# Problem B: Computer plays a hand
#
def comp_play_hand(hand, words):
    """
     Allows the computer to play the given hand, as follows:

     * The hand is displayed.
     * The computer chooses a word using comp_choose_words(hand, word_dict).
     * After every valid word: the score for that word is displayed, 
       the remaining letters in the hand are displayed, and the computer 
       chooses another word.
     * The sum of the word scores is displayed when the hand finishes.
     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     words: list of strings
    """
    # TO DO ...    
    
#
# Problem C: Playing a game
#
def play_game(words):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
       * If the user inputs 'n', play a new (random) hand.
       * If the user inputs 'r', play the last hand again.
       * If the user inputs 'e', exit the game.
       * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
       * If the user inputs 'u', let the user play the game as before using
         play_hand.
       * If the user inputs 'c', let the computer play the game using
         comp_play_hand (created above).
       * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    words: list of strings
    """
    # TO DO...
        
#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    words = load_words()
    play_game(words)
