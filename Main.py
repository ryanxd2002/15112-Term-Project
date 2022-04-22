from cmu_112_graphics import *
import math, random, copy, characters, seperation
################################################################################
################################################################################

def appStarted(app):

    app.cubeColor = "blue"

    ########################################
    # Generate the game and its attributes #
    ########################################

    app.terrain = [(0, 555), (1440, 555)]
    play_generateTerrain(app)

    app.drones = []
    generateDrone(app)
    
    app.isSeen = False

    app.spikes = []
    play_generateSpikes(app)

    app.turtles = []
    play_generateTurtles(app)

    app.turtleDX = 2

    app.crushers = []
    play_generateCrushers(app)

    # Coordinates of cube
    app.cube = [app.width // 2 + 30, 
                  2 * app.height // 3 + 30, 
                  app.width // 2 - 30, 
                  2 * app.height // 3 - 30]

    

    # Velocities and other shifters
    app.gravity = 0.2
    app.velocityX = 3
    app.velocityY = 0
    app.droneShifter = -1
    app.droneDX = 1
    app.turtleDX = 1

    app.gameOver = False
    app.paused = False
    app.helpMode = False
    app.showHelp = True


    # Set high score 
    app.highScore = int(seperation.readFile("score.txt"))

    app.stateX = "left"
    app.stateY = "down"

    # Screen
    app.mode = "home"
    app.modes = ["home", "help", "play", "scores", "gameOver"]

    # Checks total distance moved
    app.distanceMoved = 0
    
    # Checks distance right now
    app.distanceNow = 0

    # Shiters
    app.shifterX = 0
    app.shifterY = 0
    app.hidden = False

    # Timer Delay
    app.timerDelay = 1

    app.shots = []

################################################################################

# Draws home screen
def home_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
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

    if app.showHelp == True:

        canvas.create_arc(200, 300, 600, 100, 
                                start = 50, extent = 120, outline = "white",
                                style = ARC, width = 5)

        canvas.create_polygon(530, 100, 520, 150, 550, 130, fill = "white")

        canvas.create_text(200, 225, text = "CLICK HERE!!!", font = "Arial 50", 
                        fill = "white")

def home_mousePressed(app, event):

    # Pressed play button
    if app.width // 2 - 175 <= event.x <= app.width // 2 + 175:
        if app.height // 2 - 100 <= event.y <= app.height // 2 + 100:
            app.mode = "play"
            app.showHelp = False

    # Pressed scores button
    if app.width // 2 - 150 <= event.x <= app.width // 2 + 150:
        if app.height // 2 + 150 <= event.y <= app.height // 2 + 300:
            app.mode = "scores"

    # Pressed help button
    if app.width // 2 - 150 <= event.x <= app.width // 2 + 150:
        if app.height // 2 - 300 <= event.y <= app.height // 2 - 150:
            app.mode = "help"
            app.showHelp = False

def home_keyPressed(app, event):
    if event.key == "e":
        app.mode = "gameOver"
################################################################################

# Draws help screen
def help_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")

    canvas.create_text(app.width // 2, 100,
                    text = "Press left, right, up, and down arrow keys to move",         
                                      font = "Arial 50", fill = "white")

    canvas.create_line(0, 200, app.width, 200, fill = "white", width = 10)

    canvas.create_text(app.width // 2, 300,
                    text = "While you can hide in the walls to your right...",         
                                      font = "Arial 50", fill = "white")

    canvas.create_line(0, 400, app.width, 400, fill = "white", width = 10)

    canvas.create_text(app.width // 2, 500,
                    text = "Just don't get stabbed by spikes on your way out!",         
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

# Draws high score screen
def scores_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    canvas.create_text(app.width // 2, 150, 
                       text = f"HIGH SCORE",         
                       font = "Arial 200", fill = "white")

    canvas.create_rectangle(50, 300, 1390, 700,
                            outline = "white", width = "5")

    canvas.create_text(770, 500, text = f"{app.highScore}",
                       fill = "white", font = "Arial 200")

def scores_keyPressed(app, event):

    # Returns home
    if event.key == "Escape":
        app.mode = "home"

################################################################################

# Draws gameover screen
def gameOver_redrawAll(app, canvas):
        canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
        canvas.create_text(app.width // 2, 200, text = "Game Over ",
                           font = "Arial 200", fill = "white")

        canvas.create_text(app.width // 2, 500, 
                           text = f"Score: {app.distanceNow // 10}", 
                           font = "Arial 200", fill = "white")

# Set high score
def gameOver_setHighScore(app):
    app.highScore = seperation.readFile("score.txt")

# Get the high score
def gameOver_getHighScore(app):
        if app.distanceNow // 10 > app.highScore:
            seperation.truncate("score.txt")
            seperation.writeFile("score.txt", f"{app.distanceNow // 10}")

def gameOver_keyPressed(app, event):

    # Return home
    if event.key == "Escape":
       appStarted(app)
       app.showHelp = False

################################################################################

# Draws cube
def play_drawCube(app, canvas):
    
    # Draws cube
    canvas.create_rectangle(app.cube[0], app.cube[1], app.cube[2], app.cube[3], 
                            fill = app.cubeColor, outline = app.cubeColor)

# Tells whether block is hidden
def play_isHidden(app):
    
    point = None
    point1 = None

    # Find point right in front of block
    for i in range(len(app.terrain) - 1):
        if (app.terrain[i][0] + app.shifterX) >= (app.width // 2 - 30):

            # Check if it is a wall or a cliff 
            if app.terrain[i + 1][1] < app.terrain[i][1]:
                point = app.terrain[i]
                point1 = app.terrain[i + 1]
                break

    # Check if hidden
    if ((point[0] + app.shifterX) <= (app.width // 2 - 20) and 
          (2 * app.height // 3 - 30 >= point1[1] + app.shifterY)):
        return True
    
    return False
    
def play_keyPressed(app, event):
    if app.gameOver == False:
        
        # Left, Right
        if event.key == "Left":
            if app.distanceNow > 0:
                app.stateX = "left"
        
        elif event.key == "Right":
            app.stateX = "right"

        # Jump
        elif event.key == "Up":
            if ((play_isAbove(app)[1][1] + app.shifterY - 6) < 
                (2 * app.height // 3 + 30)):
                app.velocityY = -10

        # Pause
        elif event.key == "p":
            app.paused = not app.paused
        
        # Restart
        elif event.key == "r":
            appStarted(app)
            app.showHelp = False

        # Go to home screen
        elif event.key == "Escape":
            appStarted(app)
            app.showHelp = False

        # Start AI / hands off mode
        elif event.key == "h":
            app.helpMode = not app.helpMode


    elif event.key == "Escape":
        appStarted(app)
        app.showHelp = False


def play_isAbove(app):
    
    # Check if the block is above everything
    for i in range(0, len(app.terrain) - 1):
        if ((app.width // 2 - 30) < (app.terrain[i][0] + app.shifterX)):
            point = app.terrain[i]
            break

    # Check if is above
    if point[1] + app.shifterY < 2 * app.height // 3 + 30:
                return [False]

    # Return point if needed in other functions
    return [True, point]

def play_isLegal(app):
    # Check if isLegal, may have different conditions
    return play_isAbove(app)[0]

# Functions to move the pieces 
def play_moveLeft(app):

    # Move the distance and shifter if possible
    app.shifterX += app.velocityX
    app.distanceNow -= app.velocityX
    
    if not play_isLegal(app):
        app.shifterX -= app.velocityX
        app.distanceNow += app.velocityX

def play_moveRight(app):

    # Move the distance and shifter if possible
    app.shifterX -= app.velocityX
    app.distanceMoved += app.velocityX
    app.distanceNow += app.velocityX
    
    if not play_isLegal(app):
        app.shifterX += app.velocityX
        app.distanceMoved -= app.velocityX
        app.distanceNow -= app.velocityX

def play_moveUp(app):

    # Move the distance and shifter if possible
    app.shifterY += app.velocityY
    
    if not play_isLegal(app):
        app.shifterY -= app.velocityY

def play_moveDown(app):
    
    # Move the distance and shifter if possible
    app.shifterY -= app.velocityY

    if not play_isLegal(app):
        app.shifterY += app.velocityY
        
# Timerfired
def play_timerFired(app):

    if app.helpMode == True:
        play_helpMode(app)

    if app.paused == False:

        # Check for drone detection
        for i in range(len(app.drones)):

            if app.drones[i].point == []:
                continue
            
            if seperation.separating_axis_theorem(
                [(app.width // 2 + 30, 2 * app.height // 3 + 30),
                 (app.width // 2 - 30,2 * app.height // 3 - 30)],
                [(app.drones[i].scanner[0] + app.shifterX, 
                  app.drones[i].point[0][1] - 600+ app.shifterY),
                 (app.drones[i].scanner[2]  + app.shifterX, app.height),
                 (app.drones[i].scanner[3]  + app.shifterX, app.height)]):
                                
                                app.isSeen = True

            else:
                app.isSeen = False

            if app.isSeen == True and not play_isHidden(app):
                
                app.mode = "gameOver"
                gameOver_getHighScore(app)
                gameOver_setHighScore(app)
                

        if play_isHidden(app):
            app.cubeColor = "black"

        else:
            app.cubeColor = "blue"

        # Check for other detection
        if (play_turtleCollision(app) or 
           (play_ballCollision(app) and not play_isHidden(app))
            or play_spikeCollision(app)):
                app.mode = "gameOver"
                gameOver_getHighScore(app)
                gameOver_setHighScore(app)

        # Moves objects
        play_moveDrone(app)
        play_moveTurtles(app)
        play_dropBall(app)

        # Checks to make sure the gravity should keep changing
        if app.velocityY < 5:
            app.velocityY += app.gravity
        
        # Checks movement direction
        if app.stateX == "right":
            
            play_moveRight(app)

        elif app.stateX == "left":

            if app.distanceNow > 0:
                play_moveLeft(app)

        if app.stateY == "up":
            play_moveUp(app)

        elif app.stateY == "down":
            play_moveDown(app)

################################################################################

def play_helpMode(app):

    # Check if it is on a bound to see if will jump

    if play_isHidden(app):

        if ((play_isAbove(app)[1][1] + app.shifterY - 6) < 
                (2 * app.height // 3 + 30)):
                app.velocityY = -10

    if app.distanceNow <= 5:
        app.stateX = "right"

################################################################################

def generateDrone(app):
    
    for i in range(100, 100000, 1000):

        x = characters.Drone(i, i + 1000)
        app.drones.append(x)

    # Remove first few drones
    app.drones.pop(0)
    app.drones.pop(0)

    for aDrone in app.drones:


        # Find spawn point for the drone
        for i in range(len(app.terrain)):
            point = None
            if aDrone.spawn < app.terrain[i][0]:
                point = app.terrain[i]
                break

        # Skip if there is no midpoint
        if point == None: 
                continue

        aDrone.point.append(point)

    for aDrone in app.drones:
        if aDrone.point == []:
            app.drones.remove(aDrone)


def play_drawDrone(app, canvas):

    for aDrone in app.drones:

        # Find spawn point for the drone
        for i in range(len(app.terrain)):
            point = None
            if aDrone.spawn < app.terrain[i][0]:
                point = app.terrain[i]
                break

        # Skip if there is no midpoint
        if point == None: 
                continue

        # Draw drone
        canvas.create_rectangle(aDrone.body[0] + app.shifterX, 
                                point[1] - 600+ app.shifterY, 
                                aDrone.body[2]+ app.shifterX, 
                                point[1] - 700  + app.shifterY, 
                                fill = "black", outline = "black")

        canvas.create_oval(aDrone.eye[0] + app.shifterX, 
                           point[1] - 600 + app.shifterY, 
                           aDrone.eye[2]+ app.shifterX, 
                           point[1] - 700  + app.shifterY, 
                           fill = "white", outline = "black")

        canvas.create_oval(aDrone.pupil[0] + app.shifterX, 
                           point[1] - 600+ app.shifterY, 
                           aDrone.pupil[2]+ app.shifterX, 
                           point[1] - 650  + app.shifterY, 
                           fill = "black", outline = "white")

        canvas.create_polygon(aDrone.scanner[0]  + app.shifterX, 
                              point[1] - 600+ app.shifterY,
                              aDrone.scanner[2]  + app.shifterX, app.height,
                              aDrone.scanner[3]  + app.shifterX, app.height, 
                              fill = "white")

def play_moveDrone(app):

    for aDrone in app.drones:

        # Check if move is possible
        if (((aDrone.body[0] + app.shifterX + app.droneDX > 
            aDrone.patrolPoint2 + app.shifterX) or 
            aDrone.body[0] + app.shifterX + (app.droneDX * -1)) >= 
            aDrone.patrolPoint1 + app.shifterX):
            app.droneDX = app.droneDX  * -1
        
        # Move each part
        aDrone.body[0] += app.droneDX
        aDrone.body[2] += app.droneDX
        aDrone.eye[0] += app.droneDX
        aDrone.eye[2] += app.droneDX
        aDrone.pupil[0] += app.droneDX
        aDrone.pupil[2] += app.droneDX
        aDrone.scanner[0] += app.droneDX
        aDrone.scanner[2] += app.droneDX
        aDrone.scanner[3] += app.droneDX


################################################################################

def play_generateSpikes(app):   

    # Create a temporary list of spikes 
    tempList = []
    for i in range(2, len(app.terrain) - 2):

            # Change number of spikes based on progress
            if 0 < i <= 25:
                numberOfSpikes = random.randint(1, 3)

            elif 25 < i <= 75:
                numberOfSpikes = random.randint(1, 5)

            elif 75 < i <= 150:
                numberOfSpikes = random.randint(1, 7)

            else:
                numberOfSpikes = random.randint(3, 7)

            # Find x point to spawn the first spike on
            difference = abs(app.terrain[i + 2][0] - app.terrain[i][0])
            spikesDX = random.randint(0, difference // 2)

            # Make sure the spikes are in range
            if app.terrain[i][0] + spikesDX < app.terrain[i + 1][0]:

                # Create new spikes
                newSpikes = characters.Spikes(app.terrain[i][0] + spikesDX, 
                                              app.terrain[i][1])

                # Create appropriate number of spikes
                for i in range(numberOfSpikes):
                    if i == 0:
                        continue

                    # Add spikes coordinates to attributes
                    else:
                        nextPoint1 = newSpikes.coords[-1]
                        nextPoint2 = (newSpikes.coords[-2][0] + 10, 
                                      newSpikes.coords[-2][1])
                        nextPoint3 = (newSpikes.coords[-3][0] + 20, 
                                      newSpikes.coords[-3][1])
                        newSpikes.coords.append(nextPoint1)
                        newSpikes.coords.append(nextPoint2)
                        newSpikes.coords.append(nextPoint3)

                tempList.append(newSpikes)

    # Generate spikes based on player progess
    for i in range(len(tempList)):

            probability = None

            if 0 < i <= 25:
                probability = random.randint(1, 7)

            elif 75 < i <= 150:
                probability = random.randint(1, 4)

            else:
                probability = random.randint(1, 3)

            if probability == 1:
                    app.spikes.append(tempList[i])

# Draw spikes
def play_drawSpikes(app,canvas):

    for i in range(len(app.spikes)):

        spikesCoords = app.spikes[i].coords
        
        for i in range(len(spikesCoords) // 3):
                canvas.create_polygon(spikesCoords[3*i][0] + app.shifterX, 
                                      spikesCoords[3*i][1]+ app.shifterY,
                                      spikesCoords[3*i+1][0]+ app.shifterX, 
                                      spikesCoords[3*i+1][1]+ app.shifterY,
                                      spikesCoords[3*i+2][0]+ app.shifterX, 
                                      spikesCoords[3*i+2][1]+ app.shifterY, 
                                      fill ="black")

def play_spikeCollision(app):
    for spikes in app.spikes:

        midpoints = []

        # Find midpoints for better midpoint detection
        for i in range(len(spikes.coords)-1):
            midpoints.append(midpoint(spikes.coords[i][0], 
                                      spikes.coords[i][1], 
                                      spikes.coords[i + 1][0], 
                                      spikes.coords[i + 1][1],))

        # Check for collisions
        for point in midpoints:
            if app.cube[2] <= point[0] + app.shifterX <= app.cube[0]:
                if app.cube[3] <= point[1] + app.shifterY <= app.cube[1]:
                    return True

        for point in spikes.coords:
            if app.cube[2] <= point[0] + app.shifterX <= app.cube[0]:
                if app.cube[3] <= point[1] + app.shifterY <= app.cube[1]:
                    return True

    return False

def midpoint(x0, y0, x1, y1):
    return (((x0 + x1) / 2, (y0 + y1) / 2))

################################################################################

def play_generateTurtles(app):

    tempList = []

    # Create new turtles
    for i in range(2, len(app.terrain) - 2):
        if app.terrain[i + 1][0] - app.terrain[i][0] >= 150:
            newTurtle = characters.Turtle(app.terrain[i][0] + 5, 
                                        app.terrain[i][1], i)
            tempList.append(newTurtle)

    # Only add appropriate turtles
    for i in range(len(tempList)):
        if i > 5:
            if i % 2 == 0:
                app.turtles.append(tempList[i])

def play_drawTurtles(app, canvas):
    
    # Draw turtles
    for i in range(len(app.turtles)):
        
        canvas.create_oval(app.turtles[i].coords[0][0] + app.shifterX, 
                             app.turtles[i].coords[0][1] + app.shifterY, 
                             app.turtles[i].coords[1][0] + app.shifterX,
                             app.turtles[i].coords[1][1] + app.shifterY, 
                             fill = "black")

        canvas.create_rectangle(app.turtles[i].coords[2][0] + app.shifterX, 
                             app.turtles[i].coords[2][1] + app.shifterY, 
                             app.turtles[i].coords[3][0] + app.shifterX,
                             app.turtles[i].coords[3][1] + app.shifterY, 
                             fill = "black")


def play_moveTurtles(app):

    for aTurtle in app.turtles:
        # Check if move is possible
        if (((aTurtle.coords[3][0] + app.shifterX + app.turtleDX >= 
            app.terrain[aTurtle.i + 1][0] + app.shifterX) or 

            aTurtle.coords[0][0] + app.shifterX + (app.turtleDX)) <= 
            app.terrain[aTurtle.i][0] + app.shifterX):
            app.turtleDX = app.turtleDX  * -1
        
        # Move each part
        aTurtle.coords[0][0] += app.turtleDX
        aTurtle.coords[1][0] += app.turtleDX
        aTurtle.coords[2][0] += app.turtleDX
        aTurtle.coords[3][0] += app.turtleDX


def play_turtleCollision(app):

    # Find points on turtle
    for i in range(len(app.turtles)):
        turtle = app.turtles[i]
        centerX = turtle.coords[0][0] + 20
        centerY = turtle.coords[0][1] + 20

        point1 = [centerX - (10 * (2 ** 0.5)), centerY - (10 * (2 ** 0.5))]
        point2 = [centerX - (10 * (2 ** 0.5)), centerY + (10 * (2 ** 0.5))]
        point3 = [centerX - 20, centerY]
        point4 = [centerX, centerY + 20]
        point5 = [centerX, centerY - 20]
        point6 = [centerX + 60, centerY + 20]
        point7 = [centerX + 60, centerY - 20]

        listOfPoints = [point1, point2, point3, point4, point5, point6, point7]

        # Check for collision
        for point in listOfPoints:
            if app.cube[2] <= point[0] + app.shifterX <= app.cube[0]:
                if app.cube[3] <= point[1] + app.shifterY <= app.cube[1]:
                    return True

    return False
    
################################################################################

def play_generateCrushers(app):

    tempList = []
    
    for i in range(len(app.terrain) - 2):

        # Create start point of crusher
        point1 = app.terrain[i]
        point2 = app.terrain[i + 2]
        startPoint = ((point1[0] + point2[0]) // 2, point2[1] - 450)

        # Create crusher and add to list
        newCrusher = characters.Crusher(startPoint[0] ,startPoint[1])
        tempList.append(newCrusher)

    # Generate crushers based on progress of player
    for i in range(len(tempList)):

            if i == 0 or i == 1:
                continue 

            probability = None

            if 0 < i <= 25:
                probability = random.randint(1, 7)

            elif 75 < i <= 150:
                probability = random.randint(1, 5)

            else:
                probability = random.randint(1, 4)

            if probability == 1:
                if i % 3 == 0:
                    app.crushers.append(tempList[i])


def play_drawCrushers(app, canvas):

    # Draw crushers
    for i in range(len(app.crushers)):
        canvas.create_rectangle(app.crushers[i].coords[0][0] - 50 +app.shifterX, 
                                app.crushers[i].coords[0][1] - 25 +app.shifterY,
                                app.crushers[i].coords[0][0] + 50 +app.shifterX, 
                                app.crushers[i].coords[0][1] + 25 +app.shifterY,
                                fill = "black", outline = "black")

        # Draw ball
        canvas.create_oval(app.crushers[i].ball[0][0] - 25 + app.shifterX, 
                            app.crushers[i].ball[0][1] - 25 + app.shifterY,
                      app.crushers[i].ball[0][0] + 25 + app.shifterX, 
                      app.crushers[i].ball[0][1] +25 + app.shifterY,
                      fill = "black", outline = "black")


def play_dropBall(app):

    # Drop the ball unless it reaches the bottom of screen
    for i in range(len(app.crushers)):
        if app.crushers[i].ball[0][1] + app.shifterY >= app.height:
            app.crushers[i].ball[0][1] = app.crushers[i].coords[0][1]
        else:
            app.crushers[i].ball[0][1] += 3
        

def play_ballCollision(app):
    
    # Check for ball interaction 
    for i in range(len(app.crushers)):

        if (app.cube[2] <= app.crushers[i].ball[0][0] + 25 + app.shifterX 
            <= app.cube[0]):

            if (app.cube[3] <= app.crushers[i].ball[0][1] + app.shifterY 
                <= app.cube[1]):
                return True

        if (app.cube[2] <= app.crushers[i].ball[0][0] - 25 + app.shifterX 
            <= app.cube[0]):
            if (app.cube[3] <= app.crushers[i].ball[0][1] + app.shifterY 
                <= app.cube[1]):
                return True

        if (app.cube[2] <= app.crushers[i].ball[0][0] + app.shifterX 
            <= app.cube[0]):
            if (app.cube[3] <= app.crushers[i].ball[0][1] + app.shifterY + 25 
                <= app.cube[1]):
                return True

        if (app.cube[2] <= app.crushers[i].ball[0][0] + app.shifterX 
            <= app.cube[0]):
            if (app.cube[3] <= app.crushers[i].ball[0][1] + app.shifterY - 25 
                <= app.cube[1]):
                return True
                       
    return False

################################################################################

def play_generateTerrain(app):

    while len(app.terrain) <= 25:

        # Take the points we just had
        oldX = app.terrain[-1][0]
        oldY = app.terrain[-1][1]

        # Choose a random number to change x by
        dx = random.randrange(100, 200, 5)    

        # Get list of possible change in y
        dyList = [2.5 * 30, 
                3 * 30,
                4 * 30]

        # Choose y 
        i = random.randint(0, 2)
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

    while 25 < len(app.terrain) <= 75:
        # Take the points we just had
        oldX = app.terrain[-1][0]
        oldY = app.terrain[-1][1]

        # Choose a random number to change x by
        dx = random.randrange(200, 300, 5)

        dyList = [2.5 * 30, 
                3 * 30,
                4 * 30, 5 * 30]

        # Choose y 
        i = random.randint(0, 3)
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

    while 75 < len(app.terrain) <= 150:
        # Take the points we just had
        oldX = app.terrain[-1][0]
        oldY = app.terrain[-1][1]

        # Choose a random number to change x by
        dx = random.randrange(300, 350, 5)

        # Get the cube height
        dyList = [2.5 * 30, 
                3 * 30,
                4 * 30, 5 * 30]

        # Choose y 
        i = random.randint(0, 3)
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
        dx = random.randrange(200, 400, 5)

        dyList = [2.5 * 30, 
                3 * 30,
                4 * 30, 5 * 30]

        # Choose y 
        i = random.randint(0, 3)
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

    # Draws enemies
    play_drawCrushers(app, canvas)

    play_drawSpikes(app,canvas)
    play_drawTurtles(app, canvas)
    play_drawDrone(app, canvas)

    # Draws cube
    play_drawCube(app, canvas)

    # Draws terrain
    play_drawTerrain(app, canvas)
    # Create pointless terrain to the left of x = 0
    canvas.create_rectangle(-100000, app.height, 0, 555, fill = "black")

    # Draws score
    canvas.create_text(app.width // 2, 20, 
                       text = f"Score: {app.distanceNow // 10}", 
                       fill = "black", font = "Arial 30" )

    # Draw paused screen
    if app.paused == True:
        canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")

        canvas.create_text(app.width // 2, app.height // 2, 
                       text = "PAUSED",
                       font = "Arial 200", fill = "white")



runApp(width = 1440, height = 770)

################################################################################