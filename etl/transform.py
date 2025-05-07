import pandas as pd

def aggregate_data(df):
    """
    Realiza agregação 10-minutal com média, mínimo, máximo e desvio padrão.
    
    Args:
        df (pd.DataFrame): DataFrame com as colunas 'timestamp', 'wind_speed', 'power'
    
    Returns:
        pd.DataFrame: DataFrame agregado com colunas ['timestamp', 'variable', 'mean', 'min', 'max', 'std']
    """

    # Converte timestamp para índice e arredonda para 10min
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    df = df.resample('10T').agg({
        'wind_speed': ['mean', 'min', 'max', 'std'],
        'power': ['mean', 'min', 'max', 'std']
    })

    # Ajusta nome das colunas
    df.columns = ['_'.join(col).strip() for col in df.columns.values]
    df.reset_index(inplace=True)

    # Prepara para formato final (long / tidy format)
    long_df = pd.melt(
        df,
        id_vars=['timestamp'],
        value_vars=df.columns[1:],  # ignora timestamp
        var_name='variable_stat',
        value_name='value'
    )

    # Separa variável e estatística
    long_df[['variable', 'stat']] = long_df['variable_stat'].str.rsplit('_', n=1, expand=True)
    long_df.drop(columns=['variable_stat'], inplace=True)

    # Organiza colunas
    final_df = long_df.pivot_table(
        index=['timestamp', 'variable'],
        columns='stat',
        values='value'
    ).reset_index()

    return final_df
