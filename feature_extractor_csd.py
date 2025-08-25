import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

'''
Given the 2000 images of the UKentuckyDatabse, this script produces a .npy file
with 2000 CSD histograms indexated by the image number
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

def rgb2hmmd(img_rgb):
    # Given a RGB image, this function returns the same image converted
    # into the HMMD color space (Hue,Diff,Sum)
    img_hmmd = np.zeros([img_rgb.shape[0],img_rgb.shape[1],img_rgb.shape[2]],dtype="float32")
    # looping through the whole image
    for i in range(1,img_rgb.shape[0]):
        for j in range(1,img_rgb.shape[1]):
            # Max and Min
            maxx = max(img_rgb[i,j,:])
            minn = min(img_rgb[i,j,:])

            # Computing Hue
            r = img_rgb[i,j,0]
            g = img_rgb[i,j,1]
            b = img_rgb[i,j,2]

            if maxx == minn:
                hue = 0
            elif (maxx == r) and (g >= b):
                hue = 60*((g-b)/(maxx-minn))
            elif (maxx == r) and (g < b):
                hue = 360 + 60*((g-b)/(maxx-minn))
            elif g == maxx:
                hue = 60*(2.0+ ((b-r)/(maxx-minn)))
            else:
                hue = 60*(4.0+ ((r-g)/(maxx-minn)))

            hue = hue / 360; # Hue normalisation

            # Diff and Sum computing
            difference = maxx - minn
            summ = (maxx + minn)/2

            # Value assignment in each channel
            img_hmmd[i,j,0]=hue
            img_hmmd[i,j,1]=difference
            img_hmmd[i,j,2]=summ        

    return img_hmmd

def hmmd_quantize(img_hmmd):
    # Given a HMMD image, this function returns a quantized HMMD image
    rows = img_hmmd.shape[0]
    columns = img_hmmd.shape[1]

    img_hmmd_quantized = np.zeros([rows,columns])

    diff_thresholds = [6/255, 20/255, 60/255, 110/255]
    #          Hue  Sum
    levels = [ [1, 32],  # Subspace 0 - 1*32=32 + 0 = 32 | 1st offset
               [4,  8],  # Subspace 1 - 4*8=32 + 32 = 64 | 2nd offset
               [16,  4], # Subspace 2 - 16*4=64 + 64 = 128 | 3rd offset
               [16,  4], # Subspace 3 - 16*4=64 + 128 = 192 | 4th offset
               [16,  4]] # Subspace 4 - 16*4=64 + 192 = 256
    
    # Offset for each histogram zone
    zone_offsets = [0, 32, 64, 128, 192];  # bin accumulation per subspace
    
    for i in range(rows):
        for j in range(columns):         
            H = img_hmmd[i,j][0]
            D = img_hmmd[i,j][1]
            S = img_hmmd[i,j][2]

            # Avoid overflow per 1.0 values
            epsilon = 1e-10
            H = min(H, 1 - epsilon)
            S = min(S, 1 - epsilon)           

            if 0 <= D < diff_thresholds[0]:
                zone = 0
            elif diff_thresholds[0] <= D < diff_thresholds[1]:
                zone = 1
            elif diff_thresholds[1] <= D < diff_thresholds[2]:
                zone = 2
            elif diff_thresholds[2] <= D < diff_thresholds[3]:
                zone = 3 
            else:
                zone = 4

            #print("diff: "  + str(diff_thresholds))
            #print("HDS: " + str(H) + " " + str(D) + " " + str(S))
            #print(str(zone))

            hue_levels = levels[zone][0]
            sum_levels = levels[zone][1]

            # Quantization
            h_q = np.floor(H * hue_levels)
            s_q = np.floor(S * sum_levels)

            # Global value of the [i,j]st bin
            img_hmmd_quantized[i,j] = zone_offsets[zone] + s_q * hue_levels + h_q

    return img_hmmd_quantized  
    

tic()
img_folder = "test_imgs" # UKentuckyDatabase test_imgs
current_path = os.getcwd()
img_names = os.listdir(current_path + "/" + img_folder)
bins=256
num_of_images=len(img_names)

hists = []

for img_name in img_names:
    img_bgr = cv2.imread(img_folder+"/"+img_name,cv2.IMREAD_COLOR).astype(np.float32)/255 # had an overflow problem using default uint8 type when transforming into hmmd colorspace
    img_rgb = img_bgr[:, :, ::-1]

    # Convert from RGB to HMMD color space
    img_hmmd = rgb2hmmd(img_rgb)

    # Non-uniform quantization to the HMMD image
    img_hmmd_quantized = hmmd_quantize(img_hmmd)

    # Sweep with the 8x8 structuring element
    csd_hist = np.zeros(bins)









#np.save("hists_"+str(bins)+"-bins_"+str(num_of_images)+"-imgs_csd.npy", np.array(hists, dtype=object), allow_pickle=True)
toc()