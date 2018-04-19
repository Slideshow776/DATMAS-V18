import sys
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import numpy as np

sys.path.append('../Backend')
from NPRA import NPRA_weekly

workbook = load_workbook('../Backend/NPRA/Ukestrafikk 2013-2017 utvalgte punkter Bergen - Stavanger - Oslo.xlsx')
worksheet = workbook['Oslo']

NPRA_Y = NPRA_weekly.NPRA_weekly(
    '../Backend/NPRA/Ukestrafikk 2013-2017 utvalgte punkter Bergen - Stavanger - Oslo.xlsx'
    ).getData(2017, worksheet)

fig, ax1 = plt.subplots()

# flu year 2017
NIPH_Y = np.array([8017*.222, 7420*.172, 6402*.165, 6038*.163, 6059*.147, 5648*.136, 4912*.143, 5102*.152, 4494*.134, 4237*.115, 4024*.115, 3800*.109, 3753*.106, 3477*.101, 2017*.098, 2865*.082, 3090*.072, 2450*.077, 2888*.104, 2807*.103, 3039*.092, 3103*.055, 2052*.04, 2034*.025, 1526*.029, 1143*.017, 1097*.021, 1168*.014, 794*.014, 514*.016, 557*.014, 591*.017, 644*.014, 994*.011, 201*.03, 585*.015, 317*.016, 281*.004, 497*.004, # this is week 1-39
    2349*.006, 3007*.006, 3219*.007, 3782*.009, 4140*.013, 4387*.014, 4472*.025, 4539*.022, 4671*.037, 5235*.054, 5722*.084, 6367*.149, 4438*.223]) # this is week 40-52

x = []
for i in range(52):
    x.append(i)

x = np.array(x)
print(x)
y1 = np.array(NPRA_Y)
y2 = np.array(NIPH_Y)

ax1.plot(x, y1, color='#4286f4')
ax1.set_ylabel('This is NPRA_Y', color='#4286f4')
ax1.tick_params('y', colors='#4286f4')

ax2 = ax1.twinx()
ax2.plot(x, y2, color='#872323')
ax2.set_ylabel('This is NIPH_Y', color='#872323')
ax2.tick_params('y', colors='#872323')

fig.tight_layout()
plt.show()