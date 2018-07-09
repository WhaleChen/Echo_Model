# -*- coding: utf-8 -*-
"""
Created on Tue May 29 21:29:41 2018

@author: Leo
"""


import agent as gt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import animation




#   生成基因序列
def gene_sequence(k, gene):
    genes = []
    for i in range(sum(k)+1):
        if i < k[0]:
            genes.append(gene[0])
        if i < k[1]+k[0] and i >= k[0]:
            genes.append(gene[1])
        if i >= k[1]+k[0]:
            genes.append(gene[2])
    return genes

# 定义主体之间的距离
def distance_agents(agents):
    agents_num = len(agents)
    dists = []
    for i in range(agents_num):
        temp = []
        for j in range(agents_num):
            if i != j:
                d = np.sqrt((agents[j].y - agents[i].y)**2 + (agents[j].x - agents[i].x)**2)
            else:
                d = 0
            temp.append(d)
        dists.append(temp)
    return dists
   
#   两个主体交互，标识匹配   (匹配：2,不匹配：-2,超出：1)    
def tag_match_score(offense_tag, defense_tag):
    len_o = len(offense_tag)
    len_d = len(defense_tag)
    len_match = min(len_o, len_d)
    score = 0
    for i in range(len_match):
        if offense_tag[i] == defense_tag[i]:
            score = score + 2
        else:
            score = score - 2
    
    score += (len_o - len_d)
#    if len_o >len_d:
#        score += (len_o - len_d)
#    else:
#        score -= (len_o - len_d)    
    return score

#   根据标识匹配得分（score）交换资源[+-,--,-+,++]
def exchangge(agent1,agent2, score_1, score_2):
    if max(score_1, score_2) > 0:
        if score_1 > score_2:
            ex_rate = (score_1 - max([0, score_2]))/score_1*0.8
            
            agent1. founders +=  (agent2. founders) * ex_rate
            agent1. capitals +=  (agent2. capitals) * ex_rate
            agent1. fans +=  (agent2. fans) * ex_rate
            
            agent2. founders =  (agent2. founders) * (1 - ex_rate)
            agent2. capitals =  (agent2. capitals) * (1 - ex_rate)
            agent2. fans =  (agent2. fans) * (1 - ex_rate)
            
            print(1)
            
            
        else:
            ex_rate = (score_2 - max([0,score_1]))/score_2*0.8
            
            agent2. founders +=  (agent1. founders) * ex_rate
            agent2. capitals +=  (agent1. capitals) * ex_rate
            agent2. fans +=  (agent1. fans) * ex_rate
            
            agent1. founders =  (agent1. founders) * (1 - ex_rate)
            agent1. capitals =  (agent1. capitals) * (1 - ex_rate)
            agent1. fans =  (agent1. fans) * (1 - ex_rate)
            print(2)
    else:
        print('未交换资源')
    #   交互完成 两个主体随机游走
    temp1 = np.random.randint(-1,2)
    temp2 = np.random.randint(-1,2)
    temp3 = np.random.randint(-1,2)
    temp4 = np.random.randint(-1,2)
        
    if agent1.x + temp1 <= maxy and agent1.x + temp1 >= maxx :
       agent1.x += temp1
    if agent1.y + temp2 <= maxy and agent1.y + temp2 >= maxx:
       agent1.y += temp2
       
    if agent2.x + temp3 <= maxy and agent2.x + temp3 >= maxx:
       agent2.x += temp3          
    if agent2.y + temp4 <= maxy and agent2.y + temp4 >= maxx:
       agent2.y += temp4
     
    print('Resource exchange has finished!')          
 
    
#   获取所有主体的 位置 和 资源信息
def get_agents_position(agents):
    position = []
    resource_total = []
    for agent in agents:
        position.append(agent.get_position())
        resource_total.append(agent.get_resource())
    return position, resource_total


#   主体之间进行进攻防御交互
def offense_defense(agents):
    dist = distance_agents(agents)
    for i in range(len(agents)):
        temp = [k*(-1) for k in dist[i]]
        j = temp.index(min(temp))  # 与第 i 主体最近的主体 index = j (-号排除了离自己最近)
        score_i = tag_match_score(agents[i].offense_tag, agents[j].defense_tag)
        score_j = tag_match_score(agents[j].offense_tag, agents[i].defense_tag)
        
        # 根据得分设定资源交换  并随机游走
        exchangge(agents[i],agents[j], score_i, score_j)
        
    #   获取交互完成以后的主体 位置 和 资源
    position_agent, resource_total = get_agents_position(agents) 
    
    return position_agent, resource_total

#==========================================函数主体  上面定义小功能 ==============================


## 数据预处理，定义位置、主体、资源  （预设）
#maxx, maxy = 100,100   # 世界的大小
#agent_num = 3         # 主体的起始数量
#resource_kind = 3      # 资源种类
#resource_num = 10      # 资源数量



def data_process(maxx, maxy, agent_num, resource_kind, resource_num):
    # 路由矩阵
    agents_mat = np.zeros([maxy - maxx, maxy - maxx])   # 主体路由矩阵
#    resource_mat = np.zeros([maxx, maxy])   # 资源路由矩阵(暂时无用)
    
    
    # ==================================主体定义==================================================
    # 随机 主体定义起始点位置
    position_agent = np.random.randint(maxx, maxy, size=(agent_num, 2))  
    
    agents = []
    temp = []
    for i in range(agent_num):
        # 标识初始化
        temp1 = list(np.random.randint(0, 5, size=(1, 3))[0])
        temp2 = list(np.random.randint(0, 5, size=(1, 3))[0])
        
        offense = gene_sequence(temp1, ['a','b','c'])
        defense = gene_sequence(temp2, ['a','b','c'])
        
        # 主体资源初始化        
        founders = temp1[0] + temp2[0]
        capitals = temp1[1] + temp2[1]
        fans = temp1[2] + temp2[2]
        
            
        agents.append(gt. Agent(position = position_agent[i], offense_tag = offense, defense_tag = defense, founders = founders, capitals = capitals, fans = fans))
        agents_mat[position_agent[i][0]][position_agent[i][1]] = 1   # 标记有此位置有一个主体
      
        
        
    #=========================世界位置   资源初始化 【暂时不考虑】======================================================================
    resources = []
    
    for i in range(maxx):
        res_row = []
        for j in range(maxy):
            temp = list(np.random.randint(0, 5, size=(1, 3))[0])  # 分别代表三种资源的数量
            res_row.append(temp) 
        resources.append(res_row)
    return agents, agents_mat
            


     
# ===================================== 可视化过程 =====================================        


def init():
    p1.set_offsets([])
    return p1,


def update_scatter(i):
    #    获取新的数据
    position_agent, resource_total = offense_defense(agents)    
    x = np.array(position_agent)[:,0]
    y = np.array(position_agent)[:,1]
    
    #    传入新的数据
    p1.set_offsets([x,y])
    # Set sizes...
    p1._sizes = 100 * np.array(resource_total)
#    Set colors..
    p1.set_array(np.array(resource_total) )

        
    ax.set_xlabel('frame {0}'.format(i))
    return p1  


if __name__ == '__main__':
    
    # 数据预处理，定义位置、主体、资源  （预设）
    global maxx, maxy
    maxx, maxy = 0,100   # 世界的大小
    agent_num =  30        # 主体的起始数量
    resource_kind = 3      # 资源种类
    resource_num = 10      # 资源数量
    
    #======================= 预处理（以后为外部数据输入窗口）==================================
    agents, agents_mat = data_process(maxx, maxy, agent_num, resource_kind, resource_num)
        
    #===============================主体交互作用 ==============================================
    #   获得主体的位置以及大小（根据资源大小确定）
    position_agent, resource_total = get_agents_position(agents)    
    x = np.array(position_agent)[:,0]
    y = np.array(position_agent)[:,1]
    
    
    # ============================= 可视化 ===================================================
#    fig = plt.figure(figsize=(10, 10), facecolor="white")
#    ax = fig.add_subplot(111)
#    p1, = ax.plot(x, y, 'o', lw = 2)       
    
    fig = plt.figure()
    ax = plt.axes(xlim=(0-20, maxy+20), ylim=(0-20, maxy+20))
    p1 = ax.scatter(x, y, c = np.array(resource_total), marker = 'o', alpha = 0.8, cmap = 'viridis')
       
    plt.colorbar(p1)
    plt.grid(True)
    plt.title("Agent evolution ")
    plt.xlabel('x')
    plt.ylabel('y')



    anim = FuncAnimation(fig, update_scatter, init_func=init, frames = range(200), interval=200, repeat = True)
    plt.show() 
    
#    anim.save('/tmp/animation.gif', writer='imagemagick', fps=30)
    
#    mywriter = animation.FFMpegWriter(fps=10)
#    anim.save('/result/myanimation.mp4',writer=mywriter) 
    
#    anim.save('/result/animation.mp4')   






