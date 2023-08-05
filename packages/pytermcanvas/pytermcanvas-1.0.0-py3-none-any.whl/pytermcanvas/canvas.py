# version: 1.0.0 (alpha)
import cursor
from PIL import Image

class TerminalCanvas:
    def __init__(self, xsize, ysize, auto_render=True, empty=' '):
        self.cols = xsize
        self.rows = ysize
        self.data = []
        self.auto_render = auto_render
        self.empty = empty
        self.clear()

    # method called after any drawing method
    def autoRender(self):
        if(self.auto_render == True):
            self.render()

    # rendering method
    def render(self):
        z = 0
        print("\033c", end="")
        cursor.hide()
        try:
            for y in range(self.rows):
                for x in range(self.cols):
                    print(self.data[z], end="")
                    z = z + 1
                print("\n",end="")
        except:
            cursor.show()
        cursor.show()

    # method to clear the screen
    def clear(self):
        self.data.clear()
        for i in range(self.rows*self.cols):
            self.data.append(self.empty)
        self.autoRender()

    # method to insert string or list of characters to specified row
    def insertRow(self, y, row_data, offset=0):
        if(type(row_data) is list or type(row_data) is tuple):
            row_arr = row_data
        else:
            row_arr = list(row_data)

        for i in range(len(row_arr)):
            self.data[i+(self.cols * y)+offset] = row_arr[i]
        self.autoRender()

    # method to insert string or list of characters to specified column
    def insertCol(self, x, col_data, offset=0):
        if(type(col_data) is list or type(col_data) is tuple):
            col_arr = col_data
        else:
            col_arr = list(col_data)

        for i in range(self.rows):
            try:
                self.data[(i+offset) * self.cols + x] = col_arr[i]
            except:
                break
        self.autoRender()

    # changes character at specified location
    def setChar(self, x, y, char):
        self.data[(self.cols*y) + x] = char
        self.autoRender()

    # get character from specified location
    def getChar(self, x, y):
        return self.data[(self.cols*y) + x]

    # get list of characters from specified row
    def getRow(self, y):
        return_data = []
        for i in range(self.cols):
            return_data.append(self.data[(y * self.cols) + i])
        return return_data

    # get list of characters from specified column
    def getCol(self, x):
        return_data = []
        for i in range(self.rows):
            return_data.append(self.data[i * self.cols + x])
        return return_data

    # draw image with specified size
    def drawImage(self, path, **kwargs):
        if("mode" in kwargs):
            mode = kwargs["mode"]
        else:
            mode = "bg"
        if("char" in kwargs):
            char = kwargs["char"]
        else:
            char = " "
        if("size" in kwargs):
            size = kwargs["size"]
        else:
            size = (self.cols, self.rows)
        temp_render = self.auto_render
        self.auto_render = False
        image = Image.open(path)
        image = image.resize((size[0], size[1]), Image.ANTIALIAS)
        for x in range(size[0]):
            for y in range(size[1]):
                pixel = image.getpixel((x, y))
                r = pixel[0]
                g = pixel[1]
                b = pixel[2]
                if(mode == "fg"):
                    color_char = "\x1b[38;2;%d;%d;%dm%c\x1b[0m" % (r, g, b, char)
                elif(mode == "bg"):
                    color_char = "\x1b[48;2;%d;%d;%dm%c\x1b[0m" % (r, g, b, char)
                self.setChar(x, y, color_char)

        self.auto_render = temp_render
        self.autoRender()

    # draw rectangle
    def drawRect(self, x, y, w, h, **kwargs):
        if("mode" in kwargs):
            mode = kwargs["mode"]
        else:
            mode = "bg"
        if("char" in kwargs):
            char = kwargs["char"]
        else:
            char = " "
        if("color" in kwargs):
            color = kwargs["color"]
        else:
            color = (255, 255, 255)
        temp_render = self.auto_render
        self.auto_render = False
        for i in range(h):
            if(mode == "fg"):
                color_char = "\x1b[38;2;%d;%d;%dm%c\x1b[0m" % (color[0], color[1], color[2], char)
                self.insertRow(i+y, [color_char]*w, x)
            elif(mode == "bg"):
                color_char = "\x1b[48;2;%d;%d;%dm%c\x1b[0m" % (color[0], color[1], color[2], char)
                self.insertRow(i+y, [color_char]*w, x)
        self.auto_render = temp_render
        self.autoRender()

    # resize the canvas
    def resize(self, xsize, ysize):
        self.rows = ysize
        self.cols = xsize
        self.clear()
