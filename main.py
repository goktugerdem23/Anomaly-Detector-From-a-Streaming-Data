"""
Anomly Detector
We will consider values outside mean ± 3 * standart deviation as anomalous data
For calculating standart deviation, we will use Exponentially Weighted Moving Average (EWMA)
"""

import numpy as np
import time
import pandas as pd

#First, for continuous data stream, let's write a function that generates a continuous data stream

def continuous_data_stream(length = 1000,seasonality=True):
    try: 
        for i in range(length):
            #Noise
            base = np.sin(i * 0.1) if seasonality else 1
            noise = np.random.normal(0,0.1)
            #Anomalies
            if np.random.random() > 0.80: # Generate random number between 0 and 1, if this number is greater than 0.80 (with %20 possibility) it is an anomaly
                anomaly = np.random.uniform(2,5)
            else:
                anomaly = 0
            data_point =  base + noise + anomaly
            yield data_point
            time.sleep(0.1)
    except Exception as e:
        print(f"Error during data generation: {e}")
#insert the first 100 generated data to a list to test the function
stream_data = list(continuous_data_stream(length=2000)) 


#Anomaly Detection
def EWMA(data, alpha=0.06):
    try:
        ewma = pd.Series(np.zeros(len(data)))  
        ewma[0] = data[0]  
        for i in range(1, len(data)):
            ewma[i] = alpha * data[i] + (1 - alpha) * ewma[i-1] 
        return ewma
    except Exception as e:
        print(f"Error during anomly detection {e}")

    
rets = pd.Series(stream_data)

lam = 0.94
ewma = EWMA(rets,lam)
print(ewma)

mean = rets.mean()
threshold = 3
def detect_anomalies(data,ewma_vol,mean,threshold=3):
    anomalies = ((data < mean - threshold * ewma_vol) | (data > mean + threshold * ewma_vol))
    return anomalies

anomalies = detect_anomalies(rets,ewma,mean)
print(anomalies)
print(f"Anomalies detected: {anomalies.sum()} values")



