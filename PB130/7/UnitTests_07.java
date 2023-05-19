package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.PlugIn;
import ij.process.ImageProcessor;

/** This plugin automatically validates the plugins within Exercise 07. */
public class UnitTests_07 implements PlugIn 
{	
	int failedTests = 0;
	String plugDir = IJ.getDirectory("plugins") + "PB130/";
	String srcDir = plugDir + "images/";
	String refDir = plugDir + "refs/";	

	public void run(String arg) 
	{
		IJ.open(srcDir + "point.tif");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_ChessboardDistanceTransform.java");
		IJ.wait(500);
		IJ.selectWindow("point.tif");
		IJ.wait(500);
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_RegionLabeling.java");
		IJ.wait(500);
		IJ.run("Close All");
		IJ.log("\\Clear");
		IJ.run("Refresh Menus");
		IJ.log("Please wait, running all pre-defined tests...");
		IJ.log("Source image directory: " + srcDir);
		IJ.log("Reference image directory: " + refDir);
		IJ.log("=============================================");
		testPlugin("My ChessboardDistanceTransform", "image=Foreground", "point.tif", "point_dt_fg.tif");
		testPlugin("My ChessboardDistanceTransform", "image=Background", "point.tif", "point_dt_bg.tif");
		testPlugin("My ChessboardDistanceTransform", "image=Foreground", "wheel.tif", "wheel_dt_fg.tif");
		testPlugin("My ChessboardDistanceTransform", "image=Background", "wheel.tif", "wheel_dt_bg.tif");
		testPlugin("My ChessboardDistanceTransform", "image=Foreground", "flat.tif", "flat_dt_fg.tif");
		testPlugin("My ChessboardDistanceTransform", "image=Background", "flat.tif", "flat_dt_bg.tif");
		testPlugin("My RegionLabeling", "", "nuts_bolts.tif", "nuts_bolts_lab.tif");
		testPlugin("My RegionLabeling", "", "point.tif", "point_lab.tif");
		testPlugin("My RegionLabeling", "", "salt.tif", "salt_lab.tif");

		if (failedTests > 0)
		{
			IJ.log("Total number of tests failed: " + failedTests);
		}
		else
		{
			IJ.log("CONGRATULATIONS! ALL TESTS PASSED.");
		}

		IJ.run("Close All");		
	}

	private void testPlugin(String pluginName, String pluginParams, String srcImage, String refImage)
	{
		IJ.log("Plugin name: " + pluginName);
		IJ.log("Source image: " + srcImage);
		IJ.log("Reference image: " + refImage);
		IJ.open(srcDir + srcImage);
		ImagePlus src = IJ.getImage();
		IJ.run(pluginName, pluginParams);
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

		src.changes = false;
		src.close();
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
