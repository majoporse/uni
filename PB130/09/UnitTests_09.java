package PB130;

import ij.IJ;
import ij.ImagePlus;
import ij.plugin.PlugIn;
import ij.process.ImageProcessor;

/** This plugin automatically validates the plugins within Exercise 09. */
public class UnitTests_09 implements PlugIn 
{	
	int failedTests = 0;
	String plugDir = IJ.getDirectory("plugins") + "PB130/";
	String srcDir = plugDir + "images/";
	String refDir = plugDir + "refs/";
	
	public void run(String arg) 
	{
		IJ.open(srcDir + "cermet.tif");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_GradientThresholding.java");
		IJ.wait(500);
		IJ.selectWindow("cermet.tif");
		IJ.run("Compile and Run...", "compile=" + plugDir + "My_UnimodalThresholding.java");
		IJ.wait(500);
		IJ.run("Close All");
		IJ.log("\\Clear");
		IJ.run("Refresh Menus");
		IJ.log("Please wait, running all pre-defined tests...");
		IJ.log("Source image directory: " + srcDir);
		IJ.log("Reference image directory: " + refDir);
		IJ.log("=============================================");
		testPlugin("My GradientThresholding", "cermet.tif", "cermet_gradient.tif", 139);
		testPlugin("My GradientThresholding", "nuts_bolts.tif", "nuts_bolts_gradient.tif", 140);
		testPlugin("My GradientThresholding", "pisa.tif", "pisa_gradient.tif", 125);
		testPlugin("My GradientThresholding", "rice.tif", "rice_gradient.tif", 128);
		testPlugin("My GradientThresholding", "shapes.tif", "shapes_gradient.tif", 104);
		testPlugin("My UnimodalThresholding", "cermet.tif", "cermet_triangle.tif", 207);
		testPlugin("My UnimodalThresholding", "nuts_bolts.tif", "nuts_bolts_triangle.tif", 243);
		testPlugin("My UnimodalThresholding", "pisa.tif", "pisa_triangle.tif", 216);
		testPlugin("My UnimodalThresholding", "rice.tif", "rice_triangle.tif", 102);
		testPlugin("My UnimodalThresholding", "shapes.tif", "shapes_triangle.tif", 94);

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

	private void testPlugin(String pluginName, String srcImage, String refImage, int threshold)
	{
		IJ.log("Plugin name: " + pluginName);
		IJ.log("Source image: " + srcImage);
		IJ.log("Reference image: " + refImage);
		IJ.log("Reference threshold: " + threshold);
		IJ.open(srcDir + srcImage);
		ImagePlus src = IJ.getImage();
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
