import pandas as pd
import matplotlib.pyplot as plt
import originpro as op

df  = pd.read_csv('TGIdVd_E31-M2.csv', skiprows=259)
df.drop(df.columns[0], axis=1, inplace=True)
df[' ID'] = df[' ID'] * 1E6


# df.head()

df[' forward'] = True

df.loc[(df.index >= 101) & (df.index <= 201), ' forward'] = False
df.loc[(df.index >= 303) & (df.index <= 403), ' forward'] = False
df.loc[(df.index >= 505) & (df.index <= 605), ' forward'] = False
df.loc[(df.index >= 707) & (df.index <= 807), ' forward'] = False
df.loc[(df.index >= 909) & (df.index <= 1009), ' forward'] = False
df.loc[(df.index >= 1111) & (df.index <= 1211), ' forward'] = False
df.loc[(df.index >= 1313) & (df.index <= 1413), ' forward'] = False

df_new = pd.pivot_table(df,columns=' VG',values=[' ID'],index=[' VD',' forward'])

df_sorted = df_new.sort_values(by=[' forward',' VD'])

wks=op.new_sheet()
wks.from_df(df_sorted)