if __name__ == '__main__':
    from hearthstone.enums import CardType, Zone, GameTag
    from hslog import LogParser, packets
    from hslog.export import EntityTreeExporter

    parser = LogParser()
    with open("C:\\Program Files (x86)\\Hearthstone\\Logs\\Power.log", encoding='utf-8') as f:
        parser.read(f)
    parser.flush()
    # 最近一场战斗
    packet_tree = parser.games[-1]
    exporter = EntityTreeExporter(packet_tree, player_manager=parser.player_manager)
    a = exporter.export()
    game = a.game
    for e in game.initial_entities:
        # 获取随从信息

        # 以下为游戏状态
        if e.type == CardType.GAME:
            # GameTag.ACTION_STEP_TYPE : 1为选择随从 0为战斗
            pass
        elif e.type == CardType.MINION:
            # e.tags.get() 获取属性
            # GameTag.ENTITY_ID 佣兵id
            # GameTag.ATK 攻击力
            # GameTag.HEALTH 血量
            # GameTag.ZONE 是否上场，死亡
            # GameTag.ZONE_POSITION  获取战场位置 从左往右1开始
            # INVALID = 0 施法者CASTER = 1 斗士FIGHTER = 2 TANK = 3 NEUTRAL = 4
            # GameTag.LETTUCE_ROLE   : INVALID = 0 施法者CASTER = 1 斗士FIGHTER = 2 护卫TANK = 3  无NEUTRAL = 4
            # GameTag.CARDRACE 种族
            # GameTag.WINDFURY 风怒
            # GameTag.DIVINE_SHIELD 圣盾
            # GameTag.LETTUCE_CONTROLLER 控制权

            # 场上随从
            # if e.tags.get(GameTag.ZONE) == Zone.PLAY:
            #     print(e.tags, end='\n\n')
            # print(e.tags.get(GameTag.ATK))
            pass
        # 佣兵技能信息
        elif e.type == CardType.LETTUCE_ABILITY:
            # 以下为技能
            # GameTag.LETTUCE_ABILITY_OWNER 技能主人
            # GameTag.COST 技能速度
            # GameTag.LETTUCE_ROLE 技能属性： 护卫 施法者 斗士
            # GameTag.SPELL_SCHOOL 法术种类： 神圣 火焰...
            # GameTag.LETTUCE_COOLDOWN_CONFIG 冷却
            # GameTag.LETTUCE_CURRENT_COOLDOWN 目前冷却
            print()
        print(e, e.tags, end='\n\n\n')
    pass
