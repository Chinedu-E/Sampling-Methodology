import numpy as np
from fractions import Fraction


METRICS = ['mean','total','proportion']

class SystematicSampling:
    @staticmethod
    def one_in_sample(y: list,k: int) -> list[list[float]]:
        out = [[]for _ in range(k)]
        for i in range(k):
            out[i] = y[i::k]
        return out
    
    @staticmethod
    def statistats(samples: list[list[float]]) -> dict[str, dict[str, float]]:
        total =  len(samples)*len(samples[0])
        k = len(samples)
        stats = ['mean','total','proportion']
        out = {str(i+1): {s: 0 for s in stats} for i in range(k)}
        for i in range(len(samples)):
            out[f'{i+1}']['mean'] = np.mean(samples[i])
            out[f'{i+1}']['total'] = total * np.mean(samples[i])
            out[f'{i+1}']['proportion'] = len([j for j in samples[i] if j != 0])/len(samples[i])
            out[f'{i+1}']['s'] = Fraction(1,k-1) * np.sum([(j - np.mean(samples[i]))**2 for j in samples[i]])
            out[f'{i+1}']['MSE'] = np.sqrt((1-k/total)*out[f'{i+1}']['s']/k)
            out[f'{i+1}']['TSE'] = np.sqrt((total**2) * out[f'{i+1}']['MSE'])
            out[f'{i+1}']['PSE'] = np.sqrt((1-(k/total))* (out[f'{i+1}']['proportion']*(1-out[f'{i+1}']['proportion']))/(k-1))
        return out

    @staticmethod
    def expected_values(samples: list[list[float]]) -> dict[str, float]:
        k = len(samples)
        p = 1/k  #probability of choosing a sample
        out = {}
        stats = SystematicSampling.statistats(samples)
        for j in METRICS[:3]:
            value = 0
            for i in stats:
                value += stats[i][j]
            out[f'E({j})'] = value*p
        return out

    @staticmethod
    def sample_size(x: list ,y: list,metric: str, bound:float, population_size: int, confidence: int = 95) -> int:
        z = 0
        x = np.array(x)
        y = np.array(y)
        N = population_size
        n = len(x)
        variance = Fraction(1,n-1) * np.sum([(y[i] - np.mean(y))**2 for i in range(n)])
        p = len([i for i in y if i != 0])/n # proportion of pre-specified characteristics
        q = 1-p
        d: float = bound**2/(z**2)
        if confidence == 95:
            z = 2
        if metric == 'mean':
            samplesize  =  N*variance/((N-1)*d + variance)
            return round(samplesize,0)
        elif metric == 'total':
            d: float = d/(N**2)
            samplesize  =  N*variance/((N-1)*d + variance)
            return round(samplesize,0)
        elif metric == 'proportion':
            samplesize = (N*p*q)/((N-1)*d + (p*q))
            return round(samplesize,0)

        return 0
      
if __name__ == '__main__':   
    x = np.array([i+1 for i in range(25)])
    y = np.array([5,0,1,4,7,0,12,0,0,22,0,5,6,4,8,0,7,0,37,0,8,0,0,1,0])
    samples = SystematicSampling.one_in_sample(y,5)
    all_stats = SystematicSampling.statistats(samples)
    ev = SystematicSampling.expected_values(samples)
    sum = 0
    for i in all_stats:
        sum += all_stats[i]['PSE']
    print(sum)
    print(ev)
