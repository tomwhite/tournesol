from pawt import swing, awt

class ClockController(swing.JInternalFrame):
  def __init__(self, clock):
    swing.JInternalFrame.__init__(self, "Clock")
    self.clock = clock

    panel = swing.JPanel();
    self.start = swing.JButton("Start", actionPerformed = self.doStart)
    self.stop = swing.JButton("Stop", actionPerformed = self.doStop)
    self.updateButtons()
    panel.add(self.start)
    panel.add(self.stop)
    self.getContentPane().setLayout(awt.BorderLayout());
    self.getContentPane().add(panel, awt.BorderLayout.SOUTH);
    self.visible = 1

  def updateButtons(self):
    if self.clock.suspended:
      self.start.enabled = 1
      self.stop.enabled = 0
    else:
      self.start.enabled = 0
      self.stop.enabled = 1

  def doStart(self, event):
    self.clock.suspended = 0
    self.updateButtons()

  def doStop(self, event):
    self.clock.suspended = 1
    self.updateButtons()
