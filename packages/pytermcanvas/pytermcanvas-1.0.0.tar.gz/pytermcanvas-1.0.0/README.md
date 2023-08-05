# pytermcanvas

## Requirements
* terminal emulator (with [true color support](https://gist.github.com/sindresorhus/bed863fb8bedf023b833c88c322e44f9))
* python3
  * pip
  * [PIL](https://pypi.org/project/Pillow/)
  * [cursor](https://pypi.org/project/cursor/)

## Install
```sh
pip install pytermcanvas
```
## Usage
### *class* TerminalCanvas(*x_size, y_size, auto_render, empty_char*)
##### Parameters:
* **x_size** (Int) - number of columns to use, stored in *self.cols*
* **y_size** (Int) - number of rows to use, stored in *self.rows*
* **auto_render** (Bool) [default: `True`]
  * `True` - enable automatic canvas rendering
  * `False` - disable automatic canvas rendering
* **empty_char** (Char) [default: `SPACE`] - character used to fill the canvas on creation


##### Methods:
####  render()
*Renders canvas*
****
####  clear()
*Clears canvas*
****
#### resize(*x_size, y_size*)
* **x_size** (Int) - number of columns to use, stored in *self.cols*
* **y_size** (Int) - number of rows to use, stored in *self.rows*
****
#### drawImage(*path, **\*kwargs)
*Draws image on canvas*
* **path** (Str) - path to image<br><br>
* **mode** (Str) [default: `bg`] - mode to use for rendering
  * `bg` - change color behind character
  * `fg` - change color of specified character
* **size** (List or Tuple) [default: canvas size] - desired size of image
  * **size**[0] (Int) - number of columns to use
  * **size**[1] (Int) - number of rows to use
* **char** (Char) [defualt: `SPACE`] - character to print, mainly used for `fg` rendering
****
#### drawRect(*col, row, width, height, **\*kwargs)
*Draws rectangle on canvas*
* **col** (Int) - position of top left corner in column
* **row** (Int) - position of top left corner in row
* **width** (Int) - width of rectangle
* **height** (Int) - height of rectangle<br><br>
* **mode** (Str) [default: `bg`] - mode to use for rendering
  * `bg` - change color behind character
  * `fg` - change color of specified character
* **color** (List or Tuple) [default: `(255, 255, 255)`] - RGB color of rectangle
  * **color**[0] (Int) - Red, `0 - 255`
  * **color**[1] (Int) - Green, `0 - 255`
  * **color**[2] (Int) - Blue, `0 - 255`
* **char** (Char) [defualt: `SPACE`] - character to print, mainly used for `fg` rendering
****
#### insertRow(*row, data, offset*)
*Inserts set of characters to specified row*
* **row** (Int) - row to insert data to
* **data** (Str, List or Tuple) - data inserted into desired row
  * (Str) - standard string
  * (List or Tuple) - sequence of characters
* **offset** (Int) [default: `0`] - defines the starting column
****
#### insertCol(*col, data, offset*)
*Inserts set of characters to specified column*
* **col** (Int) - column to insert data to
* **data** (Str, List or Tuple) - data inserted into desired column
  * (Str) - standard string
  * (List or Tuple) - sequence of characters
* **offset** (Int) [default: `0`] - defines the starting row
****
#### getRow(*row*)
*Returns list of characters from specified row*
* **row** (Int) - row to fetch data from
****
#### getCol(*col*)
*Returns list of characters from specified column*
* **col** (Int) - column to fetch data from
****
#### setChar(*col, row, char*)
*Changes character on specified location*
* **col** (Int) - column of character
* **row** (Int) - row of character
* **char** (Char) - replacement character
****
#### getChar(*col, row*)
*Returns character from specified location*
* **col** (Int) - column of character
* **row** (Int) - row of character
