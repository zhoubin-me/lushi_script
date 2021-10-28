if __name__ == '__main__':
    from hearthstone.enums import CardType, Zone, GameTag
    from hslog import LogParser, packets
    from hslog.export import EntityTreeExporter

    parser = LogParser()
    with open("test.log", encoding='utf-8') as f:
        parser.read(f)
    parser.flush()
    # 最近一场战斗
    packet_tree = parser.games[-1]
    exporter = EntityTreeExporter(packet_tree, player_manager=parser.player_manager)
    a = exporter.export()
    game = a.game
    for e in game.initial_entities:
        # 获取随从信息
        if e.type == CardType.MINION:
            # e.tags.get() 获取属性
            # GameTag.ENTITY_ID 佣兵id
            # GameTag.ATK 攻击力
            # GameTag.HEALTH 血量
            # GameTag.ZONE 是否上场，死亡
            # GameTag.ZONE_POSITION  获取战场位置 从左往右1开始
            # INVALID = 0 施法者CASTER = 1 斗士FIGHTER = 2 TANK = 3 NEUTRAL = 4
            # GameTag.LETTUCE_ROLE   : INVALID = 0 施法者CASTER = 1 斗士FIGHTER = 2 护卫TANK = 3  无NEUTRAL = 4
            # GameTag.CARDRACE 种族
            # 以下为技能
            # 查询技能主人
            # GameTag.LETTUCE_ABILITY_OWNER
            # GameTag.COST 技能速度
            # GameTag.LETTUCE_ROLE 技能属性： 护卫 施法者 斗士
            # GameTag.SPELL_SCHOOL 法术种类： 神圣 火焰...

            # print(e, e.type, e.zone, end='\n\n\n')
            # 打印攻击力
            print(e.tags.get(GameTag.ATK))
            pass

    pass
