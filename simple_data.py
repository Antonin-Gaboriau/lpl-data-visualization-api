from os import listdir
from numpy import *
from scipy import signal, interpolate
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot

#Lecture des metadonnées du corpus
def read_metadata():
    for file_name in listdir("data"):
        file_info = file_name.replace(".csv", "").split("_")
        if (file_info[1] == "metadata"):
            data_format = {'names': ("id", "id_conv","id_caller","id_speaker","id_topic",
                                     "sex","age","geography","level_study"),
                           'formats': ('i', 'i', 'U64', 'i', 'U64', 'U64', 'i', 'U64', 'i')}
            return loadtxt(open("data/"+file_name, "rb"), delimiter="\t", skiprows=1, dtype=data_format)
    print ("metadonnées introuvable")
def find_info(metadata, conv, caller):
    for line in metadata:
        if line["id_conv"] == int(conv) and line["id_caller"] == caller:
            return line
    print("aucune donnée ne correspond à l'id_conv "+conv+" et caller "+caller+" dans les métadonnées" )
    
# Lecture des données du corpus depuis tous les fichiers du répertoire "data"
def read_corpus_conversations():
    corpus = {}
    for file_name in listdir("data"):
        file_info = file_name.replace(".csv", "").split("_")
        if (file_info[1] != "metadata"):
            if (file_info[1] not in corpus.keys()):
                corpus[file_info[1]]={}
            corpus[file_info[1]][file_info[4]]=loadtxt(open("data/"+file_name, "rb"), delimiter="\t", skiprows=1)
    return corpus

# Recherche et lecture des données d'une conversation
def read_conversation(id_conv):
    conversation = {}
    for file_name in listdir("data"):
        file_info = file_name.replace(".csv", "").split("_")
        if file_info[1] == id_conv:
            conversation[file_info[4]]=loadtxt(open("data/"+file_name, "rb"), delimiter="\t", skiprows=1)
    return conversation

# Lissage des données   
def smooth(x,y,window_len):
    window=hanning(window_len)
    z=r_[y[window_len-1:0:-1],y,y[-2:-window_len-1:-1]]
    y2=convolve(window/window.sum(),z,mode='valid')
    smoothed = interpolate.CubicSpline(linspace(0, int(x[-1]),y2.size), y2)
    return {'x':arange(0, x[-1],0.5),'y':smoothed(arange(0, x[-1],0.5))}

# Création de la visualisation du speech rate d'une conversation
def get_conversation_plot(id_conv, conversation):
    plot = figure(width=800, height=250, y_range=[0,3.5], title="Speech rate evolution conversation number "+id_conv)
    color_palette = ["red", "blue", "green", "purple", "yellow"]
    color_number = 0

    for speaker, data in conversation.items():

        smoothed_data = smooth(data[:,2], data[:,1],int(data[-1,2]/20))

        plot.line(data[:,2], data[:,1], legend="Speaker "+speaker,
                  line_width=1, color=color_palette[color_number%9], alpha=0.5, line_dash="10 4")
        plot.line(smoothed_data['x'], smoothed_data['y'], legend="Smooth Speaker "+speaker,
                  line_width=2, color=color_palette[color_number%9])
        color_number += 1

    plot.legend.click_policy="hide"
    return plot   

# Création de la visualisation du speech rate moyenne entre entre les donnée passées en paramètres
# aligné en chaque pourcentage des conversation
def get_average_plot(data):
    plot = figure(width=800,height=250, y_range=[0.5,2.5 ])
    ys = []
    for d in data:
        x=[]
        for index, value in enumerate(d[:,2]):
            x.append(value * 100 / d[-1,2])
        s = smooth(x, d[:,1], int(d[-1,2]/20))
        ys.append(s['y'])
        plot.line(s['x'],s['y'], line_width=2, color="grey", alpha = 0.4)
    a = mean(ys, axis=0)
    plot.line(linspace(0,100, a.size), a, legend="Average", line_width=2, color="blue")
    return plot

# Visualisation des conversations passées en paramètre
# si aucun paramètre : visualisation de toutes les conversation du corpus
def display_conversation(*conversations):
    grid = []
    if (len(conversations) == 0):
        corpus=read_corpus_conversations()
        for id_conv, conversation in corpus.items():
            if (id_conv != "metadata"):
                grid.append(get_conversation_plot(id_conv, conversation))
    else:
        for id_conv in conversations:
            conversation = read_conversation(id_conv)
            if (len(conversation) == 0):
                print("La conversation "+id_conv+" n'existe pas")
            else:
                grid.append(get_conversation_plot(id_conv, conversation))           
    show(gridplot(grid, ncols=1))
   
# Visualisation de la de la moyenne du speechrate sur le pourcentage du temps
# de chaque données sélectionné en paramètres selon leur conversation et où locuteurs
def display_average_data(conv=[], speakers=[]):
    metadata = read_metadata();
    selected_data = []
    for file_name in listdir("data"):
        file_info = file_name.replace(".csv", "").split("_")
        if file_info[1] != "metadata":
            id_caller = find_info(metadata, file_info[1], file_info[-1])[3]
            if (len(conv) == 0 or int(file_info[1]) in conv) and (len(speakers) == 0 or id_caller in speakers):
                selected_data.append(loadtxt(open("data/"+file_name, "rb"), delimiter="\t", skiprows=1))
    show(get_average_plot(selected_data))
    

