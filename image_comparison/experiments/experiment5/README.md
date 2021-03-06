### Russ Wisdom

you can think of the replication question really as an image comparison problem.  what I want to do is create a “gold standard” situation for replication, and then work backwards from there to ask how different approaches to replication behave.  the goldest standard I can think of is this:  take the HCP data for a motor task (where we can pretty certain that we should replicate), and then cluster subjects by their overall statistical map similarity in order to find a set of subjects whose maps are as close as possible.  then we sample subjects from the most coherent cluster (i.e. stack the decks in favor of replication).  

using pairs of samples from this set of subjects, we can ask how each of a number of approaches behaves (across a range of sample sizes):
- global correlation of unthresholded statistical maps
- global weighted correlation of unthresholded statistical maps
- overlap of thresholded statistical maps
- overlap of regional activation (using any of several different ROI sets that vary in their size)
- effect size estimates (using either supra threshold clusters, or using one of the two runs to generate a functional ROI for the other run - this has a slight disadvantage which is that the two runs were generated with L-R versus R-L phase encoding)
- ROI based on neurosynth

once we have characterized it for the simple motor task, then we can move to unconstrained sampling, either for that task or the other tasks in the dataset, to see how much things start to break down for each approach.

### Steps

 - Step 1: organize HCP data from the motor task (input file). Since we will possibly want to extend to other tasks, we will use the set of 465 subjects that have all data defined [1.prep_subjects.py](1.prep_subjects.py)
 - Step 2: *currently running* generate distance matrices for each contrast from the motor task in the following ways
   - pearsonr for brainmasked, complete case analysis set of voxels
   - same, but apply normalized weight (0,1) generated from mean values of two images
   - same, but apply normalized weight (0,1) generated from min value between two images
 - Step 3: *not started yet* cluster matrices (representing overall statistical map similarity of subjects) in order to find a set of subjects whose maps are as close as possible.


### Thinking about Reproducibility

I would define replication and reproducibility as follows:
- replication: "is there enough information to do the same thing"
- reproducibility: "do I generate the same result?"

#### Levels of replication
- the environment (OS, software)
- the subject population (what if we reproduce a finding with a different population?)
- the technical steps (Entities, Agents, Activities) that could be captured in something like NIDM
- the unthresholded result map (what we are testing)
- the statistical evaluation for significance
- the final inferences
