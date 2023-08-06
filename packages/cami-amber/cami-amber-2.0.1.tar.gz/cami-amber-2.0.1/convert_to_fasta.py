#!/usr/bin/env python3

from src.utils import load_data
from src import binning_classes
from src.utils import argparse_parents
import argparse
from Bio import SeqIO
import os


def get_labels(labels, bin_files):
    if labels:
        labels_list = [x.strip() for x in labels.split(',')]
        if len(set(labels_list)) != len(bin_files):
            print('Number of different labels does not match the number of binning files. Please check parameter -l, --labels.')
            exit(1)
        return labels_list
    tool_id = []
    for bin_file in bin_files:
        tool_id.append(bin_file.split('/')[-1].split('.binning')[0])
    return tool_id


def main():
    parser = argparse.ArgumentParser(description="AMBER: Assessment of Metagenome BinnERs", parents=[argparse_parents.PARSER_MULTI2])
    parser.add_argument('-o', '--output_dir', help="Directory to write the results to", required=True)
    parser.add_argument('-f', '--fasta', help="FASTA file", required=True)
    args = parser.parse_args()

    options = binning_classes.Options(filter_tail_percentage=None,
                                      genome_to_unique_common=None,
                                      filter_keyword=None,
                                      min_length=None,
                                      rank_as_genome_binning=None,  # args.rank_as_genome_binning,
                                      output_dir=None,
                                      min_completeness=None,
                                      max_contamination=None)

    labels = get_labels(args.labels, args.bin_files)

    sample_id_to_queries_list, sample_ids_list = load_data.load_queries(args.gold_standard_file, args.bin_files, labels,
                                                                            options, options)

    print('loading fasta')
    record_dict = SeqIO.to_dict(SeqIO.parse(args.fasta, "fasta"))
    print('done loading')
    # print(record_dict['aaa'].seq)

    for sample_id in sample_id_to_queries_list:
        for query in sample_id_to_queries_list[sample_id]:
            label = 'gs' if query.label == 'Gold standard' else query.label
            print(label)
            for bin_id, df_group in query.df.groupby('BINID'):
                f = open(os.path.join(args.output_dir, label, str(bin_id) + '.fasta'), 'w')
                for sequence_id in df_group['SEQUENCEID'].tolist():
                    f.write('>' + sequence_id + '\n')
                    f.write(str(record_dict[sequence_id].seq) + '\n')
                f.close()


if __name__ == "__main__":
    main()
