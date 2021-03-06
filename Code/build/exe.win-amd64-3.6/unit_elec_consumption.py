unit_elec_consumption_dictionary = {#  For municipal wastewater treatment processes.
                                    'aerated_grit': {'min': 0.01, 'max': 0.02},
                                    'grinding': {'min': 0, 'max': 0},
                                    'filtration_wastewater': {'min': 0.005, 'max': 0.014},
                                    'grit_removal': {'min': 0.01, 'max': 0.02},
                                    'screening': {'min': 0, 'max': 0},
                                    'wastewater sedimentation': {'min': 0.008, 'max': 0.01},
                                    'activated_sludge': {'min': 0.33, 'max': 0.60},
                                    'aeration': {'min': 0.008, 'max': 0.01},
                                    'clarification': {'min': 0.01, 'max': 0.01},
                                    'lagoon': {'min': 0.09, 'max': 0.29},
                                    'stabilization': {'min': 0.008, 'max': 0.01},
                                    'trickling_filter': {'min': 0.201, 'max': 0.441},
                                    'dechlorination': {'min': 0.03, 'max': 0.15},
                                    'hypochlorination_wastewater': {'min': 2e-5, 'max': 5e-4},
                                    'uv_disinfection_wastewater': {'min': 0.015, 'max': 0.066},
                                    'denitrifcation_nitrification': {'min': 0.08, 'max': 0.09},
                                    'phosphorous_removal': {'min': 0.06, 'max': 0.14},
                                    'aerobic_digestion': {'min': 0.05, 'max': 0.30},
                                    'anaerobic_digestion': {'min': 0.25, 'max': 0.28},
                                    'gravity_thickening': {'min': 0, 'max': 0},
                                    'mechanical_dewatering': {'min': 0.01, 'max': 0.02},
                                    'polymer_dewatering': {'min': 0.15, 'max': 0.15},

                                    #  For drinking water treatment processes.
                                    'flocculation': {'min': 0.008, 'max': 0.022},
                                    'coagulation': {'min': 0.0005, 'max': 0.0014},
                                    'sedimentation': {'min': 0.0005, 'max': 0.001},
                                    'generic_filtration': {'min': 0.005, 'max': 0.014},
                                    'cartridge_filtration': {'min': 0.005, 'max': 0.014},
                                    'diatomaceous_filtration': {'min': 0.005, 'max': 0.014},
                                    'greensand_filtration': {'min': 0.005, 'max': 0.014},
                                    'pressurized_sand_filtration': {'min': 0.005, 'max': 0.014},
                                    'rapid_sand_filtration': {'min': 0.005, 'max': 0.014},
                                    'slow_sand_filtration': {'min': 0.005, 'max': 0.014},
                                    'ultrafiltration': {'min': 0.005, 'max': 0.014},
                                    'hypochlorination_surface': {'min': 2e-5, 'max': 5e-4},
                                    'hypochlorination_groundwater': {'min': 0.002, 'max': 0.002},
                                    'chloramination': {'min': 0.008, 'max': 0.022},
                                    'iodine_addition': {'min': 0.008, 'max': 0.022},
                                    'ozonation': {'min': 0.23, 'max': 0.35},
                                    'uv_disinfection_drinking': {'min': 0.01, 'max': 0.5},
                                    'fluoridation': {'min': 0.008, 'max': 0.022},
                                    'lime_soda_ash_softening': {'min': 0.0085, 'max': 0.023},
                                    'pH_adjustment': {'min': 0.008, 'max': 0.022},
                                    'reducing_agent_addition': {'min': 0.008, 'max': 0.022},
                                    'bimetallic_phosphate_addition': {'min': 0.008, 'max': 0.022},
                                    'hexametaphosphate_addition': {'min': 0.008, 'max': 0.022},
                                    'orthophosphate_addition': {'min': 0.008, 'max': 0.022},
                                    'polyphosphate_addition': {'min': 0.008, 'max': 0.022},
                                    'silicate_addition': {'min': 0.008, 'max': 0.022},
                                    'permaganate_addition': {'min': 0.008, 'max': 0.022},
                                    'sodium_bisulfate_addition': {'min': 0.008, 'max': 0.022},
                                    'sodium_sulfite_addition': {'min': 0.008, 'max': 0.022},
                                    'sulfur_dioxide_addition': {'min': 0.008, 'max': 0.022},
                                    'granular_activated_carbon': {'min': 0.029, 'max': 0.029},
                                    'reverse_osmosis_brackish': {'min': 0.7989, 'max': 2.5},
                                    'reverse_osmosis_seawater': {'min': 2.5, 'max': 6},

                                    #  For industrial wastewater treatment.
                                    'lime_soda_ash_softening_industrial': {'min': 0.0085, 'max': 0.023},
                                    'chemical_addition': {'min': 0.008, 'max': 0.022},
                                    'activated_sludge_industrial': {'min': 0.33, 'max': 0.60},
                                    'aeration_industrial': {'min': 0.008, 'max': 0.01},
                                    'clarification_industrial': {'min': 0.01, 'max': 0.01},
                                    'lagoon_industrial': {'min': 0.09, 'max': 0.29},
                                    'stabilization_industrial': {'min': 0.008, 'max': 0.01},
                                    'trickling_filter_industrial': {'min': 0.201, 'max': 0.441},
                                    'mechanical_vapor_compression': {'min': 7, 'max': 12}, #Al-Karaghouli et al. 2013
                                    'thermal_vapor_compression': {'min': 1.6, 'max': 1.8},  #Al-Karaghouli et al. 2013
                                    'reverse_osmosis_industrial': {'min': 2.5, 'max': 4},
                                    'forward_osmosis': {'min': 2, 'max': 2.5},
                                    'multiple_effect_distillation': {'min': 2, 'max': 2.5},  #Al-Karaghouli et al. 2013
                                    'multistage_flash_distillation': {'min': 2.5, 'max': 5},  #Al-Karaghouli et al. 2013
                                    'membrane_distillation': {'min': 0, 'max': 0},
                                    'crystallization': {'min': 52, 'max': 66}}