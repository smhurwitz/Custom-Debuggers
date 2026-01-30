import desc
import inspect
import linecache
import numpy as np
import sys
import threading
import time
import traceback

def siena_debugger(func):
    def wrapper(*args, **kwargs):
        thread_2 = None
        stop_event = None
        stack_old = None

        """
        Dynamically updates a timer on the screen until `stop_event` is reached
        in the primary thread. 
        """
        def timer(stop_event, premodifier):
            start = time.perf_counter()
            while not stop_event.is_set():
                elapsed = time.perf_counter() - start
                sys.stdout.write(f"\r{premodifier} Elapsed time: {elapsed:.2f}s ")
                sys.stdout.flush()
                time.sleep(0.1)
            print()
        
        """
        This function is called by sys.settrace(tracer) each time and 
        immediately before a line of code in the primary thread is executed.
        Its role is to stop the previous timer (if it exists) and start a new 
        one. 
        """
        def tracer(frame, event, arg):
            # stop previous if not first loop                        
            nonlocal stop_event, thread_2
            if stop_event is not None:
                stop_event.set()
                thread_2.join()

            stack_new = traceback.extract_stack(frame)
            # fmt_trace = traceback.format_list([stack[-1]])[0]

            

            
            ###### -----------------------------------
            #TODO: define stacktrace_new = stack
            # extract filenamestack from old and new stacktrace, if old is None then []
            # pass to print_tree

            #### ------------------------------------


            lines, start_line = inspect.getsourcelines(frame.f_code)
            end_line = start_line + len(lines) - 1

            if frame.f_lineno < end_line: #set another timer...
                func_name = frame.f_code.co_name
                fileloc = frame.f_code.co_filename
                lineno = frame.f_lineno
                premod = f"{fileloc} | function: {func_name}(); Line {lineno}: "
                stop_event = threading.Event()
                thread_2 = threading.Thread(target=timer, args=(stop_event, premod, ))
                thread_2.start()
            return tracer
        
        sys.settrace(tracer)
        try:
            return func(*args, **kwargs)
        finally:
            sys.settrace(None)
    return wrapper

@siena_debugger
def heavy_lifting():
    x = 10
    time.sleep(0.5) # Simulate a slow operation
    y = 20
    z = x + y
    # desc.set_device('cpu')
    return z

# heavy_lifting()

# prints progression through a tree by comparing an old and new stacktrace
def print_tree(namestack_old, namestack_new):
    # calculate lengths of the stacks
    l_old = len(namestack_old)
    l_new = len(namestack_new)

    # pad the arrays if they're not the same length
    if l_new > l_old:
        namestack_old = np.pad(namestack_old, (0, l_new-l_old), mode='constant')
    elif l_new < l_old:
        namestack_new = np.pad(namestack_new, (0, l_old-l_new), mode='constant')

    # calculate number of shared nodes
    n = np.argwhere((namestack_old == namestack_new) == False)[:, 0][0]
    
    if n < l_old: # if the tree backtracks
        print("| " * n + "- " * (l_old - n))
    if n < l_new: # if the tree forwardtracks
        i = n
        while i < l_new:
            print("| " * i + "* " + namestack_new[i])
            i += 1

stack0 = []
stack1 = ["a", "b", "c"]
stack2 = ["a", "b", "c", "d", "e"]
stack3 = ["a", "f", "g"]
stack4 = ["a", "f"]

print_tree(stack0, stack1)
print_tree(stack1, stack2)
print_tree(stack2, stack3)
print_tree(stack3, stack4)
