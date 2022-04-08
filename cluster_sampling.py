import numpy as np
from fractions import Fraction
from dataclasses import dataclass, field

@dataclass
class OneStageCluster:
    m : list[int]
    y : list[int or float]
    N : int  # population clusters total
    n : int = field(init=False) # number of clusters in sample (srs)
    M: int = 0
    m_: float = field(init=False) # average cluster size for sample
    M_: float = field(init=False) # average cluster size for population
    z: float = 2.0
    
    def __post_init__(self):
        self.n = len(self.m)
        self.m_ = sum(self.m)/self.n
        self.M_ = self.M/self.N
    
    def estimate_mean(self)  -> tuple[float, float] :
        mean_per_element = sum(self.y)/sum(self.m)
        mean_per_cluster = sum(self.y)/self.n
        return (mean_per_element, mean_per_cluster)
    
    def estimate_mean_variances(self) -> tuple[tuple[float, float], tuple[float, float]]:
        means = self.estimate_mean()
        element_mean = means[0]
        cluster_mean = means[1]
        element_mean_variance = Fraction(1,self.n-1) * np.sum([(self.y[i] - element_mean*self.m[i])**2 for i in range(self.n)])
        M_bar = self.M_ if self.M != 0 else self.m_
        est_element_variance = (1-Fraction(self.n,self.N))*(element_mean_variance/(self.n*(M_bar**2)))
        element_bound = 2 * np.sqrt(est_element_variance)
        cluster_mean_variance = Fraction(1,self.n-1) * np.sum([(self.y[i]-cluster_mean)**2 for i in range(self.n)])
        est_cluster_variance = (1-Fraction(self.n,self.N))*(cluster_mean_variance/self.n)
        cluster_bound = 2 * np.sqrt(est_cluster_variance)
        out = ((est_element_variance,element_bound),(est_cluster_variance, cluster_bound))
        return out
    
    def estimate_total(self) -> float : 
        m_p_element, m_p_cluster = self.estimate_mean()
        if self.M != 0:
            total = self.M * m_p_element
        else:
            total = self.N * m_p_cluster
        return total
    
    def estimate_total_variance(self) -> tuple[float, float]:
        m_p_element, m_p_cluster = self.estimate_mean()
        if self.M != 0:
            variance = Fraction(1,self.n-1) * np.sum([(self.y[i] - m_p_element*self.m[i])**2 for i in range(self.n)])
        else:
            variance = Fraction(1,self.n-1) * np.sum([(self.y[i] - m_p_cluster)**2 for i in range(self.n)])
        est_variance = self.N**2 * (1-Fraction(self.n,self.N))*(variance/self.n)
        bound = 2 * np.sqrt(est_variance)
        return (est_variance, bound)
    
    def estimate_proportion(self) -> float:
        proportion = sum(self.y)/sum(self.m)
        return proportion
    
    def estimate_proportion_variance(self) -> tuple[float, float]:
        '''Return the estimated variance of the proportion along with the bound on error of estimation '''
        proportion = self.estimate_proportion() 
        variance = Fraction(1,self.n-1) * np.sum([(self.y[i] - proportion*self.m[i])**2 for i in range(self.n)])
        M_bar = self.M_ if self.M != 0 else self.m_
        est_variance = (1-Fraction(self.n,self.N))*(variance/(self.n*(M_bar**2)))
        bound = 2 * np.sqrt(est_variance)
        return (est_variance,bound)
    
    def sample_size(self, bound: float, metric: str) -> int:
        m_p_element, m_p_cluster = self.estimate_mean()
        d = bound**2 * self.M_**2 /self.z**2 if self.M != 0 else ((bound**2) * (self.m_**2))/(self.z**2) #if we know the population total we use population mean else, we use sample mean
        variance = Fraction(1,self.n-1) * np.sum([(self.y[i] - m_p_element*self.m[i])**2 for i in range(self.n)])
        proportion = self.estimate_proportion()
        if metric == 'mean':
            samplesize = (self.N * variance)/ (self.N*d + variance)
            return round(samplesize,0)
        elif metric == 'total':
            d = bound**2/ ((self.z**2) * (self.N**2))
            if self.M != 0:
                samplesize = (self.N * variance)/ (self.N*d + variance)
                return round(samplesize,0)
            else:
                variance = Fraction(1,self.n-1) * np.sum([(self.y[i] - m_p_cluster)**2 for i in range(self.n)])
                samplesize = (self.N * variance)/ (self.N*d + variance)
                return round(samplesize,0)
        elif metric == 'proportion':
            variance = Fraction(1,self.n-1) * np.sum([(self.y[i] - proportion*self.m[i])**2 for i in range(self.n)])
            samplesize = (self.N * variance)/ (self.N*d + variance)
            return round(samplesize,0)
        return 0


@dataclass
class TwoStageCluster(OneStageCluster):
    pass

if __name__ == '__main__':
    m = np.array([51,62,49,73,101,48,65,49,73,61,58,52,65,49,55])
    y = np.array([42,53,40,45,63,31,38,30,54,45,51,29,46,37,42])
    cluster = OneStageCluster(m,y,87)
    cluster_proportion = cluster.estimate_proportion()
    cluster_variance = cluster.estimate_proportion_variance()
    cluster_size = cluster.sample_size(0.08, 'proportion')
    print(cluster)
    print(cluster_proportion)
    print(cluster_variance)
    print(cluster_size)
    
    print('\n\n\n\n\n\n\n\n\n\n')
    print('Question 4')
    
    m = np.array([31,29,25,35,15,31,22,27,25,19,30,18,21,40,38,28,17,22,41,32,35,19,29,18,31])
    y = np.array([1590,1510,1490,1610,800,1720,1310,1427,1290,860,1620,710,1140,1980,1990,1420,900,1080,2010,1740,1750,890,1470,910,1740])
    cluster = OneStageCluster(m,y,108)
    cluster_means = cluster.estimate_mean()
    cluster_variance = cluster.estimate_mean_variances()
    cluster.N = 100
    cluster_size = cluster.sample_size(2, 'mean')
    print(cluster)
    print(cluster_means)
    print(cluster_variance)
    print(cluster_size)
    
    print('\n\n\n\n\n\n\n\n\n\n')
    print('Question 5')
    
    m = np.array([55,60,63,58,71,78,69,58,52,71,73,64,69,58,63,75,78,51,67,70])
    y = np.array([2210,2390,2430,2380,2760,3110,2780,2370,1990,2810,2930,2470,2830,2370,2390,2870,3210,2430,2730,2880])
    cluster = OneStageCluster(m,y,60)
    cluster_means = cluster.estimate_mean()
    cluster_total = cluster.estimate_total()
    cluster_variance = cluster.estimate_total_variance()
    cluster_size = cluster.sample_size(5000, 'total')
    print(cluster)
    print(cluster_means)
    print(cluster_total)
    print(cluster_variance)
    print(cluster_size)