import sys
import pygame
import numpy as np
import random
import math 
from numba import jit, int32, float32
from numba.experimental import jitclass
from scripts.entities import *


def fps_counter(display):
    font = pygame.font.SysFont("Arial" , 18 , bold = True)
    fps = str(int(clock.get_fps()))
    fps_t = font.render(fps , 1, pygame.Color("RED"))
    display.blit(fps_t,(0,0))

def flatten(xss):
    return [x for xs in xss for x in xs]

def run(x_res,y_res):
    while True:
    #self.display.blit(self.assets['background'],[0,0])
        display.fill((0,0,0))



        for part in range(0,len(particle_list)):

            #This need changnig to only add in grids
            rangeG = 1
            local_particles = []
            g_row = int(particle_list[part,3])
            g_col = int(particle_list[part,4])

            for row in range(-1,2):
                for col in range(-1,2):
                    #Wrap around:
                    row_val =int((row+g_row+y_res)%y_res)
                    col_val =int((col+g_col+x_res)%x_res)
                    if row_val >= grid_rows:
                        row_val = 0
                    if col_val >= grid_cols:
                        col_val = 0
                    local_particles.append(grid[row_val][col_val])
                    #print(row,col)
            local_particles = flatten(local_particles)
            local_particles = np.array(local_particles)

            pos = update(part,particle_list,local_particles,attraction_matrix,x_res,y_res)
            particle_list[part,0:2] = pos
            render(display,particle_list[part])

            #now use pos to remove particle from old grid and add to new grid.
            new_g_row = int(math.floor(pos[1]/interaction_range))
            new_g_col = int(math.floor(pos[0]/interaction_range))

            g_row = new_g_row
            g_col = new_g_col



        for event in pygame.event.get():
            #event is an input of some description
            #CLose window event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        fps_counter(display)
        #Scale up screen
        screen.blit(pygame.transform.scale(display, screen.get_size()),(0,0))
        pygame.display.update()
        #Force game to run at 60 FPS
        clock.tick(60)








    # This function allows us to call screen and clock in any future functions containing (self) as an initialisation
pygame.init()

        #Create screen
        #Set windows name
pygame.display.set_caption("Particle Life!")
# resolution of window
x_window = 1400
y_window = 1000

#scale of game. >1 means smaller pixels, <1 means bigger pixels
scale = 1


x_res = x_window*scale
y_res = y_window*scale
screen = pygame.display.set_mode((x_window,y_window))

        # To scale up the screen we render at a smaller size then scale it up.
        #Create a black box with 320,240 size.
display = pygame.Surface((x_res,y_res))

        #self.particle = Particle(self,(1,1),)

        #set max FPS
clock = pygame.time.Clock()
        #Tilemap load
        #self.tilemap = Tilemap(self,tile_size=20)

        #Camera


n_particles = 2000
particle_list = np.zeros([n_particles,5])
n_particle_types = 5


#define sub-regions
interaction_range = 100

grid_rows = int(y_res/interaction_range)
grid_cols = int(x_res/interaction_range)

#create list of lists
grid = [ [] for _ in range(grid_rows)]
for row in range(0,grid_rows):
    grid[row] = [ [] for _ in range(grid_cols)]


#create particvles
for particle in range(0,n_particles):
    position = [int(random.random()*x_res),int(random.random()*y_res)]
    ptype = int(random.random()*n_particle_types)

    #Find grid that each particle is in and add to list of lists
    g_row = int(math.floor(position[1]/interaction_range))
    g_col = int(math.floor(position[0]/interaction_range))
    grid[g_row][g_col].append(particle)

    particle_list[particle,0] = position[0]
    particle_list[particle,1] = position[1]
    particle_list[particle,2] = ptype 
    particle_list[particle,3] = g_row 
    particle_list[particle,4] = g_col 
        
        #set up attraction matrix
    attraction_matrix = np.zeros([n_particle_types,n_particle_types])

for row in range(0,n_particle_types):
    for col in range(0,n_particle_types):
        if row == col:
            attraction_matrix[row,col] = 1#*random.random()*(1-(-1))+-1
        else:
            attraction_matrix[row,col] = 1*random.random()*(1-(-1))+-1
print(attraction_matrix)






#run simulation
run(x_res,y_res)

