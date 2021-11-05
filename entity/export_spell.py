# -*- coding: utf-8 -*-
from mercenaries import MERCENARIES

if __name__ == '__main__':
    m = MERCENARIES
    for h in m:
        id = h['skins'][-1][:-3]
        if not id.startswith('LETL_030H'):
            continue
        print(id)
        for abl in h['abilities']:
            print(abl['tiers'][-1][:-3])

        for equip in h['equipment']:
            print(equip['tiers'][-1][:-3])


        break
    pass
