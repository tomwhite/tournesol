package org.tiling.tournesol.events;

import java.util.EventObject;

/**
 * I am an event indicating a "tick".
 */
public class TimeEvent extends EventObject {
	protected long ticks = 0;
	protected TimeEvent(Object source) {
		super(source);
	}
	public long getTicks() {
		return ticks;
	}
}
