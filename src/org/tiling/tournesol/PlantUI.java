package org.tiling.tournesol;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Shape;
import java.awt.RenderingHints;
import java.awt.Stroke;
import java.awt.geom.Ellipse2D;
import java.awt.geom.GeneralPath;
import java.awt.geom.Rectangle2D;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import org.tiling.UI;
import org.tiling.tournesol.events.TimeEvent;
import org.tiling.tournesol.events.TimeListener;

/**
 * I am a graphical representation of a growing plant.
 */
public class PlantUI implements UI, TimeListener {
	public static final float LINE_WIDTH = 0.1f;

	private PlantInterface plant;
	protected Color backgroundColor = Color.black;
	protected List elements = new ArrayList();

	private GeneralPath origin;

	protected Rectangle2D bounds;

	protected RenderingHints qualityHints;
	protected Stroke stroke;
	public PlantUI(PlantInterface plant) {
		this.plant = plant;
		initialiseGraphics();
		initialiseShapes();
	}
	public Object clone() {
		try {
			PlantUI ui = (PlantUI) super.clone();
			return ui;
		} catch (CloneNotSupportedException e) {
			// this shouldn't happen, since we are Cloneable
			throw new InternalError();
		}		
	}
	private synchronized void createShapes() {
		bounds = new Rectangle2D.Double();
		elements.clear();
		for (Iterator i = plant.getElements().iterator(); i.hasNext(); ){
			ElementInterface element = (ElementInterface) i.next();
			double radius = element.getRadius();
			double diameter = 2 * radius;
			Ellipse2D ellipse = new Ellipse2D.Double(element.getX() - radius, element.getY() - radius, diameter, diameter);
			elements.add(ellipse);
			bounds.add(ellipse.getBounds2D());
		}

	}
	public Color getBackground() {
		return backgroundColor;
	}
	public Rectangle2D getBounds2D() {
		return bounds;
	}
	protected void initialiseGraphics() {
		qualityHints = new RenderingHints(RenderingHints.KEY_ANTIALIASING,
											RenderingHints.VALUE_ANTIALIAS_ON);
		qualityHints.put(RenderingHints.KEY_RENDERING, RenderingHints.VALUE_RENDER_QUALITY);
		stroke = new BasicStroke(LINE_WIDTH);
	}
	private void initialiseShapes() {
		origin = new GeneralPath();
		origin.moveTo(1, 0);
		origin.lineTo(-1, 0);
		origin.moveTo(0, 1);
		origin.lineTo(0, -1);
	}
	public synchronized void paint(java.awt.Graphics2D g2) {
	    g2.setRenderingHints(qualityHints);
	    g2.setStroke(stroke);

	    int alpha = 200 - elements.size();
	    if (alpha < 0) {
			alpha = 0;
	    }
	    for (Iterator i = elements.iterator(); i.hasNext(); ) {
		    g2.setColor(new Color(255, 255, 0, alpha));
	        if (alpha < 255) {
				alpha++;
	        }

		    g2.fill((Shape) i.next());
	    }
	    g2.setColor(Color.white);
	    g2.draw(origin);
	    
	}
	public void setBackground(Color c) {
		backgroundColor = c;
	}
	public void tick(TimeEvent event) {
		plant.tick(event);
		createShapes();
	}
}
