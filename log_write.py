
def logger(message):
    # Open log file in append mode to record system events
    with open('log.txt', 'a') as f:
        # Write the log message followed by a newline
        f.write(message + '\n')