title = 'dyntable'
db_name = 'dyntable'
columns = [ "name", "address" ]

# ugly load and save.
# TODO find a better way for saving configurations.
try:
    with open('columns.txt') as f:
        import string
        l = f.readline()
        columns = map(string.strip, l.split(','))
        columns = [x.decode('utf8') for x in columns]
except:
    pass

def save_columns(cs):
    global columns
    columns = cs
    with open('columns.txt', 'w') as f:
        f.write(','.join(cs).encode('utf8')+"\n")
