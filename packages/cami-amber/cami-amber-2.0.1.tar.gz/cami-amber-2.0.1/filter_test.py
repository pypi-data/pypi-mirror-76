import pandas as pd

x = open('/home/fmeyer/tmp/x.txt', 'r')

xpd = pd.DataFrame()

for line in x:
    list_rank = []
    list_all_val = []
    list_filtered_val = []
    if line.strip() == '':
        tool = x.readline().strip()
        list_tool = [tool] * 7
    for i in range(0, 7):
        rank = x.readline().strip()
        all_val = float(x.readline().strip())
        filtered_val = float(x.readline().strip())
        # print(tool, rank, all_val, filtered_val)
        list_rank.append(rank)
        list_all_val.append(all_val)
        list_filtered_val.append(filtered_val)
    ypd = pd.DataFrame({'tool': list_tool, 'rank': list_rank, 'all_val': list_all_val, 'filtered_val': list_filtered_val})
    print(tool)
    xpd = pd.concat([xpd, ypd])

# for (tool, rank), aa in xpd.groupby(['tool', 'rank']):
#     print(tool, rank)
#     print(aa)
for rank, aa in xpd.groupby(['rank']):
    print(rank)
    print(aa)
    aa.to_csv('/home/fmeyer/tmp/xpd_' + rank + '.tsv', sep='\t')

# xpd.to_csv('/home/fmeyer/tmp/xpd.tsv', sep='\t')


x.close()

# filter_tail_percentage = 1
# x = pd.read_csv('/home/fmeyer/tmp/x_species.tsv', sep='\t', index_col='TAXID')
# list1 = x.index[x.loc[:, 'total_length'] > 0]
# print(x.loc[list1]['total_length'].mean())
#
# x['total_length_pct'] = x['total_length'] / x['total_length'].sum()
# x.sort_values(by='total_length', inplace=True)
# x['cumsum_length_pct'] = x['total_length_pct'].cumsum(axis=0)
# x['precision_bp'].mask(x['cumsum_length_pct'] <= filter_tail_percentage / 100, inplace=True)
# x['precision_seq'].mask(x['precision_bp'].isna(), inplace=True)
# x.drop(columns=['cumsum_length_pct', 'total_length_pct'], inplace=True)
#
# list1 = x.index[(x.loc[:, 'total_length'] > 0) & x['precision_bp'].isna()]
# print(x.loc[list1]['total_length'].mean())
