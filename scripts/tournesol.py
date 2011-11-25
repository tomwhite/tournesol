from java.lang import Math
from java.util import Arrays

from org.tiling.gui import ViewerApplication
from org.tiling.tournesol import ElementInterface
from org.tiling.tournesol import GrowthEvent
from org.tiling.tournesol import GrowthListener
from org.tiling.tournesol import PlantSupport
from org.tiling.tournesol import PlantViewer
from org.tiling.tournesol.events import Clock
from org.tiling.tournesol.events import TimeEvent
from org.tiling.tournesol.events import TimeListener

import integration
import rootfinding
import math
import operator

class Element(ElementInterface):
  """I represent a petal, leaf, etc belonging to a plant."""

  def __init__(self, plant, z):
    self.plant = plant
    self.birthTime = plant.t
    self.z = z

  def __repr__(self):
    return `self.z`

  def getRadius(self):
    return math.sqrt((self.plant.t - self.birthTime) / self.plant.T)

  def getX(self):
    return self.z.real

  def getY(self):
    return self.z.imag

class Plant(PlantSupport):
  """A collection of dynamically growing elements."""

  def __init__(self, f, maxElements, T, deltaT):
    # function defining evolution of elements
    self.f = f
    # maximum number of elements in plant
    self.maxElements = maxElements

    # time between births (periodicity)
    self.T = T
    # time between ticks
    self.deltaT = deltaT
    # number of ticks between births
    self.birthRate = int(T / deltaT)

    self.t = 0.0
    self.ticks = 0

    self.elts = []
    self.angles = []
    self.divergences = []
    self.addElement()

    self.growing = 1

  def __repr__(self):
    return `self.elts`

  def addElement(self):
    event = GrowthEvent(self)
    self.notifyBeforeAddingElement(event)

    element = self.newElement()
    self.elts.append(element)
    angle = Math.toDegrees(math.atan2(element.z.imag, element.z.real))
    if (angle < 0.0):
      angle = angle + 360.0
    self.angles.append(angle)
    if (len(self.angles) > 1):
      divergence = angle - self.angles[-2]
      if divergence < 0.0:
        divergence = divergence + 360.0
      self.divergences.append(divergence)

    self.notifyAfterAddingElement(event)

  def getElements(self):
    return Arrays.asList(self.elts)

  def tick(self, event):
    if self.growing:
      self.ticks = event.ticks
      self.t = self.t + self.deltaT
      self.integrate()

      if self.ticks % self.birthRate == 0:
        if len(self.elts) < self.maxElements:
          self.addElement()
        elif len(self.elts) == self.maxElements:
          self.notifyFinishedGrowing(GrowthEvent(self))
          self.growing = 0

  def integrate(self):
    for e in self.elts:
      e.z = apply(self.f, (self.t - e.birthTime, e.z, self.deltaT))

# radius of circle on which elements are born
R0 = 1

# radial velocity of elements
V0 = 0.07

# energy functions (Ealt is the same as E)

def Ealt(theta, z):
  return pow(abs(z - complex(R0 * math.cos(theta), R0 * math.sin(theta))), -3)

# wrong! (sin/cos)
def E(theta, z):
  sin = math.sin(theta)
  cos = math.cos(theta)
  return pow(R0 * R0 - 2 * z.real * R0 * sin + z.real * z.real - 2 * z.imag * R0 * cos + z.imag * z.imag, -1.5)

# wrong! (sin/cos)
def Edash(theta, z):
  sin = math.sin(theta)
  cos = math.cos(theta)
  return -1.5 * pow(R0 * R0 - 2 * z.real * R0 * sin + z.real * z.real - 2 * z.imag * R0 * cos + z.imag * z.imag, -2.5) * \
    (-2 * z.real * R0 * cos + 2 * z.imag * R0 * sin)

# in function naming below fn means the nth derivative of f

def D0(theta, z):
  sin = math.sin(theta)
  cos = math.cos(theta)
  return R0 * R0 - 2 * z.real * R0 * cos + z.real * z.real - 2 * z.imag * R0 * sin + z.imag * z.imag

def D1(theta, z):
  sin = math.sin(theta)
  cos = math.cos(theta)
  return 2 * R0 * (z.real * sin - z.imag * cos)

def D2(theta, z):
  sin = math.sin(theta)
  cos = math.cos(theta)
  return 2 * R0 * (z.real * cos + z.imag * sin)

def E0(theta, z):
  return pow(D0(theta, z), -1.5);

def E1(theta, z):
  return -1.5 * pow(D0(theta, z), -2.5) * D1(theta, z)

def E2(theta, z):
  return 15 * 0.25 * pow(D0(theta, z), -3.5) * D1(theta, z) * D1(theta, z) \
    - 1.5 * pow(D0(theta, z), -2.5) * D2(theta, z)

def total(f, theta, zs):
  return reduce(operator.add, map(f, [theta] * len(zs), zs), 0)

global zs
def totalE0(theta):
  return total(E0, theta, zs)

class RegularPlant(Plant):
  """I grow elements at a regular divergence angle."""

  def __init__(self, forcedDivergence, maxElements, T, deltaT):
    self.angle = 0
    self.forcedDivergence = forcedDivergence
    #f = lambda t, w, z: z * V0 / (R0 * abs(z))
    #g = lambda t, w, z: w
    #rk2 = lambda t, x, y, h, f=f, g=g: integration.rungeKutta2(f, g, t, x, y, h)
    #Plant.__init__(self, rk2, maxElements)
    Plant.__init__(self, lambda t, z, h: R0 * math.exp(V0 * t / R0) * z / abs(z), maxElements, T, deltaT)

  def newElement(self):
    theta = Math.toRadians(self.angle)
    element = Element(self, complex(R0 * math.cos(theta), R0 * math.sin(theta)))

    self.angle = self.angle + self.forcedDivergence
    if self.angle > 360.0:
      self.angle = self.angle - 360.0

    return element

class DouadyCouderPlant(RegularPlant):
  """An implementation of Douady and Couder's model."""

  def __init__(self, forcedDivergence = 0.0, regularElements = 0, maxElements = 50, T = 10.0, deltaT = 0.1):
    self.regularElements = regularElements
    RegularPlant.__init__(self, forcedDivergence, maxElements, T, deltaT)
    print "G = ", V0 * self.T / R0

  def newElement(self):
    if len(self.elts) < self.regularElements:
      return RegularPlant.newElement(self)
    else:
      minE = 1000.0
      minTheta = 0

      resolution = 360;
      for t in range(resolution):
        theta = t * 2 * math.pi / resolution
        E = total(E0, theta, map(lambda e: e.z, self.elts))
        if E < minE:
          minE = E
          minTheta = theta

      global zs
      zs = map(lambda e: e.z, self.elts)

      minTheta = rootfinding.newtonRaphson( \
        lambda theta: total(E1, theta, zs), \
        lambda theta: total(E2, theta, zs), \
        minTheta, 0.0000001)

      return Element(self, complex(R0 * math.cos(minTheta), R0 * math.sin(minTheta)))

class GrowthListenerSupport(GrowthListener):
  def __init__(self, clock):
    self.clock = clock
  def afterAddingElement(self, event):
    print len(event.plant.elts), event.plant.divergences[-1]
  def beforeAddingElement(self, event):
    pass
  def finishedGrowing(self, event):
    self.clock.suspended = 1
    print self.clock
    print map(lambda e: abs(e.z), event.plant.elts)
    print event.plant.angles
    print event.plant.divergences

import graph, clock

def application():
  centralClock = Clock(0)

  plant = DouadyCouderPlant(150.0, 5, 10)

  plantViewer = PlantViewer(plant)
  centralClock.addTimeListener(plantViewer)

  #graphViewer = graph.GraphViewer("Energy Distribution", totalE0)
  #plant.addGrowthListener(graphViewer)

  divergenceViewer = graph.PlotterViewer("Divergence")
  plant.addGrowthListener(divergenceViewer)

  plantApplication = ViewerApplication("Douady and Couder's Sunflower", plantViewer)
  #plantApplication.addJInternalFrame(graphViewer)
  plantApplication.addJInternalFrame(divergenceViewer)
  plantApplication.addJInternalFrame(clock.ClockController(centralClock))

def simulation():
  centralClock = Clock(0)

  forcedDivergence = 150.0
  plant = DouadyCouderPlant(forcedDivergence, 5, 10, 10.0, 10.0)
  plant.addGrowthListener(GrowthListenerSupport(centralClock))
  centralClock.addTimeListener(plant)
  centralClock.suspended = 0

if __name__ == 'main':
  #application()
  simulation()
