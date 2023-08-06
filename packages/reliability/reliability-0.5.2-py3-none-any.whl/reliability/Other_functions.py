'''
Other Functions

This is a collection of several other functions that did not otherwise fit within their own module.
Included functions are:
similar_distributions - finds the parameters of distributions that are similar to the input distribution and plots the results.
convert_dataframe_to_grouped_lists - groups values in a 2-column dataframe based on the values in the left column and returns those groups in a list of lists
make_right_censored_data - a simple tool to right censor a complete dataset based on a threshold. Primarily used for testing Fitters when some right censored data is needed.
histogram - generates a histogram with optimal bin width and has an option to shade some bins white above a chosen threshold.
crosshairs - adds x,y crosshairs to plots based on mouse position
'''

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from mplcursors import cursor
import warnings
from reliability.Distributions import Weibull_Distribution, Normal_Distribution, Lognormal_Distribution, Exponential_Distribution, Gamma_Distribution, Beta_Distribution
from reliability.Fitters import Fit_Everything


class similar_distributions:
    '''
    similar_distributions

    This is a tool to find similar distributions when given an input distribution.
    It is useful to see how similar one distribution is to another. For example, you may look at a Weibull distribution and think it looks like a Normal distribution.
    Using this tool you can determine the parameters of the Normal distribution that most closely matches your Weibull distribution.

    Inputs:
    distribution - a distribution object created using the reliability.Distributions module
    include_location_shifted - True/False. Default is True. When set to True it will include Weibull_3P, Lognormal_3P, Gamma_3P, Expon_2P
    show_plot - True/False. Default is True
    print_results - True/False. Default is True
    number_of_distributions_to_show - the number of similar distributions to show. Default is 3. If the number specified exceeds the number available (typically 8), then the number specified will automatically be reduced.

    Outputs:
    results - an array of distributions objects ranked in order of best fit.
    most_similar_distribution - a distribution object. This is the first item from results.

    Example usage:
    from reliability.Distributions import Weibull_Distribution
    from reliability.Other_functions import similar_distributions
    dist = Weibull_Distribution(alpha=50,beta=3.3)
    similar_distributions(distribution=dist)
    '''

    def __init__(self, distribution, include_location_shifted=True, show_plot=True, print_results=True, number_of_distributions_to_show=3):
        # ensure the input is a distribution object
        if type(distribution) not in [Weibull_Distribution, Normal_Distribution, Lognormal_Distribution, Exponential_Distribution, Gamma_Distribution, Beta_Distribution]:
            raise ValueError('distribution must be a probability distribution object from the reliability.Distributions module. First define the distribution using Reliability.Distributions.___')

        # sample the CDF from 0.001 to 0.999. These samples will be used to fit all other distributions.
        RVS = distribution.quantile(np.linspace(0.001, 0.999, 698))  # 698 samples is the ideal number for the points to align. Evidenced using plot_points.

        # filter out negative values
        RVS_filtered = []
        negative_values_error = False
        for item in RVS:
            if item > 0:
                RVS_filtered.append(item)
            else:
                negative_values_error = True
        if negative_values_error is True:
            print('WARNING: The input distribution has non-negligible area for x<0. Samples from this region have been discarded to enable other distributions to be fitted.')

        fitted_results = Fit_Everything(failures=RVS_filtered, print_results=False, show_probability_plot=False, show_histogram_plot=False, show_PP_plot=False)  # fit all distributions to the filtered samples
        ranked_distributions = list(fitted_results.results.index.values)
        ranked_distributions.remove(distribution.name2)  # removes the fitted version of the original distribution

        ranked_distributions_objects = []
        ranked_distributions_labels = []
        sigfig = 2
        for dist_name in ranked_distributions:
            if dist_name == 'Weibull_2P':
                ranked_distributions_objects.append(Weibull_Distribution(alpha=fitted_results.Weibull_2P_alpha, beta=fitted_results.Weibull_2P_beta))
                ranked_distributions_labels.append(str('Weibull_2P (α=' + str(round(fitted_results.Weibull_2P_alpha, sigfig)) + ',β=' + str(round(fitted_results.Weibull_2P_beta, sigfig)) + ')'))
            elif dist_name == 'Gamma_2P':
                ranked_distributions_objects.append(Gamma_Distribution(alpha=fitted_results.Gamma_2P_alpha, beta=fitted_results.Gamma_2P_beta))
                ranked_distributions_labels.append(str('Gamma_2P (α=' + str(round(fitted_results.Gamma_2P_alpha, sigfig)) + ',β=' + str(round(fitted_results.Gamma_2P_beta, sigfig)) + ')'))
            elif dist_name == 'Normal_2P':
                ranked_distributions_objects.append(Normal_Distribution(mu=fitted_results.Normal_2P_mu, sigma=fitted_results.Normal_2P_sigma))
                ranked_distributions_labels.append(str('Normal_2P (μ=' + str(round(fitted_results.Normal_2P_mu, sigfig)) + ',σ=' + str(round(fitted_results.Normal_2P_sigma, sigfig)) + ')'))
            elif dist_name == 'Lognormal_2P':
                ranked_distributions_objects.append(Lognormal_Distribution(mu=fitted_results.Lognormal_2P_mu, sigma=fitted_results.Lognormal_2P_sigma))
                ranked_distributions_labels.append(str('Lognormal_2P (μ=' + str(round(fitted_results.Lognormal_2P_mu, sigfig)) + ',σ=' + str(round(fitted_results.Lognormal_2P_sigma, sigfig)) + ')'))
            elif dist_name == 'Exponential_1P':
                ranked_distributions_objects.append(Exponential_Distribution(Lambda=fitted_results.Expon_1P_lambda))
                ranked_distributions_labels.append(str('Exponential_1P (lambda=' + str(round(fitted_results.Expon_1P_lambda, sigfig)) + ')'))
            elif dist_name == 'Beta_2P':
                ranked_distributions_objects.append(Beta_Distribution(alpha=fitted_results.Beta_2P_alpha, beta=fitted_results.Beta_2P_beta))
                ranked_distributions_labels.append(str('Beta_2P (α=' + str(round(fitted_results.Beta_2P_alpha, sigfig)) + ',β=' + str(round(fitted_results.Beta_2P_beta, sigfig)) + ')'))

            if include_location_shifted is True:
                if dist_name == 'Weibull_3P':
                    ranked_distributions_objects.append(Weibull_Distribution(alpha=fitted_results.Weibull_3P_alpha, beta=fitted_results.Weibull_3P_beta, gamma=fitted_results.Weibull_3P_gamma))
                    ranked_distributions_labels.append(str('Weibull_3P (α=' + str(round(fitted_results.Weibull_3P_alpha, sigfig)) + ',β=' + str(round(fitted_results.Weibull_3P_beta, sigfig)) + ',γ=' + str(round(fitted_results.Weibull_3P_gamma, sigfig)) + ')'))
                elif dist_name == 'Gamma_3P':
                    ranked_distributions_objects.append(Gamma_Distribution(alpha=fitted_results.Gamma_3P_alpha, beta=fitted_results.Gamma_3P_beta, gamma=fitted_results.Gamma_3P_gamma))
                    ranked_distributions_labels.append(str('Gamma_3P (α=' + str(round(fitted_results.Gamma_3P_alpha, sigfig)) + ',β=' + str(round(fitted_results.Gamma_3P_beta, sigfig)) + ',γ=' + str(round(fitted_results.Gamma_3P_gamma, sigfig)) + ')'))
                elif dist_name == 'Lognormal_3P':
                    ranked_distributions_objects.append(Lognormal_Distribution(mu=fitted_results.Lognormal_3P_mu, sigma=fitted_results.Lognormal_3P_sigma, gamma=fitted_results.Lognormal_3P_gamma))
                    ranked_distributions_labels.append(str('Lognormal_3P (μ=' + str(round(fitted_results.Lognormal_3P_mu, sigfig)) + ',σ=' + str(round(fitted_results.Lognormal_3P_sigma, sigfig)) + ',γ=' + str(round(fitted_results.Lognormal_3P_gamma, sigfig)) + ')'))
                elif dist_name == 'Exponential_2P':
                    ranked_distributions_objects.append(Exponential_Distribution(Lambda=fitted_results.Expon_1P_lambda, gamma=fitted_results.Expon_2P_gamma))
                    ranked_distributions_labels.append(str('Exponential_1P (lambda=' + str(round(fitted_results.Expon_1P_lambda, sigfig)) + ',γ=' + str(round(fitted_results.Expon_2P_gamma, sigfig)) + ')'))

        number_of_distributions_fitted = len(ranked_distributions_objects)
        self.results = ranked_distributions_objects
        self.most_similar_distribution = ranked_distributions_objects[0]
        if print_results is True:
            print('The input distribution was:')
            print(distribution.param_title_long)
            if number_of_distributions_fitted < number_of_distributions_to_show:
                number_of_distributions_to_show = number_of_distributions_fitted
            print('\nThe top', number_of_distributions_to_show, 'most similar distributions are:')
            counter = 0
            while counter < number_of_distributions_to_show and counter < number_of_distributions_fitted:
                dist = ranked_distributions_objects[counter]
                print(dist.param_title_long)
                counter += 1

        if show_plot is True:
            plt.figure(figsize=(14, 6))
            plt.suptitle(str('Plot of similar distributions to ' + distribution.param_title_long))
            counter = 0
            xlower = distribution.quantile(0.001)
            xupper = distribution.quantile(0.999)
            x_delta = xupper - xlower
            plt.subplot(121)
            distribution.PDF(label=str('Input distribution [' + distribution.name2 + ']'), linestyle='--')
            while counter < number_of_distributions_to_show and counter < number_of_distributions_fitted:
                ranked_distributions_objects[counter].PDF(label=ranked_distributions_labels[counter])
                counter += 1
            plt.xlim([xlower - x_delta * 0.1, xupper + x_delta * 0.1])
            plt.legend()
            plt.title('PDF')
            counter = 0
            plt.subplot(122)
            distribution.CDF(label=str('Input distribution [' + distribution.name2 + ']'), linestyle='--')
            while counter < number_of_distributions_to_show and counter < number_of_distributions_fitted:
                ranked_distributions_objects[counter].CDF(label=ranked_distributions_labels[counter])
                counter += 1
            plt.xlim([xlower - x_delta * 0.1, xupper + x_delta * 0.1])
            plt.legend()
            plt.title('CDF')
            plt.subplots_adjust(left=0.08, right=0.95)
            plt.show()


def histogram(data, white_above=None, bins=None, density=True, cumulative=False, **kwargs):
    '''
    histogram

    plots a histogram using the data specified
    This is similar to plt.hist except that it calculates the optimal number of bins to use based on the Freedman–Diaconis rule ==> https://en.wikipedia.org/wiki/Freedman%E2%80%93Diaconis_rule
    If you would like to specify the number of bins rather than having the optimal number calculated, then the bins argument allows this.
    This function also shades the bins white above a specified value (white_above). This is useful for representing complete data as right censored data in a histogram.

    Inputs:
    data - the data to plot. Array or list.
    white_above - bins above this value will be shaded white
    bins - the number of bins to use. Must be int. Leave empty to have the optimal number calculated automatically
    density - True/False. Default is True. Always use True if plotting with a probability distribution.
    cumulative - True/False. Default is False. Use False for PDF and True for CDF.
    kwargs - plotting kwargs for the histogram (color, alpha, etc.)
    '''

    if type(data) not in [np.ndarray, list]:
        raise ValueError('data must be an array or list')

    if white_above is not None:
        if type(white_above) not in [int, float, np.float64]:
            raise ValueError('white_above must be int or float')
        if white_above < min(data):
            raise ValueError('white_above must be greater than min(data)')

    if bins is not None:
        if type(bins) is not int:
            raise ValueError('bins is the number of bins to use. It must be type int. Leave empty to calculate the optimal number')
    else:
        iqr = np.subtract(*np.percentile(data, [75, 25]))  # interquartile range
        bin_width = 2 * iqr * len(data) ** -(1 / 3)  # Freedman–Diaconis rule ==> https://en.wikipedia.org/wiki/Freedman%E2%80%93Diaconis_rule
        bins = int(np.ceil((max(data) - min(data)) / bin_width))

    if 'color' in kwargs:
        color = kwargs.pop('color')
    elif 'c' in kwargs:
        color = kwargs.pop('c')
    else:
        color = 'lightgrey'

    if 'edgecolor' in kwargs:
        edgecolor = kwargs.pop('egdecolor')
    else:
        edgecolor = 'k'

    if 'linewidth' in kwargs:
        linewidth = kwargs.pop('linewidth')
    elif 'lw' in kwargs:
        linewidth = kwargs.pop('lw')
    else:
        linewidth = 0.5

    _, bins_out, patches = plt.hist(data, density=density, cumulative=cumulative, color=color, bins=bins, edgecolor=edgecolor, linewidth=linewidth, **kwargs)  # plots the histogram of the data

    if white_above is not None:
        for i in range(np.argmin(abs(np.array(bins_out) - white_above)), len(patches)):  # this is to shade part of the histogram as white
            patches[i].set_facecolor('white')


def convert_dataframe_to_grouped_lists(input_dataframe):
    '''
    Accepts a dataframe containing 2 columns
    This function assumes the identifying column is the left column
    returns:
    lists , names - lists is a list of the grouped lists
                  - names is the identifying values used to group the lists from the first column

    Example usage:
    #create sample data
    import pandas as pd
    data = {'outcome': ['Failed', 'Censored', 'Failed', 'Failed', 'Censored'],
        'cycles': [1253,1500,1342,1489,1500]}
    df = pd.DataFrame(data, columns = ['outcome', 'cycles'])
    #usage of the function
    lists,names = convert_dataframe_to_grouped_lists(df)
    print(names[1]) >>> Failed
    print(lists[1]) >>> [1253, 1342, 1489]
    '''
    df = input_dataframe
    column_names = df.columns.values
    if len(column_names) > 2:
        raise ValueError('Dataframe contains more than 2 columns. There should only be 2 columns with the first column containing the labels to group by and the second containing the values to be returned in groups.')
    grouped_lists = []
    group_list_names = []
    for key, items in df.groupby(column_names[0]):
        values = list(items.iloc[:, 1].values)
        grouped_lists.append(values)
        group_list_names.append(key)
    return grouped_lists, group_list_names


class make_right_censored_data:
    '''
    make_right_censored_data
    Right censors data based on specified threshold
    Inputs:
    data - list or array of data
    threshold - point to right censor (right censoring is done if value is > threshold)

    Outputs:
    failures - array of failures (data <= threshold)
    right_censored - array of right_censored values (data > threshold). These will be set to the value of the threshold.
    '''

    def __init__(self, data, threshold):
        if type(data) is list:
            data = np.array(data)
        self.failures = data[data <= threshold]
        self.right_censored = np.ones_like(data[data > threshold]) * threshold


class crosshairs:
    '''
    Adds interactive crosshairs to matplotlib plots
    Ensure this is used after you plot everything as anything plotted after crosshairs() is called will not be recognised by the snap-to feature.

    :param xlabel: the xlabel for annotations. Default is 'x'
    :param ylabel: the ylabel for annotations. Default is 'y'
    :param decimals: the number of decimals for rounding. Default is 2.
    :param kwargs: plotting kwargs to change the style of the crosshairs (eg. color, linestyle, etc.)
    '''

    def __init__(self, xlabel=None, ylabel=None, decimals=2, **kwargs):
        crosshairs.__generate_crosshairs(self, xlabel=xlabel, ylabel=ylabel, decimals=decimals, **kwargs)

    def __add_lines_and_text_to_crosshairs(sel, decimals, **kwargs):
        # set the default properties of the lines and text if they were not provided as kwargs
        if 'c' in kwargs:
            color = kwargs.pop('c')
        elif 'color' in kwargs:
            color = kwargs.pop('color')
        else:
            color = 'k'
        if 'lw' in kwargs:
            linewidth = kwargs.pop('lw')
        elif 'linewidth' in kwargs:
            linewidth = kwargs.pop('linewidth')
        else:
            linewidth = 0.5
        if 'ls' in kwargs:
            linestyle = kwargs.pop('ls')
        elif 'linestyle' in kwargs:
            linestyle = kwargs.pop('linestyle')
        else:
            linestyle = '--'
        if 'size' in kwargs:
            fontsize = kwargs.pop('size')
        elif 'fontsize' in kwargs:
            fontsize = kwargs.pop('fontsize')
        else:
            fontsize = 10
        if 'fontweight' in kwargs:
            fontweight = kwargs.pop('fontweight')
        elif 'weight' in kwargs:
            fontweight = kwargs.pop('weight')
        else:
            fontweight = 0
        if 'fontstyle' in kwargs:
            fontstyle = kwargs.pop('fontstyle')
        elif 'style' in kwargs:
            fontstyle = kwargs.pop('style')
        else:
            fontstyle = 'normal'

        sel.annotation.set(visible=False)  # Hide the normal annotation during hover
        try:
            ax = sel.artist.axes
        except:
            ax = sel.annotation.axes  # this exception occurs for bar charts
        x, y = sel.target
        lines = [Line2D([x, x], [0, 1], transform=ax.get_xaxis_transform(), c=color, lw=linewidth, ls=linestyle, **kwargs),
                 Line2D([0, 1], [y, y], transform=ax.get_yaxis_transform(), c=color, lw=linewidth, ls=linestyle, **kwargs)]
        texts = [ax.text(s=round(y, decimals), x=0, y=y, transform=ax.get_yaxis_transform(), color=color, fontsize=fontsize, fontweight=fontweight, fontstyle=fontstyle, **kwargs),
                 ax.text(s=round(x, decimals), x=x, y=0, transform=ax.get_xaxis_transform(), color=color, fontsize=fontsize, fontweight=fontweight, fontstyle=fontstyle, **kwargs)]
        for i in [0, 1]:
            line = lines[i]
            text = texts[i]
            ax.add_line(line)
            # the lines and text need to be registered with sel so that they are updated during mouse motion events
            sel.extras.append(line)
            sel.extras.append(text)

    def __format_annotation(sel, decimals, label):  # this is some simple formatting for the annotations (applied on click)
        [x, y] = sel.annotation.xy
        text = str(label[0] + ' = ' + str(round(x, decimals)) + '\n' + label[1] + ' = ' + str(round(y, decimals)))
        sel.annotation.set_text(text)
        sel.annotation.get_bbox_patch().set(fc="white")

    def __hide_crosshairs(event):
        ax = event.inaxes  # this gets the axes where the event occurred.
        if len(ax.texts) >= 2:  # the lines can't be deleted if they haven't been drawn.
            if ax.texts[-1].get_position()[1] == 0 and ax.texts[-2].get_position()[0] == 0:  # this identifies the texts (crosshair text coords) based on their combination of unique properties
                ax.lines[-1].set_visible(False)
                ax.lines[-2].set_visible(False)
                ax.texts[-1].set_visible(False)
                ax.texts[-2].set_visible(False)
        event.canvas.draw()

    def __generate_crosshairs(self, xlabel=None, ylabel=None, decimals=2, **kwargs):  # this is the main program
        warnings.simplefilter('ignore')  # required when using fill_between due to warning in mplcursors: "UserWarning: Pick support for PolyCollection is missing."
        ch = cursor(hover=True)
        add_lines_and_text_with_kwargs = lambda _: crosshairs.__add_lines_and_text_to_crosshairs(_, decimals, **kwargs)  # adds the line's kwargs before connecting it to cursor
        ch.connect("add", add_lines_and_text_with_kwargs)
        plt.gcf().canvas.mpl_connect('axes_leave_event', crosshairs.__hide_crosshairs)  # hide the crosshairs and text when the mouse leaves the axes

        # does the annotation part
        if xlabel is None:
            xlabel = 'x'
        if ylabel is None:
            ylabel = 'y'
        warnings.simplefilter('ignore')  # required when using fill_between due to warning in mplcursors: "UserWarning: Pick support for PolyCollection is missing."
        annot = cursor(multiple=True, bindings={"toggle_visible": "h"})
        format_annotation_labeled = lambda _: crosshairs.__format_annotation(_, decimals, [xlabel, ylabel])  # adds the labels to the 'format_annotation' function before connecting it to cursor
        annot.connect("add", format_annotation_labeled)
