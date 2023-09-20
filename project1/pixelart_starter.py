# Project 1
# Treverrio Primandaru
# December 11, 2022

from graphics import *

class Square:
    """ A Square object appears as a (colored-in) square.
        The Square knows when it's clicked on, what color it is.
        The Square also can highlight and unhighlight itself.
    """

    def __init__(self, win, center, size, color):
        """ win: GraphWin object
            center: Point object, specifying the center of the Square
            size: int or float, specifying the length of the side of the Square
            color: string specifying color of the Square

            Creates and draws the Square in the win object.
        """
        self.win = win # set all parameters as class attributes
        self.center = center
        self.size = size
        self.color = color
        self.highlighted = False # # create bool state for highlight

        x, y, radius = center.getX(), center.getY(), self.size/2 # get center of square as well as "radius"
        self.xmax, self.xmin = x+radius, x-radius # borders of square are determined by x and y min and max values (since it is essentially a Rectangle object)
        self.ymax, self.ymin = y+radius, y-radius # these values are the values from the center to the edges of the square
        self.square = Rectangle(Point(self.xmin, self.ymin), Point(self.xmax, self.ymax)) # create a Rectangle object
        self.square.setFill(self.color) # set fill of Rectangle object
        self.square.draw(self.win) # draw Rectangle object

    def isClicked(self, p):
        """ p: Point object
            Returns True if p is inside the Square, False otherwise.
        """
        return (self.xmin <= p.getX() <= self.xmax and # if click is within square borders, then square has been clicked
                self.ymin <= p.getY() <= self.ymax)

    def getColor(self):
        """ Return color of square
        """
        return self.color

    def changeColor(self, newcolor):
        """ newcolor: string specifying color
            Changes the color of the Square
        """
        self.color = newcolor # assign passed in parameter as new color
        self.square.setFill(self.color) # refill the square with new color

    def highlight(self):
        """ Make the outline thick and red """
        self.square.setWidth(5) # set width of highlight border
        self.square.setOutline("red") # set outline color of highlight
        self.highlighted = True # switch highlight state to true

    def unhighlight(self):
        """ Make the outline thin and gray """
        self.square.setWidth(3) # set width of highlight border
        self.square.setOutline("gray") # set outline of highlight
        self.highlighted = False # switch highlight state to false
        
class Canvas:
    """ Object filled with rows and columns of Squares.
        Canvas knows the current color, can determine which Square is clicked on,
        and changes that Square to the current color.
    """

    def __init__(self, win, pt, rows, columns, size, color):
        """ win: GraphWin object
            pt: Point object, specifies lower-left coordinate.
            columns, rows: int indicating number of rows and columns of Square objects
            size: int or float, size of the Square objects
            color: initial color of the Square objects

            Creates and draws the Canvas in the win object.
        """
        self.win = win # set all parameters as class attributes
        self.pt = pt
        self.rows, self.columns = rows, columns
        self.size = size # size of Square objects
        self.color = color # initial color of squares, this will become the "brush"
        
        self.canvas_xmin, self.canvas_xmax = self.pt.getX(), self.rows*size # set borders of entire canvas
        self.canvas_ymin, self.canvas_ymax = self.pt.getY(), self.columns*size
        
        self.square_radius = self.size / 2 # get radius of the squares (all squares have same radius)
        self.xbase, self.ybase = self.pt.getX(), self.pt.getY() # get coordinates of base of canvas
        self.squares = [] # keep all squares in a 2d list
        
        for i in range(self.rows):
            self.squares.append([]) # create 2nd dimension of list
            for j in range(self.columns):
                self.square_center = Point((self.xbase + self.square_radius + i*self.size), (self.ybase + self.square_radius + j*self.size)) # set center of squares (since Square class only creates squares given the center)
                self.square = Square(self.win, self.square_center, self.size, self.color) # create square object
                self.squares[i].append(self.square) # place newly created squares into list

    def getSqColor(self, i, j):
        """ Gets the color of the Square at i-th row and j-th column """
        return self.squares[i][j].getColor() # squares list is structured exactly like GUI grid, so index at [i][j] represents i-th row and j-th column
    
    def changeCurrentColor(self, newcolor):
        """ Changes current color to newcolor. """
        self.color = newcolor # assign "brush" color to new color

    def isClicked(self, p):
        """ p: Point object
            Returns True if p is inside the Canvas, False otherwise.
        """
        return (self.canvas_xmin <= p.getX() <= self.canvas_xmax and # if click is within canvas borders, then canvas has been clicked
                self.canvas_ymin <= p.getY() <= self.canvas_ymax)

    def changeSquare(self, p):
        """ p: Point object
            Changes the Square clicked by the Point p to the current color.
        """
        for i in self.squares: # iterate through 2d list
            for j in i: 
                if j.isClicked(p): # checks if square is clicked
                    j.changeColor(self.color) # changes color of square

        

class Controls:
    """ Control panel.
        Has the color palette, and the Draw button.
    """

    def __init__(self, win, P1, P2, sqsize):
        """ win: GraphWin object
            P1, P2: Point objects, lower-left and upper-right points
            sqsize : int or float, size of the squares in the color palette.
        """
        self.win = win # set all parameters as class attributes
        self.P1, self.P2 = P1, P2
        self.sqsize = sqsize
        
        self.controls_xmin, self.controls_xmax = self.P1.getX(), self.P2.getX() 
        self.controls_ymin, self.controls_ymax = self.P1.getY(), self.P2.getY()
        
        self.black = Square(self.win, Point(16*4, 665), self.sqsize, "black") # created custom center points for color palletes
        self.gray = Square(self.win, Point(16*8, 665), self.sqsize, "gray")
        self.white = Square(self.win, Point(16*12, 665), self.sqsize, "white")
        self.colors = [self.black, self.gray, self.white] # create a list to store color palletes
        
        self.draw_btn_xmin, self.draw_btn_xmax = 16*30, 16*36 # create custom p1 and p2 for "Draw" button (which is a Rectangle object)
        self.draw_btn_ymin, self.draw_btn_ymax = 645, 685
        self.draw_btn = Rectangle(Point(self.draw_btn_xmin, self.draw_btn_ymin), Point(self.draw_btn_xmax, self.draw_btn_ymax))
        self.draw_txt = Text(Point(16*33, 665), "Draw") # create text for "Draw" button
        
        self.draw_btn.setFill("white") # set "Draw" button fill as white
        
        self.draw_btn.draw(self.win) # draw "Draw" button with text
        self.draw_txt.draw(self.win)


    def isClicked(self, p):
        """ p: Point object
            Returns True if p is inside the Controls, False otherwise
        """
        return (self.controls_xmin <= p.getX() <= self.controls_xmax and # if click is within controls borders, then controls has been clicked 
                self.controls_ymin <= p.getY() <= self.controls_ymax)

    def ColorIsClicked(self, p):
        """ p: Point object
            If clicked on a color square in the color palette, return True.
            Otherwise return False.
        """
        for i in self.colors: # iterates through color palletes
            if i.isClicked(p): # checks if square is clicked
                return i.isClicked(p) # return True if clicked
                
    def getClickedColor(self, p):
        """ p: Point object inside a color square in the color palette.
            Return the color of the square.
        """
        for i in self.colors: # iterates through color palletes
            i.unhighlight() # makes sure to "refresh" GUI by unhighlighting all colors
        
        for i in self.colors: # iterates through color palletes
            if i.isClicked(p): # only highlight the color that was clicked
                i.highlight()
                return i.getColor() # gets new color of square

    def DRAWClicked(self, p):
        """ True if p is inside the DRAW button, False otherwise. """
        return (self.draw_btn_xmin <= p.getX() <= self.draw_btn_xmax and # if click is within "Draw" button borders, then "Draw" button has been clicked
                self.draw_btn_ymin <= p.getY() <= self.draw_btn_ymax)



class PixelArt:
    """ Combines the following:
        A GraphWin object for this application
        The Canvas object
        The Controls object
        The drawing square where the pixel art will be drawn.
    """

    def __init__(self):
        # This constructor method is already written for you.
        self.win = GraphWin("Pixel Art", 640, 640 + 50, autoflush = False)
        self.win.setCoords(0, 0, 640, 640+50)
        self.controls = Controls(self.win, Point(0,640), Point(640-50, 640+50), 40)
        self.drawing = Rectangle(Point(640-50, 640), Point(640, 640+50))
        self.drawing.setFill("white")
        self.drawing.draw(self.win)
        self.columns, self.rows = 16, 16
        self.canvas = Canvas(self.win, Point(0,0), self.columns, self.rows, 40, "white")
        update()

    def drawPixelArt(self):
        """ Draws the pixel art in the center of the Drawing rectangle,
            with pixels corresponding to the squares in the Canvas.
        """
        colors = [] # create a 2d list to store colors
        for i in range(self.rows):
            colors.append([]) # create 2nd dimension of list
            for j in range(self.columns):
                colors[i].append(self.canvas.getSqColor(i, j)) # stores all current colors of squares in canvas into a list
        
        for i in range(self.rows):
            for j in range(self.columns):
                self.win.plot(607+i, 657+j, colors[i][j]) # use plot function to map all items in colors list; value of x, y coordinates calculated by hand
        
    def handleClick(self, p):
        """ Handles a click, as appropriate. """
        if self.canvas.isClicked(p): self.canvas.changeSquare(p) # if canvas is clicked, square in canvas changes color
        if self.controls.isClicked(p): # if controls is clicked
            if self.controls.ColorIsClicked(p): # if a color pallete is clicked
                self.canvas.changeCurrentColor(self.controls.getClickedColor(p)) # change "brush" color
            if self.controls.DRAWClicked(p): # if "Draw" button is clicked
                self.drawPixelArt() # draw the pixel art
        update()  # End this method with an a call to update the GraphWin object
 

    def runApp(self):
        """ Runs the PixelArt app """
        # This method is already written for you.
        while self.win.isOpen():
            click = self.win.checkMouse()
            if click:
                self.handleClick(click)
        

def run_PixelArt():
    # This function is already written for you.
    app = PixelArt()
    app.runApp()
    
          
if __name__ == "__main__":
    run_PixelArt()