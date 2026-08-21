import pandas as pd
import numpy as np
from datetime import datetime


"""
    Builds a cumulative paid loss triangle (accident month x development
    month) as of a given evaluation date.

    eval_date can be a datetime object or a 'YYYY-MM-DD' string.

    - Accident months that haven't started yet by eval_date are excluded.
    - Claims not yet paid by eval_date contribute $0 (not yet observed).
    - Cells beyond what's observable for a given accident month (the
      staircase) are set to NaN, not 0 -- NaN means "unknown", 0 means
      "known to be zero".
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



    ## PICK UP FROM HERE## 
    
    # Max observable development month for each accident month, as of eval_date
    df['max_dev_month'] = (
        (eval_date.year - df['Incurred_Date'].dt.year) * 12 +
        (eval_date.month - df['Incurred_Date'].dt.month)
    )

    # Only claims actually paid by eval_date contribute to paid amounts
    paid = df[df['Paid_Date'] <= eval_date].copy()
    paid['dev_month'] = (
        (paid['Paid_Date'].dt.year - paid['Incurred_Date'].dt.year) * 12 +
        (paid['Paid_Date'].dt.month - paid['Incurred_Date'].dt.month)
    )

    # Incremental paid amounts by (accident_month, dev_month)
    incr = paid.groupby(['accident_month', 'dev_month'])['Claim_Amount'].sum().unstack(fill_value=0)

    # Build the full grid: every accident month present, dev months 0..max
    all_accident_months = sorted(df['accident_month'].unique())
    max_dev = df['max_dev_month'].max()
    incr = incr.reindex(index=all_accident_months, columns=range(0, max_dev + 1), fill_value=0)

    # Cumulative sum across development months
    cum = incr.cumsum(axis=1)

    # Mask cells beyond what's observable for each accident month
    max_dev_by_row = df.groupby('accident_month')['max_dev_month'].first()
    for am in cum.index:
        limit = max_dev_by_row.loc[am]
        cum.loc[am, cum.columns > limit] = np.nan

    return cum