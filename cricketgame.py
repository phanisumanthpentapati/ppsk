import pygame as py
import random
import cv2

# Initialize video captures
bgv1 = cv2.VideoCapture("data/Untitled video - Made with Clipchamp (online-video-cutter.com).mp4")
bgv2 = cv2.VideoCapture("data/Cricket Video Promo - Ahmad Ejaz (720p, h264, youtube) (online-video-cutter.com).mp4")
bgv3 = cv2.VideoCapture("data/CricketToss Coin Animation Green Green Screen __ rupee Animation __ download transparent GIF + PNG images - Yash Goswami (480p, h264, youtube) (online-video-cutter.com).mp4")
homebgv = cv2.VideoCapture("data/homebgvid.mp4")

def createButton(x, y, wd, ht, txtFont, text, btcolor, tcolor):
    """Draws a button and returns its Rect."""
    Button = py.Rect(x, y, wd, ht)
    py.draw.rect(screen, btcolor, Button, border_radius=25)
    Text = txtFont.render(text, True, tcolor)
    screen.blit(Text, (
        Button.x + (Button.width - Text.get_width()) // 2,
        Button.y + (Button.height - Text.get_height()) // 2
    ))
    return Button

class cricket:
    # Buttons
    start_button = py.Rect(535, 507, 200, 60)
    startbuttoncolor = "red"
    starttextcolor = "white"

    Title_rect = py.Rect(300, 250, 700, 100)
    r = 0
    toss_button_heads = py.Rect(300, 400, 200, 60)
    toss_button_tails = py.Rect(700, 400, 200, 60)
    bat_button = py.Rect(300, 500, 200, 60)
    ball_button = py.Rect(700, 500, 200, 60)
    proceed_button = py.Rect(525, 600, 200, 60)  # Proceed button

    # TEAM buttons
    team_a_rect = py.Rect(245, 500, 200, 60)
    team_b_rect = py.Rect(745, 500, 200, 60)

    # Input box for overs
    input_box = py.Rect(500, 400, 200, 50)
    input_active = False
    input_text = ''

    # TEAM state variables
    team_a_label = "TEAM - A"
    team_b_label = "TEAM - B"
    team_selection_done = False
    selected_team = None
    team_message = ""

py.init()

# Screen setup
screen = py.display.set_mode((1300, 750))
py.display.set_caption("Cricket Simulator")

# Load and scale images
bgimg = py.image.load('data/imagebg.jpg')
imgwd, imght = screen.get_size()
bgimg = py.transform.scale(bgimg, (imgwd, imght))
homebgimg = py.image.load("data/wickets images.jpg")
homebgimg = py.transform.scale(homebgimg, (imgwd, imght))

# Load and scale game sprites
batsman = py.image.load("data/batsman-removebg-preview.png")
batsman = py.transform.scale(batsman, (70, 90))

bowler = py.image.load("data/bowler-removebg-preview.png")
bowler = py.transform.scale(bowler, (65, 80))
bowler = py.transform.scale(bowler, (75, 90))
ball = py.image.load("data/cricket-ball-vector-illustration-removebg-preview.png")
ball = py.transform.scale(ball, (10, 10))

# Fonts
startfont = py.font.SysFont("Comic Sans MS", 50)
smallfont = py.font.SysFont("Comic Sans MS", 30)

# Ball movement variables
ht = 370
wd = 645

# Game state flags
ball_click = False
toss_result = None
toss_winner = None
team_choice = None
overs_choice = None
overs_played = 0

# Functions for game mechanics
def ballgo(ht):
    return ht - 0.5 if ht > 300 else ht

def ballhit(wd):
    return wd - 0.5 if wd > 100 else wd

def titleFunc():
    """Displays the game title with changing colors and the START button."""
    py.time.wait(10)
    colors = ["red", "green", "violet", "pink", "yellow", "blue", "black", "orange", 'white']
    cricket.r = (cricket.r + 1) % len(colors)
    py.draw.rect(screen, "white", cricket.Title_rect, border_radius=10)
    titleText = startfont.render("CRICKET SIMULATOR", True, colors[cricket.r])
    screen.blit(titleText, (370, 260))
    py.draw.rect(screen, cricket.startbuttoncolor, cricket.start_button, border_radius=20)
    startText = startfont.render("START", True, cricket.starttextcolor)
    screen.blit(startText, (
        cricket.start_button.x + (cricket.start_button.width - startText.get_width()) // 2,
        cricket.start_button.y + (cricket.start_button.height - startText.get_height()) // 2
    ))

def tossFunc():
    """Displays the HEADS and TAILS buttons for the toss."""
    py.draw.rect(screen, "white", cricket.toss_button_heads, border_radius=10)
    headsText = smallfont.render("HEADS", True, "black")
    screen.blit(headsText, (360,415))
        
    
    
    py.draw.rect(screen, "white", cricket.toss_button_tails, border_radius=10)
    tailsText = smallfont.render("TAILS", True, "black")
    screen.blit(tailsText, (760,415))
       
    

def batOrBallFunc():
    """Displays the BAT and BOWL buttons for team decision."""
    py.draw.rect(screen, "white", cricket.bat_button, border_radius=10)
    batText = smallfont.render("BAT", True, "black")
    screen.blit(batText, (360,515))
        
    
    
    py.draw.rect(screen, "white", cricket.ball_button, border_radius=10)
    ballText = smallfont.render("BOWL", True, "black")
    screen.blit(ballText, (760,515))
       
    

def proceedFunc():
    """Displays the PROCEED button after team selection."""
    createButton(
        cricket.proceed_button.x,
        cricket.proceed_button.y,
        cricket.proceed_button.width,
        cricket.proceed_button.height,
        smallfont,
        "PROCEED",
        "green",
        "white"
    )

       
       
    

def drawOversInput():
    """Displays the input box for entering the number of overs."""
    py.draw.rect(screen, "white", cricket.input_box, border_radius=10)
    oversText = smallfont.render(cricket.input_text, True, "black")
    screen.blit(oversText, (cricket.input_box.x + 10, cricket.input_box.y + 10))

    instruction_text = smallfont.render("Enter the number of overs:", True, "black")
    screen.blit(instruction_text, (480, 350))

def backgroundVideo1():
    """Plays the first background video."""
    py.time.wait(10)
    val, frame = bgv1.read()
    if not val:
        bgv1.set(cv2.CAP_PROP_POS_FRAMES, 0) 
        val, frame = bgv1.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (1300, 750))
    frame = py.surfarray.make_surface(frame.swapaxes(0, 1))
    screen.blit(frame, (0, 0))

def backgroundVideo2():
    """Plays the second background video."""
    py.time.wait(20)
    val, frame = bgv2.read()
    if not val:
        bgv2.set(cv2.CAP_PROP_POS_FRAMES, 0) 
        val, frame = bgv2.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (1300, 750))
    frame = py.surfarray.make_surface(frame.swapaxes(0, 1))
    screen.blit(frame, (0, 0))
    
def backgroundVideo3():
    """Plays the second background video."""
    py.time.wait(20)
    val, frame = bgv3.read()
    if not val:
        bgv2.set(cv2.CAP_PROP_POS_FRAMES, 0) 
        val, frame = bgv2.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (1300, 750))
    frame = py.surfarray.make_surface(frame.swapaxes(0, 1))
    screen.blit(frame, (0, 0))
    

def homebgvideo():
    """Plays the home background video."""
    val, frame = homebgv.read()
    if not val:
        homebgv.set(cv2.CAP_PROP_POS_FRAMES, 0)
        val, frame = homebgv.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (1300, 750))
    frame = py.surfarray.make_surface(frame.swapaxes(0, 1))
    screen.blit(frame, (0, 0)) 

# Define game states
HOME = 0
TEAM = 1
TOSS = 2
DECISION = 3
OVER_INPUT = 4
GAME = 5
state = HOME
wickets=0
over=0
score=0
ball_hit = False
# Main game loop
running = True
while running:
    # Event handling
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
            break

        if state == HOME:
            if event.type == py.MOUSEBUTTONDOWN:
                if cricket.start_button.collidepoint(event.pos):
                    state = TEAM

        elif state == TEAM:
            if not cricket.team_selection_done:
                if event.type == py.MOUSEBUTTONDOWN:
                    if cricket.team_a_rect.collidepoint(event.pos):
                        # User selected Team A
                        cricket.selected_team = "A"
                        cricket.team_selection_done = True
                        cricket.team_a_label = "HEAD"
                        cricket.team_b_label = "TAIL"
                        cricket.team_message = "TEAM A predicted HEAD"
                    elif cricket.team_b_rect.collidepoint(event.pos):
                        # User selected Team B
                        cricket.selected_team = "B"
                        cricket.team_selection_done = True
                        cricket.team_a_label = "TAIL"
                        cricket.team_b_label = "HEAD"
                        cricket.team_message = "TEAM B predicted HEAD"
            else:
                if event.type == py.MOUSEBUTTONDOWN:
                    if cricket.proceed_button.collidepoint(event.pos):
                        state = GAME

        elif state == TOSS:
            backgroundVideo3()
            tossFunc()
            if event.type == py.MOUSEBUTTONDOWN:
                if cricket.toss_button_heads.collidepoint(event.pos):
                    toss_result = "HEAD"
                    if toss_result == "HEAD":
                          toss_winner = f"Team {'A' if cricket.selected_team == 'A' else 'B'}"
                    else:
                         toss_winner = f"Team {'B' if cricket.selected_team == 'A' else 'A'}"
                         state = DECISION
                         
                if cricket.toss_button_tails.collidepoint(event.pos):
                    toss_result = "HEAD"
                    if toss_result == "HEAD":
                          toss_winner = f"Team {'A' if cricket.selected_team == 'A' else 'B'}"
                    else:
                         toss_winner = f"Team {'B' if cricket.selected_team == 'A' else 'A'}"
                         state = DECISION

        '''elif state == DECISION:
            if event.type == py.MOUSEBUTTONDOWN:
                if toss_winner == "Team A":
                    if cricket.bat_button.collidepoint(event.pos):
                        team_choice = "Team A chose to bat"
                        state = OVER_INPUT
                    elif cricket.ball_button.collidepoint(event.pos):
                        team_choice = "Team A chose to bowl"
                        state = OVER_INPUT
                elif toss_winner == "Team B":
                    if cricket.bat_button.collidepoint(event.pos):
                        team_choice = "Team B chose to bat"
                        state = OVER_INPUT
                    elif cricket.ball_button.collidepoint(event.pos):
                        team_choice = "Team B chose to bowl"
                        state = OVER_INPUT

        if state == OVER_INPUT:
            if event.type == py.MOUSEBUTTONDOWN:
                if cricket.input_box.collidepoint(event.pos):
                    cricket.input_active = True
                else:
                    cricket.input_active = False

            if event.type == py.KEYDOWN:
                if cricket.input_active:
                    if event.key == py.K_RETURN:
                        try:
                            overs_choice = int(cricket.input_text)
                            state = GAME
                        except ValueError:
                            cricket.input_text = ''  # Reset input on invalid entry
                    elif event.key == py.K_BACKSPACE:
                        cricket.input_text = cricket.input_text[:-1]
                    else:
                        # Allow only digit inputs
                        if event.unicode.isdigit():
                            cricket.input_text += event.unicode'''

        if state == GAME:
            if event.type == py.KEYDOWN:
                if event.key == py.K_RETURN:
                    ball_click = True
                    wd = 645
                    ht = 370
            if event.type == py.K_LSHIFT:
                    ball_hit = True
            else:
                ball_click = False

    # Drawing based on the current state
    if state == HOME:
        homebgvideo()
        titleFunc()

    elif state == TEAM:
        backgroundVideo2()
        if not cricket.team_selection_done:
            # Draw Team A and Team B buttons
            createButton(245,500,200,60,smallfont,cricket.team_a_label, "red", "white") 
            createButton(745,500,200,60,smallfont, cricket.team_b_label, "red", "white")
        else:
            # Draw updated buttons
            createButton(
                cricket.team_a_rect.x, cricket.team_a_rect.y,
                cricket.team_a_rect.width, cricket.team_a_rect.height,
                smallfont, cricket.team_a_label, "red", "white"
            )
            createButton(
                cricket.team_b_rect.x, cricket.team_b_rect.y,
                cricket.team_b_rect.width, cricket.team_b_rect.height,
                smallfont, cricket.team_b_label, "red", "white"
            )
            # Display the prediction message
            message_text = smallfont.render(cricket.team_message, True, "black")
            screen.blit(message_text, (
                cricket.team_a_rect.x,
                cricket.team_a_rect.y + cricket.team_a_rect.height + 10
            ))
            # Draw the PROCEED button
            proceed_button_rect = createButton(
                cricket.proceed_button.x, cricket.proceed_button.y,
                cricket.proceed_button.width, cricket.proceed_button.height,
                smallfont, "PROCEED", "green", "white"
            )

    elif state == TOSS:
        backgroundVideo1()
        tossFunc()

    elif state == DECISION:
        screen.fill("lightblue")
        decision_text = f"{toss_winner} won the toss"
        decision_render = smallfont.render(decision_text, True, "black")
        screen.blit(decision_render, (400, 350))
        batOrBallFunc()

    elif state == OVER_INPUT:
        screen.fill("lightyellow")
        drawOversInput()

    elif state == GAME:
        screen.blit(bgimg, (0, 0))
        screen.blit(batsman, (615, 265))
        screen.blit(bowler, (615, 360))
        if ball_click:
            ht = ballgo(ht)
            if ht <= 300:
                wd = ballhit(wd)
            if ball_hit:
                screen.blit(ball, (wd, ht))
        screen.blit(batsman, (80, 290))

        # Display overs and team choice
        overs_text = smallfont.render(f"Overs: {overs_choice}", True, "black")
        screen.blit(overs_text, (50, 50))

        team_choice_text = smallfont.render(f"{team_choice}", True, "black")
        screen.blit(team_choice_text, (50, 100))
   
    py.display.update()

py.quit()


