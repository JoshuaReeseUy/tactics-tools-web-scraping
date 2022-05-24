import pandas as pd
import matplotlib.pyplot as plt


def unit_summation (df, preferences):
    names = df['name'].tolist()
    preferences = preferences.loc[preferences['name'].isin(names)]
    df_counts = preferences.iloc[:,1:].apply(pd.Series.value_counts).fillna(0)
    df_counts['Sum'] = df_counts.sum(axis=1)
    return df_counts.sort_values(by=['Sum', 'unit0'], ascending=False)['Sum']


def unit_comparison(df1, df2, preferences):
    counts_1 = unit_summation(df1, preferences)
    counts_2 = unit_summation(df2, preferences)
    return pd.concat([counts_1, counts_2], axis=1).fillna(0)


def make_bar_plot(df):
    columns = df.columns
    series = pd.Series(data=df[columns[0]].tolist(), index=df[columns[1]].tolist())
    plot = series.plot(kind='barh')
    plot.invert_yaxis()
    plt.tight_layout()
    return plot


units = pd.read_json('units.json')
players = pd.read_json('players.json')
profiles = pd.read_json('profiles.json')
preferences = pd.read_json('unit_choices.json')
unit_counts = preferences.iloc[:,1:].apply(pd.Series.value_counts).fillna(0)
unit_counts['Sum'] = unit_counts.sum(axis=1)



# unit data preprocessing
duplicate_indices = [i for i in range(60, 120)]
for index in duplicate_indices:
    units.at[index, 'patch'] = '12.7'
old = units[units["patch"] == '12.7']
current = units[units["patch"] != '12.7']
df = pd.merge(old, current, on="unit")
df['playrate_x'] = df['playrate_x'] * (100/8)
df['playrate_y'] = df['playrate_y'] * (100/8)
df['playrate_change'] = df['playrate_y'] - df['playrate_x']
df['placement_change'] = df['placement_y'] - df['placement_x']



avg_playrate_change_top = df.nlargest(n=10, columns=['playrate_change'])[['playrate_change', 'unit']]
avg_placement_change_top = df.nlargest(n=10, columns=['placement_change'])[['placement_change', 'unit']]
avg_playrate_change_bottom = df.nsmallest(n=10, columns=['playrate_change'])[['playrate_change', 'unit']]
avg_placement_change_bottom = df.nsmallest(n=10, columns=['placement_change'])[['placement_change', 'unit']]

## profile data preprocessing
full_player_data = pd.merge(players, profiles, on='name')
full_player_data = pd.merge(full_player_data,preferences, on= "name")
df_mapping = pd.DataFrame({'grade': ['F', 'D', 'C', 'B', 'A', 'S', 'S+']})
sort_mapping = df_mapping.reset_index().set_index('grade')
del(df_mapping)

categories = ['Econ', 'Execution', 'Items', 'Flexibility', 'Compositions']
leaderboard_data = ['patch-lp', 'patch-games']
for category in categories:
    full_player_data[category + '_num'] = full_player_data[category].map(sort_mapping['index'])
del(sort_mapping)



for category in categories:
    top_10 = full_player_data.sort_values([category + '_num'], ascending=False)[['name', category]].head(10)
    bottom_10 = full_player_data.sort_values([category + '_num'], ascending=False)[['name', category]].tail(10)
    if category in ['Flexibility', 'Econ']:
        comparison = unit_comparison(top_10, bottom_10, preferences)
        comparison.columns = ['Top 10', 'Bottom 10']
        print(comparison)
for data in leaderboard_data:
    top_10 = full_player_data.sort_values([data], ascending=False)[['name',data]].head(10)
    bottom_10 = full_player_data.sort_values([data], ascending=False)[['name', data]].tail(10)

plt.style.use('fivethirtyeight')
make_bar_plot(avg_playrate_change_top)
# plt.show()
make_bar_plot(avg_playrate_change_bottom)
# plt.show()
make_bar_plot(avg_placement_change_top)
# plt.show()
make_bar_plot(avg_placement_change_bottom)
# plt.show()

