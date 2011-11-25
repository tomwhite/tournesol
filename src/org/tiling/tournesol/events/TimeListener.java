package org.tiling.tournesol.events;

import java.util.EventListener;

/**
 * I am the listener interface for receiving {@link TimeEvent}s.
 */
public interface TimeListener extends EventListener {
	public void tick(TimeEvent event);
}
