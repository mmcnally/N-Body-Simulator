// Density Constant (can be removed to have differing desnity objects)
//var D = Math.pow(10,28);
var D = 1;

// name: string,
// mass: int
// pos: array of 2 ints
// vel: array of 2 ints
// color: rgb color
var Body = function(name, mass, pos, vel, color){
  radius = mass/D;
  return {'name': name, 'mass': mass, 'radius': radius, 'pos': pos, 'vel': vel, 'color' : color};
}
