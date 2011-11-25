package org.tiling.tournesol;

import org.tiling.gui.Canvas2D;
import org.tiling.gui.Viewer2D;

import org.tiling.tournesol.events.TimeEvent;
import org.tiling.tournesol.events.TimeListener;

/**
 * I provide a view of a growing plant.
 */
public class PlantViewer extends Viewer2D implements TimeListener {
	private PlantUI ui;
	public PlantViewer(PlantInterface plant) {
		super("Plant");
		ui = new PlantUI(plant);
		Canvas2D canvas = new Canvas2D(ui);
		setCanvas2D(canvas);
	}
	public void tick(TimeEvent event) {
		ui.tick(event);
		repaint();
	}
}
