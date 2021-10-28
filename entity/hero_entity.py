from base_entity import BaseEntity


class HeroEntity(BaseEntity):

    def __init__(self):
        super().__init__()

    @classmethod
    def basic(cls, pos_x, pos_y, role, atk, health):
        e = HeroEntity()
        e.atk = atk
        e.health = health
        e.role = role  # 斗士
        e.pos = [pos_x, pos_y]
        return e
