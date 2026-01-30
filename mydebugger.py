import inspect
import linecache
import desc
import sys
import threading
import time
import traceback

def siena_debugger(func):
    def wrapper(*args, **kwargs):
        first_line = True
        stop_event = threading.Event()
        t = 0
        headerfile = ""
        lastfile = ""

        """
        TODO: create a dynamic timer that, when called, will execute until a stop event is set
        """
        def dynamic_timer(stop_event, current_line):
            start = time.perf_counter()
            while not stop_event.is_set():
                elapsed = time.perf_counter() - start
                sys.stdout.write(f"\rLine: {current_line} Elapsed time: {elapsed:.2f}s ")
                sys.stdout.flush()
                time.sleep(0.1)
            # print("\nDone!")
        
        """
        TODO: tracer starts before line begins. so, 
            0) (if not first liine) tell previous timer to end
            1) print line about to execute to screen
            2) start dynamic timer
        """
        def tracer(frame, event, arg):
            lines, start_line = inspect.getsourcelines(frame.f_code)
            end_line = start_line + len(lines) - 1
            lineno = frame.f_lineno
                        
            nonlocal stop_event
            nonlocal t
            nonlocal headerfile
            nonlocal currentfile
            if lineno > start_line:
                stop_event.set()
                t.join()

            stack = traceback.extract_stack(frame)
            fmt_trace = traceback.format_list([stack[-1]])
            fileloc = fmt_trace[0].split(", line ")[0]
            print(fileloc)
            print(lineno)

            if lineno == start_line:
                headerfile = fileloc
            lastfile = fileloc    
            
            # print(f"DEBUG TRACE:\n{fmt_trace[0]}", end="")

            stop_event = threading.Event()
            if frame.f_lineno < end_line:
                t = threading.Thread(target=dynamic_timer, args=(stop_event, lineno, ))
                t.start()
            return tracer
        
        sys.settrace(tracer)
        try:
            return func(*args, **kwargs)
        finally:
            sys.settrace(None)
    return wrapper

# do3es next thread start before i see final_line=true?

# let's print the file location on each new line if it changes. if it's not the main file location, add an indent
# on each subsequent line

# make it so every new function has a treelike structure where "*" represents one indent in
# so like, here's an example format

"""

* File "/Users/sienahurwitz/Documents/Physics/Projects/2024---Islands-Representation/mydebugger.py"
| Line 1: 0.67s
| Line 2: 0.59s
| * File "/users/whatever"
| | Line 57: 1.23s
| | Line 58: 1.23s


"""



@siena_debugger
def heavy_lifting():
    x = 10
    time.sleep(0.5) # Simulate a slow operation
    # hello()
    y = 20
    z = x + y
    desc.set_device('cpu')
    return z

heavy_lifting()



#TODO: IF THERE IS A FAILURE INSIDE HEAVYLIFTING IT DOESNT WORK


# ------------------------------------------------------------------


# import sys
# import time

# def time_lines(func):
#     def wrapper(*args, **kwargs):
#         last_time = time.perf_counter()
#         def dynamic_timer(stop_event):
#             start = time.perf_counter()
#             while not stop_event.is_set():
#                 elapsed = time.perf_counter() - start
#                 sys.stdout.write(f"\rElapsed time: {elapsed:.2f}s ")
#                 sys.stdout.flush()
#                 time.sleep(0.1)
#             print("\nDone!")

#         def tracer(frame, event, arg):
#             nonlocal last_time
#             if event == 'line': # when tracer hits a new line...

#                 #TODO end live timer with stop signal
#                 #TODO block next line from going until timer is done

#                 now = time.perf_counter() # calculate current time
#                 elapsed = now - last_time # and thus calculate time elapsed
                
#                 # tracer pauses before executing a new line frame.f_lineno, so
#                 # frame.f_lineno-1 is the last line number
#                 print(f"Line {frame.f_lineno-1} took {elapsed:.6f}s")
                
#                 last_time = now # updated last time to when following line begin execution

#                 #TODO set stop signal to false 
#                 #TODO begin live timer
#             return tracer
        
#         sys.settrace(tracer)
#         try:
#             #TODO set stop signal to false
#             #TODO begin live timer
            
#             return func(*args, **kwargs)
#         finally:
#             sys.settrace(None)
#     return wrapper

# @time_lines
# def heavy_lifting():
#     x = 10
#     time.sleep(0.5) # Simulate a slow operation
#     y = 20
#     z = x + y
#     return z

# heavy_lifting()