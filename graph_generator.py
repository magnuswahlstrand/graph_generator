import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import argparse


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
            print(i)

            if 'label' in d:
                label = d['label']
            else:
                label = 'Data %i' % (line_number + 1)


            # Type of graph
            if args.type == 'bar':
                axes[i].bar(d['x'],d['y'],label=label)
            else:
                axes[i].plot(d['x'],d['y'],label=label)
                
            
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
        plt.show()

valid_graph_types = ['bar','line']
types_help_text = "%s or %s" % (",".join(valid_graph_types[:-1]), valid_graph_types[-1])
def parse_graph_type(s):
    
    if not s in valid_graph_types:
        raise argparse.ArgumentTypeError("Graph type has to be one of the following: %s" % types_help_text)
    else:
        return s

def parse_data_args(s):
    try:   
        
        data = s.split(';')
        
        if len(data) == 1:
            y = data[0]
            return {'y': [float(i) for i in y.split(',')],
                    'x': range(len(y.split(',')))}
        elif len(data) == 2:
            y, x = data
            try:
                return {'x': [float(i) for i in x.split(',')],
                        'y': [float(i) for i in y.split(',')]}
                
            except ValueError as e:
                return {'label': x,
                        'x': range(len(y.split(','))),
                        'y': [float(i) for i in y.split(',')]}
                
        elif len(data) == 3:
            y, x, label = data
            return {'x': [float(i) for i in x.split(',')],
                    'y': [float(i) for i in y.split(',')],
                    'label' : label }
        else:
            raise argparse.ArgumentTypeError("Input should either be --data-set \"y0\", --data-set \"y0;x0\", --data-set \"y0;TITLE\" or --data-set \"y0;x0;TITLE\"")
    except:
        raise argparse.ArgumentTypeError("Input should either be --data-set \"y0\", --data-set \"y0;x0\", --data-set \"y0;TITLE\" or --data-set \"y0;x0;TITLE\"")

# graph_generator.py --title "Magnus plot" --labels "x" --data 1,3,1,3,1;1,2,3,4,5 
if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--xlabel', action="store", required=False)
    parser.add_argument('--ylabel', action="store", required=False)

    parser.add_argument('--xlim', nargs=2, type=float)
    parser.add_argument('--ylim', nargs=2, type=float)
    
    parser.add_argument('--title', action='append', required=False, default=[])

    parser.add_argument('--data-set', dest="data", type=parse_data_args, required=True, action="append",
                        help='y and x and TITLE separated by \';\' examples: (--data-set 1,4,5;6,1,2;THROUGHPUT --data-set 1,4,5;delay, --data-set 1,4,5;6,1,2). Multiple --data-set is allowed.')

    parser.add_argument('--filename', "-f", action='store', required=False, default='graph.png' ,
        help='Filename to save. Default: graph.png')

    parser.add_argument('--graph-type', dest="type", type=parse_graph_type, default=None, help=types_help_text)
    
    parser.add_argument('--sharex', action="store_true", required=False, default=True)
    parser.add_argument('--sharey', action="store_true", required=False, default=False)
    parser.add_argument('--sub-plots', dest="subplot", action="store_true", required=False, help="Divides data sets over multiple graphs")

    args = parser.parse_args()
    print(args.data)

    small_plot = GraphGenerator(args)
    small_plot.save_and_show(args)
    
    