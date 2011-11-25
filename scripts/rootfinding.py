def newtonRaphson(f, fdash, x0, tolerance):
  """The Newton-Raphson method for finding a root of f(x) = 0, fdash = f'(x)
  and x0 is the initial guess. I may get stuck in an endless loop!
  """
  x = x0
  while 1:
    xold = x
    fx = f(x)
    fdashx = fdash(x)
    if fdashx == 0:
      return x
    x = x - f(x) / fdashx
    if abs(x - xold) < tolerance:
       return x
