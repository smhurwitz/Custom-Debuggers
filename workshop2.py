import traceback

def alpha():
    beta()

def beta():
    gamma()

def gamma():
    # This prints the entire call chain to the console
    traceback.print_stack()

alpha()