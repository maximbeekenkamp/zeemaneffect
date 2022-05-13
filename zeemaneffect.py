from cmath import pi

import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from scipy.stats import linregress

"""
Baseline wavelength of green light in mecury vapour used throughout the document
"""
wavl = 546.1 * 10**(-9)

"""
Import csv files
"""
ringdata = pd.read_csv(
    "/Users/maximbeekenkamp/Desktop/Physics/PHYS 560/Zeeman Effect/zeeman_ring_data.csv", sep=",")
angledata = pd.read_csv(
    "/Users/maximbeekenkamp/Desktop/Physics/PHYS 560/Zeeman Effect/zeeman_angle_data.csv", sep=",")
HPFP_1 = pd.read_csv(
    "/Users/maximbeekenkamp/Desktop/Physics/PHYS 560/Zeeman Effect/HorizontalPFP_Splitting.csv", sep=",")
HPFP_2 = pd.read_csv(
    "/Users/maximbeekenkamp/Desktop/Physics/PHYS 560/Zeeman Effect/HPFP_effect2.csv", sep=",")
HPFP_3 = pd.read_csv(
    "/Users/maximbeekenkamp/Desktop/Physics/PHYS 560/Zeeman Effect/HPFP_effect3.csv", sep=",")
HPFP_4 = pd.read_csv(
    "/Users/maximbeekenkamp/Desktop/Physics/PHYS 560/Zeeman Effect/HPFP_effect4.csv", sep=",")
HPFP_5 = pd.read_csv(
    "/Users/maximbeekenkamp/Desktop/Physics/PHYS 560/Zeeman Effect/HPFP_effect5.csv", sep=",")
HPFP_6 = pd.read_csv(
    "/Users/maximbeekenkamp/Desktop/Physics/PHYS 560/Zeeman Effect/HPFP_effect6.csv", sep=",")
HPFP_7 = pd.read_csv(
    "/Users/maximbeekenkamp/Desktop/Physics/PHYS 560/Zeeman Effect/HorizontalProfilePlot.csv", sep=",")

"""
Make lists for both pixel and intesity data containing all the different plots 
"""

HPFP_pixels = []
HPFP_intensity = []

ring_increment = ringdata["increment(m)"].to_numpy()
ring_count = ringdata["count"].to_numpy()

angle_left = angledata["left"].to_numpy()
angle_right = angledata["right"].to_numpy()

HPFP_1_pixels = HPFP_1["X"].to_numpy()
HPFP_pixels.append(HPFP_1_pixels)
HPFP_1_intensity = HPFP_1["Y"].to_numpy()
HPFP_intensity.append(HPFP_1_intensity)

HPFP_2_pixels = HPFP_2["X"].to_numpy()
HPFP_pixels.append(HPFP_2_pixels)
HPFP_2_intensity = HPFP_2["Y"].to_numpy()
HPFP_intensity.append(HPFP_2_intensity)

HPFP_3_pixels = HPFP_3["X"].to_numpy()
HPFP_pixels.append(HPFP_3_pixels)
HPFP_3_intensity = HPFP_3["Y"].to_numpy()
HPFP_intensity.append(HPFP_3_intensity)

HPFP_4_pixels = HPFP_4["X"].to_numpy()
HPFP_pixels.append(HPFP_4_pixels)
HPFP_4_intensity = HPFP_4["Y"].to_numpy()
HPFP_intensity.append(HPFP_4_intensity)

HPFP_5_pixels = HPFP_5["X"].to_numpy()
HPFP_pixels.append(HPFP_5_pixels)
HPFP_5_intensity = HPFP_5["Y"].to_numpy()
HPFP_intensity.append(HPFP_5_intensity)

HPFP_6_pixels = HPFP_6["X"].to_numpy()
HPFP_pixels.append(HPFP_6_pixels)
HPFP_6_intensity = HPFP_6["Y"].to_numpy()
HPFP_intensity.append(HPFP_6_intensity)

HPFP_7_pixels = HPFP_7["X"].to_numpy()
HPFP_pixels.append(HPFP_7_pixels)
HPFP_7_intensity = HPFP_7["Y"].to_numpy()
HPFP_intensity.append(HPFP_7_intensity)


"""
This section analyses the ring counting portion of our experiment (day 1 of lab)
Here we are trying to measure the wavelength by changing the variable d which is 
the distance between the mirrors of our Fabry Perot interferometer.
"""

"""
Initialising graph plot 0
"""
fig0, ax0 = plt.subplots()
ax0.set_title("Zeeman Effect - Count Rings, change distance between mirrors")
ax0.set_xlabel("Increment (m)")  # Increment is refering to d
ax0.set_ylabel("Ring Count")

# Increment vs Ring Count Plot
ax0.plot(ring_increment, ring_count, label="Rings")

def linear_fit(x: list[float], A: float, B: float) -> list[float]:
    """
    Linear fit creates a straight line 
    output looks like:
    list[float]

    :param x: the list of floats which act as the input data for our x axis.
    :param A: a float which will be the gradient of our straight line.
    :param B: a float which will be the y intercept.
    :return: a list y for input x where y is defined by Ax + B.
    """
    return [A*x1 + B for x1 in x]


"""
Initialising graph plot 0 fit
"""

"""
popt contains all the relevant information of our linear fit such as the 
gradient [0] of our fit and the y intercept [1] of our fit
"""

popt, pcov = curve_fit(linear_fit, ring_increment, ring_count)

"""
lineregress does in theory the same thing as curve_fit but is less finiky and 
seems more accurate at times.
"""
linfit = linregress(ring_increment, ring_count)
# print(linfit)

# Fit plot superimposed on the count increment plot
ax0.plot(ring_increment, linear_fit(ring_increment, popt[0], popt[1]),
         label="Fit", color="red")

ax0.legend(bbox_to_anchor=(1.0, 1.0), loc='upper right')

"""
Here we're using the measured data to measure the wavelength. We're using 
the small angle approximation n=2d/wavl. 
"""

measured_wavl = (linfit[0] ** (-1))/2
# print(measured_wavl)

wavl_error = ((abs(wavl - measured_wavl))/abs(wavl))*100
# print(wavl_error)

"""
This section analyses the ring counting portion of our experiment (day 2 of lab)
Here we are trying to measure the wavelength by changing the variable theta 
which is the angle from the normal of the light as it enters our Fabry Perot 
interferometer.
"""

cam_extent_fov = (8 + (53/60)) * (pi/180)


def difference(lst: list[float]) -> list[float]:
    """
    Gives us the difference between neighbouring elements of a list 
    output looks like:
    list[float]

    :param lst: the list of floats which act as the input data
    :return: a list containing the absolute difference between two adjacent 
    elements of the list. The output list will be of length len(lst)-1
    """
    return [abs(j-i) for i, j in zip(lst, lst[1:])]


anglesleft = difference(angle_left)
anglesright = difference(angle_right)

angles_dif_av = [0] * len(anglesleft)

for i in range(len(anglesleft)):
    angles_dif_av[i] = (abs(anglesright[i] - anglesleft[i])) * (pi/180)


def cumulative(lst: list[float]) -> list[float]:
    """
    Gives us the cumulative sum of the elements of a list
    output looks like:
    list[x0, (x0+x1), (x0+x1+x2), ...]

    :param lst: the list of floats which act as the input data.
    :return: a list containing the cumulative sum of the input list.
    """
    cu_list = []
    length = len(lst)
    cu_list = [sum(lst[0:x:1]) for x in range(0, length+1)]
    return cu_list[1:]


theta_y_data = [0] + cumulative(angles_dif_av)

for i in range(len(theta_y_data)):
    theta_y_data[i] = theta_y_data[i]**2
# print(theta_y_data)

p_x_data: list[float] = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]

"""
Initialising graph plot 1
"""
fig1, ax1 = plt.subplots()
ax1.set_title("Zeeman Effect - Count Rings, change angle")
ax1.set_xlabel(r"$p$")
ax1.set_ylabel(r"$\theta^2$")

# Theta^2 vs Ring Count Plot
ax1.plot(p_x_data[2:], theta_y_data[2:])

"""
Initialising graph plot 1 fit
"""
popt1, pcov1 = curve_fit(linear_fit, p_x_data[2:], theta_y_data[2:])
# print(popt1[0])
linfit1 = linregress(p_x_data[2:], theta_y_data[2:])
print(linfit1)
# print(theta_y_data)
popt1 = [float(x) for x in popt1]  # this avoids some weird errors with plot
print(popt1)
# Fit plot superimposed on the angle count plot
ax1.plot(p_x_data[2:], linear_fit(p_x_data[2:], popt1[0], popt1[1]),
         label="Fit", color="red")

ax1.legend(bbox_to_anchor=(1.0, 1.0), loc='upper right')

"""
This section contains all the data analysis of the magnetic field portion of the 
lab.
"""

def show_plot7(num: int):
    """
    Gives us the plot of our 7th csv input file. Plot 7 is the plot which has 
    zero magnetic field acting upon it. As such it acts as our reference plot 
    and is treated seperately from our other plots. This function gives both the
    plot as well as the peaks.
    output looks like:
    <graph of plot 7 + peaks>
    list[float]

    :param num: the num of the plot the function should analyse. For this 
    function this should only ever be 7.
    :return: a list containing the pixel location of the peaks of our plot.
    The function will also output the plot for this data set.
    """

    """
    Initialising local graph plot
    """
    fig, ax = plt.subplots()
    ax.set_title("Zeeman Effect - Horizontal PFP " + str(num))
    ax.set_xlabel("Pixels")
    ax.set_ylabel("Intensity")

    # Intensity vs Pixel Plot
    ax.plot(HPFP_pixels[num-1], HPFP_intensity[num-1],
            label="HPFP " + str(num))

    """
    Initialising local graph peak plot
    """
    peaks = find_peaks(HPFP_intensity[num-1], height=0, distance=7, width=4)
    height = peaks[1]['peak_heights']
    a = len(height)  # this prevents dimension errors for the scatter plot
    peak_pos = HPFP_pixels[num-1][peaks[0]]
    # Peak plot superimposed on the intensity pixel plot
    ax.scatter(peak_pos, height, s=a,  color="r", marker="x", label="Maxima")

    ax.legend(bbox_to_anchor=(1.0, 1.0), loc='upper right')
    return peak_pos

# pixel to distance conversion
# distance between peaks is on wavelength


"""
This section contains the pixel to r conversion as well as r to theta. The data 
from plot 7 is used here as it is the most well defined.
"""
# f constant
f = 67.2 * 10 ** (-3)

av_pixel_spacing = sum(difference(show_plot7(7)))/(len(show_plot7(7)-1))
conversion_r = (wavl/av_pixel_spacing)
conversion_theta = conversion_r/f


def show_plot(num: int):
    """
    Gives us the plot of our num input csv input file. All these plots have 
    various amounts of magnetic field (check lab book). As such we must relax
    our restrictions on what can be counted as a peak (see peak in show_plot7 vs
    peak in show_plot). This means we will have more peaks than we want which 
    we'll have to remove later by hand. This function gives both the plot as 
    well as the peaks.
    output looks like:
    <graph of plot (num) + peaks>
    list[float]

    :param num: the num of the plot the function should analyse. For this 
    function this should be our options other than 7 (function will still work 
    with 7).
    :return: a list containing the pixel location of the peaks of our plot.
    The function will also output the plot for this data set.
    """

    """
    Initialising local graph plot
    """
    fig, ax = plt.subplots()
    ax.set_title("Zeeman Effect - Horizontal PFP " + str(num))
    ax.set_xlabel("Pixels")
    ax.set_ylabel("Intensity")

    # Intensity vs Pixel Plot
    ax.plot(HPFP_pixels[num-1], HPFP_intensity[num-1],
            label="HPFP " + str(num))

    """
    Initialising local graph peak plot
    """
    peaks = find_peaks(HPFP_intensity[num-1], height=0)
    height = peaks[1]['peak_heights']
    a = len(height)  # this prevents dimension errors for the scatter plot
    peak_pos = HPFP_pixels[num-1][peaks[0]]
    # Peak plot superimposed on the intensity pixel plot
    ax.scatter(peak_pos, height, s=a,  color="r", marker="x", label="Maxima")

    ax.legend(bbox_to_anchor=(1.0, 1.0), loc='upper right')
    return list(peak_pos)


# bug prevention
peak_pos_1 = list(show_plot(1))
peak_pos_2 = list(show_plot(2))
peak_pos_3 = list(show_plot(3))
peak_pos_4 = list(show_plot(4))
peak_pos_5 = list(show_plot(5))
peak_pos_6 = list(show_plot(6))
peak_pos_7 = list(show_plot7(7))


def findMiddle(lst: list[float]):
    """
    Gives us the middle x pixel of out input list.
    output looks like:
    tuple(list[int], list[int])

    :param lst: the list of floats which act as the input data.
    :return: a list which contains the middle pixel or a tuple containing a list
    containing the int pixel value of the two middle pixels if the input list is
    of an odd length. 
    """
    middle = float(len(lst))/2
    if middle % 2 != 0:
        return lst[int(middle - .5)]
    else:
        return (lst[int(middle)], lst[int(middle-1)])


def middle(num: int) -> float:
    """
    Gives us the middle x pixel of out input list.
    output looks like:
    float

    :param lst: the num of the plot which we want to find the middle pixel for.
    :return: a float of the singular pixel value of the middle for the input 
    plot. If the input list is of an odd length it is the average of the two
    middle pixels. 
    """
    middle_pixel = findMiddle(show_plot(num))
    if type(middle_pixel) is tuple:
        middle_pixel = (middle_pixel[0]+middle_pixel[1])/2
    return middle_pixel


""" 
This step has to happen here before we change our input list changing our
middle pixel
"""
middle_list = [0] * 7
for i in range(len(middle_list)):
    middle_list[i] = middle(i+1)

"""
This section is were we manually remove peaks when our show_plot function was
too sensitive and add extra peaks (on top of the middle peak) when there wasn't
a left/right peak detected. This means all our peaks will be in groups of three
allowing us to loop through later. We will only analyse the left side of our 
rings because a) time and b) the data was better.
"""
trim_lst = []

"""
trim_list is populated from 7 to 1 because we want the list to be filled from
no magnetic field to our max strength B-field.
"""
# 7
for i in range(0, len(HPFP_pixels)):
    peak_pos_7.insert(i*3, peak_pos_7[i*3])
    peak_pos_7.insert(i*3, peak_pos_7[i*3])
peak_pos_7 = peak_pos_7[:18]  # ignore the right hand side of middle
trim_lst = trim_lst + [peak_pos_7]


# 6
del peak_pos_6[0]
peak_pos_6.insert(0, peak_pos_6[0])
peak_pos_6.insert(0, peak_pos_6[0])
del peak_pos_6[3:7]
peak_pos_6.insert(3, peak_pos_6[3])
peak_pos_6.insert(3, peak_pos_6[3])
del peak_pos_6[6:8]
peak_pos_6.insert(6, peak_pos_6[6])
del peak_pos_6[9:13]
peak_pos_6.insert(9, peak_pos_6[9])
peak_pos_6.insert(9, peak_pos_6[9])
del peak_pos_6[12:15]
peak_pos_6.insert(12, peak_pos_6[12])
peak_pos_6.insert(12, peak_pos_6[12])
del peak_pos_6[15:17]
peak_pos_6.insert(15, peak_pos_6[15])
peak_pos_6 = peak_pos_6[:18]
trim_lst = trim_lst + [peak_pos_6]

# 5
del peak_pos_5[0]
peak_pos_5.insert(0, peak_pos_5[0])
peak_pos_5.insert(0, peak_pos_5[0])
del peak_pos_5[3:5]
peak_pos_5.insert(3, peak_pos_5[3])
peak_pos_5.insert(3, peak_pos_5[3])
del peak_pos_5[6]
peak_pos_5.insert(6, peak_pos_5[6])
del peak_pos_5[9:11]
del peak_pos_5[12:15]
peak_pos_5.insert(12, peak_pos_5[12])
peak_pos_5.insert(12, peak_pos_5[12])
del peak_pos_5[15]
peak_pos_5.insert(15, peak_pos_5[15])
peak_pos_5 = peak_pos_5[:18]
trim_lst = trim_lst + [peak_pos_5]

# 4
del peak_pos_4[0]
peak_pos_4.insert(0, peak_pos_4[0])
peak_pos_4.insert(0, peak_pos_4[0])
del peak_pos_4[3]
peak_pos_4.insert(4, peak_pos_4[4])
del peak_pos_4[6]
peak_pos_4.insert(6, peak_pos_4[6])
peak_pos_4.insert(6, peak_pos_4[6])
del peak_pos_4[9:11]
del peak_pos_4[12:14]
peak_pos_4.insert(12, peak_pos_4[12])
del peak_pos_4[15:17]
peak_pos_4.insert(15, peak_pos_4[15])
peak_pos_4 = peak_pos_4[:18]
trim_lst = trim_lst + [peak_pos_4]

# 3
del peak_pos_3[0:2]
peak_pos_3.insert(1, peak_pos_3[1])
del peak_pos_3[3]
peak_pos_3.insert(4, peak_pos_3[4])
del peak_pos_3[6]
peak_pos_3.insert(8, peak_pos_3[8])
del peak_pos_3[9]
del peak_pos_3[12]
del peak_pos_3[15:17]
peak_pos_3 = peak_pos_3[:18]
trim_lst = trim_lst + [peak_pos_3]

# 2
del peak_pos_2[0]
peak_pos_2.insert(1, peak_pos_2[1])
del peak_pos_2[9]
del peak_pos_2[12:14]
del peak_pos_2[15]
del peak_pos_2[17]
peak_pos_2 = peak_pos_2[:18]
trim_lst = trim_lst + [peak_pos_2]

# 1
del peak_pos_1[6]
del peak_pos_1[15]
peak_pos_1 = peak_pos_1[:21]  # plot 1 had an extra set of 3 peaks
trim_lst = trim_lst + [peak_pos_1]

"""
This section looks at Zeeman splitting, more specifically how the wavelength is
effected by the change in B-field.
"""


def av_wavel_shift(trim_lst: list, num: int):
    """
    Gives us the average wavelength shift of each plot left and right in metres.
    output looks like:
    tuple(av_shift_L, av_shift_R)

    :param trim_lst: the list within trim_list which contains the specific peak
    plot locations (in pixels) for that plot.
    :param num: the num of the plot we're looking at.
    :return: a tuple of the av wavelength shift left and right for this specific
    plot in metres. 
    """
    # turns our pixel data into the number of pixels from the centre
    trim_lst = list(map(lambda x: abs(x - middle_list[num-1]), trim_lst))
    # turns our pixels into metres
    trim_lst = list(map(lambda x: x * conversion_r, trim_lst))

    wavel_shift_L_temp = []
    wavel_shift_R_temp = []
    av_wavel_shift_L_temp = []
    av_wavel_shift_R_temp = []

    for i in range(0, len(trim_lst), 3):
        # (+ve) => increase in wavelength => decrease in energy
        wavel_shift_L_temp = wavel_shift_L_temp + [trim_lst[i]-trim_lst[i+1]]
        # (-ve) => decrease in wavelength => increase in energy
        wavel_shift_R_temp = wavel_shift_R_temp + [trim_lst[i+2]-trim_lst[i+1]]

    av_wavel_shift_L_temp = sum(wavel_shift_L_temp)/len(wavel_shift_L_temp)
    av_wavel_shift_R_temp = sum(wavel_shift_R_temp)/len(wavel_shift_R_temp)

    return av_wavel_shift_L_temp, av_wavel_shift_R_temp


av_wavel_shift_L = []
av_wavel_shift_R = []


"""
This gets all the wavelength shifts (L and R) for all the plots.
"""
for i in range(len(HPFP_pixels)):
    av_wavel_shift_L = av_wavel_shift_L + [av_wavel_shift(trim_lst[i], i+1)[0]]
    av_wavel_shift_R = av_wavel_shift_R + [av_wavel_shift(trim_lst[i], i+1)[1]]

# from lab book
x_current = [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2]

"""
Initialising graph plot 2
"""
fig2, ax2 = plt.subplots()
ax2.set_title("Zeeman Splitting")
# B-field remains proportional to current for Helmholtz Coils
ax2.set_xlabel("Relative Strength of B-Field")
ax2.set_ylabel(r"Change in $\lambda$ $(m)$")

# Wavelength Shift vs B-Field Plot
ax2.plot(x_current, av_wavel_shift_L, label=r"$\pi = -\frac{1}{2}$" "\n"
         r"$E_\downarrow = -\frac{1}{2} m_\ell \mu_B B$")
ax2.plot(x_current, av_wavel_shift_R, label=r"$\pi = +\frac{1}{2}$" "\n"
         r"$E_\uparrow = +\frac{1}{2} m_\ell \mu_B B$")

"""
Initialising graph plot 2 fits (L and R)
"""
linfit2_L = linregress(x_current, av_wavel_shift_L)
linfit2_R = linregress(x_current, av_wavel_shift_R)

popt2_L, pcov2_L = curve_fit(linear_fit, x_current, av_wavel_shift_L)
popt2_R, pcov2_R = curve_fit(linear_fit, x_current, av_wavel_shift_R)

# print(linfit2_L)
# print(linfit2_R)

popt2_L = [float(x) for x in popt2_L]
popt2_R = [float(x) for x in popt2_R]

# Fit plots superimposed on the wavelength b-field plot
ax2.plot(x_current, linear_fit(x_current, popt2_L[0], popt2_L[1]),
         label="Fit", color="red")
ax2.plot(x_current, linear_fit(x_current, popt2_R[0], popt2_R[1]), color="red")

ax2.legend(loc='upper left', prop={'size': 10})

plt.show()
