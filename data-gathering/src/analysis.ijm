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

// Let user input folder path
folderPath = getDirectory("Choose a Directory"); 
files = getFileList(folderPath);

// Define result arrays
var labels = newArray;
var areaPercentages = newArray;
var areas = newArray;
var means = newArray;
var mins = newArray;
var maxes = newArray;
var xs = newArray;
var ys = newArray;
var perims = newArray;
var vasculatureLengths = newArray;
var numBranchesList = newArray;
var numJunctionsList = newArray;
var numEndpointVoxelsList = newArray;
var numJunctionVoxelsList = newArray;
var numSlabVoxelsList = newArray;
var averageBranchLengths = newArray;
var numTriplePointsList = newArray;
var numQuadruplePointsList = newArray;
var maximumBranchLengths = newArray;
var maxVesselDistances = newArray;
var meanVesselDistances = newArray;
var minVesselDistances = newArray;
var sdVesselDistances = newArray;

// Analyze each image
imgCount = 0;
for (row = 0; row < files.length; row++) {
	filePath = folderPath + "/" + files[row];
	// Only process images
	if (endsWith(filePath, ".png") || endsWith(filePath, ".jpeg") || endsWith(filePath, ".jpg")) {
		processFile(filePath, imgCount);
		imgCount++;
	}
}
	
// Save results to table
run("Clear Results");
for (i = 0; i < imgCount; i++) {
	setResult("Label", i, labels[i]);	
	setResult("Area Percentage", i, areaPercentages[i]);	
	setResult("Area", i, areas[i]);
	setResult("Mean Intensity", i, means[i]);
	setResult("Min Intensity", i, mins[i]);
	setResult("Max Intensity", i, maxes[i]);
	setResult("X", i, xs[i]);
	setResult("Y", i, ys[i]);
	setResult("Perimeter", i, perims[i]);
	setResult("Vasculature Length", i, vasculatureLengths[i]);	
	setResult("Max Vessel Distance", i, maxVesselDistances[i]);
	setResult("Mean Vessel Distance", i, meanVesselDistances[i]);
	setResult("Min Vessel Distance", i, minVesselDistances[i]);
	setResult("SD Vessel Distance", i, sdVesselDistances[i]);
}

saveResultsToFile(folderPath);

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
function analyzeArea(filePath, row) {
	run("Clear Results");
	run("Set Measurements...", "area mean min centroid perimeter area_fraction redirect=None decimal=2"); 
	run("Measure"); 
	
	// Extract all Results
	areaPercent = getResult("%Area", 0);
	area = getResult("Area", 0);
	mean = getResult("Mean", 0);
	min = getResult("Min", 0);
	max = getResult("Max", 0);
	x = getResult("X", 0);
	y = getResult("Y", 0);
	perimeter = getResult("Perim.", 0);

	areaPercentages[row] = areaPercent;
	areas[row] = area;
	means[row] = mean;
	mins[row] = min;
	maxes[row] = max;
	xs[row] = x;
	ys[row] = y;
	perims[row] = perimeter;
}

/**
 * Analyze the vessel lengths.
 */
function analyzeVesselLength(filePath, row) {
	run("Clear Results");
	run("Set Measurements...", "area mean min centroid perimeter area_fraction redirect=None decimal=2"); 
	run("Duplicate...", " "); 
	run("Skeletonize"); 
	run("Measure Skeleton Length Tool"); // Install this pplugin!  
	vasculatureLength = getResult("length", 0); 
	vasculatureLengths[row] = vasculatureLength;
}

/**
 * Analyze branches in an image.
 */
function analyzeBranches(filePath, row) {
	run("Clear Results");
	open(filePath);
	run("8-bit");
	run("Median...", "radius=1");
	setOption("BlackBackground", true);
	setThreshold(66, 255); 
	run("Convert to Mask"); 
	run("Analyze Particles...", "size=20-Infinity show=Masks");
	run("Set Measurements...", "area_fraction area mean min centroid perimeter redirect=None decimal=2"); 
	run("Skeletonize (2D/3D)");
	run("Analyze Skeleton (2D/3D)", "prune=none prune_0 show display");
	
	// Save branch analysis results to file
	selectWindow("Results");
	ind = lastIndexOf(filePath, "/");
	folder = substring(filePath, 0, ind);
	fileName = substring(filePath, ind + 1);
	savePath = folder + "../data/branch-data/" + fileName + ".csv";
	saveAs("Results", savePath);

	// Save branch information to file
	selectWindow("Branch information");
	savePath = folder + "../data/branch-data/" + fileName + "-branch-info" + ".csv";
	saveAs("Results", savePath);
	close("Branch information");
	selectWindow("Results");
}

/**
 * Analyze distances between vessels.
 */
function analyzeVesselDistances(filePath, row) {
	getOriginalBinaryImage(filePath);
	
	run("Clear Results");
	run("Put Behind [tab]"); 
	run("Set Measurements...", "area centroid kurtosis area_fraction display redirect=None decimal=6"); 
	run("Duplicate...", " "); 
	run("Analyze Particles...", "size=20-Infinity show=Nothing display"); 
	run("Nnd "); 
	nearestNeighbourDistances = Table.getColumn("C1");
	// Get mean and standard deviation of distances between vessels
	Array.getStatistics(nearestNeighbourDistances, minVesselDistance, maxVesselDistance, meanVesselDistance, sdVesselDistance);	
	
	maxVesselDistances[row] = maxVesselDistance;
	meanVesselDistances[row] = meanVesselDistance;
	minVesselDistances[row] = minVesselDistance;
	sdVesselDistances[row] = sdVesselDistance;
}

/**
 * Analyze a single image, gather various data and save it to respective arrays.
 */
function processFile(filePath, row) {
	print("Analyzing: " + filePath + "...");
	run("Clear Results");
	getOriginalBinaryImage(filePath);
	labels[row] = filePath;
	
	//1 Area fraction 
	analyzeArea(filePath, row);

	//2 Vascular length 
	analyzeVesselLength(filePath, row);
	
	//3 Analyze Branches
	analyzeBranches(filePath, row);
	
	//4 Nearest neighbor distance 
	analyzeVesselDistances(filePath, row);
	
	close("*");
	close("Results");
	close("Branch information");
	close("Nearest Neighbour Distances");
	print("Finished analyzing: " + filePath + ".");
}

/**
 * Save the results table to a csv file.
 */
function saveResultsToFile(folderPath) {
	outputPath = folderPath + "/../data/output.csv";
	saveAs("Results", outputPath); 
	print("Saved results to: " + outputPath);
}