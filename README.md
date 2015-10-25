# N-Body-Simulator

Simulates the movement of objects through space. No force other than the gravitational pull of the other bodies is taken into account
within this model. The brute force method for implementing an N-body simulation has a runtime complexity of O(N^2), in order to reduce the
runtime complexity this simulator makes use of the The Barnes-Hut Algorithm. The Barnes-Hut Algorithm, utilizes the divide and conquer
methodology of programming and effectively reduces the runtime complexity to O(NlogN).

## Functionality

### Creating new bodies
