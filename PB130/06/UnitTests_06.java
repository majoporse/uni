package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.PlugIn;
import ij.process.ImageProcessor;

/** This plugin automatically validates the plugins within Exercise 06. */
public class UnitTests_06 implements PlugIn 
{	
	int failedTests = 0;
	String plugDir = IJ.getDirectory("plugins") + "PB130/";
	String srcDir = plugDir + "images/";
	String refDir = plugDir + "refs/";	

	public void run(String arg) 
	{
		IJ.open(srcDir + "whoamI.tif");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_MedianFilter.java");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_AdvancedMedianFilter.java");
		IJ.wait(500);
		IJ.run("Close All");
		IJ.log("\\Clear");
		IJ.run("Refresh Menus");
		IJ.log("Please wait, running all pre-defined tests...");
		IJ.log("Source image directory: " + srcDir);
		IJ.log("Reference image directory: " + refDir);
		IJ.log("=============================================");
		testPlugin("My MedianFilter", "square=1", "whoamI.tif", "whoamI_med1.tif");
		testPlugin("My MedianFilter", "square=3", "whoamI.tif", "whoamI_med3.tif");
		testPlugin("My MedianFilter", "square=5", "whoamI.tif", "whoamI_med5.tif");
		testPlugin("My AdvancedMedianFilter", "square=1", "whoamI.tif", "whoamI_advmed1.tif");
		testPlugin("My AdvancedMedianFilter", "square=3", "whoamI.tif", "whoamI_advmed3.tif");
		testPlugin("My AdvancedMedianFilter", "square=5", "whoamI.tif", "whoamI_advmed5.tif");


		if (failedTests > 0)
		{
			IJ.log("Total number of tests failed: " + failedTests);
		}
		else
		{
			IJ.log("CONGRATULATIONS! ALL TESTS PASSED.");
		}		
	}

	private void testPlugin(String pluginName, String pluginParams, String srcImage, String refImage)
	{
		IJ.log("Plugin name: " + pluginName);
		IJ.log("Source image: " + srcImage);
		IJ.log("Reference image: " + refImage);
		IJ.open(srcDir + srcImage);
		ImagePlus out = IJ.getImage();
		IJ.run(pluginName, pluginParams);
		IJ.open(refDir + refImage);
		ImagePlus ref = IJ.getImage();
		
		if (compare(ref.getProcessor(), out.getProcessor()))
		{
			IJ.log("Test passed!");
			
		}
		else
		{
			IJ.log("Test failed!");
			++failedTests;
		}

		out.changes = false;
		out.close();
		ref.changes = false;
		ref.close();
		IJ.log("=============================================");
	}
	

	private boolean compare(ImageProcessor ref, ImageProcessor out)
	{	
		if (ref.getWidth() != out.getWidth() || ref.getHeight() != out.getHeight())
		{
			IJ.log("Error: Inconsistent image size between the reference and tested images!");
			return false;
		}
		
		int num = ref.getPixelCount();

		for (int i = 0; i < num; ++i)
		{
			if (ref.get(i) != out.get(i))
			{
				return false;  		
			}
		}
		
		return true;		
	}

}
