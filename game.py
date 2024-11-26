import sys
import pygame
import numpy as np
import random
import math 

from scripts.entities import Particle


class Game:
    # This function allows us to call screen and clock in any future functions containing (self) as an initialisation
    def __init__(self):
        pygame.init()

        #Create screen
        #Set windows name
        pygame.display.set_caption("Particle Life!")
        #640,480 = resolution
        self.x_res = 1000
        self.y_res = 700
        self.screen = pygame.display.set_mode((self.x_res,self.y_res))

        # To scale up the screen we render at a smaller size then scale it up.
        #Create a black box with 320,240 size.
        self.display = pygame.Surface((1000,700))

        #self.particle = Particle(self,(1,1),)

        #set max FPS
        self.clock = pygame.time.Clock()
        #Tilemap load
        #self.tilemap = Tilemap(self,tile_size=20)

        #Camera
        self.scroll = [0,0]

        self.n_particles = 200
        self.particle_list = np.zeros([self.n_particles,3])
        self.n_particle_types = 3


        self.particle_list = []
        for particle in range(0,self.n_particles):
            position = [int(random.random()*self.x_res),int(random.random()*self.y_res)]
            ptype = int(random.random()*self.n_particle_types)

            self.particle_list.append(Particle(self,position,ptype))
        
        #set up attraction matrix
        self.attraction_matrix = np.zeros([self.n_particle_types,self.n_particle_types])

        for row in range(0,self.n_particle_types):
            for col in range(0,self.n_particle_types):
                if row == col:
                    self.attraction_matrix[row,col] = 1
                else:
                    self.attraction_matrix[row,col] = random.random()*(1-(-1))+-1
        print(self.attraction_matrix)


    def fps_counter(self):
        font = pygame.font.SysFont("Arial" , 18 , bold = True)
        fps = str(int(self.clock.get_fps()))
        fps_t = font.render(fps , 1, pygame.Color("RED"))
        self.display.blit(fps_t,(0,0))



    def run(self):
        while True:
        #self.display.blit(self.assets['background'],[0,0])
            self.display.fill((0,0,0))


            for particle in self.particle_list:
                particle.update(self.particle_list,self.attraction_matrix)
                particle.render(self.display)



            for event in pygame.event.get():
                #event is an input of some description
                #CLose window event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.fps_counter()
            #Scale up screen
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()),(0,0))
            pygame.display.update()
            #Force game to run at 60 FPS
            self.clock.tick(60)


Game().run()