from src.utils import labels as utils_labels
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import os
import pandas as pd
import seaborn as sns


def get_colors():
    x = sns.color_palette('colorblind')
    return x
    # return [x[0], x[1], x[2], x[4], x[7]]


def get_number_of_hq_bins(tools, pd_bins):
    pd_counts = pd.DataFrame()
    pd_bins_copy = pd_bins[[utils_labels.TOOL, 'Purity (bp)', 'Completeness (bp)']].copy().dropna(subset=['Purity (bp)'])
    for tool in tools:
        pd_tool_bins = pd_bins_copy[pd_bins_copy[utils_labels.TOOL] == tool]
        x50 = pd_tool_bins[(pd_tool_bins['Completeness (bp)'] > .5) & (pd_tool_bins['Purity (bp)'] > .9)].shape[0]
        x70 = pd_tool_bins[(pd_tool_bins['Completeness (bp)'] > .7) & (pd_tool_bins['Purity (bp)'] > .9)].shape[0]
        x90 = pd_tool_bins[(pd_tool_bins['Completeness (bp)'] > .9) & (pd_tool_bins['Purity (bp)'] > .9)].shape[0]
        pd_tool_counts = pd.DataFrame([[x90, x70, x50]], columns=['>90%', '>70%', '>50%'], index=[tool])
        pd_counts = pd_counts.append(pd_tool_counts)
    return pd_counts


def get_number_of_hq_bins_by_score(tools, pd_bins):
    pd_counts = pd.DataFrame()
    pd_bins_copy = pd_bins[[utils_labels.TOOL, 'Purity (bp)', 'Completeness (bp)']].copy().dropna(subset=['Purity (bp)'])
    # pd_bins_copy['newcolumn'] = pd_bins_copy['Completeness (bp)'] + 5 * (pd_bins_copy['Purity (bp)'] - 1)
    for tool in tools:
        pd_tool_bins = pd_bins_copy[pd_bins_copy[utils_labels.TOOL] == tool]
        # x50 = pd_tool_bins[pd_tool_bins['newcolumn'] > .5].shape[0]
        # x70 = pd_tool_bins[pd_tool_bins['newcolumn'] > .7].shape[0]
        # x90 = pd_tool_bins[pd_tool_bins['newcolumn'] > .9].shape[0]
        x50 = pd_tool_bins[(pd_tool_bins['Completeness (bp)'] > .5) & (pd_tool_bins['Purity (bp)'] > .9)].shape[0]
        x70 = pd_tool_bins[(pd_tool_bins['Completeness (bp)'] > .7) & (pd_tool_bins['Purity (bp)'] > .9)].shape[0]
        x90 = pd_tool_bins[(pd_tool_bins['Completeness (bp)'] > .9) & (pd_tool_bins['Purity (bp)'] > .9)].shape[0]

        x50 -= x70
        x70 -= x90

        pd_tool_counts = pd.DataFrame([[x90, x70, x50]], columns=['>90%', '>70%', '>50%'], index=[tool])
        pd_counts = pd_counts.append(pd_tool_counts)
    return pd_counts


def plot_counts(pd_bins, tools, output_dir, output_file, get_bin_counts_function, counts_pos):
    pd_counts = get_bin_counts_function(tools, pd_bins)
    colors = get_colors()

    fig, axs = plt.subplots(figsize=(8, 4))
    fig = pd_counts.plot.bar(ax=axs, stacked=True, color=[colors[7], colors[1], colors[2]], width=.8, legend=None).get_figure()

    axs.tick_params(axis='x', labelrotation=45, length=0)
    axs.set_xticklabels(tools, horizontalalignment='right', fontsize=14)
    axs.set_xlabel(None)

    # axs.yaxis.set_major_locator(MaxNLocator(integer=True))

    h, l = axs.get_legend_handles_labels()
    axs.set_ylabel('#genome bins', fontsize=16)

    # axs.grid(which='major', linestyle=':', linewidth='0.5')
    # axs.grid(which='minor', linestyle=':', linewidth='0.5')

    ph = [plt.plot([], marker='', ls='')[0]]
    handles = ph + h

    labels = ['Contamination < 10%           Completeness  '] + l
    # bbox_to_anchor = (0.49, 1.02)
    y_values = (pd_counts['>90%'] + pd_counts['>70%'] + pd_counts['>50%']).tolist()
    for i, v in enumerate(y_values):
        axs.text(i - counts_pos[0], v + counts_pos[1], str(v), color='black', fontweight='bold')
    bbox_to_anchor = (0.47, 1.02)

    lgd = plt.legend(handles, labels, bbox_to_anchor=bbox_to_anchor, columnspacing=.5, loc=8, borderaxespad=0., handlelength=1, frameon=False, fontsize=14, ncol=5)

    # plt.subplots_adjust(hspace=0.6, wspace=0.2)

    fig.savefig(os.path.join(output_dir, output_file + '.pdf'), dpi=100, format='pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, output_file + '.png'), dpi=200, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
    exit()
    # fig.savefig(os.path.join(output_dir, output_file + '.png'), dpi=200, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, output_file + '.pdf'), dpi=100, format='pdf', bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, output_file + '.png'), dpi=200, format='png', bbox_inches='tight')
    plt.close(fig)


def main():
    output_dir = '/home/fmeyer/cami2/ismb2020/'

    input_dir = '/home/fmeyer/cami2/ismb2020/marine/amber_marine/'
    labels = 'A1,A2,B1,B2,B3,C1,C2,D1,E1,F1,G1'.split(',')
    pd_all = pd.DataFrame()
    for label in labels:
        pd_tool = pd.read_csv(os.path.join(input_dir, 'genome', label, 'metrics_per_bin.tsv'), sep='\t')
        pd_tool['Tool'] = label
        pd_all = pd.concat([pd_all, pd_tool])
    plot_counts(pd_all, labels, output_dir, 'bin_counts_marine', get_number_of_hq_bins_by_score, (.28, 2))

    input_dir = '/home/fmeyer/cami2/ismb2020/marine/amber_marine_megahit/'
    labels = 'A1,A2,B2,B3,B4,B5,B7,B8,B9,D1,E1,E2,F1,G1,J1'.split(',')
    pd_all = pd.DataFrame()
    for label in labels:
        pd_tool = pd.read_csv(os.path.join(input_dir, 'genome', label, 'metrics_per_bin.tsv'), sep='\t')
        pd_tool['Tool'] = label
        pd_all = pd.concat([pd_all, pd_tool])
    plot_counts(pd_all, labels, output_dir, 'bin_counts_marine_megahit', get_number_of_hq_bins_by_score, (.38, 2))

    input_dir = '/home/fmeyer/cami2/ismb2020/strain_madness/amber_strain_madness/'
    labels = 'A1,A2,B1,B2,B3,B4,C1,C2,D1,E1,E2,E3,F1,G1,H1,H2,H3,I1'.split(',')
    pd_all = pd.DataFrame()
    for label in labels:
        pd_tool = pd.read_csv(os.path.join(input_dir, 'genome', label, 'metrics_per_bin.tsv'), sep='\t')
        pd_tool['Tool'] = label
        pd_all = pd.concat([pd_all, pd_tool])
    plot_counts(pd_all, labels, output_dir, 'bin_counts_strain_madness', get_number_of_hq_bins_by_score, (.3, 0.5))

    input_dir = '/home/fmeyer/cami2/ismb2020/strain_madness/amber_strain_madness_megahit/'
    labels = 'B2,B3,B4,B5,B6,B7,B8,D1,E1,E2,F1,G1,J1'.split(',')
    pd_all = pd.DataFrame()
    for label in labels:
        pd_tool = pd.read_csv(os.path.join(input_dir, 'genome', label, 'metrics_per_bin.tsv'), sep='\t')
        pd_tool['Tool'] = label
        pd_all = pd.concat([pd_all, pd_tool])
    plot_counts(pd_all, labels, output_dir, 'bin_counts_strain_madness_megahit', get_number_of_hq_bins_by_score, (.25, .1))


if __name__ == "__main__":
    main()