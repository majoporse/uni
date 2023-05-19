package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;

/**
 * This plugin thresholds a given 8-bit grayscale image using the triangle
 * method.
 */
public class My_UnimodalThresholding implements PlugInFilter {
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

		// the number of pixels in the image 'ip'
		int num = ip.getPixelCount();

		// threshold
		int thresh = 0;

		// compute the intensity histogram and find the minimum and maximum intensities
		int min = ip.get(0);
		int max = ip.get(0);
		int[] hist = new int[256];
		int value = 0;

		for (int i = 0; i < num; ++i) {
			value = ip.get(i);
			++hist[value];

			if (value < min) {
				min = value;
			} else if (value > max) {
				max = value;
			}
		}

		// find a suitable threshold 'thresh' for the image 'ip' using the triangle
		// method
		// the distance between a point [sx, sy] and a line a * x + b * y + c = 0 is
		// given as |a * sx + b * sy + c| / sqrt(a * a + b * b)
		// threshold the image 'ip' with the computed threshold 'thresh' (<thresh ->
		// background, >=thresh -> foreground)
		// write the thresholded image into the image 'out' (background -> 0, foreground
		// -> 255)
		// WRITE YOUR CODE HERE
		// IJ.showMessage("NOT IMPLEMENTED!");

		max = 0;
		for (int i = 0; i < hist.length; ++i) {
			if (hist[i] > hist[max]) {
				max = i;
			}
		}
		min = max;
		for (int i = 0; i < hist.length; ++i) {
			if (hist[i] == 0) {
				continue;
			}
			if (Math.abs(max - i) > Math.abs(max - min)) {
				min = i;
			}
		}
		float x1 = min;
		float y1 = hist[min];
		float x2 = max;
		float y2 = hist[max];

		int res = min;
		double len = 0;
		double curLen;

		double k = (y2 - y1) / (x2 - x1);
		double c = hist[max] - k * max;

		int mi = (min < max) ? (min) : (max);
		int ma = (min > max) ? (min) : (max);

		for (int i = 0; i < hist.length; ++i) {

			curLen = Math.abs(k * i - hist[i] + c) / Math.sqrt(k * k + 1);

			if (len < curLen && i > mi && i < ma) {
				len = curLen;
				res = i;
			}
		}

		for (int i = 0; i < out.getPixelCount(); ++i) {
			if (ip.get(i) < res) {
				out.set(i, 0);
			} else {
				out.set(i, 255);
			}
		}

		// NO CHANGES NEEDED AFTER THIS LINE

		// show the output image
		ImagePlus outImg = new ImagePlus(String.format("My unimodal thresholding (thresh=%d) of ", thresh) + title,
				out);
		outImg.show();
	}

}
