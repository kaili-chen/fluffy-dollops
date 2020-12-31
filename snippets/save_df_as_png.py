from matplotlib.font_manager import FontProperties
import numpy as np

columns = list(year_flights.columns)

col_colours = plt.cm.BuPu( 0.1)

# Plot bars and create text labels for the table
cell_text = []
for row in range(year_flights.shape[0]):
    cell_text.append(list(year_flights.iloc[row]))
#     print(list(year_flights.iloc[row]))


ax = plt.gca()
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
plt.box(on=None)

ax = plt.table(cellText=cell_text, cellLoc='center', colLabels=columns, colLoc='center', loc='center')

for (row, col), cell in ax.get_celld().items():
    if (row == 0):
        cell.set_text_props(fontproperties=FontProperties(weight='bold'))

ax.scale(1, 1.5)

plt.title('yearly flight passengers', va='top')

plt.savefig('table.png')
