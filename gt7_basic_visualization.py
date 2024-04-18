import plotly.graph_objects as go
import pandas as pd
import glob

folder_path = 'data/*csv'

track_bounds = dict(
        xaxis=dict(range=[-4000,4000]),
        yaxis=dict(range=[-4000,4000]),
        zaxis=dict(range=[-4000,4000])
)

def createline(filename, xOffset, yOffset, zOffset, color):
    df = pd.read_csv(filename,sep=',')
    return go.Scatter3d(x=-df['posX'] + xOffset, y=df['posZ'] + yOffset, z=df['posY'] + zOffset, name=filename, marker=dict(size=1), line=dict(width=2, color=color))

def load_files(folder_path):
    data_folder = glob.glob(folder_path)
    files = []
    for filename in data_folder:
        files.append(filename)
    return files

files = []
files += load_files(folder_path)

fig = go.Figure()

fig.update_layout(scene=track_bounds)

for filename in files:
    fig.add_trace(createline(filename,0,0,0,'blue'))

fig.show()

