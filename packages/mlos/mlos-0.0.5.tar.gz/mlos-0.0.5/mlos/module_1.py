def display1(msg):
    print(msg)


def dx (tst):
    print(tst)


def mltext(_ini,msg):
    valx= str(msg).replace("",'')
    with open(_ini["fn_logs"], 'a') as f1:
        f1.write('\n')
        f1.write(valx)
    if True:
        lgtxt =valx