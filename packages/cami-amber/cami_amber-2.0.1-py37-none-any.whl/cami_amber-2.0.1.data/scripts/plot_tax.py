from src.utils import labels as utils_labels
from src.utils import load_ncbi_taxinfo
from src import binning_classes
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
import numpy as np
import os, sys, inspect
import pandas as pd
from collections import OrderedDict

RANKS = load_ncbi_taxinfo.RANKS[:-1]


def plot_taxonomic_results(df_summary_t, metrics_list, errors_list, file_name, output_dir):
    colors_list = ["#006cba", "#008000", "#ba9e00", "red"] ##006cba=blue, #008000=green, #ba9e00=gold

    df_summary_t = df_summary_t.groupby([utils_labels.TOOL, 'rank']).mean().reset_index()
    # df_summary_t.to_csv('/home/fmeyer/tmp/ambe_tax_test/mean.tsv', sep='\t')

    for tool, pd_results in df_summary_t.groupby(utils_labels.TOOL):
        if tool == 'Gold standard':
            continue
        metrics_list_to_ranks_dict = []
        for metric in metrics_list:
            rank_to_metric = OrderedDict([(k, .0) for k in RANKS])
            metrics_list_to_ranks_dict.append(rank_to_metric)
        errors_list_to_ranks_dict = []
        for error in errors_list:
            rank_to_metric_error = OrderedDict([(k, .0) for k in RANKS])
            errors_list_to_ranks_dict.append(rank_to_metric_error)

        for index, row in pd_results.iterrows():
            for rank_to_metric, metric in zip(metrics_list_to_ranks_dict, metrics_list):
                rank_to_metric[row[utils_labels.RANK]] = .0 if np.isnan(row[metric]) else row[metric]
            for rank_to_metric_error, error in zip(errors_list_to_ranks_dict, errors_list):
                rank_to_metric_error[row[utils_labels.RANK]] = .0 if np.isnan(row[error]) else row[error]
        # print(rank_to_metric)

        fig, axs = plt.subplots(figsize=(5.5, 5.5))

        # force axes to be from 0 to 100%
        axs.set_xlim([0, len(RANKS)-1])
        axs.set_ylim([0.0, 1.0])
        x_values = range(len(RANKS))

        y_values_list = []
        for rank_to_metric, color in zip(metrics_list_to_ranks_dict, colors_list):
            print(rank_to_metric)
            y_values = list(rank_to_metric.values())
            axs.plot(x_values, y_values, color=color)
            y_values_list.append(y_values)

        for rank_to_metric_error, y_values, color in zip(errors_list_to_ranks_dict, y_values_list, colors_list):
            sem = list(rank_to_metric_error.values())
            plt.fill_between(x_values, np.subtract(y_values, sem).tolist(), np.add(y_values, sem).tolist(), color=color, alpha=0.5)

        plt.xticks(x_values, RANKS, rotation='vertical', fontsize=18)
        axs.tick_params(axis='y', labelsize=16)

        vals = axs.get_yticks()
        axs.set_yticklabels(['{:3.0f}%'.format(x * 100) for x in vals])

        # lgd = plt.legend(metrics_list, loc=1, borderaxespad=0., handlelength=2, frameon=False)

        plt.tight_layout()
        fig.savefig(os.path.join(output_dir, 'taxonomic', tool, file_name + '.png'), dpi=100, format='png', bbox_inches='tight')
        # fig.savefig(os.path.join(output_dir, 'taxonomic', tool, file_name + '.png'), dpi=100, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
        # fig.savefig(os.path.join(output_dir, 'taxonomic', tool, file_name + '.pdf'), dpi=100, format='pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
        plt.close(fig)


def go(summary_file, output_dir):
    df_summary_t = pd.read_csv(summary_file, sep='\t')

    metrics_list = [utils_labels.AVG_RECALL_BP, utils_labels.AVG_PRECISION_BP, utils_labels.RECALL_PER_BP, utils_labels.PRECISION_PER_BP]
    errors_list = [utils_labels.AVG_RECALL_BP_SEM, utils_labels.AVG_PRECISION_BP_SEM]
    plot_taxonomic_results(df_summary_t, metrics_list, errors_list, 'avg_precision_recall_bp', output_dir)

    # metrics_list = [utils_labels.PRECISION_PER_BP, utils_labels.RECALL_PER_BP, utils_labels.PRECISION_PER_SEQ,
    #                 utils_labels.RECALL_PER_SEQ]

    metrics_list = [utils_labels.RECALL_PER_BP, utils_labels.PRECISION_PER_BP]
    plot_taxonomic_results(df_summary_t, metrics_list, [], 'precision_recall', output_dir)


if __name__ == "__main__":
    # go('/home/fmeyer/cami2/amber_grave_ritchie_0/results.tsv', '/home/fmeyer/cami2/ismb2020/ambe_tax_test/')
    # go('/home/fmeyer/cami2/amber_marine_nbcpp/results.tsv', '/home/fmeyer/cami2/ismb2020/ambe_tax_test/')
    # go('/home/fmeyer/cami2/datasets/marine/short_read/amber_tax/results.tsv', '/home/fmeyer/cami2/ismb2020/ambe_tax_test/')

    # go('/home/fmeyer/cami2/datasets/strain_madness/short_read/amber_tax/results.tsv', '/home/fmeyer/cami2/ismb2020/ambe_tax_test/')
    # go('/home/fmeyer/cami2/ismb2020/strain_madness/amber_strain_madness_tax/results.tsv', '/home/fmeyer/cami2/ismb2020/ambe_tax_test/')
    # go('/home/fmeyer/cami2/amber_hopeful_lovelace_0/results.tsv', '/home/fmeyer/cami2/ismb2020/ambe_tax_test/')
    go('/home/fmeyer/cami2/amber_grave_ritchie_2/results.tsv', '/home/fmeyer/cami2/ismb2020/ambe_tax_test/')
