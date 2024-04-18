import plotly.graph_objects as go
import pandas as pd
import glob

folder_path = 'data/*csv'

track_bounds = dict(
        xaxis=dict(range=[-4000,4000]),
        yaxis=dict(range=[-4000,4000]),
        zaxis=dict(range=[-4000,4000])
)

throttle_colorscale = [
    [0, 'rgb(255, 0, 0)'],    # Low value color (e.g., red)
    [0.5, 'rgb(255, 160, 0)'], # Medium value color (e.g., yellow)
    [1, 'rgb(0, 185, 0)']      # High value color (e.g., green)
]

def createline(filename, xOffset, yOffset, zOffset):
    df = pd.read_csv(filename,sep=',')
    color_values = df['throttle'].astype(float) - df['brake'].astype(float) / 100
    return go.Scatter3d(x=-df['posX'] + xOffset, y=df['posZ'] + yOffset, z=df['posY'] + zOffset, name=filename, marker=dict(size=1), line=dict(width=20, color=color_values, colorscale=throttle_colorscale, cmin=-1, cmax=1))

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
    fig.add_trace(createline(filename,0,0,0))

fig.show()

