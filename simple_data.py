from numpy import loadtxt, linspace, ones, convolve
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot
from scipy import signal

# Lecture des fichiers scv
data4936A = loadtxt(open("data/SW_4936_speech_rate_A.csv", "rb"), delimiter="\t", skiprows=1)
data4936B = loadtxt(open("data/SW_4936_speech_rate_B.csv", "rb"), delimiter="\t", skiprows=1)
data2005A = loadtxt(open("data/SW_2005_speech_rate_A.csv", "rb"), delimiter="\t", skiprows=1)
data2005B = loadtxt(open("data/SW_2005_speech_rate_B.csv", "rb"), delimiter="\t", skiprows=1)

# Fonction de lissage des données
def smooth(data):
    b, a = signal.butter(10, 0.1)
    zi = signal.lfilter_zi(b, a)
    z, _ = signal.lfilter(b, a, data, zi=zi*data[0])
    z2, _ = signal.lfilter(b, a, z, zi=zi*z[0])
    return signal.filtfilt(b, a, data)

# Création graphique discussion 1
graph1 = figure(width=1000, height=300, y_range=[0,3.5], title="Speech rate discussion 4936")
graph1.line(data4936A[:,2], data4936A[:,1], legend="Locuteur A",
            line_width=1, color="blue", alpha=0.5, line_dash="10 4")
graph1.line(data4936A[:,2], smooth(data4936A[:,1]), legend="Locuteur A lissé",
            line_width=2, color="blue")
graph1.line(data4936B[:,2], data4936B[:,1], legend="Locuteur B",
            line_width=1, color="red", alpha=0.5, line_dash="10 4")
graph1.line(data4936B[:,2], smooth(data4936B[:,1]), legend="Locuteur B lissé",
            line_width=2, color="red")

# Création graphique discussion 2
graph2 = figure(width=1000, height=300, y_range=[0,3.5], title="Speech rate discussion 2005")
graph2.line(data2005A[:,2], data2005A[:,1], legend="Locuteur A",
            line_width=1, color="blue", alpha=0.5, line_dash="10 4")
graph2.line(data2005A[:,2], smooth(data2005A[:,1]), legend="Locuteur A lissé",
            line_width=2, color="blue")
graph2.line(data2005B[:,2], data2005B[:,1], legend="Locuteur B",
            line_width=1, color="red", alpha=0.5, line_dash="10 4")
graph2.line(data2005B[:,2], smooth(data2005B[:,1]), legend="Locuteur B lissé",
            line_width=2, color="red")

# Affichage des grapgiques
graphs = gridplot([[graph1],[graph2]])
show(graphs)

