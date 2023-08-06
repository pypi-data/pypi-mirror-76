from src.utils import labels as utils_labels
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import os
import pandas as pd


# def test(output_dir, counts):
#     available_tools = list(map(str, range(sum(counts))))
#
#     cmaps = ['Blues_r', 'Reds_r', 'Greens_r', 'Purples_r', 'Greys_r', 'YlOrBr_r', 'cool_r']
#
#     colors_list = []
#     for i, count in enumerate(counts):
#         print(i, count)
#         for color in plt.get_cmap(cmaps[i])(np.linspace(.1, .7, count+1))[:-1]:
#             colors_list.append(tuple(color))
#
#     colors_iter = iter(colors_list)
#     circles = [Line2D([], [], markeredgewidth=0.0, linestyle="None", marker="o", markersize=10, markerfacecolor=next(colors_iter)) for label in available_tools]
#
#     fig = plt.figure(figsize=(0.5, 0.5))
#     fig.legend(circles, available_tools, loc='center', frameon=False, ncol=1, handletextpad=0.1)
#     fig.savefig(os.path.join(output_dir, 'colors.pdf'), dpi=100, format='pdf', bbox_inches='tight')
#     plt.close(fig)


def plot_summary(counts, df_results, tools, output_dir, rank, file_name, xlabel, ylabel):
    cmaps = ['Blues_r', 'Reds_r', 'Greens_r', 'Purples_r', 'Wistia', 'Greys_r', 'Oranges', 'cool_r', 'pink', 'GnBu_r']
    colors_list = []
    for i, count in enumerate(counts):
        if isinstance(count, list):
            print(cmaps[i], 'X')
            colors = plt.get_cmap(cmaps[i])(np.linspace(.3, .7, count[-1] + 1))[:-1]
            for j, color in enumerate(colors, start=1):
                if j in count:
                    colors_list.append(tuple(color))
        elif count != 0:
            print(cmaps[i])
            colors = plt.get_cmap(cmaps[i])(np.linspace(.3, .7, count + 1))[:-1]
            for color in colors:
                colors_list.append(tuple(color))

    df_mean = df_results.groupby(utils_labels.TOOL).mean().reindex(tools)

    # binning_type = df_results[utils_labels.BINNING_TYPE].iloc[0]

    # if len(df_mean) > len(colors_list):
    #     raise RuntimeError("Plot only supports 29 colors")

    fig, axs = plt.subplots(figsize=(5, 4.5))

    # force axes to be from 0 to 100%
    axs.set_xlim([0.0, 1.0])
    axs.set_ylim([0.0, 1.0])

    for i, (tool, df_row) in enumerate(df_mean.iterrows()):
        axs.errorbar(df_row[utils_labels.AVG_PRECISION_BP], df_row[utils_labels.AVG_RECALL_BP], xerr=df_row['avg_precision_bp_var'], yerr=df_row['avg_recall_bp_var'],
                     fmt='o',
                     ecolor=colors_list[i],
                     mec=colors_list[i],
                     mfc=colors_list[i],
                     capsize=3,
                     markersize=8)

    # turn on grid
    # axs.minorticks_on()
    axs.grid(which='major', linestyle=':', linewidth='0.5')
    # axs.grid(which='minor', linestyle=':', linewidth='0.5')

    axs.tick_params(axis='x', labelsize=12)
    vals = axs.get_yticks()
    axs.set_yticklabels(['{:3.0f}'.format(x * 100) for x in vals], fontsize=11)

    if rank:
        file_name = rank + '_' + file_name
        plt.title(rank)
        ylabel = ylabel.replace('genome', 'taxon')

    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.tight_layout()
    # fig.savefig(os.path.join(output_dir, file_name + '.eps'), dpi=100, format='eps', bbox_inches='tight')

    colors_iter = iter(colors_list)
    circles = []
    for x in range(len(df_mean)):
        circles.append(Line2D([], [], markeredgewidth=0.0, linestyle="None", marker="o", markersize=11, markerfacecolor=next(colors_iter)))
    lgd = plt.legend(circles, tools, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., handlelength=0, frameon=False, fontsize=12)

    # fig.savefig(os.path.join(output_dir, binning_type, file_name + '.pdf'), dpi=100, format='pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, file_name + '.png'), dpi=200, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, file_name + '.pdf'), dpi=200, format='pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.close(fig)


def main():
    output_dir = '/home/fmeyer/tmp/test_old/'
    df_results = pd.read_csv('/home/fmeyer/tmp/test_old/results.tsv',
                             sep='\t')
    labels = 'B2,B3,B4,B5,B6,B7,B8,D1,E1,E2,F1,G1,J1'.split(',')
    counts = [0, [2, 3, 4, 5, 6, 7, 8], 0, 1, 2, 1, 1, 0, 0, 1]
    file_name = '_strain_madness_megahit'

    plot_summary(counts, df_results, labels, output_dir, None,
                 'avg_purity_completeness_bp' + file_name,
                 'Average purity per bin (%)',
                 'Average completeness per genome (%)')
    exit()



    output_dir = '/home/fmeyer/cami2/ismb2020/'
    # test(output_dir, [3, 3, 3, 3, 3, 3, 3])

    df_results = pd.read_csv('/home/fmeyer/cami2/ismb2020/marine/amber_marine/results.tsv', sep='\t')
    labels = 'A1,A2,B1,B2,B3,C1,C2,D1,E1,F1,G1'.split(',')
    counts = [2, 3, 2, 1, 1, 1, 1]
    file_name = '_marine'

    plot_summary(counts, df_results, labels, output_dir, None,
                 'avg_purity_completeness_bp' + file_name,
                 'Average purity per bin (%)',
                 'Average completeness per genome (%)')

    df_results = pd.read_csv('/home/fmeyer/cami2/ismb2020/marine/amber_marine_megahit/results.tsv', sep='\t')
    labels = 'A1,A2,B2,B3,B4,B5,B7,B8,B9,D1,E1,E2,F1,G1,J1'.split(',')
    counts = [2, [2, 3, 4, 5, 7, 8, 9], 0, 1, 2, 1, 1, 0, 0, 1]
    file_name = '_marine_megahit'

    plot_summary(counts, df_results, labels, output_dir, None,
                 'avg_purity_completeness_bp' + file_name,
                 'Average purity per bin (%)',
                 'Average completeness per genome (%)')

    df_results = pd.read_csv('/home/fmeyer/cami2/ismb2020/strain_madness/amber_strain_madness/results.tsv', sep='\t')
    labels = 'A1,A2,B1,B2,B3,B4,C1,C2,D1,E1,E2,E3,F1,G1,H1,H2,H3,I1'.split(',')
    counts = [2, 4, 2, 1, 3, 1, 1, 3, 1]
    file_name = '_strain_madness'

    plot_summary(counts, df_results, labels, output_dir, None,
                 'avg_purity_completeness_bp' + file_name,
                 'Average purity per bin (%)',
                 'Average completeness per genome (%)')

    df_results = pd.read_csv('/home/fmeyer/cami2/ismb2020/strain_madness/amber_strain_madness_megahit/results.tsv', sep='\t')
    labels = 'B2,B3,B4,B5,B6,B7,B8,D1,E1,E2,F1,G1,J1'.split(',')
    counts = [0, [2, 3, 4, 5, 6, 7, 8], 0, 1, 2, 1, 1, 0, 0, 1]
    file_name = '_strain_madness_megahit'

    plot_summary(counts, df_results, labels, output_dir, None,
                 'avg_purity_completeness_bp' + file_name,
                 'Average purity per bin (%)',
                 'Average completeness per genome (%)')


if __name__ == "__main__":
    main()