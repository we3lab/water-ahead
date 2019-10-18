from tkinter import *
from tkinter import ttk
import tkinter.simpledialog
import tkinter.messagebox
import os
import numpy as np

from chem_manufacturing_distribution_dictionary import chem_manufacturing_share_dict
from unit_elec_consumption import unit_elec_consumption_dictionary

def menu_option_selected():
    print('Called the callback!')

class Notebook(Frame):
    """Notebook Widget"""

    def __init__(self, parent, activerelief=RAISED, inactiverelief=RIDGE, xpad=4, ypad=6, activefg='black',
                 inactivefg='black', **kw):
        """Construct a Notebook Widget

        Notebook(self, parent, activerelief = RAISED, inactiverelief = RIDGE, xpad = 4, ypad = 6, activefg = 'black', inactivefg = 'black', **kw)

        Valid resource names: background, bd, bg, borderwidth, class,
        colormap, container, cursor, height, highlightbackground,
        highlightcolor, highlightthickness, relief, takefocus, visual, width, activerelief,
        inactiverelief, xpad, ypad.

        xpad and ypad are values to be used as ipady and ipadx
        with the Label widgets that make up the tabs. activefg and inactivefg define what
        color the text on the tabs when they are selected, and when they are not

        """
        # Make various argument available to the rest of the class
        self.activefg = activefg
        self.inactivefg = inactivefg
        self.deletedTabs = []
        self.xpad = xpad
        self.ypad = ypad
        self.activerelief = activerelief
        self.inactiverelief = inactiverelief
        self.kwargs = kw
        self.tabVars = {}  # This dictionary holds the label and frame instances of each tab
        self.tabs = 0  # Keep track of the number of tabs
        self.noteBookFrame = Frame(parent)  # Create a frame to hold everything together
        self.BFrame = Frame(self.noteBookFrame)  # Create a frame to put the "tabs" in
        self.noteBook = Frame(self.noteBookFrame, relief=RAISED, bd=2,
                              **kw)  # Create the frame that will parent the frames for each tab
        self.noteBook.grid_propagate(0)  # self.noteBook has a bad habit of resizing itself, this line prevents that
        Frame.__init__(self)
        self.noteBookFrame.grid()
        self.BFrame.grid(row=0, sticky=W)
        self.noteBook.grid(row=1, column=0, columnspan=27)

    def change_tab(self, IDNum):
        """Internal Function"""

        for i in (a for a in range(0, len(self.tabVars.keys()))):
            if i not in self.deletedTabs:  # Make sure tab hasn't been deleted
                if i != IDNum:  # Check to see if the tab is the one that is currently selected
                    self.tabVars[i][1].grid_remove()  # Remove the Frame corresponding to each tab that is not selected
                    self.tabVars[i][0][
                        'relief'] = self.inactiverelief  # Change the relief of all tabs that are not selected to "Groove"
                    self.tabVars[i][0][
                        'fg'] = self.inactivefg  # Set the fg of the tab, showing it is selected, default is black
                else:  # When on the tab that is currently selected...
                    self.tabVars[i][1].grid()  # Re-grid the frame that corresponds to the tab
                    self.tabVars[IDNum][0][
                        'relief'] = self.activerelief  # Change the relief to "Raised" to show the tab is selected
                    self.tabVars[i][0][
                        'fg'] = self.activefg  # Set the fg of the tab, showing it is not selected, default is black

    def add_tab(self, width=2, **kw):
        """Creates a new tab, and returns it's corresponding frame

        """

        temp = self.tabs  # Temp is used so that the value of self.tabs will not throw off the argument sent by the label's event binding
        self.tabVars[self.tabs] = [Label(self.BFrame, relief=RIDGE, **kw)]  # Create the tab
        self.tabVars[self.tabs][0].bind("<Button-1>", lambda Event: self.change_tab(temp))  # Makes the tab "clickable"
        self.tabVars[self.tabs][0].pack(side=LEFT, ipady=self.ypad,
                                        ipadx=self.xpad)  # Packs the tab as far to the left as possible
        self.tabVars[self.tabs].append(
            Frame(self.noteBook, **self.kwargs))  # Create Frame, and append it to the dictionary of tabs
        self.tabVars[self.tabs][1].grid(row=0, column=0)  # Grid the frame ontop of any other already existing frames
        self.change_tab(0)  # Set focus to the first tab
        self.tabs += 1  # Update the tab count
        return self.tabVars[temp][1]  # Return a frame to be used as a parent to other widgets

    def destroy_tab(self, tab):
        """Delete a tab from the notebook, as well as it's corresponding frame

        """

        self.iteratedTabs = 0  # Keep track of the number of loops made
        for b in self.tabVars.values():  # Iterate through the dictionary of tabs
            if b[1] == tab:  # Find the NumID of the given tab
                b[0].destroy()  # Destroy the tab's frame, along with all child widgets
                self.tabs -= 1  # Subtract one from the tab count
                self.deletedTabs.append(
                    self.iteratedTabs)  # Apend the NumID of the given tab to the list of deleted tabs
                break  # Job is done, exit the loop
            self.iteratedTabs += 1  # Add one to the loop count

    def focus_on(self, tab):
        """Locate the IDNum of the given tab and use
        change_tab to give it focus

        """

        self.iteratedTabs = 0  # Keep track of the number of loops made
        for b in self.tabVars.values():  # Iterate through the dictionary of tabs
            if b[1] == tab:  # Find the NumID of the given tab
                self.change_tab(
                    self.iteratedTabs)  # send the tab's NumID to change_tab to set focus, mimicking that of each tab's event bindings
                break  # Job is done, exit the loop
            self.iteratedTabs += 1  # Add one to the loop count


def main():
    def adjustCanvas(someVariable=None):
        fontLabel["font"] = ("arial", var.get())

    def combine_funcs(*funcs):
        """"Combines function for the command."""
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)

        return combined_func

    def calculate_electricity_consumption(flocculation, flocculation_installed, coagulation, coagulation_installed,
                                          sedimentation, sedimentation_installed, filtration, primary_disinfection,
                                          secondary_disinfection, fluoridation, softening, ph_adjustment,
                                          ph_adjustment_installed, granular_activated_carbon,
                                          granular_activated_carbon_installed, reverse_osmosis,
                                          reverse_osmosis_installed, corrosion_control, aerated_grit,
                                          aerated_grit_installed, grinding, grit_removal, grit_removal_installed,
                                          screening, screening_installed, secondary_treatment,
                                          nitrification_denitrification, nitrification_denitrification_installed,
                                          phosphorous_removal, phosphorous_removal_installed, disinfection,
                                          dechlorination, digestion, dewatering, softening_process,
                                          chemical_addition_input, bio_treatment, bio_treatment_installed,
                                          volume_reduction, volume_reduction_installed, crystallization,
                                          new_elec_min_input, new_elec_best_input, new_elec_max_input, runs):
        if (reverse_osmosis == 1) and (system_type == 'Drinking Water System'):
            if source_water == 'Seawater':
                volume_scale_factor = 1/0.5
            else:
                volume_scale_factor = 1/0.85
        else:
            volume_scale_factor = 1

        if system_type == 'Municipal Wasteawter System':
            if secondary_treatment == 'None':
                tertiary_treatment_scale_factor = 1
                solids_processing_scale_factor = 0
            else:
                tertiary_treatment_scale_factor = 0.95
                solids_processing_scale_factor = 0.05

        if system_type == 'Industrial Wastewater System':
            if volume_reduction == 'None':
                crystallization_scale_factor = 1
            else:
                crystallization_scale_factor = 0.67

        if flocculation == 1:
            flocculation_electricity = np.random.uniform(unit_elec_consumption_dictionary['flocculation']['min'],
                                                            unit_elec_consumption_dictionary['flocculation']['max'],
                                                            (runs, flocculation_installed)) * volume_scale_factor
        else:
            flocculation_electricity = np.zeros(runs)
        if coagulation == 1:
            coagulation_electricity = np.random.uniform(unit_elec_consumption_dictionary['coagulation']['min'],
                                                            unit_elec_consumption_dictionary['coagulation']['max'],
                                                            (runs, coagulation_installed)) * volume_scale_factor
        else:
            coagulation_electricity  = np.zeros(runs)
        if sedimentation == 1:
            sedimentation_electricity = np.random.uniform(unit_elec_consumption_dictionary['sedimentation']['min'],
                                                           unit_elec_consumption_dictionary['sedimentation']['max'],
                                                           (runs, sedimentation_installed)) * volume_scale_factor
        else:
            sedimentation_electricity  = np.zeros(runs)

        if filtration == 'Generic':
            filtration_electricity = np.random.uniform(unit_elec_consumption_dictionary['generic_filtration']['min'],
                                                       unit_elec_consumption_dictionary['generic_filtration']['max'],
                                                       (runs,1)) * volume_scale_factor
        elif filtration == 'Cartridge':
                filtration_electricity = np.random.uniform(unit_elec_consumption_dictionary['cartridge_filtration']['min'],
                    unit_elec_consumption_dictionary['cartridge_filtration']['max'], (runs, 1)) * volume_scale_factor
        elif filtration == 'Diatomaceous Earth':
                filtration_electricity = np.random.uniform(unit_elec_consumption_dictionary['diatomaceous_filtration']['min'],
                    unit_elec_consumption_dictionary['diatomaceous_filtration']['max'], (runs, 1)) * volume_scale_factor
        elif filtration == 'Greensand':
                filtration_electricity = np.random.uniform(unit_elec_consumption_dictionary['greensand_filtration']['min'],
                    unit_elec_consumption_dictionary['greensand_filtration']['max'], (runs, 1)) * volume_scale_factor
        elif filtration == 'Pressurized Sand':
                filtration_electricity = np.random.uniform(unit_elec_consumption_dictionary['pressurized_sand_filtration']['min'],
                    unit_elec_consumption_dictionary['pressurized_sand_filtration']['max'], (runs, 1)) * volume_scale_factor
        elif filtration == 'Rapid Sand':
            filtration_electricity = np.random.uniform(unit_elec_consumption_dictionary['rapid_sand_filtration']['min'],
                                                       unit_elec_consumption_dictionary['rapid_sand_filtration']['max'],
                                                       (runs, 1)) * volume_scale_factor
        elif filtration == 'Slow Sand':
            filtration_electricity = np.random.uniform(unit_elec_consumption_dictionary['slow_sand_filtration']['min'],
                unit_elec_consumption_dictionary['slow_sand_filtration']['max'], (runs, 1)) * volume_scale_factor
        elif filtration == 'Ultrafiltration Membrane':
            filtration_electricity = np.random.uniform(unit_elec_consumption_dictionary['ultrafiltration']['min'],
                                                       unit_elec_consumption_dictionary['ultrafiltration']['max'],
                                                       (runs, 1)) * volume_scale_factor
        else:
            filtration_electricity  = np.zeros(runs)

        if (primary_disinfection == 'Hypochlorite') and (source_water == "Fresh Surface Water"):
            primary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['hypochlorination_surface']['min'],
                                                       unit_elec_consumption_dictionary['hypochlorination_surface']['max'],
                                                       (runs, 1))
        elif primary_disinfection == 'Hypochlorite' and (source_water == "Fresh Groundwater"):
            primary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['hypochlorination_groundwater']['min'],
                    unit_elec_consumption_dictionary['hypochlorination_groundwater']['max'], (runs, 1))
        elif primary_disinfection == 'Hypochlorite' and (source_water == "Brackish Groundwater"):
            primary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['hypochlorination_groundwater']['min'],
                    unit_elec_consumption_dictionary['hypochlorination_groundwater']['max'], (runs, 1))
        elif primary_disinfection == 'Hypochlorite' and (source_water == "Seawater"):
            primary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['hypochlorination_surface']['min'],
                    unit_elec_consumption_dictionary['hypochlorination_surface']['max'], (runs, 1))
        elif primary_disinfection == 'Chloramine':
            primary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['chloramination']['min'],
                    unit_elec_consumption_dictionary['chloramination']['max'], (runs, 1))
        elif primary_disinfection == 'Iodine':
            primary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['iodine_addition']['min'],
                                                       unit_elec_consumption_dictionary['iodine_addition']['max'],
                                                       (runs, 1))
        elif primary_disinfection == 'Ozonation':
            primary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['ozonation']['min'],
                unit_elec_consumption_dictionary['ozonation']['max'], (runs, 1))
        elif filtration == 'UV Disinfection':
            primary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['uv_disinfection_drinking']['min'],
                                                       unit_elec_consumption_dictionary['uv_disinfection_drinking']['max'],
                                                       (runs, 1))
        else:
            primary_disinfection_electricity = np.zeros(runs)

        if (secondary_disinfection == 'Hypochlorite') and (source_water == "Fresh Surface Water"):
            secondary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['hypochlorination_surface']['min'],
                                                       unit_elec_consumption_dictionary['hypochlorination_surface']['max'],
                                                       (runs, 1))
        elif secondary_disinfection == 'Hypochlorite' and (source_water == "Fresh Groundwater"):
            secondary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['hypochlorination_groundwater']['min'],
                    unit_elec_consumption_dictionary['hypochlorination_groundwater']['max'], (runs, 1))
        elif secondary_disinfection == 'Hypochlorite' and (source_water == "Brackish Groundwater"):
            secondary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['hypochlorination_groundwater']['min'],
                    unit_elec_consumption_dictionary['hypochlorination_groundwater']['max'], (runs, 1))
        elif secondary_disinfection == 'Hypochlorite' and (source_water == "Seawater"):
            secondary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['hypochlorination_surface']['min'],
                    unit_elec_consumption_dictionary['hypochlorination_surface']['max'], (runs, 1))
        elif secondary_disinfection == 'Chloramine':
            secondary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['chloramination']['min'],
                    unit_elec_consumption_dictionary['chloramination']['max'], (runs, 1))
        else:
            secondary_disinfection_electricity = np.zeros(runs)

        if fluoridation == 1:
            fluoridation_electricity = np.random.uniform(unit_elec_consumption_dictionary['fluoridation']['min'],
                                                           unit_elec_consumption_dictionary['fluoridation']['max'],
                                                           (runs, 1))
        else:
            fluoridation_electricity  = np.zeros(runs)

        if softening == 1:
            softening_electricity = np.random.uniform(unit_elec_consumption_dictionary['lime_soda_ash_softening']['min'],
                                                           unit_elec_consumption_dictionary['lime_soda_ash_softening']['max'],
                                                           (runs, 1)) * volume_scale_factor
        else:
            softening_electricity = np.zeros(runs)

        if ph_adjustment == 1:
            ph_adjustment_electricity = np.random.uniform(unit_elec_consumption_dictionary['pH_adjustment']['min'],
                                                           unit_elec_consumption_dictionary['pH_adjustment']['max'],
                                                           (runs, ph_adjustment_installed))
        else:
            ph_adjustment_electricity  = np.zeros(runs)

        if granular_activated_carbon == 1:
            granular_activated_carbon_electricity = np.random.uniform(unit_elec_consumption_dictionary['granular_activated_carbon']['min'],
                                                           unit_elec_consumption_dictionary['granular_activated_carbon']['max'],
                                                           (runs, granular_activated_carbon_installed)) * volume_scale_factor
        else:
            granular_activated_carbon_electricity  = np.zeros(runs)

        if (reverse_osmosis == 1) and (source_water == 'Brackish Groundwater'):
            reverse_osmosis_electricity = np.random.uniform(unit_elec_consumption_dictionary['reverse_osmosis_brackish']['min'],
                                                           unit_elec_consumption_dictionary['reverse_osmosis_brackish']['max'],
                                                           (runs, reverse_osmosis_installed))
        elif (reverse_osmosis == 1) and (source_water == 'Seawater'):
            reverse_osmosis_electricity = np.random.uniform(unit_elec_consumption_dictionary['reverse_osmosis_seawater']['min'],
                unit_elec_consumption_dictionary['reverse_osmosis_seawater']['max'],
                (runs, reverse_osmosis_installed))
        elif (reverse_osmosis == 1) and (system_type == 'Industrial Wastewater Treatment'):
            reverse_osmosis_electricity = np.random.uniform(unit_elec_consumption_dictionary['reverse_osmosis_industrial']['min'],
                unit_elec_consumption_dictionary['reverse_osmosis_industrial']['max'],
                (runs, reverse_osmosis_installed))
        else:
            reverse_osmosis_electricity = np.zeros(runs)

        if corrosion_control == 'None':
            corrosion_control_electricity = np.zeros(runs)
        else:
            corrosion_control_electricity =np.random.uniform(unit_elec_consumption_dictionary['bimetallic_phosphate_addition']['min'],
                                                             unit_elec_consumption_dictionary['bimetallic_phosphate_addition']['max'],
                                                             (runs,1))

        if aerated_grit == 1:
            aerated_grit_electricity = np.random.uniform(unit_elec_consumption_dictionary['aerated_grit_electricity']['min'],
                                                           unit_elec_consumption_dictionary['aerated_grit_electricity']['max'],
                                                           (runs, aerated_grit_installed))
        else:
            aerated_grit_electricity  = np.zeros(runs)

        if grinding == 1:
            grinding_electricity = np.random.uniform(unit_elec_consumption_dictionary['grinding']['min'],
                                                           unit_elec_consumption_dictionary['grinding']['max'],
                                                           (runs, 1))
        else:
            grinding_electricity  = np.zeros(runs)

        if grit_removal == 1:
            grit_removal_electricity = np.random.uniform(unit_elec_consumption_dictionary['grit_removal']['min'],
                                                           unit_elec_consumption_dictionary['grit_removal']['max'],
                                                           (runs, grit_removal_installed))
        else:
            grit_removal_electricity  = np.zeros(runs)

        if screening == 1:
            screening_electricity = np.random.uniform(unit_elec_consumption_dictionary['screening']['min'],
                                                           unit_elec_consumption_dictionary['screening']['max'],
                                                           (runs, screening_installed))
        else:
            screening_electricity  = np.zeros(runs)

        if secondary_treatment == 'Activated Sludge and Clarification':
            secondary_treatment_electricity = np.random.uniform(unit_elec_consumption_dictionary['activated_sludge']['min'],
                                                       unit_elec_consumption_dictionary['activatd_sludge']['max'],
                                                       (runs, 1)) + \
                                              np.random.uniform(unit_elec_consumption_dictionary['aeration']['min'],
                                                       unit_elec_consumption_dictionary['aeration']['max'],
                                                       (runs, 1)) + \
                                              np.random.uniform(unit_elec_consumption_dictionary['clarification']['min'],
                                                       unit_elec_consumption_dictionary['clarification']['max'],
                                                       (runs, 1))
        elif secondary_treatment == 'Lagoon':
            secondary_treatment_electricity = np.random.uniform(unit_elec_consumption_dictionary['lagoon']['min'],
                    unit_elec_consumption_dictionary['lagoon']['max'], (runs, 1))
        elif secondary_treatment == 'Stabilization Pond':
            secondary_treatment_electricity = np.random.uniform(unit_elec_consumption_dictionary['stabilization']['min'],
                    unit_elec_consumption_dictionary['stabilization']['max'], (runs, 1))
        elif secondary_treatment == 'Trickling Filter':
            secondary_treatment_electricity = np.random.uniform(unit_elec_consumption_dictionary['trickling_filter']['min'],
                    unit_elec_consumption_dictionary['tricklking_filter']['max'], (runs, 1))
        else:
            secondary_treatment_electricity  = np.zeros(runs)

        if nitrification_denitrification == 1:
            nitrification_denitrification_electricity = np.random.uniform(unit_elec_consumption_dictionary['nitrification_denitrification']['min'],
                                                           unit_elec_consumption_dictionary['nitrification_denitrification']['max'],
                                                           (runs, nitrification_denitrification_installed)) * tertiary_treatment_scale_factor
        else:
            nitrification_denitrification_electricity  = np.zeros(runs)

        if phosphorous_removal == 1:
            phosphorous_removal_electricity = np.random.uniform(unit_elec_consumption_dictionary['phosphorous_removal']['min'],
                                                           unit_elec_consumption_dictionary['phosphorous_removal']['max'],
                                                           (runs, phosphorous_removal_installed)) * tertiary_treatment_scale_factor
        else:
            phosphorous_removal_electricity  = np.zeros(runs)

        if disinfection == 'Hypochlorite':
            disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['hypochlorination_wastewater']['min'],
                    unit_elec_consumption_dictionary['hypochlorination_wastewater']['max'], (runs, 1)) * tertiary_treatment_scale_factor
        elif disinfection == 'Ultraviolet':
            disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['uv_disinfection_wastewater']['min'],
                    unit_elec_consumption_dictionary['uv_disinfection_wastewater']['max'], (runs, 1)) * tertiary_treatment_scale_factor
        elif disinfection == 'Ozone':
            disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['ozonation']['min'],
                    unit_elec_consumption_dictionary['ozonation']['max'], (runs, 1)) * tertiary_treatment_scale_factor
        else:
            disinfection_electricity = np.zeros(runs)

        if dechlorination == 1:
            dechlorination_electricity = np.random.uniform(unit_elec_consumption_dictionary['dechlorination']['min'],
                                                           unit_elec_consumption_dictionary['dechlorination']['max'],
                                                           (runs, 1)) * tertiary_treatment_scale_factor
        else:
            dechlorination_electricity  = np.zeros(runs)

        if digestion == 'Aerobic Digestion':
            disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['aerobic_digestion']['min'],
                    unit_elec_consumption_dictionary['aerobic_digestion']['max'], (runs, 1)) * solids_processing_scale_factor
        elif digestion == 'Anaerobic Digestion w/ Biogas Use':
            disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['anaerobic_digestion']['min'],
                    unit_elec_consumption_dictionary['anaerobic_digestion']['max'], (runs, 1)) * solids_processing_scale_factor
        # TODO Add biogas recovery to below estimates.
        elif digestion == 'Anaerobic Digestion w/o Biogas Use':
            disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['anaerobic_digestion']['min'],
                    unit_elec_consumption_dictionary['anaerobic_digestion']['max'], (runs, 1)) * solids_processing_scale_factor
        else:
            digestion_electricity = np.zeros(runs)

        if dewatering == 'Gravity Thickening':
            dewatering_electricity = np.random.uniform(unit_elec_consumption_dictionary['gravity_thickening']['min'],
                    unit_elec_consumption_dictionary['gravity_thickening']['max'], (runs, 1)) * solids_processing_scale_factor
        elif dewatering == 'Mechanical Dewatering':
            dewatering_electricity = np.random.uniform(unit_elec_consumption_dictionary['mechanical_dewatering']['min'],
                    unit_elec_consumption_dictionary['mechanical_dewatering']['max'], (runs, 1)) * solids_processing_scale_factor
        elif dewatering == 'Polymer Dewatering':
            dewatering_electricity = np.random.uniform(unit_elec_consumption_dictionary['polymer_dewatering']['min'],
                    unit_elec_consumption_dictionary['poiymer_dewatering']['max'], (runs, 1)) * solids_processing_scale_factor
        else:
            dewatering_electricity = np.zeros(runs)

        if softening_process == 1:
            softening_process_electricity = np.random.uniform(unit_elec_consumption_dictionary['softening']['min'],
                                                           unit_elec_consumption_dictionary['softening']['max'],
                                                           (runs, 1))
        else:
            softening_process_electricity  = np.zeros(runs)

        if chemical_addition_input == 1:
            chemical_addition_input_electricity = np.random.uniform(unit_elec_consumption_dictionary['chemical_addition']['min'],
                                                           unit_elec_consumption_dictionary['chemical_addition']['max'],
                                                           (runs, 1))
        else:
            chemical_addition_input_electricity  = np.zeros(runs)

        if bio_treatment == 'Activated Sludge and Clarification':
            bio_treatment_electricity = np.random.uniform(unit_elec_consumption_dictionary['activated_sludge_industrial']['min'],
                                                       unit_elec_consumption_dictionary['activatd_sludge_industrial']['max'],
                                                       (runs, bio_treatment_installed)) + \
                                              np.random.uniform(unit_elec_consumption_dictionary['aeration_industrial']['min'],
                                                       unit_elec_consumption_dictionary['aeration_industrial']['max'],
                                                       (runs, bio_treatment_installed)) + \
                                              np.random.uniform(unit_elec_consumption_dictionary['clarification_industrial']['min'],
                                                       unit_elec_consumption_dictionary['clarification_industrial']['max'],
                                                       (runs, bio_treatment_installed))
        elif bio_treatment == 'Lagoon':
            bio_treatment_electricity = np.random.uniform(unit_elec_consumption_dictionary['lagoon_industrial']['min'],
                    unit_elec_consumption_dictionary['lagoon_industrial']['max'], (runs, bio_treatment_installed))
        elif bio_treatment == 'Stabilization Pond':
            bio_treatment_electricity = np.random.uniform(unit_elec_consumption_dictionary['stabilization_industrial']['min'],
                    unit_elec_consumption_dictionary['stabilization_industrial']['max'], (runs, bio_treatment_installed))
        elif bio_treatment == 'Trickling Filter':
            bio_treatment_electricity = np.random.uniform(unit_elec_consumption_dictionary['trickling_filter_industrial']['min'],
                    unit_elec_consumption_dictionary['tricklking_filter_industrial']['max'], (runs, bio_treatment_installed))
        else:
            bio_treatment_electricity = np.zeros(runs)


        if volume_reduction == 'Mechanical Vapor Compression':
            volume_reduction_electricity = np.random.uniform(unit_elec_consumption_dictionary['mechanical_vapor_compression']['min'],
                                                       unit_elec_consumption_dictionary['mechanical_vapor_compression']['max'],
                                                       (runs, volume_reduction_installed))
        elif volume_reduction == 'Thermal Vapor Compression':
                volume_reduction_electricity = np.random.uniform(unit_elec_consumption_dictionary['thermal_vapor_compression']['min'],
                    unit_elec_consumption_dictionary['thermal_vapor_compression']['max'], (runs, 1))
        elif volume_reduction == 'Reverse Osmosis':
                volume_reduction_electricity = np.random.uniform(unit_elec_consumption_dictionary['reverse_osmosis_industrial']['min'],
                    unit_elec_consumption_dictionary['reverse_osmosis_industrial']['max'], (runs, 1))
        elif volume_reduction == 'Forward Osmosis':
                volume_reduction_electricity = np.random.uniform(unit_elec_consumption_dictionary['forward_osmosis']['min'],
                    unit_elec_consumption_dictionary['forward_osmosis']['max'], (runs, 1))
        elif volume_reduction == 'Multiple-Effect Distillation':
                volume_reduction_electricity = np.random.uniform(unit_elec_consumption_dictionary['multiple_effect_distillation']['min'],
                    unit_elec_consumption_dictionary['multiple_effect_distillation']['max'], (runs, 1))
        elif volume_reduction == 'Multi-Stage Flash Distillation':
            volume_reduction_electricity = np.random.uniform(unit_elec_consumption_dictionary['multistage_flash_distillation']['min'],
                                                       unit_elec_consumption_dictionary['multistage_flash_distillation']['max'],
                                                       (runs, 1))
        elif volume_reduction == 'Membrane Distillation':
            volume_reduction_electricity = np.random.uniform(unit_elec_consumption_dictionary['membrane_distillation']['min'],
                unit_elec_consumption_dictionary['membrane_distillation']['max'], (runs, 1))
        else:
            volume_reduction_electricity = np.zeros(runs)

        if crystallization == 1:
            crystallization_electricity = np.random.uniform(unit_elec_consumption_dictionary['crystallization']['min'],
                                                           unit_elec_consumption_dictionary['crystallization']['max'],
                                                           (runs, 1))* crystallization_scale_factor
        else:
            crystallization_electricity = np.zeros(runs)

        new_process_electricity = np.random.triangular(new_elec_min_input, new_elec_best_input,
                                                             new_elec_max_input, runs)

        total_electricity_consumption = flocculation_electricity + coagulation_electricity  + \
                                        sedimentation_electricity  + filtration_electricity + \
                                        primary_disinfection_electricity + secondary_disinfection_electricity + \
                                        fluoridation_electricity + softening_electricity + ph_adjustment_electricity + \
                                        granular_activated_carbon_electricity + reverse_osmosis_electricity + \
                                        corrosion_control_electricity + aerated_grit_electricity + \
                                        grinding_electricity + grit_removal_electricity + screening_electricity + \
                                        secondary_treatment_electricity + nitrification_denitrification_electricity \
                                        + phosphorous_removal_electricity + disinfection_electricity + \
                                        dechlorination_electricity + digestion_electricity + dewatering_electricity + \
                                        softening_process_electricity + chemical_addition_input_electricity + \
                                        bio_treatment_electricity + volume_reduction_electricity + \
                                        crystallization_electricity + new_process_electricity

        return total_electricity_consumption

    #Create the notebook.
    root = Tk()

    root.title("Water AHEAD")
    note = Notebook(root, width=600, height=500, activefg='black', inactivefg='gray')  # Create a Note book Instance
    note.grid()
    tab1 = note.add_tab(text='General Properties')  # Create an overview tab.
    tab2 = note.add_tab(text='Geography')  # Create a tab to ask about the system geography (i.e., where is it located  or will you be using nationwide averages?)
    tab3 = note.add_tab(text='Baseline Treatment Process')  # Create a tab with the text "Tab Three"
    tab4 = note.add_tab(text='New Treatment Process')  # Create a tab with the text "Tab Four"
    tab5 = note.add_tab(text='Results')  # Create a tab with the text "Tab Five"

    def callback(P):
        if str.isalpha(P):
            return False
        else:
            return True

    vcmd = (tab1.register(callback))

    Label(tab3, text='Drinking Water System', font=('Arial', 10, 'bold')).grid(column=0, row=0, columnspan=3)

    Label(tab3, text='Source Water Type:', font=('Arial', 10)).grid(column=0, row=1, sticky=E)
    source_water = StringVar(root)
    source_water_choices = ['Fresh Surface Water', 'Fresh Groundwater', 'Brackish Groundwater', 'Seawater']
    source_water.set('Fresh Surface Water')
    source_water_type_popup_menu = OptionMenu(tab3, source_water, *source_water_choices).grid(column=1, row=1, sticky=W)

    Label(tab3, text='Number of Processes Installed', font=('Arial', 10, 'bold')).grid(column=2, row=1)
    Label(tab3, text='Preliminary Treatment:', font=('Arial', 10)).grid(column=0, row=3, sticky=E)

    flocculation = BooleanVar(root)
    flocculation_button = Checkbutton(tab3, text='Flocculation', variable=flocculation).grid(column=1, row=2, sticky=W)
    flocculation_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    flocculation_installed.grid(column=2, row=2)

    coagulation = BooleanVar(root)
    coagulation_button = Checkbutton(tab3, text='Coagulation', variable=coagulation).grid(column=1, row=3, sticky=W)
    coagulation_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    coagulation_installed.grid(column=2, row=3)

    sedimentation = BooleanVar(root)
    sedimentation_button = Checkbutton(tab3, text='Sedimentation', variable=sedimentation).grid(column=1, row=4,
                                                                                                sticky=W)
    sedimentation_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    sedimentation_installed.grid(column=2, row=4)

    Label(tab3, text='Filtration:', font=('Arial', 10)).grid(column=0, row=5, sticky=E)
    filtration = StringVar(root)
    filtration_choices = ['No Filtration', 'Generic', 'Cartridge', 'Diatomaceous Earth', 'Greensand',
                          'Pressurized Sand', 'Rapid Sand', 'Slow Sand', 'Ultrafiltration Membrane']
    filtration.set('Generic')
    filtration_popup_menu = OptionMenu(tab3, filtration, *filtration_choices).grid(column=1, row=5, sticky=W)
    filtration_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    filtration_installed.grid(column=2, row=5)

    Label(tab3, text='Primary Disinfection:', font=('Arial', 10)).grid(column=0, row=6, sticky=E)
    primary_disinfection = StringVar(root)
    primary_disinfection_choices = ['Hypochlorite', 'Chloramine', 'Iodine', 'Ozonation', 'UV Disinfection', 'None']
    primary_disinfection.set('Hypochlorite')
    primary_disinfection_popup_menu = OptionMenu(tab3, primary_disinfection, *primary_disinfection_choices).grid(
        column=1, row=6, sticky=W)

    Label(tab3, text='Secondary Disinfection:', font=('Arial', 10)).grid(column=0, row=7, sticky=E)
    secondary_disinfection = StringVar(root)
    secondary_disinfection_choices = ['Hypochlorite', 'Chloramine', 'None']
    secondary_disinfection.set('Hypochlorite')
    secondary_disinfection_popup_menu = OptionMenu(tab3, secondary_disinfection, *secondary_disinfection_choices).grid(
        column=1, row=7, sticky=W)

    Label(tab3, text='Advanced Processes:', font=('Arial', 10)).grid(column=0, row=8, sticky=E)

    fluoridation = BooleanVar(root)
    fluoridation_button = Checkbutton(tab3, text='Fluoridation', variable=fluoridation).grid(column=1, row=8, sticky=W)

    softening = BooleanVar(root)
    softening_button = Checkbutton(tab3, text='Soda Ash Softening', variable=softening).grid(column=1, row=9, sticky=W)

    ph_adjustment = BooleanVar(root)
    ph_adjustment_button = Checkbutton(tab3, text='pH Adjustment', variable=ph_adjustment).grid(column=1, row=10,
                                                                                                sticky=W)
    ph_adjustment_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    ph_adjustment_installed.grid(column=2, row=10)

    granular_activated_carbon = BooleanVar(root)
    granular_activated_carbon_button = Checkbutton(tab3, text='Granular Activated Carbon',
                                                   variable=granular_activated_carbon).grid(column=1, row=11, sticky=W)
    granular_activated_carbon_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    granular_activated_carbon_installed.grid(column=2, row=11)

    reverse_osmosis = BooleanVar(root)
    reverse_osmosis_button = Checkbutton(tab3, text='Reverse Osmosis', variable=reverse_osmosis).grid(column=1, row=12,
                                                                                                      sticky=W)
    reverse_osmosis_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    reverse_osmosis_installed.grid(column=2, row=12)

    Label(tab3, text='Corrosion Control:', font=('Arial', 10)).grid(column=0, row=13, sticky=E)
    corrosion_control = StringVar(root)
    corrosion_control_choices = ['Bimetallic Phosphate', 'Hexametaphosphate', 'Orthophosphate', 'Polyphosphate',
                                 'Silicate', 'Permagnate', 'Sodium Bisulfate', 'Sodium Sulfate',
                                 'Sulfur Dioxide', 'None']
    corrosion_control.set('None')
    corrosion_control_popup_menu = OptionMenu(tab3, corrosion_control, *corrosion_control_choices).grid(column=1,
                                                                                                        row=13,
                                                                                                        sticky=W)

    Label(tab1, text='System Parameters',font=('Arial', 10, 'bold')).grid(row=0, column=1)  # Use each created tab as a parent, etc etc...
    Label(tab1, text='System Type:', font=('Arial', 10)).grid(row=1, column=0, sticky=E)
    Label(tab1, text='System Size:', font=('Arial', 10)).grid(row=2, column=0, sticky=E)

    system_type = StringVar(root)
    system_type_choices = ['Drinking Water System', 'Municipal Wastewater System', 'Industrial Wastewater System']
    system_type.set('Drinking Water System')
    system_type_popup_menu = OptionMenu(tab1, system_type, *system_type_choices).grid(row=1, column=1)

    def change_dropdown(*args):
        selected_system_type = system_type.get()
        print(selected_system_type)

    def all_children(window):
        _list = window.winfo_children()

        for item in _list:
            if item.winfo_children():
                _list.extend(item.winfo_children())

        return _list

    def change_value(value):
        value_updated = value.get()

        return value_updated

    def change_dropdown_change_window(*args):
        tab3_list = all_children(tab3)
        for item in tab3_list:
            item.grid_forget()
        if system_type.get() == 'Drinking Water System':
            Label(tab3, text='Drinking Water System', font=('Arial', 10, 'bold')).grid(column=0, row=0, columnspan=3)

            Label(tab3, text='Source Water Type:', font=('Arial', 10)).grid(column=0, row=1, sticky=E)
            source_water = StringVar(root)
            source_water_choices = ['Fresh Surface Water', 'Fresh Groundwater', 'Brackish Groundwater', 'Seawater']
            source_water.set('Fresh Surface Water')
            source_water_type_popup_menu = OptionMenu(tab3, source_water, *source_water_choices).grid(column=1, row=1, sticky=W)

            Label(tab3, text='Number of Processes Installed', font=('Arial', 10, 'bold')).grid(column=2, row=1)
            Label(tab3, text='Preliminary Treatment:', font=('Arial', 10)).grid(column=0, row=3, sticky=E)

            flocculation = BooleanVar(root)
            flocculation_button = Checkbutton(tab3, text='Flocculation', variable=flocculation).grid(column=1, row=2, sticky=W)
            flocculation_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            flocculation_installed.grid(column=2, row=2)

            coagulation = BooleanVar(root)
            coagulation_button = Checkbutton(tab3, text='Coagulation', variable=coagulation).grid(column=1, row=3, sticky=W)
            coagulation_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            coagulation_installed.grid(column=2, row=3)

            sedimentation = BooleanVar(root)
            sedimentation_button = Checkbutton(tab3, text='Sedimentation', variable=sedimentation).grid(column=1, row=4, sticky=W)
            sedimentation_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            sedimentation_installed.grid(column=2, row=4)

            Label(tab3, text='Filtration:', font=('Arial', 10)).grid(column=0, row=5, sticky=E)
            filtration = StringVar(root)
            filtration_choices = ['No Filtration', 'Generic', 'Cartridge', 'Diatomaceous Earth', 'Greensand',
                                  'Pressurized Sand', 'Rapid Sand', 'Slow Sand', 'Ultrafiltration Membrane']
            filtration.set('Generic')
            filtration_popup_menu = OptionMenu(tab3, filtration, *filtration_choices).grid(column=1, row=5, sticky=W)
            filtration_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            filtration_installed.grid(column=2, row=5)

            Label(tab3, text='Primary Disinfection:', font=('Arial', 10)).grid(column=0, row=6, sticky=E)
            primary_disinfection = StringVar(root)
            primary_disinfection_choices = ['Hypochlorite', 'Chloramine', 'Iodine', 'Ozonation', 'UV Disinfection', 'None']
            primary_disinfection.set('Hypochlorite')
            primary_disinfection_popup_menu = OptionMenu(tab3, primary_disinfection, *primary_disinfection_choices).grid(column=1, row=6, sticky=W)

            Label(tab3, text='Secondary Disinfection:', font=('Arial', 10)).grid(column=0, row=7, sticky=E)
            secondary_disinfection = StringVar(root)
            secondary_disinfection_choices = ['Hypochlorite', 'Chloramine', 'None']
            secondary_disinfection.set('Hypochlorite')
            secondary_disinfection_popup_menu = OptionMenu(tab3, secondary_disinfection, *secondary_disinfection_choices).grid(column=1, row=7, sticky=W)

            Label(tab3, text='Advanced Processes:', font=('Arial', 10)).grid(column=0, row=8, sticky=E)

            fluoridation = BooleanVar(root)
            fluoridation_button = Checkbutton(tab3, text='Fluoridation', variable=fluoridation).grid(column=1, row=8, sticky=W)

            softening = BooleanVar(root)
            softening_button = Checkbutton(tab3, text='Soda Ash Softening', variable=softening).grid(column=1, row=9, sticky=W)

            ph_adjustment = BooleanVar(root)
            ph_adjustment_button = Checkbutton(tab3, text='pH Adjustment', variable=ph_adjustment).grid(column=1, row=10, sticky=W)
            ph_adjustment_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            ph_adjustment_installed.grid(column=2, row=10)

            granular_activated_carbon = BooleanVar(root)
            granular_activated_carbon_button = Checkbutton(tab3, text='Granular Activated Carbon', variable=granular_activated_carbon).grid(column=1, row=11, sticky=W)
            granular_activated_carbon_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            granular_activated_carbon_installed.grid(column=2, row=11)

            reverse_osmosis = BooleanVar(root)
            reverse_osmosis_button = Checkbutton(tab3, text='Reverse Osmosis', variable=reverse_osmosis).grid(column=1, row=12, sticky=W)
            reverse_osmosis_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            reverse_osmosis_installed.grid(column=2, row=12)

            Label(tab3, text='Corrosion Control:', font=('Arial', 10)).grid(column=0, row=13, sticky=E)
            corrosion_control = StringVar(root)
            corrosion_control_choices = ['Bimetallic Phosphate', 'Hexametaphosphate', 'Orthophosphate', 'Polyphosphate',
                                         'Silicate', 'Permagnate', 'Sodium Bisulfate', 'Sodium Sulfate',
                                         'Sulfur Dioxide', 'None']
            corrosion_control.set('None')
            corrosion_control_popup_menu = OptionMenu(tab3, corrosion_control, *corrosion_control_choices).grid(column=1, row=13, sticky=W)

        elif system_type.get() == 'Municipal Wastewater System':
            Label(tab3, text='Municipal Wastewater System', font=('Arial', 10, 'bold')).grid(column=0, row=0, columnspan=2)
            Label(tab3, text='Treatment Train', font=('Arial', 10, 'bold')).grid(column=0, row=1, columnspan=2)
            Label(tab3, text='Number of Processes Installed', font=('Arial', 10, 'bold')).grid(column=2, row=1)

            Label(tab3, text='Preliminary Treatment:', font=('Arial', 10)).grid(column=0, row=2, sticky=E)

            aerated_grit = BooleanVar(root)
            aerated_grit_button = Checkbutton(tab3, text='Aerated Grit', variable=aerated_grit).grid(column=1, row=2, sticky=W)
            aerated_grit_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            aerated_grit_installed.grid(column=2, row=2)

            grinding = BooleanVar(root)
            grinding_button = Checkbutton(tab3, text='Grinding', variable=grinding).grid(column=1, row=3, sticky=W)

            filtration = BooleanVar(root)
            filtration_button = Checkbutton(tab3, text='Filtration', variable=filtration).grid(column=1, row=4, sticky=W)
            filtration_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            filtration_installed.grid(column=2, row=4)

            grit_removal = BooleanVar(root)
            grit_removal_button = Checkbutton(tab3, text='Grit Removal', variable=grit_removal).grid(column=1, row=5, sticky=W)
            grit_removal_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            grit_removal_installed.grid(column=2, row=5)

            screening = BooleanVar(root)
            screening_button = Checkbutton(tab3, text='Screening', variable=screening).grid(column=1, row=6, sticky=W)
            screening_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            screening_installed.grid(column=2, row=6)

            Label(tab3, text='Primary Treatment:', font=('Arial', 10)).grid(column=0, row=7, sticky=E)

            sedimentation = BooleanVar(root)
            sedimentation_button = Checkbutton(tab3, text='Sedimentation', variable=sedimentation).grid(column=1, row=7, sticky=W)
            sedimentation_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            sedimentation_installed.grid(column=2, row=7)

            Label(tab3, text='Secondary Treatment:', font=('Arial', 10)).grid(column=0, row=8, sticky=E)
            secondary_treatment = StringVar(root)
            secondary_treatment_choices = ['Activated Sludge and Clarification', 'Lagoon', 'Stabilization Pond',
                                           'Trickling Filter','None']
            secondary_treatment.set('Activated Sludge and Clarification')
            secondary_treatment_popup_menu = OptionMenu(tab3, secondary_treatment, *secondary_treatment_choices).grid(column=1, row=8, sticky=W)

            Label(tab3, text='Tertiary Treatment:', font=('Arial', 10)).grid(column=0, row=9, sticky=E)

            nitrification_denitrification = BooleanVar(root)
            nitrification_denitrification_button = Checkbutton(tab3, text='Nitrification/Denitrification', variable=nitrification_denitrification).grid(column=1, row=9, sticky=W)
            nitrification_denitrification_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            nitrification_denitrification_installed.grid(column=2, row=9)

            phosphorous_removal = BooleanVar(root)
            phosphorous_removal_button = Checkbutton(tab3, text='Phosphorous Removal', variable=phosphorous_removal).grid(column=1, row=10, sticky=W)
            phosphorous_removal_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            phosphorous_removal_installed.grid(column=2, row=10)

            reverse_osmosis = BooleanVar(root)
            reverse_osmosis_button = Checkbutton(tab3, text='Reverse Osmosis', variable=reverse_osmosis).grid(column=1, row=11, sticky=W)
            reverse_osmosis_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            reverse_osmosis_installed.grid(column=2, row=11)

            Label(tab3, text='Disinfection:', font=('Arial', 10)).grid(column=0, row=12, sticky=E)
            disinfection = StringVar(root)
            disinfection_choices = ['Hypochlorite', 'Ultraviolet', 'Ozone', 'None']
            disinfection.set('Hypochlorite')
            disinfection_popup_menu = OptionMenu(tab3, disinfection, *disinfection_choices).grid(column=1, row=12, sticky=W)

            dechlorination = BooleanVar(root)
            dechlorination_button = Checkbutton(tab3, text='Dechlorination', variable=dechlorination).grid(column=1, row=13, sticky=W)

            Label(tab3, text='Digestion:', font=('Arial', 10)).grid(column=0, row=14, sticky=E)
            digestion = StringVar(root)
            digestion_choices = ['Aerobic Digestion', 'Anaerobic Digestion w/o Biogas Use',
                                 'Anaerobic Digestion w/ Biogas Use', 'None']
            digestion.set('Aerobic Digestion')
            digestion_popup_menu = OptionMenu(tab3, digestion, *digestion_choices).grid(column=1, row=14, sticky=W)

            Label(tab3, text='Solids Dewatering:', font=('Arial', 10)).grid(column=0, row=15, sticky=E)
            dewatering = StringVar(root)
            dewatering_choices = ['Gravity Thickening', 'Mechanical Dewatering', 'Polymer Dewatering', 'None']
            dewatering.set('Mechanical Dewatering')
            dewatering_popup_menu = OptionMenu(tab3, dewatering, *dewatering_choices).grid(column=1, row=15, sticky=W)

            print(aerated_grit.get())

        elif system_type.get() == 'Industrial Wastewater System':
            Label(tab3, text='Industrial Wastewater System', font=('Arial', 10, 'bold')).grid(column=0, row=0, columnspan=5)
            Label(tab3, text='Treatment Train', font=('Arial', 10, 'bold')).grid(column=0, row=1, columnspan=2)
            Label(tab3, text='Number of Processes Installed', font=('Arial', 10, 'bold')).grid(column=2, row=1, columnspan=3)

            Label(tab3, text='Soda Ash Softening:', font=('Arial', 10)).grid(column=0, row=2, sticky=E)
            softening_process = BooleanVar(root)
            softening_process_button = Checkbutton(tab3, text='', variable=softening_process).grid(column=1, row=2, sticky=W)

            Label(tab3, text='Number of Chemical Addition Reactors:', font =('Arial', 10)).grid(column=0, row=3, sticky=E)
            chemcial_addition_input = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10).grid(column=1, row=3, sticky=W)

            Label(tab3, text='Biological Treatment Process:', font=('Arial', 10)).grid(column=0, row=4, sticky=E)
            bio_treatment = StringVar(root)
            bio_treatment_choices = ['None', 'Activated Sludge and Clarification', 'Lagoon', 'Stabilization Pond',
                                     'Trickling Filter']
            bio_treatment.set('None')
            bio_treatment_popup_menu = OptionMenu(tab3, bio_treatment, *bio_treatment_choices).grid(column=1, row=4, columnspan=3, sticky=W)
            bio_treatment_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            bio_treatment_installed.grid(column=2, row=4, columnspan=3)

            Label(tab3, text='Volume Reduction Process:', font=('Arial', 10)).grid(column=0, row=5, sticky=E)
            volume_reduction = StringVar(root)
            volume_reduction_choices = ['None', 'Mechanical Vapor Compression', 'Thermal Vapor Compression',
                                        'Reverse Osmosis', 'Forward Osmosis', 'Multiple Effect Distillation',
                                        'Multi-Stage Flash Distillation', 'Membrane Distillation']
            volume_reduction.set('None')
            volume_reduction_popup_menu = OptionMenu(tab3, volume_reduction, *volume_reduction_choices).grid(column=1, row=5, columnspan=3, sticky=W)
            volume_reduction_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            volume_reduction_installed.grid(column=2, row=5, columnspan=3)

            Label(tab3, text='Crystallization:', font=('Arial', 10)).grid(column=0, row=6, sticky=E)
            crystallization = BooleanVar(root)
            crystallization_button = Checkbutton(tab3, text='', variable=crystallization).grid(column=1, row=6, sticky=W)

            Label(tab3, text='Chemical Consumption', font=('Arial', 10, 'bold')).grid(column=0, row=7, columnspan=5)
            Label(tab3, text='Min', font=('Arial', 10)).grid(column=1, row=8)
            Label(tab3, text='Best', font=('Arial', 10)).grid(column=2, row=8)
            Label(tab3, text='Max', font=('Arial', 10)).grid(column=3, row=8)

            Label(tab3, text='CaOH:', font=('Arial', 10)).grid(column=0, row=9, sticky=E)
            caoh_dose_min_input = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            caoh_dose_min_input.grid(column=1, row=9, sticky=W)
            caoh_dose_best_input = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            caoh_dose_best_input.grid(column=2, row=9, sticky=W)
            caoh_dose_max_input = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            caoh_dose_max_input.grid(column=3, row=9, sticky=W)
            Label(tab3, text='mg/L of wastewater', font=('Arial', 10)).grid(column=4, row=9, sticky=W)

            Label(tab3, text=f'FeCl\N{SUBSCRIPT THREE}:', font=('Arial', 10)).grid(column=0, row=10, sticky=E)
            fecl3_dose_min_input = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            fecl3_dose_min_input.grid(column=1, row=10, sticky=W)
            fecl3_dose_best_input = Entry(tab3, validate='all', validatecommand=(vcmd, 'P%'), width=10)
            fecl3_dose_best_input.grid(column=2, row=10, sticky=W)
            fecl3_dose_max_input = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            fecl3_dose_max_input.grid(column=3, row=10, sticky=W)
            Label(tab3, text='mg/L of wastewater', font=('Arial', 10)).grid(column=4, row=10, sticky=W)

            Label(tab3, text='HCl:', font=('Arial', 10)).grid(column=0, row=11, sticky=E)
            hcl_dose_min_input = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            hcl_dose_min_input.grid(column=1, row=11, sticky=W)
            hcl_dose_best_input = Entry(tab3, validate='all', validatecommand=(vcmd, 'P%'), width=10)
            hcl_dose_best_input.grid(column=2, row=11, sticky=W)
            hcl_dose_max_input = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            hcl_dose_max_input.grid(column=3, row=11, sticky=W)
            Label(tab3, text='mg/L of wastewater', font=('Arial', 10)).grid(column=4, row=11, sticky=W)

            Label(tab3, text='Nutrients:', font=('Arial', 10)).grid(column=0, row=12, sticky=E)
            nutrients_dose_min_input = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            nutrients_dose_min_input.grid(column=1, row=12, sticky=W)
            nutrients_dose_best_input = Entry(tab3, validate='all', validatecommand=(vcmd, 'P%'), width=10)
            nutrients_dose_best_input.grid(column=2, row=12, sticky=W)
            nutrients_dose_max_input = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            nutrients_dose_max_input.grid(column=3, row=12, sticky=W)
            Label(tab3, text='mg/L of wastewater', font=('Arial', 10)).grid(column=4, row=12, sticky=W)
            
            Label(tab3, text=f'Na\N{SUBSCRIPT TWO}CO\N{SUBSCRIPT THREE}:', font=('Arial', 10)).grid(column=0, row=13, sticky=E)
            sodium_carbonate_dose_min_input = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            sodium_carbonate_dose_min_input.grid(column=1, row=13, sticky=W)
            sodium_carbonate_dose_best_input = Entry(tab3, validate='all', validatecommand=(vcmd, 'P%'), width=10)
            sodium_carbonate_dose_best_input.grid(column=2, row=13, sticky=W)
            sodium_carbonate_max_input = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            sodium_carbonate_max_input.grid(column=3, row=13, sticky=W)
            Label(tab3, text='mg/L of wastewater', font=('Arial', 10)).grid(column=4, row=13, sticky=W)

            Label(tab3, text='Granular Activated Carbon:', font=('Arial', 10)).grid(column=0, row=14, sticky=E)
            gac_dose_min_input = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            gac_dose_min_input.grid(column=1, row=14, sticky=W)
            gac_dose_best_input = Entry(tab3, validate='all', validatecommand=(vcmd, 'P%'), width=10)
            gac_dose_best_input.grid(column=2, row=14, sticky=W)
            gac_dose_max_input = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            gac_dose_max_input.grid(column=3, row=14, sticky=W)
            Label(tab3, text='mg/L of wastewater', font=('Arial', 10)).grid(column=4, row=14, sticky=W)

            Label(tab3, text='Other Inorganic Chemicals:', font=('Arial', 10)).grid(column=0, row=15, sticky=E)
            inorganics_dose_min_input = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            inorganics_dose_min_input.grid(column=1, row=15, sticky=W)
            inorganics_dose_best_input = Entry(tab3, validate='all', validatecommand=(vcmd, 'P%'), width=10)
            inorganics_dose_best_input.grid(column=2, row=15, sticky=W)
            inorganics_dose_max_input = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            inorganics_dose_max_input.grid(column=3, row=15, sticky=W)
            Label(tab3, text='mg/L of wastewater', font=('Arial', 10)).grid(column=4, row=15, sticky=W)

            Label(tab3, text='Other Organic Chemicals:', font=('Arial', 10)).grid(column=0, row=16, sticky=E)
            organics_dose_min_input = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            organics_dose_min_input.grid(column=1, row=16, sticky=W)
            organics_dose_best_input = Entry(tab3, validate='all', validatecommand=(vcmd, 'P%'), width=10)
            organics_dose_best_input.grid(column=2, row=16, sticky=W)
            organics_dose_max_input = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
            organics_dose_max_input.grid(column=3, row=16, sticky=W)
            Label(tab3, text='mg/L of wastewater', font=('Arial', 10)).grid(column=4, row=16, sticky=W)

    system_type.trace('w', change_dropdown)
    system_type.trace('w', change_dropdown_change_window)

    system_size_input = Entry(tab1, validate='all', validatecommand=(vcmd, '%P'))
    system_size_input.grid(row=2, column=1)
    Label(tab1, text=f'm\N{SUPERSCRIPT THREE}/d', font=('Arial', 10)).grid(row=2, column=2, sticky=W)

    Label(tab1, text='Economic Parameters', font=('Arial', 10, 'bold')).grid(row=3, column=1)

    Label(tab1, text='Year for Inflation Adjustment:', font=('Arial', 10)).grid(row=4, column=0, sticky=E)
    year_for_inflation = StringVar(root)
    year_for_inflation_choices = range(2000, 2019)
    year_for_inflation.set(2015)
    year_for_inflation_popup_menu = OptionMenu(tab1, year_for_inflation, *year_for_inflation_choices).grid(row=4, column=1)

    Label(tab1, text='Value of a Statistical Life:', font=('Arial', 10)).grid(row=5, column=0, sticky=E)
    vsl = DoubleVar(root)
    vsl.set(8.6)
    scale = Scale(tab1, from_=0.1, to=20, resolution=0.1, font=('Arial', 10), orient='horizontal', variable=vsl).grid(row=5, column=1)
    Label(tab1, text='$M (in $2015USD)', font=('Arial', 10)).grid(row=5, column=2, sticky=W)

    Label(tab1, text='Social Cost of Carbon:', font=('Arial', 10)).grid(row=6, column=0, sticky=E)
    scc = IntVar(root)
    scc.set(40)
    scale = Scale(tab1, from_=0, to=250, font=('Arial', 10), orient='horizontal', variable=scc).grid(row=6, column=1)
    Label(tab1, text=f'$/short ton CO\N{SUBSCRIPT TWO} (in $2015 USD)', font=('Arial', 10)).grid(row=6, column=2, sticky=W)

    Label(tab1, text='Simulation Parameters', font=('Arial', 10, 'bold')).grid(row=7, column=1)
    Label(tab1, text='Number of Simulations:', font=('Arial', 10)).grid(row=8, column=0, sticky=E)
    model_runs = Entry(tab1, validate='all', validatecommand=(vcmd, '%P'))
    model_runs.grid(row=8, column=1)

    Label(tab2,
          text='Electricity Generation and Chemical Manufacturing Geography',
          font=("Arial", 10, 'bold')).grid(row=0, column=0, columnspan=2)

    Label(tab2, text='Grid State:', font=('Arial', 10)).grid(row=1, column=0, sticky=E)
    grid_state = StringVar(root)
    grid_state_choices = ['US Average', 'AL', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'ID', 'IL', 'IN', 'IA',
                          'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                          'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT',
                          'VA', 'WA', 'WV', 'WI', 'WY']
    grid_state.set('US Average')
    grid_state_popup_menu = OptionMenu(tab2, grid_state, *grid_state_choices).grid(row=1, column=1, sticky=W)

    Label(tab2, text='Chemical Manufacturing State:', font=('Arial', 10)).grid(row=2, column=0, sticky=E)
    chem_state = StringVar(root)
    chem_state_choices = ['US Average', 'Off-Shore', 'AL', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'ID', 'IL',
                          'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV',
                          'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
                          'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    chem_state.set('US Average')
    chem_state_popup_menu = OptionMenu(tab2, chem_state, *chem_state_choices).grid(row=2, column=1, sticky=W)

    Label(tab4, text='Enter electricity consumption and chemical dosages for the new process.').grid(column=0, row=1, columnspan=4)

    Label(tab4, text='Electricity Consumption', font=('Arial', 10)).grid(column=0, row=2, columnspan=4)
    Label(tab4, text='Min', font=('Arial', 10)).grid(column=1, row=3)
    Label(tab4, text='Best', font=('Arial', 10)).grid(column=2, row=3)
    Label(tab4, text='Max', font=('Arial', 10)).grid(column=3, row=3)
    Label(tab4, text='Unit Electricity Consumption:', font=('Arial', 10)).grid(column=0, row=4, sticky=E)
    new_elec_min_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_elec_min_input.grid(column=1, row=4, sticky=W)
    new_elec_best_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_elec_best_input.grid(column=2, row=4, sticky=W)
    new_elec_max_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_elec_max_input.grid(column=3, row=4, sticky=W)
    Label(tab4, text='kWh/m\N{SUPERSCRIPT THREE} of water', font=('Arial', 10)).grid(column=4, row=4, sticky=W)

    Label(tab4, text='Chemical Consumption', font=('Arial', 10)).grid(column=0, row=5, columnspan=4)
    Label(tab4, text='Min', font=('Arial', 10)).grid(column=1, row=6)
    Label(tab4, text='Best', font=('Arial', 10)).grid(column=2, row=6)
    Label(tab4, text='Max', font=('Arial', 10)).grid(column=3, row=6)

    Label(tab4, text='CaOH:', font=('Arial', 10)).grid(column=0, row=7, sticky=E)
    new_caoh_dose_min_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_caoh_dose_min_input.grid(column=1, row=7, sticky=W)
    new_caoh_dose_best_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_caoh_dose_best_input.grid(column=2, row=7, sticky=W)
    new_caoh_dose_max_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_caoh_dose_max_input.grid(column=3, row=7, sticky=W)
    Label(tab4, text='mg/L of water', font=('Arial', 10)).grid(column=4, row=7, sticky=W)

    Label(tab4, text=f'FeCl\N{SUBSCRIPT THREE}:', font=('Arial', 10)).grid(column=0, row=8, sticky=E)
    new_fecl3_dose_min_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_fecl3_dose_min_input.grid(column=1, row=8, sticky=W)
    new_fecl3_dose_best_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_fecl3_dose_best_input.grid(column=2, row=8, sticky=W)
    new_fecl3_dose_max_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_fecl3_dose_max_input.grid(column=3, row=8, sticky=W)
    Label(tab4, text='mg/L of water', font=('Arial', 10)).grid(column=4, row=8, sticky=W)

    Label(tab4, text='HCl:', font=('Arial', 10)).grid(column=0, row=9, sticky=E)
    new_hcl_dose_min_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_hcl_dose_min_input.grid(column=1, row=9, sticky=W)
    new_hcl_dose_best_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_hcl_dose_best_input.grid(column=2, row=9, sticky=W)
    new_hcl_dose_max_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_hcl_dose_max_input.grid(column=3, row=9, sticky=W)
    Label(tab4, text='mg/L of water', font=('Arial', 10)).grid(column=4, row=9, sticky=W)

    Label(tab4, text='Nutrients:', font=('Arial', 10)).grid(column=0, row=10, sticky=E)
    new_nutrients_dose_min_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_nutrients_dose_min_input.grid(column=1, row=10, sticky=W)
    new_nutrients_dose_best_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_nutrients_dose_best_input.grid(column=2, row=10, sticky=W)
    new_nutrients_dose_max_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_nutrients_dose_max_input.grid(column=3, row=10, sticky=W)
    Label(tab4, text='mg/L of water', font=('Arial', 10)).grid(column=4, row=10, sticky=W)

    Label(tab4, text=f'Na\N{SUBSCRIPT TWO}CO\N{SUBSCRIPT THREE}:', font=('Arial', 10)).grid(column=0, row=11, sticky=E)
    new_sodium_carbonate_dose_min_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_sodium_carbonate_dose_min_input.grid(column=1, row=11, sticky=W)
    new_sodium_carbonate_dose_best_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_sodium_carbonate_dose_best_input.grid(column=2, row=11, sticky=W)
    new_sodium_carbonate_dose_max_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_sodium_carbonate_dose_max_input.grid(column=3, row=11, sticky=W)
    Label(tab4, text='mg/L of water', font=('Arial', 10)).grid(column=4, row=11, sticky=W)

    Label(tab4, text='Granular Activated Carbon:', font=('Arial', 10)).grid(column=0, row=12, sticky=E)
    new_gac_dose_min_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_gac_dose_min_input.grid(column=1, row=12, sticky=W)
    new_gac_dose_best_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_gac_dose_best_input.grid(column=2, row=12, sticky=W)
    new_gac_dose_max_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_gac_dose_max_input.grid(column=3, row=12, sticky=W)
    Label(tab4, text='mg/L of water', font=('Arial', 10)).grid(column=4, row=12, sticky=W)

    Label(tab4, text='Other Inorganic Chemicals:', font=('Arial', 10)).grid(column=0, row=13, sticky=E)
    new_inorganics_dose_min_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_inorganics_dose_min_input.grid(column=1, row=13, sticky=W)
    new_inorganics_dose_best_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_inorganics_dose_best_input.grid(column=2, row=13, sticky=W)
    new_inorganics_dose_max_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_inorganics_dose_max_input.grid(column=3, row=13, sticky=W)
    Label(tab4, text='mg/L of water', font=('Arial', 10)).grid(column=4, row=13, sticky=W)

    Label(tab4, text='Other Organic Chemicals:', font=('Arial', 10)).grid(column=0, row=14, sticky=E)
    new_organics_dose_min_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_organics_dose_min_input.grid(column=1, row=14, sticky=W)
    new_organics_dose_best_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_organics_dose_best_input.grid(column=2, row=14, sticky=W)
    new_organics_dose_max_input = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_organics_dose_max_input.grid(column=3, row=14, sticky=W)
    Label(tab4, text='mg/L of water', font=('Arial', 10)).grid(column=4, row=14, sticky=W)

    Label(tab5, text='Results', font=('Arial', 10, 'bold')).grid(column=0, row=0, columnspan=8)
    Label(tab5, text='Embedded Air Emissions [g/m\N{SUPERSCRIPT THREE}]', font=('Arial', 10)).grid(column=3, row=1, columnspan=4)
    Label(tab5, text='Annual Air Damages [$/yr]', font=('Arial', 10)).grid(column=7, row=1, columnspan=3)
    Label(tab5, text='Required Dose', font=('Arial', 10)).grid(column=1, row=2, columnspan=2)
    Label(tab5, text='NOx', font=('Arial', 10)).grid(column=3, row=2)
    Label(tab5, text='SO\N{SUBSCRIPT TWO}', font=('Arial', 10)).grid(column=4, row=2)
    Label(tab5, text='PM2.5', font=('Arial', 10)).grid(column=5, row=2)
    Label(tab5, text='CO\N{SUBSCRIPT TWO}', font=('Arial', 10)).grid(column=6, row=2)
    Label(tab5, text='Health', font=('Arial', 10)).grid(column=7, row=2)
    Label(tab5, text='Climate', font=('Arial', 10)).grid(column=8, row=2)
    Label(tab5, text='Total', font=('Arial', 10, 'italic')).grid(column=9, row=2)
    Label(tab5, text='Electricity', font=('Arial', 10, 'italic')).grid(column=0, row=3)
    Label(tab5, text='(25th-75th)', font=('Arial', 10, 'italic')).grid(column=0, row=4)
    Label(tab5, text='Chemicals', font=('Arial', 10, 'italic')).grid(column=0, row=5)
    Label(tab5, text='(25th-75th)', font=('Arial', 10, 'italic')).grid(column=0, row=6)
    Label(tab5, text='CaOH', font=('Arial', 10)).grid(column=0, row=7)
    Label(tab5, text='(25th-75th)', font=('Arial', 10)).grid(column=0, row=8)
    Label(tab5, text='FeCl\N{SUBSCRIPT THREE}', font=('Arial', 10)).grid(column=0, row=9)
    Label(tab5, text='(25th-75th)', font=('Arial', 10)).grid(column=0, row=10)
    Label(tab5, text='HCl', font=('Arial', 10)).grid(column=0, row=11)
    Label(tab5, text='(25th-75th)', font=('Arial', 10)).grid(column=0, row=12)
    Label(tab5, text='Na\N{SUBSCRIPT TWO}CO\N{SUBSCRIPT THREE}', font=('Arial', 10)).grid(column=0, row=13)
    Label(tab5, text='(25th-75th)', font=('Arial', 10)).grid(column=0, row=14)
    Label(tab5, text='Activated Carbon', font=('Arial', 10)).grid(column=0, row=15)
    Label(tab5, text='(25th-75th)', font=('Arial', 10)).grid(column=0, row=16)
    Label(tab5, text='Assorted Inorganics', font=('Arial', 10)).grid(column=0, row=17)
    Label(tab5, text='(25th-75th)', font=('Arial', 10)).grid(column=0, row=18)
    Label(tab5, text='Associated Organics', font=('Arial', 10)).grid(column=0, row=19)
    Label(tab5, text='(25th-75th)', font=('Arial', 10)).grid(column=0, row=20)
    # Label(tab5, text=np.median())
    Label(tab5, text='kWh/m\N{SUPERSCRIPT THREE}', font=('Arial', 10)).grid(column=2, row=3, rowspan=2)
    Label(tab5, text='mg/L', font=('Arial', 10)).grid(column=2, row=7, rowspan=2)
    Label(tab5, text='mg/L', font=('Arial', 10)).grid(column=2, row=9, rowspan=2)
    Label(tab5, text='mg/L', font=('Arial', 10)).grid(column=2, row=11, rowspan=2)
    Label(tab5, text='mg/L', font=('Arial', 10)).grid(column=2, row=13, rowspan=2)
    Label(tab5, text='mg/L', font=('Arial', 10)).grid(column=2, row=15, rowspan=2)
    Label(tab5, text='mg/L', font=('Arial', 10)).grid(column=2, row=17, rowspan=2)
    Label(tab5, text='mg/L', font=('Arial', 10)).grid(column=2, row=19, rowspan=2)

    def round_sig(x, sig=2):
        try:
            return round(x, sig - int(np.floor(np.log10(abs(x)))) - 1)

        except ValueError:
            return 0

    def gather_inputs():
        '''This function collects the model inputs and stores them into a dictionary.'''
        basic_info={'system type': system_type.get(), 'system size': system_size_input.get(),
                      'inflation year': year_for_inflation.get(), 'vsl': vsl.get(), 'scc': scc.get(),
                     'mc runs': model_runs.get()}

        geography_info = {'electricity state': grid_state.get(), 'chemicals state': chem_state.get()}

        if system_type.get() == 'Drinking Water System':
             baseline_treatment_process_info = {'flocculation': flocculation.get(),
                                           'no. of flocculation units': flocculation_installed.get(),
                                           'coagulation': coagulation.get(),
                                           'no. of coagulation units': coagulation_installed.get(),
                                           'sedimentation': sedimentation.get(),
                                           'no. of sedimentation units': sedimentation_installed.get(),
                                           'filtration': filtration.get(),
                                           'primary disinfection': primary_disinfection.get(),
                                           'secondary disinfection': secondary_disinfection.get(),
                                           'fluoridation': fluoridation.get(),
                                           'softening': softening.get(),
                                           'pH adjustment': ph_adjustment.get(),
                                           'no. of pH adjustment units': ph_adjustment_installed.get(),
                                           'gac': granular_activated_carbon.get(),
                                           'no. of gac units': granular_activated_carbon_installed.get(),
                                           'ro': reverse_osmosis.get(),
                                           'no. or ro units': reverse_osmosis_installed.get(),
                                           'corrosion control': corrosion_control.get(),
                                           'aerated grit': FALSE,
                                           'no. of aerated grit units': 0,
                                           'grinding': FALSE,
                                           'grit removal': FALSE,
                                           'no. of grit removal units': 0,
                                           'screening': FALSE,
                                           'no. of screening units': 0,
                                           'secondary treatment': FALSE,
                                           'nitrification denitrification': FALSE,
                                           'no. of nitrification denitrification units': 0,
                                           'phosphorous removal': FALSE,
                                           'no. of phosphorous removal units': 0,
                                           'disinfection': FALSE,
                                           'dechlorination': FALSE,
                                           'digestion': FALSE,
                                           'dewatering': FALSE,
                                           'softening process': FALSE,
                                           'chemical addition input': FALSE,
                                           'bio treatment': FALSE,
                                           'no. of bio treatment units': 0,
                                           'volume reduction': FALSE,
                                           'no. of volume reduction units': 0,
                                           'crystallization': FALSE,
                                           'caoh dose min input': 0,
                                           'caoh dose best input': 0,
                                           'caoh dose max input': 0,
                                           'fecl3 dose min input': 0,
                                           'fecl3 dose best input': 0,
                                           'fecl3 dose max input': 0,
                                           'hcl dose min input': 0,
                                           'hcl dose best input': 0,
                                           'hcl dose max input': 0,
                                           'nutrients dose min input': 0,
                                           'nutrients dose best input': 0,
                                           'nutrients dose max input': 0,
                                           'sodium carbonate dose min input': 0,
                                           'sodium carbonate dose best input': 0,
                                           'sodium carbonate dose max input': 0,
                                           'gac dose min input': 0,
                                           'gac dose best input': 0,
                                           'gac dose max input': 0,
                                           'organics dose min input': 0,
                                           'organics dose best input': 0,
                                           'organics dose max input': 0,
                                           'inorganics dose min input': 0,
                                           'inorganics_dose_best_input': 0,
                                           'inorganics_dose_max_input': 0}
        elif system_type.get() == 'Municipal Wastewater System':
             baseline_treatment_process_info = {'flocculation': FALSE,
                                           'no. of flocculation units': 0,
                                           'coagulation': FALSE,
                                           'no. of coagulation units': 0,
                                           'sedimentation': FALSE,
                                           'no. of sedimentation units': 0,
                                           'filtration': FALSE,
                                           'primary disinfection': FALSE,
                                           'secondary disinfection': FALSE,
                                           'fluoridation': FALSE,
                                           'softening': FALSE,
                                           'pH adjustment': FALSE,
                                           'no. of pH adjustment units': FALSE,
                                           'gac': FALSE,
                                           'no. of gac units': 0,
                                           'ro': FALSE,
                                           'no. or ro units': 0,
                                           'corrosion control': FALSE,
                                           'aerated grit': aerated_grit.get(),
                                           'no. of aerated grit units': aerated_grit_installed.get(),
                                           'grinding': grinding.get(),
                                           'grit removal': grit_removal.get(),
                                           'no. of grit removal units': grit_removal_installed.get(),
                                           'screening': screening.get(),
                                           'no. of screening units': screening_installed.get(),
                                           'secondary treatment': secondary_treatment.get(),
                                           'nitrification denitrification': nitrification_denitrification.get(),
                                           'no. of nitrification denitrification units': nitrification_denitrification_installed.get(),
                                           'phosphorous removal': phosphorous_removal.get(),
                                           'no. of phosphorous removal units': phosphorous_removal_installed.get(),
                                           'disinfection': disinfection.get(),
                                           'dechlorination': dechlorination.get(),
                                           'digestion': digestion.get(),
                                           'dewatering': dewatering.get(),
                                           'softening process': FALSE,
                                           'chemical addition input': FALSE,
                                           'bio treatment': FALSE,
                                           'no. of bio treatment units': 0,
                                           'volume reduction': FALSE,
                                           'no. of volume reduction units': 0,
                                           'crystallization': FALSE,
                                           'caoh dose min input': 0,
                                           'caoh dose best input': 0,
                                           'caoh dose max input': 0,
                                           'fecl3 dose min input': 0,
                                           'fecl3 dose best input': 0,
                                           'fecl3 dose max input': 0,
                                           'hcl dose min input': 0,
                                           'hcl dose best input': 0,
                                           'hcl dose max input': 0,
                                           'nutrients dose min input': 0,
                                           'nutrients dose best input': 0,
                                           'nutrients dose max input': 0,
                                           'sodium carbonate dose min input': 0,
                                           'sodium carbonate dose best input': 0,
                                           'sodium carbonate dose max input': 0,
                                           'gac dose min input': 0,
                                           'gac dose best input': 0,
                                           'gac dose max input': 0,
                                           'organics dose min input': 0,
                                           'organics dose best input': 0,
                                           'organics dose max input': 0,
                                           'inorganics dose min input': 0,
                                           'inorganics_dose_best_input': 0,
                                           'inorganics_dose_max_input': 0}
        elif system_type.get() == 'Industrial Wastewater System':
             baseline_treatment_process_info = {'flocculation': FALSE,
                                           'no. of flocculation units': 0,
                                           'coagulation': FALSE,
                                           'no. of coagulation units': 0,
                                           'sedimentation': FALSE,
                                           'no. of sedimentation units': 0,
                                           'filtration': FALSE,
                                           'primary disinfection': FALSE,
                                           'secondary disinfection': FALSE,
                                           'fluoridation': FALSE,
                                           'softening': FALSE,
                                           'pH adjustment': FALSE,
                                           'no. of pH adjustment units': 0,
                                           'gac': FALSE,
                                           'no. of gac units': 0,
                                           'ro': FALSE,
                                           'no. or ro units': 0,
                                           'corrosion control': FALSE,
                                           'aerated grit': FALSE,
                                           'no. of aerated grit units': 0,
                                           'grinding': FALSE,
                                           'grit removal': FALSE,
                                           'no. of grit removal units': 0,
                                           'screening': FALSE,
                                           'no. of screening units': 0,
                                           'secondary treatment': FALSE,
                                           'nitrification denitrification': FALSE,
                                           'no. of nitrification denitrification units': 0,
                                           'phosphorous removal': FALSE,
                                           'no. of phosphorous removal units': 0,
                                           'disinfection': FALSE,
                                           'dechlorination': FALSE,
                                           'digestion': FALSE,
                                           'dewatering': FALSE,
                                           'softening process': softening_process.get(),
                                           'chemical addition input': chemical_addition_input.get(),
                                           'bio treatment': bio_treatment.get(),
                                           'no. of bio treatment units': bio_treatment_installed.get(),
                                           'volume reduction': volume_reduction.get(),
                                           'no. of volume reduction units': volume_reduction_installed.get(),
                                           'crystallization': crystallization.get(),
                                           'caoh dose min input': caoh_dose_min_input.get(),
                                           'caoh dose best input': caoh_dose_best_input.get(),
                                           'caoh dose max input': caoh_dose_max_input.get(),
                                           'fecl3 dose min input': fecl3_dose_min_input.get(),
                                           'fecl3 dose best input': fecl3_dose_best_input.get(),
                                           'fecl3 dose max input': fecl3_dose_max_input.get(),
                                           'hcl dose min input': hcl_dose_min_input.get(),
                                           'hcl dose best input': hcl_dose_best_input.get(),
                                           'hcl dose max input': hcl_dose_max_input.get(),
                                           'nutrients dose min input': nutrients_dose_min_input.get(),
                                           'nutrients dose best input': nutrients_dose_best_input.get(),
                                           'nutrients dose max input': nutrients_dose_max_input.get(),
                                           'sodium carbonate dose min input': sodium_carbonate_dose_min_input.get(),
                                           'sodium carbonate dose best input': sodium_carbonate_dose_best_input.get(),
                                           'sodium carbonate dose max input': sodium_carbonate_dose_max_input.get(),
                                           'gac dose min input': gac_dose_min_input.get(),
                                           'gac dose best input': gac_dose_best_input.get(),
                                           'gac dose max input': gac_dose_max_input.get(),
                                           'organics dose min input': organics_dose_min_input.get(),
                                           'organics dose best input': organics_dose_best_input.get(),
                                           'organics dose max input': organics_dose_max_input.get(),
                                           'inorganics dose min input': inorganics_dose_min_input.get(),
                                           'inorganics_dose_best_input': inorganics_dose_best_input.get(),
                                           'inorganics_dose_max_input': inorganics_dose_max_input.get()}

        new_process_info = {'new electricity min input': new_elec_min_input.get(),
                             'new electricity best input': new_elec_best_input.get(),
                             'new electricity max input': new_elec_max_input.get(),
                             'new caoh dose min input': new_caoh_dose_min_input.get(),
                             'new caoh dose best input': new_caoh_dose_best_input.get(),
                             'new caoh dose max input': new_caoh_dose_max_input.get(),
                             'new fecl3 dose min input': new_fecl3_dose_min_input.get(),
                             'new fecl3 dose best input': new_fecl3_dose_best_input.get(),
                             'new fecl3 dose max input': new_fecl3_dose_max_input.get(),
                             'new hcl dose min input': new_hcl_dose_min_input.get(),
                             'new hcl dose best input': new_hcl_dose_best_input.get(),
                             'new hcl dose max input': new_hcl_dose_max_input.get(),
                             'new nutrients dose min input': new_nutrients_dose_min_input.get(),
                             'new nutrients dose best input': new_nutrients_dose_best_input.get(),
                             'new nutrients dose max input': new_nutrients_dose_max_input.get(),
                             'new sodium carbonate dose min input': new_sodium_carbonate_dose_min_input.get(),
                             'new sodium carbonate dose best input': new_sodium_carbonate_dose_best_input.get(),
                             'new sodium carbonate dose max input': new_sodium_carbonate_dose_max_input.get(),
                             'new gac dose min input': new_gac_dose_min_input.get(),
                             'new gac dose best input': new_gac_dose_best_input.get(),
                             'new gac dose max input': new_gac_dose_max_input.get(),
                             'new organics dose min input': new_organics_dose_min_input.get(),
                             'new organics dose best input': new_organics_dose_best_input.get(),
                             'new organics dose max input': new_organics_dose_max_input.get(),
                             'new inorganics dose min input': new_inorganics_dose_min_input.get(),
                             'new inorganics dose best input': new_inorganics_dose_best_input.get(),
                             'new inorganics dosemax input': new_inorganics_dose_max_input.get()}

        return basic_info, geography_info, baseline_treatment_process_info, new_process_info


    def calculate_results():
        global system_size_input, year_for_inflation, vsl, scc, model_runs,\
            grid_state, chem_state, \
            flocculation, flocculation_installed, coagulation, coagulation_installed, sedimentation, \
            sedimentation_installed, filtration, primary_disinfection, secondary_disinfection, fluoridation, softening, \
            ph_adjustment, ph_adjustment_installed, granular_activated_carbon, granular_activated_carbon_installed, \
            reverse_osmosis, reverse_osmosis_installed, corrosion_control, aerated_grit, aerated_grit_installed, \
            grinding, grit_removal, grit_removal_installed, screening, screening_installed, secondary_treatment, \
            nitrification_denitrification, nitrification_denitrification_installed, phosphorous_removal, \
            phosphorous_removal_installed, disinfection, dechlorination, \
            digestion, dewatering, softening_process, chemical_addition_input, bio_treatment, bio_treatment_installed, \
            volume_reduction, volume_reduction_installed, crystallization, caoh_dose_min_input, caoh_dose_best_input, \
            caoh_dose_max_input, fecl3_dose_min_input, fecl3_dose_best_input, fecl3_dose_max_input, hcl_dose_min_input, \
            hcl_dose_best_input, hcl_dose_max_input, nutrients_dose_min_input, nutrients_dose_best_input, \
            nutrients_dose_max_input, sodium_carbonate_dose_min_input, sodium_carbonate_dose_best_input, \
            sodium_carbonate_dose_max_input, gac_dose_min_input, gac_dose_best_input, gac_dose_max_input, \
            organics_dose_min_input, organics_dose_best_input, organics_dose_max_input, inorganics_dose_min_input, \
            inorganics_dose_best_input, inorganics_dose_max_input, new_elec_min_input, new_elec_best_input, \
            new_elec_max_input, new_caoh_dose_min_input, new_caoh_dose_best_input, new_caoh_dose_max_input, \
            new_fecl3_dose_min_input, new_fecl3_dose_best_input, new_fecl3_dose_max_input, new_hcl_dose_min_input, \
            new_hcl_dose_best_input, new_hcl_dose_max_input, new_nutrients_dose_min_input, new_nutrients_dose_best_input, \
            new_nutrients_dose_max_input, new_sodium_carbonate_dose_min_input, new_sodium_carbonate_dose_best_input, \
            new_sodium_carbonate_dose_max_input, new_gac_dose_min_input, new_gac_dose_best_input, new_gac_dose_max_input, \
            new_organics_dose_min_input, new_organics_dose_best_input, new_organics_dose_max_input, \
            new_inorganics_dose_min_input, new_inorganics_dose_best_input, new_inorganics_dose_max_input

        basic_info, geography_info, baseline_treatment_process_info, new_process_info = gather_inputs()

        print(basic_info)
        print(geography_info)
        print(baseline_treatment_process_info)
        print(new_process_info)
        print("Calculating")

    # Create the menu.
    menu = Menu(root)
    root.config(menu=menu)

    filemenu = Menu(menu)
    savemenu = Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="New", command=menu_option_selected)
    filemenu.add_cascade(label="Save Options", menu=savemenu, command=menu_option_selected)
    savemenu.add_cascade(label="Save All", command=menu_option_selected)
    savemenu.add_cascade(label="Save Inputs", command=menu_option_selected)
    savemenu.add_cascade(label="Save Results", command=menu_option_selected)
    filemenu.add_command(label="Open", command=menu_option_selected)
    # TODO Create save functions (save_all, save_inputs, save_results)
    # savemenu.add_cascade(label="Save All", command=save_all)
    # savemenu.add_cascade(label="Save Inputs", command=save_inputs)
    # savemenu.add_cascade(label="Save Results", command=save_results)
    # TODO Create open_input function
    # filemenu.add_command(label="Open", command=combine_funcs(menu_option_selected, open_input))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)

    # TODO Create check_input function
    # TODO Create calcualte_input fucntion
    analysismenu = Menu(menu)
    menu.add_cascade(label="Analysis", menu=analysismenu)
    analysismenu.add_command(label='Calculate', command=calculate_results)

    # TODO Create a help menu.
    # TODO Create an About tab.
    # TODO Create a License tab.
    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="About", command=menu_option_selected)
    helpmenu.add_command(label="License", command=menu_option_selected)

    root.mainloop()

if __name__ == "__main__":
    main()

# class App:
#
#     def __init__(self, master):
#
#         frame = Frame(master)
#         frame.pack()
#
#         self.button = Button(
#             frame, text="QUIT", fg="red", command=frame.quit
#             )
#         self.button.pack(side=LEFT)
#
#         self.hi_there = Button(frame, text="Hello", command=self.say_hi)
#         self.hi_there.pack(side=LEFT)
#
#     def say_hi(self):
#         print("Hi there, everyone!")

# class MyDialog:
#
#     def __init__(self, parent):
#
#         top = self.top = Toplevel(parent)
#
#         Label(top, text='Value').pack()
#
#         self.e = Entry(top)
#         self.e.pack(padx=5)
#
#         b = Button(top, text='OK', command=self.ok)
#         b.pack(pady=5)
#
#     def ok(self):
#
#         print("Value is", self.e.get())
#
#         self.top.destroy()
#
#
# class Dialog(Toplevel):
#
#     def __init__(self, parent, title=None):
#
#         Toplevel.__init__(self, parent)
#         self.transient(parent)
#
#         if title:
#             self.title(title)
#
#         self.parent = parent
#
#         self.result = None
#         body = Frame(self)
#         self.initial_focus = self.body(body)
#         body.pack(padx=5, pady=5)
#
#         self.buttonbox()
#
#         self.grab_set()
#
#         if not self.initial_focus:
#             self.initial_focus = self
#
#         self.protocol('WM_DELETE_WINDOW', self.cancel)
#
#         self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
#                                   parent.winfo_rooty() + 50))
#
#         self.initial_focus.focus_set()
#
#         self.wait_window(self)
#
#     # construction hooks
#
#     def body(self,master):
#         # Create dialog body.  Return widget that should have initial focus.  This method should be overriden.
#         pass
#
#     def buttonbox(self):
#         # Add standard button box.  Override if you don't want the standard buttons.
#
#         box = Frame(self)
#
#         w = Button(box, text='OK', width=10, command=self.ok, default=ACTIVE)
#         w.pack(side=LEFT, padx=5, pady=5)
#         w = Button(box, text='Cancel', width=10, command=self.cancel)
#         w.pack(side=LEFT, padx=5, pady=5)
#
#         self.bind('<Return>', self.ok)
#         self.bind('<Escape>', self.cancel)
#
#         box.pack()
#
#     # standard button semantics
#
#     def ok(self, event=None):
#
#         if not self.validate():
#             self.initial_focus.focus_set()
#             return
#
#         self.withdraw()
#         self.update_idletasks()
#
#         self.apply()
#
#         self.cancel()
#
#     def cancel(self, event=None):
#
#         # Put focus back to the parent window.
#         self.parent.focus_set()
#         self.destroy()
#
#     # command hooks
#
#     def validate(self):
#
#         return 1 #override
#
#     def apply(self):
#
#         pass #override
#
#
# class MyDialog(tkinter.simpledialog.Dialog):
#
#     def body(self, master):
#
#         Label(master, text='Number 1:').grid(row=0, sticky=W)
#         Label(master, text='Number 2:').grid(row=1, sticky=W)
#
#         self.e1 = Entry(master)
#         self.e2 = Entry(master)
#
#         self.e1.grid(row=0, column=1)
#         self.e2.grid(row=1, column=1)
#
#         self.cb = Checkbutton(master, text='Hardcopy')
#         self.cb.grid(row=2, columnspan=2, sticky=W)
#
#         return self.e1  # initial focus
#
#     def validate(self):
#         try:
#             first = int(self.e1.get())
#             second = int(self.e2.get())
#             result = first + second
#             self.result_string = f'The sum of your numbers is {result}.'
#             return 1
#         except ValueError:
#             tkinter.messagebox.showwarning(
#                 'Bad input',
#                 'Illegal values, please try again'
#             )
#             return 0
#
#     def apply(self):
#         tkinter.messagebox.showinfo(
#             'Result',
#             self.result_string
#         )
#
#         return
#
# root = Tk()
#
# d = MyDialog(root)
# #print(d.result_string)
#
# # root.wait_window(d.top)
#
# # Create a toolbar.
# toolbar = Frame(root)
#
# b = Button(toolbar, text="New", width=6, command=callback)
# b.pack(side=LEFT, padx=2, pady=2)
#
# b = Button(toolbar, text="Open", width=6, command=callback)
# b.pack(side=LEFT, padx=2, pady=2)
#
# toolbar.pack(side=TOP, fill=X)

# Define a Status Bar class.
#
#
# class StatusBar(Frame):
#
#     def __init__(self, master):
#         Frame.__init__(self, master)
#         self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
#         self.label.pack(fill=X)
#
#     def set(self, format, *args):
#         self.label.config(text=format % args)
#         self.label.update_idletasks()
#
#     def clear(self):
#         self.label.config(text="")
#         self.label.update_idletasks()
#
# status = StatusBar(root)
# status.pack(side=BOTTOM, fill=X)
#
# app = App(root)
#
#
#
# root.mainloop()
