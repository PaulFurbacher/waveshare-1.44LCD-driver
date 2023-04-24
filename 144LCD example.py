from waveshare144LCD import LCD_1inch44
from machine import Pin

def draw_shapes():

    LCD.fill(LCD.BLACK)

    #draw some labels and boxes beside the buttons
    LCD.fill_rect(15,40,75,12,LCD.YELLOW)
    LCD.rect(15,40,75,12,LCD.YELLOW)
    LCD.text("1in44-LCD",17,42,LCD.BLUE)
    
    LCD.fill_rect(15,60,75,12,LCD.BLUE)
    LCD.rect(15,60,75,12,LCD.BLUE)
    LCD.text("128x128Px ",17,62,LCD.WHITE)
    
    LCD.fill_rect(15,80,75,12,LCD.GREEN)
    LCD.rect(15,80,75,12,LCD.GREEN)
    LCD.text("ST7735S",17,82,LCD.RED)

    LCD.hline(5,5,120,LCD.GBLUE)
    LCD.hline(5,125,120,LCD.GBLUE)
    LCD.vline(5,5,120,LCD.GBLUE)
    LCD.vline(125,5,120,LCD.GBLUE)

if __name__=='__main__':

    LCD = LCD_1inch44()

    #MAXIMUM BRIGHTNESS
    LCD.set_brightness(100)
    
    draw_shapes()
    
    LCD.show()
   
    key0 = Pin(15,Pin.IN,Pin.PULL_UP) 
    key1 = Pin(17,Pin.IN,Pin.PULL_UP)
    key2 = Pin(2 ,Pin.IN,Pin.PULL_UP)
    key3 = Pin(3 ,Pin.IN,Pin.PULL_UP)
   
    looping=True

    #Loop until you press button 3 on the LCD
    while(looping):  

        draw_shapes()

        if(key0.value() == 0):
            LCD.fill_rect(100,100,20,20,LCD.GBLUE)
            LCD.write_text("HELLO",12,102,2,LCD.PURPLE)
        else :
            LCD.fill_rect(100,100,20,20,LCD.BLACK)
            LCD.rect(100,100,20,20,LCD.GBLUE)
            
        if(key1.value() == 0):
            LCD.fill_rect(100,70,20,20,LCD.GBLUE)
            LCD.rect(15,10,75,20,LCD.GBLUE)
            text = 'Lorem Ipsum'
            LCD.text_wrap(text,16,12,LCD.colour(255,0,0),75,20)
        else :
            LCD.fill_rect(100,70,20,20,LCD.BLACK)
            LCD.rect(100,70,20,20,LCD.GBLUE)
            
        if(key2.value() == 0):
            LCD.fill_rect(100,40,20,20,LCD.GBLUE)
        else :
            LCD.fill_rect(100,40,20,20,LCD.BLACK)
            LCD.rect(100,40,20,20,LCD.GBLUE)
        if(key3.value() == 0):
            looping=False
            LCD.fill_rect(100,10,20,20,LCD.GBLUE)  
        else :
            LCD.fill_rect(100,10,20,20,LCD.RED)
            LCD.rect(100,10,20,20,LCD.GBLUE) 
                      
        LCD.show()

    LCD.fill(0xFFFF)
    LCD.show()
    print("Script done")