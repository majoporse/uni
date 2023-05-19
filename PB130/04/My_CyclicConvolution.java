package PB130;

import ij.IJ;
import ij.plugin.PlugIn;
import java.util.Arrays;

/** A two-dimensional periodic matrix representation with the interface similar to the "ij.process.ImageProcessor" class. */
class MyPeriodicMatrix
{
	/** A two-dimensional array storing the matrix values. */	
	int[][] m_array;

	/** Constructor. */		
	public MyPeriodicMatrix(int[][] array)
	{
		m_array = array;
	}	

	/** Constructor. The matrix is initialized with zeros. */
	public MyPeriodicMatrix(int width, int height)
	{
		m_array = new int[height][width];
	}	

	/** Get the width of the matrix. */
	public int getWidth()
	{
		return m_array[0].length;
	}	

	/** Get the height of the matrix. */
	public int getHeight()
	{
		return m_array.length;
	}

	/** Get the value at the x-th column and y-th row. If the given position is outside the matrix domain, 
	    return the value based on periodic boundary conditions. Note that modular arithmetics can substitute for nested conditional statements. */
	public int getElement(int x, int y)
	{
		// WRITE YOUR CODE HERE
		return m_array[y][x];
	}

	/** Set the value at the x-th column and y-th row to the given value. If the given position is outside the matrix domain, do nothing. */
	public void setElement(int x, int y, int value)
	{
		// check whether the given position is outside the matrix domain or not
		if (x >= 0 && x < getWidth() && y >= 0 && y < getHeight())
		{
			m_array[y][x] = value;
		}
	}

	/** Check the content equality to a given two-dimensional array that stores the matrix values. */
	public boolean equalContent(int[][] array)
	{
		return Arrays.deepEquals(m_array, array);
	}

	/** Convert the matrix content to a string representation. */
	public String print()
	{
		String str = "";
		int w = getWidth();
		int h = getHeight();

		for (int y = 0; y < h; ++y)
		{
			str += "\n";

			for (int x = 0; x < w; ++x)
			{
				str += String.format("%5d ", m_array[y][x]);
			}
		}

		return str;
	}
}

/** This plugin convolves two integer matrices with periodic boundary conditions. */
public class My_CyclicConvolution implements PlugIn
{	
	public void run(String arg) 
	{	
		// input matrix
		int[][] matArray = { {-2, 0, 1}, {0, 4, 3}, {2, 1, -1} }; 
		MyPeriodicMatrix matrix = new MyPeriodicMatrix(matArray);

		// convolution kernel
		int[][] kerArray = { {-1, 0, 1}, {0, 3, 2} };
		MyPeriodicMatrix kernel = new MyPeriodicMatrix(kerArray);

		// convolve the input matrix with the convolution kernel
		MyPeriodicMatrix result = doConvolution(matrix, kernel);
		
		// the reference output matrix to compare with
		int[][] refArray = { {1, 5, 4, 1, 5}, {7, -5, -7, 7, -5}, {16, 4, 15, 16, 4}, {1, 5, 4, 1, 5} };
		
		// display the result and check its equality to the reference output matrix
		IJ.showMessage("Correct result: " + result.equalContent(refArray),
			       "Matrix:" + matrix.print() +  "\n \nKernel:" + kernel.print() + "\n \nResult:" + result.print());
	}

	private MyPeriodicMatrix doConvolution(MyPeriodicMatrix matrix, MyPeriodicMatrix kernel)
	{
		// size of the input matrix
		int matW = matrix.getWidth();
		int matH = matrix.getHeight();

		// size of the convolution kernel
		int kerW = kernel.getWidth();
		int kerH = kernel.getHeight();

		// size of the result
		int resW = matW + kerW - 1;
		int resH = matH + kerH - 1;

		// create the output matrix filled with zeros by default
		MyPeriodicMatrix result = new MyPeriodicMatrix(resW, resH);
				
		// convolve the input matrix with the convolution kernel
		// to obtain a value from or modify a value in a matrix 'm', call m.getElement(x, y) or m.setElement(x, y, value), respectively
		// WRITE YOUR CODE HERE
		

		for(int my = 0; my < resH; ++my){
			for (int mx = 0; mx < resW; ++mx){

				int sum = 0;

				for (int ky = 0; ky < kerH; ++ky){
					for (int kx = 0; kx < kerW; ++kx){

						int ker = kernel.getElement(kx, ky);
						int mat = matrix.getElement(Math.floorMod(mx - kx, matW), 
										    Math.floorMod(my - ky, matH));
						sum += mat * ker;
						
					}
				}

				result.setElement(mx, my, sum);

			}
			
		}
		
		
		return result;
	}
	
}
