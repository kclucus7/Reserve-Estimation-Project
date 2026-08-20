import numpy as np
import matplotlib.pyplot as plt

# paramters (to be changed to test the distribution of payment lags)
mu_intercept = 0.62
mu_slope = 0.3
sigma_intercept = -0.02
sigma_slope = 0.035

#Claim sizes (distribution copied from dataset_creation file)
np.random.seed(42)
claims_number = 20000
claim_sizes = np.random.lognormal(5.8, 1.5, claims_number)
claim_sizes = np.clip(claim_sizes, 10.0, 100000.0)

# Generate payment lags from the claim sizes
log_sizes = np.log(claim_sizes)
mus = mu_intercept + mu_slope*log_sizes
sigmas = np.maximum(0.1, sigma_intercept + sigma_slope*log_sizes)
payment_lags = np.random.lognormal(mus, sigmas)

# clip payment lags at 120 days no matter the claim size to account for 
# regulatory compliance
payment_lags = np.clip(payment_lags, None, 120)

# Graph 1: checking the distribution of the payment lags
plt.figure()
plt.hist(payment_lags, 1000, density=True)
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