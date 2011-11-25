import math, unittest, rootfinding

class NewtonRaphsonTest(unittest.TestCase):
  """I test the Newton Raphson Method."""

  def assertEqualsRange(self, first, second, tolerance, msg=None):
    """Fail if the two numbers differ by more than the given tolerance.
    """
    if abs(first - second) > tolerance:
        raise self.failureException, (msg or '%s != %s' % (first, second))

  def test(self):
    f = lambda x: x * x - 2
    fdash = lambda x: 2 * x
    x0 = 1.0
    tolerance = 0.0000001
    self.assertEqualsRange(rootfinding.newtonRaphson(f, fdash, x0, tolerance), math.sqrt(2), tolerance)

if __name__ == '__main__':

  unittest.main()