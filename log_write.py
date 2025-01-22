

def logger(message):
    with open('log.txt', 'a') as f:
        f.write(message + '\n')