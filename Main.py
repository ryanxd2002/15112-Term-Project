from cmu_112_graphics import *
import math, random, copy, characters
################################################################################

# Make everything in appstarted into the restart button
# # 2. How to make jump


# Take points, make square, check if it is in the square, do this for list

# check center minus radius, x and y

################################################################################
def appStarted(app):
    app.gravity = 0.2
    app.keeptrack = 0
    app.velocityX = 2
    app.velocityY = 0
    app.jumpCounter = 0
    app.gameOver = False
    app.paused = False
    # Coordinates of cube
    app.cube = [app.width // 2 + app.height // 20, 
                  2 * app.height // 3 + app.height // 20, 
                  app.width // 2 - app.height // 20, 
                  2 * app.height // 3 - app.height // 20]

    app.stateX = "leftx"
    app.stateY = "down"

    app.drones = []
    generateDrone(app)

    # Screen
    app.mode = "home"
    app.modes = ["home", "help", "play", "scores", "gameOver"]

    # points on the terrain
    app.terrain = [(0, 555), (1440, 555)]
    play_generateTerrain(app)

    app.checkPoints = []
    getCheckPoints(app)

    # Check is cube is moving
    app.moving = False

    # Checks total distance moved
    app.distanceMoved = 0
    
    # Checks distance right now
    app.distanceNow = 0

    # Shiters
    app.shifterX = 0
    app.shifterY = 0

    # Timer Delay
    app.timerDelay = 1


################################################################################

# Draws home screen
def home_redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = "black")
    canvas.create_rectangle(app.width // 2 - 175, app.height // 2 + 100, 
                            app.width // 2 + 175, app.height // 2 - 100,

                            outline = "white", width = "5")

    canvas.create_rectangle(app.width // 2 - 150, app.height // 2 + 300, 
                            app.width // 2 + 150, app.height // 2 + 150,

                            outline = "white", width = "5")

    canvas.create_rectangle(app.width // 2 - 150, app.height // 2 - 150, 
                            app.width // 2 + 150, app.height // 2 - 300,

                            outline = "white", width = "5")

    canvas.create_text(app.width // 2, app.height // 2,
                    text = "Play", font = "Arial 100", fill = "white")

    canvas.create_text(app.width // 2, app.height // 2 + 225,
                    text = "Scores", font = "Arial 75", fill = "white")

    canvas.create_text(app.width // 2, app.height // 2 - 225,
                    text = "Help", font = "Arial 75", fill = "white")

def home_mousePressed(app, event):
    if app.width // 2 - 175 <= event.x <= app.width // 2 + 175:
        if app.height // 2 - 100 <= event.y <= app.height // 2 + 100:
            app.mode = "play"

    if app.width // 2 - 150 <= event.x <= app.width // 2 + 150:
        if app.height // 2 + 150 <= event.y <= app.height // 2 + 300:
            app.mode = "scores"

    if app.width // 2 - 150 <= event.x <= app.width // 2 + 150:
        if app.height // 2 - 300 <= event.y <= app.height // 2 - 150:
            app.mode = "help"

def home_keyPressed(app, event):
    if event.key == "e":
        app.mode = "gameOver"
################################################################################

# Draws help screen
def help_redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = "black")
    canvas.create_text(app.width // 2, 100,
                    text = "Press left, right, up, and down arrow keys to move",         
                                      font = "Arial 50", fill = "white")
    canvas.create_line(0, 200, app.width, 200, fill = "white", width = 10)
    canvas.create_text(app.width // 2, 300,
                    text = "Avoid enemies and get the highest score possible!",         
                                      font = "Arial 50", fill = "white")
    canvas.create_line(0, 400, app.width, 400, fill = "white", width = 10)

    canvas.create_text(app.width // 2, 500,
                    text = "Good Luck...",         
                                      font = "Arial 50", fill = "white")
    canvas.create_line(0, 600, app.width, 600, fill = "white", width = 10)

    canvas.create_text(app.width // 2, 700,
                    text = "Press esc to return to main screen",         
                                      font = "Arial 20", fill = "white")

def help_keyPressed(app, event):
    
    # Return to home screen
    if event.key == "Escape":
        app.mode = "home"

################################################################################

# Draws high score
def scores_redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = "black")
    canvas.create_text(app.width // 2, 150,
                    text = "HIGH SCORE ",         
                                      font = "Arial 200", fill = "white")

    canvas.create_rectangle(50, 300, 
                            1390, 700,

                            outline = "white", width = "5")

def scores_keyPressed(app, event):

    # Returns home
    if event.key == "Escape":
        app.mode = "home"

################################################################################

def gameOver_redrawAll(app, canvas):
        canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
        canvas.create_text(app.width // 2, 200,
                    text = "Game Over ",         
                                      font = "Arial 200", fill = "white")

        canvas.create_text(app.width // 2, 500,
                    text = f"Score: {app.distanceNow}",         
                                      font = "Arial 200", fill = "white")

def gameOver_keyPressed(app, event):
    if event.key == "h":
        app.mode = "home"


################################################################################
def getCheckPoints(app):
    for i in range(0, len(app.terrain), 2):
        app.checkPoints.append(app.terrain[i])


def play_drawCube(app, canvas):
    
    # Draws cube
    canvas.create_rectangle(app.cube[0], app.cube[1], app.cube[2], app.cube[3], 
                        fill = "blue", outline = "blue")

def play_keyPressed(app, event):
    if app.gameOver == False:
        
        # Left, Right, Up, Down
        if event.key == "Left":
            if app.distanceNow > 0:
                app.stateX = "left"
        
        elif event.key == "Right":
            app.stateX = "right"
           

        elif event.key == "Up":
            print(play_isAbove(app)[1][1]+app.shifterY-2, 2 * app.height // 3 + app.height // 20)
            if play_isAbove(app)[1][1]+app.shifterY-6 < 2 * app.height // 3 + app.height // 20:
            
                app.velocityY = -10
            
            # Fuck

        elif event.key == "Down":
            app.stateY = "down"

        elif event.key == "p":
            app.paused = not app.paused
        
        elif event.key == "r":
            appStarted(app)

        elif event.key == "Escape":
            app.mode = "home"

            # Reset all values
            app.gameOver = False
            app.paused = False
            app.cube = [app.width // 2 + app.height // 20, 
                        2 * app.height // 3 + app.height // 20, 
                        app.width // 2 - app.height // 20, 
                        2 * app.height // 3 - app.height // 20]
            app.terrain = [(0, 551), (1440, 551)]
            app.moving = False

            app.distanceMoved = 0
            
            app.distanceNow = 0

            app.shifterX = 0
            app.shifterY = 0

    elif event.key == "r":
        appStarted(app)

    elif event.key == "h":
        app.mode = "home"

def play_mousePressed(app, event):
    if event.x <= app.width // 2:
        play_moveLeft(app)

    if event.x > app.width // 2:
        play_moveRight(app)


def play_mouseDragged(app, event):
    if event.x <= app.width // 2:
        play_moveLeft(app)

    if event.x > app.width // 2:
        play_moveRight(app)   


'''
THIS IS THE IS ABOVE FUNCTION
'''

def play_isAbove(app):
    
    # Check if the block is above everything
    
    

    for i in range(0, len(app.terrain) - 1):
        if ((app.width // 2 - app.height // 20) < (app.terrain[i][0] + app.shifterX)):
            point = app.terrain[i]
            break


    if point[1] + app.shifterY < 2 * app.height // 3 + app.height // 20:
                return [False]

    return [True, point]
#####




def play_isLegal(app):
    # point1, point2 = findBlockItIsOn(app)
    return play_isAbove(app)[0]


# Functions to move the pieces 
def play_moveLeft(app):
    app.shifterX += app.velocityX
    app.distanceNow -= app.velocityX
    
    if not play_isLegal(app):
        app.shifterX -= app.velocityX
        app.distanceNow += app.velocityX

def play_moveRight(app):
    app.shifterX -= app.velocityX
    app.distanceMoved += app.velocityX
    app.distanceNow += app.velocityX
    
    if not play_isLegal(app):
        app.shifterX += app.velocityX
        app.distanceMoved -= app.velocityX
        app.distanceNow -= app.velocityX

def play_moveUp(app):
    app.shifterY += app.velocityY
    
    if not play_isLegal(app):
        app.shifterY -= app.velocityY

def play_moveDown(app):
    app.shifterY -= app.velocityY

    
    if not play_isLegal(app):
        app.shifterY += app.velocityY
        

def play_jump(app):
    app.shifterY += 200
    
    if not play_isLegal(app):
        app.shifterY -= 200


def play_timerFired(app):
    if app.velocityY <3:
        app.velocityY += app.gravity
    if app.stateX == "right":
        play_moveRight(app)

    elif app.stateX == "left":
        if app.distanceNow > 0:

            play_moveLeft(app)


    
    if app.stateY == "up":
        play_moveUp(app)

    elif app.stateY == "down":
        play_moveDown(app)

    


def generateDrone(app):
    
    for i in range(100, 100000, 1000):

        x = characters.Drone(i, i + 1000)
        app.drones.append(x)

    app.drones.pop(0)
    app.drones.pop(1)

def drawDrone(app, canvas):
    
    for aDrone in app.drones:
        if aDrone == None:
            continue
        for i in range(len(app.terrain)):
            point = None
            if aDrone.spawn < app.terrain[i][0]:
                point = app.terrain[i]
                break

            
        if point == None: 
                continue

        canvas.create_rectangle(aDrone.body[0] + app.shifterX, point[1] - 450+ app.shifterY, 
                                    aDrone.body[2]+ app.shifterX, point[1] -550  + app.shifterY , 
                                    fill = "black", outline = "black")

        canvas.create_oval(aDrone.eye[0] + app.shifterX, point[1] - 450+ app.shifterY , 
                                    aDrone.eye[2]+ app.shifterX, point[1] -550  + app.shifterY, 
                                    fill = "white", outline = "black")

        canvas.create_oval(aDrone.pupil[0] + app.shifterX, point[1] -450+ app.shifterY, 
                                    aDrone.pupil[2]+ app.shifterX, point[1] -500  + app.shifterY, 
                                    fill = "black", outline = "white")



def play_generateTerrain(app):
    while len(app.terrain) <= 50:
        # Take the points we just had
        oldX = app.terrain[-1][0]
        oldY = app.terrain[-1][1]

        # Choose a random number to change x by
        dx = random.randint(100, 200)

        # Get the cube height
        cubeHeight = app.height // 10

        # Get list of possible change in y
        dyList = [cubeHeight, 1.5 * cubeHeight, 
                2 * cubeHeight, 2.5 * cubeHeight,
                3 * cubeHeight, 3.5 * cubeHeight, 4 * cubeHeight]

        # Choose y 
        i = random.randint(0, 6)
        dy = dyList[i]

        # Establish new x coord
        newX = int(oldX + dx)

        # Decide whether the next point will be up or down
        direction = 0
        if i in [0,1,2,3]:
            x = random.randint(0,2)
            if x == 0:
                direction = 1
            if x == 1 or x == 2:
                direction = -1
        
        # Get new y coord
        newY  = int(oldY + direction * dy)
        
        # Get the two new points to make a line
        newPoint1 = (oldX, newY)
        newPoint2 = (newX, newY)

        # Add points to terrain
        app.terrain.append(newPoint1)
        app.terrain.append(newPoint2)



    while 50 < len(app.terrain) <= 100:
        # Take the points we just had
        oldX = app.terrain[-1][0]
        oldY = app.terrain[-1][1]

        # Choose a random number to change x by
        dx = random.randint(150, 250)

        # Get the cube height
        cubeHeight = app.height // 10

        # Get list of possible change in y
        dyList = [cubeHeight, 1.5 * cubeHeight, 
                2 * cubeHeight, 2.5 * cubeHeight,
                3 * cubeHeight, 3.5 * cubeHeight, 4 * cubeHeight]

        # Choose y 
        i = random.randint(0, 6)
        dy = dyList[i]

        # Establish new x coord
        newX = int(oldX + dx)

        # Decide whether the next point will be up or down
        direction = 0
        if i in [0,1,2,3]:
            x = random.randint(0,1)
            if x == 0:
                direction = 1
            if x == 1:
                direction = -1
        
        # Get new y coord
        newY  = int(oldY + direction * dy)
        
        # Get the two new points to make a line
        newPoint1 = (oldX, newY)
        newPoint2 = (newX, newY)

        # Add points to terrain
        app.terrain.append(newPoint1)
        app.terrain.append(newPoint2)

    while 100 < len(app.terrain) <= 150:
        # Take the points we just had
        oldX = app.terrain[-1][0]
        oldY = app.terrain[-1][1]

        # Choose a random number to change x by
        dx = random.randint(200, 300)

        # Get the cube height
        cubeHeight = app.height // 10

        # Get list of possible change in y
        dyList = [cubeHeight, 1.5 * cubeHeight, 
                2 * cubeHeight, 2.5 * cubeHeight,
                3 * cubeHeight, 3.5 * cubeHeight, 4 * cubeHeight]

        # Choose y 
        i = random.randint(0, 6)
        dy = dyList[i]

        # Establish new x coord
        newX = int(oldX + dx)

        # Decide whether the next point will be up or down
        direction = 0
        if i in [0,1,2,3]:
            x = random.randint(0,4)
            if x == 0 or x == 1 or x == 2:
                direction = 1
            if x == 3 or x == 4:
                direction = -1
        
        # Get new y coord
        newY  = int(oldY + direction * dy)
        
        # Get the two new points to make a line
        newPoint1 = (oldX, newY)
        newPoint2 = (newX, newY)

        # Add points to terrain
        app.terrain.append(newPoint1)
        app.terrain.append(newPoint2)



    while 150 < len(app.terrain) <= 200:
        # Take the points we just had
        oldX = app.terrain[-1][0]
        oldY = app.terrain[-1][1]

        # Choose a random number to change x by
        dx = random.randint(300, 400)

        # Get the cube height
        cubeHeight = app.height // 10

        # Get list of possible change in y
        dyList = [cubeHeight, 1.5 * cubeHeight, 
                2 * cubeHeight, 2.5 * cubeHeight,
                3 * cubeHeight, 3.5 * cubeHeight, 4 * cubeHeight]

        # Choose y 
        i = random.randint(0, 6)
        dy = dyList[i]

        # Establish new x coord
        newX = int(oldX + dx)

        # Decide whether the next point will be up or down
        direction = 0
        if i in [0,1,2,3]:
            x = random.randint(0,3)
            if x == 0 or x == 1 or x == 2:
                direction = 1
            if x == 3:
                direction = -1
        
        # Get new y coord
        newY  = int(oldY + direction * dy)
        
        # Get the two new points to make a line
        newPoint1 = (oldX, newY)
        newPoint2 = (newX, newY)

        # Add points to terrain
        app.terrain.append(newPoint1)
        app.terrain.append(newPoint2)







# Draw the terrain
def play_drawTerrain(app, canvas):


    for i in range(len(app.terrain) - 1):
        canvas.create_rectangle(app.terrain[i][0] + app.shifterX, 
                           app.terrain[i][1] + app.shifterY, 
                           app.terrain[i + 1][0] + app.shifterX, 
                           app.height, 
                           fill = "black", outline = "black")

def play_redrawAll(app, canvas):

    
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "grey35")
    # Draws cube
    play_drawCube(app, canvas)

    # Draws terrain
    play_drawTerrain(app, canvas)
    canvas.create_text(app.width // 2, 20, 
                       text = f"Score: {app.distanceNow // 10}", 
                       fill = "black", font = "Arial 30" )

    drawDrone(app, canvas)


    # Create pointless terrain to the left of x = 0
    canvas.create_rectangle(-100000, app.height, 0, 555, fill = "black")
    

runApp(width = 1440, height = 770)




################################################################################
################################################################################
################################################################################
################################################################################

