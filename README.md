# organize_ukbb

The order of operations is:

### 1 - makePhase.R
	Inputs: scott.fam - which is from the calls file and the sample qc, eid in first column
		p1Index - Indices of the scott.fam which correspond to the first and second phase
	Outputs: scott.phase1/2 - eids for those in phase1 and phase2 (determined however you want)
	Description: Does not do very much but split up a big fam file into two small ones

### 2 - reoderPheno.R
	Inputs: scottPheno.csv.gz - the raw output from the ukbfetch code (should be from two applications, although code easily change code for 1)
		scott.phase1/2 - output from above
	Outputs: scottPheno.1/2.RDS - The column bound phenotype files read in and seperated according to the phases
		scott2.phenIndex.1/2 - The row indices of each scott.phase1/2 that correspond to the rows of scottPheno.1/2.RDS

### 3 - convertRDS.R
	Description: will split up the large scottPheno.1/2.RDS files into chunks of plain text scott.opcs.1 for example that are just about opcs

### 4 - evalPheno.py
	Description: Finally reformat everything into a really nice file where each column corresponds to one diagnosis
