import numpy as np 
import pandas as pd
from payment_triangle_at import payment_triangle_at
from claim_count_triangle_at import claim_count_triangle_at

# read the simulated dataset of healthcare claims into a dataframe
claims = pd.read_csv('health_claims_sample_dataset.csv')

# Create quarterly payment triangles using sample data starting with June 2024 
# with a maximum development period of 6 months 
june24_payment_triangle = payment_triangle_at(claims, '2024-06-30', 6)
september24_payment_triangle = payment_triangle_at(claims, '2024-09-30', 6)
december24_payment_triangle = payment_triangle_at(claims, '2024-12-31', 6)
march25_payment_triangle = payment_triangle_at(claims, '2025-03-31', 6)
june25_payment_triangle = payment_triangle_at(claims, '2025-06-30', 6)
september25_payment_triangle = payment_triangle_at(claims, '2025-09-30', 6)
december25_payment_triangle = payment_triangle_at(claims, '2025-12-31', 6)

# Create quarterly claim count triangles using sample data starting with June 
# 2024 with a maximum development period of 6 month 
june24_claim_count_triangle = claim_count_triangle_at(claims, '2024-06-30', 6)
september24_claim_count_triangle = claim_count_triangle_at(claims, '2024-09-30', 6)
december24_claim_count_triangle = claim_count_triangle_at(claims, '2024-12-31', 6)
march25_claim_count_triangle = claim_count_triangle_at(claims, '2025-03-31', 6)
june25_claim_count_triangle = claim_count_triangle_at(claims, '2025-06-30', 6)
september25_claim_count_triangle = claim_count_triangle_at(claims, '2025-09-30', 6)
december25_claim_count_triangle = claim_count_triangle_at(claims, '2025-12-31', 6)

# Export the quarterly payment reports as CSVs for manipulation in Excel
june24_payment_triangle.to_csv('quarterly_payments_june24.csv')
september24_payment_triangle.to_csv('quarterly_payments_september24.csv')
december24_payment_triangle.to_csv('quarterly_payments_december24.csv')
march25_payment_triangle.to_csv('quarterly_payments_march25.csv')
june25_payment_triangle.to_csv('quarterly_payments_june25.csv')
september25_payment_triangle.to_csv('quarterly_payments_september25.csv')
december25_payment_triangle.to_csv('quarterly_payments_december25.csv')

# Export the quarterly claim count reports as CSVs for manipulation in Excel
june24_claim_count_triangle.to_csv('quarterly_claim_counts_june24.csv')
september24_claim_count_triangle.to_csv('quarterly_claim_counts_september24.csv')
december24_claim_count_triangle.to_csv('quarterly_claim_counts_december24.csv')
march25_claim_count_triangle.to_csv('quarterly_claim_counts_march25.csv')
june25_claim_count_triangle.to_csv('quarterly_claim_counts_june25.csv')
september25_claim_count_triangle.to_csv('quarterly_claim_counts_september25.csv')
december25_claim_count_triangle.to_csv('quarterly_claim_counts_december25.csv')