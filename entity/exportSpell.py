# -*- coding: utf-8 -*-
from hearthstone.mercenaryxml import MercenaryXML, load

a = load(locale='zhCN')

for i, x in a[0].items():
    print(x.specializations)
    break
