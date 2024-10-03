
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
            'procedures': np.random.randint(1,10, 100),
            'has_diabetes': np.random.choice([True, False], 100, p=[0.25, 0.75]),
    }
    df = pd.DataFrame(data)
    df.loc[100] = [np.nan]*3 + ['Control', 3, True]
    return df

def get_test_data():
    """
    Enriches the sample data with further column for testing

    :return: sample data
    :rtype: pandas dataframe
    """
    np.random.seed(42)
    df = get_sample_data()
    df['colmissing'] = np.random.random(101) * 100
    df.loc[df.group=="Experimental", "colmissing"] = np.nan
    return df

