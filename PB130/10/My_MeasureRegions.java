package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.measure.ResultsTable;
import ij.plugin.filter.Analyzer;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;
import ij.process.ShortProcessor;
import java.util.Queue;
import java.util.ArrayDeque;
import java.util.ArrayList;

/** This class encapsulates the coordinates of a single pixel. */
class Pixel {
	/** Pixel coordinates. */
	int x, y;

	/** Constructor. */
	Pixel(int x, int y) {
		this.x = x;
		this.y = y;
	}
}

/** This class encapsulates the parameters of a bounding box. */
class BoundingBox {
	/** The coordinates of the bounding box origin (i.e., its top-left corner). */
	Pixel origin;
	/** The width of the bounding box. */
	int width;
	/** The height of the bounding box. */
	int height;

	/** Constructor. */
	BoundingBox(Pixel origin) {
		this.origin = origin;
		width = 1;
		height = 1;
	}

	/**
	 * Update the bounding box parameters based on the coordinates of a newly added
	 * pixel.
	 */
	void update(Pixel pixel) {
		if (pixel.x < origin.x) {
			width += origin.x - pixel.x;
			origin.x = pixel.x;
		} else {
			width = Math.max(width, pixel.x - origin.x + 1);
		}

		if (pixel.y < origin.y) {
			height += origin.x - pixel.x;
			origin.y = pixel.y;
		} else {
			height = Math.max(height, pixel.y - origin.y + 1);
		}
	}
}

/** This class encapsulates the basic properties of a single region. */
class Region {
	/** The bounding box of the region. */
	BoundingBox bbox;
	/** The region label. */
	int label;
	/** The region size. */
	int size;
	/** The average grayscale intensity within the region. */
	double avgI;
	/** X-coordinate of the region centroid. */
	double cX;
	/** Y-coordinate of the region centroid. */
	double cY;
	/** The region eccentricity. */
	double ecc;
	/** The region orientation. */
	double orient;

	/** Constructor. */
	Region(Pixel origin, int label) {
		this.bbox = new BoundingBox(origin);
		this.label = label;
		this.size = 0;
		this.avgI = 0.0;
		this.cX = 0.0;
		this.cY = 0.0;
		this.ecc = -1.0;
		this.orient = 0.0;
	}
}

/**
 * This plugin measures several basic properties of 4-connected foreground
 * regions obtained using thresholding of a given 8-bit grayscale image.
 */
public class My_MeasureRegions implements PlugInFilter {
	String title = null;
	final static int UNLABELED = 65535;

	public int setup(String arg, ImagePlus im) {
		if (im != null) {
			// store the short image title for future use
			title = im.getShortTitle();

			// this plugin accepts 8-bit grayscale images only
			return DOES_8G + NO_CHANGES;
		} else {
			// no image is open
			IJ.noImage();
			return DONE;
		}
	}

	public void run(ImageProcessor ip) {
		// size of the input image
		int w = ip.getWidth();
		int h = ip.getHeight();

		// threshold the input image
		ImageProcessor tip = ip.duplicate();
		tip.threshold(50);

		// show the thresholded image
		ImagePlus tImg = new ImagePlus("My thresholding of " + title, tip);
		tImg.show();

		// create a labeled image initialized with zeros
		ImageProcessor lip = new ShortProcessor(w, h);

		// mark all foreground pixels as UNLABELED
		int num = w * h;
		for (int i = 0; i < num; ++i) {
			if (tip.get(i) == 255) {
				lip.set(i, UNLABELED);
			}
		}

		// a list used for storing regions
		ArrayList<Region> rList = new ArrayList<Region>();

		// region label
		int label = 1;

		// go through the labeled image 'lip' and label individual 4-connected
		// foreground regions using a breadth-first flood filling routine
		for (int y = 0; y < h; ++y) {
			for (int x = 0; x < w; ++x) {
				// check if the current pixel is UNLABELED
				if (lip.get(x, y) == UNLABELED) {
					rList.add(floodFill(lip, x, y, label));
					++label;
				}
			}
		}

		// show the labeled image
		ImagePlus lImg = new ImagePlus(String.format("My labeling (Num=%d) of ", label - 1) + title, lip);
		lImg.show();

		// apply a color look-up table
		IJ.run("3-3-2 RGB");

		// measure the basic properties of the detected regions
		measure(ip, lip, rList);

		// show the computed measurements in a table
		ResultsTable table = Analyzer.getResultsTable();
		table.showRowNumbers(false);

		for (int i = 0; i < rList.size(); ++i) {
			Region reg = rList.get(i);
			table.incrementCounter();
			table.addValue("ID", reg.label);
			table.addValue("BBox Origin X", reg.bbox.origin.x);
			table.addValue("BBox Origin Y", reg.bbox.origin.y);
			table.addValue("BBox Width", reg.bbox.width);
			table.addValue("BBox Height", reg.bbox.height);
			table.addValue("Size", reg.size);
			table.addValue("Average Intensity", reg.avgI);
			table.addValue("Centroid X", reg.cX);
			table.addValue("Centroid Y", reg.cY);
			table.addValue("Eccentricity", reg.ecc);
			table.addValue("Orientation", reg.orient);
			table.addResults();
		}

		table.updateResults();
		IJ.renameResults("My measurements of " + title);

		ImageProcessor cip = lip.duplicate();
		classifyEcc(cip, rList);

		// show the labeled image with classified objects
		ImagePlus cImg = new ImagePlus("My classification of " + title, cip);
		cImg.show();

		// apply a color look-up table
		IJ.run("3-3-2 RGB");

	}

	/**
	 * Perform breadth-first flood filling using a given label from a seed with
	 * coordinates 'x' and 'y'.
	 */
	private Region floodFill(ImageProcessor lip, int x, int y, int label) {
		// the region for the given seed and label
		Region reg = new Region(new Pixel(x, y), label);

		// size of the input image
		int w = lip.getWidth();
		int h = lip.getHeight();

		// create an empty queue
		Queue<Pixel> q = new ArrayDeque<Pixel>();

		// add the seed pixel to the tail of the queue
		q.add(new Pixel(x, y));

		while (!q.isEmpty()) {
			// remove a pixel from the head of the queue
			Pixel n = q.remove();

			// check if the pixel 'n' is within the image domain and is UNLABELED
			if (n.x >= 0 && n.x < w && n.y >= 0 && n.y < h && lip.get(n.x, n.y) == UNLABELED) {
				reg.bbox.update(n);
				lip.set(n.x, n.y, label);
				q.add(new Pixel(n.x - 1, n.y));
				q.add(new Pixel(n.x + 1, n.y));
				q.add(new Pixel(n.x, n.y - 1));
				q.add(new Pixel(n.x, n.y + 1));
			}
		}

		return reg;
	}

	/**
	 * Measure the basic properties of individual regions in the given list of
	 * regions 'rList'.
	 */
	private void measure(ImageProcessor ip, ImageProcessor lip, ArrayList<Region> rList) {
		// measure the size, centroid, average intensity in the original image 'ip',
		// eccentricity, and orientation of individual regions in 'rList'
		// store the region size to the 'size' attribute of the 'Region' class
		// store the region centroid to the 'cX' and 'cY' attributes of the 'Region'
		// class
		// store the region average intensity to the 'avgI' attribute of the 'Region'
		// class
		// store the region eccentricity to the 'ecc' attribute of the 'Region' class
		// store the region orientation in degrees to the 'orient' attribute of the
		// 'Region' class
		// for measuring the region eccentricity and orientation, you may find useful
		// the method 'centralMoment()' after its completion
		//
		// to increment the size attribute of the region with label 'label' in the
		// region list 'rList', you may find useful the following code:
		//
		// Region reg = rList.get(label - 1);
		// ++reg.size;
		//
		// note that 'reg' is just a reference to the particular object in the region
		// list 'rList'
		// therefore, any change to 'reg' propagates directly to the particular object
		// in 'rList'
		//
		// WRITE YOUR CODE HERE

		int h = lip.getHeight();
		int w = lip.getWidth();

		for (int y = 0; y < h; ++y) {
			for (int x = 0; x < w; ++x) {
				if (lip.get(x, y) == 0) {
					continue;
				}

				Region reg = rList.get(lip.get(x, y) - 1);
				++reg.size;
				reg.cX += x;
				reg.cY += y;
				reg.avgI += ip.get(x, y);
			}
		}

		for (Region region : rList) {
			region.cX /= region.size;
			region.cY /= region.size;
			region.avgI /= region.size;
			double u11 = centralMoment(lip, region, 1, 1);
			double u20 = centralMoment(lip, region, 2, 0);
			double u02 = centralMoment(lip, region, 0, 2);
			region.orient = Math.toDegrees(Math.atan2(2 * u11, u20 - u02) / 2);
			region.ecc = (u20 + u02 + Math.sqrt((u20 - u02) * (u20 - u02) + 4 * u11 * u11)) /
					(u20 + u02 - Math.sqrt((u20 - u02) * (u20 - u02) + 4 * u11 * u11));
		}
		// classifyEcc(lip, rList);
	}

	/**
	 * Compute the central moment of order 'p' and 'q' for the given binary region
	 * 'reg' in the image 'lip'.
	 */
	private double centralMoment(ImageProcessor lip, Region reg, int p, int q) {
		// go through the bounding box of the given region only, being specified by its
		// origin ['reg.bbox.origin.x', 'reg.bbox.origin.y'], width 'reg.bbox.width',
		// and height 'reg.bbox.height'
		// WRITE YOUR CODE HERE AND RETURN CORRECT VALUE

		int a = reg.bbox.origin.x;
		int b = reg.bbox.origin.y;

		int h = b + reg.bbox.height;
		int w = a + reg.bbox.width;

		double cm = 0;
		int size = 0;

		for (int y = b; y < h; ++y) {
			for (int x = a; x < w; ++x) {

				if (lip.get(x, y) != reg.label) {
					continue;
				}

				cm += Math.pow((x - reg.cX), p) * Math.pow((y - reg.cY), q);
			}
		}
		return cm;
	}

	/**
	 * Classify regions in the given list of regions 'rList' into three categories
	 * (bolt - label 2, nut without any hole - label 4,
	 * nut with a hole - label 10) depending on their eccentricity. Write the
	 * classification labels directly to the image 'cip'.
	 */
	private void classifyEcc(ImageProcessor cip, ArrayList<Region> rList) {
		// WRITE YOUR CODE HERE
		for (Region region : rList) {

			if (region.ecc > 7) {
				regionFill(cip, region, 2);
			} else if (region.ecc > 2) {
				regionFill(cip, region, 4);
			} else {
				regionFill(cip, region, 10);
			}
		}
	}

	private void regionFill(ImageProcessor cip, Region region, int label) {
		int x = region.bbox.origin.x;
		int y = region.bbox.origin.y;
		while (cip.get(x, y) != region.label) {
			++x;
		}
		regionFloodFill(cip, region, x, y, label);
	}

	private void regionFloodFill(ImageProcessor cip, Region region, int x, int y, int label) {

		int w = cip.getWidth();
		int h = cip.getHeight();

		Queue<Pixel> q = new ArrayDeque<Pixel>();

		q.add(new Pixel(x, y));

		while (!q.isEmpty()) {
			Pixel n = q.remove();

			if (region.label != label && n.x >= 0 && n.x < w && n.y >= 0 && n.y < h
					&& cip.get(n.x, n.y) == region.label) {
				cip.set(n.x, n.y, label);
				q.add(new Pixel(n.x - 1, n.y));
				q.add(new Pixel(n.x + 1, n.y));
				q.add(new Pixel(n.x, n.y - 1));
				q.add(new Pixel(n.x, n.y + 1));
			}
		}
	}
}
