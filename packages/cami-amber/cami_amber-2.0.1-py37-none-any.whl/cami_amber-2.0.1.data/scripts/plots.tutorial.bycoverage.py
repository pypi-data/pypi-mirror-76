#!python
from src.utils import load_data
import matplotlib
from src import plots
matplotlib.use('Agg')
from src.utils import labels as utils_labels
from src import binning_classes

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
import numpy as np
import os, sys, inspect
import pandas as pd
from collections import OrderedDict


def create_colors_list():
    x = sns.color_palette('colorblind')
    return [x[0], x[1], x[2], x[4], x[7]]


def get_pd_genomes_recall(sample_id_to_queries_list):
    pd_genomes_recall = pd.DataFrame()
    for sample_id in sample_id_to_queries_list:
        for query in sample_id_to_queries_list[sample_id]:
            if not isinstance(query, binning_classes.GenomeQuery):
                continue
            recall_df = query.recall_df[['genome_id', 'recall_bp']].copy()
            recall_df[utils_labels.TOOL] = query.label
            recall_df['sample_id'] = sample_id
            recall_df = recall_df.reset_index().set_index(['sample_id', utils_labels.TOOL])
            pd_genomes_recall = pd.concat([pd_genomes_recall, recall_df])
    return pd_genomes_recall


def plot_by_genome_coverage(pd_bins, pd_target_column, available_tools, output_dir):
    colors_list = create_colors_list()
    if len(available_tools) > len(colors_list):
        raise RuntimeError("Plot only supports 29 colors")

    fig, axs = plt.subplots(figsize=(5, 4.5))

    for i, (color, tool) in enumerate(zip(colors_list, available_tools)):
        pd_tool = pd_bins[pd_bins[utils_labels.TOOL] == tool].sort_values(by=['genome_index'])
        axs.scatter(pd_tool['genome_coverage'], pd_tool[pd_target_column], marker='o', color=colors_list[i], s=[2] * pd_tool.shape[0])
        window = 50
        rolling_mean = pd_tool[pd_target_column].rolling(window=window, min_periods=10).mean()
        axs.plot(pd_tool['genome_coverage'], rolling_mean, color=colors_list[i])

    axs.set_xlim([0.0, pd_tool['genome_coverage'].max()])
    axs.set_ylim([0.0, 1.0])

    # transform plot_labels to percentages
    vals = axs.get_yticks()
    axs.set_yticklabels(['{:3.0f}'.format(x * 100) for x in vals], fontsize=12)

    axs.tick_params(axis='x', labelsize=12)

    if pd_target_column == 'precision_bp':
        ylabel = 'Purity per bin (%)'
        file_name = 'purity_by_genome_coverage'
    else:
        ylabel = 'Completeness per genome (%)'
        file_name = 'completeness_by_genome_coverage'

    plt.ylabel(ylabel, fontsize=15)
    plt.xlabel('log$_{10}$(average genome coverage)', fontsize=15)

    colors_iter = iter(colors_list)
    circles = []
    for x in range(len(available_tools)):
        circles.append(Line2D([], [], markeredgewidth=0.0, linestyle="None", marker="o", markersize=11, markerfacecolor=next(colors_iter)))
    lgd = plt.legend(circles, available_tools, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., handlelength=0, frameon=False, fontsize=14)

    fig.savefig(os.path.join(output_dir, file_name + '.pdf'), dpi=100, format='pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.close(fig)


def plot_precision_recall_by_coverage(sample_id_to_queries_list, pd_bins_g, coverages_pd, available_tools, output_dir):
    # compute average genome coverage if coverages for multiple samples were provided
    coverages_pd = coverages_pd.groupby(['GENOMEID']).mean()
    coverages_pd.rename(columns={'GENOMEID': 'genome_id'})
    coverages_pd = coverages_pd.sort_values(by=['COVERAGE'])
    coverages_pd['rank'] = coverages_pd['COVERAGE'].rank()

    # pd_genomes_recall = get_pd_genomes_recall(sample_id_to_queries_list)
    # pd_genomes_recall['genome_index'] = pd_genomes_recall['genome_id'].map(coverages_pd['rank'].to_dict())
    # pd_genomes_recall = pd_genomes_recall.groupby([utils_labels.TOOL, 'genome_id']).mean().reset_index()
    # pd_genomes_recall['genome_coverage'] = np.log10(pd_genomes_recall['genome_id'].map(coverages_pd['COVERAGE'].to_dict()))
    # plot_by_genome_coverage(pd_genomes_recall, 'recall_bp', available_tools, output_dir)

    pd_bins_precision = pd_bins_g[[utils_labels.TOOL, 'purity_bp', 'most_abundant_genome']].copy().dropna(subset=['purity_bp'])
    pd_bins_precision['genome_index'] = pd_bins_precision['most_abundant_genome'].map(coverages_pd['rank'].to_dict())
    pd_bins_precision['genome_coverage'] = np.log10(pd_bins_precision['most_abundant_genome'].map(coverages_pd['COVERAGE'].to_dict()))
    plot_by_genome_coverage(pd_bins_precision, 'purity_bp', available_tools, output_dir)


coverage_file = '/home/fmeyer/cami2/datasets/19122017_mousegut_scaffolds/average_coverage.tsv'
coverages_pd = load_data.open_coverages(coverage_file)
output_dir = '/home/fmeyer/tmp'
available_tools = ['MaxBin 2.2.7', 'MetaBAT 2.12.1', 'CONCOCT 1.0.0', 'DAS Tool 1.1.2']

input_dir = '/home/fmeyer/projects/tutorial/amber_mouse_gut'
pd_bins = pd.read_csv(os.path.join(input_dir, 'pd_bins.tsv'), sep='\t', index_col=0)
# print(pd_bins)
# exit()

sample_id_to_queries_list = None

plot_precision_recall_by_coverage(sample_id_to_queries_list,
                                  pd_bins, coverages_pd, available_tools,
                                  output_dir)