import flamegraph
import inspect
import numpy as np
import os
import subprocess
import sys
import threading
import time
import traceback
import webbrowser

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
            
            ###### -----------------------------------
            nonlocal stack_old
            stack_new = traceback.extract_stack(frame)

            #TODO 2) extract filenamesstacks for old and new; if old is None then []
            if stack_old is None:
                filesstack_old = np.array([""])
            else:
                filesstack_old = np.array([f"{f.filename} {f.name}()" for f in stack_old])
            filesstack_new = np.array([f"{f.filename} {f.name}()" for f in stack_new])

            #TODO 3) pass to print_tree
            print_tree(filesstack_old, filesstack_new)

            stack_old = stack_new
            #### ------------------------------------


            lines, start_line = inspect.getsourcelines(frame.f_code)
            end_line = start_line + len(lines) - 1

            if frame.f_lineno < end_line: #set another timer...
                lineno = frame.f_lineno
                premod = "| " * len(filesstack_new) + f"Line {lineno}: "
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
    argwhere = np.argwhere((namestack_old == namestack_new) == False)
    n = l_new if argwhere.size == 0 else argwhere[:, 0][0]
    
    if n < l_old: # if the tree backtracks
        print("| " * n + "- " * (l_old - n))
    if n < l_new: # if the tree forwardtracks
        i = n
        while i < l_new:
            print("| " * i + "* " + namestack_new[i])
            i += 1

def flamegraphss(func):
    def wrapper(*args, **kwargs):
        saveloc = "./"
        savename = "perf.log"
        flamegraphloc = "/Users/sienahurwitz/Documents/Physics/Codes/flamegraph.pl"
        title = "title!!"
        brows = "safari"

        profile_thread = flamegraph.start_profile_thread(fd=open(saveloc + savename, "w"))
        result = func(*args, **kwargs)
        profile_thread.stop()

        with open("perf.svg", "w") as output_file:
            # 3. Run the command and pipe the output to the file
            subprocess.run([flamegraphloc, "--title", title, "perf.log"], stdout=output_file, check=True)
        
        file_path = os.path.abspath("perf.svg")
        url = f"file://{file_path}"

        try:
            # 2. Specifically request Safari
            browser = webbrowser.get(brows)
            browser.open(url)
        except webbrowser.Error:
            # Fallback if Safari is not found/registered for some reason
            webbrowser.open(url)

        return result
    return wrapper



