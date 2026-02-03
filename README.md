# Custom Debuggers
This mini library contains two `Python` decorator functions to aid in performance debugging by displaying the evluation times of its various subcomponents in tree-like structures.
## Homebrew
The `@homebrew_debugger()` displays the line-by-line wall-clock execution time of whatever function it is attached to. As a result, this debugger is best for smaller pieces of code where individual lines may matter more. Consider the following example.

```
>>> @homebrew_debugger()
>>> def simple(delay=1.5):
>>>     a = 1
>>>     b = 2
>>>     c = a + b
>>>     d = np.array(range(100000000))
>>>     e = d ** 3.3
>>>     time.sleep(delay)
>>>     d = c * 1.0 / b
>>>     return c

- 
* /Users/username/abc.py simple()
| Line 6:  Elapsed time: 0.00s 
| Line 8:  Elapsed time: 0.00s 
| Line 9:  Elapsed time: 0.00s 
| Line 10:  Elapsed time: 0.00s 
| Line 11:  Elapsed time: 4.25s 
| Line 12:  Elapsed time: 0.74s 
| Line 13:  Elapsed time: 1.45s 
| Line 14:  Elapsed time: 0.00s 
```

You can see here that the execution time of each line is printed to the screen.

For longer pieces of code, it is helpful to exclude certain times below a `threshold`. This can simply be done with the `threshold` argument in `@homebrew_debugger()`. For example, changing the argument `@homebrew_debugger(threshold=1)` to the above code would yield the following.

```
- 
* /Users/username/abc.py simple()
| Line 11:  Elapsed time: 4.25s 
| Line 13:  Elapsed time: 1.45s 
```

Another nice aspect of this decorator is that it displays the nesting of various functions and files as they are called by one another. For example, consider another function call. 

```
>>> @homebrew_debugger()
>>> def complicated():
>>>     a = 1
>>>     nestc()
>>>     b = 2
>>>     c = a + b
>>>     nesta()
>>>     d = np.array(range(100000000))
>>>     e = d ** 3.3
>>>     time.sleep(0.75)
>>>     nestb()
>>>     d = c * 1.0 / b
>>>     return c
>>> 
>>> def nesta():
>>>     time.sleep(0.3)
>>> 
>>> def nestb():
>>>     time.sleep(1)
>>>     nesta()
>>> 
>>> def nestc():
>>>     nestb()
>>>     time.sleep(1.33)
>>> 
>>> complicated()

- 
* /Users/username/abc.py complicated()
| Line 6:  Elapsed time: 0.00s 
| Line 8:  Elapsed time: 0.00s 
| Line 9:  Elapsed time: 0.00s 
| * /Users/username/abc.py nestc()
| | Line 27:  Elapsed time: 0.00s 
| | Line 28:  Elapsed time: 0.00s 
| | * /Users/username/abc.py nestb()
| | | Line 23:  Elapsed time: 0.00s 
| | | Line 24:  Elapsed time: 0.98s 
| | | * /Users/username/abc.py nesta()
| | | | Line 20:  Elapsed time: 0.00s 
| | | - 
| | - 
| - 
| Line 10:  Elapsed time: 1.64s 
| Line 11:  Elapsed time: 0.00s 
| Line 12:  Elapsed time: 0.00s 
| * /Users/username/abc.py nesta()
| | Line 20:  Elapsed time: 0.00s 
| - 
| Line 13:  Elapsed time: 4.56s 
| Line 14:  Elapsed time: 0.75s 
| Line 15:  Elapsed time: 0.75s 
| Line 16:  Elapsed time: 0.00s 
| * /Users/username/abc.py nestb()
| | Line 23:  Elapsed time: 0.00s 
| | Line 24:  Elapsed time: 0.96s 
| | * /Users/username/abc.py nesta()
| | | Line 20:  Elapsed time: 0.00s 
| | - 
| - 
| Line 17:  Elapsed time: 0.31s 
```

## Flame Graph
The `@flamegraph_debugger()` uses a [Python implementation](https://github.com/evanhempel/python-flamegraph) of the [Flame Graph](https://www.brendangregg.com/flamegraphs.html) stack trace visualization tool which displays stack depth on the vertical axis and CPU cycles (or various other types of cycles) on the horizontal axis. For example, adding this decorator to `complicated()` would give the following.

![Alt text](./controllers_brief.svg)
<img src="./controllers_brief.svg">


A more complicated Flame Graph example from the original website is shown [here](https://www.brendangregg.com/FlameGraphs/cpu-mysql-updated.svg)
