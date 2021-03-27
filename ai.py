"""
Checkers AI
CS 550 - Artificial Intelligence
Fall 2020
"""

from lib import abstractstrategy, boardlibrary


class AlphaBetaSearch:

    def __init__(self, strategy, maxplayer, minplayer, maxplies=3,
                 verbose=False):
        """"alphabeta_search - Initialize a class capable of alphabeta search
        problem - problem representation
        maxplayer - name of player that will maximize the utility function
        minplayer - name of player that will minimize the uitlity function
        maxplies- Maximum ply depth to search
        verbose - Output debugging information
        """
        self.strategy = strategy
        self.maxplayer = maxplayer
        self.minplayer = minplayer
        self.maxplies = maxplies
        self.verbose = verbose

    def alphabeta(self, state):
        """
        Conduct an alpha beta pruning search from state
        :param state: Instance of the game representation
        :return: best action for maxplayer
        """
        # begin search, with very large values to use as infinity, depth of 1
        value, bestaction = self.maxvalue(state, -9999, 9999, 1)

        return bestaction

    def cutoff(self, state, ply):
        """
        cutoff_test - Should the search stop?
        :param state: current game state
        :param ply: current ply (depth) in search tree
        :return: True if search is to be stopped (terminal state or cutoff
           condition reached)
        """
        # check if the game is over or if max depth has been reached while searching
        gameover, winner = state.is_terminal()
        if gameover or ply == self.maxplies:
            return True
        else:
            return False

    def maxvalue(self, state, alpha, beta, ply):
        """
        maxvalue - - alpha/beta search from a maximum node
        Find the best possible move knowing that the next move will try to
        minimize utility.
        :param state: current state
        :param alpha: lower bound of best move max player can make
        :param beta: upper bound of best move max player can make
        :param ply: current search depth
        :return: (value, maxaction)
        """
        if self.cutoff(state, ply):
            value = self.strategy.evaluate(state)
            maxaction = None  # we don't need one
            return value, maxaction
        else:
            value = -9999
            actions = state.get_actions(self.maxplayer)
            maxaction = None
            # iterate through all actions and find best
            for act in actions:
                if self.minvalue(state.move(act), alpha, beta, ply + 1)[0] > value:
                    value = self.minvalue(state.move(act), alpha, beta, ply + 1)[0]
                    maxaction = act
                if value >= beta:
                    return value, maxaction  # this return functions as pruning
                else:
                    alpha = max(alpha, value)  # update alpha
                    return value, maxaction

    def minvalue(self, state, alpha, beta, ply):
        """
        minvalue - alpha/beta search from a minimum node
        :param state: current state
        :param alpha:  lower bound on best move for min player
        :param beta:  upper bound on best move for max player
        :param ply: current depth
        :return: (v, minaction)  Value of min action and the action that
           produced it.
        """

        if self.cutoff(state, ply):
            value = self.strategy.evaluate(state)
            minaction = None
            return value, minaction
        else:
            value = 9999  # high start value, functions as infinity
            actions = state.get_actions(self.minplayer)
            minaction = None
            # iterate through all actions and find best
            for act in actions:
                if self.maxvalue(state.move(act), alpha, beta, ply + 1)[0] < value:
                    value = self.maxvalue(state.move(act), alpha, beta, ply + 1)[0]
                    minaction = act
                if value <= alpha:
                    return value, minaction  # this return functions as pruning
                else:
                    beta = min(beta, value)  # update beta
                    return value, minaction


class Strategy(abstractstrategy.Strategy):
    """Your strategy, maybe you can beat Tamara Tansykkuzhina, 
       2019 World Women's Champion
    """

    def __init__(self, *args):
        """
        Strategy - Concrete implementation of abstractstrategy.Strategy
        See abstractstrategy.Strategy for parameters
       """

        super(Strategy, self).__init__(*args)

        self.search = AlphaBetaSearch(self, self.maxplayer, self.minplayer,
                                      maxplies=self.maxplies, verbose=False)

    def play(self, board):
        """
        play(board) - Find best move on current board for the maxplayer
        Returns (newboard, action)
        """
        bestaction = self.search.alphabeta(board)

        # same board if no actions
        if not bestaction:
            return board, bestaction
        # update the board after a move
        newboard = board.move(bestaction)
        return newboard, bestaction

    def evaluate(self, state, turn=None):
        """
        evaluate - Determine utility of terminal state or estimated
        utility of a non-terminal state
        :param state: Game state
        :param turn: Optional turn (None to omit)
        :return:  utility or utility estimate based on strength of board
                  (bigger numbers for max player, smaller numbers for
                   min player)
        """
        # update piece count to avoid errors
        state.update_counts()

        # check if game is over
        gameover, winner = state.is_terminal()

        # estimated utility of a non-terminal state
        if not gameover:
            utility = 0
            king = 10
            pawn = 5

            # utility for # of kings and pawns of players
            redpawns = state.get_pawnsN()[state.playeridx(self.maxplayer)]
            redkings = state.get_kingsN()[state.playeridx(self.maxplayer)]
            blackpawns = state.get_pawnsN()[state.playeridx(self.minplayer)]
            blackkings = state.get_kingsN()[state.playeridx(self.minplayer)]

            # utility based on piece count
            utility += pawn * redpawns  # maxplayer
            utility += king * redkings
            utility -= pawn * blackpawns  # minplayer
            utility -= king * blackkings

            # utility based on each pawn's distance to becoming a king
            for (row, col, piece) in state:
                player, isKing = state.identifypiece(piece)
                # utility for maxplayer
                if player == 0:
                    if not isKing:
                        utility += state.edgesize - state.disttoking(piece, row)
                        # state.disttoking(self.minplayer, distancerow[0])
                # utility for minplayer
                else:
                    if not isKing:
                        utility -= state.edgesize - state.disttoking(piece, row)

        # utility for terminal state
        else:
            if winner == self.maxplayer:
                utility = 500  # very high number to prioritize wins
            elif winner == self.minplayer:
                utility = -500
            else:
                utility = 0  # no points for draw
        return utility


# Run test cases if invoked as main module
if __name__ == "__main__":
    b = boardlibrary.boards['SingleHopsRed']
    print(b)
    redstrat = Strategy('r', b, 6)
    blackstrat = Strategy('b', b, 6)

    while not b.is_terminal()[0]:
        (b, action) = redstrat.play(b)
        print("Red would select ", action)
        print(b)

        (b, action) = blackstrat.play(b)
        print("Black would select ", action)
        print(b)
    print(b.is_terminal()[1])