import math
import numpy as np


class binomial_tree:
    '''This class implements the CRR Bimonial Tree method to calculate European Option Price.
    The volatility as an input is set to be an array instead of a constant to provide expanded
    ability to incorpate volatility changes during the calculated period. 
    This implementation does not enforce recombination. So the Number of Steps is limited to <20.
    Author: Sean X. Li, Shixu Lu
    Date: April 27, 2019.
    '''    
    def __init__ (self,StepNumber,Days2Maturity,SigmaList,InterestRate,UnderlyingPx,StrickPx,CallOption=True):
        self.DoY = 365  # Day of Year
        self.InterestRate = InterestRate
        self.Days2Maturity = Days2Maturity
        self.delta_t = (Days2Maturity/StepNumber)/self.DoY       
        self.ulist = [math.exp(x*math.sqrt(self.delta_t)) for x in SigmaList]
        self.dlist = [1.0/x for x in self.ulist]
        self.plist = [(math.exp(InterestRate*self.delta_t)-d)/(u-d) for u,d in zip(self.ulist, self.dlist)]           
        self.UD = np.asarray([self.ulist, self.dlist])
        self.prob_matrix = np.asarray([self.plist, [1.0 - p for p in self.plist]])
        self.binary_list = (bin(i)[2:].zfill(StepNumber) for i in range(2**StepNumber))   
        self.price_list = []
        self.prob_list = []    
        for bn in self.binary_list:
            PxM = 1;
            PrM = 1;
            for idx in range(len(bn)):
                PxM = PxM * self.UD[int(bn[idx]), idx]
                PrM = PrM * self.prob_matrix[int(bn[idx]), idx]
            self.price_list.append(UnderlyingPx*PxM)
            self.prob_list.append(PrM)        
        if CallOption:
            self.value_list = [max(0, p - StrickPx) for p in self.price_list]
        else:
            self.value_list = [max(0, StrickPx - p) for p in self.price_list]     
        
    def option_value (self):
        ExpValueList = [x*y for x, y in zip(self.value_list, self.prob_list)]           
        return sum(ExpValueList) * math.exp((-1.0)*self.InterestRate*(self.Days2Maturity/self.DoY))
