""" Python 3 API for interactive oral data visualization with Bokeh
Coding : utf-8
Docstrings in reStructuredText style
Develop in internship in Laboratoire Parole et Langage (lpl-aix.fr)
22/06/2018 V1.0 by Antonin Gaboriau (antonin.gaboriau@hotmail.fr)
"""

from os import listdir, rename
from numpy import *
from scipy import signal, interpolate
from bokeh.plotting import figure, show
from bokeh.models import Legend, ColumnDataSource, HoverTool
from bokeh.models.widgets import Button
from bokeh.layouts import gridplot
from bokeh.io import output_notebook
from ipywidgets import interact, HBox
from re import match, search
from ipywidgets import widgets
from collections import defaultdict
from inspect import getsource
import warnings
warnings.simplefilter('ignore')
output_notebook()


class VisualizationData:
    """ Class to read data and be visualize by Display's methods"""
    
    def __init__(self, directory, conversations=[], speakers=[], corpus_format="minimalist", **format_details):
        """ VisualizationData Constructor
        
        Read csv files that matchs with conversation and speaker filters, then store readed data and metadata
        
        :param directory: Name of directory (with path) where the scv files are
        :type directory: string
        
        :param conversations: To be read, a data file must have one of the conversation ID from this optionnal list
        unless the list is empty or undefined.
        :type conversations: list of string
        
        :param speakers: To be read, a data file must have one of the speaker ID from this optionnal list
        unless the list is empty or undefined.
        :type speakers: list of string
        
        :param corpus_format: Predefined format for data reading, including all format details from next parameter. 
                              By default the format is set to a minimalist format.
        :type corpus_format: string 'SW' or 'CID'
        
        :param \**format_detail: List of named parameters, 8 possible :
        * data_columns: List of data files columns names in the right order. Must include at least 'time' and 'values'
                        type: list of string
        * metadata_columns: List of metadata file columns names in the right order.
                            Must include at least 'corpus', 'data_type', 'id_conv' and 'id_speaker'
                            type: list of string
        * data_delimiter: Data file delimiter between columns
                          type: string
        * metadata_delimiter: Metadata file delimiter between columns
                              type: string
        * data_head_lines: Head lines number in data files
                           type: int
        * metadata_head_lines: Head lines number in metadata file
                               type: int
        * file_name: List of informations (that are also in metadata file) with wich data files name are makes. 
                     type: list of string
        * file_name_delimiter: Delimiter between information in data files name
                               type: string
        """
        
        # Initialize predefined formats
        if corpus_format == "CID":
            format = { 'data_columns'       : ['corpus', 'id_speaker', 'fill', 'time',
                                               'time_stop', 'values', 'fill'],
                       'metadata_columns'   : ['id_conv','id_speaker','data_type','corpus'],
                       'data_delimiter'     : ",",
                       'metadata_delimiter' : "\t",
                       'data_head_lines'    : 0,
                       'metadata_head_lines': 1,
                       'file_name'          : ['id_speaker'],
                       'file_name_delimiter': " " }
        elif corpus_format == "SW":
            format = { 'data_columns'       : ['id_line','values', 'time'],
                       'metadata_columns'   : ['id','id_conv','id_caller','id_speaker','id_topic',
                                               'sex','age','geography','level_study','corpus','data_type'],
                       'data_delimiter'     : "\t",
                       'metadata_delimiter' : "\t",
                       'data_head_lines'    : 1,
                       'metadata_head_lines': 1,
                       'file_name'          : ['corpus','id_conv','data_type','id_caller'],
                       'file_name_delimiter': "_" }
        else: # minimalist  format
            format = { 'data_columns'       : ['time', 'values'],
                       'metadata_columns'   : ['id_conv','id_speaker','data_type','corpus'],
                       'data_delimiter'     : "\t",
                       'metadata_delimiter' : "\t",
                       'data_head_lines'    : 0,
                       'metadata_head_lines': 0,
                       'file_name'          : ['id_speaker'],
                       'file_name_delimiter': "" }
        for info in format:
            if info in format_details:
                format[info] = format_details[info]
                
        # Read the metadata
        for file_name in listdir(directory):
            if match(".*metadata.*\.csv$",file_name):
                metadata_file = open(directory+"/"+file_name, "r")
                self.metadata = genfromtxt(metadata_file, skip_header=format['metadata_head_lines'],
                                   encoding=None, delimiter=format['metadata_delimiter'],
                                  names=format['metadata_columns'], dtype=None)
                break

        self.data = []
        cpt = 0
        
        # Read files which match with the filters
        for line in self.metadata:
            if ((len(conversations) == 0 or str(line['id_conv']) in conversations)
                and (len(speakers) == 0 or str(line['id_speaker']) in speakers)):
                cpt += 1
                to_add = {'data':{},}
                for info_key in format['metadata_columns']:
                    to_add[info_key] = line[info_key]
                file_name = line[format['file_name'][0]]
                if len(format['file_name']) > 1:
                    for i in range(1, len(format['file_name'])):
                        info = line[format['file_name'][i]]
                        file_name = file_name + format['file_name_delimiter'] + str(info)
                file_name += ".csv"
                to_add['data'] = genfromtxt(open(directory + "/" + file_name), encoding=None, 
                                            skip_header=format['data_head_lines'], 
                                            delimiter=format['data_delimiter'],
                                            names=format['data_columns'], dtype=None)
                self.data.append(to_add)
        
        print(str(cpt)+" data files have been read")

        
        

class Plot:
    """ Plot class for visualization """

    def __init__(self, smoothing_window, points_number):
        """ Plot constructor
        
        Create the Plot object by setting up its smoothing_window and points_number member values
        
        :param smoothing_window: used window length to smooth data
        :type smoothing_window: int 
        
        :param points_number: points number to display
        :type points_number: int
        """
        self.smoothing_window = smoothing_window
        self.points_number = points_number        
        
    def smooth(x, y, window_len, points_number):
        """ Smoothing function
        
        Change x and y data into new smoothed data
        
        :param x: x values of raw data
        :type x: array like
        
        :param y: y values of raw data
        :type y:array like
        
        :param window_len: used window length to smooth data
        :type window_len: int
        
        :param points_number: points number for the smoothed values
        :type points_number: int
        
        :returns: smoothed x and y list of values
        :rtype: dict of {string : list of float}
        """
        if window_len is None:
            window_len = int(x[-1]/15)
        if points_number is None:
            points_number = 200
        
        # First step, get the values closer together by averaging each values with a window of hann :
        window = hanning(window_len)
        if len:
            wider_data = r_[y[window_len-1:0:-1],y,y[-2:-window_len-1:-1]]
        else:
            wider_data = [y]
        new_y=convolve(window/window.sum(),wider_data,mode='valid')

        # Second step, create new points to smooth the curve :
        smooth_function = interpolate.CubicSpline(linspace(0, int(x[-1]),new_y.size), new_y)
        smooth_x = linspace(0, x[-1], points_number)
        smooth_y = smooth_function(smooth_x)
    
        return {'x':smooth_x, 'y':smooth_y}


class AveragePlot (Plot):
    """ Extending Plot class for average visualization """
    
    def __init__(self, title, smoothing_window, points_number, meta_info):
        """ AveragePlot constructor
        
        :param title: Graphic title
        :type title: string
        
        :param smoothing_window: Window length used to smooth data
        :type smoothing_window: int
        
        :param points_number: Displayed points number
        :type points_number: int
        
        :param meta_info: Meta_informations names for hover tool
        :type meta_info: list of string
        """
        Plot.__init__(self, smoothing_window, points_number)
        informations = []
        for info in meta_info:
            informations.append((info,"@"+info))
        hover = HoverTool(tooltips=informations)
        self.plot = figure(width=950,height=300, title=title,
                           tools=["box_zoom", "pan", hover, "wheel_zoom", "reset", "save"],
                           x_axis_label="conversation progress (%)", y_axis_label=title)
        self.src = defaultdict(list)

    def add_data(self, data):
        """ Add data to display souce data, after change x values in percent and smooth y values
        
        :param data: Data to add
        :type data: dict of {string : string or array like}:
        """
        x=[]
        for row_x in data['data']['time']:
            x.append(row_x * 100 / data['data']['time'][-1])
        smoothed_values = Plot.smooth(x, data['data']['values'], self.smoothing_window, self.points_number)
        self.src['x'].append(smoothed_values['x'])
        self.src['y'].append(smoothed_values['y'])
        for info_key in data:
            if info_key != "data":
                self.src[info_key].append(data[info_key])
    
    def get_plot (self):
        """ Draw lines and legends from data source on plot and return it
        
        :returns: Bokeh plot to display
        :rtype: Bokeh.plot 
        """
        if len(self.src.keys()) == 0:
            self.plot.text(x=100, y=100, text=["Aucune donnée ne correspond aux filtres"])
            return self.plot
        self.average = mean(self.src['y'], axis=0)
        self.patch_x = linspace(0, 100, self.average.size)
        patch_y1 = self.average - std(self.src['y'], axis=0)
        patch_y2 = self.average + std(self.src['y'], axis=0)
        self.patch_y = hstack((patch_y1, patch_y2[::-1]))
        source = ColumnDataSource(self.src)
        g1 = self.plot.multi_line(source=source, xs='x', ys='y', line_width=1, color="grey", alpha = 0.4)
        g2 = self.plot.line(linspace(0, 100, self.average.size), self.average, line_width=4, color="blue")
        g3 = self.plot.patch(hstack((self.patch_x, self.patch_x[::-1])), self.patch_y,
                             fill_alpha=0.2, fill_color="blue", line_color="blue")
        legend = Legend(items=[("All data",[g1]), ("Average",[g2]), ("Standard deviation",[g3])],
                        location=(20,20))
        self.plot.add_layout(legend, 'right')
        self.plot.legend.click_policy="hide"
        return self.plot
    

class ConversationPlot (Plot):    
    """ Extending Plot class for average visualization"""
    
    def __init__(self, id_conv, smoothing_window, points_number, color_palette):
        """ AveragePlot constructor
        
        :param id_conv: Conversation ID for this plot
        :type id_conv: string or int
        
        :param smoothing_window: Window length used to smooth data
        :type smoothing_window: int
        
        :param color_palette: List of colors used for drawed lines.
        Colors can be set by Python predefined classic colours like 'blue, 'red', ...
        or with hexadecimal code like '#ff0000' for example.
        :type color_palette: list of string
        """
        Plot.__init__(self, smoothing_window, points_number)
        self.plot = figure(width=950, height=250, title="Conversation "+str(id_conv),
                           x_axis_label="time (s)")
        self.color_palette = color_palette
        self.legend_items = [("Raw data",[]),("Averages",[])]
        self.color_number = 0
 
    def add_data (self, speaker, data):
        """ Draw raw, smooth and average lines on the plot
        
        :param speaker: Speaker ID of data 
        :type speaker: string
        
        :param data: Data to add informations, including time and values
        :type data: dict of {string : array like or string}
        """
        color=self.color_palette[self.color_number%len(self.color_palette)]
        average = mean(data['values'])
        smoothed_data = Plot.smooth(data['time'], data['values'],
                                    self.smoothing_window, self.points_number)
        g1 = self.plot.line(data['time'], data['values'],
                            alpha=0.2, line_dash="10 4", line_width=1, color=color)
        g2 = self.plot.cross(data['time'], data['values'],
                             line_width=1, alpha=0.3, size=10, color=color)
        g3 = self.plot.line(smoothed_data['x'], smoothed_data['y'],
                            line_width=3, color=color)
        g4 = self.plot.line([0,data['time'][-1]], [average, average],
                            line_width=1, line_dash="20 3", color=color)
        self.legend_items[0][1].append(g1)
        self.legend_items[0][1].append(g2)
        self.legend_items[1][1].append(g4)
        self.legend_items.append(("Smooth Speaker "+speaker, [g3]))
        self.color_number += 1
        
    def get_plot (self):
        """ Return the plot after add the legend on it
        
        :returns: Bokeh plot to display
        :rtype: Bokeh.plot
        """
        legend = Legend(items=self.legend_items)
        self.plot.add_layout(legend, 'right')
        self.plot.legend.click_policy="hide"
        return self.plot

    
    
    
    
class Display():
    """ Abstract class (there is no object of this class) for visualization functions """
    
    @staticmethod
    def average(vdata, smoothing_window=50, filters={}, interactive=False, output_visibility=False):
        """ Display the average evolution of all vdata data
      
        :param vdata: VisualisationData object including data (and metadata) to visualize
        :type vdata: VisualisationData
        
        :param smoothing_window: Smoothness in percent
        :type smoothing_window: int in range (5, 100)
        
        :param filters: Dynamic filters value.
                        A dictionary with a metadata columns names for keys and string or range for values
        :type filters: dict of {string : string or tuple of (int, int)}
        
        :param interactive: Display interactive filters  widgets if True. False by default.
        :type interactive: boolean
        
        :param output_visibility: Display widgets for export if True. False by default.
        :type output_visibility: boolean 
        """
        
        plot = AveragePlot(vdata.data[1]['data_type'], smoothing_window, 120, vdata.metadata.dtype.names)
        
        if 'output' not in globals(): 
            global output
            output = {}
            
        # add on plot data which match with dynamic filters
        for data in vdata.data:
            if filters is None:
                plot.add_data(data)
                continue
            correct = True
            for filter_name, filter_value in filters.items():
                if type(filter_value) == tuple:
                    if data[filter_name] < filter_value[0] or data[filter_name] > filter_value[1]:
                        correct = False
                elif filter_value != " " and data[filter_name] != filter_value:
                    correct = False
            if correct:
                plot.add_data(data)    
                
        # set dynamic filters widgets
        def update(smoothness=50, **args):
            lens=0
            for d in vdata.data:
                lens += len(d['data']['time'])
            smoothing_window = int((lens/len(vdata.data))*smoothness/100)
            Display.average(vdata, smoothing_window=smoothing_window, filters=args, output_visibility=True)
        if interactive:
            filters_string = "smoothness=widgets.IntSlider(description=u'smoothness'," 
            filters_string += "min=3, max=100, value=30, continuous_update=False)"
            for key in vdata.metadata.dtype.names:
                if type(vdata.metadata[key][0]) == int32:
                    minimum = str(min(vdata.metadata[key]))
                    maximum = str(max(vdata.metadata[key]))
                    filters_string += ", " + key + " = widgets.IntRangeSlider(description=u'" + key + "', "
                    filters_string += "min=" + minimum + ", max=" + maximum + ", "
                    filters_string += "value=[" + minimum + ", " + maximum + "], "
                    filters_string += "continuous_update=False)"
                else:
                    filters_string += ", " + key + " = widgets.Dropdown(options=[' '" 
                    for option in set(vdata.metadata[key]):
                        filters_string += ", '" + option + "'"
                    filters_string += "], value=' ', description=u'" + key + "', continuous_update=False)"
            eval("interact(update, " + filters_string + ")")
            
        else:
            show(plot.get_plot())
            
            # set output widgets for export
            if output_visibility:
                name_output = widgets.Text(placeholder='Curent filtered data name')
                add_output = widgets.Button(description='Add to output')
                clear_output = widgets.Button(description='Clear output')
                def add(button):
                    global output
                    plot.get_plot()
                    output[name_output.value] = {'avg':plot.average, 'patch_x':plot.patch_x,
                                                 'patch_y':plot.patch_y}    
                    print("output contient " + str(len(output)) + " élements")
                def clear(button):
                    global output
                    output = {}
                    print("output est vide")
                add_output.on_click(add)
                clear_output.on_click(clear)
                display(HBox([name_output, add_output, clear_output]))
            
    @staticmethod
    def conversation(vdata, smoothing_window=50, points_number=None, linked=False, interactive=False,
                     color_palette = ["red", "blue", "green", "purple", "yellow"]):
        """Display vdata conversations with every speakers data (raw, smooth and average) for each plot
        
        :param vdata: VisualizationData object including data (and metadata) to visualize
        :type vdata: VisualizationData
        
        :param smoothing_window: Smoothness in percent
        :type smoothing_window: int in range (5, 100)
        
        :param points_number: Points number by plots lines to display 
        :type points_number: int
        
        :param linked: Link plots through x and y ranges if True. False by default
        :type linked: boolean
        
        :param interactive: Display dynamic smoothness widget if True. False by default.
        :type interactive: boolean
        
        :param color_palette: Colors used for drawn lines, each speaker his color
                              They can be set by Python predefined classic colours like 'blue, 'red', ...
                              or with hexadecimal code like '#ff0000' for example.
        :type color palette: list of string
        """
        
        grid = []
        
        # Build conversation by assembling the data
        conversations = {}
        for d in vdata.data:
            if d['id_conv'] not in conversations:
                conversations[d['id_conv']] = {}
            if 'id_caller' in d:
                conversations[d['id_conv']][d['id_caller']] = d
            elif 'id_speaker' in d:
                conversations[d['id_conv']][d['id_speaker']] = d
                
        # Create and add each conversation plots to the grid layout
        lens=[]
        for conv_data in conversations.values():
            for data in conv_data.values():
                lens.append(len(data['data']['time']))
        smoothness = int((sum(lens)/len(lens)*smoothing_window/250))
        for conv_id, conv_data in conversations.items():
            conv = ConversationPlot(conv_id, smoothness, points_number, color_palette)
            for speaker, data in conv_data.items():
                conv.add_data(speaker, data['data'])  
            grid.append(conv.get_plot())
        
        # Link plots if required
        if linked == True:
            for i in range(1, len(grid)):
                grid[i].x_range = grid[0].x_range
                grid[i].y_range = grid[0].y_range
        
        # Display the plot
        def update(smoothing_window=30, points_number=100):
            Display.conversation(vdata, smoothing_window=smoothing_window, points_number=points_number)
        if interactive:
            interact(update, smoothing_window=(5,100), points_number=(3, 150))
        else:
            show(gridplot(grid, ncols=1))
            
            
    @staticmethod
    def comparison(elements, color_palette = ["red", "blue", "green", "purple", "yellow"]):
        """Display comparison between every filtered data exported in Display.convesation() output
        
        :param elements: Filtered data to compare
        :type elements: Display.conversation() output ( dict of {string : dict {string : list of float}} ) 
                
        :param color_palette: Colors used for drawn lines, can be set with hexadecimal code like '#ff0000' for example
                              or with Python predefined classic colours like 'blue, 'red', ...
        :type color_palette: list of string
        """
        plot = figure(width=950,height=300)
        color_iterator = 0
        legend_items = []
        for name, data in elements.items():
            color = color_palette[color_iterator%len(color_palette)]
            g1 = plot.line(linspace(0, 100, data['avg'].size), data['avg'], line_width=5, color=color)
            g2 = plot.patch(hstack((data['patch_x'], data['patch_x'][::-1])), data['patch_y'],
                                 fill_alpha=0.1, fill_color=color, line_color=color)
            legend_items.append((name + " average",[g1]))
            legend_items.append((name + " standard deviation",[g2]))
            color_iterator += 1
        plot.add_layout(Legend(items=legend_items), 'right')
        plot.legend.click_policy="hide"
        show(plot)        
        
        
    @staticmethod  
    def aggregation(*args, smoothing_window = 30, color_palette = ["green", "blue", "red"]):
        """Display two data aggregation with defined operation in parameters
        
        :param \*args: list of two unamed arguments
        (not directly two different arguments to be able to use getsource(operation) later)
          * vdata: VisualizationData object including two data (and metadata)
                   type: VisualizationData 
          * operation: Operation between two data. Differnece is lambda a,b: a-b , for example
                       type: lambda function
       
        :param smoothing_window: Smoothness in percent
        :type smoothing_window: int in range (5, 100)
        
        :param color_palette: Colors used for drawn lines, can be set with hexadecimal code like '#ff0000' for example
                              or with Python predefined classic colours like 'blue, 'red', ...
        :type color_palette: list of string
        """
        vdata, operation = args 
        
        if len(vdata.data) != 2:
            print("2 données sont demandées, pas " + str(len(vdata.data)))
            return
        plot = figure(width=950,height=300)
        legend_items = []
        color_iterator = 0
        len_avg = (len(vdata.data[0]['data']['time']) + len(vdata.data[1]['data']['time'])) / 2
        smoothness = int(len_avg / 2 * smoothing_window / 90)
        smoothed_data = []
        for d in vdata.data:
            x = []
            for row_x in d['data']['time']:
                x.append(row_x * 100 / d['data']['time'][-1])
            smoothed_data.append(Plot.smooth(x, d['data']['values'], smoothness, 120))
        g1 = plot.line(smoothed_data[0]['x'], smoothed_data[0]['y'], alpha= 0.7, color=color_palette[0])
        g2 = plot.line(smoothed_data[1]['x'], smoothed_data[1]['y'], alpha= 0.7, color=color_palette[1])
        ga = plot.line(linspace(0,100,120), operation(smoothed_data[0]['y'], smoothed_data[1]['y']),
                       color = color_palette[2], line_width = 5)
        legend_items.append(("speaker " + str(vdata.data[0]['id_speaker']), [g1]))
        legend_items.append(("speaker " + str(vdata.data[1]['id_speaker']), [g2]))
        op = search(":.+,",getsource(operation))[0].replace(":","").replace(",","")
        legend_items.append((op, [ga]))
        plot.add_layout(Legend(items=legend_items), 'right')
        plot.legend.click_policy="hide"
        show(plot)   


