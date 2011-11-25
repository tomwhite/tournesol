package org.tiling.tournesol;

import java.util.List;

import org.tiling.tournesol.events.TimeListener;

/**
 * I am a growing plant.
 */
public interface PlantInterface extends TimeListener {
	public List getElements();
}
