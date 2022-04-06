# Import your libraries
import pandas as pd
import numpy as np

# Start writing code
df = players_results

#Method_1
df1 = df.sort_values(['player_id', 'match_date'], ascending = True)
df1['pre'] = df1.groupby('player_id')['match_result'].shift(1)
df1['cpr'] = np.where((df1['match_result'] == 'L') & (df1['pre'] == ('W')) | ((df1['match_result'] == 'W') & (df1['pre'] == 'W')), False, True)

df1['w_grp'] = df1.groupby('player_id')['cpr'].cumsum()

df2 = df1[~df1.cpr]

#df3 = df2.groupby(['player_id', 'w_grp'])['match_date'].count().reset_index(name = 'streak')
df2['streak'] = df2.groupby(['player_id', 'w_grp'])['match_date'].transform('count')

#Find ID wiht the longest streak
df2[df2['streak'] == df2.streak.max()]

#Get the all players with their longest streak
df3 = df2.pivot_table(columns = 'player_id', values = 'streak', aggfunc = 'max').melt()

##Method_2
df1 = df.groupby('player_id', as_index = False).agg({'match_result': 'sum'})

df1['streak']= df1.match_result.str.split('L')

df2 = df1.explode('streak')

df2['n'] = df2.streak.apply(lambda x: len(x))

df2[df2.n == df2.n.max()]

##Method_3
m = df['match_result'].str.upper().ne('W')
t = m.cumsum()
r = m.cumsum()[~m]
s = m.cumsum()[~m].groupby(df['player_id']).value_counts().reset_index(level =1, drop = True)

df3 = s.reset_index()

df3[df3.match_result == df3.match_result.max()]

df4 = s.agg({'player_id': 'idxmax', 'longest_winningstreak':'max'}).to_frame(0).T

#df1['new'] = df1.match_result.apply(lambda x: x.replace('', ',')[1:-1])
#str = 'wwllwwllw'
#str[1:-1]
