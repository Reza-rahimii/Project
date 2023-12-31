import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.font_manager import FontProperties
import numpy as np
import math
from src.makeMolecule import heavy_atoms


def gauss(x, x0, sigma):
    """
    This function returns a Gaussian distribution.
    """
    return (1/(sigma*math.sqrt(2 * math.pi))) * np.exp(-(x - x0)**2 / (2 * sigma**2))


def performance_plot(outputs, predictions, test, prop, folder="NewPredictions", fold=0, model="ANN"):
    if prop == "h" or prop == "Enthalpy":
        prop = "Enthalpy"
        metric = "kJ mol$^{-1}$"
    elif prop == "s" or prop == "Entropy":
        prop = "Entropy"
        metric = "J mol$^{-1}$ K$^{-1}$"
    elif prop == "cp" or prop == "Heat Capacity":
        prop = "Heat Capacity"
        metric = "J mol$^{-1}$ K$^{-1}$"
        outputs = outputs[:, 0]
        predictions = predictions[:, 0]
    elif prop == "sg" or prop == "SG" or prop == "Specific Gravity":
        prop = "Specific Gravity (60/60$\degree$F)"
        metric = "-"
        outputs = outputs / 1000
        predictions = predictions / 1000
    elif prop == "pvap" or prop == "pVap" or prop == "Vapor Pressure":
        prop = "Vapor Pressure"
        metric = "kPa"
        outputs = outputs / 1000
        predictions = predictions / 1000
    elif prop.lower() == "mu" or prop.lower() == "viscosity" or prop.lower() == "dynamic viscosity":
        prop = "Dynamic Viscosity"
        metric = "Pa$\cdot$s"
        outputs = outputs / 1000
        predictions = predictions / 1000
    elif prop.lower() == "kinematic viscosity":
        prop = "Kinematic Viscosity"
        metric = "m$^{2}$s^{-1}"
        outputs = outputs / 1000
        predictions = predictions / 1000
    elif prop.lower() == "surface tension" or prop.lower() == "st":
        prop = "Surface Tension"
        metric = "N m^{-1}"
        outputs = outputs / 1000
        predictions = predictions / 1000
    else:
        metric = "-"
    if "test" in test:
        name = "testResults"
    elif "validation" in test:
        name = "validationResults"
    else:
        name = str(test + "_plot")
    hfont = {'fontname': 'UGent Panno Text'}
    font = FontProperties(family='UGent Panno Text',
                          weight='normal',
                          style='normal', size=24)
    plt.rc('font', size=24)
    fig, ax = plt.subplots()
    fig.set_size_inches(15, 10)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(1.5)
    ax.tick_params(direction='in', top=True, right=True, color='black', width=2)
    # ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    ax.set_xlabel(str("Experimental " + prop + " [" + metric + "]"), **hfont)
    ax.set_ylabel(str("ANN predicted " + prop + " [" + metric + "]"), **hfont)
    for tick in ax.get_xticklabels():
        tick.set_fontname("UGent Panno Text")
    for tick in ax.get_yticklabels():
        tick.set_fontname("UGent Panno Text")
    plt.plot([min(outputs), max(outputs)], [min(outputs), max(outputs)], c='#D01C1F', linewidth=1.5, label='Parity')
    plt.scatter(outputs, predictions, s=80, c='#0F4C81', label='Data points', alpha=0.5)
    # plt.plot([min(outputs), max(outputs)], [min(outputs) + 10, max(outputs) + 10],
    #          c='#FFA44A', label='$\pm$ 10 J mol$^{-1}$ K$^{-1}$', linestyle='--')
    # plt.plot([min(outputs), max(outputs)], [min(outputs) - 10, max(outputs) - 10],
    #          c='#FFA44A', linestyle='--')
    plt.legend(loc='best', prop=font)
    if prop == "Specific Gravity (60/60$\degree$F)":
        plt.savefig(str(folder + "/" + name + "_" + model + "_sg_" + str(fold) + ".png"), bbox_inches='tight')
    elif prop == "Vapor Pressure @ 100 $\degree$F":
        plt.savefig(str(folder + "/" + name + "_" + model + "_pvap_" + str(fold) + ".png"), bbox_inches='tight')
    else:
        plt.savefig(str(folder + "/" + name + "_" + model + "_" + prop + "_" + str(fold) + ".png"), bbox_inches='tight')


#     UGent yellow: #FFD200
#     Pantone Classic Blue: #0F4C81
#     Pantone Chili Pepper: #9B1B30
#     Pantone Buff Orange: #FFBE79
#     Pantone Red 032 C: #EF3340
#     Pantone Blazing Orange: #FFA44A
#     Pantone Fiery Red: #D01C1F


def histogram_plots(histogram_values, num_bins=200, title=None, c='#0F4C81', alpha=1,
                    folder=None, metric=None, unit=None):
    plt.figure()
    hfont = {'fontname': 'UGent Panno Text'}
    font = FontProperties(family='UGent Panno Text',
                          weight='normal',
                          style='normal', size=24)
    plt.rc('font', size=24)
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 6)
    plt.hist(histogram_values, num_bins, facecolor=c, alpha=alpha)
    if metric is not None and unit is not None:
        ax.set_xlabel(str(metric + " [" + unit + "]"), **hfont)
        # plt.xlabel(str(metric + " [" + unit + "]"))
    ax.set_ylabel('Occurrence', **hfont)
    # plt.ylabel('Occurrence')
    for tick in ax.get_xticklabels():
        tick.set_fontname("UGent Panno Text")
    for tick in ax.get_yticklabels():
        tick.set_fontname("UGent Panno Text")
    if title is not None:
        ax.set_title(title, **hfont)
        # plt.title(title, prop=font)
        if folder is not None:
            plt.savefig(folder + "/" + title + ".png", bbox_inches='tight')
        else:
            plt.show()
    else:
        plt.show()


def gmm_plot(histogram_values, gmm_values, title=None, c_curve='#0f4c81', c_peak='#ea733d',
             folder=None, metric=None, unit=None):
    plt.figure()
    hfont = {'fontname': 'UGent Panno Text'}
    font = FontProperties(family='UGent Panno Text',
                          weight='normal',
                          style='normal', size=24)
    plt.rc('font', size=24)
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 6)
    for tick in ax.get_xticklabels():
        tick.set_fontname("UGent Panno Text")
    for tick in ax.get_yticklabels():
        tick.set_fontname("UGent Panno Text")
    ls = np.arange(min(histogram_values), max(histogram_values), 0.001)
    for mu, sigma in gmm_values:
        gd = gauss(ls, mu, sigma)
        plt.plot(ls, gd, c=c_curve)
        plt.plot(mu, 1/(sigma*math.sqrt(2*math.pi)), "x", c=c_peak)
        if metric is not None and unit is not None:
            ax.set_xlabel(str(metric + " [" + unit + "]"), **hfont)
            # plt.xlabel(str(metric + " [" + unit + "]"))
        ax.set_ylabel('Occurrence', **hfont)
        # plt.ylabel('Occurrence')
        if title is not None:
            ax.set_title(title, **hfont)
            # plt.title(title, prop=font)
            if folder is not None:
                plt.savefig(folder + "/" + title + ".png", bbox_inches='tight')
            else:
                plt.show()
        else:
            plt.show()


def output_plot(molecules, outputs, prop, name="output_plot", folder="newPredictions"):
    if prop == "h":
        y_label = "Ab Initio Enthalpy [kJ mol$^{-1}$]"
    elif prop == "s":
        y_label = "Ab Initio Entropy [J mol$^{-1}$ K$^{-1}$]"
    elif prop == "cp":
        y_label = "Ab Initio Heat Capacity (298.15 K) [J mol$^{-1}$ K$^{-1}$]"
        outputs = outputs[:, 0]
    else:
        y_label = "Experimental Value"
        if len(outputs.shape) > 1:
            outputs = outputs[:, 0]
    ha = []
    for mol in molecules:
        ha.append(heavy_atoms(mol))
    ha = np.asarray(ha).astype(np.float)
    hfont = {'fontname': 'UGent Panno Text'}
    font = FontProperties(family='UGent Panno Text',
                          weight='normal',
                          style='normal', size=24)
    plt.rc('font', size=24)
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 6)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(1.5)
    ax.tick_params(direction='in', top=True, right=True, color='black', width=2)
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    ax.set_ylabel(y_label, **hfont)
    ax.set_xlabel('Number of Heavy Atoms', **hfont)
    for tick in ax.get_xticklabels():
        tick.set_fontname("UGent Panno Text")
    for tick in ax.get_yticklabels():
        tick.set_fontname("UGent Panno Text")
    plt.scatter(ha, outputs, s=6, c='#0F4C81', alpha=0.1)
    location = str(folder + "/" + name + ".png")
    plt.savefig(location, format="png", bbox_inches='tight')
    print("A plot of the output distribution is stored in {}".format(location))
    # plt.show()


def store_histograms(histogram_dict, save_folder):
    for key in histogram_dict:
        v = histogram_dict[key]
        if len(key) == 2:
            metric = "Distance"
            unit = "Å"
        else:
            metric = "Angle"
            unit = "rad"
        histogram_plots(v, title=key, folder=str(save_folder + "/hist"), metric=metric, unit=unit)
    print("Stored all histogram plots in {}".format(str(save_folder + "/hist")))


def store_gaussians(histogram_dict, gmm_dictionary, save_folder):
    for key in histogram_dict:
        v = histogram_dict[key]
        t = gmm_dictionary[key]
        if len(key) == 2:
            metric = "Distance"
            unit = "Å"
        else:
            metric = "Angle"
            unit = "rad"
        gmm_plot(v, t, title=key, folder=str(save_folder + "/gmm"), metric=metric, unit=unit)
    print("Stored all gmm plots in {}".format(str(save_folder + "/gmm")))
