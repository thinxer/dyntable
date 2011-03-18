# encoding=utf8

LONGEST_WORD = 6

def segment(text):
    ''' 
    Temporary solution.
    require the text to be UNICODE. '''
    s = set()
    for i in range(len(text)):
        for j in range(i, min(len(text), i+LONGEST_WORD)):
            s.add(text[i:j+1])
    return list(s)

if __name__ == '__main__':
    print segment('你好'.decode('utf8'))
