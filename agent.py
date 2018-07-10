# -*- coding: utf-8 -*-
"""
Created on Tue May 29 20:16:44 2018

@author: Leo
"""


# 确定主体的位置坐标
class Position():

    def __init__(self, position):
        self. x = position[0]
        self. y = position[1]


#  染色体:tag  control 片段（先只写标识tag片段）
class Chromosome():

    def __init__(self, offense_tag, defense_tag):
        self. offense_tag = offense_tag
        self. defense_tag = defense_tag


# 资源
class Resource():

    def __init__(self, founders, capitals, fans):
        self. founders = founders
        self. capitals = capitals
        self. fans = fans


#    主体
class Agent(Position, Chromosome):

    def __init__(self, position,
            offense_tag=None,
            defense_tag=None,
            founders=None,
            capitals=None,
            fans=None):
        #   坐标
        Position. __init__(self, position)
        #   染色体
        Chromosome. __init__(self, offense_tag, defense_tag)
        #   资源
        Resource. __init__(self, founders, capitals, fans)

    def get_position(self):
        return [self.x, self.y]

    def get_resource(self):
        return sum([self. founders, self. capitals, self. fans])
