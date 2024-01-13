// FIJI (IMAGEJ) GUIDE FOR VASCULAR ANALYSIS 
// Ruslan Rust 
// 03/10/2019 

/* Before Starting you will need to install two packages to perform the analysis    
*  Package 1: Measure Skeleton Length:  
*  Link: dev.mri.cnrs.fr/attachments/download/1487/Measure_Skeleton_Length_Tool.ijm 
*  Save the document under ImageJ/plugins/  
*   
*  Package 2: NND: Nearest neighbor distance 
*  Link: https://icme.hpc.msstate.edu/mediawiki/images/9/9a/Nnd_.class 
*  Save the file in  ImageJ/Plugins/Analyze 
*/ 

/**
 * Analyze a folder containing images, then save results to Results table. 
 */
function processFolder(folderPath) {	
	files = getFileList(folderPath);
	
	// Count how many images
	fileCount = 0;
	for (row = 0; row < files.length; row++) {
		filePath = folderPath + "/" + files[row];
		// Only process images
		if (!endsWith(filePath, ".csv")) {
			fileCount++;
		}
	}
	
	// Define result arrays
	labels = newArray(fileCount);
	areaPercentages = newArray(fileCount);
	vasculatureLengths = newArray(fileCount);
	numBranchesList = newArray(fileCount);
	averageBranchLengths = newArray(fileCount);
	maximumBranchLengths = newArray(fileCount);
	meanVesselDistances = newArray(fileCount);
	minVesselDistances = newArray(fileCount);
	
	// Analyze each image
	for (row = 0; row < files.length; row++) {
		filePath = folderPath + "/" + files[row];
		// Only process images
		if (!endsWith(filePath, ".csv")) {
			processFile(filePath, row, labels, areaPercentages,  
				vasculatureLengths, numBranchesList, averageBranchLengths,
				maximumBranchLengths, meanVesselDistances, minVesselDistances
			);
		}
	}
	
	// Save results to table
	run("Clear Results");
	for (i = 0; i < fileCount; i++) {
		setResult("Label", i, labels[i]);	
		setResult("Area Percentage", i, areaPercentages[i]);	
		setResult("Vasculature Length", i, vasculatureLengths[i]);	
		setResult("Number of Branches", i, numBranchesList[i]);	
		setResult("Average Branch Length", i, averageBranchLengths[i]);	
		setResult("Maximum Branch Length", i, maximumBranchLengths[i]);	
		setResult("Mean Vessel Distance", i, meanVesselDistances[i]);
		setResult("Min Vessel Distance", i, minVesselDistances[i]);
	}
}

/**
 * Preprocess the image, results in binary image.
 */
function preProcessImage() {
	//PRE-PROCESSING 
	run("Duplicate...", "duplicate"); // dublicate image, to keep the raw image 
	run("8-bit");  // alternatively use 16 bit  

	// Remove noise, radius can be adjusted 
	run("Median...", "radius=1"); 

	//BINARIZED IMAGE  
	// either use AutoThreshold or adjust manually with setThredhold 
	setThreshold(66, 255); 
	run("Convert to Mask"); 
	run("Analyze Particles...", "size=20-Infinity show=Masks"); //remove small artefacts 
	// Analyze all parameters seperately, start always from binary image 
	// The parameters presented here are: Area fraction, Vascular length, Vascular branching, Nearest neighbor distance 
}

/**
 * Start with a fresh binary.
 */
function getOriginalBinaryImage(filePath) {
	close("*");
	open(filePath);
	preProcessImage();
}

/**
 * Analyze the blood vessel density (area).
 */
function analyzeArea(filePath, row, areaPercentages) {
	getOriginalBinaryImage(filePath);
	
	run("Clear Results");
	run("Set Measurements...", "area mean min centroid perimeter area_fraction redirect=None decimal=2"); 
	run("Measure"); 
	areaPercent = getResult("%Area", 0);
	
	areaPercentages[row] = areaPercent;
}

/**
 * Analyze the vessel lengths.
 */
function analyzeVesselLength(filePath, row, vasculatureLengths) {
	getOriginalBinaryImage(filePath);
	
	run("Clear Results");
	run("Set Measurements...", "area mean min centroid perimeter area_fraction redirect=None decimal=2"); 
	run("Duplicate...", " "); 
	run("Skeletonize"); 
	run("Measure Skeleton Length Tool"); // Install this pplugin!  
	vasculatureLength = getResult("length", 0); 
	
	vasculatureLengths[row] = vasculatureLength;
}

/**
 * Analyze a single branch.
 */ 
function analyzeBranch(v1x, v1y, v2x, v2y) {
	// Analyze a single branch, assuming the original binary image is open?
	// Emma do your thing here
	width = v2x - v1x + 1;
	height = v2y - v1y + 1;
	print("x: " + v1x);
	print("y: " + v1y);
	print("x2: " + v2x);
	print("y2: " + v2y);
	print("width: " + width);
	print("height: " + height);
	if (width > 0 && height > 0) {
		setTool("rectangle");
		makeRectangle(v1x - 1, v1y - 1, width, height);
		roiManager("Add");
	}
}

/**
 * Analyze vessel branches. 
 */ 
function branchAnalysis(filePath, numBranchesList, averageBranchLengths, maximumBranchLengths, row) {
	getOriginalBinaryImage(filePath);
	
	// First get general branch info
	run("Clear Results");
	run("Set Measurements...", "area_fraction area mean min centroid perimeter redirect=None decimal=2"); 
	run("Duplicate...", " "); 
	run("Skeletonize");
	run("Analyze Skeleton (2D/3D)", "prune=none show"); 
	// you get as a result many parameters including Number of junctions, branches, branch length etc. 
	// Detailed information you can find under: https://imagej.net/AnalyzeSkeleton 
	numBranches = getResult("# Branches", 0);
	averageBranchLength = getResult("Average Branch Length", 0);
	maximumBranchLength = getResult("Maximum Branch Length", 0);

	// Get branch coordinates
	getOriginalBinaryImage(filePath);
	run("Clear Results");
	run("Set Measurements...", "area_fraction area mean min centroid perimeter redirect=None decimal=2"); 
	run("Duplicate...", " "); 
	run("Analyze Skeleton (2D/3D)", "prune=none show"); 
	selectWindow("Branch information");
	v1xs = Table.getColumn("V1 x");
	v1ys = Table.getColumn("V1 y");
	v2xs = Table.getColumn("V2 x");
	v2ys = Table.getColumn("V2 y");
	selectWindow("Results");
	
	getOriginalBinaryImage(filePath);
	
	// Analyze each branch
	for (i = 0; i < v1xs.length; i++) {
		v1x = v1xs[i];
		v1y = v1ys[i];
		v2x = v2xs[i];
		v2y = v2ys[i];
		
		analyzeBranch(v1x, v1y, v2x, v2y);
	}
	
	// I have no idea how to automate the popup windows.....
	// you should save the file when prompted and click no for all the questions
	roiManager("Show All without labels");
	n = roiManager("count");
	for (i = 0; i < n; i++) {
    	roiManager("select", i);
  		run("Diameter Measurements", "distance=222 distance_0=222");
	}
	// Update result arrays
	numBranchesList[row] = numBranches;
	averageBranchLengths[row] = averageBranchLength;
	maximumBranchLengths[row] = maximumBranchLength;
}

/**
 * Analyze distances between vessels.
 */
function analyzeVesselDistances(filePath, row, meanVesselDistances, minVesselDistances) {
	getOriginalBinaryImage(filePath);
	
	run("Clear Results");
	run("Put Behind [tab]"); 
	run("Set Measurements...", "area centroid kurtosis area_fraction display redirect=None decimal=6"); 
	run("Duplicate...", " "); 
	run("Analyze Particles...", "size=20-Infinity show=Nothing display"); 
	run("Nnd "); 
	nearestNeighbourDistances = Table.getColumn("C1");
	// Get mean and standard deviation of distances between vessels
	Array.getStatistics(nearestNeighbourDistances, minVesselDistance, max, meanVesselDistance, sdVesselDistance);	
	
	meanVesselDistances[row] = meanVesselDistance;
	minVesselDistances[row] = minVesselDistance;
}

/**
 * Analyze a single image, gather various data and save it to respective arrays.
 */
function processFile(
	filePath, row, labels, areaPercentages, vasculatureLengths, 
	numBranchesList, averageBranchLengths, maximumBranchLengths,
	meanVesselDistances, minVesselDistances
) {
	print("Analyzing: " + filePath + "...");
	run("Clear Results");
	
	//1 Area fraction 
	//analyzeArea(filePath, row, areaPercentages);

	//2 Vascular length 
	//analyzeVesselLength(filePath, row, vasculatureLengths);

	//3 Vascular branches  
	branchAnalysis(filePath, numBranchesList, averageBranchLengths, maximumBranchLengths, row);

	//4 Nearest neighbor distance 
	//analyzeVesselDistances(filePath, row, meanVesselDistances, minVesselDistances);
	
	// Update result arrays
	labels[row] = filePath;
	
	close("*");
	close("Results");
	//close("Branch information");
	close("Nearest Neighbour Distances");
	print("Finished analyzing: " + filePath + ".");
}

function saveResultsToFile(folderPath) {
	outputPath = folderPath + "/output.csv";
	saveAs("Results", outputPath); 
	print("Saved results to: " + outputPath);
}

folderPath = getDirectory("Choose a Directory"); 
processFolder(folderPath); 
saveResultsToFile(folderPath);