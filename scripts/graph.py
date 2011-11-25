from org.tiling.tournesol import GrowthListener

from pawt import swing, awt, colors

import java.io

import math, pickle, os

class Chart(swing.JComponent):
    color = colors.black
    style = 'Line'

    def getPreferredSize(self):
        return awt.Dimension(300,200)

    def paint(self, graphics):
        clip = self.bounds
        graphics.color = colors.white
        graphics.fillRect(0, 0, clip.width, clip.height)

        width = int(clip.width * .8)
        height = int(clip.height * .8)
        x_offset = int(clip.width * .1)
        y_offset = clip.height - int(clip.height * .1)

        N = len(self.data); xs = [0]*N; ys = [0]*N

        xmin, xmax = 0, N-1
        ymax = max(self.data)
        ymin = min(self.data)

        if abs(ymax - ymin) < 0.01:
          ymax = ymax + 0.005
          ymin = ymin - 0.005

        zero_y = y_offset - int(-ymin/(ymax-ymin)*height)
        zero_x = x_offset + int(-xmin/(xmax-xmin)*width)

        for i in range(N):
            xs[i] = int(float(i)*width/N) + x_offset
            ys[i] = y_offset - int((self.data[i]-ymin)/(ymax-ymin)*height)
        graphics.color = self.color
        if self.style == "Line":
            graphics.drawPolyline(xs, ys, len(xs))
        else:
            xs.insert(0, xs[0]); ys.insert(0, zero_y)
            xs.append(xs[-1]); ys.append(zero_y)
            graphics.fillPolygon(xs, ys, len(xs))

        # draw axes
        graphics.color = colors.black
        graphics.drawLine(x_offset,zero_y, x_offset+width, zero_y)
        graphics.drawLine(zero_x, y_offset, zero_x, y_offset-height)

        # draw labels
        leading = graphics.font.size
        graphics.drawString("%.3f" % xmin, x_offset, zero_y+leading)
        graphics.drawString("%.3f" % xmax, x_offset+width, zero_y+leading)
        graphics.drawString("%.3f" % ymin, zero_x-50, y_offset)
        graphics.drawString("%.3f" % ymax, zero_x-50, y_offset-height+leading)

class GraphViewer(swing.JInternalFrame, GrowthListener):
  def __init__(self, title, f):
    swing.JInternalFrame.__init__(self, title, 1)
    self.f = f
    self.numelements = 100
    self.scaledf = lambda f, x: f(x * 2 * math.pi / 100)

    self.chart = Chart(visible=1)
    self.contentPane.layout = awt.BorderLayout()
    self.contentPane.add(self.chart, awt.BorderLayout.CENTER)
    self.update()
    self.visible = 1
    self.size = self.getPreferredSize()

  def afterAddingElement(self, event):
    pass

  def beforeAddingElement(self, event):
    self.update()

  def finishedGrowing(self, event):
    pass

  def update(self):
    numbers = [0]*self.numelements
    for x in xrange(self.numelements):
        numbers[x] = apply(self.scaledf, (self.f, x))
    self.chart.data = numbers
    self.chart.repaint()

class PlotterViewer(swing.JInternalFrame, GrowthListener):
  def __init__(self, title):
    swing.JInternalFrame.__init__(self, title, 1)

    self.chart = Chart(visible=1)
    self.chart.data = [0.0]
    self.contentPane.layout = awt.BorderLayout()
    self.contentPane.add(self.chart, awt.BorderLayout.CENTER)
    self.update(2)
    self.visible = 1
    self.size = self.getPreferredSize()

  def afterAddingElement(self, event):
    self.update(event.plant.divergences[-1])

  def beforeAddingElement(self, event):
    pass

  def finishedGrowing(self, event):
    pass

  def update(self, value):
    self.chart.data.append(value)
    self.chart.repaint()
