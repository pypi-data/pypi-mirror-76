import pandas as pd
import logging
import itertools
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import os
from abc import ABC, abstractmethod
from collections import defaultdict
from collections import OrderedDict
from src.utils import labels as utils_labels
from src.utils import load_ncbi_taxinfo
from src.utils import ProfilingTools as pf
from src import unifrac_distance as uf
from src import precision_recall_per_bin
from src import plots
import seaborn as sns


def get_colors():
    x = sns.color_palette('colorblind')
    return [x[0], x[1], x[2], x[4], x[7]]


def plot_precision_vs_bin_size(precision_df, labels, output_dir):
    # colors_list = plots.create_colors_list()
    colors_list = get_colors()
    fig, axs = plt.subplots(figsize=(4.5, 4))

    groups = precision_df.groupby('Tool')
    for i, label in enumerate(labels):
        groupx = groups.get_group(label)
        df_sorted = groupx[['total_length', 'precision_bp']].sort_values(by=['total_length'])
        # axs.scatter(np.log(df_sorted['total_length']), df_sorted['precision_bp'], marker='o', color=colors_list[i], s=[2] * df_sorted.shape[0])
        # window = int(df_sorted.shape[0] / 50) if df_sorted.shape[0] > 100 else int(df_sorted.shape[0] / 10)
        # print(window)
        window = 30
        rolling_mean = df_sorted['precision_bp'].rolling(window=window, min_periods=2).mean()
        axs.plot(np.log(df_sorted['total_length']), rolling_mean, color=colors_list[i])

    xmax = np.log(precision_df['total_length'].max())
    plt.xticks(np.arange(10, xmax + 1, 2.0))
    axs.set_xlim([None, 18.2])
    axs.set_ylim([-0.04, 1.04])

    axs.tick_params(axis='x', labelsize=11)
    axs.tick_params(axis='y', labelsize=11)

    axs.grid(which='major', linestyle=':', linewidth='0.5')

    vals = axs.get_xticks()
    # axs.set_xticklabels(['{:3.0f}'.format(np.exp(x)) for x in vals], ha='right')
    axs.set_xticklabels(['{:,}'.format(int(np.exp(x)/1000)) for x in vals], ha='right')

    # transform plot_labels to percentages
    vals = axs.get_yticks()
    axs.set_yticklabels(['{:3.0f}'.format(y * 100) for y in vals])

    # axs.set_title(self.label, fontsize=12)
    plt.ylabel('Purity per bin (%)', fontsize=14)
    plt.xlabel('Bin size (Kb)', fontsize=14)
    # lgd = plt.legend(labels, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., handlelength=1, frameon=False, fontsize=12)
    # fig.savefig(os.path.join(output_dir, 'purity_vs_bin_size_png'), dpi=200, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
    # fig.savefig(os.path.join(output_dir, 'purity_vs_bin_size.pdf'), dpi=200, format='pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, 'purity_vs_bin_size.pdf'), dpi=200, format='pdf', bbox_inches='tight')
    plt.close(fig)


def plot_recall_vs_genome_size(recall_df, labels, output_dir):
    # colors_list = plots.create_colors_list()
    colors_list = get_colors()
    fig, axs = plt.subplots(figsize=(4.5, 4))

    groups = recall_df.groupby('Tool')
    for i, label in enumerate(labels):
        groupx = groups.get_group(label)
        df_sorted = groupx[['total_length', 'recall_bp']].sort_values(by=['total_length'])

        # axs.scatter(np.log(df_sorted['total_length']), df_sorted['recall_bp'], marker='o', color=colors_list[i], s=[2] * df_sorted.shape[0])
        window = 30
        # window = int(df_sorted.shape[0] / 50) if df_sorted.shape[0] > 100 else int(df_sorted.shape[0] / 10)
        rolling_mean = df_sorted['recall_bp'].rolling(window=window, min_periods=2).mean()
        axs.plot(np.log(df_sorted['total_length']), rolling_mean, color=colors_list[i])

    xmax = np.log(recall_df['total_length'].max())
    plt.xticks(np.arange(10, xmax + 1, 2.0))
    axs.set_xlim([None, 18.2])
    axs.set_ylim([-0.04, 1.04])

    axs.tick_params(axis='x', labelsize=11)
    axs.tick_params(axis='y', labelsize=11)

    axs.grid(which='major', linestyle=':', linewidth='0.5')

    vals = axs.get_xticks()
    axs.set_xticklabels(['{:,}'.format(int(np.exp(x)/1000)) for x in vals], ha='right')

    # transform plot_labels to percentages
    vals = axs.get_yticks()
    axs.set_yticklabels(['{:3.0f}'.format(y * 100) for y in vals])

    # axs.set_title(self.label, fontsize=12)
    plt.ylabel('Completeness per genome (%)', fontsize=14)
    plt.xlabel('Genome size (Kb)', fontsize=14)
    # lgd = plt.legend(labels, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., handlelength=1, frameon=False, fontsize=12)
    # fig.savefig(os.path.join(output_dir, 'completeness_vs_bin_size_png'), dpi=200, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
    # fig.savefig(os.path.join(output_dir, 'completeness_vs_bin_size.pdf'), dpi=200, format='pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, 'completeness_vs_bin_size.pdf'), dpi=200, format='pdf', bbox_inches='tight')
    plt.close(fig)


FILES1 = ['/home/fmeyer/tmp/amber_mouse_gut_genome/genome/Gold standard/precision_df_gsa_pooled.tsv',
    '/home/fmeyer/tmp/amber_mouse_gut_genome/genome/CONCOCT 1.0.0/precision_df_gsa_pooled.tsv',
'/home/fmeyer/tmp/amber_mouse_gut_genome/genome/DAS Tool 1.1.2/precision_df_gsa_pooled.tsv',
'/home/fmeyer/tmp/amber_mouse_gut_genome/genome/MaxBin 2.2.7/precision_df_gsa_pooled.tsv',
'/home/fmeyer/tmp/amber_mouse_gut_genome/genome/MetaBAT 2.12.1/precision_df_gsa_pooled.tsv']

FILES2 = ['/home/fmeyer/tmp/amber_mouse_gut_genome/genome/Gold standard/recall_df_gsa_pooled.tsv',
          '/home/fmeyer/tmp/amber_mouse_gut_genome/genome/MaxBin 2.2.7/recall_df_gsa_pooled.tsv',
          '/home/fmeyer/tmp/amber_mouse_gut_genome/genome/MetaBAT 2.12.1/recall_df_gsa_pooled.tsv',
          '/home/fmeyer/tmp/amber_mouse_gut_genome/genome/CONCOCT 1.0.0/recall_df_gsa_pooled.tsv',
          '/home/fmeyer/tmp/amber_mouse_gut_genome/genome/DAS Tool 1.1.2/recall_df_gsa_pooled.tsv']


def main():
    labels = "Gold standard, MaxBin 2.2.7, MetaBAT 2.12.1, CONCOCT 1.0.0, DAS Tool 1.1.2".split(', ')
    output_dir = '/home/fmeyer/tmp/amber_mouse_gut_genome'
    precision_df = pd.DataFrame()
    for file in FILES1:
        xx = pd.read_csv(file, sep='\t')
        precision_df = pd.concat([precision_df, xx])
    plot_precision_vs_bin_size(precision_df, labels, output_dir)

    recall_df = pd.DataFrame()
    for label, file in zip(labels, FILES2):
        xx = pd.read_csv(file, sep='\t')
        xx['Tool'] = label
        recall_df = pd.concat([recall_df, xx])
    plot_recall_vs_genome_size(recall_df, labels, output_dir)


if __name__ == "__main__":
    main()
