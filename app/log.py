import inspect


# log message with context indentation
# http://stackoverflow.com/questions/5498907/python-indentation-context-level-to-log-prefix-length
def log(msg):
    # frame, filename, line_number, function_name, lines, index = inspect.getouterframes(inspect.currentframe())[1]
    # line = lines[0]
    # level = line.find(line.lstrip())
    # print " " * level + msg
    print msg  # TODO get indentation levels working
