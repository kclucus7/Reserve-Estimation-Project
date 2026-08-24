import pandas as pd
import numpy as np
from datetime import datetime


"""
    Builds a cumulative paid loss triangle with accident months as rows and 
    development months as columns as of a given evaluation date input.

    Inputs: 
    eval_date can be a datetime object or a string structured as 'YYYY-MM-DD'.

    claims_df must be a pandas dataframe with at least fields: 
    - 'Incurred Date'
    - 'Paid Date'
    - 'Claim Amount'

    Output:
    a pandas datframe with
"""

def payment_triangle_at(claims_df, eval_date):

    # make the evaluation date into a datetime data type to make it easier 
    # to work with
    if isinstance(eval_date, str):
        eval_date = datetime.strptime(eval_date, '%Y-%m-%d')

    # make a copy of the dataframe to not change the input data
    df = claims_df.copy()

    # Since claims_df will be populated using read_csv(...), the date fields 
    # will be populated with strings, so we need to convert the strings 
    # to pandas datetime datatypes to work with them
    df['Incurred_Date'] = pd.to_datetime(df['Incurred_Date'])
    df['Paid_Date'] = pd.to_datetime(df['Paid_Date'])

    # Filter df to only include entries with the incurred date before the 
    # evaluation date using boolean indexing
    before_eval_indexes = df['Incurred_Date'] <= eval_date
    df = df[before_eval_indexes].copy()

    # Labeling claims according to the month the accident occurred 
    # (rows of triangle)
    df['accident_month'] = df['Incurred_Date'].dt.to_period('M')

    # Filter entries to only include claims actually paid by eval_date
    paid = df[df['Paid_Date'] <= eval_date].copy()

    # Add a new entry to each claim representing development month for placement
    # in the triangle later
    paid['dev_month'] = (
        (paid['Paid_Date'].dt.year - paid['Incurred_Date'].dt.year) * 12 +
        (paid['Paid_Date'].dt.month - paid['Incurred_Date'].dt.month))

    # Max observable development month for each accident month, as of eval_date
    # Keeps a record of every claim's max development (from incurred date to 
    # the evaluation date) so that triangle construction is more straigthforward
    # with no confusion between NaN entries (development hasn't reached that 
    # month) and cumulative months with maybe no additional payments
    df['max_dev_month'] = (
        (eval_date.year - df['Incurred_Date'].dt.year) * 12 +
        (eval_date.month - df['Incurred_Date'].dt.month))

    # Populating incremental paid amounts by (accident_month, dev_month):
    # After bucketing all claims with the same accident and development month, 
    # their claim amounts are summed so there's only 1 entry per 
    # [accident month, development month] pair
    incremental_payments = paid.groupby(['accident_month', 'dev_month'])['Claim_Amount'].sum()

    # Break the multi-index series created above into a grid with rows of 
    # accident months and columns of development month count
    # If an accident_month - dev_month pair doesn't have any values, the entry
    # is filled with 0
    incremental_payments = incremental_payments.unstack(fill_value=0)

    # Identify the unique accident months that occur in the data, and
    # sort them chronologically
    unique_accident_months = df['accident_month'].unique()
    sorted_accident_months = sorted(unique_accident_months)
    
    
    # Identify the longest development period possible from data
    # Reindex the incremental payment matrix with accident months as rows and 
    # development months sorted chrnonologically as columns 
    # (with 0s in empty entries)
    max_dev = df['max_dev_month'].max()
    incremental_payments = incremental_payments.reindex(index=sorted_accident_months, columns=range(0, max_dev + 1), fill_value=0)

    # Taking the cumulative sum across development months for all rows
    cumulative_sums = incremental_payments.cumsum(axis=1)

    # Find the max development period for every accident month
    max_dev_by_row = df.groupby('accident_month')['max_dev_month'].first()

    # For every accident month, make all entries that haven't been observed yet
    # NaN (entries with dev_month larger than the respective max_dev_by_row)
    for accident_month in cumulative_sums.index:
        dev_limit = max_dev_by_row.loc[accident_month]
        for dev_month in cumulative_sums.columns:
            if dev_month > dev_limit:
                cumulative_sums.loc[accident_month, dev_month] = np.nan

    return cumulative_sums