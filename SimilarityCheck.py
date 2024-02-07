import argparse
import time
import cv2
import numpy as np
import HelperFunctions as helper



def read_names(file_path):
    with open(file_path) as f:
        lines = f.readlines()
    

    lines = [line.strip() for line in lines]
    return lines

def list_images(folder_path, names, hsvOn:bool):
    start = time.time()
    print("Start")

    images = {}
    for name in names:
        image = cv2.imread(folder_path + name)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        images[name] = image

    if hsvOn:
        images = {name: helper.rgb_to_hsv_image(image) for name, image in images.items()}
        
    end = time.time()
    print(f"time: {end - start}")
    return images        


def precalculate_histograms_for3D(images, names, bindNum, gridNum: int):
    histograms = {name: [] for name in names}

    height, width, _ = images[names[0]].shape

    height //= gridNum
    width //= gridNum

    for name in names:
        for i in range(gridNum):
            for j in range(gridNum):
                histogram = helper.create_histogram_3D(images[name][i * height: (i + 1) * height, j * width: (j + 1) * width], bindNum)
                histogram = np.array(histogram, dtype=float)
                histograms[name].append(histogram)


    return histograms

def apply_similarity_all_3D(histograms1, histograms2, names, size:int):
    correctNum = 0


    for name in names:
        max_similarity = 0
        max_name = name

        hist1_3D = histograms1[name]
        
        for unknown in names:
            hist2_3D = histograms2[unknown]

            similarity = 0

        
            similarity += helper.compare_histograms_3D(hist1_3D, hist2_3D)

            similarity /= size*size



            if max_similarity < similarity:
                max_similarity = similarity
                max_name = unknown
        
        if name == max_name:
            correctNum += 1


    return correctNum / len(names)
    

def precalculate_histograms_for_3channel(images, names, bindNum, gridNum):
    histograms = {name: [] for name in names}

    height, width, _ = images[names[0]].shape

    height //= gridNum
    width //= gridNum

    for name in names:
        for i in range(gridNum):
            for j in range(gridNum):
                histogram = helper.create_histogram_for_3channel(images[name][i * height: (i + 1) * height, j * width: (j + 1) * width], bindNum)
                histogram = np.array(histogram, dtype=float)
                histograms[name].append(histogram)

    return histograms


def apply_similarity_all_3channel(histograms1, histograms2, names, size:int):

    correctNum = 0

    for name in names:
        max_similarity = 0
        max_name = None 
        
        hist1_rgb = histograms1[name]

        for unknown in names:
            hist2_rgb = histograms2[unknown]

            similarity_rgb = 0
            similarity_rgb += helper.compare_histograms_2D(hist1_rgb, hist2_rgb)
            similarity_rgb /= size*size

            average_similarity = similarity_rgb

            if max_similarity < average_similarity:
                max_similarity = average_similarity
                max_name = unknown

        if name == max_name:
            correctNum += 1

           

    return correctNum / len(names)
        

def Find_Similarity( gridNum: int, queryNum:int, channelType:int, hsvOn:bool, bindNums:list):
    pathsupport = "./support_96/"
    path1 = "./query_1/"
    path2 = "./query_2/"
    path3 = "./query_3/"

    names_path = "./InstanceNames.txt"
    names = read_names(names_path)

    supportImages = list_images(pathsupport, names, hsvOn)
    print("supportImages are done") 
    images1 = list_images(path1, names, hsvOn)
    print("images1 are done")
    images2 = list_images(path2, names, hsvOn)
    print("images2 are done")
    images3 = list_images(path3, names, hsvOn)
    print("images3 are done")

    print("ALL IMAGES ARE LISTED")


    for bindNum in bindNums:

        print("NUMBER OF BINDS = " + str(bindNum))
        if channelType == 0:
            histogramsSupport = precalculate_histograms_for3D(supportImages, names, bindNum, gridNum)
            histograms1 = precalculate_histograms_for3D(images1, names, bindNum, gridNum)
            histograms2 = precalculate_histograms_for3D(images2, names, bindNum, gridNum)
            histograms3 = precalculate_histograms_for3D(images3, names, bindNum, gridNum)
        else:
            histogramsSupport = precalculate_histograms_for_3channel(supportImages, names, bindNum, gridNum)
            histograms1 = precalculate_histograms_for_3channel(images1, names, bindNum, gridNum)
            histograms2 = precalculate_histograms_for_3channel(images2, names, bindNum, gridNum)
            histograms3 = precalculate_histograms_for_3channel(images3, names, bindNum, gridNum)


        if queryNum > 0 and queryNum < 4:
            if queryNum == 1:
                histogramsOne = histograms1
            elif queryNum == 2:
                histogramsOne = histograms2
            elif queryNum == 3:
                histogramsOne = histograms3

            if channelType == 0:
                onlyResult = apply_similarity_all_3D(histogramsOne, histogramsSupport, names, gridNum)

            else:
                onlyResult = apply_similarity_all_3channel(histogramsOne, histogramsSupport, names, gridNum)

            print("query" + str(queryNum) + "= " + str(onlyResult))


        else:
            if channelType == 0:
                result1 = apply_similarity_all_3D(histograms1, histogramsSupport, names, gridNum)
                result2 = apply_similarity_all_3D(histograms2, histogramsSupport, names, gridNum)
                result3 = apply_similarity_all_3D(histograms3, histogramsSupport, names, gridNum)
            else:
                result1 = apply_similarity_all_3channel(histograms1, histogramsSupport, names, gridNum)
                result2 = apply_similarity_all_3channel(histograms2, histogramsSupport, names, gridNum)
                result3 = apply_similarity_all_3channel(histograms3, histogramsSupport, names, gridNum)

            print("query1 = " + str(result1))
            print("query2 = " + str(result2))
            print("query3 = " + str(result3))








    


if __name__ == "__main__":

    parser = argparse.ArgumentParser()


    parser.add_argument(
        "gridNum", 
        type=int, 
        help="grid number"
    )
    parser.add_argument(
        "queryNum", 
        type=int, 
        choices=[0, 1, 2, 3],
        help="Query number (choose from 0, 1, 2, or 3)"
    )
    parser.add_argument(
        "channelType", 
        type=int, 
        choices=[0, 1],
        help="Channel type (0 for 3D, 1 for 3-channel)"
    )
    parser.add_argument(
        "--hsvOn", 
        action="store_true", 
        help="Use HSV color space"
    )
    parser.add_argument(
        "bindNums", 
        type=int, 
        nargs='+',
        metavar="bindNum",
        help="List of bind numbers"
    )

    # Parse command-line arguments
    args = parser.parse_args()

    startmain = time.time()
    print("StartMain")


    Find_Similarity(args.gridNum ,args.queryNum, args.channelType, args.hsvOn, args.bindNums)

    endMain = time.time()
    print(f"time: {endMain - startmain}")