package org.tiling.tournesol;

import java.util.EventObject;

/**
 * I am an event indicating growth has occured or is about to occur.
 */
public class GrowthEvent extends EventObject {
	private PlantInterface plant;
	public GrowthEvent(PlantInterface plant) {
		super(plant);
		this.plant = plant;
	}
	public PlantInterface getPlant() {
		return plant;
	}
}
