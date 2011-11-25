import unittest, integration

class IntegrationTest(unittest.TestCase):
  """I test the numerical integration functions. The data is from
  Elementary Differential Equations and Boundary Value Problems by Boyce and DiPrima."""

  def assertEqualsRange(self, first, second, tolerance, msg=None):
    """Fail if the two numbers differ by more than the given tolerance.
    """
    if abs(first - second) > tolerance:
        raise self.failureException, (msg or '%s != %s' % (first, second))

  def testEuler(self):
    expected = (1.5000000, 2.1900000, 3.1460000, 4.4744000, 6.3241600, \
                8.9038240, 12.505354, 17.537495, 24.572493, 34.411490)
    self.check(integration.euler, expected);

  def testHeun(self):
    expected = (1.5950000, 2.4636000, 3.7371280, 5.6099494, 8.3697252, \
                12.442193, 18.457446, 27.348020, 40.494070, 59.938223)
    self.check(integration.heun, expected);

  def testRungeKutta(self):
    expected = (1.6089333, 2.5050062, 3.8294145, 5.7927853, 8.7093175, \
                13.047713, 19.507148, 29.130609, 43.473954, 64.858107)
    self.check(integration.rungeKutta, expected);

  def check(self, integrationFormula, expected):
    f = lambda t, y: 1 - t + 4 * y
    t = 0
    y = 1
    h = 0.1

    for e in expected:
      y = integrationFormula(f, t, y, h)
      t = t + h
      self.assertEqualsRange(e, y, 0.000001)

    # The exact value at t = 1 is 64.897803

  def testEuler2(self):
    expected = ((1.1, -0.1), (1.25, -0.22))
    self.check2(integration.euler2, expected, 0.1);

  def testRungeKutta2(self):
    expected = ((1.3200667, -0.25066667),)
    self.check2(integration.rungeKutta2, expected, 0.2);

  def check2(self, integrationFormula, expected, h):
    f = lambda t, x, y: x - 4 * y
    g = lambda t, x, y: -x + y
    t = 0
    x = 1
    y = 0

    for e in expected:
      x, y = integrationFormula(f, g, t, x, y, h)
      t = t + h
      self.assertEqualsRange(e[0], x, 0.000001)
      self.assertEqualsRange(e[1], y, 0.000001)

    # The exact value at t = 0.2 is (1.3204248, -0.25084701)


if __name__ == '__main__':

  unittest.main()


