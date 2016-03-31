# -*- coding: utf-8 -*-
import cv2
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt


def show_image(img, window_name='image'):
    '''
    Display the image.
    When a key is pressed, the window is closed

    Parameters:
    ------
    img: multidimensional numpy array
        image
    window_name: str, optional
        name of the window
    '''
    fig = plt.figure()
    plt.axis("off")
    if len(img.shape) == 3:
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    else:
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_GRAY2RGB))
    fig.canvas.set_window_title(window_name)
    plt.gcf().canvas.mpl_connect('key_press_event',
                                lambda event: plt.close(event.canvas.figure))
    plt.show()


def visualize_elements(img,
                       holes=None, islands=None,
                       indentations=None, protrusions=None,
                       visualize=True,
                       display_name='salient regions'):
    '''
    Display the image with the salient regions provided.

    Parameters:

    img: multidimensional numpy array
        image
    holes:  2-dimensional numpy array with values 0/255, optional
        The holes, to display in blue
    islands:  2-dimensional numpy array with values 0/255, optional
        The islands, to display in yellow
    indentations:  2-dimensional numpy array with values 0/255, optional
        The indentations, to display in green
    protrusions:  2-dimensional numpy array with values 0/255, optional
        The protrusions, to display in red
    visualize:  bool, optional
        vizualizations flag
    display_name: str, optional
        name of the window



    Returns:
    ------
    img_to_show: 3-dimensional numpy array
        image with the colored regions
    '''
    # colormap bgr
    colormap = {'holes': [255, 0, 0],  # BLUE
                'islands': [0, 255, 255],  # YELLOW
                'indentations': [0, 255, 0],  # GREEN
                'protrusions': [0, 0, 255]  # RED
                }

    # if the image is grayscale, make it BGR:
    if len(img.shape) == 2:
        img_to_show = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    else:
        img_to_show = img.copy()
    if holes is not None:
        img_to_show[[holes>0]] = colormap['holes']
    if islands is not None:
        img_to_show[[islands>0]] = colormap['islands']
    if indentations is not None:
        img_to_show[[indentations>0]] = colormap['indentations']
    if protrusions is not None:
        img_to_show[[protrusions>0]] = colormap['protrusions']

    if visualize:
        show_image(img_to_show, window_name=display_name)
    return img_to_show


def binarize(img, threshold=-1, visualize=True):
    '''
    Binarize the image according to a given threshold.
    Returns a one-channel image with only values of 0 and 255.

    Parameters:
    ------
    img: 3-dimensional numpy array
        image to fill
    threshold: int, optional
        threshold value. If -1 (default), OTSU thresholding is used.
    visualize: bool, optional
        option for vizualizing the process

    Returns:
    ------
    binzarized:  2-dimensional numpy array with values 0/255
        The binarized image
    '''
    if threshold == -1:
        _, binarized = cv2.threshold(img, 0, 255,
                                     cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    else:
        _, binarized = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

    # If the image still has three channels, only pick one
    if len(binarized.shape) > 2:
        binarized = binarized[:,:,0]
    if visualize:
        show_image(binarized,
                   window_name=('Binarized with threshold %i' % threshold))
    return binarized


def read_matfile(filename, visualize=True):
    '''
    Read a matfile with the binary masks for the salient regions.
    Returns:
        islands, holes, protrusions, indentations
    These are masks with 0/255 values for the 4 salient types

    Parameters:
    ------
    filename: str
        Path to the mat file
    visualize: bool, optional
        option for vizualizing the process

    Returns:
    ------
    holes:  2-dimensional numpy array with values 0/255
        Binary image with holes as foreground
    islands:  2-dimensional numpy array with values 0/255
        Binary image with islands as foreground
    protrusions:  2-dimensional numpy array with values 0/255
        Binary image with protrusions as foreground
    indentations:  2-dimensional numpy array with values 0/255
        Binary image with indentations as foreground
    '''
    matfile = sio.loadmat(filename)
    regions = matfile['saliency_masks']*255
    holes = regions[:,:,0]
    islands = regions[:,:,1]
    indentations = regions[:,:,2]
    protrusions = regions[:,:,3]
    if visualize:
        show_image(holes, 'holes')
        show_image(islands, 'islands')
        show_image(indentations, 'indentations')
        show_image(protrusions, 'protrusions')
    return holes, islands, indentations, protrusions


def image_diff(img1, img2, visualize=True):
    '''
    Compares two images and shows the difference.
    Useful for testing purposes.

    Parameters:
    ------
    img1: 2-dimensional numpy array with values 0/255
        first image to compare
    img1: 2-dimensional numpy array with values 0/255
        second image to compare
    visualize: bool, optional
        option for vizualizing the process

    Returns:
    ------
    is_same: bool
        True if all pixels of the two images are equal
    '''
    if visualize:
        show_image(cv2.bitwise_xor(img1, img2), 'difference')
    return np.all(img1 == img2)

def array_diff(arr1, arr2):
    '''
    Compares two arrays. Useful for testing purposes.

    Parameters:
    ------
    arr1: 2-dimensional numpy, first array to compare
    arr2: 2-dimensional numpy, second array to compare

    Returns:
    ------
    is_close: bool
        True if elemetns of the two arrays are close within the given tolerance
    '''
    return np.allclose(arr1, arr2)


def get_SE(img, SE_size_factor=0.15, lam_factor=5):
    '''
    Get the structuring element en minimum salient region area for this image.

    Parameters:
    ------
    img: 2-dimensionalnumpyarray with values 0/255
        image to detect islands
    SE_size_factor: float, optional
        The fraction of the image size that the SE should be

    Returns:
    ------
    SE: 2-dimensional numpy array of shape (k,k)
        The structuring element to use in processing the image
    lam: float
        lambda, minimumm area of a salient region
    '''
    nrows, ncols = img.shape
    ROI_area = nrows*ncols
    SE_size = int(np.round(SE_size_factor*np.sqrt(ROI_area/np.pi)))
    SE_dim_size = SE_size * 2 - 1
    SE = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                   (SE_dim_size, SE_dim_size))
    lam = lam_factor*SE_size
    return SE, lam


def get_SEhi(SE, lam, scaleSE=2, scalelam=10):
    '''
    Get the smaller structuring element from the large structuring element

    Parameters:
    ------
    SE: 2-dimensional numpy array of shape (k,k)
        The large structuring element
    scale: int
        scale indicating how much smaller the smal SE should be

    Returns:
    ------
    SEhi: 2-dimensional numpy array of shape (k,k)
        The smaller structuring element to use in processing the image
    lam_hi: float
        Minimum area of salient region detected on boundaries of holes/islands
    '''
    SEhi = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                     (int(SE.shape[0]/scaleSE),
                                      int(SE.shape[1]/scaleSE)))
    lamhi = lam/scalelam
    return SEhi, lamhi


def data_driven_binarization(img,
                             area_factor_large=0.001,
                             area_factor_verylarge=0.1,
                             lam=-1, SE_size_factor=0.15,
                             weights=(0.33, 0.33, 0.33),
                             offset=80,
                             num_levels=256, otsu_only=False,
                             connectivity=4, visualize=True):
    '''
    Binarize the image such that the desired number of (large) connected
    components is maximized.

    Parameters:
    ------
    img: 2-dimensional numpy array with values between 0 and 255
        grayscale image to binarize
    area_factor_large: float, optional
        factor that describes the minimum area of a large CC
    area_factor_verylarge: float, optional
        factor that describes the minimum area of a very large CC
    lam: float, optional
        lambda, minimumm area of a connected component
    weights: (float, float, float)
        weights for number of CC, number of large CC
        and number of very large CC respectively.
    offset: int, optional
        The offset (number of gray levels) to search for around the Otsu level
    num_levels: int, optional
        number of gray levels to be considered [1..255],
        the default number 256 gives a stepsize of 1.
    otsu_only: bool, optional
        Option to only perform otsu binarization
    connectivity: int
        What connectivity to use to define CCs
    visualize: bool, optional
        option for vizualizing the process

    Returns:
    ------
    t_opt: int
        optimal threshold
    binarized: 2-dimensional numpy array with values 0/255
        The binarized image
    '''
    t_otsu, binarized_otsu = cv2.threshold(img, 0, 255,
                                           cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    t_otsu = int(t_otsu)
    if otsu_only:
        return t_otsu, binarized_otsu
    area = img.size
    if lam == -1:
        _, lam = get_SE(img)
    area_large = area_factor_large*area
    area_verylarge = area_factor_verylarge*area

    # Initialize the count arrays
    a_nccs = np.zeros(256)
    a_nccs_large = np.zeros(256)
    a_nccs_verylarge = np.zeros(256)

    step = 256/num_levels
    for t in xrange(max(t_otsu-offset, 0), min(t_otsu+offset, 255), step):
        bint = binarize(img, threshold=t, visualize=False)
        nccs, labels, stats, centroids = cv2.connectedComponentsWithStats(
                                            bint, connectivity=connectivity)
        areas = stats[:, cv2.CC_STAT_AREA]
        a_nccs[t] = sum(areas > lam)
        a_nccs_large[t] = sum(areas > area_large)
        a_nccs_verylarge[t] = sum(areas > area_verylarge)

    # Normalize
    a_nccs = a_nccs/float(a_nccs.max())
    a_nccs_large = a_nccs_large/float(a_nccs_large.max())
    a_nccs_verylarge = a_nccs_verylarge/float(a_nccs_verylarge.max())
    scores = weights[0]*a_nccs + \
             weights[1]*a_nccs_large + \
             weights[2]*a_nccs_verylarge
    t_opt = scores.argmax()
    binarized = binarize(img, threshold=t_opt, visualize=visualize)
    if visualize:
        fig = plt.figure()
        fig.canvas.set_window_title('Number of CCs per threshold level')
        plt.plot(scores)
        plt.axvline(x=t_opt, color='red')
        plt.axvline(x=t_otsu, color='green')
        plt.xlim(0, 255)
        plt.gcf().canvas.mpl_connect('key_press_event',
                                    lambda event: plt.close(event.canvas.figure))
        plt.show()
    return t_opt, binarized


def region2ellipse(half_major_axis, half_minor_axis, theta):
    ''' Conversion of elliptic parameters to polynomial coefficients.

    Parameters:
    ------
    half_major_axis: float, half of the length of the ellipse's major axis
    half_minor_axis: float, half of the length of the ellipse's minor axis
    thetha- the ellipse orientaiton- angle (radians) between the major and x axis

    Returns:
    ------
    A, B, C: floats, the coefficients of the equation of ellipse
    '''

    # thrigonometric functions
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)
    sin_cos_theta = sin_theta * cos_theta

    # squares
    a_sq = half_major_axis * half_major_axis
    b_sq = half_minor_axis * half_minor_axis
    sin_theta_sq = sin_theta * sin_theta
    cos_theta_sq = cos_theta * cos_theta

    # common denominator
    denom = a_sq*b_sq

    A = (b_sq*cos_theta_sq + a_sq*sin_theta_sq)/denom
    B = ((b_sq - a_sq)*sin_cos_theta)/denom
    C = (b_sq*sin_theta_sq + a_sq*cos_theta_sq)/denom

    return A, B, C
