import pandas as pd
import numpy as np
 
 
def compute_age_to_age_factors(triangle):
    """
    Computes volume-weighted average age-to-age (link) development factors
    from a cumulative paid triangle.
 
    For each pair of consecutive development months, the factor is:
        sum(next column, using only accident months where BOTH columns
            are observed) / sum(current column, same accident months)
 
    Returns a pandas Series indexed by the "from" development month --
    e.g. factors[0] is the factor to go from dev month 0 to dev month 1.
    """
    return 0