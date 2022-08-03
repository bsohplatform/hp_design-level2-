from CoolProp.CoolProp import PropsSI

class Compander_module:
    
    def __init__(self, primary_in, primary_out):
        self.primary_in = primary_in
        self.primary_out = primary_out
    
    def COMP(self, eff_isen: float = 0.7, eff_mech: float = 1.0):    
        while 1:
            h_comp_out_isen = PropsSI('H','P',self.primary_out.p,'S',self.primary_in.s,self.primary_in.fluidmixture)
            self.primary_out.h = (h_comp_out_isen - self.primary_in.h)/eff_isen + self.primary_in.h
            self.primary_out.T = PropsSI('T','H',self.primary_out.h,'P',self.primary_out.p,self.primary_in.fluidmixture)
            try:
                T_comp_out_sat = PropsSI('T','P',self.primary_out.p,'Q',1.0,self.primary_in.fluidmixture)
            except:
                T_comp_out_sat = self.primary_out.T_crit
            if (self.primary_out.T - T_comp_out_sat) > 0.01: # Overhanging problem protection
                break
                    
            
        self.Pspecific = (self.primary_out.h - self.primary_in.h)/eff_mech
            
    def EXPAND(self, eff_isen: float = 0.8, eff_mech: float = 1.0):
        h_expand_out_isen = PropsSI('H','P',self.primary_out.p,'S', self.primary_in.s, self.primary_in.fluidmixture)
        self.primary_out.h = self.primary_in.h - (self.primary_in.h - h_expand_out_isen)*eff_isen
        self.primary_out.T = PropsSI('T','H',self.primary_out.h,'P',self.primary_out.p,self.primary_in.fluidmixture)
        
        self.Pspecific = (self.primary_in.h - self.primary_out.h)*eff_mech