def numerical_answers(df):
    # I trnsform the yes/no answers in the dataframe in numerical ones (0/1)
    df.replace({'CommonAnswer': {'yes': 1, 'YES': 1, 'Yes': 1, 'no': 0, 'NO': 0, 'NO ': 0}}, inplace=True)
    df.replace({'1': {'yes': 1, 'no': 0}}, inplace=True)
    df.replace({'2': {'yes': 1, 'no': 0}}, inplace=True)
    df.replace({'3': {'yes': 1, 'ynes': 1, 'no': 0}}, inplace=True)


def correct_data(data):
    # I correct the commonAnswer field in case it is wrong (e.g. 2/3 experts say yes,
    # but in the commonAnswer is reported no)
    for i in range(len(data)):
        check_sum = data.loc[i, '1'] + data.loc[i, '2'] + data.loc[i, '3']
        if check_sum >= 2 and data.loc[i, 'CommonAnswer'] == 0:
            data.loc[i, 'CommonAnswer'] = 1
        if check_sum <= 1 and data.loc[i, 'CommonAnswer'] == 1:
            data.loc[i, 'CommonAnswer'] = 0
