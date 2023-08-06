#!python

import os
import os.path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.utils import constants as c
from collections import OrderedDict
import seaborn as sns


def get_colors():
    x = sns.color_palette('colorblind')
    return [x[0], x[1], x[2], x[4], x[7]]


def go_workshop(pd_std_over_samples, pd_mean, output_dir):
    ranks = c.ALL_RANKS[0:-1]
    x = range(len(ranks))
    rank_to_index = dict(zip(ranks, list(range(len(ranks)))))

    # pd_mean = pd_mean.drop(c.GS, level='tool').drop(['strain', 'rank independent'], level='rank')
    pd_mean_group = pd_mean.groupby(['tool'])

    # labels = pd_mean.index.get_level_values(1).unique().to_list()
    # labels = ['MS1','MS2','MS3','MS4','MS5','MS6','MS7','MS8','MS9','MS10','MS11','MS12','MS13','MS14','MS15','MS16','MS17','ML1']
    # labels = ['SS1','SS2','SS3','SS4','SS5','SS6','SS7','SS8','SS9','SS10','SS11','SS12','SS13','SS14','SL1']
    labels = ['MetaPhlAn 2.2.0', 'MetaPhlAn 2.9.21', 'mOTUs 1.1', 'mOTUs 2.5.1', 'Bracken 2.5', 'MetaPalette 1.0.0', 'MetaPhyler 1.25', 'FOCUS 0.31', 'TIPP 2.0.0', 'CAMIARKQuikr 1.0.0']

    num_cols = 5
    fig, axs = plt.subplots(2, num_cols, figsize=(26, 9.5))

    fontsize = 24

    # metrics = [c.RECALL, c.PRECISION, 'Purity (1% filtered)', c.L1NORM, 'L1 norm error (no normalization)']
    # metrics = [c.RECALL, c.PRECISION, 'Purity (1% filtered)', c.L1NORM]
    metrics = [c.RECALL, 'Purity (1% filtered)', 'Purity (unfiltered)', c.L1NORM]
    # colors = [plt.cm.tab10(2), plt.cm.tab10(0), 'blue', plt.cm.tab10(3), 'black']
    colors = get_colors()
    colors = [colors[0], colors[1], colors[4], colors[2]]
    # colors_band = [plt.cm.tab10(2), plt.cm.tab10(0), None, plt.cm.tab10(3), None]
    colors_band = [colors[0], colors[1], None, colors[3]]

    row = 0
    col = 0
    for i, tool in enumerate(labels):
        tool_group = pd_mean_group.get_group(tool)

        metric_to_rank_to_values = OrderedDict((metric, []) for metric in metrics)
        metric_to_rank_to_std = OrderedDict((metric, []) for metric in metrics)

        for metric in metrics:
            metric_to_rank_to_values[metric] = [0] * len(ranks)
            metric_to_rank_to_std[metric] = [0] * len(ranks)
            for rank, rank_group in tool_group.groupby(['rank']):
                index = rank_to_index[rank]
                metric_to_rank_to_values[metric][index] = rank_group[metric].values[0]
                if metric in pd_std_over_samples.columns:
                    metric_to_rank_to_std[metric][index] = pd_std_over_samples.loc[(rank, tool)][metric]

        axs[row, col].set_title(tool, fontsize=fontsize)

        # force axis to be from 0 to 100%
        axs[row, col].set_ylim([0.0, 1.0])
        axs[row, col].set_xlim([0, 6])

        plots = []
        for metric, color, color_band in zip(metrics, colors, colors_band):
            values = metric_to_rank_to_values[metric]
            stds = metric_to_rank_to_std[metric]
            plot1 = axs[row, col].plot(x, values, color=color, linewidth=3)
            if color_band:
                plot2 = axs[row, col].fill_between(x, np.subtract(values, stds), np.add(values, stds), facecolor=color, alpha=0.3, edgecolor=None)
                plots.append((plot1[0], plot2))
            else:
                plots.append((plot1[0]))

        # axs[row, col].set_xticklabels([''] + ranks, horizontalalignment='right', fontsize=24)
        axs[row, col].set_xticklabels(ranks, horizontalalignment='right', fontsize=fontsize)

        # axs[row, col].tick_params(axis='x', labelsize=16, labelrotation=35)

        # axs[row, col].tick_params(axis='x', labelrotation=35, length=(0 if 0 <= row <= 2 else 10))
        # axs[row, col].tick_params(axis='y', labelsize=fontsize, length=(10 if col == 0 else 0))
        axs[row, col].tick_params(axis='x', labelrotation=35)
        axs[row, col].tick_params(axis='y', labelsize=fontsize)

        # reduce number of ticks
        axs[row, col].yaxis.set_major_locator(plt.MaxNLocator(4))

        yticks = axs[row, col].get_yticks()
        axs[row, col].set_yticklabels(['{:,.0%}'.format(x) for x in yticks])

        axs[row, col].grid(which='major', linestyle=':', linewidth='0.5')

        if (i + 1) % num_cols == 0:
            row += 1
            col = 0
        else:
            col += 1

    for ax in fig.get_axes():
        ax.label_outer()

    plt.subplots_adjust(hspace=0.15, wspace=0.2)

    lgd = plt.legend(plots, metrics, bbox_to_anchor=(-2.0, 2.3), loc=8, borderaxespad=0., handlelength=2, frameon=False, fontsize=fontsize, ncol=5)
    for lgd_hanle in lgd.legendHandles:
        lgd_hanle.set_linewidth(5.0)
    # lgd = plt.legend(plots, metrics, bbox_to_anchor=(-1.35, 4.75), loc=8, borderaxespad=0., handlelength=2, frameon=False, fontsize=24, ncol=5)
    # lgd = plt.legend([(plot1a[0], plot1b), (plot2a[0], plot2b), (plot3a[0], plot3b)], [c.RECALL, c.PRECISION, c.L1NORM], bbox_to_anchor=(-1.85, 3.6), loc=8, borderaxespad=0., handlelength=2, frameon=False, fontsize=24, ncol=4)

    fig.savefig(os.path.join(output_dir, 'purity_completeness_per_rank.pdf'), dpi=100, format='pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, 'purity_completeness_per_rank.png'), dpi=100, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
    # fig.savefig(os.path.join(output_dir, 'by_tool', 'purity_completeness_per_rank.png'), dpi=50, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.close(fig)


def plot_purity_completeness_per_tool_and_rank(pd_std_over_samples, pd_mean, output_dir):
    # pd_sem_over_samples = pd_grouped.groupby(['rank', 'tool'], sort=False).sem()

    ranks = c.ALL_RANKS[0:-1]
    x = range(len(ranks))
    rank_to_index = dict(zip(ranks, list(range(len(ranks)))))

    # pd_mean = pd_mean.drop(c.GS, level='tool').drop(['strain', 'rank independent'], level='rank')
    pd_mean_group = pd_mean.groupby(['tool'])
    # print(pd_mean.groupby(['tool']).get_group('MetaPhlAn 2.9.21'))
    # exit()
    labels = ['MetaPhlAn 2.2.0', 'MetaPhlAn 2.9.21', 'mOTUs 1.1', 'mOTUs 2.5.1', 'Bracken 2.5', 'MetaPalette 1.0.0', 'MetaPhyler 1.25', 'FOCUS 0.31', 'TIPP 2.0.0', 'CAMIARKQuikr 1.0.0']

    # labels = pd_mean.reset_index()['tool'].unique()
    # labels = pd_mean.index.get_level_values(1).unique().to_list()

    # pd_mean = pd_mean.reindex(labels, level='tool')

    num_cols = 5
    fig, axs = plt.subplots(2, num_cols, figsize=(30, 14))

    fontsize = 20

    row = 0
    col = 0
    # for i, (tool, tool_group) in enumerate(pd_mean.groupby(['tool'])):
    for i, tool in enumerate(labels):
        tool_group = pd_mean_group.get_group(tool)
        recall_list = [0] * len(ranks)
        recall_sem_list = [0] * len(ranks)
        precision_list = [0] * len(ranks)
        precision_sem_list = [0] * len(ranks)
        precision_list_u = [0] * len(ranks)
        precision_sem_list_u = [0] * len(ranks)
        braycurtis_list = [0] * len(ranks)
        braycurtis_sem_list = [0] * len(ranks)
        for rank, rank_group in tool_group.groupby(['rank']):
            index = rank_to_index[rank]
            recall_list[index] = rank_group[c.RECALL].values[0]
            recall_sem_list[index] = pd_std_over_samples.loc[(rank, tool)][c.RECALL]
            precision_list[index] = rank_group[c.PRECISION].values[0]
            precision_sem_list[index] = pd_std_over_samples.loc[(rank, tool)][c.PRECISION]
            # precision_list_u[index] = rank_group[c.PRECISION_UNFILTERED].values[0]
            # precision_sem_list_u[index] = pd_std_over_samples.loc[(rank, tool)][c.PRECISION_UNFILTERED]
            # braycurtis_list[index] = rank_group[c.BRAY_CURTIS].values[0]
            # braycurtis_sem_list[index] = pd_std_over_samples.loc[(rank, tool)][c.BRAY_CURTIS]

        axs[row, col].set_title(tool, fontsize=fontsize)

        # force axis to be from 0 to 100%
        axs[row, col].set_ylim([0.0, 1.0])
        axs[row, col].set_xlim([0, 6])

        plot1a = axs[row, col].plot(x, recall_list, color=plt.cm.tab10(2))
        plot2a = axs[row, col].plot(x, precision_list, color=plt.cm.tab10(0))
        # plot2xa = axs[row, col].plot(x, precision_list_u, color='blue')
        plot3a = axs[row, col].plot(x, braycurtis_list, color=plt.cm.tab10(3))
        plot1b = axs[row, col].fill_between(x, np.subtract(recall_list, recall_sem_list), np.add(recall_list, recall_sem_list), facecolor=plt.cm.tab10(2), alpha=0.3, edgecolor=None)
        plot2b = axs[row, col].fill_between(x, np.subtract(precision_list, precision_sem_list), np.add(precision_list, precision_sem_list), facecolor=plt.cm.tab10(0), alpha=0.3, edgecolor=None)
        # plot2xb = axs[row, col].fill_between(x, np.subtract(precision_list_u, precision_sem_list_u), np.add(precision_list_u, precision_sem_list_u), facecolor='blue', alpha=0.3, edgecolor=None)
        plot3b = axs[row, col].fill_between(x, np.subtract(braycurtis_list, braycurtis_sem_list), np.add(braycurtis_list, braycurtis_sem_list), facecolor=plt.cm.tab10(3), alpha=0.3, edgecolor=None)

        # axs[row, col].set_xticklabels([''] + ranks, horizontalalignment='right', fontsize=24)
        axs[row, col].set_xticklabels(ranks, horizontalalignment='right', fontsize=fontsize)

        # axs[row, col].tick_params(axis='x', labelsize=16, labelrotation=35)
        axs[row, col].tick_params(axis='x', labelrotation=45, length=(0 if row == 0 or row == 1 else 10))
        axs[row, col].tick_params(axis='y', labelsize=fontsize, length=(10 if col == 0 else 0))

        # reduce number of ticks
        axs[row, col].yaxis.set_major_locator(plt.MaxNLocator(4))

        yticks = axs[row, col].get_yticks()
        axs[row, col].set_yticklabels(['{:,.0%}'.format(x) for x in yticks])

        if (i + 1) % num_cols == 0:
            row += 1
            col = 0
        else:
            col += 1

    for ax in fig.get_axes():
        ax.label_outer()

    # plt.locator_params(axis='y', nbins=1)
    plt.subplots_adjust(hspace=0.2, wspace=0.2)

    # plt.setp(ax.get_xticklabels(), fontsize=16, rotation=35)
    # plt.yticks(fontsize=25)
    # plt.xticks(fontsize=16, rotation=35)

    # axs.set_title(tool, fontsize=25)


    lgd = plt.legend([(plot1a[0], plot1b), (plot2a[0], plot2b), (plot3a[0], plot3b)], [c.RECALL, c.PRECISION, c.L1NORM], bbox_to_anchor=(-1.85, 3.6), loc=8, borderaxespad=0., handlelength=2, frameon=False, fontsize=24, ncol=4)
    # lgd = plt.legend([(plot1a[0], plot1b), (plot2a[0], plot2b), (plot2xa[0]), (plot3a[0], plot3b)], [c.RECALL, 'Purity (1% filtered)', c.PRECISION_UNFILTERED, c.L1NORM], bbox_to_anchor=(-1.95, 2.4), loc=8, borderaxespad=0., handlelength=2, frameon=False, fontsize=24, ncol=4)


    # lgd = plt.legend([(plot1a[0], plot1b), (plot2a[0], plot2b), (plot2xa[0]), (plot3a[0], plot3b)], [c.RECALL, c.PRECISION, c.PRECISION_UNFILTERED, c.L1NORM], bbox_to_anchor=(-1.95, 2.4), loc=8, borderaxespad=0., handlelength=2, frameon=False, fontsize=24, ncol=4)

    # lgd = plt.legend((plot1a[0], plot2a[0]), ('Completeness', 'Purity'), bbox_to_anchor=(-2.1, -0.8), loc=8, borderaxespad=0., handlelength=2, frameon=False, fontsize=24, ncol=2)
    # lgd = plt.legend(['Completeness', 'Purity'], bbox_to_anchor=(-2.1, -0.8), loc=8, borderaxespad=0., handlelength=2, frameon=False, fontsize=24, ncol=2)
    # plt.tight_layout()
    # plt.tight_layout()

    print(output_dir)
    fig.savefig(os.path.join(output_dir, 'purity_completeness_per_rank.pdf'), dpi=100, format='pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, 'purity_completeness_per_rank.png'), dpi=100, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
    # fig.savefig(os.path.join(output_dir, 'by_tool', 'purity_completeness_per_rank.png'), dpi=50, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.close(fig)



# add to plot_purity_completeness_per_tool_and_rank in plots.py
# pd_std_over_samples.to_csv(os.path.join(output_dir, 'pd_std_over_samples.tsv'), sep='\t')
# pd_mean.to_csv(os.path.join(output_dir, 'pd_mean.tsv'), sep='\t')

output_dir = '/home/fmeyer/projects/tutorial/revision/opal_mouse_gut_filter_no_normalization_xx/'
pd_mean = pd.read_csv(output_dir + 'pd_mean.tsv', sep='\t', index_col=['rank', 'tool'])
pd_std_over_samples = pd.read_csv(output_dir +  'pd_std_over_samples.tsv', sep='\t', index_col=['rank', 'tool'])


pd_std_over_samples_unnorm = pd.read_csv('/home/fmeyer/projects/tutorial/revision/opal_mouse_gut_filter_xx/pd_std_over_samples.tsv', sep='\t', index_col=['rank', 'tool'])



pd_mean['Purity (1% filtered)'] = pd_mean[c.PRECISION]
pd_mean.drop(c.L1NORM, axis=1, inplace=True)
pd_mean.rename(columns={c.BRAY_CURTIS: c.L1NORM}, inplace=True)

pd_std_over_samples['Purity (1% filtered)'] = pd_std_over_samples[c.PRECISION]
pd_std_over_samples.drop(c.L1NORM, axis=1, inplace=True)
pd_std_over_samples.rename(columns={c.BRAY_CURTIS: c.L1NORM}, inplace=True)

# plot_purity_completeness_per_tool_and_rank(pd_std_over_samples, pd_mean, output_dir)
go_workshop(pd_std_over_samples, pd_mean, output_dir)
exit()





# workdir = '/home/fmeyer/cami2/datasets/strain_madness/short_read/opal/'
# workdir2 = '/home/fmeyer/cami2/datasets/strain_madness/short_read/opal_filter1/'
# workdir3 = '/home/fmeyer/cami2/datasets/strain_madness/short_read/opal_no_normalization/'

# workdir = '/home/fmeyer/cami2/datasets/strain_madness/opal_short_long/'
# workdir2 = '/home/fmeyer/cami2/datasets/strain_madness/opal_short_long_filter1/'
# workdir3 = '/home/fmeyer/cami2/datasets/strain_madness/opal_short_long_no_normalization/'

# workdir = '/home/fmeyer/cami2/datasets/marine/opal_short_long_ABC/'
# workdir2 = '/home/fmeyer/cami2/datasets/marine/opal_short_long_filter1_ABC/'
# workdir3 = '/home/fmeyer/cami2/datasets/marine/opal_short_long_no_normalization_ABC/'

# workdir = '/home/fmeyer/cami2/datasets/strain_madness/opal_short_long_ABC/'
# workdir2 = '/home/fmeyer/cami2/datasets/strain_madness/opal_short_long_filter1_ABC/'
# workdir3 = '/home/fmeyer/cami2/datasets/strain_madness/opal_short_long_no_normalization_ABC/'
#
# pd_mean = pd.read_csv(workdir + 'pd_mean.tsv', sep='\t', index_col=['rank', 'tool'])
# pd_mean2 = pd.read_csv(workdir2 + 'pd_mean.tsv', sep='\t', index_col=['rank', 'tool'])
# pd_mean3 = pd.read_csv(workdir3 + 'pd_mean.tsv', sep='\t', index_col=['rank', 'tool'])
#
# pd_mean['Purity (1% filtered)'] = pd_mean2[c.PRECISION]
# pd_mean.drop(c.L1NORM, axis=1, inplace=True)
# pd_mean.rename(columns={c.BRAY_CURTIS: c.L1NORM}, inplace=True)
#
# pd_std_over_samples = pd.read_csv(workdir + 'pd_std_over_samples.tsv', sep='\t', index_col=['rank', 'tool'])
#
# pd_std_over_samples.drop(c.L1NORM, axis=1, inplace=True)
# pd_std_over_samples.rename(columns={c.BRAY_CURTIS: c.L1NORM}, inplace=True)
#
# pd_mean['L1 norm error (no normalization)'] = pd_mean3[c.BRAY_CURTIS]

# plot_purity_completeness_per_tool_and_rank(pd_std_over_samples, pd_mean, '/home/fmeyer/tutorial/opal_mouse_gut_filter')
# go_workshop(pd_std_over_samples, pd_mean, workdir)

