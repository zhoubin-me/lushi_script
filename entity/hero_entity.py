from .base_entity import BaseEntity


class HeroEntity(BaseEntity):

    def __init__(self):
        super().__init__()
        self.atk = 0
        self.health = 0
        # INVALID = 0 施法者CASTER = 1 斗士FIGHTER = 2 TANK = 3 NEUTRAL = 4
        self.lettuce_role = 2  # 斗士
        self.race = None
        self.pos = [0, 0]  # 坐标[x, y]
        # 场上位置
        self.zone_position = 0
        # 预留
        self.cost = 0
        self.divine_shield = 0
        self.wind_fury = 0
        self.spell = [None, None, None, None]  # 被动 一技能 二技能 三技能...
        self.spell_dmg = 0
        self.deathrattle = 0

    @classmethod
    def basic(cls, pos_x, pos_y, role, atk, health):
        e = HeroEntity()
        e.atk = atk
        e.health = health
        e.role = role  # 斗士
        e.pos = [pos_x, pos_y]
        return e

    def attack(self, target, dmg):
        total_dmg = dmg * BaseEntity.damage_advantage[self.lettuce_role][target.lettuce_role]
        target.health -= total_dmg
        return total_dmg
