// Density Constant (can be removed to have differing desnity objects)
//var D = Math.pow(10,28);
var D = 1;

var Body = function(name, mass, pos, vel, color){
  radius = mass/D;
  return {'name': name, 'mass': mass, 'radius': radius, 'pos': pos, 'vel': vel, 'color' : color};
}
