# graph_generator.py

A simple python tool for linux to generate graphs using the Matplotlib. 
Purpose was to create a simple way of generating graphs using one liners in the terminal


### Help
```bash
usage: graph_generator.py [-h] [--xlabel XLABEL] [--ylabel YLABEL]
                          [--xlim XLIM XLIM] [--ylim YLIM YLIM]
                          [--title TITLE] --data-set DATA
                          [--filename FILENAME] [--graph-type TYPE] [--sharex]
                          [--sharey] [--sub-plots]

optional arguments:
  -h, --help            show this help message and exit
  --xlabel XLABEL
  --ylabel YLABEL
  --xlim XLIM XLIM
  --ylim YLIM YLIM
  --title TITLE
  --data-set DATA       y and x and TITLE separated by ';' 
                        Multiple --data-set is allowed
                        Examples:	
                        --data-set 1,4,5;6,1,2;THROUGHPUT	
                        --data-set 1,4,5;delay	
                        --data-set 1,4,5;6,1,2	
                        
  --filename FILENAME, -f FILENAME
                        Filename to save. Default: graph.png
  --graph-type TYPE     bar or line
  --sharex
  --sharey
  --sub-plots           Divides data sets over multiple graphs

```
### Examples

**Example: Simple graph***
```bash
# Data for the y-axis
DATA="10,8,15,17,1"
python graph_generator.py --data-set "$DATA"

display graph.png
```

![Example 1](/images/example_1.png)

**Example: Bar chart***

```bash
# Get number of lines per file in this repo
#   find * -type f  - list all files (not directories) in repo
#   xargs wc -l     - get number of lines in files
#   tr -s ' '		- turn multiple spaces into single ones
#   cut -f2 -d" "   - remove file name
# 	tr "\n" ","		- turn line feed seperated list into commas separated list
FILE_CHARS=$(find * -type f | xargs wc -l | tr -s ' ' | cut -f2 -d" " | tr "\n" ",")

#Remove trailing comma
FILE_CHARS=${FILE_CHARS::-1}

#Set nice title for the graph
TITLE="# of lines in file"

# Create graph
python graph_generator.py --data-set "$FILE_CHARS;$TITLE" --filename images/bar_graph.png --graph-type bar

display images/bar_graph.png

```
![Bar graph](/images/bar_graph.png)


**Example: Bar chart (improved)**
Add text labels on the x-axis
```bash
# Get number of lines per file in this repo
FILE_CHARS=$(find * -type f | xargs wc -l | grep -v total | tr -s ' ' | cut -f2 -d" " | tr "\n" ",")
FILE_NAMES=$(find * -type f | tr '\n' ',')

#Remove trailing comma
FILE_CHARS=${FILE_CHARS::-1}
FILE_NAMES=${FILE_NAMES::-1}

#Set nice title for the graph
TITLE="# of lines in file"

# Create graph
python graph_generator.py --data-set "$FILE_CHARS;$FILE_NAMES;$TITLE" --filename images/bar_graph2.png --graph-type bar

display images/bar_graph2.png


```
![Bar graph](/images/bar_graph2.png)

**Example: option/kwargs
Pass any options to your graph that is supported by matplotlib. [Available Line options here]

```bash
python graph_generator.py --data-set "115,22,113;My score,Your score,Her score;Ugly boxes" -o '{"linewidth":10, "linestyle": "dashed", "facecolor":"green"}' -c b --graph-type bar --data-set "50,60,40;Ugly line" --graph-type line -o '{"linewidth":5, "linestyle": ":", "dash_joinstyle" : "round"}'

```

![Bar graph](/images/ugly_graph.png)


[available line options here]: http://matplotlib.org/api/lines_api.html#matplotlib.lines.Line2D

## Possible improvements
* ~~Use strings on the x-axis instead of numbers~~
* ~~Being able to specify color, width and type of line or bar charts~~
* ~~Combine multiple type of charts~~
* Automatically choose colors of bar charts
* Add bars side by side
* Allow other type of charts

