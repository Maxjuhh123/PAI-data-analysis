/**
 * This is a macro to get the vessel diameters given a grayscale image.
 * 
 * !! FLASH WARNING !! This macro will make your screen flash.
 * It is a computationally expensive macro so strong processing power is recommended.
 */


/**
 * FUNCTION DEFINITIONS
 */


/**
 * Get binary mask of the original image.
 */
function getBinaryImage(originalId) {
	selectImage(originalId);
	
	// Preprocess
	run("Duplicate...", "duplicate");
	run("8-bit"); 
	run("Median...", "radius=1"); 

	//Binarize
	setThreshold(66, 255); 
	run("Convert to Mask"); 
	run("Analyze Particles...", "size=20-Infinity show=Nothing"); //remove small artefacts 
}

/**
 * Given coordinates (v1, v2) representing a (vessel) line, estimate the vessel diameter using the perpendicular line.
 * 
 * @param v1x - x coordinate of v1
 * @param v1y - y coordinate of v1
 * @param v2x - x coordinate of v2
 * @param v2y - y coordinate of v2
 * @param binaryMaskName - Name of the binary mask of the original image
 */
function estimateVesselDiameter(v1x, v1y, v2x, v2y, binaryMaskName) {
	// First find the perpendicular line
	midX = (v1x + v2x)/2;
	midY = (v1y + v2y)/2;
	
	// Calculate the angle of the line
   	angle = Math.atan2(v2y - v1y, v2x - v1x);
	length = 20;

    // Calculate the perpendicular line
    perpendicularAngle = angle + PI / 2;
    x1 = midX - length / 2 * Math.cos(perpendicularAngle);
    y1 = midY - length / 2 * Math.sin(perpendicularAngle);
    x2 = midX + length / 2 * Math.cos(perpendicularAngle);
    y2 = midY + length / 2 * Math.sin(perpendicularAngle);

    // Get mask of perpendicular line
    WAIT_TIME_MS = 30; // Waiting time after creating a mask, increase value if program crashes
    makeLine(x1, y1, x2, y2);
    run("Create Mask");
    wait(WAIT_TIME_MS);
    maskName = getTitle();
    
    // Find intersection of mask with original image mask
    imageCalculator("Multiply create", binaryMaskName, maskName);
    wait(WAIT_TIME_MS);
    inters = getTitle();
    
    // Find Feret's diameter of intersection
    run("Analyze Particles...", "display");
    close(maskName);
    close(inters);
}


/**
 * DIAMETER ANALYSIS STEPS
 */


ORIGINAL_ID = getImageID();
getBinaryImage(ORIGINAL_ID);

// Get vessel branch coordinates
run("Skeletonize (2D/3D)");
run("Analyze Skeleton (2D/3D)", "prune_0 show"); 
selectWindow("Branch information");
// Iterate over results and filter out bad vessels
n = 0;
l = Table.size;
v1xs = Table.getColumn("V1 x");
v1ys = Table.getColumn("V1 y");
v2xs = Table.getColumn("V2 x");
v2ys = Table.getColumn("V2 y");
eds = Table.getColumn("Euclidean distance");
for (i = 0; i < l; i++) {
	v1x = v1xs[i];
	v2x = v2xs[i];
	v1y = v1ys[i];
	v2y = v2ys[i];
	ed = eds[i];
	isGoodDistance = ed >= 10; // Filter out short vessels
	if (isGoodDistance) {
		v1xs[n] = v1x;
		v2xs[n] = v2x;
		v1ys[n] = v1y;
		v2ys[n] = v2y;
		n++;
	}
}
selectWindow("Results");

// Get diameter of each vessel
run("Clear Results");
selectImage(ORIGINAL_ID);
run("8-bit"); 
run("Geometry to Distance Map", "threshold=150");
setThreshold(1.0000, 1000000000000000000000000000000.0000);
run("Convert to Mask"); // Get binary mask of vessels (mask 1)
binaryMaskName = getTitle();

print("Starting diameter measurements for " + n + " vessels, this may take a while...");
setTool("line");
	run("Set Measurements...", "feret's redirect=None decimal=2");
for (i = 0; i < n; i++) {
	// find min x
	minX = minOf(v1xs[i], v2xs[i]); 
	// find min y
	minY = minOf(v1ys[i], v2ys[i]);
	// find max x
	maxX = maxOf(v1xs[i], v2xs[i]);
	// find max y
	maxY = maxOf(v1ys[i], v2ys[i]);
	// width and height
	width = maxX - minX + 1;
	height = maxY - minY + 1;
	
	estimateVesselDiameter(v1xs[i], v1ys[i], v2xs[i], v2ys[i], binaryMaskName);
}
print("Finished measuring diameters.");
// You should now have a table containing results (in pixels)
close("*");