import os
import cv2
import numpy as np
'''
Given the 2000 images of the UKentuckyDatabse, this script produces a .npy file
with 2000 gray-color histograms indexated by the image number
'''

# Python's version of Matlab's "Tic / Toc" functions
# Credits to StackOverflow user GuestPoster
def tic():
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()

def toc():
    import time
    if 'startTime_for_tictoc' in globals():
        print("Elapsed time is " + str(time.time() - startTime_for_tictoc) + " seconds.")
    else:
        print("Toc: start time not set")

tic()
img_folder = "UKentuckyDatabase" # UKentuckyDatabase test_imgs
current_path = os.getcwd()
img_names = os.listdir(current_path + "/" + img_folder)
bins=256
num_of_images=len(img_names)

hists = []

for img_name in img_names:
    img = cv2.imread(img_folder+"/"+img_name)
    hist = cv2.calcHist([img],[0],None,[bins],[0,bins])
    hist = hist/max(hist) # normalize histogram
    hists.append(hist)

np.save("hists_"+str(bins)+"-bins_"+str(num_of_images)+"-imgs_gray.npy", np.array(hists, dtype=object), allow_pickle=True)
toc()