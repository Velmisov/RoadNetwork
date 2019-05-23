import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse
import glob
from cycler import cycler
import brewer2mpl


bmap = brewer2mpl.get_map('Set1', 'qualitative', 3)
colors = bmap.mpl_colors

plt.rc('lines', linewidth=2)
plt.rc('font', family='sans-serif')
plt.rc('axes', prop_cycle=(cycler('color', colors)))


def fig():
    fig = 1
    while True:
        yield fig
        fig += 1


fig_gen = fig()


def moving_average(interval, window_size):
    if window_size == 1:
        return interval
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')


def plot_figure(figsize=(12, 9), x_label='', y_label='', title=''):
    plt.figure(next(fig_gen), figsize=figsize)
    plt.rcParams.update({'font.size': 20})
    ax = plt.subplot()

    plt.grid(axis='y')

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)


def to_intervals(arr, interval=10):
    arr_interval = []
    result = []
    for i in range(len(arr)):
        arr_interval.append(arr[i])
        if len(arr_interval) == interval:
            result.append(np.mean(arr_interval))
            arr_interval = []
    result.append(np.mean(arr_interval))
    return result


if __name__ == '__main__':

    prs = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    prs.add_argument("-f", dest="file", nargs='+', required=True, help="The csv file to plot.\n")
    prs.add_argument("-label", dest="label", nargs='+', required=False, help="Figure labels.\n")
    prs.add_argument("-out", dest="out", required=False, default='', help="The .pdf filename in which the figure will be saved.\n")
    prs.add_argument("-w", dest="window", required=False, default=5, type=int, help="The moving average window.\n")
    args = prs.parse_args()
    if args.label:
        labels = args.label
    else:
        labels = ['' for _ in range(len(args.file))]

    plot_figure(x_label='Time Step (s)', y_label='Total Waiting Time of Vehicles (s)')

    for filename in args.file:
        main_df = pd.DataFrame()
        for file in glob.glob(filename+'*'):
            df = pd.read_csv(file)
            if main_df.empty:
                main_df = df
            else:
                main_df = pd.concat((main_df, df))

        steps = main_df.groupby('step_time').total_stopped.mean().keys()
        result_steps = to_intervals(steps)

        mean = moving_average(main_df.groupby('step_time').mean()['total_wait_time'], window_size=args.window)
        result_mean = to_intervals(mean)

        plt.plot(result_steps, result_mean, label=labels[0])
        labels.pop(0)

    if args.label is not None:
        plt.legend()

    if args.out != '':
        plt.savefig(args.out+'.pdf', bbox_inches="tight")
    plt.show()
