def euler(f, t, y, h):
  """The Euler Method.
  y' = f(t, y) where t is typically time, h is the step size
  """
  return y + h * f(t, y)

def heun(f, t, y, h):
  """The Improved Euler Method, aka the Heun formula.
  y' = f(t, y) where t is typically time, h is the step size
  """
  return y + 0.5 * h * (f(t, y) + f(t + h, y + h * f(t, y)))

def rungeKutta(f, t, y, h):
  """The Runge-Kutta Method.
  y' = f(t, y) where t is typically time, h is the step size
  """
  k1 = f(t, y)
  k2 = f(t + 0.5 * h, y + 0.5 * h * k1)
  k3 = f(t + 0.5 * h, y + 0.5 * h * k2)
  k4 = f(t + h, y + h * k3)
  return y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

def euler2(f, g, t, x, y, h):
  """The Euler Method for two first order equations
  """
  return x + h * f(t, x, y), y + h * g(t, x, y)

def rungeKutta2(f, g, t, x, y, h):
  """The Runge-Kutta Method for two first order equations
  x' = f(t, x, y)
  y' = g(t, x, y)
  (So x'' = g(t, x, x') can be solved using y' = g(t, x, y), x' = f(t, x, y) = y)
  t is time
  h is the step size
  """
  k1 = f(t, x, y)
  l1 = g(t, x, y)

  k2 = f(t + 0.5 * h, x + 0.5 * h * k1, y + 0.5 * h * l1)
  l2 = g(t + 0.5 * h, x + 0.5 * h * k1, y + 0.5 * h * l1)

  k3 = f(t + 0.5 * h, x + 0.5 * h * k2, y + 0.5 * h * l2)
  l3 = g(t + 0.5 * h, x + 0.5 * h * k2, y + 0.5 * h * l2)

  k4 = f(t + h, x + h * k3, y + h * l3)
  l4 = g(t + h, x + h * k3, y + h * l3)

  return x + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4), y + (h / 6) * (l1 + 2 * l2 + 2 * l3 + l4)
