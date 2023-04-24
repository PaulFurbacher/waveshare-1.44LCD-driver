
from machine import Pin,SPI,PWM
import framebuf

#Pin assignments for the Pico W
BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10    
CS = 9

class LCD_1inch44(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 128
        self.height = 128
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs.on()
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc.on()
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()

        self.pwm = PWM(Pin(BL))
        self.pwm.freq(1000)
        self.set_brightness(75)

        self.WHITE  =   self.colour(255,255,255)
        self.BLACK  =  self.colour(0,0,0)
        self.GREEN  =  self.colour(0,255,0)
        self.RED    =  self.colour(255,0,0)
        self.BLUE   = self.colour(0,0,255)
        self.GBLUE = self.colour(0,255,255)
        self.YELLOW = self.colour(255,255,0)
        self.PURPLE = self.colour(255,0,255)    

    def set_brightness(self, percent): #controls the brightness for the LCD. Takes an integer value for % of the backlight brightness.
        if percent < 0 or percent > 100:
            raise ValueError()
        
        pwmValue = int((percent / 100) * 65535)
        self.pwm.duty_u16(pwmValue)

    def colour(self,R,G,B) -> int: # Convert RGB888 to RGB565. Each of R,G,B is an int from 0 to 255 representing intensity of each.
        return (((G&0b00011100)<<3) +((R&0b11111000)>>3)<<8) + (B&0b11111000)+((G&0b11100000)>>5)

    def write_cmd(self, cmd):    
        self.cs.on()
        self.dc.off()
        self.cs.off()
        self.spi.write(bytearray([cmd]))
        self.cs.on()

    def write_data(self, buf):
        self.cs.on()
        self.dc.on()
        self.cs.off()
        self.spi.write(bytearray([buf]))
        self.cs.on()

    def init_display(self):
        """Initialize display"""  
        self.rst.on()
        self.rst.off()
        self.rst.on()
        
        self.write_cmd(0x36)
        self.write_data(0x70)
        
        self.write_cmd(0x3A)
        self.write_data(0x05)

         #ST7735R Frame Rate
        self.write_cmd(0xB1)
        self.write_data(0x01)
        self.write_data(0x2C)
        self.write_data(0x2D)

        self.write_cmd(0xB2)
        self.write_data(0x01)
        self.write_data(0x2C)
        self.write_data(0x2D)

        self.write_cmd(0xB3)
        self.write_data(0x01)
        self.write_data(0x2C)
        self.write_data(0x2D)
        self.write_data(0x01)
        self.write_data(0x2C)
        self.write_data(0x2D)

        self.write_cmd(0xB4) #Column inversion
        self.write_data(0x07)

        #ST7735R Power Sequence
        self.write_cmd(0xC0)
        self.write_data(0xA2)
        self.write_data(0x02)
        self.write_data(0x84)
        self.write_cmd(0xC1)
        self.write_data(0xC5)

        self.write_cmd(0xC2)
        self.write_data(0x0A)
        self.write_data(0x00)

        self.write_cmd(0xC3)
        self.write_data(0x8A)
        self.write_data(0x2A)
        self.write_cmd(0xC4)
        self.write_data(0x8A)
        self.write_data(0xEE)

        self.write_cmd(0xC5) #VCOM
        self.write_data(0x0E)

        #ST7735R Gamma Sequence
        self.write_cmd(0xe0)
        self.write_data(0x0f)
        self.write_data(0x1a)
        self.write_data(0x0f)
        self.write_data(0x18)
        self.write_data(0x2f)
        self.write_data(0x28)
        self.write_data(0x20)
        self.write_data(0x22)
        self.write_data(0x1f)
        self.write_data(0x1b)
        self.write_data(0x23)
        self.write_data(0x37)
        self.write_data(0x00)
        self.write_data(0x07)
        self.write_data(0x02)
        self.write_data(0x10)

        self.write_cmd(0xe1)
        self.write_data(0x0f)
        self.write_data(0x1b)
        self.write_data(0x0f)
        self.write_data(0x17)
        self.write_data(0x33)
        self.write_data(0x2c)
        self.write_data(0x29)
        self.write_data(0x2e)
        self.write_data(0x30)
        self.write_data(0x30)
        self.write_data(0x39)
        self.write_data(0x3f)
        self.write_data(0x00)
        self.write_data(0x07)
        self.write_data(0x03)
        self.write_data(0x10)

        self.write_cmd(0xF0) #Enable test command
        self.write_data(0x01)

        self.write_cmd(0xF6) #Disable ram power save mode
        self.write_data(0x00)
            #sleep out
        self.write_cmd(0x11)
        #Turn on the LCD display
        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x00)
        self.write_data(0x80)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x02)
        self.write_data(0x00)
        self.write_data(0x82)
        
        self.write_cmd(0x2C)
        
        self.cs.on()
        self.dc.on()
        self.cs.off()
        self.spi.write(self.buffer)
        self.cs.on()
    
    def text_wrap(self,str,x,y,color,w,h): #Wraps colored text within a box starting at x,y with width w and height h. Only for default framebuf text size
        cols = w // 8
        # for each row
        j = 0
        for i in range(0, len(str), cols):
            # draw as many chars fit on the line
            self.text(str[i:i+cols], x, y + j, color)
            j += 8
            # dont overflow text outside the box
            if j >= h:
                break
    
    def write_text(self,text,x,y,size,color): #write text of different sizes to the display. Size is a direct multiplier.
        ''' Method to write Text on OLED/LCD Displays
            with a variable font size
            Args:
                text: the string of chars to be displayed
                x: x co-ordinate of starting position
                y: y co-ordinate of starting position
                size: font size of text
                color: color of text to be displayed
        '''
        background = self.pixel(x,y)
        info = []
        # Creating reference charaters to read their values
        self.text(text,x,y,color)
        for i in range(x,x+(8*len(text))):
            for j in range(y,y+8):
                # Fetching and saving details of pixels, such as
                # x co-ordinate, y co-ordinate, and color of the pixel
                px_color = self.pixel(i,j)
                info.append((i,j,px_color)) if px_color == color else None
        # Clearing the reference characters from the screen
        self.text(text,x,y,background) # type: ignore
        # Writing the custom-sized font characters on screen
        for px_info in info:
            self.fill_rect(size*px_info[0] - (size-1)*x , size*px_info[1] - (size-1)*y, size, size, px_info[2])