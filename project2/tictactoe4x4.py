# Project 2
# Treverrio Primandaru
# December 13, 2022

from graphics import *

class Square:
    """ Class for squares of board.
    win is inherited GraphWin object.
    row is int of row that square rests on.
    col is int of col that square rests on."""
    def __init__(self, win, row, col):
        self.win = win
        self.row = row
        self.col = col
        self.value = "" # stores its value
        
        self.point_one = Point(row, col) # make square from Rectangle class with row and col
        self.point_two = Point(row+1, col+1)
        self.square = Rectangle(self.point_one, self.point_two)
        self.square.setFill("white")
        self.square.draw(self.win)
    
    def setValue(self, value):
        """Set the value of the square."""
        self.value = value
    
    def getValue(self):
        """Get the value of the square."""
        return self.value        
    
    def getRow(self):
        return self.row
    
    def getCol(self):
        return self.col
    
    def getCenter(self):
        return Point(self.row+0.5, self.col+0.5) # center of square is 0.5 from boundaries, based on set coordinates
    
    def isClicked(self, p):
        return (self.point_one.getX() <= p.getX() <= self.point_two.getX() and
                self.point_one.getY() <= p.getY() <= self.point_two.getY())



class Markers:
    """ Class to store different markers.
    win is inherited GraphWin object"""
    def __init__(self, win):
        self.win = win
        self.x_markers, self.o_markers = [], [] # list to store markers; used to check if 6 squares are already occoupied
    
    def getCenter(self, row, col):
        return Point(row+0.5, col+0.5)
    
    def drawX(self, row, col):
        self.x = Text(self.getCenter(row, col), "X") # use Text class to create X and O markers
        self.x.draw(self.win)
        self.x_markers.append(self.x) # append class to list to keep track of marker count later
        
    def drawO(self, row, col):
        self.o = Text(self.getCenter(row, col), "O")
        self.o.draw(self.win)
        self.o_markers.append(self.o)
    
    def undrawX(self):
        self.x_markers[0].undraw() # undraw object and remove it from list
        self.x_markers.pop(0)
        
    def undrawO(self):
        self.o_markers[0].undraw()
        self.o_markers.pop(0)
    
    def drawLine(self, square_first, square_last):
        self.center_first = square_first.getCenter() # marker for the winning combination
        self.center_last = square_last.getCenter()
        self.line = Line(self.center_first, self.center_last)
        self.line.draw(self.win)
     
        

class TicTacToe:
    """ Plays the actual game
    p1_marker is string specifying which player goes first"""
    def __init__(self, p1_marker):
        self.win = GraphWin("4x4 Tic Tac Toe", 640, 640)
        self.win.setCoords(0, 0, 4, 4)
        self.board = [[Square(self.win, i, j) for i in range(4)] for j in range(4)] # create UI board
        self.board_values = [[j.getValue() for j in i] for i in self.board] # create 2d array which is abstract of real board; empty at first
        
        self.x_count, self.o_count = 0, 0 # keep track of how many times X and O went
        self.p1 = p1_marker # p1 marker
        self.turn = "X" # specifies X always goes first
        self.winning_combo = [] # list of 1st and last points to create Line object
        
        self.marker = Markers(self.win) # create Marker object
        
    def checkSquare(self, i, j):
        """ check if square is occupied """
        if self.board_values[i][j] == "":
            return True
        else: return False
    
    def makeMove(self, i, j):
        """ draws the move """
        if self.turn == "X":
            self.sixXMarkersReached()
            self.marker.drawX(self.board[i][j].getRow(), self.board[i][j].getCol())
            self.board_values[i][j] = "X" # sets the index of abstract board to the same value of corresponding square
            self.x_count += 1
        elif self.turn == "O": 
            self.sixOMarkersReached()
            self.marker.drawO(self.board[i][j].getRow(), self.board[i][j].getCol())
            self.board_values[i][j] = "O"
            self.o_count += 1
            
    def switchPlayer(self):
        """ switch player """
        if self.turn == "X": self.turn = "O"
        else: self.turn = "X"
        
    def checkWin(self):
        """ check all winning combinations from abstract board;
        take 1st and last points to make line which signifies 4 in a row"""
        
        # check rows
        for row in self.board_values: # checks 1st dimension (row) of board
            if row == ['X', 'X', 'X', 'X']:
                self.winning_combo = [self.board[self.board_values.index(row)][0], self.board[self.board_values.index(row)][3]] # store 1st and last point of winning combo
                return "X"
            elif row == ['O', 'O', 'O', 'O']:
                self.winning_combo = [self.board[self.board_values.index(row)][0], self.board[self.board_values.index(row)][3]]
                return "O"

        # check columns
        for col in range(4):
            if self.board_values[0][col] == 'X' and self.board_values[1][col] == 'X' and self.board_values[2][col] == 'X' and self.board_values[3][col] == 'X':
                self.winning_combo = [self.board[0][col], self.board[3][col]]
                return "X"
            elif self.board_values[0][col] == 'O' and self.board_values[1][col] == 'O' and self.board_values[2][col] == 'O' and self.board_values[3][col] == 'O':
                self.winning_combo = [self.board[0][col], self.board[3][col]]
                return "O"

        # check diagonals
        if self.board_values[0][0] == 'X' and self.board_values[1][1] == 'X' and self.board_values[2][2] == 'X' and self.board_values[3][3] == 'X':
            self.winning_combo = [self.board[0][0], self.board[3][3]]
            return "X"
        elif self.board_values[0][0] == 'O' and self.board_values[1][1] == 'O' and self.board_values[2][2] == 'O' and self.board_values[3][3] == 'O':
            self.winning_combo = [self.board[0][0], self.board[3][3]]
            return "O"
        if self.board_values[0][3] == 'X' and self.board_values[1][2] == 'X' and self.board_values[2][1] == 'X' and self.board_values[3][0] == 'X':
            self.winning_combo = [self.board[0][3], self.board[3][0]]
            return "X"
        elif self.board_values[0][3] == 'O' and self.board_values[1][2] == 'O' and self.board_values[2][1] == 'O' and self.board_values[3][0] == 'O':
            self.winning_combo = [self.board[0][3], self.board[3][0]]
            return "O"

        return False # returns false if no one has won
    
    def sixXMarkersReached(self):
        """ undraw 1st of 6 marker for X """
        if self.x_count == 6:
            self.marker.undrawX()
    
    def sixOMarkersReached(self):
        if self.o_count == 6:
            self.marker.undrawO()

    def handleClick(self, p):
        """ handles click and checks for win """
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j].isClicked(p):
                    if self.checkSquare(i, j):
                        self.makeMove(i, j)
                        self.switchPlayer()
        
    def winUX(self, winner):
        """ game logic for when player win """
        p1_center = self.winning_combo[0].getCenter()
        p2_center = self.winning_combo[1].getCenter()
        self.win_line = Line(p1_center, p2_center) # creates line from winning combos list
        self.win_line.setOutline("red")
        self.win_line.setWidth(5)
        self.win_line.draw(self.win)
        self.win_screen = WinScreen(winner) # creates win screen object which notifies which player won
        
        while self.win_screen.windowOpen(): # checks if win screen is still open
            click = self.win_screen.checkMouse()
            if click:
                self.win.close()
                self.win_screen.handleClick(click) # handles clicks within win screen
    
    def runApp(self):
        """ runs the entire app """
        while self.win.isOpen():
            self.board_values = [[j.getValue() for j in i] for i in self.board] # resets abstrac board so that check win func isn't always true and game will wait for user to click things on win screen
            while (type(self.checkWin())!=str): # all return values of checkWin are strings except when no one is winning - then it's a bool; so this will keep the game running as long as no player has won
                click = self.win.checkMouse()
                if click:
                    self.handleClick(click)
            if self.checkWin() == self.p1: # checks winner
                winner = "P1"
                self.winUX(winner) # calls winning function
            elif self.checkWin != self.p1:
                winner = "P2"
                self.winUX(winner)



class SplashScreen:
    """ Splash screen for P1 to choose marker or quit """
    def __init__(self):
        self.win = GraphWin("Player Choice", 300, 150)
        self.win.setCoords(0, 0, 6.5, 10)
        
        self.x = Rectangle(Point(0.5, 5.5), Point(3, 9.5))
        self.x.setFill("white")
        self.x.draw(self.win)
        self.x_text = Text(self.getCenter(self.x), "P1: X")
        self.x_text.setSize(30)
        self.x_text.draw(self.win)
        
        self.o = Rectangle(Point(3.5, 5.5), Point(6, 9.5))
        self.o.setFill("white")
        self.o.draw(self.win)
        self.o_text = Text(self.getCenter(self.o), "P1: O")
        self.o_text.setSize(30)
        self.o_text.draw(self.win)
        
        self.quit = Rectangle(Point(3.5, 0.5), Point(4.5, 4.5))
        self.quit.setFill("white")
        self.quit.draw(self.win)
        self.quit_text = Text(self.getCenter(self.quit), "QUIT")
        self.quit_text.setSize(15)
        self.quit_text.draw(self.win)
        
        self.choice = False # stores p1 choice; false for now because program won't go on until variable type changes to string (specifying choice)
        
    def getCenter(self, object):
        """ get center of objects on screen """
        x_var = (object.getP1().getX() + object.getP2().getX()) 
        y_var = (object.getP1().getY() + object.getP2().getY()) 
        return Point(x_var/2, y_var/2)
    
    def getBoundaries(self, object):
        """ get x and y boundaries of objectts """
        x_min = object.getP1().getX()
        x_max = object.getP2().getX()
        y_min = object.getP1().getY()
        y_max = object.getP2().getY()
        return [x_min, x_max, y_min, y_max]
        
    def isClicked(self, p, i):
        """ checks if object has been clicked """
        return (self.getBoundaries(i)[0] <= p.getX() <= self.getBoundaries(i)[1] and
                self.getBoundaries(i)[2] <= p.getY() <= self.getBoundaries(i)[3])
        
    def handleClick(self, p):     
        """ decides what to do when objects are clicked """   
        if self.isClicked(p, self.quit):
            self.win.close() # close if quit button is clicked
            return False
        
        if self.isClicked(p, self.x):
            return "X"
        elif self.isClicked(p, self.o):
            return "O"
        
    def getOptions(self):
        """ as long as window is open, keep checking for click;
        return choice of what player 1 wants to play as """
        while self.win.isOpen():
            click = self.win.checkMouse()
            if click:
                self.choice = self.handleClick(click)
                self.win.close()
        
        return self.choice 

    def closeWindow(self):
        self.win.close()



class WinScreen:
    """ win screen for when a player wins
    winner is str object specifying which player won"""
    def __init__(self, winner):
        self.winner = winner
        self.win = GraphWin(f"{self.winner} wins!", 300, 100)
        self.win.setCoords(0, 0, 30, 10)
        
        self.banner = Rectangle(Point(1, 1), Point(9, 9))
        self.banner.setFill("green")
        self.banner.draw(self.win)
        
        self.winner_text = Text(Point(5, 5), f"{self.winner} wins!")
        self.winner_text.setOutline("white")
        self.winner_text.draw(self.win)
        
        self.play_again = Rectangle(Point(11, 1), Point(19, 9))
        self.play_again.setFill("white")
        self.play_again.draw(self.win)
        
        self.play_again_text = Text(Point(15, 5), f"Play again")
        self.play_again_text.setOutline("green")
        self.play_again_text.draw(self.win)
        
        self.quit = Rectangle(Point(21, 1), Point(29, 9))
        self.quit.setFill("white")
        self.quit.draw(self.win)
        
        self.quit_text = Text(Point(25, 5), f"Quit")
        self.quit_text.setOutline("green")
        self.quit_text.draw(self.win)
        
    def checkMouse(self):
        """ gets mouse as this function is neeeded by TicTacToe class """
        return self.win.getMouse()
        
    def windowOpen(self):
        """ checks if window is open """
        return self.win.isOpen()

    def isClicked(self, p, object):
        return (object.getP1().getX() <= p.getX() <= object.getP2().getX() and
                object.getP1().getY() <= p.getY() <= object.getP2().getY())
        
    def handleClick(self, p):
        """ handles what to do with clicks """
        if self.isClicked(p, self.play_again): # if play again is clicked, current window closes and program restarts
            self.win.close()
            run_TicTacToe()
        if self.isClicked(p, self.quit):
            self.win.close()

def run_TicTacToe():
    """ main function """
    splash = SplashScreen() # creates splash screen
    choice = splash.getOptions() # gets p1 marker choice from splash screen
    splash.closeWindow()
    if isinstance(choice, str): # only goes on if choice is valid (other option is False bool)
        app = TicTacToe(choice) # passes in p1 choice as argument
        app.runApp()
    
if __name__ == "__main__":
    run_TicTacToe()