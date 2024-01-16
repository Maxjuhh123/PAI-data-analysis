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
 * Analyze branches in an image.
 */
function analyzeBranches(filePath, row, numBranchesList, averageBranchLengths, maximumBranchLengths) {
	// Analyze original binary image
	getOriginalBinaryImage(filePath);
	run("Clear Results");
	run("Set Measurements...", "area_fraction area mean min centroid perimeter redirect=None decimal=2"); 
	run("Duplicate...", " "); 
	run("Skeletonize");
	run("Analyze Skeleton (2D/3D)", "prune=none show"); 
	
	// Extract results from table
	numBranches = getResult("# Branches", 0);
	averageBranchLength = getResult("Average Branch Length", 0);
	maximumBranchLength = getResult("Maximum Branch Length", 0);

	// Save results in arrays
	numBranchesList[row] = numBranches;
	averageBranchLengths[row] = averageBranchLength;
	maximumBranchLengths[row] = maximumBranchLength;
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
	analyzeArea(filePath, row, areaPercentages);

	//2 Vascular length 
	analyzeVesselLength(filePath, row, vasculatureLengths);
	
	//3 Analyze Branches
	analyzeBranches(filePath, row, numBranchesList, averageBranchLengths, maximumBranchLengths);
	
	//4 Nearest neighbor distance 
	analyzeVesselDistances(filePath, row, meanVesselDistances, minVesselDistances);
	
	// Update result arrays
	labels[row] = filePath;
	
	close("*");
	close("Results");
	//close("Branch information");
	close("Nearest Neighbour Distances");
	print("Finished analyzing: " + filePath + ".");
}

/**
 * Save the results table to a csv file.
 */
function saveResultsToFile(folderPath) {
	outputPath = folderPath + "/output.csv";
	saveAs("Results", outputPath); 
	print("Saved results to: " + outputPath);
}

folderPath = getDirectory("Choose a Directory"); 
processFolder(folderPath); 
saveResultsToFile(folderPath);