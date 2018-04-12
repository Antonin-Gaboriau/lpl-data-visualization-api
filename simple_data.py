from numpy import *
from scipy import signal, interpolate
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot

# Lecture des fichiers scv 
corpus = [{"A":loadtxt(open("data/SW_2001_speech_rate_A.csv", "rb"), delimiter="\t", skiprows=1),
           "B":loadtxt(open("data/SW_2001_speech_rate_B.csv", "rb"), delimiter="\t", skiprows=1)},
          {"A":loadtxt(open("data/SW_2005_speech_rate_A.csv", "rb"), delimiter="\t", skiprows=1),
           "B":loadtxt(open("data/SW_2005_speech_rate_B.csv", "rb"), delimiter="\t", skiprows=1)},
          {"A":loadtxt(open("data/SW_4936_speech_rate_A.csv", "rb"), delimiter="\t", skiprows=1),
           "B":loadtxt(open("data/SW_4936_speech_rate_B.csv", "rb"), delimiter="\t", skiprows=1)}]  

# Pour le lissage des données
def smooth(x,y,window_len):
    window=hanning(window_len)
    z=r_[y[window_len-1:0:-1],y,y[-2:-window_len-1:-1]]
    y2=convolve(window/window.sum(),z,mode='valid')
    smoothed = interpolate.CubicSpline(linspace(0, int(x[-1]),y2.size), y2)
    return {'x':arange(0, x[-1],0.5),'y':smoothed(arange(0, x[-1],0.5))}


grid = []
# Visualisation des données :
for discussion in corpus:
    sA = smooth(discussion["A"][:,2], discussion["A"][:,1],12)
    sB = smooth(discussion["B"][:,2], discussion["B"][:,1],12)
        
    plot = figure(width=800, height=250, y_range=[0,3.5], title="Speech rate")
    plot.line(discussion["A"][:,2], discussion["A"][:,1], legend="Speaker A",
                line_width=1, color="blue", alpha=0.5, line_dash="10 4")
    plot.line(sA['x'], sA['y'], legend="Smooth Speaker A ",
                line_width=2, color="blue")
    plot.line(discussion["B"][:,2], discussion["B"][:,1], legend="Speaker B",
                line_width=1, color="red", alpha=0.5, line_dash="10 4")
    plot.line(sB['x'], sB['y'], legend="Smooth Speaker B",
                line_width=2, color="red")
    grid.append(plot)
    
show(gridplot(grid, ncols=1))
