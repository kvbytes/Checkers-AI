'''
@author: mroch
'''

# Game representation and mechanics

# tonto - Professor Roch's not too smart strategy
# You are not given source code to this, but compiled .pyc files
# are available for Python 3.7 and 3.8 (fails otherwise).
# This will let you test some of your game logic without having to worry
# about whether or not your AI is working and let you pit your player
# against another computer player.
#

import statistics

# Python can load compiled modules using the imp module (deprecated)
# We'll format the path to the tonto module based on the
# release of Python.  Note that we provided tonto compilations for Python 3.7
# and 3.8.  If you're not using one of these, it won't work.
if True:
    # import imp
    import sys

    major = sys.version_info[0]
    minor = sys.version_info[1]
    # modpath = "lib/__pycache__/tonto.cpython-37.pyc".format(major, minor)
    # tonto = imp.load_compiled("tonto", modpath)

# human - human player, prompts for input
from lib import human, checkerboard
import ai
from lib.timer import Timer


def Game(red=ai.Strategy, black=human.Strategy, init=None, maxplies=8, verbose=False):
    """Game(red, black, maxplies, init, verbose, turn)
    Start a game of checkers
    red,black - Strategy classes (not instances)
    maxplies - # of turns to explore (default 10)
    init - Start with given board (default None uses a brand new game)
    verbose - Show messages (default True)
    firstmove - Player N starts 0 (red) or 1 (black).  Default 0. 

    Returns winning player 'r' or 'b'
    """
    t = Timer()
    with open('game.txt', 'w') as f:

        # start with a new board if there isn't a starting configuration
        if init is None:
            b = checkerboard.CheckerBoard()
            redstrat = red('r', b, maxplies)
            blackstrat = black('b', b, maxplies)
        else:
            b = init
            redstrat = red('r', b, maxplies)
            blackstrat = black('b', b, maxplies)

        # loop through turns while the game isn't over
        while not b.is_terminal()[0]:
            (b, action) = redstrat.play(b)
            print("Red would select ", action)
            print(b)
            f.write("Red would select " + str(action) + "\n")
            f.write(str(b) + "\n\n")

            (b, action) = blackstrat.play(b)
            print("Black would select ", action)
            print(b)
            f.write("Black would select " + str(action) + "\n")
            f.write(str(b) + "\n\n")

        # determine the winner when game ends
        if b.is_terminal()[1] == 'r':
            winner = 'r'
            print("Winner is Red!")
            print("Time elapsed in seconds: ", t.elapsed_s())
            f.write(str("Winner is Red!" + "\n"))
            f.write("Time elapsed in seconds: " + str(t.elapsed_s()))
            f.close()
            return winner
        else:
            winner = 'b'
            print("Winner is Black!")
            print("Time elapsed in seconds: ", t.elapsed_s())
            f.write(str("Winner is Black!") + "\n")
            f.write("Time elapsed in seconds: " + str(t.elapsed_s()))
            f.close()
            return winner


if __name__ == "__main__":
    # Examples
    # Starting from specific board with default strategy
    # Game(init=boardlibrary.boards["multihop"])
    # Game(init=boardlibrary.boards["StrategyTest1"])
    # Game(init=boardlibrary.boards["EndGame1"], firstmove = 1)

    # Tonto vs Tonto
    # Game(red=tonto.Strategy, black=tonto.Strategy)

    # AI vs human
    winner = Game(red=ai.Strategy, black=human.Strategy, maxplies=10)

    # Play with default strategies...
    # Game()
