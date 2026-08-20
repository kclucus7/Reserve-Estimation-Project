import numpy as np 
import pandas as pd

def gen_payment_lags(claim_sizes, claims_number): 
    payment_lags = []

    # Log-transforming the sizes ensures smooth transitions between the means 
    # sds as they grow extremely large and we can scale a linear model
    log_sizes = np.log(claim_sizes)

     
    # Increasing mu and sigma to scale with log claim sizes to represent the 
    # increased payment lag and volatility in the lag depending on the size 
    # (and thereby complexity) of a claim

    # Mu and Sigma values with parameters based on testing file
    mu_intercept = 0.62
    mu_slope = 0.33
    mus = mu_intercept + mu_slope*log_sizes
    sigma_intercept = -0.02
    sigma_slope = 0.042
    sigmas = sigma_intercept + sigma_slope * log_sizes

    # Floor sigma slightly to prevent mathematically impossible zero/negative variance on tiny claims
    sigmas = np.maximum(0.10, sigmas)

    # Simulates payment lags according to a log-normal distribution with 
    # variable parameters depending on the claim size as calculated above. 
    # Log-normal dsitribution was chosen to cluster payment lags toward the 
    # short-term while maintaining a portion of longer payment lags in response 
    # to larger, more complicated claims
    payment_lags = np.random.lognormal(mus, sigmas)
    
    return payment_lags