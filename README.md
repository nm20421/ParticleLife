This program implements a particle life simulation in which particles interact with each other via an interaction matrix.

NB:
1. A repulsion is needed at very small distance to stop particles collapsing on on themselves.
2. The attraction matrix is defined randomly and represents the attraction at the mid point between the inter-particle repulsion and the end of particle interaction. The attraction decays linearly from this mid point. 

Requires the following python libraries:
random,
math,
numpy,
pygame


To run:
Simply download the files and run game.py
