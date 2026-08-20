import numpy as np 
import pandas as pd

def gen_payment_lags(claim_sizes): 
    payment_lags = []

    # Log-transforming the sizes ensures smooth transitions between the means + 
    # sds as they grow large, so we can scale a linear model
    log_sizes = np.log(claim_sizes)
     
    # Calibrating Mu: 
    mu_intercept = 0.62
    mu_slope = 0.33
    mus = mu_intercept + mu_slope*log_sizes
    
    # Calibrating Sigma:
    sigma_intercept = -0.02
    sigma_slope = 0.042
    sigmas = sigma_intercept + sigma_slope*log_sizes
    
    # Floor sigma slightly to prevent mathematically impossible zero/negative variance on tiny claims
    sigmas = np.maximum(0.10, sigmas)

    # 3. Vectorized Simulation Run
    # numpy handles arrays for both parameters seamlessly, ensuring every claim 
    # gets its own custom probability curve based on its precise cost.
    payment_lags = np.random.lognormal(mean=mus, sigma=sigmas)
    
    return payment_lags


