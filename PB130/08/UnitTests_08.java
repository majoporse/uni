package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.PlugIn;
import ij.process.ImageProcessor;

/** This plugin automatically validates the plugins within Exercise 08. */
public class UnitTests_08 implements PlugIn 
{	
	int failedTests = 0;
	String plugDir = IJ.getDirectory("plugins") + "PB130/";
	String srcDir = plugDir + "images/";
	String refDir = plugDir + "refs/";	

	public void run(String arg) 
	{
		IJ.open(srcDir + "rectangle.tif");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_BinaryMorphology.java");
		IJ.wait(500);
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_BinaryHoleFilling.java");
		IJ.wait(500);
		IJ.run("Close All");
		IJ.log("\\Clear");
		IJ.run("Refresh Menus");
		IJ.log("Please wait, running all pre-defined tests...");
		IJ.log("Source image directory: " + srcDir);
		IJ.log("Reference image directory: " + refDir);
		IJ.log("=============================================");
		testPlugin("My BinaryMorphology", "operator=Erosion radius=1", "black_point.tif", "black_point_e1.tif");
		testPlugin("My BinaryMorphology", "operator=Erosion radius=53", "black_point.tif", "black_point_e53.tif");
		testPlugin("My BinaryMorphology", "operator=Dilation radius=2", "white_point.tif", "white_point_d2.tif");
		testPlugin("My BinaryMorphology", "operator=Dilation radius=25", "white_point.tif", "white_point_d25.tif");
		testPlugin("My BinaryMorphology", "operator=Opening radius=12", "rectangle.tif", "rectangle_o12.tif");
		testPlugin("My BinaryMorphology", "operator=Closing radius=8", "rectangle.tif", "rectangle_c8.tif");
		testPlugin("My BinaryHoleFilling", "", "black_point.tif", "black_point_filled.tif");
		testPlugin("My BinaryHoleFilling", "", "nuts_bolts.tif", "nuts_bolts_filled.tif");
		testPlugin("My BinaryHoleFilling", "", "rectangle.tif", "rectangle_filled.tif");
				
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