from worldstate import WorldModifier


class Ability:

    def __init__(self, charge_rate, world_modifier):
        self.charge_rate = charge_rate
        self.world_modifier = world_modifier

joe = Ability(WorldModifier("pipe_speed", 10))