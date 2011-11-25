package org.tiling.tournesol;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

/**
 * I provide safe (synchronized) support for managing {@link GrowthListener}s
 * for a {@link PlantInterface Plant}.
 */
public abstract class PlantSupport implements PlantInterface {
	private ArrayList listeners = new ArrayList();
	public PlantSupport() {
	}
	public synchronized void addGrowthListener(GrowthListener listener) {
		if (!listeners.contains(listener)) {
			listeners.add(listener);
		}
	}
	protected void notifyAfterAddingElement(GrowthEvent event) {
		synchronized(this) {
			for (int i = 0; i < listeners.size(); i++) {
				((GrowthListener) listeners.get(i)).afterAddingElement(event);
			}
		}
	}
	protected void notifyBeforeAddingElement(GrowthEvent event) {
		synchronized(this) {
			for (int i = 0; i < listeners.size(); i++) {
				((GrowthListener) listeners.get(i)).beforeAddingElement(event);
			}
		}
	}
	protected void notifyFinishedGrowing(GrowthEvent event) {
		synchronized(this) {
			for (int i = 0; i < listeners.size(); i++) {
				((GrowthListener) listeners.get(i)).finishedGrowing(event);
			}
		}
	}
	public synchronized void removeGrowthListener(GrowthListener listener) {
		if (listeners.contains(listener)) {
			listeners.remove(listener);
		}
	}
}
