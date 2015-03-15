import kivy
kivy.require('1.0.8')

from kivy.core.window import Window
from kivy.uix.widget import Widget
#from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
#from kivy.graphics import Ellipse
#from kivy.graphics import Fbo
from kivy.app import App
from kivy.clock import Clock
import math
import random
import os 
import time
#from kivy.properties import NumericProperty
from kivy.graphics import PushMatrix
from kivy.graphics import PopMatrix
from kivy.graphics import Translate
from kivy.graphics import Rotate
from kivy.graphics import Scale
IsDebug = False
#PPS will stand for Pixels Per Second
pixelsPerMeter = 64.0
framesPerSecond = 60.0


def equalSize(thisSize, thatSize):
    return thisSize[0]==thatSize[0] and thisSize[1]==thatSize[1]

def getStringFromRectangle(thisRectangle):
    return "("+str(thisRectangle.pos[0])+"+"+str(thisRectangle.size[0])+","+str(thisRectangle.pos[1])+"+"+str(thisRectangle.size[0])+")"

fullCircleRadians = math.radians(360.0)
negativeFullCircleRadians = math.radians(-360.0)
halfCircleRadians = math.radians(180.0)
negativeHalfCircleRadians = math.radians(-180.0)
def angleDiffAbsolueValue_Radians(angle1, angle2):
    global fullCircleRadians
    global halfCircleRadians
    angle1 = getPositiveAngleLessThanFullCircleRadians(angle1)
    angle2 = getPositiveAngleLessThanFullCircleRadians(angle2)
    diff = angle2 - angle1
    if (diff<0.0):
        diff = diff * -1.0
    if (diff>halfCircleRadians):
        diff = fullCircleRadians - diff
    return diff

def angleDiff_Radians(angle1, angle2):
    global fullCircleRadians
    global halfCircleRadians
    global negativeHalfCircleRadians
    delta = angle2-angle1
    if delta < negativeHalfCircleRadians:
        delta = fullCircleRadians+delta
    elif delta > halfCircleRadians:
        delta = delta-fullCircleRadians
    return delta

def getPositiveAngleLessThanFullCircleRadians(angle):
    global fullCircleRadians
    while (angle<0.0):
        angle += fullCircleRadians
    while angle >= fullCircleRadians:
        angle -= fullCircleRadians
    return angle

#does NOT pass destAngle
def getRotatedTowardDestAngleByDeltaRadians(startAngle, destAngle, desiredDelta, minDelta):
    global halfCircleRadians
    global fullCircleRadians
    global IsDebug
    #startAngle = getPositiveAngleLessThanFullCircleRadians(startAngle)
    #destAngle = getPositiveAngleLessThanFullCircleRadians(destAngle)
    positiveDesiredDelta = abs(desiredDelta)
    actualDelta = angleDiff_Radians(startAngle, destAngle)
    #positiveActualDelta = abs(actualDelta)
    newDelta = actualDelta
    if actualDelta < 0.0:
        desiredDelta = positiveDesiredDelta * -1.0
        if desiredDelta < actualDelta:
            newDelta = actualDelta
        else:
            newDelta = desiredDelta
    else:
        desiredDelta = positiveDesiredDelta
        if desiredDelta > actualDelta:
            newDelta = actualDelta
        else:
            newDelta = desiredDelta
    
    if abs(newDelta) >= minDelta:
        
        #if actualDelta < 0.0:
        #    newDelta *= -1.0
    #     if IsDebug:
    #         if (actualDelta>0.01):
    #             print(str(math.degrees(startAngle))+" to "+str(math.degrees(destAngle))+": "+str(math.degrees(actualDelta)))
    #     if (destAngle<startAngle):
    #         newDelta *= -1.0
    
        #if newDelta>minDelta:
#             if (destAngle>startAngle):
#                 if destAngle-startAngle < halfCircleRadians:
#                     newDelta *= -1.0
#             else:
#                 if startAngle-destAngle < halfCircleRadians:
#                     newDelta *= -1.0
        startAngle += newDelta
        #if abs(desiredDelta)>math.radians(90):
        #    print (str(math.degrees(startAngle))+" to "+str(math.degrees(destAngle))+": "+str(math.degrees(actualDelta))+" limited to "+str(math.degrees(newDelta)))
#         if abs(newDelta)>abs(desiredDelta):
#             print (str(math.degrees(startAngle))+" to "+str(math.degrees(destAngle))+": "+str(math.degrees(actualDelta))+" limited to "+str(math.degrees(newDelta)))

    return startAngle

def getDistance1D(value1, value2):
    result = value2 - value1
    if result < 0:
        result = result * -1
    return result



def getRandRange(minimum, exclusiveMaximum):
    #global pseudorandom
    return random.randrange(minimum, exclusiveMaximum)#pseudorandom.getRandRange(minimum, exclusiveMaximum)

def getRandomColor():
    return Color(float(random.randrange(0,1000))/1000.0, float(random.randrange(0,1000))/1000.0, float(random.randrange(0,1000))/1000.0, 1.0)

def getDistance2DCoordinates(x1, y1, x2, y2):
    # **2 means squared:
    return math.sqrt( (x2 - x1) ** 2 + (y2 - y1) ** 2 )

def getDistance2DPoints(posA, posB):
    # **2 means squared:
    return math.sqrt( (posB[0] - posA[0]) ** 2 + (posB[1] - posA[1]) ** 2 )

def getDistanceBetweenCharacters(thisCharacter, thatCharacter):
    return getDistance2DCoordinates(thisCharacter.get_center_x(), thisCharacter.get_center_y(), thatCharacter.get_center_x(), thatCharacter.get_center_y())

def getPolarOffset(x1, y1, x2, y2):
    return rectToPolar_Radians(x2-x1, y2-y1)

#get random x,y integer coordinates as a tuple
def getRandomPointIntegersFromRectangle(thisRectangle):
    return random.randrange(int(thisRectangle.pos[0]),int(thisRectangle.pos[0]+thisRectangle.size[0])), random.randrange(int(thisRectangle.pos[1]),int(thisRectangle.pos[1]+thisRectangle.size[1])) 

def rectToPolar_Radians(x, y):
    r = math.sqrt(x*x + y*y)
    theta = None
    if (x==0.0 and y==0.0):
        theta = math.radians(-360.0) #technically undefined, but use -360 aka 0 for game
    elif (x==0.0):
        if (y>0.0):
            theta = math.radians(90.0)
        else: #elif (y<0.0):
            theta = math.radians(270.0)
    elif (y==0.0):
        if (x<0.0):
            theta = math.radians(180.0)
        else: #elif x>0.0
            theta = math.radians(0.0)
    else:
        theta = math.atan(y/x)  #atan is same as tan^-1
        if (x<0.0):
            theta = math.radians(180.0) + theta
        
    return r,theta

def polarToRect_Radians(r, theta):
    x = None
    y = None
    if (theta is not None):
        x = r * math.cos(float(theta))
        y = r * math.sin(float(theta))
    return x, y
    



class Character(Widget):
    Name = None
    freeAngle = None
    freePos = None
    #angle = NumericProperty(0)
    #color = None
    index = None
    teamIndex = None
    #NOTE: if Rectangle here instead of None, graphic will be shared by all!
    #graphic = None
    isAlive = None
    hasAI = False
    visible = True
    _target_x = None
    _target_y = None
    #directionRadians = None
    #maxSpeedPPS = None
    #maxSpeedPPF = None
    speed_M_s = None
    acceleration_M_s_s = None
    maxSpeedMetersPerSecond = None
    _hit_radius_at_scale_1 = None
    targetAngle = None
    maxTurnRadiansPerSecond = None
    knownMapRectangle = None
    _attack_radius_at_scale_1 = None
    aggroRadius = None
    _target_character = None
    _translate_instruction = None
    _rotate_instruction = None
    _scale_instruction = None
    _rectangle_instruction = None
    _color_instruction = None
    IsBloatable = None
    IsVampiric = None
    IsCapableOfCellDivision = None
    IsEdible = None
    IsActive = None
    _health = None
    _health_maximum = None
    i_see_characters = None
    sightRadius = None
    

    def __init__(self, **kwargs):
        super(Character, self).__init__(**kwargs)
        self.IsBloatable = False
        self.IsVampiric = False
        self.IsCapableOfCellDivision = False
        self.IsEdible = False
        self.IsActive = True
        self.freeAngle = 0.0
        self.i_see_characters = list()
        self.freePos = (10.0,100.0)
        
        self._rectangle_instruction = Rectangle(pos=(0,0), size=(20,20))
        self._translate_instruction = Translate(0,0)
        self._rotate_instruction = Rotate(origin=self.getCenterRelativePoint(), angle=self.freeAngle) #self.getCenterRelativePoint() only works AFTER setting rectangle size
        #self._rotate_instruction = Rotate(angle=0.0, origin=(self._rectangle_instruction.size[0]/2.0,self._rectangle_instruction.size[1]/2.0))
        self._scale_instruction = Scale(1.0,1.0,1.0)
        self._color_instruction = Color(1,1,1,1)


        self.canvas.add(PushMatrix())
        self.canvas.add(self._translate_instruction)
        self.canvas.add(self._rotate_instruction)
        self.canvas.add(self._scale_instruction)
        self.canvas.add(self._color_instruction)
        self.canvas.add(self._rectangle_instruction)
        self.canvas.add(PopMatrix())
        
        
        global framesPerSecond
        self.index = -1
        self.targetAngle = 0.0
        self.maxTurnRadiansPerSecond = math.radians(360)
        self.isAlive = True
        self._health_maximum = 1.0
        self._health = 1.0
        self.setMaxSpeedMetersPerSecond(.8)
        self.setColor(Color(1, 1, 1, 1))
        self._change_instructions() #updates self._hit_radius_at_scale_1
        self._attack_radius_at_scale_1 = 20.0
        self.aggroRadius = 50.0
        #self.graphic = Rectangle(pos=(0.0, 0.0), size=(self._hit_radius_at_scale_1*1.5, self._hit_radius_at_scale_1*2.5))
        self.speed_M_s = 0.0
        self.acceleration_M_s_s = 0.01
        #_target_x and _target_y must start with None for AI to work!
        self.Name = ""
        self.sightRadius = 64.0
        
    def set_health_relative(self, deltaHealth, IsAllowedPastMaximum):
        self.set_health(self._health+deltaHealth, IsAllowedPastMaximum)
        
    def set_health(self, health, IsAllowedPastMaximum):
        self._health = health
        if self._health < 0.0001: #using small value instead of 0.0 prevents rounding errors that would leave target with tiny decimal amount of health
            self._health = 0.0
        elif self._health > self._health_maximum:
            if not IsAllowedPastMaximum:
                self._health = self._health_maximum

        #self_asFood_percentage and other code below is only for changing graphics (character withering)
        self_asFood_percentage = float(self._health) / float(self._health_maximum)
        self_asFood_percentage_capped_at_1 = self_asFood_percentage
        if (self_asFood_percentage_capped_at_1>1.0):
            self_asFood_percentage_capped_at_1 = 1.0
        if (self._color_instruction.a>self_asFood_percentage_capped_at_1):
            self._color_instruction.a=self_asFood_percentage_capped_at_1
#         if (self._scale_instruction.x>self_asFood_percentage):
#             self._scale_instruction.x=self_asFood_percentage
#             self._scale_instruction.y=self_asFood_percentage
#             self._change_instructions()
        #if (attackEffectiveness>0):
        if self.IsBloatable:
            if self._scale_instruction.x!=self_asFood_percentage:
                self._scale_instruction.x=self_asFood_percentage
                self._scale_instruction.y=self_asFood_percentage
                self._change_instructions()
        else:
            if self._scale_instruction.x>self_asFood_percentage:
                self._scale_instruction.x=self_asFood_percentage
                self._scale_instruction.y=self_asFood_percentage
                self._change_instructions()
        

    def set_health_maximum(self, health_maximum, IsHealthToBeAtMaximum):
        self._health_maximum = health_maximum
        if (IsHealthToBeAtMaximum):
            self._health = self._health_maximum

    def see_character(self, seeCharacter):
        IsNew = True
        for index in range(0,len(self.i_see_characters)):
            if self.i_see_characters[index] == seeCharacter.index:
                IsNew = False
                break
        if IsNew:
            self.i_see_characters.append(seeCharacter)
            
    def isAbleToSeeCharacterIndex(self, characterIndex):
        CanSee = False
        for index in range(0,len(self.i_see_characters)):
            if self.i_see_characters[index] == characterIndex:
                CanSee = True
        return CanSee

#region position
    #def getCenterPoint(self):
    #    return (self.get_center_x(),self.get_center_y())
    def getCenterRelativePoint(self):
        return (self._rectangle_instruction.size[0]/2.0,self._rectangle_instruction.size[1]/2.0)

    def get_center_x(self):
        return self.freePos[0]
    
    def get_center_y(self):
        return self.freePos[1]
    
    def getCenterPoint(self):
        return self.freePos[0], self.freePos[1]
        
        
    def set_center_x(self, x):
        self.freePos = float(x), self.freePos[1]
        self._change_instructions()

    def set_center_y(self, y):
        self.freePos = self.freePos[0], float(y)
        self._change_instructions()
    
    def setCenterPoint(self, pos):
        self.freePos = float(pos[0]), self.freePos[1]
        self.freePos = self.freePos[0], float(pos[1])
        self._change_instructions()

    def setCenterPointCoordinates(self, x, y):
        self.setCenterPoint((x,y))
        

#     def setCenter(self,x,y):
#         self.setLeftBottom( (  float(x) - self.getWidth() / 2.0,  float(y) - self.getHeight()/2.0  ) )

        
    def getLeft(self):
        return self._translate_instruction.pos[0]
    def getBottom(self):
        return self._translate_instruction.pos[1]
    
#     def setLeftBottom(self,thisOrderedPair):
#         self._rectangle_instruction.pos = float(thisOrderedPair[0]), float(thisOrderedPair[1])
#         self._rotate_instruction.origin = self.get_center_x(), self.get_center_y()
    def setPositionRelativePolar(self, r, theta):
        moveByX,moveByY = polarToRect_Radians(r, theta)
        originalX, originalY = self.getCenterPoint()
        self.setCenterPointCoordinates( float(originalX+moveByX), float(originalY+moveByY) )        


    def getSpeedPixelsPerFrame(self):
        global pixelsPerMeter
        global framesPerSecond
        return self.speed_M_s*pixelsPerMeter/framesPerSecond
    def getMaxSpeedPixelsPerFrame(self):
        global pixelsPerMeter
        global framesPerSecond
        return self.maxSpeedMetersPerSecond*pixelsPerMeter/framesPerSecond
    def stop(self):
        self.setTargetCoordinates(self.get_center_x(), self.get_center_y())

    def setTargetPoint(self, pos):
        if (self._target_x != float(pos[0]) or self._target_y != float(pos[1])):
            self._target_x = float(pos[0])
            self._target_y = float(pos[1])
    
    def setTargetCoordinates(self, _target_x, _target_y):
        if (self._target_x != float(_target_x) or self._target_y != float(_target_y)):
            self._target_x = float(_target_x)
            self._target_y = float(_target_y)
            #self.speed_M_s = 0.0
    def chooseRandomTargetLocation(self):
        if (self.isAlive):
            if (self.knownMapRectangle is not None):
                randomX, randomY = getRandomPointIntegersFromRectangle(self.knownMapRectangle)
                self.setTargetCoordinates(randomX, randomY)
                #print("character["+str(self.index)+"] chose target "+str((self._target_x, self._target_y)))
                #print("Random target is "+str((randomX, randomY)))
            else:
                #print(self.Name+" can't see")
                pass

    def setMaxSpeedMetersPerSecond(self,set_M_s):
        #global framesPerSecond
        #global pixelsPerMeter
        #self.maxSpeedPPS = float(set_M_s) / float(pixelsPerMeter)
        #self.maxSpeedPPF = self.maxSpeedPPS / framesPerSecond
        self.maxSpeedMetersPerSecond = float(set_M_s)
        
    def setPositionRelativeRectangular(self, xOffset, yOffset):
        self.pos = self.pos[0]+float(xOffset), self.pos[1]+float(yOffset)

#endregion position

#region size
    def getWidth(self):
        return self._rectangle_instruction.size[0]
    def getHeight(self):
        return self._rectangle_instruction.size[1]
#endregion size


#region angle
    def getMaxRotationSpeedRadiansPerFrame(self):
        global framesPerSecond
        return self.maxTurnRadiansPerSecond/framesPerSecond

    def getRotationSpeedRadiansPerFrame(self):
        return self.getMaxRotationSpeedRadiansPerFrame()
    
    def setAngleRadians(self, angle):
        self.freeAngle = math.degrees(angle)
        self._change_instructions()
        
    def getAngleRadians(self):
        return math.radians(self.freeAngle)

#endregion angle

    def _change_instructions(self):
        self._translate_instruction.x = self.freePos[0]-self._rectangle_instruction.size[0]*self._scale_instruction.x/2
        self._translate_instruction.y = self.freePos[1]-self._rectangle_instruction.size[1]*self._scale_instruction.y/2
        #self._rectangle_instruction.pos = self.freePos[0]-self._rectangle_instruction.size[0]*self._scale_instruction.x/2.0, self.freePos[1]-self._rectangle_instruction.size[1]*self._scale_instruction.y/2.0
        self._rotate_instruction.origin = self._rectangle_instruction.size[0]*self._scale_instruction.x/2.0, self._rectangle_instruction.size[1]*self._scale_instruction.x/2.0 
        self._rotate_instruction.angle = self.freeAngle
        self._hit_radius_at_scale_1 = (float(self._rectangle_instruction.size[0]) + float(self._rectangle_instruction.size[1])) / 2.0


#region color
    def setColor(self, color):
        try:
            self._color_instruction.b = color.b
            self._color_instruction.g = color.g
            self._color_instruction.r = color.r
            self._color_instruction.a = color.a
        except:
            try:
                self._color_instruction.b = color[0]
                self._color_instruction.g = color[1]
                self._color_instruction.r = color[2]
                self._color_instruction.a = color[3]
            except:
                pass
    
    def getColorR(self):
        return self._color_instruction.r
    def getColorG(self):
        return self._color_instruction.g
    def getColorB(self):
        return self._color_instruction.b
    def getColorA(self):
        return self._color_instruction.a
#endregion color
    
    def getAverageScale(self):
        return float(self._scale_instruction.x + self._scale_instruction.y) / 2.0
    
    def getAttackRadius(self):
        return float(self._attack_radius_at_scale_1) * self.getAverageScale()
    
    def getHitRadius(self):
        return float(self._hit_radius_at_scale_1) * self.getAverageScale()

    def set_target_character(self, character):
        self._target_character = character
        if (character is not None):
            self.setTargetPoint(character.getCenterPoint())
            #print(self.Name+" acquired target "+character.Name+" health "+str(character._health))
        else:
            self._target_x = None
            self._target_y = None
    
    def attack(self,attackedCharacter):
        killedCharacter = None
        attackEffectiveness = 0.02
        thisAttackDistance = getDistanceBetweenCharacters(self, attackedCharacter)-attackedCharacter.getHitRadius()
        if self.isAlive:
            if thisAttackDistance < self.getAttackRadius():
                if attackedCharacter.isAlive:
                    #print("character["+str(self.index)+"] attacked from "+str(thisAttackDistance)+" away")
                    attackedCharacter.isAlive = False
                    killedCharacter = attackedCharacter
                    #attackedCharacter.setColor( Color(attackedCharacter.getColorR(),attackedCharacter.getColorG(),attackedCharacter.getColorB(),0.5) )
                    attackedCharacter.setColor( Color(attackedCharacter.getColorR()/2.0,attackedCharacter.getColorG()/2.0,attackedCharacter.getColorB()/2.0,1.0) )
                    #print(self.Name+" killed "+attackedCharacter.Name+" ("+str(attackedCharacter._health)+" health) ")
                elif attackedCharacter._health > 0.0:
                    previous_target_health = attackedCharacter._health
                    attackedCharacter.set_health_relative(-1.0*attackEffectiveness, False)
                    attackEffectiveness = previous_target_health - attackedCharacter._health  #don't steal more health than target had
                    if attackEffectiveness < 0:
                        attackEffectiveness = 0
                    elif self.IsVampiric:
                        self.set_health_relative(attackEffectiveness,self.IsBloatable)
                    #print(self.Name+" consumed "+attackedCharacter.Name+" ("+str(attackedCharacter._health)+" health) by "+str(attackEffectiveness))
            else:
                #print(self.Name+" missed "+attackedCharacter.Name+" ("+str(attackedCharacter._health)+" health) since distance "+str(thisAttackDistance)+" and range "+str(self.getAttackRadius()))
                pass
        return killedCharacter
    
    def isViableTarget(self, acquiredTarget):
        IsViable = False
        if (acquiredTarget is not None) and (acquiredTarget.IsActive):
            if self.IsVampiric:
                if acquiredTarget._health>0.0:
                    IsViable = True
            else:
                if acquiredTarget.isAlive:
                    IsViable = True
            
        return IsViable
    
    def evaluateTargets(self):
        if self.hasAI and self.isAlive:
            if self._target_character is not None:
                if (getDistance2DPoints(self._target_character.freePos, self.freePos)>self.sightRadius):
                    self.i_see_characters.remove(self._target_character)
                    self.set_target_character(None)
                    #self._target_character = None
                    #self.chooseRandomTargetLocation()
                elif not self.isViableTarget(self._target_character):
                    self.i_see_characters.remove(self._target_character)
                    self.set_target_character(None)
                    #self._target_character = None
                    #self.chooseRandomTargetLocation()
            
            potentialTarget = None
            potentialTargetDistance = None
            if self._target_character is None:
                if self.i_see_characters is not None:
                    for index in range(0,len(self.i_see_characters)):
                        thisDistance = getDistance2DPoints(self.i_see_characters[index].freePos, self.freePos)
                        if (potentialTarget is None) or (thisDistance<potentialTargetDistance):
                            if self.i_see_characters[index].teamIndex != self.teamIndex:
                                potentialTargetDistance = thisDistance
                                potentialTarget = self.i_see_characters[index]
                if potentialTarget is not None:
                    if (potentialTargetDistance<=self.aggroRadius) and self.isViableTarget(potentialTarget):
                        self.set_target_character(potentialTarget)
#                         self._target_character = potentialTarget
#                         self.setTargetPoint(self._target_character.getCenterPoint())
            if self._target_x is None or self._target_y is None:
                self.chooseRandomTargetLocation()
            
    def refresh(self):
        global IsDebug
#         if (self.speed_M_s<self.maxSpeedMetersPerSecond):
#             print()
#             print("refresh self.speed_M_s: "+str(self.speed_M_s))
#             print("refresh self.acceleration_M_s_s: "+str(self.acceleration_M_s_s))
        self.speed_M_s += self.acceleration_M_s_s
        if (self.speed_M_s > self.maxSpeedMetersPerSecond):
            self.speed_M_s = self.maxSpeedMetersPerSecond
#         if (self.speed_M_s<self.maxSpeedMetersPerSecond):
#             print("refresh self.speed_M_s: "+str(self.speed_M_s))
        if self.isAlive:
            self.evaluateTargets()
                
            if (self._target_x is not None) and (self._target_y is not None):
                rToTarget, thetaToTarget = getPolarOffset(self.get_center_x(), self.get_center_y(), self._target_x, self._target_y)
                
                speedPPF = self.getSpeedPixelsPerFrame()
                #print("moveTowardTarget speedPPF:"+str(speedPPF))
                rMove, thetaTowardDest = ( min(rToTarget, speedPPF), thetaToTarget )
                #deltaRadians = angleDiffAbsolueValue_Radians(math.radians(self._rotate_instruction.angle), thetaMove)
                if (not self.hasAI):
                    IsDebug = True
                    #print("target: "+str(self._target_x)+","+str(self._target_y) )
                thetaMove = getRotatedTowardDestAngleByDeltaRadians(self.getAngleRadians(), thetaTowardDest, self.getRotationSpeedRadiansPerFrame(), math.radians(2))
                IsDebug = False
                #print("moveTowardTarget rMove:"+str(rMove))
                #print("moveTowardTarget rToTarget:"+str(rToTarget))
                self.setAngleRadians(thetaMove)
                if (rToTarget <= self.getHitRadius()):
                    #rMove = rMove*-1.0 #move in reverse if too close
                    if self._target_character is None:
                        if self.hasAI:
                            self.chooseRandomTargetLocation()
                else:
                    #print("character["+str(self.index)+"] moveTowardTarget")
                    self.setPositionRelativePolar(rMove, thetaMove)
                    #if (self.index==0):
                        #print()
                        #print("moveTowardTarget self._rectangle_instruction.pos:"+str(self._rectangle_instruction.pos))
                        #print("moveTowardTarget self.pos:"+str(self.pos))

                



class CanvasForm(Widget):
    characters = list()
    playerCharacter = None
    playerCharacterIndex = None
    characterCount = 0
    enemyMaxCount = 10
    teams = None
    playerTeamIndex = None
    computerTeamIndex = None
    lastCreatedCharacter = None
    lastCreatedCharacterIndex = None
    IsGameWon = False
    IsGameLost = False
    gameStatusLabel = None
    hitsCount = 0
    playerAttemptCount = 0
    accuracyLabel = None
    defeatsLabel = None
    bacteriaGeneratedLabel = None
    victoriesLabel = None
    playerKillCount = 0
    playerDeathCount = 0
    leukocyteImageFileName = "leukocyte.png"
    bacteriumImageFileName = "bacterium-a.png"
    mainBoxLayout = None
    IsPressing = False
    bacteriaEverGeneratedCount = 0
    
    def generateCharacter(self, IsToBeAddedToCanvas):
        self.lastCreatedCharacterIndex = self.characterCount
        self.lastCreatedCharacter = Character()
        self.lastCreatedCharacter.index = self.lastCreatedCharacterIndex
        self.lastCreatedCharacter.Name = "character#"+str(self.lastCreatedCharacterIndex)
        self.lastCreatedCharacter.teamIndex = 0
        self.characters.append(self.lastCreatedCharacter)
        if (IsToBeAddedToCanvas):
            self.add_widget(self.lastCreatedCharacter)
        self.lastCreatedCharacter.set_center_x(getRandRange(0,600))
        self.lastCreatedCharacter.set_center_y(getRandRange(0,600))
        self.lastCreatedCharacter.hasAI = True
        
        self.characterCount += 1


    def generateLeukocyte(self):
        self.generateCharacter(False)
        self.lastCreatedCharacter.IsEdible = True
        self.lastCreatedCharacter.Name = "leukocyte#"+str(self.lastCreatedCharacterIndex)
        if (os.path.isfile(self.leukocyteImageFileName)):
            self.lastCreatedCharacter._rectangle_instruction.source=self.leukocyteImageFileName
        self.lastCreatedCharacter.teamIndex = self.playerTeamIndex
        #self.lastCreatedCharacter.set_center_x(self.getWidth() / 2)
        #self.lastCreatedCharacter.set_center_y(self.getHeight() / 2)
        self.lastCreatedCharacter.set_center_x(getRandRange(0,600))
        self.lastCreatedCharacter.set_center_y(getRandRange(0,600))
        self.lastCreatedCharacter.stop()
        self.lastCreatedCharacter.hasAI = False
            
        self.lastCreatedCharacter._attack_radius_at_scale_1 = self.lastCreatedCharacter._attack_radius_at_scale_1 * 2.0
        self.lastCreatedCharacter.set_health_maximum(5.0, True)
        self.add_widget(self.lastCreatedCharacter)

    
    def generateBacterium(self):
        #Dis is Da Enemy Dude Thingy-Mabob Numero Uno
        self.generateCharacter(True)
        self.lastCreatedCharacter.setColor(Color(0, .7, .2))
        self.lastCreatedCharacter.Name = "bacterium#"+str(self.lastCreatedCharacterIndex)
        if (os.path.isfile(self.bacteriumImageFileName)):
            self.lastCreatedCharacter._rectangle_instruction.source=self.bacteriumImageFileName
            self.lastCreatedCharacter.setColor(Color(1,1,1,1))
        self.lastCreatedCharacter.teamIndex = self.computerTeamIndex
        self.lastCreatedCharacter.hasAI = True
        self.lastCreatedCharacter.IsBloatable = True
        self.lastCreatedCharacter.IsVampiric = True
        self.lastCreatedCharacter.IsCapableOfCellDivision = True
        self.bacteriaEverGeneratedCount += 1

    def generateBacteriumAtPoint(self, pos):
        self.generateBacterium()
        self.lastCreatedCharacter.setCenterPoint(pos)
                
        
    def __init__(self, **kwargs):
        super(CanvasForm, self).__init__(**kwargs)
        try:
            self._keyboard = Window.request_keyboard(
                self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_keyboard_down)
            self.bind(on_touch_down=self.canvasTouchDown)
            self.bind(on_touch_up=self.canvasTouchUp)
            self.bind(on_touch_move=self.canvasTouchMove)
            
        except:
            pass

        #NOTES:
        #pos[0] is x coordinate for position
        #pos[1] is y coordinate for position
        #The color constructor takes Red,Green,Blue, and Alpha which is opacity
        #so Color(1,0,0,1) is red
        
        self.teams = list()
        self.teams.append("Computer")
        self.computerTeamIndex=0
        self.teams.append("Player")
        self.playerTeamIndex=1
        
        self.victoriesLabel = Label(text="", color=(0,.7,.2,1))
        self.defeatsLabel = Label(text="")
        self.accuracyLabel = Label(text="", color=(.5,.5,.5,1))
        self.bacteriaGeneratedLabel = Label(text="", color=(0,.3,.1,1))
        self.gameStatusLabel = Label(text="", color=(0,.7,1,1))
        
#         self.victoriesLabel.pos_hint = (0,100)
#         self.defeatsLabel.pos_hint = (0,70)
#         self.accuracyLabel.pos_hint = (0,40)
#         self.gameStatusLabel.pos_hint = (0,10)
                
        self.add_widget(self.victoriesLabel)
        self.add_widget(self.defeatsLabel)
        self.add_widget(self.accuracyLabel)
        self.add_widget(self.bacteriaGeneratedLabel)
        self.add_widget(self.gameStatusLabel)

        for thisEnemyIndex in range(0,self.enemyMaxCount):
            self.generateBacterium()

        self.showStats(False)

        self.generateLeukocyte()
        self.playerCharacter = self.lastCreatedCharacter
        self.playerCharacterIndex = self.lastCreatedCharacterIndex
        
        #Making update interval 1/60 sec make game run at 60 frames per second:
        global framesPerSecond
        Clock.schedule_interval(self.update, 1.0 / framesPerSecond)

    def getWidth(self):
        return self.size[0]

    def getHeight(self):
        return self.size[1]

    def _keyboard_closed(self):
        print('Keyboard disconnected!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
            
    def removeInactiveCharacters(self):
        original_Len = len(self.characters)
        for activeCharacterIndex in range(0, original_Len):
            activeCharacter = self.characters[self.characterCount-activeCharacterIndex-1]  #start from end since removing as we go
            if (activeCharacter.IsEdible and (activeCharacter._health<=0.0)):
                activeCharacter.IsActive = False
            elif (not activeCharacter.IsEdible) and (not activeCharacter.isAlive):
                activeCharacter.IsActive = False
            if not activeCharacter.IsActive:
                self.characters.remove(activeCharacter)
        self.characterCount = len(self.characters)
        for activeCharacterIndex in range(0, self.characterCount):
            activeCharacter = self.characters[activeCharacterIndex]
            if activeCharacter._target_character is not None:
                if not activeCharacter._target_character.IsActive:
                    activeCharacter.i_see_characters.remove(activeCharacter._target_character)
                    activeCharacter.set_target_character(None)
                    #activeCharacter._target_character = None
                    #activeCharacter.chooseRandomTargetLocation()
                
        
        
    def update(self, dt):
        self.removeInactiveCharacters()
        for activeCharacterIndex in range(0, self.characterCount):
            activeCharacter = self.characters[activeCharacterIndex]
            if (activeCharacter.knownMapRectangle is None) or (not equalSize(activeCharacter.knownMapRectangle.size, self.size)):
                activeCharacter.knownMapRectangle = Rectangle(pos=(0.0,0.0),size=self.size)
                #print("Enemy "+str(activeCharacterIndex)+" saw map area: "+getStringFromRectangle(activeCharacter.knownMapRectangle))
            if (activeCharacter.hasAI):
                if activeCharacter._target_character is None:
                    for passiveCharacterIndex in range(0,self.characterCount):
                        passiveCharacter = self.characters[passiveCharacterIndex]
                        if (passiveCharacterIndex != activeCharacterIndex):
                            if (passiveCharacter.teamIndex != activeCharacter.teamIndex):
                                passiveCharacterDistance = getDistanceBetweenCharacters(activeCharacter,passiveCharacter)
                                if (passiveCharacterDistance <= activeCharacter.sightRadius):
                                    activeCharacter.see_character(passiveCharacter)  #DOES NOT add if already can see
                                    #if passiveCharacter._health > 0:
                                    #    activeCharacter._target_character = passiveCharacter
                                    #    break
                if activeCharacter.IsCapableOfCellDivision and activeCharacter._health>=2.0:
                    self.generateBacteriumAtPoint(activeCharacter.getCenterPoint())
#                         self.generateCharacter(Color(1,1,1,1), False)
#                         self.lastCreatedCharacter.setCenterPoint(activeCharacter.getCenterPoint())
#                         self.add_widget(self.lastCreatedCharacter)
                    #self.lastCreatedCharacter.setTargetCoordinates(200, 200)
                    activeCharacter.set_health_relative(-1.0, activeCharacter.IsBloatable)
                    #self.add_widget(Label(text="Generated bacterium"))
                    #refresh will get a new target
                elif activeCharacter._target_character is not None:
                    #if activeCharacter._target_character._health > 0.0:
                    killedCharacter = activeCharacter.attack(activeCharacter._target_character)
                    if (killedCharacter is not None) and (killedCharacter.teamIndex == self.playerTeamIndex):
                        self.playerDeathCount += 1
                        self.generateLeukocyte()
                        self.playerCharacterIndex = self.lastCreatedCharacterIndex
                        self.playerCharacter = self.lastCreatedCharacter
                #NOTE: if there is no target, activeCharacter.refresh() will get a random _target_x and _target_y.
                    
                        
            activeCharacter.refresh()
        
#         if (self.playerCharacter._health<=0):
#             self.generateLeukocyte()
#             self.playerCharacterIndex = self.lastCreatedCharacterIndex
#             self.playerCharacter = self.lastCreatedCharacter
            
        self.showStats(False)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        #print('The key' + str(keycode) + ' pressed')
        #print(' - text is ' + text)
        #print(' - modifiers are '+ str(modifiers))
        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()
        return True

    def showStats(self, IsToBeSaved):

        if self.playerDeathCount>0:
            self.defeatsLabel.text = "Bacteria ate "+str(self.playerDeathCount)+" of your leukocytes."
            self.defeatsLabel.set_center_x(self.get_center_x())
            self.defeatsLabel.set_center_y(self.get_center_y()/20.0*6.0)

        if self.playerKillCount>0:
            if (self.playerKillCount==1):
                self.victoriesLabel.text = "You destroyed "+str(self.playerKillCount)+" bacterium."
            else:
                self.victoriesLabel.text = "You destroyed "+str(self.playerKillCount)+" bacteria."
            self.victoriesLabel.set_center_x(self.get_center_x())
            self.victoriesLabel.set_center_y(self.get_center_y()/20.0*5.0)
        
        missesCount = self.playerAttemptCount - self.hitsCount
        accuracyPercentage = 0
        if self.playerAttemptCount > 0:
            accuracyMultiplier = float(self.hitsCount)/float(self.playerAttemptCount)
            accuracyPercentage = int(accuracyMultiplier*100.0+.5)
            self.accuracyLabel.text = "accuracy: "+str(accuracyPercentage)+"% ("+str(self.hitsCount)+" hit(s),"+str(missesCount)+" miss(es))"
            self.accuracyLabel.set_center_x(self.get_center_x())
            self.accuracyLabel.set_center_y(self.get_center_y()/20.0*4.0)

        if self.bacteriaEverGeneratedCount>0:
            self.bacteriaGeneratedLabel.text = str(self.bacteriaEverGeneratedCount)+" Bacteria generated."
            self.bacteriaGeneratedLabel.set_center_x(self.get_center_x())
            self.bacteriaGeneratedLabel.set_center_y(self.get_center_y()/20.0*3.0)

        self.gameStatusLabel.set_center_x(self.get_center_x())
        self.gameStatusLabel.set_center_y(self.get_center_y()/20.0*2.0)
        
        if IsToBeSaved:
            thisFileName = "stats.txt"
            try:
                modeString = 'w'
                thisLineseperator = ""
                if os.path.isfile(thisFileName):
                    modeString = 'a'
                outFile = open(thisFileName, modeString)
                outFile.write("KivyBacteriaStatisticSet:"+thisLineseperator)
                outFile.write(time.strftime("    time:'%Y-%m-%d %H:%M:%S'")+thisLineseperator)
                outFile.write('    type:win'+thisLineseperator)
                outFile.write('    bacteriaGenerated:'+str(self.bacteriaEverGeneratedCount)+thisLineseperator)
                outFile.write('    playerDeaths:'+str(self.playerDeathCount)+thisLineseperator)
                outFile.write('    playerKills:'+str(self.playerKillCount)+thisLineseperator)
                outFile.write('    playerAttempts:'+str(self.playerAttemptCount)+thisLineseperator)
                outFile.write('    accuracyPercentage:'+str(accuracyPercentage)+thisLineseperator)
                outFile.write(thisLineseperator)
                outFile.close()
            except Exception as e:
                print("failed to write statistics to \""+thisFileName+"\": "+str(e))
        #self.gameStatusLabel.text = "nothing happened yet"
    def canvasTouchMove(self, touch, *largs):
        arguments_pos_x, arguments_pos_y = largs[0].pos
        if self.IsPressing:
            self.playerCharacter.setTargetCoordinates(arguments_pos_x, arguments_pos_y)

    def canvasTouchUp(self, touch, *largs):
        self.IsPressing = False
        
    def canvasTouchDown(self, touch, *largs):
        self.IsPressing = True
        arguments_pos_x, arguments_pos_y = largs[0].pos
        self.playerCharacter.setTargetCoordinates(arguments_pos_x, arguments_pos_y)
        #r, theta = getPolarOffset(self.playerCharacter.get_center_x(), self.playerCharacter.get_center_y(), self.playerCharacter._target_x, self.playerCharacter._target_y)
        enemiesTotalCount = 0
        enemiesAliveCount = 0
        IsAShot = False
        for passiveCharacterIndex in range(0,self.characterCount):
            passiveCharacter = self.characters[passiveCharacterIndex]
            if (passiveCharacter.index != self.playerCharacter.index):
                enemiesTotalCount += 1
                #if (passiveCharacterIndex != activeCharacterIndex):
                fromClickDistance = getDistance2DCoordinates(arguments_pos_x, arguments_pos_y, passiveCharacter.get_center_x(), passiveCharacter.get_center_y())
                if passiveCharacter.isAlive:
                    if passiveCharacter.teamIndex != self.playerTeamIndex:
                        enemiesAliveCount += 1
                    if fromClickDistance<=passiveCharacter.getHitRadius():
                        IsAShot = True
                        killedCharacter = self.playerCharacter.attack(passiveCharacter)
                        if killedCharacter is not None:
                            self.hitsCount += 1
                            self.playerKillCount += 1
                            break  #prevents higher than 100% accuracy (double shot or higher)
        if (IsAShot):
            self.playerAttemptCount += 1
        if (enemiesAliveCount == 0):
            if not self.IsGameWon:
                self.IsGameWon=True
                self.gameStatusLabel.text = "YOU WIN!"
                self.showStats(True)
        #print("canvasTouchDown r:"+str(r))


class PolarBacteriaApp(App):
    def build(self):
        return CanvasForm()

if __name__ == '__main__':
    PolarBacteriaApp().run()
