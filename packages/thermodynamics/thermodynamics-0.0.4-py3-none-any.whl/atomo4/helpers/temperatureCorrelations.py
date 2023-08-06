from numpy import exp

class TemperatureCorrelations:
    
    def equation_selector(self,number):
        if(number == '4'):
            return self.eq_4
        
        elif(number == '16'):
            return self.eq_16

        else:
            return None

    def eq_4(self,t,constants):
        a,b,c,d = constants
        return (a+b*t+c*t**2+d*t**3)

    def eq_16(self,t,constants):
        a,b,c,d,e = constants
        return (a+exp(b/t)+c+d*t+e*t**2)
