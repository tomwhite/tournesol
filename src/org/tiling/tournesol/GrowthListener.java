package org.tiling.tournesol;

import java.util.EventListener;

/**
 * I am the listener interface for receiving {@link GrowthEvent}s.
 */
public interface GrowthListener extends EventListener {
	public void afterAddingElement(GrowthEvent event);
	public void beforeAddingElement(GrowthEvent event);
	public void finishedGrowing(GrowthEvent event);
}
