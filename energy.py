from math import *
import operator

R0 = 0.1

def a(t,z):
  return pow(R0 * R0 * sin(t) * sin(t) - 2 * z.real * R0 * sin(t) + z.real * z.real + R0 * cos(t) * cos(t) - 2 * z.imag * R0 * cos(t) + z.imag * z.imag, -1.5)

def b(t, z):
  return a(t * 2 * pi/ 100, z)

def c(t, zs):
  return reduce(operator.add, map(b, [t] * len(zs), zs))
  
c(x, [3 + 4j, 1+2j, -1-3j, 8 -1j, -1+2j, 2 + 0j])