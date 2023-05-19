package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;
import ij.process.FloatProcessor;

/**
 * This plugin thresholds a given 8-bit grayscale image based on the gradient
 * information.
 */
public class My_GradientThresholding implements PlugInFilter {
	String title = null;

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
		// create the output image as a copy of the input one
		ImageProcessor out = ip.duplicate();

		// threshold
		int thresh = 0;

		// find a suitable threshold 'thresh' for the image 'ip' based on the gradient
		// information
		// skip pixels in which the gradient magnitude operator looks outside the image
		// domain
		// threshold the image 'ip' with the computed threshold 'thresh' (<thresh ->
		// background, >=thresh -> foreground)
		// write the thresholded image into the image 'out' (background -> 0, foreground
		// -> 255)
		// WRITE YOUR CODE HERE

		int w = ip.getWidth();
		int h = ip.getHeight();

		ImageProcessor grad = new FloatProcessor(w, h);
		float dx;
		float dy;
		float g;
		float sum = 0;

		for (int y = 1; y < h - 1; ++y) {
			for (int x = 1; x < w - 1; ++x) {

				dy = (ip.getf(x, y + 1) - ip.getf(x, y - 1)) / 2f;
				dx = (ip.getf(x + 1, y) - ip.getf(x - 1, y)) / 2f;
				g = (float) Math.sqrt(dx * dx + dy * dy);
				grad.setf(x, y, g);
				sum += g;

			}
		}
		float t = 0;
		for (int i = 0; i < grad.getPixelCount(); ++i) {
			t += ip.get(i) * grad.getf(i) / sum;
		}
		thresh = (int) t;

		for (int i = 0; i < out.getPixelCount(); ++i) {
			if (ip.get(i) < thresh) {
				out.set(i, 0);
			} else {
				out.set(i, 255);
			}
		}

		// IJ.showMessage("NOT IMPLEMENTED!");
		// NO CHANGES NEEDED AFTER THIS LINE

		// show the output image
		ImagePlus outImg = new ImagePlus(String.format("My gradient thresholding (thresh=%d) of ", thresh) + title,
				out);
		outImg.show();
	}

}
