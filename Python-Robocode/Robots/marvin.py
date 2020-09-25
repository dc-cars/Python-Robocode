#! /usr/bin/python
#-*- coding: utf-8 -*-

from robot import Robot #Import a base Robot
from enemy import Enemy, Enemies

"""
this is mostly based on the demo bots, but it adds a new notion of an `Enemy`
class and a container of `Enemies`.


Enemy API examples:

  Create an Enemy in the onTargetSpotted method of your bot:

      enemy = Enemy(botId, botName, botPos.x(), botPos.y())

  Get movement data:

      data = enemy.movement_data()
      data['turns_since_spotted'] # the number of turns since you last saw them
      data['previous'] # a copy of the last iteration of the enemy you spotted

  Calculate distance:

      distance_from_me = enemy.distance(my_x, my_y)

  Calculate the degrees needed to rotate to face enemy:

      # can also use self.getHeading() for the tank's direction, or
      # self.getRadarHeading() for the direction your radar is pointing
      my_heading = self.getGunHeading()
      degrees_to_rotate = enemy.angle_distance(my_heading, my_x, my_y)


Enemies API:

  In your init method:

      self.enemies = Enemies()

  If you care about movement data, make sure to update how many turns have
  passed in your `run()` method:

      self.enemies.increment_turns()

  Call add_or_update to record new enemies or update their positions:

      self.enemies.add_or_update(enemy)

  Get the closest target:

      best_target = self.enemies.get_closest_target(my_x, my_y)

  And finally, you can access `self.enemies.enemies` to get the underlying
  dictionary where keys are bot IDs and values are `Enemy` instances.
"""

class Marvin(Robot): #Create a Robot
    def init(self):# NECESARY FOR THE GAME   To initialyse your robot
        #Set the bot color in RGB
        self.setColor(204, 51, 153)
        self.setGunColor(0, 203, 153)
        self.setRadarColor(204, 0, 0)
        self.setBulletsColor(252, 33, 165)

        #get the map size
        size = self.getMapSize() #get the map size
        self.radarVisible(True) # show the radarField

        self.enemies = Enemies()

    def run(self): #NECESARY FOR THE GAME  main loop to command the bot

        # updates each enemy's "turn" (each time self.run() is called by
        # the main loop)
        self.enemies.increment_turns()

        # get your own position
        pos = self.getPosition()
        x = pos.x()
        y = pos.y()

        # find the closest known target
        best_target = self.enemies.get_closest_target(x, y)

        # if we didn't find a target, spin! why not
        # note that once we have a target this branch will never run, so
        # there might be other conditions you want to check here
        if best_target is None:
            # this will turn the radar and gun by 10 degrees at the same
            # time (.stop() collects the actions above to run them together)
            self.radarTurn(10)
            self.gunTurn(10)
            self.stop()

        # otherwise figure out how much we need to rotate
        else:
            # figure out how far we need to rotate the gun to face the
            # enemy's current position
            degrees_to_rotate = best_target.angle_distance(self.getGunHeading(),
                                                           x,
                                                           y,
                                                           )
            self.gunTurn(degrees_to_rotate)
            self.radarTurn(degrees_to_rotate)

            # this calculates the absolute distance between you and your target
            abs_distance = best_target.distance(pos.x(), pos.y())

            # careful! this damages you too. you can choose a value of 1-10,
            # so if you're sure you'll hit, go all out
            self.fire(1)
            # calling .stop() here collects the gun rotation, radar rotation,
            # and firing so that they happen at the same time
            self.stop()



    def sensors(self):  #NECESARY FOR THE GAME
        """Tick each frame to have datas about the game"""
        pos = self.getPosition() #return the center of the bot
        x = pos.x() #get the x coordinate
        y = pos.y() #get the y coordinate
        angle = self.getGunHeading() #Returns the direction that the robot's gun is facing
        angle = self.getHeading() #Returns the direction that the robot is facing
        angle = self.getRadarHeading() #Returns the direction that the robot's radar is facing
        list = self.getEnemiesLeft() #return a list of the enemies alive in the battle
        for robot in list:
            id = robot["id"]
            name = robot["name"]
            # each element of the list is a dictionnary with the bot's id and the bot's name

    def onHitByRobot(self, robotId, robotName):
        self.rPrint("damn a bot collided me!")

    def onHitWall(self):
        self.reset() #To reset the run fonction to the begining (auomatically called on hitWall, and robotHit event) 
        self.pause(100)
        self.move(-100)
        self.rPrint('ouch! a wall !')
        self.setRadarField("large") #Change the radar field form

    def onRobotHit(self, robotId, robotName): # when My bot hit another
        self.rPrint('collision with:' + str(robotName)) #Print information in the robotMenu (click on the righ panel to see it)

    def onHitByBullet(self, bulletBotId, bulletBotName, bulletPower): #NECESARY FOR THE GAME
        """ When i'm hit by a bullet"""
        self.reset() #To reset the run fonction to the begining (auomatically called on hitWall, and robotHit event) 
        self.rPrint ("hit by " + str(bulletBotName) + "with power:" +str( bulletPower))

    def onBulletHit(self, botId, bulletId):#NECESARY FOR THE GAME
        """when my bullet hit a bot"""
        self.rPrint ("fire done on " +str( botId))


    def onBulletMiss(self, bulletId):#NECESARY FOR THE GAME
        """when my bullet hit a wall"""
        self.rPrint ("the bullet "+ str(bulletId) + " fail")
        self.target = None
        # many of the examples use this pause here to wait 10 frames. it can
        # act as a kind of reset
        #self.pause(10)

    def onRobotDeath(self):#NECESARY FOR THE GAME
        """When my bot die"""
        self.rPrint ("damn I'm Dead")

    def onTargetSpotted(self, botId, botName, botPos):#NECESARY FOR THE GAME
        "when the bot see another one"
        enemy = Enemy(botId, botName, botPos.x(), botPos.y())
        self.enemies.add_or_update(enemy)
