"""
Friendlier API for amicably interfacing with non-friendlies
"""
import copy
import math

class Enemy:
    def __init__(self, bot_id, bot_name, x, y):
        self.bot_name = bot_name
        self.bot_id = bot_id
        self.x = x
        self.y = y
        self._current_turn = 0

        # since enemies may move out of view, we track the last known iteration
        self._last_tracked = copy.copy(self)

    def movement_data(self):
        turns_since_spotted = self._current_turn - self._last_tracked._current_turn
        return {
            'turns_since_spotted': turns_since_spotted,
            'previous': self._last_tracked,
        }

    def update_location(self, x, y):
        """
        Called whenever a known enemy is "spotted" again (basically, it's
        still in the player view or came back into view)
        """
        self._last_tracked = copy.copy(self)
        self.x = x
        self.y = y

    # gets the distance between this entity's coordinates and the given
    # player x and y points
    def distance(self, p_x, p_y):
        dx = self.x - p_x
        dy = self.y - p_y
        return math.sqrt(dx**2 + dy**2)

    def increment_turn(self):
        self._current_turn += 1

    def angle_distance(self, heading, p_x, p_y):
        """
        Takes a direction from player.getGunHeading(), player.getHeading(),
        or player.getRadarHeading() and then returns the distance in degrees
        from the player's current direction.
        """
        player_angle = heading % 360
        dx = self.x - p_x
        dy = self.y - p_y
        this_angle = math.degrees(math.atan2(dy, dx)) - 90

        distance = this_angle - player_angle
        if distance < -180:
            distance += 360
        elif 180 < distance:
            distance -= 360

        return distance


class Enemies:
    def __init__(self):
        self.enemies = {}

    def add_or_update(self, enemy):
        if enemy.bot_id in self.enemies:
            self.enemies[enemy.bot_id].update_location(enemy.x, enemy.y)
        else:
            self.enemies[enemy.bot_id] = enemy

    def increment_turns(self):
        for e in self.enemies.values():
            e.increment_turn()

    def get_closest_target(self, p_x, p_y):
        if len(self.enemies) == 0:
            return None

        distances = (
            (e.bot_id, e.distance(p_x, p_y)) for e in self.enemies.values()
             )

        best_bot_id = max(distances, key = lambda d: d[1])[0]

        return self.enemies[best_bot_id]
