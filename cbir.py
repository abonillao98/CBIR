import os
import numpy as np
import re

def distance(hist1,hist2,mode="taxicab"):
    # given two histograms, this function returns their distances according with the mode
    if mode=="taxicab":
        return sum(abs(hist1-hist2))
    
def ten_best_matches(distances):
    # given a list of distances, we get which images are the most similare to the candidate
    # as per the ones with the lowest distance
    d_sorted = sorted(distances)

    matches = []
    for i in range(0,10):
        matches.append(distances.index(d_sorted[i]))

    return matches


# load histogram database. databases:
# hists_256-bins_2000-imgs.npy
hists = np.load("hists_256-bins_2000-imgs.npy",allow_pickle=True)

img_folder = "UKentuckyDatabase" # UKentuckyDatabase test_imgs
current_path = os.getcwd()

f = open("input.txt")
candidates = re.findall(r'\d+', f.read())
f.close()

for candidate in candidates:
    candidate_number = int(candidate) # string to int the candidate picture number
    candidate_hist = hists[candidate_number] # get candidate's histogram
    #print("Candidate picture: " + str(candidate_number))

    # compare candidate's hist with every other picture's hist with distance fucntion
    # each distance is stored in the distances list
    distances = []
    distance_mode = "taxicab"
    for hist in hists: 
        distances.append(distance(candidate_hist,hist,distance_mode))

    matches = ten_best_matches(distances)

    

