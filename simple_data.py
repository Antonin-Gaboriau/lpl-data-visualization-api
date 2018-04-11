from numpy import loadtxt, linspace, arange
from scipy import signal, interpolate
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot

# Lecture des fichiers scv
data4936A = loadtxt(open("data/SW_4936_speech_rate_A.csv", "rb"), delimiter="\t", skiprows=1)
data4936B = loadtxt(open("data/SW_4936_speech_rate_B.csv", "rb"), delimiter="\t", skiprows=1)

# Lissage des données
def smooth(x,y):
    b, a = signal.butter(10, 0.1)
    z = signal.filtfilt(b, a, y)
    cs = interpolate.CubicSpline(x, z)
    s = {'x':arange(0, 300, 0.5),
         'y':cs(arange(0, 300, 0.5))}
    return s

s4936A = smooth(data4936A[:,2], data4936A[:,1])
s4936B = smooth(data4936B[:,2], data4936B[:,1])

# Création et affichage du graphique
plot = figure(width=1000, height=300, y_range=[0,3.5], title="Speech rate discussion 4936")
plot.line(data4936A[:,2], data4936A[:,1], legend="Speaker A",
            line_width=1, color="blue", alpha=0.5, line_dash="10 4")
plot.line(s4936A['x'], s4936A['y'], legend="Smooth Speaker A ",
            line_width=2, color="blue")
plot.line(data4936B[:,2], data4936B[:,1], legend="Speaker B",
            line_width=1, color="red", alpha=0.5, line_dash="10 4")
plot.line(s4936B['x'], s4936B['y'], legend="Smooth Speaker B",
            line_width=2, color="red")

show(plot)

