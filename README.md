# N-Body-Simulator

Simulates the movement of objects through space. No force other than the gravitational pull of the other bodies is taken into account
within this model. The brute force method for implementing an N-body simulation has a runtime complexity of O(N^2), in order to reduce the
runtime complexity this simulator makes use of the <a href="http://arborjs.org/docs/barnes-hut" title="Title">The Barnes-Hut Algorithm</a>. The Barnes-Hut Algorithm, utilizes the divide and conquer
programming methodology to recursively break the planets into four groups each stored in a quad-tree. After recurring until every quadrant holds one or zero planets
the algorithm can utilize the center of mass and total mass of the nodes within the quad-tree to effectively reduce the runtime complexity to O(NlogN).

## Functionality

### Creating new bodies

- New Bodies
  - To create a new body <b>click</b>.
  - To create a new body with initial velocity <b>click and drag</b>.
  - To set the size of new bodies, use the <B>range slider</B> on the top left of the screen.

- To reset the universe hit the escape key.

#####Practice makes perfect!
