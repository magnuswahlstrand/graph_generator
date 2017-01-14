import os
import json
import matplotlib
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    matplotlib.use('Agg')
import matplotlib.pyplot as plt


import matplotlib.pyplot as plt
import numpy as np
import argparse
from argparse import RawTextHelpFormatter


BAR_WIDTH = 0.5

class GraphGenerator():

    def __init__(self, args):

        is_single_data_set = type(args.data) == type({})
        
        # Wrap args.data in a list, if only 1 item
        if is_single_data_set:
            args.data = [args.data]


        if args.subplot:
            number_of_subplots = len(args.data)
        else:
            number_of_subplots = 1

        f, axes = plt.subplots(number_of_subplots, sharex=args.sharex, sharey=args.sharey)
    
        if number_of_subplots == 1:
            axes = [axes]
        
        i = 0
        for line_number, d in enumerate(args.data):

            if 'label' in d:
                label = d['label']
            else:
                label = 'Data %i' % (line_number + 1)


            # Type of graph
            if d['type'] == 'bar':
                axes[i].bar(d['x'],d['y'], BAR_WIDTH,label=label,color=d['color'], **d['kwargs'])

                # Set labels and position of labels
                if d.has_key('x_ticks'):
                    axes[i].set_xticks(d['x_ticks_pos'])
                    axes[i].set_xticklabels(d['x_ticks'])
                    plt.xticks(rotation=d['x_ticks_rotate'])
            else:
                axes[i].plot(d['x'],d['y'],label=label,color=d['color'],**d['kwargs'])
                
            
            if args.subplot:
                i += 1

        if len(args.title) == 1:        
            plt.suptitle(args.title[0], fontsize=18); 

        for i, ax in enumerate(axes):
            # Set the plot title

            # Only print title once, if only 1 has been specified
            if len(args.title) == 1:
                pass
            # Number of titles have capped, don't print a title
            elif i >= len(args.title):
                pass 
            else:
                ax.set_title(args.title[i])
            
            # Set plot x label
            if args.xlabel:
                ax.set_xlabel(args.xlabel)
            
            # Set plot y label
            if args.ylabel:
                ax.set_ylabel(args.ylabel)

            # Set x-axis range
            if args.xlim:
                ax.set_xlim( args.xlim )            

            # Set y-axis range
            if args.ylim:
                ax.set_ylim( args.ylim )            


            ax.legend()
            ax.grid(True)

            self.filename = args.filename

        plt.tight_layout()

        
    def save_and_show(self, args):
        plt.savefig(self.filename)
        
        if not args.no_show:
            plt.show()


def get_bar_formats(y):
    # Create an array for the position of the bar labels (x_ticks)5
    ind = np.arange(len(y))
    ind = ind + BAR_WIDTH / 2.0
    return ind

def get_filler_x_from_y(y):
    return range(len(y))

def get_rotatation_angle(x_ticks):

    max_tick_length = max(map(len, x_ticks ))
    # Rotate if ticks are longer than 5 characters

    if max_tick_length <= 5:
        return 0
    elif max_tick_length <= 8:
        return 45
    else:
        return 75


def parse_opt(s):
    parsed_opt = json.loads(s)
    return parsed_opt

valid_graph_types = ['bar','line']
types_help_text = "%s or %s" % (",".join(valid_graph_types[:-1]), valid_graph_types[-1])
def parse_graph_type(s):
    
    if not s in valid_graph_types:
        raise argparse.ArgumentTypeError("Graph type has to be one of the following: %s" % types_help_text)
    else:
        return s

def parse_data_args(s):
    #try:   
        
        data = s.split(';')
        if len(data) == 1:
            y = data[0]
            return {'y': [float(i) for i in y.split(',')],
                    'x': range(len(y.split(',')))}
        elif len(data) == 2:
            y, x = data
            try:
                # Try y0;x0
                #   y0 = float
                #   x0 = float
                return {'x': [float(i) for i in x.split(',')],
                        'y': [float(i) for i in y.split(',')]}
                
            except ValueError as e:

                y0 = [float(i) for i in y.split(',')]
                x_ticks = x.split(',')

                # If y and x are same length, assume 2nd value is ment as x-values

                if len(y0) == len(x_ticks):
                    # Both are not number series
                    # Try y0;x_labels
                    #   y0 = float
                    #   x_labels = strings
                    return { 
                        'x': get_filler_x_from_y(y0),
                        'y': y0,
                        'x_ticks' : x_ticks,
                        'x_ticks_pos' : get_bar_formats(y0),
                        'x_ticks_rotate' : get_rotatation_angle(x_ticks),
                        }

                else:
                    # Assume y0;label
                    #   y0 = float
                    #   label = strings

                    label = x
                    return {
                        'x': get_filler_x_from_y(y0),
                        'y': y0, 
                        'label': label}

                
        elif len(data) == 3:
            y, x, label = data

            y0 = [float(i) for i in y.split(',')]
            try:
                # Try y0;x0;label
                #   y0 = float
                #   x0 = float
                #   label = strings
                return {'x': [float(i) for i in x.split(',')],
                        'y': y0,
                        'label' : label }
            
            except ValueError as e:
                # Try y0;x_labels;label
                #   y0 = float
                #   x_labels = strings
                #   label = string
                x_ticks = x.split(',')
                return {
                        'y': y0,
                        'x': get_filler_x_from_y(y0),
                        'x_ticks' : x_ticks,
                        'x_ticks_pos' : get_bar_formats(y0),
                        'x_ticks_rotate' : get_rotatation_angle(x_ticks),
                        'label' : label }

            



        else:
            raise argparse.ArgumentTypeError("Input should either be --data-set \"y0\", --data-set \"y0;x0\", --data-set \"y0;TITLE\" or --data-set \"y0;x0;TITLE\"")
    #except:
    #    raise argparse.ArgumentTypeError("Input should either be --data-set \"y0\", --data-set \"y0;x0\", --data-set \"y0;TITLE\" or --data-set \"y0;x0;TITLE\"")

# graph_generator.py --title "Magnus plot" --labels "x" --data 1,3,1,3,1;1,2,3,4,5 
if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)

    parser.add_argument('--xlabel', action="store", required=False)
    parser.add_argument('--ylabel', action="store", required=False)

    parser.add_argument('--xlim', nargs=2, type=float)
    parser.add_argument('--ylim', nargs=2, type=float)
    
    parser.add_argument('--title', action='append', required=False, default=[])

    parser.add_argument('--data-set', dest="data", type=parse_data_args, required=True, action="append",
                        help='y and x and TITLE separated by \';\' \nMultiple --data-set is allowed\nExamples:\t\n--data-set 1,4,5;6,1,2;THROUGHPUT\t\n--data-set 1,4,5;delay\t\n--data-set 1,4,5;6,1,2\t\n\n')

    parser.add_argument('-c','--color', action="append")
    parser.add_argument('-o','--options', action="append", type=parse_opt)


    parser.add_argument('--filename', "-f", action='store', required=False, default='graph.png' ,
        help='Filename to save. Default: graph.png')

    parser.add_argument('--graph-type', dest="type", type=parse_graph_type, default=None, action="append", help=types_help_text)
    
    parser.add_argument('--sharex', action="store_true", required=False, default=False)
    parser.add_argument('--sharey', action="store_true", required=False, default=False)
    parser.add_argument('--sub-plots', dest="subplot", action="store_true", required=False, help="Divides data sets over multiple graphs")

    # Don't show graph upon creation
    parser.add_argument('--no-show', dest="no_show", action="store_true", required=False, default=False)

    args = parser.parse_args()

    for i, d in enumerate(args.data):
        if args.color and len(args.color) > i:
            d['color'] = args.color[i]
        else:
            d['color'] = 'blue'

        if args.type and len(args.type) > i:
            d['type'] = args.type[i]
        else:
            d['type'] = 'line'

        if args.options and len(args.options) > i:
            d['kwargs'] = args.options[i]
        else:
            d['kwargs'] = {}


        print d

    #print(args.data)

    small_plot = GraphGenerator(args)
    small_plot.save_and_show(args)
    
    