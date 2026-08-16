import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# set seed for study replication and establish number of claims
np.random.seed(42)
claims_number = 20000

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
claim_sizes = np.random.lognormal(5.8, 1.5, claims_number)
claim_sizes = np.clip(claim_sizes, 10.0, 100000.0)



# # 3. Simulate processing lag (days between doctor visit and insurance payout)
# # Real insurance lag is heavily skewed: most claims pay fast, a few take a long time.
# # We use a Gamma distribution to realistically model this operational bottleneck.
# processing_lag_days = np.random.gamma(shape=2.0, scale=25.0, size=num_claims).astype(int)
# processing_lag_days = np.clip(processing_lag_days, 1, 360) # Keep lag between 1 day and 1 year

# # 4. Calculate Paid Dates based on the lag
# paid_dates = [inc + timedelta(days=int(lag)) for inc, lag in zip(incurred_dates, processing_lag_days)]

# # 5. Generate realistic Claim Amounts using a Log-Normal distribution
# # Most health claims are small ($50-$150), but a few are massive hospitalizations.
# claim_amounts = np.random.lognormal(mean=5.0, sigma=1.2, size=num_claims).round(2)
# claim_amounts = np.clip(claim_amounts, 10.0, 50000.0) # Cap at a maximum of $50,000

# # 6. Assemble into a structured DataFrame
# df_claims = pd.DataFrame({
#     'Claim_ID': np.arange(1, num_claims + 1),
#     'Incurred_Date': incurred_dates,
#     'Paid_Date': paid_dates,
#     'Claim_Amount': claim_amounts
# })

# # 7. Inject an operational anomaly (Simulation Feature)
# # Let's simulate a 2-month processor system outage in Nov/Dec 2024 where payouts lagged significantly
# outage_mask = (df_claims['Incurred_Date'] >= datetime(2024, 11, 1)) & (df_claims['Incurred_Date'] <= datetime(2024, 12, 31))
# df_claims.loc[outage_mask, 'Paid_Date'] = df_claims.loc[outage_mask, 'Paid_Date'] + timedelta(days=45)

# # Save dataset to work with later
# df_claims.to_csv('hypothetical_health_claims.csv', index=False)
# print(df_claims.head(10))
