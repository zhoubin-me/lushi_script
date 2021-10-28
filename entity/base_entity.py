class BaseEntity:
    damage_advantage = {
        'r': {'r': 1, 'g': 2, 'b': 1, 'n': 1},
        'g': {'r': 1, 'g': 1, 'b': 2, 'n': 1},
        'b': {'r': 2, 'g': 1, 'b': 1, 'n': 1},
        'n': {'r': 1, 'g': 1, 'b': 1, 'n': 1}
    }

    def __init__(self):
        self.eid = 0
        self.name = ''
        self.atk = 0
        self.health = 0
        self.role = 'n'  # 斗士
        self.race = None
        self.pos = [0, 0]  # 坐标[x, y]
        # 预留
        self.shield = False
        self.wind_fury = False
        self.skill1 = None
        self.skill2 = None
        self.skill3 = None
        self.passive = None
        self.spell_dmg = 0

    def attack(self, target, dmg):
        total_dmg = dmg * BaseEntity.damage_advantage[self.role][target.role]
        target.health -= total_dmg
        return total_dmg

    def heal(self, target, hp):
        total_hp = hp + self.spell_dmg
        target.health += total_hp
        return total_hp

    def buff(self, target, attribute):
        """ attribute为buff后的属性例如 {'atk':10, 'health':20}指buff后身材为10 / 20 """
        self.__dict__.update(attribute)

    def __str__(self) -> str:
        return self.__dict__.__str__()
