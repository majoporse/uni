package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.filter.PlugInFilter;
import ij.process.ImageProcessor;
import ij.process.FloatProcessor;


/** This plugin suppresses all non-maxima in the gradient magnitude of a given 8-bit grayscale image approximated using central differences. */
public class My_NonMaximaSuppression implements PlugInFilter 
{
	String title = null;

	public int setup(String arg, ImagePlus im) 
	{
		if (im != null)
		{
			// store the short image title for future use
			title = im.getShortTitle();
			
			// this plugin accepts 8-bit grayscale images
			return DOES_8G + NO_CHANGES; 
		}
		else
		{
			// no image is open
			IJ.noImage();
			return DONE;
		}
	}

	public void run(ImageProcessor ip) 
	{	
		// size of the input image
		int w = ip.getWidth();
		int h = ip.getHeight();

		// allocate the output image
		FloatProcessor out = new FloatProcessor(w, h);

		// suppress all non-maxima in the gradient magnitude of 'ip' approximated using central differences
		// store the result in the output image 'out'
		// WRITE YOUR CODE HERE
		FloatProcessor magnitude = new FloatProcessor(w, h);
		FloatProcessor orientation = new FloatProcessor(w, h);

		for(int y = 1; y < h-1; ++y){
			for (int x = 1; x < w - 1; ++x){
				float dy = (ip.getf(x, y + 1) - ip.getf(x, y - 1)) / 2f;
				float dx = (ip.getf(x + 1, y) - ip.getf(x - 1, y)) / 2f;
				magnitude.setf(x, y, (float) Math.sqrt(dx * dx + dy * dy));
				orientation.setf(x, y, (float) Math.toDegrees(Math.atan2(dy, dx)));
			}	
		}
		FloatProcessor magnitude = new FloatProcessor(w, h);
		FloatProcessor orientation = new FloatProcessor(w, h);

		for(int y = 1; y < h-1; ++y){
			for (int x = 1; x < w - 1; ++x){
				float dy = (ip.getf(x, y + 1) - ip.getf(x, y - 1)) / 2f;
				float dx = (ip.getf(x + 1, y) - ip.getf(x - 1, y)) / 2f;
				magnitude.setf(x, y, (float) Math.sqrt(dx * dx + dy * dy));
				orientation.setf(x, y, (float) Math.atan2(dy, dx));
			}
			
		}
		for(int y = 0; y < h; ++y){
			for (int x = 0; x < w; ++x){

				if (x == 0 || x == w-1 || y == 0 || y == h-1){
					out.setf(x, y, 0);
					continue;
				}

				float degree = (float) - Math.tan(orientation.getf(x, y));
				int[] min = new int[2];
				double minval = 360f;

				for (int i = -1; i <=1; ++i){
					for (int j = -1; j <= 1; ++j){
						if (i == 0 && j == 0){
							continue;
						}

						if (Math.abs(j*degree - i) / Math.sqrt(degree * degree + 1) < minval){
							minval = Math.abs(j*degree - i) / Math.sqrt(degree * degree + 1);
							min[0] = j;
							min[1] = i;
						}

						if (Math.abs(j*degree - i) / Math.sqrt(degree * degree + 1) == minval){
							if (Math.abs(j) < Math.abs(min[0])){
								min[0] = j;
								min[1] = i;
							}
						}
					}
				}

				float x1y1 = magnitude.getf(x-min[0], y-min[1]);
				float uv = magnitude.getf(x, y);
				float xy = magnitude.getf(x+min[0], y+min[1]);

				if (uv > x1y1 && uv > xy) {

					out.setf(x, y, magnitude.getf(x, y));

				} else {

					out.setf(x, y, 0);
				}
			
		}
		
		// NO CHANGES NEEDED AFTER THIS LINE

		// show the output image
		ImagePlus outImg = new ImagePlus("My non-maxima suppression of " + title, out);
		outImg.show();
	}

}
