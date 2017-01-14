# graph_generator.py

A simple python tool for linux to generate graphs using the Matplotlib. 
Purpose was to create a simple way of generating graphs using one liners in the terminal


### Help
```bash
usage: graph_generator.py [-h] [--xlabel XLABEL] [--ylabel YLABEL]
                          [--xlim XLIM XLIM] [--ylim YLIM YLIM]
                          [--title TITLE] --data-set DATA
                          [--filename FILENAME] [--sharex] [--sharey]
                          [--sub-plots]

optional arguments:
  -h, --help            show this help message and exit
  --xlabel XLABEL
  --ylabel YLABEL
  --xlim XLIM XLIM
  --ylim YLIM YLIM
  --title TITLE
  --data-set DATA       y and x and label separated by ';' examples: (--data-
                        set 1,4,5;6,1,2;THROUGHPUT --data-set 1,4,5;delay,
                        --data-set 1,4,5;6,1,2). Multiple --data-set is
                        allowed.
  --filename FILENAME, -f FILENAME
                        Filename to save. Default: graph.png
  --sharex
  --sharey
  --sub-plots

```
### Examples

Examples:
```bash
# Data for the y-axis
DATA="10,8,15,17,1"
python graph_generator.py --data-set "$DATA"
```
Output:

![Example 1](/images/example_1.png)


## Possible improvements
* Use strings on the x-axis instead of numbers
* Automatically choose colors of bar charts
* Being able to specify color, width and type of line or bar charts
* Allow other type of charts
