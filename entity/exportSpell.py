# -*- coding: utf-8 -*-
from mercenaries import MERCENARIES

if __name__ == '__main__':
    m = MERCENARIES
    for h in m:
        id = h['skins'][0][:-3]
        print(id)
        for abl in h['abilities']:
            print(abl['tiers'][0][:-3])

        for equip in h['equipment']:
            print(equip['tiers'][0][:-3])


        break
    pass
