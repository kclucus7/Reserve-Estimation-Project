import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from gen_payment_lags import gen_payment_lags


# set seed for study replication and establish number of claims
np.random.seed(42)
claims_number = 10000000

# Generate random Incurred Dates over a 2-year window beginning January 1, 2024
start_date = datetime(2024, 1, 1)
incurred_dates = []
for i in range(1, claims_number + 1): 
    days = int(np.random.randint(0, 365*2))
    incurred_dates.append(start_date + timedelta(days))

# Simulate the size of each of the claims using a log-normal distribution
# because the majority of claims are small ($50-150) while a small portion are
# much larger (experimented with parameters until distribution was 
# approximately appropriate)
# ex: 
# print(len([amt for amt in claim_sizes if amt<250])/claims_number)
# print(len([amt for amt in claim_sizes if amt>1000])/claims_number)
# print(len([amt for amt in claim_sizes if amt>10000])/claims_number)
# Cap the claim sizes between 10 and 200000 to avoid outliers 
claim_sizes = np.random.lognormal(mean=5.8, sigma=1.5, size=claims_number).round(2)
claim_sizes = np.clip(claim_sizes, 10.0, 100000.0)



# Simulate reporting lag (days between the HCP visit occurring and the 
# report being submitted to insurance provider)
# Real insurance lag is heavily skewed, ie most are reported fast, a few take 
# a long time, we can model the lag with an exponential distribution, with mean
# of 5 days as a typical report lag is between 3-7 days
# clip report days at 180 as certain states require reporting by this threshold
report_lags = np.random.exponential(scale=5.0, size=claims_number).round().astype(int)
report_lags = np.clip(report_lags, 1, 180)

# Simulate payment lags (days between the report being filed and the claim 
# being paid out) using function
payment_lags = gen_payment_lags(claim_sizes, claims_number)

# Calculate Paid Dates based on the report and payment lags
paid_dates = []
for incdate, reportlag, paylag in zip(incurred_dates, report_lags, payment_lags): 
    paid_dates.append(incdate + timedelta(int(reportlag) + int(paylag)))

# Put pieces into a structured DataFrame
df_claims = pd.DataFrame({
    'Claim_ID': np.arange(1, claims_number + 1),
    'Incurred_Date': incurred_dates,
    'Paid_Date': paid_dates,
    'Claim_Amount': claim_sizes
})


# Save dataset to work with later
df_claims.to_csv('health_claims_sample_dataset.csv', index=False)
print(df_claims.head(20))

# ADD THIS PART LATER WHEN I WORK ON CORRECTING FOR SHOCKS

# Create an operational anomaly/shock to  (Simulation Feature)
# Let's simulate a 2-month processor system outage in Nov/Dec 2024 where payouts lagged significantly
# outage_mask = (df_claims['Incurred_Date'] >= datetime(2024, 11, 1)) & (df_claims['Incurred_Date'] <= datetime(2024, 12, 31))
# df_claims.loc[outage_mask, 'Paid_Date'] = df_claims.loc[outage_mask, 'Paid_Date'] + timedelta(days=45)
