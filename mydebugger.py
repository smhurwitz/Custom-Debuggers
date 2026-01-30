import inspect
import linecache
import desc
import sys
import threading
import time
import traceback

def siena_debugger(func):
    def wrapper(*args, **kwargs):
        thread_2 = None
        stop_event = None

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
            lines, start_line = inspect.getsourcelines(frame.f_code)
            end_line = start_line + len(lines) - 1
                        
            nonlocal stop_event
            nonlocal thread_2
            if stop_event is not None:
                stop_event.set()
                thread_2.join()

            stack = traceback.extract_stack(frame)
            fmt_trace = traceback.format_list([stack[-1]])[0]
            fileloc, lineno = fmt_trace.split(", in ")[0].split(", line ")
            premod = f"{fileloc} | Line {lineno}: "

            stop_event = threading.Event()
            if frame.f_lineno < end_line:
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

heavy_lifting()

