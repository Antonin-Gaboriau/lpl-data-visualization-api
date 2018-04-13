from os import listdir
from numpy import *
from scipy import signal, interpolate
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot


# Importation des données de tous les fichiers du corpus dans répertoire "data" :

corpus = {}
for file_name in listdir("data"):
    file_info = file_name.replace(".csv", "").split("_")
    if (file_info[1] == "metadata"):
        data_format = {'names': ("id", "id_conv","id_caller","id_speaker","id_topic","sex","age","geography","level_study"),
                       'formats': ('i', 'i', 'U64', 'i', 'U64', 'U64', 'i', 'U64', 'i')}
        corpus["metadata"]=loadtxt(open("data/"+file_name, "rb"), delimiter="\t", skiprows=1, dtype=data_format)
    else:
        if (file_info[1] not in corpus.keys()):
            corpus[file_info[1]]={}
        corpus[file_info[1]][file_info[4]]=loadtxt(open("data/"+file_name, "rb"), delimiter="\t", skiprows=1)


# Pour le lissage des données :
        
def smooth(x,y,window_len):
    window=hanning(window_len)
    z=r_[y[window_len-1:0:-1],y,y[-2:-window_len-1:-1]]
    y2=convolve(window/window.sum(),z,mode='valid')
    smoothed = interpolate.CubicSpline(linspace(0, int(x[-1]),y2.size), y2)
    return {'x':arange(0, x[-1],0.5),'y':smoothed(arange(0, x[-1],0.5))}


# Visualisation des données :
    
grid = []
color_palette = ["red", "blue", "green", "purple", "yellow"]

for id_conv, conversation in corpus.items():
    if (id_conv != "metadata"):
        plot = figure(width=800, height=250, y_range=[0,3.5], title="Speech rate evolution conversation number "+id_conv)
        color_number = 0
        
        for speaker, data in conversation.items():
               
                smoothed_data = smooth(data[:,2], data[:,1],int(data[-1,2]/20))
            
                plot.line(data[:,2], data[:,1], legend="Speaker "+speaker,
                            line_width=1, color=color_palette[color_number%9], alpha=0.5, line_dash="10 4")
                plot.line(smoothed_data['x'], smoothed_data['y'], legend="Smooth Speaker "+speaker,
                            line_width=2, color=color_palette[color_number%9])
                color_number += 1

        plot.legend.click_policy="hide"
        grid.append(plot)
    
show(gridplot(grid, ncols=1))
