import pygame
import math
import random
import numpy as np


class Particle:
    def __init__(self,game,pos,ptype):
        self.game = game
        self.pos = list(pos)
        self.ptype = ptype
        self.movement = (0,0)
        self.velocity = [0,0]
        self.interaction_range = 100
    
    def update(self,particle_list,attraction_matrix):
        p1pos = self.pos


        p_forces =[]   
    #look through list of particles and find any within the interaction range
        self.velocity[0] = 0
        self.velocity[1] = 0
        runstuff = 1
        if runstuff == 1:
            for particle in particle_list:
                
                #position
                p2pos = particle.pos
                #if itself then ignore
                if p2pos == p1pos:
                    continue
                
                #get distance.
                distance = np.sqrt((p2pos[0]-p1pos[0])**2+(p2pos[1]-p1pos[1])**2)
                #distance = 200
                if distance > self.interaction_range:
                    continue
                else:
                    #within interaction range

                    #Find the vector
                    vector = [p2pos[0]-p1pos[0],p2pos[1]-p1pos[1]]
                    norm = np.linalg.norm(vector)
                    vec_norm = vector/norm

                    #calc relative force. This is a function of distance AND the attraction matrix.
                    attraction = attraction_matrix[self.ptype,particle.ptype]

                    #If too close push away:
                    if distance < 3:
                        force = vec_norm*-1
                    else:
                        if distance <= 50:
                            f_mag =  (1/47*distance - 3/47)*attraction
                        elif distance > 50:
                            f_mag = (-1/47*distance+1+50/47)*attraction
                        force = vec_norm*f_mag
                    p_forces.append(force)
            
            f_total = sum(p_forces)

            if len(p_forces) > 0:
                self.velocity[0] = f_total[0]
                self.velocity[1] = f_total[1]
            else:
                self.velocity[0] = random.random()
                self.velocity[1] = random.random()


            #periodic boundaries:
            if self.pos[0] > self.game.x_res:
                self.pos[0] = 1.0
            elif self.pos[0] < 0:
                self.pos[0] = self.game.x_res-1
            
            if self.pos[1] > self.game.y_res:
                self.pos[1] = 1.0
            elif self.pos[1] < 0:
                self.pos[1] = self.game.y_res-1

        self.pos[0] = self.pos[0] + self.velocity[0]
        self.pos[1] = self.pos[1] + self.velocity[1]




    def render(self,surf):
        if self.ptype == 0:
            colour = (255,0,0)
        elif self.ptype == 1:
            colour = (0,255,0)
        elif self.ptype == 2:
            colour = (0,0,255)
        else:
            colour = (255,255,255)

        shape = pygame.Rect(self.pos[0],self.pos[1],5,5)
        
        pygame.draw.rect(surf,colour,shape)
        #pygame.draw.circle(surf,colour,self.pos,3)