import numpy as np 
import pandas as pd
from payment_triangle_at import payment_triangle_at

# read the simulated dataset of healthcare claims into a dataframe
claims = pd.read_csv('health_claims_sample_dataset.csv')

# Create quarterly payment triangles using sample data starting with June 2024
june24_payment_triangle = payment_triangle_at(claims, '2024-06-30')
september24_payment_triangle = payment_triangle_at(claims, '2024-09-30')
december24_payment_triangle = payment_triangle_at(claims, '2024-12-31')
march25_payment_triangle = payment_triangle_at(claims, '2025-03-31')
june25_payment_triangle = payment_triangle_at(claims, '2025-06-30')
september25_payment_triangle = payment_triangle_at(claims, '2025-09-30')
december25_payment_triangle = payment_triangle_at(claims, '2025-12-31')

# Export the quarterly reports as CSV for manipulation in Excel
june24_payment_triangle.to_csv('quarterly_payments_june24.csv', index=False)
september24_payment_triangle.to_csv('quarterly_payments_september24.csv', index=False)
december24_payment_triangle.to_csv('quarterly_payments_december24.csv', index=False)
march25_payment_triangle.to_csv('quarterly_payments_march25.csv', index=False)
june25_payment_triangle.to_csv('quarterly_payments_june25.csv', index=False)
september25_payment_triangle.to_csv('quarterly_payments_september25.csv', index=False)
december25_payment_triangle.to_csv('quarterly_payments_december25.csv', index=False)