package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.measure.ResultsTable;
import ij.plugin.PlugIn;
import ij.process.ImageProcessor;

/** This plugin automatically validates the plugins within Exercise 10. */
public class UnitTests_10 implements PlugIn 
{	
	int failedTests = 0;
	String plugDir = IJ.getDirectory("plugins") + "PB130/";
	String srcDir = plugDir + "images/";
	String refDir = plugDir + "refs/";
	
	public void run(String arg) 
	{
		IJ.open(srcDir + "nuts_bolts.tif");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_MeasureRegions.java");
		IJ.wait(500);
		IJ.run("Close All");
		IJ.log("\\Clear");
		IJ.run("Refresh Menus");
		IJ.log("Please wait, running all pre-defined tests...");
		IJ.log("Source image directory: " + srcDir);
		IJ.log("Reference image directory: " + refDir);
		IJ.log("=============================================");
		testPlugin("My MeasureRegions", "nuts_bolts.tif", "nuts_bolts_classification.tif");

		if (failedTests > 0)
		{
			IJ.log("Total number of tests failed: " + failedTests);
		}
		else
		{
			IJ.log("CONGRATULATIONS! ALL TESTS PASSED.");
		}

		
	}

	private void testPlugin(String pluginName, String srcImage, String refImage)
	{
		IJ.log("Plugin name: " + pluginName);
		IJ.log("Source image: " + srcImage);
		IJ.log("Reference image: " + refImage);
		IJ.open(srcDir + srcImage);
		IJ.run(pluginName);
		ImagePlus out = IJ.getImage();
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

		IJ.run("Close All");
		IJ.wait(500);
		IJ.run("Close");		
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
