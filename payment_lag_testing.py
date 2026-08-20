import numpy as np
import matplotlib.pyplot as plt
from gen_payment_lags import gen_payment_lags

# claim_sizes set up same as in dataset_creation file
# create payment_lags using gen_payment_lag function
# changing the mu_intercept, mu_slope, sigma_intercept, and sigma_slope 
# paramters inside of the function file, checking against the graphs to make 
# small changes to most accurately model the payment lag
np.random.seed(42)
claim_sizes = np.random.lognormal(mean=5.8, sigma=1.5, size=20000).round(2)
claim_sizes = np.clip(claim_sizes, 10.0, 100000.0)
payment_lags = gen_payment_lags(claim_sizes)

# Graph 1: checking the distribution of the payment lags
plt.figure()
plt.hist(payment_lags, 100, density=True)
plt.xlabel("Payment Lag (days)")
plt.ylabel("Density")
plt.title("Payment Lag Distribution")
plt.show()

# Graph 2: checking the payment lags against claim sizes
plt.figure()
plt.scatter(claim_sizes, payment_lags, s=2, alpha=0.3)
plt.xscale('log')
plt.xlabel("Claim Size ($)")
plt.ylabel("Payment Lag (days)")
plt.title("Claim Size vs. Payment Lag")
plt.grid(alpha=0.3)
plt.show()