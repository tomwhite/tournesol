package org.tiling.tournesol.events;

import java.util.ArrayList;

/**
 * I am a ticking clock that may be stopped and started.
 * I am used to drive a dynamical system.
 * When constructed I am in the suspended state.
 */
public class Clock implements Runnable {
	private TimeEvent timeEvent = new TimeEvent(this);
	private ArrayList listeners = new ArrayList();
	private boolean suspended = true;
	private final int delayMilliseconds;
	private long millisecondsElapsed = 0;
	public Clock() {
		this(10);
	}
	public Clock(int delayMilliseconds) {
		this.delayMilliseconds = delayMilliseconds;
		new Thread(this).start();
	}
	public synchronized void addTimeListener(TimeListener listener) {
		if (!listeners.contains(listener)) {
			listeners.add(listener);
		}
	}
	public long getMillisecondsElapsed() {
		return millisecondsElapsed;
	}
	public boolean isSuspended() {
		return suspended;
	}
	private void notifyTick() {
		timeEvent.ticks++;
//		synchronized(this) {
			for (int i = 0; i < listeners.size(); i++) {
				((TimeListener) listeners.get(i)).tick(timeEvent);
			}
//		}
	}
	public synchronized void removeTimeListener(TimeListener listener) {
		if (listeners.contains(listener)) {
			listeners.remove(listener);
		}
	}
	public void run() {
		while (true) {
			try {
				Thread.sleep(delayMilliseconds);
				if (suspended) {
					synchronized(this) {
						while (suspended) {
							wait();
						}
					}
				}
			} catch (InterruptedException e) {
				// do nothing
			}
			notifyTick();
		}
	}
	public synchronized void setSuspended(boolean suspended) {
		this.suspended = suspended;
		if (suspended) {
			millisecondsElapsed = System.currentTimeMillis() - millisecondsElapsed;
		} else {
			millisecondsElapsed = System.currentTimeMillis();
			notify();
		}
	}
	public String toString() {
		return millisecondsElapsed + "ms";
	}
}
