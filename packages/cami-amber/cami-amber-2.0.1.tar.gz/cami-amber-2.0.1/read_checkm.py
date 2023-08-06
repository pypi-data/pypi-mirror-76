#!/usr/bin/env python3

import ast
import pandas as pd
import numpy as np
from scipy import stats
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from src.plots import create_colors_list
from src.utils import labels as utils_labels
import seaborn as sns


FILES = ['/home/fmeyer/projects/tutorial/revision/checkm/gs/bin_stats_ext.tsv',
         '/home/fmeyer/projects/tutorial/revision/checkm/maxbin/bin_stats_ext.tsv',
         '/home/fmeyer/projects/tutorial/revision/checkm/metabat/bin_stats_ext.tsv',
         '/home/fmeyer/projects/tutorial/revision/checkm/concoct/bin_stats_ext.tsv',
         '/home/fmeyer/projects/tutorial/revision/checkm/dastool/bin_stats_ext.tsv']

LABELS = [utils_labels.GS, 'MaxBin 2.2.7', 'MetaBAT 2.12.1', 'CONCOCT 1.0.0', 'DAS Tool 1.1.2']


def get_colors():
    x = sns.color_palette('colorblind')
    return [x[0], x[1], x[2], x[4], x[7]]


def plot_summary(color_indices, df_results, labels, output_dir, file_name, xlabel, ylabel):
    # available_tools = df_results[utils_labels.TOOL].unique()
    # tools = [tool for tool in labels if tool in available_tools]

    # colors_list = create_colors_list()
    colors_list = get_colors()
    if color_indices:
        colors_list = [colors_list[i] for i in color_indices]
    # df_mean = df_results.groupby(utils_labels.TOOL).mean().reindex(tools)
    # df_mean = df_results.groupby(utils_labels.TOOL).mean().reindex(tools)

    # fig, axs = plt.subplots(figsize=(5, 4.5))
    fig, axs = plt.subplots(figsize=(4.5, 4))

    # force axes to be from 0 to 100%
    axs.set_xlim([-0.04, 1.04])
    axs.set_ylim([-0.04, 1.04])

    # for i, (tool, df_row) in enumerate(df_results.iterrows()):
    for i, label in enumerate(labels):
        df_rows = df_results.loc[label]
        df_row = df_rows[df_rows['checkm'] == False]

        axs.errorbar(df_row['precision_bp'], df_row['recall_bp'], xerr=df_row['avg_precision_bp_var'], yerr=df_row['avg_recall_bp_var'],
                     fmt='o',
                     ecolor=colors_list[i],
                     mec=colors_list[i],
                     mfc=colors_list[i],
                     capsize=3,
                     markersize=8)
        df_row = df_rows[df_rows['checkm'] == True]
        axs.errorbar(df_row['precision_bp'], df_row['recall_bp'], xerr=df_row['avg_precision_bp_var'], yerr=df_row['avg_recall_bp_var'],
                     fmt='D',
                     ecolor=colors_list[i],
                     mec=colors_list[i],
                     mfc=colors_list[i],
                     capsize=3,
                     markersize=8)

    # turn on grid
    # axs.minorticks_on()
    axs.grid(which='major', linestyle=':', linewidth='0.5')
    # axs.grid(which='minor', linestyle=':', linewidth='0.5')

    vals = axs.get_xticks()
    axs.set_xticklabels(['{:3.0f}'.format(x * 100) for x in vals], fontsize=11)
    vals = axs.get_yticks()
    axs.set_yticklabels(['{:3.0f}'.format(x * 100) for x in vals], fontsize=11)

    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.tight_layout()

    colors_iter = iter(colors_list)
    circles = []
    # for x in range(len(labels)):
    #     circles.append(Line2D([], [], markeredgewidth=0.0, linestyle="None", marker="s", markersize=10, markerfacecolor=next(colors_iter)))
    # circles.append(Line2D([], [], markeredgewidth=.1, markeredgecolor='black', linestyle="None", marker="o", markersize=10, markerfacecolor='white'))
    # circles.append(Line2D([], [], markeredgewidth=.1, markeredgecolor='black', linestyle="None", marker="D", markersize=9, markerfacecolor='white'))
    # lgd = plt.legend(circles, labels + ['AMBER', 'CheckM'], bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., handlelength=0, frameon=False, fontsize=12)

    circles.append(Line2D([], [], markeredgewidth=2, markeredgecolor='black', linestyle="None", marker="o", markersize=10, markerfacecolor='white'))
    circles.append(Line2D([], [], markeredgewidth=2, markeredgecolor='black', linestyle="None", marker="D", markersize=9, markerfacecolor='white'))
    lgd = plt.legend(circles, ['AMBER', 'CheckM'], loc='lower right', borderaxespad=0., handlelength=0, frameon=False, fontsize=13)

    fig.savefig(os.path.join(output_dir, file_name + '.pdf'), dpi=100, format='pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
    fig.savefig(os.path.join(output_dir,file_name + '.png'), dpi=200, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.close(fig)
    print('Done')


def mydivision(row):
    return (row['# markers'] / row['divisor']) if row['divisor'] > 0 else 0


def load_checkm(file, label):
    print(label)
    genomes_dict = {}

    with open(file, 'r') as f:
        for line in f:
            line_split = line.strip().split('\t')
            genomes_dict[line_split[0]] = ast.literal_eval(line_split[1])

    results_pd = pd.DataFrame.from_dict(genomes_dict).T[['Completeness', '0', '1', '2', '3', '4', '5+', 'Genome size', '# markers']]
    results_pd['Completeness'] = results_pd['Completeness'] / 100
    # results_pd['Contamination'] = 1 - results_pd['Contamination'] / 100
    # results_pd.rename(columns={'Completeness': 'recall_bp', 'Contamination': 'precision_bp'}, inplace=True)
    results_pd['divisor'] = results_pd['0'] + results_pd['1'] + results_pd['2'] * 2 + results_pd['3'] * 3 + results_pd['4'] * 4 + results_pd['5+'] * 5



    results_pd['precision_bp'] = results_pd.apply(lambda row: mydivision(row), axis=1)
    results_pd.rename(columns={'Completeness': 'recall_bp'}, inplace=True)

    if label == 'CONCOCT 1.0.0':
        print(results_pd)
    # exit()



    results_pd['Tool'] = label
    results_pd.index.name = 'BINID'
    return results_pd.reset_index()

    # complteness_list = [item[1]['Completeness'] for item in genomes_dict.items()]
    # contamination_list = [item[1]['Contamination'] for item in genomes_dict.items()]

    # print(np.average(complteness_list))
    # print(np.std(complteness_list))
    # print(np.average(contamination_list))
    # print(stats.sem(contamination_list))
    # print(np.sem(contamination_list))


def create_legend(labels):
    colors_list = get_colors()

    colors_iter = iter(colors_list)
    circles = [Line2D([], [], markeredgewidth=0.0, linestyle="None", marker="o", markersize=10, markerfacecolor=next(colors_iter)) for label in labels]

    fig = plt.figure(figsize=(0.5, 0.5))
    fig.legend(circles, labels, loc='center', frameon=False, ncol=5, columnspacing=0.5, handletextpad=-0.1)
    fig.savefig(os.path.join('/home/fmeyer/tmp', 'legend.pdf'), dpi=100, format='pdf', bbox_inches='tight')
    plt.close(fig)


def main():
    # create_legend(LABELS)
    # exit()

    checkm = pd.DataFrame()
    for file, label in zip(FILES, LABELS):
        results_pd = load_checkm(file, label)
        checkm = pd.concat([checkm, results_pd])
    checkm = checkm.astype({'recall_bp': 'float64', 'precision_bp': 'float64'})
    checkm['checkm'] = True
    checkm['avg_recall_bp_var'] = checkm['recall_bp']
    checkm['avg_precision_bp_var'] = checkm['precision_bp']
    # print(all.groupby('Tool').mean()[['recall_bp', 'precision_bp']])
    # print(all.columns)
    # exit()


    # bins = pd.read_csv('/home/fmeyer/tmp/amber_mouse_gut_genome/bins.tsv', sep='\t')
    # bins = bins.loc[bins.groupby(['Tool', 'genome_id'])['recall_bp'].idxmax()]
    # for tool, pdgroup in bins.groupby('Tool'):
    #     print(tool, pdgroup['recall_bp'].mean())

    # genome_sizes_df = all.groupby('BINID', sort=False).agg({'Genome size': 'sum'}).rename(columns={'Genome size': 'length_gs'})
    # print(genome_sizes_df)
    # exit()
    #
    # precision_df = precision_df.reset_index().join(genome_sizes_df, on='genome_id', how='left', sort=False).set_index('BINID')
    # precision_df['recall_bp'] = precision_df['tp_length'] / precision_df['length_gs']
    # precision_df['recall_seq'] = precision_df['tp_seq_counts'] / precision_df['seq_counts_gs']
    # precision_df['rank'] = 'NA'
    #
    # recall_df = confusion_df.loc[confusion_df.groupby('genome_id', sort=False)['genome_length'].idxmax()]
    # recall_df = recall_df.reset_index().join(genome_sizes_df, on='genome_id', how='right', sort=False).set_index('BINID')
    # recall_df.fillna({'genome_length': 0, 'genome_seq_counts': 0}, inplace=True)
    # recall_df['recall_bp'] = recall_df['genome_length'] / recall_df['length_gs']
    # recall_df['recall_seq'] = recall_df['genome_seq_counts'] / recall_df['seq_counts_gs']


    bins = pd.read_csv('/home/fmeyer/tmp/amber_mouse_gut_genome/bins.tsv', sep='\t')
    bins = bins[['BINID', 'Tool', 'precision_bp', 'recall_bp']]
    bins['checkm'] = False
    bins['avg_recall_bp_var'] = bins['recall_bp']
    bins['avg_precision_bp_var'] = bins['precision_bp']

    # bins = bins[(bins['recall_bp'] > 0.7) & (bins['precision_bp'] > 0.9)]
    # checkm = checkm[checkm['BINID'].isin(bins['BINID'])]
    # checkm = checkm[(checkm['recall_bp'] > 0.7) & (checkm['precision_bp'] > 0.9)]
    # bins = bins[bins['BINID'].isin(bins['BINID'])]

    bins = bins.groupby('Tool').agg({'recall_bp': np.mean, 'precision_bp': np.mean, 'avg_recall_bp_var': np.var, 'avg_precision_bp_var': np.var, 'checkm': 'first'})
    bins = bins.reindex(LABELS)
    checkm = checkm.groupby('Tool').agg({'recall_bp': np.mean, 'precision_bp': np.mean, 'avg_recall_bp_var': np.var, 'avg_precision_bp_var': np.var, 'checkm': 'first'})
    checkm = checkm.reindex(LABELS)

    print(bins)
    print(checkm)
    # exit()


    print()
    x = np.absolute((checkm['recall_bp'] / bins['recall_bp']) - 1) * 100
    y = np.absolute((checkm['precision_bp'] / bins['precision_bp']) - 1) * 100
    print(x)
    print()
    print(y)
    exit()


    # amber_summary = pd.read_csv('/home/fmeyer/tmp/amber_mouse_gut_genome/results.tsv', sep='\t')
    # amber_summary.rename(columns={'Average completeness (bp) ': 'recall_bp', 'Average purity (bp)': 'precision_bp'}, inplace=True)
    # amber_summary = amber_summary[['Tool', 'precision_bp', 'recall_bp', 'avg_precision_bp_var' , 'avg_recall_bp_var']]
    # amber_summary['checkm'] = False
    # amber_summary = amber_summary.set_index('Tool').reindex(LABELS)
    # print(amber_summary)
    # exit()

    # all = pd.concat([amber_summary, all])

    all = pd.concat([bins, checkm])

    plot_summary(None, all, LABELS, '/home/fmeyer/tmp/', 'plot', 'Average purity (%)', 'Average completeness (%)')


if __name__ == "__main__":
    main()
