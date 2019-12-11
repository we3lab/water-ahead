unit_therm_consumption_dictionary = {#  For municipal wastewater treatment processes.
                                    #TODO Find old number on thermal energy consumed to heat anaerobic digesters.
                                    'aerobic_digestion': {'min': 0, 'max': 0},
                                    'anaerobic_digestion_with_biogas': {'min': 0, 'max': 0},
                                    'anaerobic_digestion_without_biogas': {'min': 0.25, 'max': 0.28},

                                    #  For industrial wastewater treatment.
                                    'mechanical_vapor_compression': {'min': 0, 'max':0},
                                    'thermal_vapor_compression': {'min': 227, 'max': 313},  #Al-Karaghouli et al. 2013
                                    'forward_osmosis': {'min': 409, 'max': 500}, #Gingerich and Mauter 2018
                                    'multiple_effect_distillation': {'min': 145, 'max': 230},  #Al-Karaghouli et al. 2013
                                    'multistage_flash_distillation': {'min': 190, 'max': 282},  #Al-Karaghouli et al. 2013
                                    'membrane_distillation': {'min': 1710, 'max': 2000}}