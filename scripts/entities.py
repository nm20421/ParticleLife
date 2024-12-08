import pygame
import math
import random
import numpy as np
from numba import jit, int32, float32
from numba import cuda



@jit(nopython=True,cache=True)
def update(part,particle_list,local_particles,attraction_matrix,x_res,y_res):
    p1pos = particle_list[part,0:2]
    ptype1 = int(particle_list[part,2])

    pos = p1pos
    mid_range = 51.5
    min_range = 15
    interaction_range = 100


#look through list of particles and find any within the interaction range
    velocity = [0,0]
    f_total = [0,0]

    p_forces = []
    runstuff = 1
    if runstuff == 1:
        for particle in local_particles:
            
            #position
            p2pos = particle_list[particle,0:2]

            #p2pos[0] = (p2pos[0]+x_res)%x_res
            #p2pos[1] = (p2pos[1]+y_res)%y_res
            ptype2 = int(particle_list[particle,2])
            #if itself then ignore
            if p2pos[0] == p1pos[0] and p2pos[0] == p1pos[0]:
                continue
            
            #get distance.
            distance = np.sqrt((p2pos[0]-p1pos[0])**2+(p2pos[1]-p1pos[1])**2)
            #distance = 200
            if distance > interaction_range:
                continue
            else:
                #within interaction range

                #Find the vector
                vector = np.array([p2pos[0]-p1pos[0],p2pos[1]-p1pos[1]], dtype=np.float64)
                #vector = [p2pos[0]-p1pos[0],p2pos[1]-p1pos[1]]
                norm = np.linalg.norm(vector)
                vec_norm = vector/norm

                #calc relative force. This is a function of distance AND the attraction matrix.
                attraction = attraction_matrix[ptype1,ptype2]

                #If too close push away:
                if distance < min_range:
                    force = vec_norm*-1
                else:
                    if distance <= interaction_range/2:
                        f_mag =  (1/(mid_range-min_range)*distance - min_range/(mid_range-min_range))*attraction
                    elif distance > interaction_range/2:
                        f_mag = (-1/(mid_range-min_range)*distance+1+mid_range/(mid_range-min_range))*attraction
                    force = vec_norm*f_mag
                p_forces.append(force)
        a = len(p_forces)
        p_f = np.zeros((len(p_forces),2))

        for i in range(0,len(p_f)):
            p_f[i,0] = p_forces[i][0]
            p_f[i,1] = p_forces[i][1]
        #p_forces = np.array(p_forces,dtype=np.float64)

        if len(p_forces) != 0:
            f_total[0] = np.sum(p_f[:,0])
            f_total[1] = np.sum(p_f[:,1])

        if len(p_forces) > 0:
            velocity[0] = f_total[0]
            velocity[1] = f_total[1]
        else:
            velocity[0] = random.random()*19
            velocity[1] = random.random()*10

        
        #periodic boundaries:
        #if pos[0] > x_res:
        #    pos[0] = 1.0 + velocity[0]
        #elif pos[0] < 0:
        #    pos[0] = x_res-1 + velocity[0]
        
        #if pos[1] > y_res:
        #    pos[1] = 1.0 + velocity[0]
        #elif pos[1] < 0:
        #    pos[1] = y_res-1 + velocity[0]

    pos[0] = pos[0] + velocity[0]
    pos[1] = pos[1] + velocity[1]



    return pos




def render(surf,particle):
    ptype = particle[2]
    pos = particle[0:2]
    if ptype == 0:
        colour = (255,0,0)
    elif ptype == 1:
        colour = (0,255,0)
    elif ptype == 2:
        colour = (0,0,255)
    elif ptype == 3:
        colour = (243,100,100)
    elif ptype == 4:
        colour = (0,100,255)
    elif ptype == 5:
        colour = (255,0,255)
    elif ptype == 6:
        colour = (200,0,55)
    else:
        colour = (0,0,0)

    shape = pygame.Rect(pos[0],pos[1],5,5)
    
    pygame.draw.rect(surf,colour,shape)
    #pygame.draw.circle(surf,colour,self.pos,3)