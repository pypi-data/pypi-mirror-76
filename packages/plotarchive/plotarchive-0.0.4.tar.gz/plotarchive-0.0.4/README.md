# plotarchive
Plotarchive is a simple package which aims to assist plotters remeber what code created which figure.
We aim to eliminate the problem where the code you used to make a figure is lost or deleted. 
Plotarchive serialises the data used to make the figure, along with the generating function, and the entire code of the project.

To save your plot, wrap it in a function and apply the plotarchive.archive decorator. Plotarchive will save all the necessary information to recreate your plot.
```python
import plotarchive
import matplotlib.pyplot as plt

@plotarchive.archive(file='myplot.pa')
def plot(x, y, title):
    plt.figure()
    plt.plot(x,y)
    plt.title(title)
    plt.show()

plot([1,2,3], [1,2,3])
```  
To re-generate your plot: 
```python
import plotarchive

plotarchive.extract('myplot.pa')
```




