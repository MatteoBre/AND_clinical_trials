def numerical_answers(df):
    df.replace({'CommonAnswer': {'yes': 1, 'YES': 1, 'Yes': 1, 'no': 0, 'NO': 0, 'NO ': 0}}, inplace=True)
    df.replace({'1': {'yes': 1, 'no': 0}}, inplace=True)
    df.replace({'2': {'yes': 1, 'no': 0}}, inplace=True)
    df.replace({'3': {'yes': 1, 'ynes': 1, 'no': 0}}, inplace=True)


def checkData(data):
    error = False
    for i in range(len(data)):
        checkSum = data.loc[i, '1'] + data.loc[i, '2'] + data.loc[i, '3']
        if(data.loc[i, 'CommonAnswer'] != 0 and data.loc[i, 'CommonAnswer'] != 1):
            print('not a valid value at', i, ':', data.loc[i, 'CommonAnswer'])
            error = True
        if(checkSum >= 2 and data.loc[i, 'CommonAnswer'] == 0):
            print('error at', i, ': common answer should be yes')
            error = True
        if(checkSum <= 1 and data.loc[i, 'CommonAnswer'] == 1):
            print('error at', i, ': common answer should be no')
            error = True
    return error


def correctData(data):
    for i in range(len(data)):
        checkSum = data.loc[i, '1'] + data.loc[i, '2'] + data.loc[i, '3']
        if(checkSum >= 2 and data.loc[i, 'CommonAnswer'] == 0):
            data.loc[i, 'CommonAnswer'] = 1
        if(checkSum <= 1 and data.loc[i, 'CommonAnswer'] == 1):
            data.loc[i, 'CommonAnswer'] = 0

