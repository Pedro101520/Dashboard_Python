
def placa_filter(placa, df):
    mask = df['placa'].isin([placa])
    return mask
