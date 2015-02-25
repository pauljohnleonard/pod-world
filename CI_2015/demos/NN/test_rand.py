min_weight=-2.0
max_weight=2.0
quant_weight=1.0
hh=quant_weight/2.0



def random_weight(x):
    """
    returns a single random weight
    """ 
    w=min_weight-hh + (max_weight-min_weight+quant_weight)*x
    www=round(w/quant_weight)*quant_weight
    return www


n=100
for i in range(n):
    ii=float(i)/(n-1)
    print random_weight(ii)
    
print