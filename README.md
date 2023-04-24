# waveshare-1.44LCD-driver
A micropython driver for the Waveshare 1.44" LCD. Default pin assignments are for the Pico W.

## Purpose
I got the waveshare 1.44" LCD and went through the process of getting it to work properly, which was non-trivial. The [driver and documentation](https://www.waveshare.com/wiki/Pico-LCD-1.44) supplied by Waveshare needed quite a bit of tweaking, which I wanted to share to save others the trouble. 

## Changes from the original driver
- Added a few helper methods that I found useful
- Created a function to change backlight brightness. Starts at 75% by default.
- Corrected small errors in the original driver 
    - changed setting pins via Pin(0) and Pin(1) to Pin.off() and Pin.on()
    - removed semicolons
- Added purple to the color constants
- Corrected the color constant for yellow

## Usage
Just initialize the object and use as if it were a framebuf class.

This will turn the screen blue.
`from waveshare144LCD import LCD_1inch44

LCD = LCD_1inch44()
LCD.fill(LCD.BLUE)
LCD.show()`

## Functions

### set_brightness(percent)
Sets the backlight intensity as a % of maximum. Argument is an integer 0-100.

### colour(R,G,B)
Use this to create custom colors for the screen. Each of R, G, B is an integer from 0-255. The function will return an integer that you can pass to other framebuf type functions that need a color. 

The 1.44" LCD uses an annoying RGB 565 format in which the bits are arranged GGGRRRRRBBBBBGGG. This function lets you choose colors for it in a sane manner.

This function is taken from [this excellent blog post](https://thepihut.com/blogs/raspberry-pi-tutorials/coding-colour-with-micropython-on-raspberry-pi-pico-displays). That blog post also has a really neat method of debugging color encoding if you don't know how color bits are arranged for other displays.

### text_wrap(str,x,y,color,w,h,border=None)
Framebuffer's text function has no line wrapping. This will wrap the string str within a box starting at x,y of width w and height h. You set the text color using the color argument. If you set border, you'll get a rectangle drawn around the box that you are wrapping the words within.

This will only output text of the default framebuf size.

Function taken from [this post](https://forum.micropython.org/viewtopic.php?t=4434).

### write_text(text,x,y,size,color)

Write text to the LCD at point x,y, but multiplied by size to make it larger. E.g. setting size to 2 will double the default famebuf text size. 

Taken from [this work](https://github.com/dhargopala/pico-custom-font).
