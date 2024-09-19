
import numpy as np
import pandas as pd

def get_sample_data():
    """
    Gets some data for testing and demo purposes

    :return: sample data
    :rtype: pandas dataframe
    """
    np.random.seed(42)
    data = {'gender': np.random.choice(['Male', 'Female'], 100, p=[0.6, 0.4]),
            'age': np.random.randint(20, 80, 100),
            'region': np.random.choice(['North', 'South', 'East', 'West'], 100, p=[0.3, 0.2, 0.1, 0.4]),
            'group': np.random.choice(['Control', 'Experimental'], 100, p=[0.4, 0.6]),
    }
    df = pd.DataFrame(data)
    df.loc[100] = [np.nan]*3 + ['Control']
    return df
