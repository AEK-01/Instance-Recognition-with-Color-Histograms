
import numpy as np
import cv2



def rgb_to_hsv_image(image):

    hsv_image = np.zeros_like(image, dtype=np.float32)


    for i in range(image.shape[0]):
        for j in range(image.shape[1]):

            r, g, b = image[i, j]


            h, s, v = rgb_to_hsv((r, g, b))


            hsv_image[i, j] = [h, s, v]

    return hsv_image



def rgb_to_hsv(rgb):

    r, g, b = rgb
    r, g, b = r / 255.0, g / 255.0, b / 255.0


    cMax = max(r, g, b)
    cMin = min(r, g, b)
    deltaC = cMax - cMin


    if deltaC == 0:
        h = 0
    elif cMax == r:
        h = 1/6 * (((r - g) / deltaC) % 6)
    elif cMax == g:
        h = 1/6 * ((g - b) / deltaC + 2)
    elif cMax == b:
        h = 1/6 * ((b - r) / deltaC + 4)



    v = cMax


    
    if v == 0:
        s = 0
    else:
        s = (deltaC / cMax)

    h *= 255
    s *= 255
    v *= 255
    return h, s, v



def create_histogram_for_3channel(image, num_of_bins):

    quantized_image = image  / 256.0


    ind_r = (quantized_image[:, :, 0] * num_of_bins).astype(int)
    ind_g = (quantized_image[:, :, 1] * num_of_bins).astype(int)
    ind_b = (quantized_image[:, :, 2] * num_of_bins).astype(int)



    r_histogram = np.bincount(ind_r.flatten(), minlength=num_of_bins)
    g_histogram = np.bincount(ind_g.flatten(), minlength=num_of_bins)
    b_histogram = np.bincount(ind_b.flatten(), minlength=num_of_bins)


    return r_histogram, g_histogram, b_histogram




def create_histogram_3D(image, num_of_bins):

    quantized_image = image / 256.0


    ind_r = (quantized_image[:, :, 0] * num_of_bins).astype(int)
    ind_g = (quantized_image[:, :, 1] * num_of_bins).astype(int)
    ind_b = (quantized_image[:, :, 2] * num_of_bins).astype(int)


    combined_indices = ind_r + num_of_bins * (ind_g + num_of_bins * ind_b)
 

    histogram_3d = np.bincount(combined_indices.flatten(), minlength=num_of_bins**3).reshape((num_of_bins, num_of_bins, num_of_bins))


    return histogram_3d













def compare_histograms_3D(histogram1, histogram2):

    histogram1 = np.array(histogram1, dtype=float)
    histogram2 = np.array(histogram2, dtype=float)


    histogram1 /= np.sum(histogram1)
    histogram2 /= np.sum(histogram2)


    similarity_array = np.minimum(histogram1, histogram2)

    similarity = np.sum(similarity_array)

    return similarity


def compare_histograms_2D(histogram1, histogram2):

    histogram1 = np.array(histogram1, dtype=float)
    histogram2 = np.array(histogram2, dtype=float)




    histogram1 /= np.sum(histogram1)
    histogram2 /= np.sum(histogram2)



    similarity_array = np.minimum(histogram1, histogram2)

    similarity = np.sum(similarity_array)

    return similarity


