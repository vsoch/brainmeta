#!/usr/bin/python

# ---------------------------------------------------------------------------------
# Experiment 1 Analysis:
# Individual images compared to transformations of themselves.

# INPUT: a single brainmap image
# OUTPUT: similarity metrics for the image across different transformations (compared to original)

# 1. generate multiple transformations
# 2. calculate similarity metrics
# 3. save results


# This is the worker script to run for a single author (on SLURM cluster)
# Usage : authorSynth_cluster.py uuid "author" email outdirectory
# This will look up papers on pubmed, and cross list with
# neurosynth database. You should run this with run_authorSynth_cluster.py

import sys
import pandas
import pickle
import numpy as np
import nibabel as nib
import similarity_metrics as SM
import image_transformations as IT

# Get arguments
image_id = sys.argv[1]
indirectory = sys.argv[2]
tmpdirectory = sys.argv[3]
output_directory = sys.argv[4]
standard_mask = sys.argv[5]
input_file = sys.argv[6]
threshold = sys.argv[7]

# Load other image paths
inputs = pandas.read_csv(input_file,sep="\t")
image_path = "%s/000%s.nii.gz" %(indirectory,image_id)
print "Processing image %s" %(image_path)
original = nib.load(image_path)
mask = nib.load(standard_mask)

# Produce thresholdings (these are all Z score maps, this includes original image (thresh 0))
thresholded1 = IT.threshold_abs(original,thresholds=[threshold])
thresholds1 = np.sort(thresholded1.keys())
image1_labels = ["%s_thr_%s" %(image_id,thresh) for thresh in thresholds1]

# We will have a matrix of image threshold combinations (rows) by similarity metrics (columns)
ordered_column_names = SM.get_column_labels()

# Extract a column (list of similarity metrics) for each image vs original (index 0 == original)
for t in range(0,len(thresholds1)):
  thresh = thresholds1[t]
  image1 = thresholded1[thresh]
  label1 = image1_labels[t]
  # Do a comparison for each pairwise set at each threshold
  for i in inputs.ID:
    image2_path = "%s/000%s.nii.gz" %(indirectory,i)
    image2 = nib.load(image2_path)
    idx=0
    # We will save a data frame for each threshold/image2 of the image
    similarity_metrics = pandas.DataFrame(columns=ordered_column_names)
    #single_metrics = dict()
    # Only proceed if image dimensions are equal, and in same space
    if ((image1.shape == image2.shape) and np.all(image1.get_affine() == image2.get_affine())):
      row_index = []
      thresholded2 = IT.threshold_abs(image2)
      thresholds2 = np.sort(thresholded2.keys())
      image2_labels = ["%s_thr_%s" %(i,th) for th in thresholds2]
      for tt in range(0,len(thresholds2)):
        thresh2 = thresholds2[tt]
        image2 = thresholded2[thresh2]
        label2 = image2_labels[tt]
        try:
          pairwise_metrics,single_metric = SM.run_all(image1=image1,image2=image2,
                               label1=label1,label2=label2,brain_mask=mask,tmpdir=tmpdirectory) 
          # order metric dictionary by our column names, add to data frame   
          similarity_metrics.loc[idx] = [pairwise_metrics[x] for x in ordered_column_names]
          print similarity_metrics.loc[idx]
          #single_metrics.update(single_metric)
          idx+=1
          row_index.append(label2)
        except: print "ERROR: %s and %s" %(label1,label2)
    else:
      print "ERROR: %s and %s are not the same shape!" %(image2_path,image_path)
    # Save the similarity metrics to file
    similarity_metrics.index = row_index
    similarity_metrics.to_csv("%s/000%s_%s_pairwise_metrics.tsv" %(output_directory,label1,i),sep="\t")
    #pickle.dump(single_metrics,open("%s/000%s_%s_single_metrics.pkl" %(output_directory,label1,i),"wb"))
