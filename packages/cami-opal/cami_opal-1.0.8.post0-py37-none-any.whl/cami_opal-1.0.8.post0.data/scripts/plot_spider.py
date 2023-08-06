#!python

import os
import pandas as pd
import numpy as np
from collections import OrderedDict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.utils import spider_plot_functions as spl
from src.utils import constants as c
from src import plots
from collections import defaultdict


def spider_plot(metrics, labels, rank_to_metric_to_toolvalues, output_dir, file_name, colors, grid_points=None, fill=False, absolute=False):
    N = len(labels)
    if N < 3:
        return []

    theta = spl.radar_factory(N, frame='polygon')
    fig, axes = plt.subplots(figsize=(9, 9), nrows=2, ncols=3, subplot_kw=dict(projection='radar'))
    # fig.subplots_adjust(wspace=0.25, hspace=0.35, top=0.87, bottom=0.45)
    fig.subplots_adjust(wspace=1.0, hspace=0, top=0.87, bottom=0.45)

    for ax, rank in zip(axes.flat, c.PHYLUM_SPECIES):
        if grid_points:
            ax.set_rgrids(grid_points, fontsize='xx-small')
        else:
            ax.set_rgrids([0.2, 0.4, 0.6, 0.8], ('', '', '', ''))  # get rid of the labels of the grid points
        ax.set_title(rank, weight='normal', size=9, position=(0.5, 1.1),
                     horizontalalignment='center', verticalalignment='center')

        # if absolute:
        #     metric_suffix = 'absolute'
        # else:
        #     metric_suffix = ''
        # select only metrics in metrics list
        metrics_subdict = OrderedDict((metric, rank_to_metric_to_toolvalues[rank][metric]) for metric in metrics)
        it = 1
        metric_to_toolindex = []
        for d, color in zip(metrics_subdict.values(), colors):

            # store index of tools without a value for the current metric
            metric_to_toolindex.append([i for i, x in enumerate(d) if x is None or np.isnan(x)])
            d = [0 if x is None or np.isnan(x) else x for x in d]

            ax.plot(theta, d, '--', color=color, linewidth=2, dashes=(it, 1))
            # if fill:
            ax.fill(theta, d, facecolor=color, alpha=0.25)
            it += 1
        ax.set_varlabels(labels)

        ax.set_rmax(1)

        # color red label of tools without a value for at least one metric
        xticklabels = ax.get_xticklabels()
        # for metric in metric_to_toolindex:
        #     for toolindex in metric:
        #         xticklabels[toolindex].set_color([1, 0, 0])

        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]
        for label, angle in zip(ax.get_xticklabels(), angles):
            if angle in (0, np.pi):
                label.set_horizontalalignment('center')
            elif 0 < angle < np.pi:
                label.set_horizontalalignment('right')
            else:
                label.set_horizontalalignment('left')

        # move tick labels closer to plot and set font size
        for xticklabel in xticklabels:
            xticklabel.set_position((0,.21))
            # xticklabel.set_position((1,0.1))

            # xticklabel.set_fontsize('small')
            xticklabel.set_fontsize('7')

    if absolute:
        metrics = [metric[:-8] for metric in metrics]

    ax = axes[0, 0]
    # metrics_labels = [c.RECALL, c.PRECISION, c.L1NORM, c.UNIFRAC]
    metrics_labels = [c.RECALL, 'Purity (1% filtered)', c.L1NORM, c.UNIFRAC]
    # ax.legend(metrics, loc=(1.9 - 0.353 * len(metrics), 1.25), labelspacing=0.1, fontsize=9, ncol=len(metrics), frameon=False)
    ax.legend(metrics_labels, loc=(1.58 - 0.353 * len(metrics_labels), 1.25), labelspacing=0.1, fontsize='9', ncol=len(metrics_labels), frameon=False)
    fig.savefig(os.path.join(output_dir, file_name + '.pdf'), dpi=100, format='pdf', bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, file_name + '.png'), dpi=200, format='png', bbox_inches='tight')
    plt.close(fig)

    return [file_name]


import seaborn as sns
def get_colors():
    x = sns.color_palette('colorblind')
    return [x[0], x[1], x[2], x[4], x[7]]


# add this line to function plot_all in src/plots.py
# pd_mean.to_csv(os.path.join(output_dir, 'pd_mean_spider.tsv'), sep='\t')

metrics_for_plot = [c.RECALL+'absolute', c.PRECISION+'absolute', c.BRAY_CURTIS+'absolute', c.UNIFRAC]
# colors = [plt.cm.tab10(2), plt.cm.tab10(0), plt.cm.tab10(3), 'k', 'm', 'y']
colors = get_colors()

labels = 'MetaPhlAn 2.2.0,MetaPhlAn 2.9.21,mOTUs 1.1,mOTUs 2.5.1,Bracken 2.5,MetaPalette 1.0.0,MetaPhyler 1.25,FOCUS 0.31,TIPP 2.0.0,CAMIARKQuikr 1.0.0'.split(',')
output_dir = '/home/fmeyer/projects/tutorial/revision/opal_mouse_gut_filter_no_normalization_xx/'
pd_mean = pd.read_csv(output_dir + '/pd_mean_spider.tsv', sep='\t', index_col=['rank', 'tool'])
pd_mean.drop(index=c.GS, level=1, inplace=True)
tool_to_rank_to_metric_to_value = plots.spider_plot_preprocess_metrics(pd_mean, labels)


rank_to_metric_to_toolvalues = defaultdict(lambda : defaultdict(list))
for label in labels:
    for rank in c.PHYLUM_SPECIES:
        for metric in metrics_for_plot: #+ [c.RECALL+'absolute', c.PRECISION+'absolute']:
            if metric in tool_to_rank_to_metric_to_value[label][rank]:
                rank_to_metric_to_toolvalues[rank][metric].append(tool_to_rank_to_metric_to_value[label][rank][metric])
        rank_to_metric_to_toolvalues[rank][c.UNIFRAC].append(tool_to_rank_to_metric_to_value[label]['rank independent'][c.UNIFRAC])


spider_plot(metrics_for_plot,
             labels,
             rank_to_metric_to_toolvalues,
             output_dir,
             'spider_plot',
             colors[:len(metrics_for_plot)],
            grid_points=[0.2, 0.4, 0.6, 0.8, 1.0],
            absolute=True)

