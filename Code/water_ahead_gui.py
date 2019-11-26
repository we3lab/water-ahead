from tkinter import *
import numpy as np
import pandas as pd
import pathlib

fileDir = pathlib.Path(__file__).parents[1]


# TODO Add embedded energy in chemicals
# TODO Add cost tab

from chem_manufacturing_distribution_dictionary import chem_manufacturing_share_dict
from empty_state_dictionary import empty_state_dict
from unit_elec_consumption import unit_elec_consumption_dictionary
from unit_therm_consumption import unit_therm_consumption_dictionary
from unit_chem_consumption import unit_sodium_carbonate_consumption_dictionary, unit_gac_consumption_dictionary, \
    unit_inorganics_consumption_dictionary, unit_organics_consumption_dictionary

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

    def calculate_electricity_consumption(basic_info_dict, baseline_process_dict, new_process_dict):
        source_water = baseline_process_dict['source water']
        flocculation = baseline_process_dict['flocculation']
        flocculation_installed = baseline_process_dict['no. of flocculation units']
        flocculation_recovery = baseline_process_dict['flocculation recovery']
        coagulation = baseline_process_dict['coagulation']
        coagulation_installed = baseline_process_dict['no. of coagulation units']
        coagulation_recovery = baseline_process_dict['coagulation recovery']
        sedimentation = baseline_process_dict['sedimentation']
        sedimentation_installed = baseline_process_dict['no. of sedimentation units']
        sedimentation_recovery = baseline_process_dict['sedimentation recovery']
        filtration = baseline_process_dict['filtration']
        filtration_recovery = baseline_process_dict['filtration recovery']
        primary_disinfection = baseline_process_dict['primary disinfection']
        primary_disinfection_recovery = baseline_process_dict['primary disinfection recovery']
        secondary_disinfection = baseline_process_dict['secondary disinfection']
        secondary_disinfection_recovery = baseline_process_dict['secondary disinfection recovery']
        fluoridation = baseline_process_dict['fluoridation']
        fluoridation_recovery = baseline_process_dict['fluoridation recovery']
        softening = baseline_process_dict['softening']
        softening_recovery = baseline_process_dict['softening recovery']
        ph_adjustment = baseline_process_dict['pH adjustment']
        ph_adjustment_installed = baseline_process_dict['no. of pH adjustment units']
        ph_adjustment_recovery = baseline_process_dict['pH adjustment recovery']
        granular_activated_carbon = baseline_process_dict['gac']
        granular_activated_carbon_installed = baseline_process_dict['no. of gac units']
        granular_activated_carbon_recovery = baseline_process_dict['gac recovery']
        reverse_osmosis = baseline_process_dict['ro']
        reverse_osmosis_installed = baseline_process_dict['no. of ro units']
        reverse_osmosis_recovery = baseline_process_dict['ro recovery']
        corrosion_control = baseline_process_dict['corrosion control']
        corrosion_control_recovery = baseline_process_dict['corrosion control recovery']
        aerated_grit = baseline_process_dict['aerated grit']
        aerated_grit_installed = baseline_process_dict['no. of aerated grit units']
        aerated_grit_recovery = baseline_process_dict['aerated grit recovery']
        grinding = baseline_process_dict['grinding']
        grit_removal = baseline_process_dict['grit removal']
        grit_removal_installed = baseline_process_dict['no. of grit removal units']
        grit_removal_recovery = baseline_process_dict['grit removal recovery']
        screening = baseline_process_dict['screening']
        screening_installed = baseline_process_dict['no. of screening units']
        screening_recovery = baseline_process_dict['screening recovery']
        wastewater_sedimentation = baseline_process_dict['wastewater sedimentation']
        wastewater_sedimentation_installed = baseline_process_dict['no. of wastewater sedimentation units']
        wastewater_sedimentation_recovery = baseline_process_dict['wastewater sedimentation recovery']
        secondary_treatment = baseline_process_dict['secondary treatment']
        secondary_treatment_recovery = baseline_process_dict['secondary treatment recovery']
        nitrification_denitrification = baseline_process_dict['nitrification denitrification']
        nitrification_denitrification_installed = baseline_process_dict['no. of nitrification denitrification units']
        nitrification_denitrification_recovery = baseline_process_dict['nitrification denitrification recovery']
        phosphorous_removal = baseline_process_dict['phosphorous removal']
        phosphorous_removal_installed = baseline_process_dict['no. of phosphorous removal units']
        phosphorous_recovery = baseline_process_dict['phosphorous removal recovery']
        wastewater_reverse_osmosis = baseline_process_dict['wastewater ro']
        wastewater_reverse_osmosis_installed = baseline_process_dict['no. of wastewater ro units']
        wastewater_reverse_osmosis_recovery = baseline_process_dict['wastewater ro recovery']
        disinfection = baseline_process_dict['disinfection']
        disinfection_recovery = baseline_process_dict['disinfection recovery']
        dechlorination = baseline_process_dict['dechlorination']
        dechlorination_recovery = baseline_process_dict['dechlorination recovery']
        digestion = baseline_process_dict['digestion']
        digestion_recovery = baseline_process_dict['digestion recovery']
        dewatering = baseline_process_dict['dewatering']
        dewatering_recovery = baseline_process_dict['dewatering recovery']
        softening_process = baseline_process_dict['softening process']
        softening_process_recovery = baseline_process_dict['softening process recovery']
        chemical_addition_input = baseline_process_dict['chemical addition input']
        chemcial_addition_recovery = baseline_process_dict['chemical addition recovery']
        bio_treatment = baseline_process_dict['bio treatment']
        bio_treatment_installed = baseline_process_dict['no. of bio treatment units']
        bio_treatment_recovery = baseline_process_dict['bio treatment recovery']
        volume_reduction = baseline_process_dict['volume reduction']
        volume_reduction_installed = baseline_process_dict['no. of volume reduction units']
        volume_reduction_recovery = baseline_process_dict['volume reduction recovery']
        crystallization = baseline_process_dict['crystallization']
        crystallization_recovery = baseline_process_dict['crystallization recovery']
        new_process_recovery = new_process_dict['new recovery']
        new_elec_min_input = new_process_dict['new electricity min input']
        new_elec_best_input = new_process_dict['new electricity best input']
        new_elec_max_input = new_process_dict['new electricity max input']
        runs = basic_info_dict['mc runs']
        system_type = basic_info_dict['system type']

        if flocculation == 1:
            flocculation_fraction = flocculation_recovery
            flocculation_electricity = np.random.uniform(unit_elec_consumption_dictionary['flocculation']['min'],
                                                            unit_elec_consumption_dictionary['flocculation']['max'],
                                                            (runs, flocculation_installed)) * flocculation_fraction
        else:
            flocculation_electricity = np.zeros(runs)
            flocculation_fraction = 1
        if coagulation == 1:
                coagulation_fraction = flocculation_fraction * coagulation_recovery
                coagulation_electricity = np.random.uniform(unit_elec_consumption_dictionary['coagulation']['min'],
                                                            unit_elec_consumption_dictionary['coagulation']['max'],
                                                            (runs,
                                                             coagulation_installed)) * coagulation_fraction
        else:
                coagulation_electricity = np.zeros(runs)
                coagulation_fraction = flocculation_fraction
        if softening == 1:
            softening_fraction = coagulation_fraction * softening_recovery
            softening_electricity = np.random.uniform(unit_elec_consumption_dictionary['lime_soda_ash_softening']['min'],
                                                           unit_elec_consumption_dictionary['lime_soda_ash_softening']['max'],
                                                           (runs, 1)) * softening_fraction
        else:
            softening_fraction = coagulation_fraction
            softening_electricity = np.zeros(runs)

        if ph_adjustment == 1:
            ph_adjustment_fraction = softening_fraction * ph_adjustment_recovery
            ph_adjustment_electricity = np.random.uniform(unit_elec_consumption_dictionary['pH_adjustment']['min'],
                                                           unit_elec_consumption_dictionary['pH_adjustment']['max'],
                                                           (runs, ph_adjustment_installed)) * ph_adjustment_fraction
        else:
            ph_adjustment_fraction = softening_fraction
            ph_adjustment_electricity  = np.zeros(runs)
        if sedimentation == 1:
            sedimentation_fraction = ph_adjustment_fraction * sedimentation_recovery
            sedimentation_electricity = np.random.uniform(unit_elec_consumption_dictionary['sedimentation']['min'],
                                                           unit_elec_consumption_dictionary['sedimentation']['max'],
                                                           (runs, sedimentation_installed)) * sedimentation_fraction
        else:
            sedimentation_electricity  = np.zeros(runs)
            sedimentation_fraction = ph_adjustment_fraction
        if granular_activated_carbon == 1:
            granular_activated_carbon_fraction = sedimentation_fraction * granular_activated_carbon_recovery
            granular_activated_carbon_electricity = np.random.uniform(unit_elec_consumption_dictionary['granular_activated_carbon']['min'],
                                                           unit_elec_consumption_dictionary['granular_activated_carbon']['max'],
                                                           (runs, granular_activated_carbon_installed)) * granular_activated_carbon_fraction
        else:
            granular_activated_carbon_fraction = sedimentation_fraction
            granular_activated_carbon_electricity  = np.zeros(runs)
        if filtration == 'Generic':
            filtration_fraction = granular_activated_carbon_fraction * filtration_recovery
            filtration_electricity = np.random.uniform(unit_elec_consumption_dictionary['generic_filtration']['min'],
                                                       unit_elec_consumption_dictionary['generic_filtration']['max'],
                                                       (runs, 1)) * filtration_fraction
        elif filtration == 'Cartridge':
            filtration_fraction = granular_activated_carbon_fraction * filtration_recovery
            filtration_electricity = np.random.uniform(unit_elec_consumption_dictionary['cartridge_filtration']['min'],
                                                       unit_elec_consumption_dictionary['cartridge_filtration']['max'],
                                                       (runs, 1)) * filtration_fraction
        elif filtration == 'Diatomaceous Earth':
            filtration_fraction = granular_activated_carbon_fraction * filtration_recovery
            filtration_electricity = np.random.uniform(
                unit_elec_consumption_dictionary['diatomaceous_filtration']['min'],
                unit_elec_consumption_dictionary['diatomaceous_filtration']['max'], (runs, 1)) * filtration_fraction
        elif filtration == 'Greensand':
            filtration_fraction = granular_activated_carbon_fraction * filtration_recovery
            filtration_electricity = np.random.uniform(unit_elec_consumption_dictionary['greensand_filtration']['min'],
                    unit_elec_consumption_dictionary['greensand_filtration']['max'], (runs, 1)) * filtration_fraction
        elif filtration == 'Pressurized Sand':
            filtration_fraction = granular_activated_carbon_fraction * filtration_recovery
            filtration_electricity = np.random.uniform(unit_elec_consumption_dictionary['pressurized_sand_filtration']['min'],
                    unit_elec_consumption_dictionary['pressurized_sand_filtration']['max'], (runs, 1)) * filtration_fraction
        elif filtration == 'Rapid Sand':
            filtration_fraction = granular_activated_carbon_fraction * filtration_recovery
            filtration_electricity = np.random.uniform(unit_elec_consumption_dictionary['rapid_sand_filtration']['min'],
                                                       unit_elec_consumption_dictionary['rapid_sand_filtration']['max'],
                                                       (runs, 1)) * filtration_fraction
        elif filtration == 'Slow Sand':
            filtration_fraction = granular_activated_carbon_fraction * filtration_recovery
            filtration_electricity = np.random.uniform(unit_elec_consumption_dictionary['slow_sand_filtration']['min'],
                unit_elec_consumption_dictionary['slow_sand_filtration']['max'], (runs, 1)) * filtration_fraction
        elif filtration == 'Ultrafiltration Membrane':
            filtration_fraction = granular_activated_carbon_fraction * filtration_recovery
            filtration_electricity = np.random.uniform(unit_elec_consumption_dictionary['ultrafiltration']['min'],
                                                       unit_elec_consumption_dictionary['ultrafiltration']['max'],
                                                       (runs, 1)) * filtration_fraction
        else:
            filtration_electricity = np.zeros(runs)
            filtration_fraction = granular_activated_carbon_fraction
        if (reverse_osmosis == 1) and (source_water == 'Brackish Groundwater'):
            reverse_osmosis_fraction = filtration_fraction * reverse_osmosis_recovery
            reverse_osmosis_electricity = np.random.uniform(unit_elec_consumption_dictionary['reverse_osmosis_brackish']['min'],
                                                           unit_elec_consumption_dictionary['reverse_osmosis_brackish']['max'],
                                                           (runs, reverse_osmosis_installed)) * reverse_osmosis_fraction
        elif (reverse_osmosis == 1) and (source_water == 'Seawater'):
            reverse_osmosis_fraction = filtration_fraction * reverse_osmosis_recovery
            reverse_osmosis_electricity = np.random.uniform(unit_elec_consumption_dictionary['reverse_osmosis_seawater']['min'],
                unit_elec_consumption_dictionary['reverse_osmosis_seawater']['max'],
                (runs, reverse_osmosis_installed)) * reverse_osmosis_recovery
        else:
            reverse_osmosis_fraction = filtration_fraction
            reverse_osmosis_electricity = np.zeros(runs)
        if (primary_disinfection == 'Hypochlorite') and (source_water == "Fresh Surface Water"):
            primary_disinfection_fraction = reverse_osmosis_fraction * primary_disinfection_recovery
            primary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['hypochlorination_surface']['min'],
                                                       unit_elec_consumption_dictionary['hypochlorination_surface']['max'],
                                                       (runs, 1)) * primary_disinfection_fraction
        elif primary_disinfection == 'Hypochlorite' and (source_water == "Fresh Groundwater"):
            primary_disinfection_fraction = reverse_osmosis_fraction * primary_disinfection_recovery
            primary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['hypochlorination_groundwater']['min'],
                    unit_elec_consumption_dictionary['hypochlorination_groundwater']['max'], (runs, 1))  * primary_disinfection_fraction
        elif primary_disinfection == 'Hypochlorite' and (source_water == "Brackish Groundwater"):
            primary_disinfection_fraction = reverse_osmosis_fraction * primary_disinfection_recovery
            primary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['hypochlorination_groundwater']['min'],
                    unit_elec_consumption_dictionary['hypochlorination_groundwater']['max'], (runs, 1))  * primary_disinfection_fraction
        elif primary_disinfection == 'Hypochlorite' and (source_water == "Seawater"):
            primary_disinfection_fraction = reverse_osmosis_fraction * primary_disinfection_recovery
            primary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['hypochlorination_surface']['min'],
                    unit_elec_consumption_dictionary['hypochlorination_surface']['max'], (runs, 1))  * primary_disinfection_fraction
        elif primary_disinfection == 'Chloramine':
            primary_disinfection_fraction = reverse_osmosis_fraction * primary_disinfection_recovery
            primary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['chloramination']['min'],
                    unit_elec_consumption_dictionary['chloramination']['max'], (runs, 1))  * primary_disinfection_fraction
        elif primary_disinfection == 'Iodine':
            primary_disinfection_fraction = reverse_osmosis_fraction * primary_disinfection_recovery
            primary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['iodine_addition']['min'],
                                                       unit_elec_consumption_dictionary['iodine_addition']['max'],
                                                       (runs, 1))  * primary_disinfection_fraction
        elif primary_disinfection == 'Ozonation':
            primary_disinfection_fraction = reverse_osmosis_fraction * primary_disinfection_recovery
            primary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['ozonation']['min'],
                unit_elec_consumption_dictionary['ozonation']['max'], (runs, 1))  * primary_disinfection_fraction
        elif primary_disinfection == 'UV Disinfection':
            primary_disinfection_fraction = reverse_osmosis_fraction * primary_disinfection_recovery
            primary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['uv_disinfection_drinking']['min'],
                                                       unit_elec_consumption_dictionary['uv_disinfection_drinking']['max'],
                                                       (runs, 1))  * primary_disinfection_fraction
        else:
            primary_disinfection_fraction = reverse_osmosis_fraction
            primary_disinfection_electricity = np.zeros(runs)

        if (secondary_disinfection == 'Hypochlorite') and (source_water == "Fresh Surface Water"):
            secondary_disinfection_fraction = primary_disinfection_fraction * secondary_disinfection_recovery
            secondary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['hypochlorination_surface']['min'],
                                                       unit_elec_consumption_dictionary['hypochlorination_surface']['max'],
                                                       (runs, 1)) * secondary_disinfection_fraction
        elif secondary_disinfection == 'Hypochlorite' and (source_water == "Fresh Groundwater"):
            secondary_disinfection_fraction = primary_disinfection_fraction * secondary_disinfection_recovery
            secondary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['hypochlorination_groundwater']['min'],
                    unit_elec_consumption_dictionary['hypochlorination_groundwater']['max'], (runs, 1)) * secondary_disinfection_fraction
        elif secondary_disinfection == 'Hypochlorite' and (source_water == "Brackish Groundwater"):
            secondary_disinfection_fraction = primary_disinfection_fraction * secondary_disinfection_recovery
            secondary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['hypochlorination_groundwater']['min'],
                    unit_elec_consumption_dictionary['hypochlorination_groundwater']['max'], (runs, 1)) * secondary_disinfection_fraction
        elif secondary_disinfection == 'Hypochlorite' and (source_water == "Seawater"):
            secondary_disinfection_fraction = primary_disinfection_fraction * secondary_disinfection_recovery
            secondary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['hypochlorination_surface']['min'],
                    unit_elec_consumption_dictionary['hypochlorination_surface']['max'], (runs, 1)) * secondary_disinfection_fraction
        elif secondary_disinfection == 'Chloramine':
            secondary_disinfection_fraction = primary_disinfection_fraction * secondary_disinfection_recovery
            secondary_disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['chloramination']['min'],
                    unit_elec_consumption_dictionary['chloramination']['max'], (runs, 1)) * secondary_disinfection_fraction
        else:
            secondary_disinfection_fraction = primary_disinfection_fraction
            secondary_disinfection_electricity = np.zeros(runs)

        if fluoridation == 1:
            fluoridation_fraction = secondary_disinfection_fraction * fluoridation_recovery
            fluoridation_electricity = np.random.uniform(unit_elec_consumption_dictionary['fluoridation']['min'],
                                                           unit_elec_consumption_dictionary['fluoridation']['max'],
                                                           (runs, 1)) * fluoridation_fraction
        else:
            fluoridation_fraction = secondary_disinfection_fraction
            fluoridation_electricity = np.zeros(runs)
        if corrosion_control == 'None':
            corrosion_control_fraction = fluoridation_fraction
            corrosion_control_electricity = np.zeros(runs)
        else:
            corrosion_control_fraction = fluoridation_fraction * corrosion_control_recovery
            corrosion_control_electricity =np.random.uniform(unit_elec_consumption_dictionary['bimetallic_phosphate_addition']['min'],
                                                             unit_elec_consumption_dictionary['bimetallic_phosphate_addition']['max'],
                                                             (runs,1)) * corrosion_control_recovery

        if aerated_grit == 1:
            aerated_grit_fraction = aerated_grit_recovery
            aerated_grit_electricity = np.random.uniform(unit_elec_consumption_dictionary['aerated_grit']['min'],
                                                           unit_elec_consumption_dictionary['aerated_grit']['max'],
                                                           (runs, aerated_grit_installed)) * aerated_grit_fraction
        else:
            aerated_grit_fraction = 1
            aerated_grit_electricity  = np.zeros(runs)

        if grinding == 1:
            grinding_fraction = 1
            grinding_electricity = np.random.uniform(unit_elec_consumption_dictionary['grinding']['min'],
                                                           unit_elec_consumption_dictionary['grinding']['max'],
                                                           (runs, 1)) * grinding_fraction
        else:
            grinding_fraction = aerated_grit_fraction
            grinding_electricity = np.zeros(runs)

        if grit_removal == 1:
            grit_removal_fraction = grinding_fraction * grit_removal_recovery
            grit_removal_electricity = np.random.uniform(unit_elec_consumption_dictionary['grit_removal']['min'],
                                                           unit_elec_consumption_dictionary['grit_removal']['max'],
                                                           (runs, grit_removal_installed)) * grit_removal_fraction
        else:
            grit_removal_fraction = grinding_fraction
            grit_removal_electricity  = np.zeros(runs)

        if screening == 1:
            screening_fraction = grinding_fraction * screening_recovery
            screening_electricity = np.random.uniform(unit_elec_consumption_dictionary['screening']['min'],
                                                           unit_elec_consumption_dictionary['screening']['max'],
                                                           (runs, screening_installed)) * screening_fraction
        else:
            screening_fraction = grit_removal_fraction
            screening_electricity  = np.zeros(runs)

        if wastewater_sedimentation == 1:
            wastewater_sedimentation_fraction = grit_removal_fraction * wastewater_sedimentation_recovery
            wastewater_sedimentation_electricity = np.random.uniform(unit_elec_consumption_dictionary['wastewater sedimentation']['min'],
                                                           unit_elec_consumption_dictionary['wastewater sedimentation']['max'],
                                                           (runs, wastewater_sedimentation_installed)) * wastewater_sedimentation_fraction
        else:
            wastewater_sedimentation_fraction = grit_removal_fraction
            wastewater_sedimentation_electricity  = np.zeros(runs)

        if secondary_treatment == 'Activated Sludge and Clarification':
            secondary_treatment_fraction = wastewater_sedimentation_fraction * secondary_treatment_recovery
            secondary_treatment_electricity = (np.random.uniform(unit_elec_consumption_dictionary['activated_sludge']['min'],
                                                       unit_elec_consumption_dictionary['activated_sludge']['max'],
                                                       (runs, 1)) + \
                                              np.random.uniform(unit_elec_consumption_dictionary['aeration']['min'],
                                                       unit_elec_consumption_dictionary['aeration']['max'],
                                                       (runs, 1)) + \
                                              np.random.uniform(unit_elec_consumption_dictionary['clarification']['min'],
                                                       unit_elec_consumption_dictionary['clarification']['max'],
                                                       (runs, 1))) * secondary_treatment_fraction
        elif secondary_treatment == 'Lagoon':
            secondary_treatment_fraction = wastewater_sedimentation_fraction * secondary_treatment_recovery
            secondary_treatment_electricity = np.random.uniform(unit_elec_consumption_dictionary['lagoon']['min'],
                    unit_elec_consumption_dictionary['lagoon']['max'], (runs, 1)) * secondary_treatment_fraction
        elif secondary_treatment == 'Stabilization Pond':
            secondary_treatment_fraction = wastewater_sedimentation_fraction * secondary_treatment_recovery
            secondary_treatment_electricity = np.random.uniform(unit_elec_consumption_dictionary['stabilization']['min'],
                    unit_elec_consumption_dictionary['stabilization']['max'], (runs, 1)) * secondary_treatment_fraction
        elif secondary_treatment == 'Trickling Filter':
            secondary_treatment_fraction = wastewater_sedimentation_fraction * secondary_treatment_recovery
            secondary_treatment_electricity = np.random.uniform(unit_elec_consumption_dictionary['trickling_filter']['min'],
                    unit_elec_consumption_dictionary['tricklking_filter']['max'], (runs, 1)) * secondary_treatment_fraction
        else:
            secondary_treatment_fraction = wastewater_sedimentation_fraction
            secondary_treatment_electricity  = np.zeros(runs)

        if nitrification_denitrification == 1:
            nitrification_denitrification_fraction = secondary_treatment_fraction * nitrification_denitrification_recovery
            nitrification_denitrification_electricity = np.random.uniform(unit_elec_consumption_dictionary['nitrification_denitrification']['min'],
                                                           unit_elec_consumption_dictionary['nitrification_denitrification']['max'],
                                                           (runs, nitrification_denitrification_installed)) * nitrification_denitrification_fraction
        else:
            nitrification_denitrification_fraction = secondary_treatment_fraction
            nitrification_denitrification_electricity  = np.zeros(runs)

        if phosphorous_removal == 1:
            phosphorous_removal_fraction = nitrification_denitrification_fraction * phosphorous_recovery
            phosphorous_removal_electricity = np.random.uniform(unit_elec_consumption_dictionary['phosphorous_removal']['min'],
                                                           unit_elec_consumption_dictionary['phosphorous_removal']['max'],
                                                           (runs, phosphorous_removal_installed)) * phosphorous_removal_fraction
        else:
            phosphorous_removal_fraction = nitrification_denitrification_fraction
            phosphorous_removal_electricity  = np.zeros(runs)

        if wastewater_reverse_osmosis == 1:
            wastewater_reverse_osmosis_fraction = wastewater_reverse_osmosis_recovery * phosphorous_removal_fraction
            wastewater_reverse_osmosis_electricity = np.random.uniform(unit_elec_consumption_dictionary['reverse_osmosis_brackish']['min'],
                                                                       unit_elec_consumption_dictionary['reverse_osmosis_brackish']['max'],
                                                           (runs, wastewater_reverse_osmosis_installed)) * wastewater_reverse_osmosis_fraction
        else:
            wastewater_reverse_osmosis_fraction = phosphorous_removal_fraction
            wastewater_reverse_osmosis_electricity = np.zeros(runs)

        if disinfection == 'Hypochlorite':
            disinfection_fraction = wastewater_reverse_osmosis_fraction * disinfection_recovery
            disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['hypochlorination_wastewater']['min'],
                    unit_elec_consumption_dictionary['hypochlorination_wastewater']['max'], (runs, 1)) * disinfection_fraction
        elif disinfection == 'Ultraviolet':
            disinfection_fraction = wastewater_reverse_osmosis_fraction * disinfection_recovery
            disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['uv_disinfection_wastewater']['min'],
                    unit_elec_consumption_dictionary['uv_disinfection_wastewater']['max'], (runs, 1)) * disinfection_fraction
        elif disinfection == 'Ozone':
            disinfection_fraction = wastewater_reverse_osmosis_fraction * disinfection_recovery
            disinfection_electricity = np.random.uniform(unit_elec_consumption_dictionary['ozonation']['min'],
                    unit_elec_consumption_dictionary['ozonation']['max'], (runs, 1)) * disinfection_fraction
        else:
            disinfection_fraction = wastewater_reverse_osmosis_fraction
            disinfection_electricity = np.zeros(runs)

        if dechlorination == 1:
            dechlorination_fraction = disinfection_fraction * dechlorination_recovery
            dechlorination_electricity = np.random.uniform(unit_elec_consumption_dictionary['dechlorination']['min'],
                                                           unit_elec_consumption_dictionary['dechlorination']['max'],
                                                           (runs, 1)) * dechlorination_fraction
        else:
            dechlorination_fraction = disinfection_fraction
            dechlorination_electricity  = np.zeros(runs)

        if digestion == 'Aerobic Digestion':
            digestion_fraction = (wastewater_sedimentation_fraction - secondary_treatment_fraction) * digestion_recovery
            digestion_electricity = np.random.uniform(unit_elec_consumption_dictionary['aerobic_digestion']['min'],
                    unit_elec_consumption_dictionary['aerobic_digestion']['max'], (runs, 1)) * digestion_fraction
        elif digestion == 'Anaerobic Digestion w/ Biogas Use':
            digestion_fraction = (wastewater_sedimentation_fraction - secondary_treatment_fraction) * digestion_recovery
            digestion_electricity = np.random.uniform(unit_elec_consumption_dictionary['anaerobic_digestion']['min'],
                    unit_elec_consumption_dictionary['anaerobic_digestion']['max'], (runs, 1)) * digestion_fraction
        # TODO Add biogas recovery to below estimates.
        elif digestion == 'Anaerobic Digestion w/o Biogas Use':
            digestion_fraction = (wastewater_sedimentation_fraction - secondary_treatment_fraction) * digestion_recovery
            digestion_electricity = np.random.uniform(unit_elec_consumption_dictionary['anaerobic_digestion']['min'],
                    unit_elec_consumption_dictionary['anaerobic_digestion']['max'], (runs, 1)) * digestion_fraction
        else:
            digestion_fraction = (wastewater_sedimentation_fraction - secondary_treatment_fraction)
            digestion_electricity = np.zeros(runs)

        if dewatering == 'Gravity Thickening':
            dewatering_fraction = digestion_fraction * dewatering_recovery
            dewatering_electricity = np.random.uniform(unit_elec_consumption_dictionary['gravity_thickening']['min'],
                    unit_elec_consumption_dictionary['gravity_thickening']['max'], (runs, 1)) * dewatering_fraction
        elif dewatering == 'Mechanical Dewatering':
            dewatering_fraction = digestion_fraction * dewatering_recovery
            dewatering_electricity = np.random.uniform(unit_elec_consumption_dictionary['mechanical_dewatering']['min'],
                    unit_elec_consumption_dictionary['mechanical_dewatering']['max'], (runs, 1)) * dewatering_fraction
        elif dewatering == 'Polymer Dewatering':
            dewatering_fraction = digestion_fraction * dewatering_recovery
            dewatering_electricity = np.random.uniform(unit_elec_consumption_dictionary['polymer_dewatering']['min'],
                    unit_elec_consumption_dictionary['poiymer_dewatering']['max'], (runs, 1)) * dewatering_fraction
        else:
            dewatering_fraction = digestion_fraction * dewatering_recovery
            dewatering_electricity = np.zeros(runs)

        if softening_process == 1:
            softening_process_fraction = softening_process_recovery
            softening_process_electricity = np.random.uniform(unit_elec_consumption_dictionary['lime_soda_ash_softening']['min'],
                                                           unit_elec_consumption_dictionary['lime_soda_ash_softening']['max'],
                                                           (runs, 1)) * softening_process_fraction
        else:
            softening_process_fraction = 1
            softening_process_electricity = np.zeros(runs)

        if chemical_addition_input == 1:
            chemical_addition_fraction = softening_process_fraction * chemcial_addition_recovery
            chemical_addition_input_electricity = np.random.uniform(unit_elec_consumption_dictionary['chemical_addition']['min'],
                                                           unit_elec_consumption_dictionary['chemical_addition']['max'],
                                                           (runs, 1)) * chemical_addition_fraction
        else:
            chemical_addition_fraction = softening_process_fraction
            chemical_addition_input_electricity  = np.zeros(runs)

        if bio_treatment == 'Activated Sludge and Clarification':
            bio_treatment_fraction = chemical_addition_fraction * bio_treatment_recovery
            bio_treatment_electricity = (np.random.uniform(unit_elec_consumption_dictionary['activated_sludge_industrial']['min'],
                                                       unit_elec_consumption_dictionary['activated_sludge_industrial']['max'],
                                                       (runs, bio_treatment_installed)) + \
                                              np.random.uniform(unit_elec_consumption_dictionary['aeration_industrial']['min'],
                                                       unit_elec_consumption_dictionary['aeration_industrial']['max'],
                                                       (runs, bio_treatment_installed)) + \
                                              np.random.uniform(unit_elec_consumption_dictionary['clarification_industrial']['min'],
                                                       unit_elec_consumption_dictionary['clarification_industrial']['max'],
                                                       (runs, bio_treatment_installed))) * bio_treatment_fraction
        elif bio_treatment == 'Lagoon':
            bio_treatment_fraction = chemical_addition_fraction * bio_treatment_recovery
            bio_treatment_electricity = np.random.uniform(unit_elec_consumption_dictionary['lagoon_industrial']['min'],
                    unit_elec_consumption_dictionary['lagoon_industrial']['max'], (runs, bio_treatment_installed)) * bio_treatment_fraction
        elif bio_treatment == 'Stabilization Pond':
            bio_treatment_fraction = chemical_addition_fraction * bio_treatment_recovery
            bio_treatment_electricity = np.random.uniform(unit_elec_consumption_dictionary['stabilization_industrial']['min'],
                    unit_elec_consumption_dictionary['stabilization_industrial']['max'], (runs, bio_treatment_installed)) * bio_treatment_fraction
        elif bio_treatment == 'Trickling Filter':
            bio_treatment_fraction = chemical_addition_fraction * bio_treatment_recovery
            bio_treatment_electricity = np.random.uniform(unit_elec_consumption_dictionary['trickling_filter_industrial']['min'],
                    unit_elec_consumption_dictionary['tricklking_filter_industrial']['max'], (runs, bio_treatment_installed)) * bio_treatment_fraction
        else:
            bio_treatment_fraction = chemical_addition_fraction
            bio_treatment_electricity = np.zeros(runs)


        if volume_reduction == 'Mechanical Vapor Compression':
            volume_reduction_fraction = bio_treatment_fraction * volume_reduction_recovery
            volume_reduction_electricity = np.random.uniform(unit_elec_consumption_dictionary['mechanical_vapor_compression']['min'],
                                                       unit_elec_consumption_dictionary['mechanical_vapor_compression']['max'],
                                                       (runs, volume_reduction_installed)) * volume_reduction_fraction
        elif volume_reduction == 'Thermal Vapor Compression':
            volume_reduction_fraction = bio_treatment_fraction * volume_reduction_recovery
            volume_reduction_electricity = np.random.uniform(unit_elec_consumption_dictionary['thermal_vapor_compression']['min'],
                    unit_elec_consumption_dictionary['thermal_vapor_compression']['max'], (runs, 1)) * volume_reduction_fraction
        elif volume_reduction == 'Reverse Osmosis':
            volume_reduction_fraction = bio_treatment_fraction * volume_reduction_recovery
            volume_reduction_electricity = np.random.uniform(unit_elec_consumption_dictionary['reverse_osmosis_industrial']['min'],
                    unit_elec_consumption_dictionary['reverse_osmosis_industrial']['max'], (runs, 1)) * volume_reduction_fraction
        elif volume_reduction == 'Forward Osmosis':
            volume_reduction_fraction = bio_treatment_fraction * volume_reduction_recovery
            volume_reduction_electricity = np.random.uniform(unit_elec_consumption_dictionary['forward_osmosis']['min'],
                    unit_elec_consumption_dictionary['forward_osmosis']['max'], (runs, 1)) * volume_reduction_fraction
        elif volume_reduction == 'Multiple-Effect Distillation':
            volume_reduction_fraction = bio_treatment_fraction * volume_reduction_recovery
            volume_reduction_electricity = np.random.uniform(unit_elec_consumption_dictionary['multiple_effect_distillation']['min'],
                    unit_elec_consumption_dictionary['multiple_effect_distillation']['max'], (runs, 1)) * volume_reduction_fraction
        elif volume_reduction == 'Multi-Stage Flash Distillation':
            volume_reduction_fraction = bio_treatment_fraction * volume_reduction_recovery
            volume_reduction_electricity = np.random.uniform(unit_elec_consumption_dictionary['multistage_flash_distillation']['min'],
                                                       unit_elec_consumption_dictionary['multistage_flash_distillation']['max'],
                                                       (runs, 1)) * volume_reduction_fraction
        elif volume_reduction == 'Membrane Distillation':
            volume_reduction_fraction = bio_treatment_fraction * volume_reduction_recovery
            volume_reduction_electricity = np.random.uniform(unit_elec_consumption_dictionary['membrane_distillation']['min'],
                unit_elec_consumption_dictionary['membrane_distillation']['max'], (runs, 1)) * volume_reduction_fraction
        else:
            volume_reduction_fraction = bio_treatment_fraction
            volume_reduction_electricity = np.zeros(runs)

        if crystallization == 1:
            crystallization_fraction = volume_reduction_fraction * crystallization_recovery
            crystallization_electricity = np.random.uniform(unit_elec_consumption_dictionary['crystallization']['min'],
                                                           unit_elec_consumption_dictionary['crystallization']['max'],
                                                           (runs, 1)) * crystallization_fraction
        else:
            crystallization_electricity = np.zeros(runs)

        if new_elec_max_input > 0:
            new_process_electricity = np.random.triangular(new_elec_min_input, new_elec_best_input,
                                                             new_elec_max_input, size=(runs, 1)) * new_process_recovery
        else:
            new_process_electricity = np.zeros(runs)

        total_electricity_consumption = flocculation_electricity + coagulation_electricity  + \
                                        sedimentation_electricity  + filtration_electricity + \
                                        primary_disinfection_electricity + secondary_disinfection_electricity + \
                                        fluoridation_electricity + softening_electricity + ph_adjustment_electricity + \
                                        granular_activated_carbon_electricity + reverse_osmosis_electricity + \
                                        corrosion_control_electricity + aerated_grit_electricity + \
                                        grinding_electricity + grit_removal_electricity + screening_electricity + \
                                        wastewater_sedimentation_electricity + wastewater_reverse_osmosis_electricity + \
                                        secondary_treatment_electricity + nitrification_denitrification_electricity + \
                                        phosphorous_removal_electricity + disinfection_electricity + \
                                        dechlorination_electricity + digestion_electricity + dewatering_electricity + \
                                        softening_process_electricity + chemical_addition_input_electricity + \
                                        bio_treatment_electricity + volume_reduction_electricity + \
                                        crystallization_electricity + new_process_electricity

        return total_electricity_consumption

    def electricity_emissions(geography_info_dict, electricity_consumption_estimates, emissions_factor_dictionary):
        if geography_info_dict['electricity state'] == 'US Average':
            co2_ef = 1122.9 * 453.6 / 1000  # Value from 2014 eGRID.  Reported in lb/MWh converted to g/kWh
            so2_ef = 0.9 * 453.6 / 1000  # Value from 2014 eGRID.  Reported in lb/MWh converted to g/kWh
            nox_ef = 1.6 * 453.6 / 1000  # Value from 2014 eGRID.  Reported in lb/MWh converted to g/kWh
            pm25_ef = (
                                  182034.684 / 4093606000) * 2000 * 453.6 / 1000  # Value from 2014 EIA.  Reported in tons/MWh converted to g/kWh.
        else:
            co2_ef = float(emissions_factor_dictionary['co2'][geography_info_dict['electricity state']])
            so2_ef = float(emissions_factor_dictionary['so2'][geography_info_dict['electricity state']])
            nox_ef = float(emissions_factor_dictionary['nox'][geography_info_dict['electricity state']])
            pm25_ef = float(emissions_factor_dictionary['pm25'][geography_info_dict['electricity state']])

        co2_electricity_emissions = co2_ef * electricity_consumption_estimates
        so2_electricity_emissions = so2_ef * electricity_consumption_estimates
        nox_electricity_emissions = nox_ef * electricity_consumption_estimates
        pm25_electricity_emissions = pm25_ef * electricity_consumption_estimates

        return co2_electricity_emissions, so2_electricity_emissions, nox_electricity_emissions, \
               pm25_electricity_emissions

    def calculate_thermal_consumption(basic_info_dict, baseline_process_dict, new_process_dict):
        source_water = baseline_process_dict['source water']
        flocculation = baseline_process_dict['flocculation']
        flocculation_installed = baseline_process_dict['no. of flocculation units']
        flocculation_recovery = baseline_process_dict['flocculation recovery']
        coagulation = baseline_process_dict['coagulation']
        coagulation_installed = baseline_process_dict['no. of coagulation units']
        coagulation_recovery = baseline_process_dict['coagulation recovery']
        sedimentation = baseline_process_dict['sedimentation']
        sedimentation_installed = baseline_process_dict['no. of sedimentation units']
        sedimentation_recovery = baseline_process_dict['sedimentation recovery']
        filtration = baseline_process_dict['filtration']
        filtration_recovery = baseline_process_dict['filtration recovery']
        primary_disinfection = baseline_process_dict['primary disinfection']
        primary_disinfection_recovery = baseline_process_dict['primary disinfection recovery']
        secondary_disinfection = baseline_process_dict['secondary disinfection']
        secondary_disinfection_recovery = baseline_process_dict['secondary disinfection recovery']
        fluoridation = baseline_process_dict['fluoridation']
        fluoridation_recovery = baseline_process_dict['fluoridation recovery']
        softening = baseline_process_dict['softening']
        softening_recovery = baseline_process_dict['softening recovery']
        ph_adjustment = baseline_process_dict['pH adjustment']
        ph_adjustment_installed = baseline_process_dict['no. of pH adjustment units']
        ph_adjustment_recovery = baseline_process_dict['pH adjustment recovery']
        granular_activated_carbon = baseline_process_dict['gac']
        granular_activated_carbon_installed = baseline_process_dict['no. of gac units']
        granular_activated_carbon_recovery = baseline_process_dict['gac recovery']
        reverse_osmosis = baseline_process_dict['ro']
        reverse_osmosis_installed = baseline_process_dict['no. of ro units']
        reverse_osmosis_recovery = baseline_process_dict['ro recovery']
        corrosion_control = baseline_process_dict['corrosion control']
        corrosion_control_recovery = baseline_process_dict['corrosion control recovery']
        aerated_grit = baseline_process_dict['aerated grit']
        aerated_grit_installed = baseline_process_dict['no. of aerated grit units']
        aerated_grit_recovery = baseline_process_dict['aerated grit recovery']
        grinding = baseline_process_dict['grinding']
        grit_removal = baseline_process_dict['grit removal']
        grit_removal_installed = baseline_process_dict['no. of grit removal units']
        grit_removal_recovery = baseline_process_dict['grit removal recovery']
        screening = baseline_process_dict['screening']
        screening_installed = baseline_process_dict['no. of screening units']
        screening_recovery = baseline_process_dict['screening recovery']
        wastewater_sedimentation = baseline_process_dict['wastewater sedimentation']
        wastewater_sedimentation_installed = baseline_process_dict['no. of wastewater sedimentation units']
        wastewater_sedimentation_recovery = baseline_process_dict['wastewater sedimentation recovery']
        secondary_treatment = baseline_process_dict['secondary treatment']
        secondary_treatment_recovery = baseline_process_dict['secondary treatment recovery']
        nitrification_denitrification = baseline_process_dict['nitrification denitrification']
        nitrification_denitrification_installed = baseline_process_dict['no. of nitrification denitrification units']
        nitrification_denitrification_recovery = baseline_process_dict['nitrification denitrification recovery']
        phosphorous_removal = baseline_process_dict['phosphorous removal']
        phosphorous_removal_installed = baseline_process_dict['no. of phosphorous removal units']
        phosphorous_recovery = baseline_process_dict['phosphorous removal recovery']
        wastewater_reverse_osmosis = baseline_process_dict['wastewater ro']
        wastewater_reverse_osmosis_installed = baseline_process_dict['no. of wastewater ro units']
        wastewater_reverse_osmosis_recovery = baseline_process_dict['wastewater ro recovery']
        disinfection = baseline_process_dict['disinfection']
        disinfection_recovery = baseline_process_dict['disinfection recovery']
        dechlorination = baseline_process_dict['dechlorination']
        dechlorination_recovery = baseline_process_dict['dechlorination recovery']
        digestion = baseline_process_dict['digestion']
        digestion_recovery = baseline_process_dict['digestion recovery']
        dewatering = baseline_process_dict['dewatering']
        dewatering_recovery = baseline_process_dict['dewatering recovery']
        softening_process = baseline_process_dict['softening process']
        softening_process_recovery = baseline_process_dict['softening process recovery']
        chemical_addition_input = baseline_process_dict['chemical addition input']
        chemcial_addition_recovery = baseline_process_dict['chemical addition recovery']
        bio_treatment = baseline_process_dict['bio treatment']
        bio_treatment_installed = baseline_process_dict['no. of bio treatment units']
        bio_treatment_recovery = baseline_process_dict['bio treatment recovery']
        volume_reduction = baseline_process_dict['volume reduction']
        volume_reduction_installed = baseline_process_dict['no. of volume reduction units']
        volume_reduction_recovery = baseline_process_dict['volume reduction recovery']
        crystallization = baseline_process_dict['crystallization']
        crystallization_recovery = baseline_process_dict['crystallization recovery']
        new_process_recovery = new_process_dict['new recovery']
        new_thermal_min_input = new_process_dict['new thermal min input']
        new_thermal_best_input = new_process_dict['new thermal best input']
        new_thermal_max_input = new_process_dict['new thermal max input']
        runs = basic_info_dict['mc runs']
        system_type = basic_info_dict['system type']

        if flocculation == 1:
            flocculation_fraction = flocculation_recovery
        else:
            flocculation_fraction = 1
        if coagulation == 1:
                coagulation_fraction = flocculation_fraction * coagulation_recovery
        else:
                coagulation_fraction = flocculation_fraction
        if softening == 1:
            softening_fraction = coagulation_fraction * softening_recovery
        else:
            softening_fraction = coagulation_fraction

        if ph_adjustment == 1:
            ph_adjustment_fraction = softening_fraction * ph_adjustment_recovery
        else:
            ph_adjustment_fraction = softening_fraction
        if sedimentation == 1:
            sedimentation_fraction = ph_adjustment_fraction * sedimentation_recovery
        else:
            sedimentation_fraction = ph_adjustment_fraction
        if granular_activated_carbon == 1:
            granular_activated_carbon_fraction = sedimentation_fraction * granular_activated_carbon_recovery
        else:
            granular_activated_carbon_fraction = sedimentation_fraction
        if filtration == 'Generic':
            filtration_fraction = granular_activated_carbon_fraction * filtration_recovery
        elif filtration == 'Cartridge':
            filtration_fraction = granular_activated_carbon_fraction * filtration_recovery
        elif filtration == 'Diatomaceous Earth':
            filtration_fraction = granular_activated_carbon_fraction * filtration_recovery
        elif filtration == 'Greensand':
            filtration_fraction = granular_activated_carbon_fraction * filtration_recovery
        elif filtration == 'Pressurized Sand':
            filtration_fraction = granular_activated_carbon_fraction * filtration_recovery
        elif filtration == 'Rapid Sand':
            filtration_fraction = granular_activated_carbon_fraction * filtration_recovery
        elif filtration == 'Slow Sand':
            filtration_fraction = granular_activated_carbon_fraction * filtration_recovery
        elif filtration == 'Ultrafiltration Membrane':
            filtration_fraction = granular_activated_carbon_fraction * filtration_recovery
        else:
            filtration_fraction = granular_activated_carbon_fraction
        if (reverse_osmosis == 1) and (source_water == 'Brackish Groundwater'):
            reverse_osmosis_fraction = filtration_fraction * reverse_osmosis_recovery
        elif (reverse_osmosis == 1) and (source_water == 'Seawater'):
            reverse_osmosis_fraction = filtration_fraction * reverse_osmosis_recovery
        else:
            reverse_osmosis_fraction = filtration_fraction
        if (primary_disinfection == 'Hypochlorite') and (source_water == "Fresh Surface Water"):
            primary_disinfection_fraction = reverse_osmosis_fraction * primary_disinfection_recovery
        elif primary_disinfection == 'Hypochlorite' and (source_water == "Fresh Groundwater"):
            primary_disinfection_fraction = reverse_osmosis_fraction * primary_disinfection_recovery
        elif primary_disinfection == 'Hypochlorite' and (source_water == "Brackish Groundwater"):
            primary_disinfection_fraction = reverse_osmosis_fraction * primary_disinfection_recovery
        elif primary_disinfection == 'Hypochlorite' and (source_water == "Seawater"):
            primary_disinfection_fraction = reverse_osmosis_fraction * primary_disinfection_recovery
        elif primary_disinfection == 'Chloramine':
            primary_disinfection_fraction = reverse_osmosis_fraction * primary_disinfection_recovery
        elif primary_disinfection == 'Iodine':
            primary_disinfection_fraction = reverse_osmosis_fraction * primary_disinfection_recovery
        elif primary_disinfection == 'Ozonation':
            primary_disinfection_fraction = reverse_osmosis_fraction * primary_disinfection_recovery
        elif primary_disinfection == 'UV Disinfection':
            primary_disinfection_fraction = reverse_osmosis_fraction * primary_disinfection_recovery
        else:
            primary_disinfection_fraction = reverse_osmosis_fraction

        if (secondary_disinfection == 'Hypochlorite') and (source_water == "Fresh Surface Water"):
            secondary_disinfection_fraction = primary_disinfection_fraction * secondary_disinfection_recovery
        elif secondary_disinfection == 'Hypochlorite' and (source_water == "Fresh Groundwater"):
            secondary_disinfection_fraction = primary_disinfection_fraction * secondary_disinfection_recovery
        elif secondary_disinfection == 'Hypochlorite' and (source_water == "Brackish Groundwater"):
            secondary_disinfection_fraction = primary_disinfection_fraction * secondary_disinfection_recovery
        elif secondary_disinfection == 'Hypochlorite' and (source_water == "Seawater"):
            secondary_disinfection_fraction = primary_disinfection_fraction * secondary_disinfection_recovery
        elif secondary_disinfection == 'Chloramine':
            secondary_disinfection_fraction = primary_disinfection_fraction * secondary_disinfection_recovery
        else:
            secondary_disinfection_fraction = primary_disinfection_fraction

        if fluoridation == 1:
            fluoridation_fraction = secondary_disinfection_fraction * fluoridation_recovery
        else:
            fluoridation_fraction = secondary_disinfection_fraction
        if corrosion_control == 'None':
            corrosion_control_fraction = fluoridation_fraction
        else:
            corrosion_control_fraction = fluoridation_fraction * corrosion_control_recovery

        if aerated_grit == 1:
            aerated_grit_fraction = aerated_grit_recovery
        else:
            aerated_grit_fraction = 1

        if grinding == 1:
            grinding_fraction = 1
        else:
            grinding_fraction = aerated_grit_fraction

        if grit_removal == 1:
            grit_removal_fraction = grinding_fraction * grit_removal_recovery
        else:
            grit_removal_fraction = grinding_fraction

        if screening == 1:
            screening_fraction = grinding_fraction * screening_recovery
        else:
            screening_fraction = grit_removal_fraction

        if wastewater_sedimentation == 1:
            wastewater_sedimentation_fraction = screening_fraction * wastewater_sedimentation_recovery
        else:
            wastewater_sedimentation_fraction = screening_fraction

        if secondary_treatment == 'Activated Sludge and Clarification':
            secondary_treatment_fraction = wastewater_sedimentation_fraction * secondary_treatment_recovery
        elif secondary_treatment == 'Lagoon':
            secondary_treatment_fraction = wastewater_sedimentation_fraction * secondary_treatment_recovery
        elif secondary_treatment == 'Stabilization Pond':
            secondary_treatment_fraction = wastewater_sedimentation_fraction * secondary_treatment_recovery
        elif secondary_treatment == 'Trickling Filter':
            secondary_treatment_fraction = wastewater_sedimentation_fraction * secondary_treatment_recovery
        else:
            secondary_treatment_fraction = wastewater_sedimentation_fraction

        if nitrification_denitrification == 1:
            nitrification_denitrification_fraction = secondary_treatment_fraction * nitrification_denitrification_recovery
        else:
            nitrification_denitrification_fraction = secondary_treatment_fraction

        if phosphorous_removal == 1:
            phosphorous_removal_fraction = nitrification_denitrification_fraction * phosphorous_removal_recovery
        else:
            phosphorous_removal_fraction = nitrification_denitrification_fraction


        if wastewater_reverse_osmosis == 1:
            wastewater_reverse_osmosis_fraction = wastewater_reverse_osmosis_recovery * phosphorous_removal_fraction
        else:
            wastewater_reverse_osmosis_fraction = phosphorous_removal_fraction

        if disinfection == 'Hypochlorite':
            disinfection_fraction = wastewater_reverse_osmosis_fraction * disinfection_recovery
        elif disinfection == 'Ultraviolet':
            disinfection_fraction = wastewater_reverse_osmosis_fraction * disinfection_recovery
        elif disinfection == 'Ozone':
            disinfection_fraction = wastewater_reverse_osmosis_fraction * disinfection_recovery
        else:
            disinfection_fraction = wastewater_reverse_osmosis_fraction

        if dechlorination == 1:
            dechlorination_fraction = disinfection_fraction * dechlorination_recovery
        else:
            dechlorination_fraction = disinfection_fraction

        if digestion == 'Aerobic Digestion':
            digestion_fraction = (wastewater_sedimentation_fraction - secondary_treatment_fraction) * digestion_recovery
            digestion_thermal = np.random.uniform(unit_therm_consumption_dictionary['aerobic_digestion']['min'],
                    unit_therm_consumption_dictionary['aerobic_digestion']['max'], (runs, 1)) * digestion_fraction
        elif digestion == 'Anaerobic Digestion w/ Biogas Use':
            digestion_fraction = (wastewater_sedimentation_fraction - secondary_treatment_fraction) * digestion_recovery
            digestion_thermal = np.random.uniform(unit_therm_consumption_dictionary['anaerobic_digestion_with_biogas']['min'],
                    unit_therm_consumption_dictionary['anaerobic_digestion_with_biogas']['max'], (runs, 1)) * digestion_fraction
        # TODO Add biogas recovery to below estimates.
        elif digestion == 'Anaerobic Digestion w/o Biogas Use':
            digestion_fraction = (wastewater_sedimentation_fraction - secondary_treatment_fraction) * digestion_recovery
            digestion_thermal = np.random.uniform(unit_therm_consumption_dictionary['anaerobic_digestion_without_biogas']['min'],
                    unit_therm_consumption_dictionary['anaerobic_digestion_without_biogas']['max'], (runs, 1)) * digestion_fraction
        else:
            digestion_fraction = (wastewater_sedimentation_fraction - secondary_treatment_fraction)
            digestion_thermal = np.zeros(runs)

        if dewatering == 'Gravity Thickening':
            dewatering_fraction = digestion_fraction * dewatering_recovery
        elif dewatering == 'Mechanical Dewatering':
            dewatering_fraction = digestion_fraction * dewatering_recovery
        elif dewatering == 'Polymer Dewatering':
            dewatering_fraction = digestion_fraction * dewatering_recovery
        else:
            dewatering_fraction = digestion_fraction * dewatering_recovery

        if softening_process == 1:
            softening_process_fraction = softening_process_recovery
        else:
            softening_process_fraction = 1

        if chemical_addition_input == 1:
            chemical_addition_fraction = softening_process_fraction * chemical_addition_recovery
        else:
            chemical_addition_fraction = softening_process_fraction

        if bio_treatment == 'Activated Sludge and Clarification':
            bio_treatment_fraction = chemical_addition_fraction * bio_treatment_recovery
        elif bio_treatment == 'Lagoon':
            bio_treatment_fraction = chemical_addition_fraction * bio_treatment_recovery
        elif bio_treatment == 'Stabilization Pond':
            bio_treatment_fraction = chemical_addition_fraction * bio_treatment_recovery
        elif bio_treatment == 'Trickling Filter':
            bio_treatment_fraction = chemical_addition_fraction * bio_treatment_recovery
        else:
            bio_treatment_fraction = chemical_addition_fraction
            bio_treatment_electricity = np.zeros(runs)


        if volume_reduction == 'Mechanical Vapor Compression':
            volume_reduction_fraction = bio_treatment_fraction * volume_reduction_recovery
            volume_reduction_thermal = np.zeros(runs)
        elif volume_reduction == 'Thermal Vapor Compression':
            volume_reduction_fraction = bio_treatment_fraction * volume_reduction_recovery
            volume_reduction_thermal = np.random.uniform(unit_therm_consumption_dictionary['thermal_vapor_compression']['min'],
                    unit_therm_consumption_dictionary['thermal_vapor_compression']['max'], (runs, 1)) * volume_reduction_fraction
        elif volume_reduction == 'Reverse Osmosis':
            volume_reduction_fraction = bio_treatment_fraction * volume_reduction_recovery
            volume_reduction_thermal = np.zeros(runs)
        elif volume_reduction == 'Forward Osmosis':
            volume_reduction_fraction = bio_treatment_fraction * volume_reduction_recovery
            volume_reduction_thermal = np.random.uniform(unit_therm_consumption_dictionary['forward_osmosis']['min'],
                    unit_therm_consumption_dictionary['forward_osmosis']['max'], (runs, 1)) * volume_reduction_fraction
        elif volume_reduction == 'Multiple-Effect Distillation':
            volume_reduction_fraction = bio_treatment_fraction * volume_reduction_recovery
            volume_reduction_thermal = np.random.uniform(unit_therm_consumption_dictionary['multiple_effect_distillation']['min'],
                    unit_therm_consumption_dictionary['multiple_effect_distillation']['max'], (runs, 1)) * volume_reduction_fraction
        elif volume_reduction == 'Multi-Stage Flash Distillation':
            volume_reduction_fraction = bio_treatment_fraction * volume_reduction_recovery
            volume_reduction_thermal = np.random.uniform(unit_therm_consumption_dictionary['multistage_flash_distillation']['min'],
                                                       unit_therm_consumption_dictionary['multistage_flash_distillation']['max'],
                                                       (runs, 1)) * volume_reduction_fraction
        elif volume_reduction == 'Membrane Distillation':
            volume_reduction_fraction = bio_treatment_fraction * volume_reduction_recovery
            volume_reduction_thermal = np.random.uniform(unit_therm_consumption_dictionary['membrane_distillation']['min'],
                unit_therm_consumption_dictionary['membrane_distillation']['max'], (runs, 1)) * volume_reduction_fraction
        else:
            volume_reduction_fraction = bio_treatment_fraction
            volume_reduction_thermal = np.zeros(runs)

        if crystallization == 1:
            crystallization_fraction = volume_reduction_fraction * crystallization_recovery
        else:
            crystallization_thermal = np.zeros(runs)

        if new_thermal_max_input > 0:
            new_process_thermal = np.random.triangular(new_thermal_min_input, new_thermal_best_input,
                                                             new_thermal_max_input, runs)
        else:
            new_process_thermal = np.zeros(runs)

        total_thermal_consumption = digestion_thermal + volume_reduction_thermal + new_process_thermal

        return total_thermal_consumption

    def thermal_emissions(thermal_consumption_estimates, emissions_factor_dictionary):
        co2_thermal_emissions = emissions_factor_dictionary['co2'] * thermal_consumption_estimates
        so2_thermal_emissions = emissions_factor_dictionary['so2'] * thermal_consumption_estimates
        nox_thermal_emissions = emissions_factor_dictionary['nox'] * thermal_consumption_estimates
        pm25_thermal_emissions = emissions_factor_dictionary['pm25'] * thermal_consumption_estimates

        return co2_thermal_emissions, so2_thermal_emissions, nox_thermal_emissions, pm25_thermal_emissions


    def calculate_chemical_consumption(basic_info_dict, baseline_process_dict, new_process_dict):
        source_water = baseline_process_dict['source water']
        coagulation = baseline_process_dict['coagulation']
        coagulation_installed = baseline_process_dict['no. of coagulation units']
        filtration = baseline_process_dict['filtration']
        filtration_installed = baseline_process_dict['no. of filtration units']
        primary_disinfection = baseline_process_dict['primary disinfection']
        secondary_disinfection = baseline_process_dict['secondary disinfection']
        fluoridation = baseline_process_dict['fluoridation']
        softening = baseline_process_dict['softening']
        ph_adjustment = baseline_process_dict['pH adjustment']
        ph_adjustment_installed = baseline_process_dict['no. of pH adjustment units']
        granular_activated_carbon = baseline_process_dict['gac']
        granular_activated_carbon_installed = baseline_process_dict['no. of gac units']
        reverse_osmosis = baseline_process_dict['ro']
        reverse_osmosis_installed = baseline_process_dict['no. of ro units']
        corrosion_control = baseline_process_dict['corrosion control']
        disinfection = baseline_process_dict['disinfection']
        dechlorination = baseline_process_dict['dechlorination']
        wastewater_reverse_osmosis = baseline_process_dict['wastewater ro']
        wastewater_reverse_osmosis_installed = baseline_process_dict['no. of wastewater ro units']
        dewatering = baseline_process_dict['dewatering']
        softening_process = baseline_process_dict['softening process']
        bio_treatment = baseline_process_dict['bio treatment']
        volume_reduction = baseline_process_dict['volume reduction']
        volume_reduction_installed = baseline_process_dict['no. of volume reduction units']
        crystallization = baseline_process_dict['crystallization']
        caoh_dose_min_input = baseline_process_dict['caoh dose min input']
        caoh_dose_best_input = baseline_process_dict['caoh dose best input']
        caoh_dose_max_input = baseline_process_dict['caoh dose max input']
        new_caoh_min_input = new_process_dict['new caoh dose min input']
        new_caoh_best_input = new_process_dict['new caoh dose best input']
        new_caoh_max_input = new_process_dict['new caoh dose max input']
        fecl3_dose_min_input = baseline_process_dict['fecl3 dose min input']
        fecl3_dose_best_input = baseline_process_dict['fecl3 dose best input']
        fecl3_dose_max_input = baseline_process_dict['fecl3 dose max input']
        new_fecl3_min_input = new_process_dict['new fecl3 dose min input']
        new_fecl3_best_input = new_process_dict['new fecl3 dose best input']
        new_fecl3_max_input = new_process_dict['new fecl3 dose max input']
        hcl_dose_min_input = baseline_process_dict['hcl dose min input']
        hcl_dose_best_input = baseline_process_dict['hcl dose best input']
        hcl_dose_max_input = baseline_process_dict['hcl dose max input']
        new_hcl_min_input = new_process_dict['new hcl dose min input']
        new_hcl_best_input = new_process_dict['new hcl dose best input']
        new_hcl_max_input = new_process_dict['new hcl dose max input']
        nutrients_dose_min_input = baseline_process_dict['nutrients dose min input']
        nutrients_dose_best_input = baseline_process_dict['nutrients dose best input']
        nutrients_dose_max_input = baseline_process_dict['nutrients dose max input']
        new_nutrients_min_input = new_process_dict['new nutrients dose min input']
        new_nutrients_best_input = new_process_dict['new nutrients dose best input']
        new_nutrients_max_input = new_process_dict['new nutrients dose max input']
        sodium_carbonate_dose_min_input = baseline_process_dict['sodium carbonate dose min input']
        sodium_carbonate_dose_best_input = baseline_process_dict['sodium carbonate dose best input']
        sodium_carbonate_dose_max_input = baseline_process_dict['sodium carbonate dose max input']
        new_sodium_carbonate_min_input = new_process_dict['new sodium carbonate dose min input']
        new_sodium_carbonate_best_input = new_process_dict['new sodium carbonate dose best input']
        new_sodium_carbonate_max_input = new_process_dict['new sodium carbonate dose max input']
        gac_dose_min_input = baseline_process_dict['gac dose min input']
        gac_dose_best_input = baseline_process_dict['gac dose best input']
        gac_dose_max_input = baseline_process_dict['gac dose max input']
        new_gac_min_input = new_process_dict['new gac dose min input']
        new_gac_best_input = new_process_dict['new gac dose best input']
        new_gac_max_input = new_process_dict['new gac dose max input']
        organics_dose_min_input = baseline_process_dict['organics dose min input']
        organics_dose_best_input = baseline_process_dict['organics dose best input']
        organics_dose_max_input = baseline_process_dict['organics dose max input']
        new_organics_min_input = new_process_dict['new organics dose min input']
        new_organics_best_input = new_process_dict['new organics dose best input']
        new_organics_max_input = new_process_dict['new organics dose max input']
        inorganics_dose_min_input = baseline_process_dict['inorganics dose min input']
        inorganics_dose_best_input = baseline_process_dict['inorganics dose best input']
        inorganics_dose_max_input = baseline_process_dict['inorganics dose max input']
        new_inorganics_min_input = new_process_dict['new inorganics dose min input']
        new_inorganics_best_input = new_process_dict['new inorganics dose best input']
        new_inorganics_max_input = new_process_dict['new inorganics dose max input']
        runs = basic_info_dict['mc runs']
        system_type = basic_info_dict['system type']

        if (reverse_osmosis == 1) and (system_type == 'Drinking Water System'):
            if source_water == 'Seawater':
                volume_scale_factor = 1/0.5
            else:
                volume_scale_factor = 1/0.85
        else:
            volume_scale_factor = 1

        if system_type == 'Municipal Wastewater System':
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

        if coagulation == 1:
            coagulation_inorganics = np.random.uniform(unit_inorganics_consumption_dictionary['coagulation']['min'],
                                                            unit_inorganics_consumption_dictionary['coagulation']['max'],
                                                            (runs, coagulation_installed)) * volume_scale_factor
        else:
            coagulation_inorganics = np.zeros(runs)

        if filtration == 'Ultrafiltration Membrane':
            ultrafiltration_organics = np.random.uniform(unit_organics_consumption_dictionary['uf membrane cleaning']['min'],
                                                       unit_organics_consumption_dictionary['uf membrane cleaning']['max'],
                                                       (runs, filtration_installed)) * volume_scale_factor
        else:
            ultrafiltration_organics = np.zeros(runs)

        if (primary_disinfection == 'Hypochlorite') and (source_water == "Fresh Surface Water"):
            primary_disinfection_inorganics = np.random.uniform(unit_inorganics_consumption_dictionary['hypochlorination surface']['min'],
                                                       unit_inorganics_consumption_dictionary['hypochlorination surface']['max'],
                                                       (runs, 1))
        elif primary_disinfection == 'Hypochlorite' and (source_water == "Fresh Groundwater"):
            primary_disinfection_inorganics = np.random.uniform(
                unit_inorganics_consumption_dictionary['hypochlorination groundwater']['min'],
                    unit_inorganics_consumption_dictionary['hypochlorination groundwater']['max'], (runs, 1))
        elif primary_disinfection == 'Hypochlorite' and (source_water == "Brackish Groundwater"):
            primary_disinfection_inorganics = np.random.uniform(
                unit_inorganics_consumption_dictionary['hypochlorination groundwater']['min'],
                    unit_inorganics_consumption_dictionary['hypochlorination groundwater']['max'], (runs, 1))
        elif primary_disinfection == 'Hypochlorite' and (source_water == "Seawater"):
            primary_disinfection_inorganics = np.random.uniform(
                unit_inorganics_consumption_dictionary['hypochlorination surface']['min'],
                    unit_inorganics_consumption_dictionary['hypochlorination surface']['max'], (runs, 1))
        elif primary_disinfection == 'Chloramine':
            primary_disinfection_inorganics = np.random.uniform(
                unit_inorganics_consumption_dictionary['chloramination']['min'],
                    unit_inorganics_consumption_dictionary['chloramination']['max'], (runs, 1))
        elif primary_disinfection == 'Iodine':
            primary_disinfection_inorganics = np.random.uniform(
                unit_inorganics_consumption_dictionary['iodine_addition disinfection']['min'],
                                                       unit_inorganics_consumption_dictionary['iodine_addition disinfection']['max'],
                                                       (runs, 1))
        else:
            primary_disinfection_inorganics = np.zeros(runs)

        if (secondary_disinfection == 'Hypochlorite') and (source_water == "Fresh Surface Water"):
            secondary_disinfection_inorganics = np.random.uniform(unit_inorganics_consumption_dictionary['hypochlorination surface']['min'],
                                                       unit_inorganics_consumption_dictionary['hypochlorination surface']['max'],
                                                       (runs, 1))
        elif secondary_disinfection == 'Hypochlorite' and (source_water == "Fresh Groundwater"):
            secondary_disinfection_inorganics = np.random.uniform(unit_inorganics_consumption_dictionary['hypochlorination groundwater']['min'],
                    unit_inorganics_consumption_dictionary['hypochlorination groundwater']['max'], (runs, 1))
        elif secondary_disinfection == 'Hypochlorite' and (source_water == "Brackish Groundwater"):
            secondary_disinfection_inorganics = np.random.uniform(unit_inorganics_consumption_dictionary['hypochlorination groundwater']['min'],
                    unit_inorganics_consumption_dictionary['hypochlorination groundwater']['max'], (runs, 1))
        elif secondary_disinfection == 'Hypochlorite' and (source_water == "Seawater"):
            secondary_disinfection_inorganics = np.random.uniform(unit_inorganics_consumption_dictionary['hypochlorination surface']['min'],
                    unit_inorganics_consumption_dictionary['hypochlorination surface']['max'], (runs, 1))
        elif secondary_disinfection == 'Chloramine':
            secondary_disinfection_inorganics = np.random.uniform(unit_inorganics_consumption_dictionary['chloramination']['min'],
                    unit_inorganics_consumption_dictionary['chloramination']['max'], (runs, 1))
        else:
            secondary_disinfection_inorganics = np.zeros(runs)

        if fluoridation == 1:
            fluoridation_inorganics = np.random.uniform(unit_inorganics_consumption_dictionary['fluoridation']['min'],
                                                           unit_inorganics_consumption_dictionary['fluoridation']['max'],
                                                           (runs, 1))
        else:
            fluoridation_inorganics = np.zeros(runs)

        if softening == 1:
            softening_soda_ash = np.random.uniform(unit_sodium_carbonate_consumption_dictionary['lime soda ash softening']['min'],
                                                           unit_sodium_carbonate_consumption_dictionary['lime soda ash softening']['max'],
                                                           (runs, 1)) * volume_scale_factor
        else:
            softening_soda_ash = np.zeros(runs)

        if ph_adjustment == 1:
            ph_adjustment_inorganics = np.random.uniform(unit_inorganics_consumption_dictionary['pH adjustment']['min'],
                                                           unit_inorganics_consumption_dictionary['pH adjustment']['max'],
                                                           (runs, ph_adjustment_installed))
        else:
            ph_adjustment_inorganics = np.zeros(runs)

        if granular_activated_carbon == 1:
            gac_granular_activated_carbon = np.random.uniform(unit_gac_consumption_dictionary['granular activated carbon']['min'],
                                                           unit_gac_consumption_dictionary['granular activated carbon']['max'],
                                                           (runs, granular_activated_carbon_installed)) * volume_scale_factor
        else:
            gac_granular_activated_carbon = np.zeros(runs)

        if reverse_osmosis == 1:
            reverse_osmosis_organics = np.random.uniform(unit_organics_consumption_dictionary['ro membrane cleaning']['min'],
                                                           unit_organics_consumption_dictionary['ro membrane cleaning']['max'],
                                                           (runs, reverse_osmosis_installed))
        else:
            reverse_osmosis_organics = np.zeros(runs)

        if corrosion_control == 'Bimetallic Phosphate':
            corrosion_control_organics = np.random.uniform(
                unit_organics_consumption_dictionary['bimetallic phosphate corrosion']['min'],
                unit_organics_consumption_dictionary['bimetallic phosphate corrosion']['max'],
                (runs, 1))
            corrosion_control_inorganics = np.zeros(runs)
        elif corrosion_control == 'Hexametaphosphate':
            corrosion_control_organics = np.random.uniform(
                unit_organics_consumption_dictionary['hexametaphosphate corrosion']['min'],
                unit_organics_consumption_dictionary['hexametaphosphate corrosion']['max'],
                (runs, 1))
            corrosion_control_inorganics = np.zeros(runs)
        elif corrosion_control == 'Orthophosphate':
            corrosion_control_organics = np.random.uniform(
                unit_organics_consumption_dictionary['orthoaphosphate corrosion']['min'],
                unit_organics_consumption_dictionary['orthophosphate corrosion']['max'],
                (runs, 1))
            corrosion_control_inorganics = np.zeros(runs)
        elif corrosion_control == 'Polyphosphate':
            corrosion_control_organics = np.random.uniform(
                unit_organics_consumption_dictionary['polyphosphate corrosion']['min'],
                unit_organics_consumption_dictionary['polyphosphate corrosion']['max'],
                (runs, 1))
            corrosion_control_inorganics = np.zeros(runs)
        elif corrosion_control == 'Permagnate':
            corrosion_control_organics = np.random.uniform(
                unit_organics_consumption_dictionary['permagnate corrosion']['min'],
                unit_organics_consumption_dictionary['permagnate corrosion']['max'],
                (runs, 1))
            corrosion_control_inorganics = np.zeros(runs)
        elif corrosion_control == 'Silicate':
            corrosion_control_inorganics = np.random.uniform(
                unit_inorganics_consumption_dictionary['silicate corrosion']['min'],
                unit_inorganics_consumption_dictionary['silicate corrosion']['max'],
                (runs, 1))
            corrosion_control_organics = np.zeros(runs)
        elif corrosion_control == 'Sodium Bisulfate':
            corrosion_control_inorganics = np.random.uniform(
                unit_inorganics_consumption_dictionary['sodium bisulfate corrosion']['min'],
                unit_inorganics_consumption_dictionary['sodium bisulfate corrosion']['max'],
                (runs, 1))
            corrosion_control_organics = np.zeros(runs)
        elif corrosion_control == 'Sodium Sulfite':
            corrosion_control_inorganics = np.random.uniform(
                unit_inorganics_consumption_dictionary['sodium sulfite corrosion']['min'],
                unit_inorganics_consumption_dictionary['sodium sulfite corrosion']['max'],
                (runs, 1))
            corrosion_control_organics = np.zeros(runs)
        elif corrosion_control == 'Sulfur Dioxide':
            corrosion_control_inorganics = np.random.uniform(
                unit_inorganics_consumption_dictionary['sulfur dioxide corrosion']['min'],
                unit_inorganics_consumption_dictionary['sulfur dioxide corrosion']['max'],
                (runs, 1))
            corrosion_control_organics = np.zeros(runs)

        else:
            corrosion_control_organics = np.zeros(runs)
            corrosion_control_inorganics = np.zeros(runs)

        if disinfection == 'Hypochlorite':
            disinfection_inorganics = np.random.uniform(unit_inorganics_consumption_dictionary['hypochlorination wastewater']['min'],
                    unit_inorganics_consumption_dictionary['hypochlorination wastewater']['max'], (runs, 1)) * tertiary_treatment_scale_factor
        else:
            disinfection_inorganics = np.zeros(runs)

        if wastewater_reverse_osmosis == 1:
            wastewater_reverse_osmosis_organics = np.random.uniform(unit_organics_consumption_dictionary['ro membrane cleaning']['min'],
                                                                       unit_organics_consumption_dictionary['ro membrane cleaning']['max'],
                                                           (runs, wastewater_reverse_osmosis_installed))
        else:
            wastewater_reverse_osmosis_organics = np.zeros(runs)

        if dechlorination == 1:
            dechlorination_inorganics = np.random.uniform(unit_inorganics_consumption_dictionary['sulfur dioxide dechlorination']['min'],
                                                           unit_inorganics_consumption_dictionary['sulfur dioxide dechlorination']['max'],
                                                           (runs, 1)) * tertiary_treatment_scale_factor
        else:
            dechlorination_inorganics = np.zeros(runs)

        if dewatering == 'Polymer Dewatering':
            dewatering_organics = np.random.uniform(unit_organics_consumption_dictionary['polymer_dewatering']['min'],
                    unit_organics_consumption_dictionary['poiymer_dewatering']['max'], (runs, 1)) * solids_processing_scale_factor
        else:
            dewatering_organics = np.zeros(runs)

        if volume_reduction == 'None':
            volume_reduction_organics = np.zeros(runs)
        elif volume_reduction == 0:
            volume_reduction_organics = np.zeros(runs)
        else:
            volume_reduction_organics = np.random.uniform(unit_organics_consumption_dictionary['membrane distillation cleaning']['min'],
                unit_organics_consumption_dictionary['membrane distillation cleaning']['max'], (runs, 1))

        if caoh_dose_max_input > 0:
            industrial_process_caoh = np.random.triangular(caoh_dose_min_input, caoh_dose_best_input,
                                                             caoh_dose_max_input, runs)
        else:
            industrial_process_caoh = np.zeros(runs)

        if new_caoh_max_input > 0:
            new_process_caoh = np.random.triangular(new_caoh_min_input, new_caoh_best_input,
                                                    new_caoh_max_input, runs)
        else:
            new_process_caoh = np.zeros(runs)

        if fecl3_dose_max_input > 0:
            industrial_process_fecl3 = np.random.triangular(fecl3_dose_min_input, fecl3_dose_best_input,
                                                             fecl3_dose_max_input, runs)
        else:
            industrial_process_fecl3 = np.zeros(runs)

        if new_fecl3_max_input > 0:
            new_process_fecl3 = np.random.triangular(new_fecl3_min_input, new_fecl3_best_input,
                                                             new_fecl3_max_input, runs)
        else:
            new_process_fecl3 = np.zeros(runs)

        if hcl_dose_max_input > 0:
            industrial_process_hcl = np.random.triangular(hcl_dose_min_input, hcl_dose_best_input,
                                                             hcl_dose_max_input, runs)
        else:
            industrial_process_hcl = np.zeros(runs)

        if new_hcl_max_input > 0:
            new_process_hcl = np.random.triangular(new_hcl_min_input, new_hcl_best_input,
                                                             new_hcl_max_input, runs)
        else:
            new_process_hcl = np.zeros(runs)

        if nutrients_dose_max_input > 0:
            industrial_process_nutrients = np.random.triangular(nutrients_dose_min_input, nutrients_dose_best_input,
                                                             nutrients_dose_max_input, runs)
        else:
            industrial_process_nutrients = np.zeros(runs)

        if new_nutrients_max_input > 0:
            new_process_nutrients = np.random.triangular(new_nutrients_min_input, new_nutrients_best_input,
                                                             new_nutrients_max_input, runs)
        else:
            new_process_nutrients = np.zeros(runs)

        if sodium_carbonate_dose_max_input > 0:
            industrial_process_soda_ash = np.random.triangular(sodium_carbonate_dose_min_input, sodium_carbonate_dose_best_input,
                                                               sodium_carbonate_dose_max_input, runs)
        else:
            industrial_process_soda_ash = np.zeros(runs)

        if new_sodium_carbonate_max_input > 0:
            new_process_soda_ash = np.random.triangular(new_sodium_carbonate_min_input, new_sodium_carbonate_best_input,
                                                             new_sodium_carbonate_max_input, runs)
        else:
            new_process_soda_ash = np.zeros(runs)

        if gac_dose_max_input > 0:
            industrial_process_gac = np.random.triangular(gac_dose_min_input, gac_dose_best_input,
                                                             gac_dose_max_input, runs)
        else:
            industrial_process_gac = np.zeros(runs)

        if new_gac_max_input > 0:
            new_process_gac = np.random.triangular(new_gac_min_input, new_gac_best_input,
                                                             new_gac_max_input, runs)
        else:
            new_process_gac = np.zeros(runs)

        if inorganics_dose_max_input > 0:
            industrial_process_inorganics = np.random.triangular(inorganics_dose_min_input, inorganics_dose_best_input,
                                                             inorganics_dose_max_input, runs)
        else:
            industrial_process_inorganics = np.zeros(runs)

        if new_inorganics_max_input > 0:
            new_process_inorganics = np.random.triangular(new_inorganics_min_input, new_inorganics_best_input,
                                                             new_inorganics_max_input, runs)
        else:
            new_process_inorganics = np.zeros(runs)

        if organics_dose_max_input > 0:
            industrial_process_organics = np.random.triangular(organics_dose_min_input, organics_dose_best_input,
                                                             organics_dose_max_input, runs)
        else:
            industrial_process_organics = np.zeros(runs)

        if new_organics_max_input > 0:
            new_process_organics = np.random.triangular(new_organics_min_input, new_organics_best_input,
                                                             new_organics_max_input, runs)
        else:
            new_process_organics = np.zeros(runs)

        total_caoh_consumption = industrial_process_caoh + new_process_caoh

        total_fecl3_consumption = industrial_process_fecl3 + new_process_fecl3

        total_hcl_consumption = industrial_process_hcl + new_process_hcl

        total_nutrients_consumption = industrial_process_nutrients + new_process_nutrients

        total_soda_ash_consumption = industrial_process_soda_ash + new_process_soda_ash + softening_soda_ash

        total_gac_consumption = industrial_process_gac + new_process_gac + gac_granular_activated_carbon

        total_inorganics_consumption = industrial_process_inorganics + new_process_inorganics + coagulation_inorganics \
                                       + primary_disinfection_inorganics + secondary_disinfection_inorganics + \
                                       fluoridation_inorganics + ph_adjustment_inorganics + \
                                       corrosion_control_inorganics + disinfection_inorganics + \
                                       dechlorination_inorganics

        total_organics_consumption = industrial_process_organics + new_process_organics + ultrafiltration_organics + \
                                     reverse_osmosis_organics + corrosion_control_organics + \
                                     wastewater_reverse_osmosis_organics + dewatering_organics + \
                                     volume_reduction_organics

        return total_caoh_consumption, total_fecl3_consumption, total_hcl_consumption, total_nutrients_consumption, \
               total_soda_ash_consumption, total_gac_consumption, total_inorganics_consumption, \
               total_organics_consumption

    def chemical_emissions(geography_info, chemical_key, chemical_consumption_estimates,
                           electricity_consumption_dictionary, electrical_emissions_dictionary,
                           thermal_emissions_dictionary, direct_emission_dictionary):

        if geography_info['chemicals state'] == 'US Average':
            chem_manufacturing_distribution = chem_manufacturing_share_dict
        else:
            chem_manufacturing_distribution = empty_state_dict
            state_key = geography_info['chemicals state']
            chem_manufacturing_distribution[state_key] = 1

        chem_manufacturing_distribution_dataframe = pd.DataFrame.from_dict(chem_manufacturing_distribution,
                                                                           orient='index', columns=['Share'])
        chem_manufacturing_distribution_dataframe.index.name = 'state'
        chem_manufacturing_distribution_dataframe.reset_index()

        state_co2_ef_dataframe = pd.DataFrame.from_dict(electrical_emissions_dictionary['co2'],
                                                        orient='index', columns=['co2'], dtype=float)
        state_co2_ef_dataframe.index.name = 'state'
        state_co2_ef_dataframe.reset_index()
        merged_co2_dataframe = pd.merge(chem_manufacturing_distribution_dataframe, state_co2_ef_dataframe, on='state')
        j = 0
        weighted_co2_emissions_factor = 0
        while j <len(merged_co2_dataframe['Share']):
            weighted_co2_emissions_factor += merged_co2_dataframe['Share'][j] * merged_co2_dataframe['co2'][j]
            j += 1
        co2_chem_elec_emissions = weighted_co2_emissions_factor * electricity_consumption_dictionary[chemical_key]

        state_so2_ef_dataframe = pd.DataFrame.from_dict(electrical_emissions_dictionary['so2'],
                                                        orient='index', columns=['so2'], dtype=float)
        state_so2_ef_dataframe.index.name = 'state'
        state_so2_ef_dataframe.reset_index()
        merged_so2_dataframe = pd.merge(chem_manufacturing_distribution_dataframe, state_so2_ef_dataframe, on='state')
        j = 0
        weighted_so2_emissions_factor = 0
        while j <len(merged_so2_dataframe['Share']):
            weighted_so2_emissions_factor += merged_so2_dataframe['Share'][j] * merged_so2_dataframe['so2'][j]
            j += 1
        so2_chem_elec_emissions = weighted_so2_emissions_factor * electricity_consumption_dictionary[chemical_key]

        state_nox_ef_dataframe = pd.DataFrame.from_dict(electrical_emissions_dictionary['nox'],
                                                        orient='index', columns=['nox'], dtype=float)
        state_nox_ef_dataframe.index.name = 'state'
        state_nox_ef_dataframe.reset_index()
        merged_nox_dataframe = pd.merge(chem_manufacturing_distribution_dataframe, state_nox_ef_dataframe, on='state')
        j = 0
        weighted_nox_emissions_factor = 0
        while j <len(merged_nox_dataframe['Share']):
            weighted_nox_emissions_factor += merged_nox_dataframe['Share'][j] * merged_nox_dataframe['nox'][j]
            j += 1
        nox_chem_elec_emissions = weighted_nox_emissions_factor * electricity_consumption_dictionary[chemical_key]

        state_pm25_ef_dataframe = pd.DataFrame.from_dict(electrical_emissions_dictionary['pm25'],
                                                        orient='index', columns=['pm25'], dtype=float)
        state_pm25_ef_dataframe.index.name = 'state'
        state_pm25_ef_dataframe.reset_index()
        merged_pm25_dataframe = pd.merge(chem_manufacturing_distribution_dataframe, state_pm25_ef_dataframe, on='state')
        j = 0
        weighted_pm25_emissions_factor = 0
        while j <len(merged_pm25_dataframe['Share']):
            weighted_pm25_emissions_factor += merged_pm25_dataframe['Share'][j] * merged_pm25_dataframe['pm25'][j]
            j += 1
        pm25_chem_elec_emissions = weighted_pm25_emissions_factor * electricity_consumption_dictionary[chemical_key]

        co2_chem_therm_emissions = thermal_emissions_dictionary[chemical_key]['co2']
        so2_chem_therm_emissions = thermal_emissions_dictionary[chemical_key]['so2']
        nox_chem_therm_emissions = thermal_emissions_dictionary[chemical_key]['nox']
        pm25_chem_therm_emissions = thermal_emissions_dictionary[chemical_key]['pm25']

        co2_chem_direct_emissions = direct_emission_dictionary[chemical_key]['co2']
        so2_chem_direct_emissions = direct_emission_dictionary[chemical_key]['so2']
        nox_chem_direct_emissions = direct_emission_dictionary[chemical_key]['nox']
        pm25_chem_direct_emissions = direct_emission_dictionary[chemical_key]['pm25']

        co2_chemical_emissions = chemical_consumption_estimates/1000 * (co2_chem_elec_emissions + co2_chem_therm_emissions + co2_chem_direct_emissions) #Divide by 1000 for the unit conversions
        so2_chemical_emissions = chemical_consumption_estimates/1000 * (so2_chem_elec_emissions + so2_chem_therm_emissions + so2_chem_direct_emissions) #Divide by 1000 for the unit conversions
        nox_chemical_emissions = chemical_consumption_estimates/1000 * (nox_chem_elec_emissions + nox_chem_therm_emissions + nox_chem_direct_emissions) #Divide by 1000 for the unit conversions
        pm25_chemical_emissions = chemical_consumption_estimates/1000 * (pm25_chem_elec_emissions + pm25_chem_therm_emissions + pm25_chem_direct_emissions) #Divide by 1000 for the unit conversions

        return co2_chemical_emissions, so2_chemical_emissions, nox_chemical_emissions, pm25_chemical_emissions, \
               chem_manufacturing_distribution

    def adjust_for_inflation(uninflated_cost, baseline_year, year_for_inflation):
        inflation_dictionary = {'2000': 724060.77,
                                '2001': 743754.56,
                                '2002': 754648.99,
                                '2003': 770571.62,
                                '2004': 793617.54,
                                '2005': 818758.54,
                                '2006': 852698.89,
                                '2007': 872807.50,
                                '2008': 921685.79,
                                '2009': 902356.55,
                                '2010': 913502.39,
                                '2011': 946650.80,
                                '2012': 959983.91,
                                '2013': 978806.14,
                                '2014': 998307.17,
                                '2015': 1000000.00,
                                '2016': 1008271.39,
                                '2017': 1025694.10,
                                '2018': 1055947.10,
                                '2019': 1075075.21}
        inflated_cost = uninflated_cost * (inflation_dictionary[year_for_inflation]/inflation_dictionary[baseline_year])
        return inflated_cost


    def calculate_climate_damages(co2_unit_emissions, basic_info):
        uninflated_climate_damages = co2_unit_emissions * 1/907184.73999999 * basic_info['system size'] * 365 * basic_info['scc']  #Unit conversions for grams per ton and days per year
        inflated_climate_damages = adjust_for_inflation(uninflated_climate_damages, '2015', basic_info['inflation year'])
        return inflated_climate_damages

    # Create the notebook.
    root = Tk()

    root.title("Water AHEAD")
    note = Notebook(root, width=850, height=700, activefg='black', inactivefg='gray')  # Create a Note book Instance
    note.grid()
    tab1 = note.add_tab(text='General Properties')  # Create an overview tab.
    tab2 = note.add_tab(text='Geography')  # Create a tab to ask about the system geography (i.e., where is it located  or will you be using nationwide averages?)
    tab3 = note.add_tab(text='Drinking Water System')
    tab4 = note.add_tab(text='Municipal Wastewater System')
    tab5 = note.add_tab(text='Industrial Wastewater System')
    tab6 = note.add_tab(text='New Treatment Process')
    tab7 = note.add_tab(text='Results')

    def callback(P):
        if str.isalpha(P):
            return False
        else:
            return True

    vcmd = (tab1.register(callback))

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

    system_type.trace('w', change_dropdown)

    system_size_input = Entry(tab1, validate='all', validatecommand=(vcmd, '%P'))
    system_size_input.insert(END, 0)
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
    model_runs.insert(END, 1000)
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

    Label(tab3, text='Drinking Water System', font=('Arial', 10, 'bold')).grid(column=0, row=0, columnspan=3)

    Label(tab3, text='Source Water Type:', font=('Arial', 10)).grid(column=0, row=1, sticky=E)
    source_water = StringVar(root)
    source_water_choices = ['Fresh Surface Water', 'Fresh Groundwater', 'Brackish Groundwater', 'Seawater']
    source_water.set('Fresh Surface Water')
    source_water_type_popup_menu = OptionMenu(tab3, source_water, *source_water_choices).grid(column=1, row=1,
                                                                                              sticky=W)

    Label(tab3, text='Number of Processes Installed', font=('Arial', 10, 'bold')).grid(column=2, row=1)
    Label(tab3, text='Recovery [%]', font=('Arial', 10, 'bold')).grid(column=3, row=1)
    Label(tab3, text='Preliminary Treatment:', font=('Arial', 10)).grid(column=0, row=3, sticky=E)

    flocculation = BooleanVar(root)
    flocculation_button = Checkbutton(tab3, text='Flocculation', variable=flocculation).grid(column=1, row=2,
                                                                                             sticky=W)
    flocculation_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    flocculation_installed.grid(column=2, row=2)
    flocculation_installed.insert(END, 0)

    flocculation_recovery = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    flocculation_recovery.grid(column=3, row=2)
    flocculation_recovery.insert(END, 100)

    coagulation = BooleanVar(root)
    coagulation_button = Checkbutton(tab3, text='Coagulation', variable=coagulation).grid(column=1, row=3, sticky=W)
    coagulation_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    coagulation_installed.grid(column=2, row=3)
    coagulation_installed.insert(END, 0)

    coagulation_recovery = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    coagulation_recovery.grid(column=3, row=3)
    coagulation_recovery.insert(END, 100)

    sedimentation = BooleanVar(root)
    sedimentation_button = Checkbutton(tab3, text='Sedimentation', variable=sedimentation).grid(column=1, row=4,
                                                                                                sticky=W)
    sedimentation_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    sedimentation_installed.grid(column=2, row=4)
    sedimentation_installed.insert(END, 0)

    sedimentation_recovery = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    sedimentation_recovery.grid(column=3, row=4)
    sedimentation_recovery.insert(END, 100)

    Label(tab3, text='Filtration:', font=('Arial', 10)).grid(column=0, row=5, sticky=E)
    filtration = StringVar(root)
    filtration_choices = ['No Filtration', 'Generic', 'Cartridge', 'Diatomaceous Earth', 'Greensand',
                          'Pressurized Sand', 'Rapid Sand', 'Slow Sand', 'Ultrafiltration Membrane']
    filtration.set('Generic')
    filtration_popup_menu = OptionMenu(tab3, filtration, *filtration_choices).grid(column=1, row=5, sticky=W)
    filtration_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    filtration_installed.grid(column=2, row=5)
    filtration_installed.insert(END, 0)

    filtration_recovery = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    filtration_recovery.grid(column=3, row=5)
    filtration_recovery.insert(END, 100)

    Label(tab3, text='Primary Disinfection:', font=('Arial', 10)).grid(column=0, row=6, sticky=E)
    primary_disinfection = StringVar(root)
    primary_disinfection_choices = ['Hypochlorite', 'Chloramine', 'Iodine', 'Ozonation', 'UV Disinfection', 'None']
    primary_disinfection.set('Hypochlorite')
    primary_disinfection_popup_menu = OptionMenu(tab3, primary_disinfection, *primary_disinfection_choices).grid(
        column=1, row=6, sticky=W)

    primary_disinfection_recovery = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    primary_disinfection_recovery.grid(column=3, row=6)
    primary_disinfection_recovery.insert(END, 100)

    Label(tab3, text='Secondary Disinfection:', font=('Arial', 10)).grid(column=0, row=7, sticky=E)
    secondary_disinfection = StringVar(root)
    secondary_disinfection_choices = ['Hypochlorite', 'Chloramine', 'None']
    secondary_disinfection.set('Hypochlorite')
    secondary_disinfection_popup_menu = OptionMenu(tab3, secondary_disinfection,
                                                   *secondary_disinfection_choices).grid(column=1, row=7, sticky=W)

    secondary_disinfection_recovery = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    secondary_disinfection_recovery.grid(column=3, row=7)
    secondary_disinfection_recovery.insert(END, 100)

    Label(tab3, text='Advanced Processes:', font=('Arial', 10)).grid(column=0, row=8, sticky=E)

    fluoridation = BooleanVar(root)
    fluoridation_button = Checkbutton(tab3, text='Fluoridation', variable=fluoridation).grid(column=1, row=8,
                                                                                             sticky=W)

    fluoridation_recovery = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    fluoridation_recovery.grid(column=3, row=8)
    fluoridation_recovery.insert(END, 100)

    softening = BooleanVar(root)
    softening_button = Checkbutton(tab3, text='Soda Ash Softening', variable=softening).grid(column=1, row=9,
                                                                                             sticky=W)

    softening_recovery = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    softening_recovery.grid(column=3, row=9)
    softening_recovery.insert(END, 100)

    ph_adjustment = BooleanVar(root)
    ph_adjustment_button = Checkbutton(tab3, text='pH Adjustment', variable=ph_adjustment).grid(column=1, row=10,
                                                                                                sticky=W)
    ph_adjustment_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    ph_adjustment_installed.grid(column=2, row=10)
    ph_adjustment_installed.insert(END, 0)

    ph_adjustment_recovery = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    ph_adjustment_recovery.grid(column=3, row=10)
    ph_adjustment_recovery.insert(END, 100)

    granular_activated_carbon = BooleanVar(root)
    granular_activated_carbon_button = Checkbutton(tab3, text='Granular Activated Carbon',
                                                   variable=granular_activated_carbon).grid(column=1, row=11,
                                                                                            sticky=W)
    granular_activated_carbon_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    granular_activated_carbon_installed.grid(column=2, row=11)
    granular_activated_carbon_installed.insert(END, 0)

    granular_activated_carbon_recovery = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    granular_activated_carbon_recovery.grid(column=3, row=11)
    granular_activated_carbon_recovery.insert(END, 100)

    reverse_osmosis = BooleanVar(root)
    reverse_osmosis_button = Checkbutton(tab3, text='Reverse Osmosis', variable=reverse_osmosis).grid(column=1,
                                                                                                      row=12,
                                                                                                      sticky=W)
    reverse_osmosis_installed = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    reverse_osmosis_installed.grid(column=2, row=12)
    reverse_osmosis_installed.insert(END, 0)

    reverse_osmosis_recovery = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    reverse_osmosis_recovery.grid(column=3, row=12)
    reverse_osmosis_recovery.insert(END, 60)

    Label(tab3, text='Corrosion Control:', font=('Arial', 10)).grid(column=0, row=13, sticky=E)
    corrosion_control = StringVar(root)
    corrosion_control_choices = ['Bimetallic Phosphate', 'Hexametaphosphate', 'Orthophosphate', 'Polyphosphate',
                                 'Silicate', 'Permagnate', 'Sodium Bisulfate', 'Sodium Sulfate',
                                 'Sulfur Dioxide', 'None']
    corrosion_control.set('None')
    corrosion_control_popup_menu = OptionMenu(tab3, corrosion_control, *corrosion_control_choices).grid(column=1,
                                                                                                        row=13,
                                                                                                        sticky=W)

    corrosion_control_recovery = Entry(tab3, validate='all', validatecommand=(vcmd, '%P'), width=10)
    corrosion_control_recovery.grid(column=3, row=13)
    corrosion_control_recovery.insert(END, 100)

    Label(tab4, text='Municipal Wastewater System', font=('Arial', 10, 'bold')).grid(column=0, row=0, columnspan=2)
    Label(tab4, text='Treatment Train', font=('Arial', 10, 'bold')).grid(column=0, row=1, columnspan=2)
    Label(tab4, text='Number of Processes Installed', font=('Arial', 10, 'bold')).grid(column=2, row=1)
    Label(tab4, text='Recovery [%]', font=('Arial', 10, 'bold')).grid(column=3, row=1)

    Label(tab4, text='Preliminary Treatment:', font=('Arial', 10)).grid(column=0, row=2, sticky=E)

    aerated_grit = BooleanVar(root)
    aerated_grit_button = Checkbutton(tab4, text='Aerated Grit', variable=aerated_grit).grid(column=1, row=2,
                                                                                             sticky=W)
    aerated_grit_installed = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    aerated_grit_installed.grid(column=2, row=2)
    aerated_grit_installed.insert(END, 0)

    aerated_grit_recovery = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    aerated_grit_recovery.grid(column=3, row=2)
    aerated_grit_recovery.insert(END, 100)

    grinding = BooleanVar(root)
    grinding_button = Checkbutton(tab4, text='Grinding', variable=grinding).grid(column=1, row=3, sticky=W)

    grinding_recovery = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    grinding_recovery.grid(column=3, row=3)
    grinding_recovery.insert(END, 100)

    filtration = BooleanVar(root)
    filtration_button = Checkbutton(tab4, text='Filtration', variable=filtration).grid(column=1, row=4, sticky=W)
    filtration_installed = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    filtration_installed.grid(column=2, row=4)
    filtration_installed.insert(END, 0)

    filtration_recovery = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    filtration_recovery.grid(column=3, row=4)
    filtration_recovery.insert(END, 100)

    grit_removal = BooleanVar(root)
    grit_removal_button = Checkbutton(tab4, text='Grit Removal', variable=grit_removal).grid(column=1, row=5,
                                                                                             sticky=W)
    grit_removal_installed = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    grit_removal_installed.grid(column=2, row=5)
    grit_removal_installed.insert(END, 0)

    grit_removal_recovery = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    grit_removal_recovery.grid(column=3, row=5)
    grit_removal_recovery.insert(END, 100)

    screening = BooleanVar(root)
    screening_button = Checkbutton(tab4, text='Screening', variable=screening).grid(column=1, row=6, sticky=W)
    screening_installed = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    screening_installed.grid(column=2, row=6)
    screening_installed.insert(END, 0)

    screening_recovery = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    screening_recovery.grid(column=3, row=6)
    screening_recovery.insert(END, 100)

    Label(tab4, text='Primary Treatment:', font=('Arial', 10)).grid(column=0, row=7, sticky=E)

    wastewater_sedimentation = BooleanVar(root)
    wastewater_sedimentation_button = Checkbutton(tab4, text='Sedimentation', variable=wastewater_sedimentation).grid(column=1, row=7,
                                                                                                sticky=W)
    wastewater_sedimentation_installed = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    wastewater_sedimentation_installed.grid(column=2, row=7)
    wastewater_sedimentation_installed.insert(END, 0)

    wastewater_sedimentation_recovery = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    wastewater_sedimentation_recovery.grid(column=3, row=7)
    wastewater_sedimentation_recovery.insert(END, 100)

    Label(tab4, text='Secondary Treatment:', font=('Arial', 10)).grid(column=0, row=8, sticky=E)
    secondary_treatment = StringVar(root)
    secondary_treatment_choices = ['Activated Sludge and Clarification', 'Lagoon', 'Stabilization Pond',
                                   'Trickling Filter', 'None']
    secondary_treatment.set('Activated Sludge and Clarification')
    secondary_treatment_popup_menu = OptionMenu(tab4, secondary_treatment, *secondary_treatment_choices).grid(
        column=1, row=8, sticky=W)

    secondary_treatment_recovery = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    secondary_treatment_recovery.grid(column=3, row=8)
    secondary_treatment_recovery.insert(END, 95)

    Label(tab4, text='Tertiary Treatment:', font=('Arial', 10)).grid(column=0, row=9, sticky=E)

    nitrification_denitrification = BooleanVar(root)
    nitrification_denitrification_button = Checkbutton(tab4, text='Nitrification/Denitrification',
                                                       variable=nitrification_denitrification).grid(column=1, row=9,
                                                                                                    sticky=W)
    nitrification_denitrification_installed = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    nitrification_denitrification_installed.grid(column=2, row=9)
    nitrification_denitrification_installed.insert(END, 0)

    nitrification_denitrification_recovery = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    nitrification_denitrification_recovery.grid(column=3, row=9)
    nitrification_denitrification_recovery.insert(END, 100)

    phosphorous_removal = BooleanVar(root)
    phosphorous_removal_button = Checkbutton(tab4, text='Phosphorous Removal', variable=phosphorous_removal).grid(
        column=1, row=10, sticky=W)
    phosphorous_removal_installed = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    phosphorous_removal_installed.grid(column=2, row=10)
    phosphorous_removal_installed.insert(END, 0)

    phosphorous_removal_recovery = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    phosphorous_removal_recovery.grid(column=3, row=10)
    phosphorous_removal_recovery.insert(END, 100)

    wastewater_reverse_osmosis = BooleanVar(root)
    wastewater_reverse_osmosis_button = Checkbutton(tab4, text='Reverse Osmosis', variable=wastewater_reverse_osmosis).grid(column=1,
                                                                                                      row=11,
                                                                                                      sticky=W)
    wastewater_reverse_osmosis_installed = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    wastewater_reverse_osmosis_installed.grid(column=2, row=11)
    wastewater_reverse_osmosis_installed.insert(END, 0)

    wastewater_reverse_osmosis_recovery = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    wastewater_reverse_osmosis_recovery.grid(column=3, row=11)
    wastewater_reverse_osmosis_recovery.insert(END, 80)

    Label(tab4, text='Disinfection:', font=('Arial', 10)).grid(column=0, row=12, sticky=E)
    disinfection = StringVar(root)
    disinfection_choices = ['Hypochlorite', 'Ultraviolet', 'Ozone', 'None']
    disinfection.set('Hypochlorite')
    disinfection_popup_menu = OptionMenu(tab4, disinfection, *disinfection_choices).grid(column=1, row=12, sticky=W)

    disinfection_recovery = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    disinfection_recovery.grid(column=3, row=12)
    disinfection_recovery.insert(END, 100)

    dechlorination = BooleanVar(root)
    dechlorination_button = Checkbutton(tab4, text='Dechlorination', variable=dechlorination).grid(column=1, row=13,
                                                                                                   sticky=W)

    dechlorination_recovery = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    dechlorination_recovery.grid(column=3, row=13)
    dechlorination_recovery.insert(END, 100)

    Label(tab4, text='Digestion:', font=('Arial', 10)).grid(column=0, row=14, sticky=E)
    digestion = StringVar(root)
    digestion_choices = ['Aerobic Digestion', 'Anaerobic Digestion w/o Biogas Use',
                         'Anaerobic Digestion w/ Biogas Use', 'None']
    digestion.set('Aerobic Digestion')
    digestion_popup_menu = OptionMenu(tab4, digestion, *digestion_choices).grid(column=1, row=14, sticky=W)

    digestion_recovery = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    digestion_recovery.grid(column=3, row=14)
    digestion_recovery.insert(END, 100)

    Label(tab4, text='Solids Dewatering:', font=('Arial', 10)).grid(column=0, row=15, sticky=E)
    dewatering = StringVar(root)
    dewatering_choices = ['Gravity Thickening', 'Mechanical Dewatering', 'Polymer Dewatering', 'None']
    dewatering.set('Mechanical Dewatering')
    dewatering_popup_menu = OptionMenu(tab4, dewatering, *dewatering_choices).grid(column=1, row=15, sticky=W)

    dewatering_recovery = Entry(tab4, validate='all', validatecommand=(vcmd, '%P'), width=10)
    dewatering_recovery.grid(column=3, row=15)
    dewatering_recovery.insert(END, 100)

    Label(tab5, text='Industrial Wastewater System', font=('Arial', 10, 'bold')).grid(column=0, row=0, columnspan=5)
    Label(tab5, text='Treatment Train', font=('Arial', 10, 'bold')).grid(column=0, row=1, columnspan=2)
    Label(tab5, text='Number of Processes Installed', font=('Arial', 10, 'bold')).grid(column=2, row=1,
                                                                                       columnspan=3)
    Label(tab5, text='Recovery [%]', font=('Arial', 10, 'bold')).grid(column=5, row=1)

    Label(tab5, text='Soda Ash Softening:', font=('Arial', 10)).grid(column=0, row=2, sticky=E)
    softening_process = BooleanVar(root)
    softening_process_button = Checkbutton(tab5, text='', variable=softening_process).grid(column=1, row=2,
                                                                                           sticky=W)

    softening_process_recovery = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    softening_process_recovery.grid(column=5, row=2)
    softening_process_recovery.insert(END, 100)

    Label(tab5, text='Number of Chemical Addition Reactors:', font=('Arial', 10)).grid(column=0, row=3, sticky=E)
    chemical_addition_input = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    chemical_addition_input.grid(column=1, row=3, sticky=W)
    chemical_addition_input.insert(END, 0)

    chemical_addition_recovery = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    chemical_addition_recovery.grid(column=5, row=3)
    chemical_addition_recovery.insert(END, 100)

    Label(tab5, text='Biological Treatment Process:', font=('Arial', 10)).grid(column=0, row=4, sticky=E)
    bio_treatment = StringVar(root)
    bio_treatment_choices = ['None', 'Activated Sludge and Clarification', 'Lagoon', 'Stabilization Pond',
                             'Trickling Filter']
    bio_treatment.set('None')
    bio_treatment_popup_menu = OptionMenu(tab5, bio_treatment, *bio_treatment_choices).grid(column=1, row=4,
                                                                                            columnspan=3, sticky=W)
    bio_treatment_installed = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    bio_treatment_installed.grid(column=2, row=4, columnspan=3)
    bio_treatment_installed.insert(END, 0)

    bio_treatment_recovery = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    bio_treatment_recovery.grid(column=5, row=4)
    bio_treatment_recovery.insert(END, 100)

    Label(tab5, text='Volume Reduction Process:', font=('Arial', 10)).grid(column=0, row=5, sticky=E)
    volume_reduction = StringVar(root)
    volume_reduction_choices = ['None', 'Mechanical Vapor Compression', 'Thermal Vapor Compression',
                                'Reverse Osmosis', 'Forward Osmosis', 'Multiple Effect Distillation',
                                'Multi-Stage Flash Distillation', 'Membrane Distillation']
    volume_reduction.set('None')
    volume_reduction_popup_menu = OptionMenu(tab5, volume_reduction, *volume_reduction_choices).grid(column=1,
                                                                                                     row=5,
                                                                                                     columnspan=3,
                                                                                                     sticky=W)
    volume_reduction_installed = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    volume_reduction_installed.grid(column=2, row=5, columnspan=3)
    volume_reduction_installed.insert(END, 0)

    volume_reduction_recovery = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    volume_reduction_recovery.grid(column=5, row=5)
    volume_reduction_recovery.insert(END, 65)

    Label(tab5, text='Crystallization:', font=('Arial', 10)).grid(column=0, row=6, sticky=E)
    crystallization = BooleanVar(root)
    crystallization_button = Checkbutton(tab5, text='', variable=crystallization).grid(column=1, row=6, sticky=W)

    crystallization_recovery = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    crystallization_recovery.grid(column=5, row=6)
    crystallization_recovery.insert(END, 95)

    Label(tab5, text='Chemical Consumption', font=('Arial', 10, 'bold')).grid(column=0, row=7, columnspan=5)
    Label(tab5, text='Min', font=('Arial', 10)).grid(column=1, row=8)
    Label(tab5, text='Best', font=('Arial', 10)).grid(column=2, row=8)
    Label(tab5, text='Max', font=('Arial', 10)).grid(column=3, row=8)

    Label(tab5, text='CaOH:', font=('Arial', 10)).grid(column=0, row=9, sticky=E)
    caoh_dose_min_input = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    caoh_dose_min_input.grid(column=1, row=9, sticky=W)
    caoh_dose_min_input.insert(END, 0)
    caoh_dose_best_input = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    caoh_dose_best_input.grid(column=2, row=9, sticky=W)
    caoh_dose_best_input.insert(END, 0)
    caoh_dose_max_input = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    caoh_dose_max_input.grid(column=3, row=9, sticky=W)
    caoh_dose_max_input.insert(END, 0)
    Label(tab5, text='mg/L of wastewater', font=('Arial', 10)).grid(column=4, row=9, sticky=W)

    Label(tab5, text=f'FeCl\N{SUBSCRIPT THREE}:', font=('Arial', 10)).grid(column=0, row=10, sticky=E)
    fecl3_dose_min_input = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    fecl3_dose_min_input.grid(column=1, row=10, sticky=W)
    fecl3_dose_min_input.insert(END, 0)
    fecl3_dose_best_input = Entry(tab5, validate='all', validatecommand=(vcmd, 'P%'), width=10)
    fecl3_dose_best_input.grid(column=2, row=10, sticky=W)
    fecl3_dose_best_input.insert(END, 0)
    fecl3_dose_max_input = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    fecl3_dose_max_input.grid(column=3, row=10, sticky=W)
    fecl3_dose_max_input.insert(END, 0)
    Label(tab5, text='mg/L of wastewater', font=('Arial', 10)).grid(column=4, row=10, sticky=W)

    Label(tab5, text='HCl:', font=('Arial', 10)).grid(column=0, row=11, sticky=E)
    hcl_dose_min_input = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    hcl_dose_min_input.grid(column=1, row=11, sticky=W)
    hcl_dose_min_input.insert(END, 0)
    hcl_dose_best_input = Entry(tab5, validate='all', validatecommand=(vcmd, 'P%'), width=10)
    hcl_dose_best_input.grid(column=2, row=11, sticky=W)
    hcl_dose_best_input.insert(END, 0)
    hcl_dose_max_input = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    hcl_dose_max_input.grid(column=3, row=11, sticky=W)
    hcl_dose_max_input.insert(END, 0)
    Label(tab5, text='mg/L of wastewater', font=('Arial', 10)).grid(column=4, row=11, sticky=W)

    Label(tab5, text='Nutrients:', font=('Arial', 10)).grid(column=0, row=12, sticky=E)
    nutrients_dose_min_input = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    nutrients_dose_min_input.grid(column=1, row=12, sticky=W)
    nutrients_dose_min_input.insert(END, 0)
    nutrients_dose_best_input = Entry(tab5, validate='all', validatecommand=(vcmd, 'P%'), width=10)
    nutrients_dose_best_input.grid(column=2, row=12, sticky=W)
    nutrients_dose_best_input.insert(END, 0)
    nutrients_dose_max_input = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    nutrients_dose_max_input.grid(column=3, row=12, sticky=W)
    nutrients_dose_max_input.insert(END, 0)
    Label(tab5, text='mg/L of wastewater', font=('Arial', 10)).grid(column=4, row=12, sticky=W)

    Label(tab5, text=f'Na\N{SUBSCRIPT TWO}CO\N{SUBSCRIPT THREE}:', font=('Arial', 10)).grid(column=0, row=13,
                                                                                            sticky=E)
    sodium_carbonate_dose_min_input = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    sodium_carbonate_dose_min_input.grid(column=1, row=13, sticky=W)
    sodium_carbonate_dose_min_input.insert(END, 0)
    sodium_carbonate_dose_best_input = Entry(tab5, validate='all', validatecommand=(vcmd, 'P%'), width=10)
    sodium_carbonate_dose_best_input.grid(column=2, row=13, sticky=W)
    sodium_carbonate_dose_best_input.insert(END, 0)
    sodium_carbonate_dose_max_input = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    sodium_carbonate_dose_max_input.grid(column=3, row=13, sticky=W)
    sodium_carbonate_dose_max_input.insert(END, 0)
    Label(tab5, text='mg/L of wastewater', font=('Arial', 10)).grid(column=4, row=13, sticky=W)

    Label(tab5, text='Granular Activated Carbon:', font=('Arial', 10)).grid(column=0, row=14, sticky=E)
    gac_dose_min_input = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    gac_dose_min_input.grid(column=1, row=14, sticky=W)
    gac_dose_min_input.insert(END, 0)
    gac_dose_best_input = Entry(tab5, validate='all', validatecommand=(vcmd, 'P%'), width=10)
    gac_dose_best_input.grid(column=2, row=14, sticky=W)
    gac_dose_best_input.insert(END, 0)
    gac_dose_max_input = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    gac_dose_max_input.grid(column=3, row=14, sticky=W)
    gac_dose_max_input.insert(END, 0)
    Label(tab5, text='mg/L of wastewater', font=('Arial', 10)).grid(column=4, row=14, sticky=W)

    Label(tab5, text='Other Inorganic Chemicals:', font=('Arial', 10)).grid(column=0, row=15, sticky=E)
    inorganics_dose_min_input = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    inorganics_dose_min_input.grid(column=1, row=15, sticky=W)
    inorganics_dose_min_input.insert(END, 0)
    inorganics_dose_best_input = Entry(tab5, validate='all', validatecommand=(vcmd, 'P%'), width=10)
    inorganics_dose_best_input.grid(column=2, row=15, sticky=W)
    inorganics_dose_best_input.insert(END, 0)
    inorganics_dose_max_input = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    inorganics_dose_max_input.grid(column=3, row=15, sticky=W)
    inorganics_dose_max_input.insert(END, 0)
    Label(tab5, text='mg/L of wastewater', font=('Arial', 10)).grid(column=4, row=15, sticky=W)

    Label(tab5, text='Other Organic Chemicals:', font=('Arial', 10)).grid(column=0, row=16, sticky=E)
    organics_dose_min_input = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    organics_dose_min_input.grid(column=1, row=16, sticky=W)
    organics_dose_min_input.insert(END, 0)
    organics_dose_best_input = Entry(tab5, validate='all', validatecommand=(vcmd, 'P%'), width=10)
    organics_dose_best_input.grid(column=2, row=16, sticky=W)
    organics_dose_best_input.insert(END, 0)
    organics_dose_max_input = Entry(tab5, validate='all', validatecommand=(vcmd, '%P'), width=10)
    organics_dose_max_input.grid(column=3, row=16, sticky=W)
    organics_dose_max_input.insert(END, 0)
    Label(tab5, text='mg/L of wastewater', font=('Arial', 10)).grid(column=4, row=16, sticky=W)

    Label(tab6, text='Enter energy consumption and chemical dosages for the new process.').grid(column=0, row=1, columnspan=4)

    Label(tab6, text='Recovery:', font=('Arial', 10)).grid(column=0, row=2, sticky=E)
    new_recovery_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_recovery_input.grid(column=1, row=2, sticky=W)
    new_recovery_input.insert(END, 95)

    Label(tab6, text='Energy Consumption', font=('Arial', 10)).grid(column=0, row=3, columnspan=4)
    Label(tab6, text='Min', font=('Arial', 10)).grid(column=1, row=4)
    Label(tab6, text='Best', font=('Arial', 10)).grid(column=2, row=4)
    Label(tab6, text='Max', font=('Arial', 10)).grid(column=3, row=4)
    Label(tab6, text='Unit Electricity Consumption:', font=('Arial', 10)).grid(column=0, row=5, sticky=E)
    new_elec_min_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_elec_min_input.grid(column=1, row=5, sticky=W)
    new_elec_min_input.insert(END, 0)
    new_elec_best_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_elec_best_input.grid(column=2, row=5, sticky=W)
    new_elec_best_input.insert(END, 0)
    new_elec_max_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_elec_max_input.grid(column=3, row=5, sticky=W)
    new_elec_max_input.insert(END, 0)
    Label(tab6, text='Unit Thermal Energy Consumption:', font=('Arial', 10)).grid(column=0, row=6, sticky=E)
    new_therm_min_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_therm_min_input.grid(column=1, row=6, sticky=W)
    new_therm_min_input.insert(END, 0)
    new_therm_best_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_therm_best_input.grid(column=2, row=6, sticky=W)
    new_therm_best_input.insert(END, 0)
    new_therm_max_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_therm_max_input.grid(column=3, row=6, sticky=W)
    new_therm_max_input.insert(END, 0)
    Label(tab6, text='MJ/m\N{SUPERSCRIPT THREE} of water', font=('Arial', 10)).grid(column=4, row=6, sticky=W)

    Label(tab6, text='Chemical Consumption', font=('Arial', 10)).grid(column=0, row=7, columnspan=4)
    Label(tab6, text='Min', font=('Arial', 10)).grid(column=1, row=8)
    Label(tab6, text='Best', font=('Arial', 10)).grid(column=2, row=8)
    Label(tab6, text='Max', font=('Arial', 10)).grid(column=3, row=8)

    Label(tab6, text='CaOH:', font=('Arial', 10)).grid(column=0, row=9, sticky=E)
    new_caoh_dose_min_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_caoh_dose_min_input.grid(column=1, row=9, sticky=W)
    new_caoh_dose_min_input.insert(END, 0)
    new_caoh_dose_best_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_caoh_dose_best_input.grid(column=2, row=9, sticky=W)
    new_caoh_dose_best_input.insert(END, 0)
    new_caoh_dose_max_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_caoh_dose_max_input.grid(column=3, row=9, sticky=W)
    new_caoh_dose_max_input.insert(END, 0)
    Label(tab6, text='mg/L of water', font=('Arial', 10)).grid(column=4, row=9, sticky=W)

    Label(tab6, text=f'FeCl\N{SUBSCRIPT THREE}:', font=('Arial', 10)).grid(column=0, row=10, sticky=E)
    new_fecl3_dose_min_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_fecl3_dose_min_input.grid(column=1, row=10, sticky=W)
    new_fecl3_dose_min_input.insert(END, 0)
    new_fecl3_dose_best_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_fecl3_dose_best_input.grid(column=2, row=10, sticky=W)
    new_fecl3_dose_best_input.insert(END, 0)
    new_fecl3_dose_max_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_fecl3_dose_max_input.grid(column=3, row=10, sticky=W)
    new_fecl3_dose_max_input.insert(END, 0)
    Label(tab6, text='mg/L of water', font=('Arial', 10)).grid(column=4, row=10, sticky=W)

    Label(tab6, text='HCl:', font=('Arial', 10)).grid(column=0, row=11, sticky=E)
    new_hcl_dose_min_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_hcl_dose_min_input.grid(column=1, row=11, sticky=W)
    new_hcl_dose_min_input.insert(END, 0)
    new_hcl_dose_best_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_hcl_dose_best_input.grid(column=2, row=11, sticky=W)
    new_hcl_dose_best_input.insert(END, 0)
    new_hcl_dose_max_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_hcl_dose_max_input.grid(column=3, row=11, sticky=W)
    new_hcl_dose_max_input.insert(END, 0)
    Label(tab6, text='mg/L of water', font=('Arial', 10)).grid(column=4, row=11, sticky=W)

    Label(tab6, text='Nutrients:', font=('Arial', 10)).grid(column=0, row=12, sticky=E)
    new_nutrients_dose_min_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_nutrients_dose_min_input.grid(column=1, row=12, sticky=W)
    new_nutrients_dose_min_input.insert(END, 0)
    new_nutrients_dose_best_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_nutrients_dose_best_input.grid(column=2, row=12, sticky=W)
    new_nutrients_dose_best_input.insert(END, 0)
    new_nutrients_dose_max_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_nutrients_dose_max_input.grid(column=3, row=12, sticky=W)
    new_nutrients_dose_max_input.insert(END, 0)
    Label(tab6, text='mg/L of water', font=('Arial', 10)).grid(column=4, row=12, sticky=W)

    Label(tab6, text=f'Na\N{SUBSCRIPT TWO}CO\N{SUBSCRIPT THREE}:', font=('Arial', 10)).grid(column=0, row=13, sticky=E)
    new_sodium_carbonate_dose_min_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_sodium_carbonate_dose_min_input.grid(column=1, row=13, sticky=W)
    new_sodium_carbonate_dose_min_input.insert(END, 0)
    new_sodium_carbonate_dose_best_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_sodium_carbonate_dose_best_input.grid(column=2, row=13, sticky=W)
    new_sodium_carbonate_dose_best_input.insert(END, 0)
    new_sodium_carbonate_dose_max_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_sodium_carbonate_dose_max_input.grid(column=3, row=13, sticky=W)
    new_sodium_carbonate_dose_max_input.insert(END, 0)
    Label(tab6, text='mg/L of water', font=('Arial', 10)).grid(column=4, row=13, sticky=W)

    Label(tab6, text='Granular Activated Carbon:', font=('Arial', 10)).grid(column=0, row=14, sticky=E)
    new_gac_dose_min_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_gac_dose_min_input.grid(column=1, row=14, sticky=W)
    new_gac_dose_min_input.insert(END, 0)
    new_gac_dose_best_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_gac_dose_best_input.grid(column=2, row=14, sticky=W)
    new_gac_dose_best_input.insert(END, 0)
    new_gac_dose_max_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_gac_dose_max_input.grid(column=3, row=14, sticky=W)
    new_gac_dose_max_input.insert(END, 0)
    Label(tab6, text='mg/L of water', font=('Arial', 10)).grid(column=4, row=14, sticky=W)

    Label(tab6, text='Other Inorganic Chemicals:', font=('Arial', 10)).grid(column=0, row=15, sticky=E)
    new_inorganics_dose_min_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_inorganics_dose_min_input.grid(column=1, row=15, sticky=W)
    new_inorganics_dose_min_input.insert(END, 0)
    new_inorganics_dose_best_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_inorganics_dose_best_input.grid(column=2, row=15, sticky=W)
    new_inorganics_dose_best_input.insert(END, 0)
    new_inorganics_dose_max_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_inorganics_dose_max_input.grid(column=3, row=15, sticky=W)
    new_inorganics_dose_max_input.insert(END, 0)
    Label(tab6, text='mg/L of water', font=('Arial', 10)).grid(column=4, row=15, sticky=W)

    Label(tab6, text='Other Organic Chemicals:', font=('Arial', 10)).grid(column=0, row=16, sticky=E)
    new_organics_dose_min_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_organics_dose_min_input.grid(column=1, row=16, sticky=W)
    new_organics_dose_min_input.insert(END, 0)
    new_organics_dose_best_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_organics_dose_best_input.grid(column=2, row=16, sticky=W)
    new_organics_dose_best_input.insert(END, 0)
    new_organics_dose_max_input = Entry(tab6, validate='all', validatecommand=(vcmd, '%P'), width=10)
    new_organics_dose_max_input.grid(column=3, row=16, sticky=W)
    new_organics_dose_max_input.insert(END, 0)
    Label(tab6, text='mg/L of water', font=('Arial', 10)).grid(column=4, row=16, sticky=W)

    Label(tab7, text='Results', font=('Arial', 10, 'bold')).grid(column=0, row=0, columnspan=8)
    Label(tab7, text='Embedded Air Emissions [g/m\N{SUPERSCRIPT THREE}]', font=('Arial', 10)).grid(column=3, row=1, columnspan=4)
    Label(tab7, text='Annual Air Damages [$/yr]', font=('Arial', 10)).grid(column=7, row=1, columnspan=3)
    Label(tab7, text='Required Dose', font=('Arial', 10)).grid(column=1, row=2, columnspan=2)
    Label(tab7, text='NOx', font=('Arial', 10)).grid(column=3, row=2)
    Label(tab7, text='SO\N{SUBSCRIPT TWO}', font=('Arial', 10)).grid(column=4, row=2)
    Label(tab7, text='PM2.5', font=('Arial', 10)).grid(column=5, row=2)
    Label(tab7, text='CO\N{SUBSCRIPT TWO}', font=('Arial', 10)).grid(column=6, row=2)
    Label(tab7, text='Health', font=('Arial', 10)).grid(column=7, row=2)
    Label(tab7, text='Climate', font=('Arial', 10)).grid(column=8, row=2)
    Label(tab7, text='Total', font=('Arial', 10, 'italic')).grid(column=9, row=2)
    Label(tab7, text='Energy', font=('Arial', 10, 'italic')).grid(column=0, row=3)
    Label(tab7, text='(25th-75th)', font=('Arial', 10, 'italic')).grid(column=0, row=4)
    Label(tab7, text='Electricity', font=('Arial', 10)).grid(column=0, row=5)
    Label(tab7, text='(25th-75th)', font=('Arial', 10)).grid(column=0, row=6)
    Label(tab7, text='Thermal', font=('Arial', 10)).grid(column=0, row=7)
    Label(tab7, text='25th-75th', font=('Arial', 10)).grid(column=0, row=8)
    Label(tab7, text='Chemicals', font=('Arial', 10, 'italic')).grid(column=0, row=9)
    Label(tab7, text='(25th-75th)', font=('Arial', 10, 'italic')).grid(column=0, row=10)
    Label(tab7, text='CaOH', font=('Arial', 10)).grid(column=0, row=11)
    Label(tab7, text='(25th-75th)', font=('Arial', 10)).grid(column=0, row=12)
    Label(tab7, text='FeCl\N{SUBSCRIPT THREE}', font=('Arial', 10)).grid(column=0, row=13)
    Label(tab7, text='(25th-75th)', font=('Arial', 10)).grid(column=0, row=14)
    Label(tab7, text='HCl', font=('Arial', 10)).grid(column=0, row=15)
    Label(tab7, text='(25th-75th)', font=('Arial', 10)).grid(column=0, row=16)
    Label(tab7, text='Nutrients', font=('Arial', 10)).grid(column=0, row=17)
    Label(tab7, text='(25th-75th)', font=('Arial', 10)).grid(column=0, row=18)
    Label(tab7, text='Na\N{SUBSCRIPT TWO}CO\N{SUBSCRIPT THREE}', font=('Arial', 10)).grid(column=0, row=19)
    Label(tab7, text='(25th-75th)', font=('Arial', 10)).grid(column=0, row=20)
    Label(tab7, text='Activated Carbon', font=('Arial', 10)).grid(column=0, row=21)
    Label(tab7, text='(25th-75th)', font=('Arial', 10)).grid(column=0, row=22)
    Label(tab7, text='Assorted Inorganics', font=('Arial', 10)).grid(column=0, row=23)
    Label(tab7, text='(25th-75th)', font=('Arial', 10)).grid(column=0, row=24)
    Label(tab7, text='Associated Organics', font=('Arial', 10)).grid(column=0, row=25)
    Label(tab7, text='(25th-75th)', font=('Arial', 10)).grid(column=0, row=26)

    Label(tab7, text='kWh/m\N{SUPERSCRIPT THREE}', font=('Arial', 10)).grid(column=2, row=5, rowspan=2)
    Label(tab7, text='MJ/m\N{SUPERSCRIPT THREE}', font=('Arial', 10)).grid(column=2, row=7, rowspan=2)
    Label(tab7, text='mg/L', font=('Arial', 10)).grid(column=2, row=11, rowspan=2)
    Label(tab7, text='mg/L', font=('Arial', 10)).grid(column=2, row=13, rowspan=2)
    Label(tab7, text='mg/L', font=('Arial', 10)).grid(column=2, row=15, rowspan=2)
    Label(tab7, text='mg/L', font=('Arial', 10)).grid(column=2, row=17, rowspan=2)
    Label(tab7, text='mg/L', font=('Arial', 10)).grid(column=2, row=19, rowspan=2)
    Label(tab7, text='mg/L', font=('Arial', 10)).grid(column=2, row=21, rowspan=2)
    Label(tab7, text='mg/L', font=('Arial', 10)).grid(column=2, row=23, rowspan=2)
    Label(tab7, text='mg/L', font=('Arial', 10)).grid(column=2, row=25, rowspan=2)

    def round_sig(x, sig=2):

        if x == 0:
            return 0

        else:
            try:
                return round(x, sig - int(np.floor(np.log10(abs(x)))) - 1)

            except ValueError:
                return 0

    # Read in emissions data on the the average emissions factor per state and AP2 damages data.
    # Start with the CO2, SO2, and NOx emissions.
    average_state_efs = pd.read_csv(fileDir / 'Data' / '2014 State MEFs.csv', header=None)
    average_state_list = average_state_efs.iloc[0].dropna()
    co2_ef_list = average_state_efs.iloc[2]
    co2_ef_list = co2_ef_list.iloc[1::2]
    so2_ef_list = average_state_efs.iloc[4]
    so2_ef_list = so2_ef_list.iloc[1::2]
    nox_ef_list = average_state_efs.iloc[6]
    nox_ef_list = nox_ef_list.iloc[1::2]
    i = 0
    average_state_list_cleaned = []
    co2_ef_list_cleaned = []
    so2_ef_list_cleaned = []
    nox_ef_list_cleaned = []
    while i < 95:
        average_state_list_cleaned.append(average_state_list[i])
        co2_ef_list_cleaned.append(co2_ef_list[i+1])
        so2_ef_list_cleaned.append(so2_ef_list[i+1])
        nox_ef_list_cleaned.append(nox_ef_list[i+1])
        i += 2

    state_mefs = [('state', average_state_list_cleaned), ('co2', co2_ef_list_cleaned), ('so2', so2_ef_list_cleaned),
                  ('nox', nox_ef_list_cleaned)]
    mefs = pd.DataFrame.from_items(state_mefs)

    # Now read in and merge the PM2.5 emissions factors
    state_pm25_efs = pd.read_csv(fileDir / 'Data' / 'State PM25.csv')
    state_ef_data = pd.merge(mefs, state_pm25_efs, on='state')

    # Now read in AP2 damages and calculate the state-level average damages.
    county_level_ap2_damages = pd.read_csv(fileDir / 'Data' / 'AP2 Damages.csv')
    county_level_ap2_damages.drop('fips', axis=1, inplace=True)
    state_level_average_damages = county_level_ap2_damages.groupby('state').mean()
    state_level_average_damages['state_fips'] = state_level_average_damages.index
    state_fips_code_go_betweens = pd.read_csv(fileDir / 'Data' / 'state fips code go betweens.csv')
    state_level_damages = pd.merge(state_level_average_damages, state_fips_code_go_betweens, on='state_fips')

    # Finally create master list of EFs and Damage factors.
    state_level_efs_and_damages = pd.merge(state_ef_data, state_level_damages, on='state')
    state_level_efs_and_damages.drop('state_fips', axis=1, inplace=True)
    state_level_dictionary = state_level_efs_and_damages.set_index('state').to_dict()

    # And let's go ahead and create the dictionaries for the different chemicals and the emissions associated with
    # generating them.
    direct_chemical_emissions = {'caoh': {'nox': 0, 'so2': 0.15, 'pm25': 0.056, 'co2': 770},
                                 'fecl3': {'nox': 0, 'so2': 0, 'pm25': 0, 'co2': 0},
                                 'hcl': {'nox': 2.5, 'so2': 4.9, 'pm25': 0.067, 'co2': 2620},
                                 'nutrients': {'nox': 0.03, 'so2': 8.2, 'pm25': 0.2, 'co2': 7.1},
                                 'na2co3': {'nox': 0, 'so2': 0, 'pm25': 96.5, 'co2': 415},
                                 'gac': {'nox': 0, 'so2': 0, 'pm25': 0, 'co2': 0},
                                 'hypochlorite': {'nox': 0, 'so2': 0, 'pm25': 0, 'co2': 0},
                                 'inorganics': {'nox': 0, 'so2': 0.15, 'pm25': 0.056, 'co2': 770},
                                 'organics': {'nox': 0.12, 'so2': 0.098, 'pm25': 0.0076, 'co2': 170}}

    thermal_energy_consumption = {'caoh': {'bit coal': 0.172, 'pet': 0.0000322, 'rfo': 0, 'natgas': 0.0021, 'diesel': 0.000945},
                                  'fecl3': {'bit coal': 0,'pet': 0, 'rfo': 0, 'natgas': 0, 'diesel': 0},
                                  'hcl': {'bit coal': 0.3181+0.0266,'pet': 0, 'rfo': 0, 'natgas': 0.29839, 'diesel': 0.02643},
                                  'nutrients': {'bit coal': 0,'pet': 0, 'rfo': 0, 'natgas': 0, 'diesel': 0},
                                  'na2co3': {'bit coal': 0.108,'pet': 0.000032, 'rfo': 0, 'natgas': 0.021, 'diesel': 0.00095},
                                  'gac': {'bit coal': 0.36,'pet': 0, 'rfo': 0, 'natgas': 0.126, 'diesel': 0},
                                  'hypochlorite': {'bit coal': 0.36, 'pet': 0, 'rfo': 0, 'natgas': 0.126, 'diesel': 0},
                                  'inorganics': {'bit coal': 0.172,'pet': 0.000032, 'rfo': 0, 'natgas': 0.021, 'diesel': 0.00095},
                                  'organics': {'bit coal': 0.00078,'pet': 0.00023, 'rfo': 0.024, 'natgas': 0.12, 'diesel': 0.00093}}


    def caclulate_thermal_energy_emissions_for_chemical_manufacturing(energy_consumed_dictionary):
        bit_coal_combustion_per_kg = {'co2': 2633, 'nox': 5.75, 'so2': 16.6, 'pm25': 0}  # [g/m^3] from NREL's LCI database
        pet_combustion_per_L = {'co2': 1721, 'nox': 2.6, 'so2': 0, 'pm25': 0}  # [g/m^3] from NREL's LCI database
        rfo_combustion_per_L = {'co2': 3263.2, 'nox': 7.03, 'so2': 5.12, 'pm25': 0}  # [g/m^3] from NREL's LCI database
        ng_combustion_per_m3 = {'co2': 1960.9, 'nox': 1.6, 'so2': 0.0101, 'pm25': 0}  # [g/m^3] from NREL's LCI database
        diesel_combustion_per_L = {'co2': 2730, 'nox': 2.87, 'so2': 0.599, 'pm25': 0}  # [g/m^3] from NREL's LCI database

        fuel_co2 = (energy_consumed_dictionary['bit coal'] * bit_coal_combustion_per_kg['co2']) + \
                   (energy_consumed_dictionary['pet'] * pet_combustion_per_L['co2']) + \
                   (energy_consumed_dictionary['rfo'] * rfo_combustion_per_L['co2']) + \
                   (energy_consumed_dictionary['natgas'] * ng_combustion_per_m3['co2']) + \
                   (energy_consumed_dictionary['diesel'] * diesel_combustion_per_L['co2'])
        fuel_nox = (energy_consumed_dictionary['bit coal'] * bit_coal_combustion_per_kg['nox']) + \
                   (energy_consumed_dictionary['pet'] * pet_combustion_per_L['nox']) + \
                   (energy_consumed_dictionary['rfo'] * rfo_combustion_per_L['nox']) + \
                   (energy_consumed_dictionary['natgas'] * ng_combustion_per_m3['nox']) + \
                   (energy_consumed_dictionary['diesel'] * diesel_combustion_per_L['nox'])
        fuel_so2 = (energy_consumed_dictionary['bit coal'] * bit_coal_combustion_per_kg['so2']) + \
                   (energy_consumed_dictionary['pet'] * pet_combustion_per_L['so2']) + \
                   (energy_consumed_dictionary['rfo'] * rfo_combustion_per_L['so2']) + \
                   (energy_consumed_dictionary['natgas'] * ng_combustion_per_m3['so2']) + \
                   (energy_consumed_dictionary['diesel'] * diesel_combustion_per_L['so2'])
        fuel_pm25 = (energy_consumed_dictionary['bit coal'] * bit_coal_combustion_per_kg['pm25']) + \
                    (energy_consumed_dictionary['pet'] * pet_combustion_per_L['pm25']) + \
                    (energy_consumed_dictionary['rfo'] * rfo_combustion_per_L['pm25']) + \
                    (energy_consumed_dictionary['natgas'] * ng_combustion_per_m3['pm25']) + \
                    (energy_consumed_dictionary['diesel'] * diesel_combustion_per_L['pm25'])
        fuel_emissions_dictionary = {'co2': fuel_co2, 'nox': fuel_nox, 'so2': fuel_so2, 'pm25': fuel_pm25}

        return fuel_emissions_dictionary

    caoh_emissions_dictionary = caclulate_thermal_energy_emissions_for_chemical_manufacturing(
        thermal_energy_consumption['caoh'])
    fecl3_emissions_dictionary = caclulate_thermal_energy_emissions_for_chemical_manufacturing(
        thermal_energy_consumption['fecl3'])
    hcl_emissions_dictionary = caclulate_thermal_energy_emissions_for_chemical_manufacturing(
        thermal_energy_consumption['hcl'])
    nutrients_emissions_dictionary = caclulate_thermal_energy_emissions_for_chemical_manufacturing(
        thermal_energy_consumption['nutrients'])
    na2co3_emissions_dictionary = caclulate_thermal_energy_emissions_for_chemical_manufacturing(
        thermal_energy_consumption['na2co3'])
    gac_emissions_dictionary = caclulate_thermal_energy_emissions_for_chemical_manufacturing(
        thermal_energy_consumption['gac'])
    hypochlorite_emissions_dictionary = caclulate_thermal_energy_emissions_for_chemical_manufacturing(
        thermal_energy_consumption['hypochlorite'])
    inorganics_emissions_dictionary = caclulate_thermal_energy_emissions_for_chemical_manufacturing(
        thermal_energy_consumption['inorganics'])
    organics_emissions_dictionary = caclulate_thermal_energy_emissions_for_chemical_manufacturing(
        thermal_energy_consumption['organics'])

    thermal_chemical_emissions = {'caoh': {'co2': caoh_emissions_dictionary['co2'],
                                           'nox': caoh_emissions_dictionary['nox'],
                                           'so2': caoh_emissions_dictionary['so2'],
                                           'pm25': caoh_emissions_dictionary['pm25']},
                                  'fecl3': {'co2': fecl3_emissions_dictionary['co2'],
                                           'nox': fecl3_emissions_dictionary['nox'],
                                           'so2': fecl3_emissions_dictionary['so2'],
                                           'pm25': fecl3_emissions_dictionary['pm25']},
                                  'hcl': {'co2': hcl_emissions_dictionary['co2'],
                                           'nox': hcl_emissions_dictionary['nox'],
                                           'so2': hcl_emissions_dictionary['so2'],
                                           'pm25': hcl_emissions_dictionary['pm25']},
                                  'nutrients': {'co2': nutrients_emissions_dictionary['co2'],
                                           'nox': nutrients_emissions_dictionary['nox'],
                                           'so2': nutrients_emissions_dictionary['so2'],
                                           'pm25': nutrients_emissions_dictionary['pm25']},
                                  'na2co3':{'co2': na2co3_emissions_dictionary['co2'],
                                           'nox': na2co3_emissions_dictionary['nox'],
                                           'so2': na2co3_emissions_dictionary['so2'],
                                           'pm25': na2co3_emissions_dictionary['pm25']},
                                  'gac': {'co2': gac_emissions_dictionary['co2'],
                                           'nox': gac_emissions_dictionary['nox'],
                                           'so2': gac_emissions_dictionary['so2'],
                                           'pm25': gac_emissions_dictionary['pm25']},
                                  'hypochlorite': {'co2': hypochlorite_emissions_dictionary['co2'],
                                           'nox': hypochlorite_emissions_dictionary['nox'],
                                           'so2': hypochlorite_emissions_dictionary['so2'],
                                           'pm25': hypochlorite_emissions_dictionary['pm25']},
                                  'inorganics': {'co2': inorganics_emissions_dictionary['co2'],
                                           'nox': inorganics_emissions_dictionary['nox'],
                                           'so2': inorganics_emissions_dictionary['so2'],
                                           'pm25': inorganics_emissions_dictionary['pm25']},
                                  'organics': {'co2': organics_emissions_dictionary['co2'],
                                           'nox': organics_emissions_dictionary['nox'],
                                           'so2': organics_emissions_dictionary['so2'],
                                           'pm25': organics_emissions_dictionary['pm25']}}

    electrical_energy_consumption = {'caoh': 0.068, 'fecl3': 0, 'hcl': 0.10, 'nutrients': 0, 'na2co3': 8.5,'gac': 0.58,
                                     'hypochlorite': 0.017, 'inorganics': 0.068, 'organics': 5.4}

    # Now let's create dictionaries for thermal energy consumption.  For this, we assume that all thermal energy is
    # provided via natural gas combustion.
    ng_energy_density = 36.7 # [MJ/m^3] from NREL's LCI database
    ng_combustion_per_m3 = {'co2': 1960.9, 'nox': 1.6, 'so2': 0.0101, 'pm25': 0}  # [g/m^3] from NREL's LCI database
    ng_combustion_per_mj = {'co2': ng_combustion_per_m3['co2'] / ng_energy_density,
                            'nox': ng_combustion_per_m3['nox'] / ng_energy_density,
                            'so2': ng_combustion_per_m3['so2'] / ng_energy_density,
                            'pm25': ng_combustion_per_m3['pm25'] / ng_energy_density}


    def gather_inputs():
        '''This function collects the model inputs and stores them into a dictionary.'''
        basic_info={'system type': system_type.get(), 'system size': float(system_size_input.get()),
                      'inflation year': year_for_inflation.get(), 'vsl': vsl.get(), 'scc': scc.get(),
                     'mc runs': int(model_runs.get())}

        geography_info = {'electricity state': grid_state.get(), 'chemicals state': chem_state.get()}

        if system_type.get() == 'Drinking Water System':
            baseline_treatment_process_info = {'source water': source_water.get(),
                                            'flocculation': flocculation.get(),
                                           'no. of flocculation units': int(flocculation_installed.get()),
                                               'flocculation recovery': float(flocculation_recovery.get()) / 100,
                                           'coagulation': coagulation.get(),
                                           'no. of coagulation units': int(coagulation_installed.get()),
                                               'coagulation recovery': float(coagulation_recovery.get()) / 100,
                                           'sedimentation': sedimentation.get(),
                                           'no. of sedimentation units': int(sedimentation_installed.get()),
                                               'sedimentation recovery': float(sedimentation_recovery.get()) / 100,
                                           'filtration': filtration.get(),
                                           'no. of filtration units': int(filtration_installed.get()),
                                               'filtration recovery': float(filtration_recovery.get()) / 100,
                                           'primary disinfection': primary_disinfection.get(),
                                               'primary disinfection recovery': float(primary_disinfection_recovery.get()) / 100,
                                           'secondary disinfection': secondary_disinfection.get(),
                                               'secondary disinfection recovery': float(secondary_disinfection_recovery.get()) / 100,
                                           'fluoridation': fluoridation.get(),
                                               'fluoridation recovery': float(fluoridation_recovery.get()) / 100,
                                           'softening': softening.get(),
                                               'softening recovery': float(softening_recovery.get()) / 100,
                                           'pH adjustment': ph_adjustment.get(),
                                           'no. of pH adjustment units': int(ph_adjustment_installed.get()),
                                               'pH adjustment recovery': float(ph_adjustment_recovery.get()) / 100,
                                           'gac': granular_activated_carbon.get(),
                                           'no. of gac units': int(granular_activated_carbon_installed.get()),
                                               'gac recovery': float(granular_activated_carbon_recovery.get()) / 100,
                                           'ro': reverse_osmosis.get(),
                                           'no. of ro units': int(reverse_osmosis_installed.get()),
                                               'ro recovery': float(reverse_osmosis_recovery.get()) / 100,
                                           'corrosion control': corrosion_control.get(),
                                               'corrosion control recovery': float(corrosion_control_recovery.get()) / 100,
                                           'aerated grit': FALSE,
                                           'no. of aerated grit units': 0,
                                               'aerated grit recovery': 0,
                                           'grinding': FALSE,
                                               'grinding recovery': 0,
                                           'grit removal': FALSE,
                                           'no. of grit removal units': 0,
                                               'grit removal recovery': 0,
                                           'screening': FALSE,
                                               'screening recovery': 0,
                                           'no. of screening units': 0,
                                           'wastewater sedimentation': FALSE,
                                           'no. of wastewater sedimentation units': 0,
                                               'wastewater sedimentation recovery': 0,
                                           'secondary treatment': FALSE,
                                               'secondary treatment recovery': 0,
                                           'nitrification denitrification': FALSE,
                                           'no. of nitrification denitrification units': 0,
                                               'nitrification denitrification recovery': 0,
                                           'phosphorous removal': FALSE,
                                           'no. of phosphorous removal units': 0,
                                               'phosphorous removal recovery': 0,
                                           'disinfection': FALSE,
                                               'disinfection recovery': 0,
                                           'dechlorination': FALSE,
                                               'dechlorination recovery': 0,
                                           'wastewater ro': FALSE,
                                           'no. of wastewater ro units': 0,
                                               'wastewater ro recovery': 0,
                                           'digestion': FALSE,
                                               'digestion recovery': 0,
                                           'dewatering': FALSE,
                                               'dewatering recovery': 0,
                                           'softening process': FALSE,
                                               'softening process recovery': 0,
                                           'chemical addition input': FALSE,
                                               'chemical addition recovery': 0,
                                           'bio treatment': FALSE,
                                               'bio treatment recovery': 0,
                                           'no. of bio treatment units': 0,
                                           'volume reduction': FALSE,
                                           'no. of volume reduction units': 0,
                                               'volume reduction recovery': 0,
                                           'crystallization': FALSE,
                                               'crystallization recovery': 0,
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
                                           'inorganics dose best input': 0,
                                           'inorganics dose max input': 0}
        elif system_type.get() == 'Municipal Wastewater System':
             baseline_treatment_process_info = {'source water': 'municipal wastewater',
                                           'flocculation': FALSE,
                                           'no. of flocculation units': 0,
                                                'flocculation recovery': 0,
                                           'coagulation': FALSE,
                                           'no. of coagulation units': 0,
                                                'coagulation recovery': 0,
                                           'sedimentation': FALSE,
                                           'no. of sedimentation units': 0,
                                                'sedimentation recovery': 0,
                                           'filtration': FALSE,
                                           'no. of filtration units': 0,
                                                'filtration recovery': 0,
                                           'primary disinfection': FALSE,
                                                'primary disinfection recovery': 0,
                                                'secondary disinfection': FALSE,
                                                'secondary disinfection recovery': 0,
                                           'fluoridation': FALSE,
                                                'fluoridation recovery': 0,
                                           'softening': FALSE,
                                                'softening recovery': 0,
                                           'pH adjustment': FALSE,
                                           'no. of pH adjustment units': FALSE,
                                                'pH adjustment recovery': 0,
                                           'gac': FALSE,
                                           'no. of gac units': 0,
                                                'gac recovery': 0,
                                           'ro': FALSE,
                                           'no. of ro units': 0,
                                                'ro recovery': 0,
                                           'corrosion control': FALSE,
                                                'corrosion control recovery': 0,
                                           'aerated grit': aerated_grit.get(),
                                           'no. of aerated grit units': int(aerated_grit_installed.get()),
                                                'aerated grit recovery': float(aerated_grit_recovery.get())/100,
                                           'grinding': grinding.get(),
                                                'grinding recovery': float(grinding_recovery.get())/100,
                                           'grit removal': grit_removal.get(),
                                           'no. of grit removal units': int(grit_removal_installed.get()),
                                                'grit removal recovery': float(grit_removal_recovery.get())/100,
                                           'screening': screening.get(),
                                           'no. of screening units': int(screening_installed.get()),
                                                'screening recovery': float(screening_recovery.get())/100,
                                           'wastewater sedimentation': wastewater_sedimentation.get(),
                                           'no. of wastewater sedimentation units': int(wastewater_sedimentation_installed.get()),
                                                'wastewater sedimentation recovery': float(wastewater_sedimentation_recovery.get())/100,
                                           'secondary treatment': secondary_treatment.get(),
                                                'secondary treatment recovery': float(secondary_treatment_recovery.get())/100,
                                           'nitrification denitrification': nitrification_denitrification.get(),
                                           'no. of nitrification denitrification units': int(nitrification_denitrification_installed.get()),
                                                'nitrification denitrification recovery': float(nitrification_denitrification_recovery.get())/100,
                                           'phosphorous removal': phosphorous_removal.get(),
                                           'no. of phosphorous removal units': int(phosphorous_removal_installed.get()),
                                                'phosphorous removal recovery': float(phosphorous_removal_recovery.get())/100,
                                           'disinfection': disinfection.get(),
                                                'disinfection recovery': float(disinfection_recovery.get())/100,
                                           'dechlorination': dechlorination.get(),
                                                'dechlorination recovery': float(dechlorination_recovery.get())/100,
                                           'wastewater ro': wastewater_reverse_osmosis.get(),
                                           'no. of wastewater ro units': int(wastewater_reverse_osmosis_installed.get()),
                                                'wastewater ro recovery': float(wastewater_reverse_osmosis_recovery.get())/100,
                                           'digestion': digestion.get(),
                                                'digestion recovery': float(digestion_recovery.get())/100,
                                           'dewatering': dewatering.get(),
                                                'dewatering recovery': float(dewatering_recovery.get())/100,
                                           'softening process': FALSE,
                                                'softening process recovery': 0,
                                           'chemical addition input': FALSE,
                                                'chemical addition recovery': 0,
                                           'bio treatment': FALSE,
                                                'bio treatment recovery': 0,
                                           'no. of bio treatment units': 0,
                                           'volume reduction': FALSE,
                                           'no. of volume reduction units': 0,
                                                'volume reduction recovery': 0,
                                           'crystallization': FALSE,
                                                'crystallization recovery': 0,
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
                                           'inorganics dose best input': 0,
                                           'inorganics dose max input': 0}
        elif system_type.get() == 'Industrial Wastewater System':
             baseline_treatment_process_info = {'source water': 'industrial wastewater',
                                           'flocculation': FALSE,
                                           'no. of flocculation units': 0,
                                                'flocculation recovery': 0,
                                           'coagulation': FALSE,
                                           'no. of coagulation units': 0,
                                                'coagulation recovery': 0,
                                           'sedimentation': FALSE,
                                           'no. of sedimentation units': 0,
                                                'sedimentation recovery': 0,
                                           'filtration': FALSE,
                                           'no. of filtration units': 0,
                                                'filtration recovery': 0,
                                           'primary disinfection': FALSE,
                                                'primary disinfection recovery': 0,
                                           'secondary disinfection': FALSE,
                                                'secondary disinfection recovery': 0,
                                           'fluoridation': FALSE,
                                                'fluoridation recovery': 0,
                                           'softening': FALSE,
                                                'softening recovery': 0,
                                           'pH adjustment': FALSE,
                                           'no. of pH adjustment units': 0,
                                                'pH adjustment recovery': 0,
                                           'gac': FALSE,
                                           'no. of gac units': 0,
                                                'gac recovery': 0,
                                           'ro': FALSE,
                                           'no. of ro units': 0,
                                                'ro recovery': 0,
                                           'corrosion control': FALSE,
                                                'corrosion control recovery': 0,
                                           'aerated grit': FALSE,
                                           'no. of aerated grit units': 0,
                                                'aerated grit recovery': 0,
                                           'grinding': FALSE,
                                                'grinding recovery': 0,
                                           'grit removal': FALSE,
                                           'no. of grit removal units': 0,
                                                'grit removal recovery': 0,
                                           'screening': FALSE,
                                           'no. of screening units': 0,
                                                'screening recovery': 0,
                                           'wastewater sedimentation': FALSE,
                                           'no. of wastewater sedimentation units': 0,
                                                'wastewater sedimentation recovery': 0,
                                           'secondary treatment': FALSE,
                                                'secondary treatment recovery': 0,
                                           'nitrification denitrification': FALSE,
                                           'no. of nitrification denitrification units': 0,
                                                'nitrification denitrification recovery': 0,
                                           'phosphorous removal': FALSE,
                                           'no. of phosphorous removal units': 0,
                                                'phosphorous removal recovery': 0,
                                           'disinfection': FALSE,
                                                'disinfection recovery': 0,
                                           'dechlorination': FALSE,
                                                'dechlorination recovery': 0,
                                           'wastewater ro': FALSE,
                                           'no. of wastewater ro units': 0,
                                                'wastewater ro recovery': 0,
                                           'digestion': FALSE,
                                                'digestion recovery': 0,
                                           'dewatering': FALSE,
                                                'dewatering recovery': 0,
                                           'softening process': softening_process.get(),
                                                'softening process recovery': float(softening_process_recovery.get())/100,
                                           'chemical addition input': chemical_addition_input.get(),
                                                'chemical addition recovery': float(chemical_addition_recovery.get())/100,
                                           'bio treatment': bio_treatment.get(),
                                           'no. of bio treatment units': int(bio_treatment_installed.get()),
                                                'bio treatment recovery': float(bio_treatment_recovery.get())/100,
                                           'volume reduction': volume_reduction.get(),
                                           'no. of volume reduction units': int(volume_reduction_installed.get()),
                                                'volume reduction recovery': float(volume_reduction_recovery.get())/100,
                                           'crystallization': crystallization.get(),
                                                'crystallization recovery': float(crystallization_recovery.get())/100,
                                           'caoh dose min input': float(caoh_dose_min_input.get()),
                                           'caoh dose best input': float(caoh_dose_best_input.get()),
                                           'caoh dose max input': float(caoh_dose_max_input.get()),
                                           'fecl3 dose min input': float(fecl3_dose_min_input.get()),
                                           'fecl3 dose best input': float(fecl3_dose_best_input.get()),
                                           'fecl3 dose max input': float(fecl3_dose_max_input.get()),
                                           'hcl dose min input': float(hcl_dose_min_input.get()),
                                           'hcl dose best input': float(hcl_dose_best_input.get()),
                                           'hcl dose max input': float(hcl_dose_max_input.get()),
                                           'nutrients dose min input': float(nutrients_dose_min_input.get()),
                                           'nutrients dose best input': float(nutrients_dose_best_input.get()),
                                           'nutrients dose max input': float(nutrients_dose_max_input.get()),
                                           'sodium carbonate dose min input': float(sodium_carbonate_dose_min_input.get()),
                                           'sodium carbonate dose best input': float(sodium_carbonate_dose_best_input.get()),
                                           'sodium carbonate dose max input': float(sodium_carbonate_dose_max_input.get()),
                                           'gac dose min input': float(gac_dose_min_input.get()),
                                           'gac dose best input': float(gac_dose_best_input.get()),
                                           'gac dose max input': float(gac_dose_max_input.get()),
                                           'organics dose min input': float(organics_dose_min_input.get()),
                                           'organics dose best input': float(organics_dose_best_input.get()),
                                           'organics dose max input': float(organics_dose_max_input.get()),
                                           'inorganics dose min input': float(inorganics_dose_min_input.get()),
                                           'inorganics dose best input': float(inorganics_dose_best_input.get()),
                                           'inorganics dose max input': float(inorganics_dose_max_input.get())}

        new_process_info = {'new recovery': float(new_recovery_input.get())/100,
                            'new electricity min input': float(new_elec_min_input.get()),
                             'new electricity best input': float(new_elec_best_input.get()),
                             'new electricity max input': float(new_elec_max_input.get()),
                            'new thermal min input': float(new_therm_min_input.get()),
                            'new thermal best input': float(new_therm_best_input.get()),
                            'new thermal max input': float(new_therm_max_input.get()),
                             'new caoh dose min input': float(new_caoh_dose_min_input.get()),
                             'new caoh dose best input': float(new_caoh_dose_best_input.get()),
                             'new caoh dose max input': float(new_caoh_dose_max_input.get()),
                             'new fecl3 dose min input': float(new_fecl3_dose_min_input.get()),
                             'new fecl3 dose best input': float(new_fecl3_dose_best_input.get()),
                             'new fecl3 dose max input': float(new_fecl3_dose_max_input.get()),
                             'new hcl dose min input': float(new_hcl_dose_min_input.get()),
                             'new hcl dose best input': float(new_hcl_dose_best_input.get()),
                             'new hcl dose max input': float(new_hcl_dose_max_input.get()),
                             'new nutrients dose min input': float(new_nutrients_dose_min_input.get()),
                             'new nutrients dose best input': float(new_nutrients_dose_best_input.get()),
                             'new nutrients dose max input': float(new_nutrients_dose_max_input.get()),
                             'new sodium carbonate dose min input': float(new_sodium_carbonate_dose_min_input.get()),
                             'new sodium carbonate dose best input': float(new_sodium_carbonate_dose_best_input.get()),
                             'new sodium carbonate dose max input': float(new_sodium_carbonate_dose_max_input.get()),
                             'new gac dose min input': float(new_gac_dose_min_input.get()),
                             'new gac dose best input': float(new_gac_dose_best_input.get()),
                             'new gac dose max input': float(new_gac_dose_max_input.get()),
                             'new organics dose min input': float(new_organics_dose_min_input.get()),
                             'new organics dose best input': float(new_organics_dose_best_input.get()),
                             'new organics dose max input': float(new_organics_dose_max_input.get()),
                             'new inorganics dose min input': float(new_inorganics_dose_min_input.get()),
                             'new inorganics dose best input': float(new_inorganics_dose_best_input.get()),
                             'new inorganics dose max input': float(new_inorganics_dose_max_input.get())}

        return basic_info, geography_info, baseline_treatment_process_info, new_process_info


    def calculate_results():

        basic_info, geography_info, baseline_treatment_process_info, new_process_info = gather_inputs()

        # Calculate and report electricity consumption.
        electricity_consumption_estimates = calculate_electricity_consumption(basic_info,
                                                                              baseline_treatment_process_info,
                                                                              new_process_info)

        med_elec = round_sig(np.median(electricity_consumption_estimates))
        elec_25 = round_sig(np.percentile(electricity_consumption_estimates, 25))
        elec_75 = round_sig(np.percentile(electricity_consumption_estimates, 75))
        elec_range = str(elec_25) + '-' + str(elec_75)
        Label(tab7, text=med_elec, font=('Arial', 10)).grid(column=1, row=5)
        Label(tab7, text=elec_range, font=('Arial', 10)).grid(column=1, row=6)

        # Calculate and report the electricity emissions.
        co2_electricity_emissions, so2_electricity_emissions, nox_electricity_emissions, \
        pm25_electricity_emissions = electricity_emissions(geography_info, electricity_consumption_estimates,
                                                           state_level_dictionary)

        med_elec_co2 = round_sig(np.median(co2_electricity_emissions))
        elec_co2_25 = round_sig(np.percentile(co2_electricity_emissions, 25))
        elec_co2_75 = round_sig(np.percentile(co2_electricity_emissions, 75))
        elec_co2_range = str(elec_co2_25) + '-' + str(elec_co2_75)
        Label(tab7, text=med_elec_co2, font=('Arial', 10)).grid(column=6, row=5)
        Label(tab7, text=elec_co2_range, font=('Arial', 10)).grid(column=6, row=6)

        med_elec_so2 = round_sig(np.median(so2_electricity_emissions))
        elec_so2_25 = round_sig(np.percentile(so2_electricity_emissions, 25))
        elec_so2_75 = round_sig(np.percentile(so2_electricity_emissions, 75))
        elec_so2_range = str(elec_so2_25) + '-' + str(elec_so2_75)
        Label(tab7, text=med_elec_so2, font=('Arial', 10)).grid(column=4, row=5)
        Label(tab7, text=elec_so2_range, font=('Arial', 10)).grid(column=4, row=6)

        med_elec_nox = round_sig(np.median(nox_electricity_emissions))
        elec_nox_25 = round_sig(np.percentile(nox_electricity_emissions, 25))
        elec_nox_75 = round_sig(np.percentile(nox_electricity_emissions, 75))
        elec_nox_range = str(elec_nox_25) + '-' + str(elec_nox_75)
        Label(tab7, text=med_elec_nox, font=('Arial', 10)).grid(column=3, row=5)
        Label(tab7, text=elec_nox_range, font=('Arial', 10)).grid(column=3, row=6)

        med_elec_pm25 = round_sig(np.median(pm25_electricity_emissions))
        elec_pm25_25 = round_sig(np.percentile(pm25_electricity_emissions, 25))
        elec_pm25_75 = round_sig(np.percentile(pm25_electricity_emissions, 75))
        elec_pm25_range = str(elec_pm25_25) + '-' + str(elec_pm25_75)
        Label(tab7, text=med_elec_pm25, font=('Arial', 10)).grid(column=5, row=5)
        Label(tab7, text=elec_pm25_range, font=('Arial', 10)).grid(column=5, row=6)

        # Calculate and report electrical energy emission damages.

        elec_climate_damages = calculate_climate_damages(co2_electricity_emissions, basic_info)
        med_elec_climate = round_sig(np.median(elec_climate_damages))
        elec_climate_25 = round_sig(np.percentile(elec_climate_damages, 25))
        elec_climate_75 = round_sig(np.percentile(elec_climate_damages, 75))
        elec_climate_range = str(elec_climate_25) + '-' + str(elec_climate_75)
        Label(tab7, text=med_elec_climate, font=('Arial', 10)).grid(column=8, row=5)
        Label(tab7, text=elec_climate_range, font=('Arial', 10)).grid(column=8, row=6)

        #Calculate and report thermal energy consumption

        thermal_consumption_estimates = calculate_thermal_consumption(basic_info, baseline_treatment_process_info,
                                                                      new_process_info)

        med_therm = round_sig(np.median(thermal_consumption_estimates))
        therm_25 = round_sig(np.percentile(thermal_consumption_estimates, 25))
        therm_75 = round_sig(np.percentile(thermal_consumption_estimates, 75))
        therm_range = str(therm_25) + '-' + str(therm_75)
        Label(tab7, text=med_therm, font=('Arial', 10)).grid(column=1, row=7)
        Label(tab7, text=therm_range, font=('Arial', 10)).grid(column=1, row=8)

        co2_thermal_emissions, so2_thermal_emissions, nox_thermal_emissions, pm25_thermal_emissions = \
            thermal_emissions(thermal_consumption_estimates, ng_combustion_per_mj)

        med_therm_co2 = round_sig(np.median(co2_thermal_emissions))
        therm_co2_25 = round_sig(np.percentile(co2_thermal_emissions, 25))
        therm_co2_75 = round_sig(np.percentile(co2_thermal_emissions, 75))
        therm_co2_range = str(therm_co2_25) + '-' + str(therm_co2_75)
        Label(tab7, text=med_therm_co2, font=('Arial', 10)).grid(column=6, row=7)
        Label(tab7, text=therm_co2_range, font=('Arial', 10)).grid(column=6, row=8)

        med_therm_so2 = round_sig(np.median(so2_thermal_emissions))
        therm_so2_25 = round_sig(np.percentile(so2_thermal_emissions, 25))
        therm_so2_75 = round_sig(np.percentile(so2_thermal_emissions, 75))
        therm_so2_range = str(therm_so2_25) + '-' + str(therm_so2_75)
        Label(tab7, text=med_therm_so2, font=('Arial', 10)).grid(column=4, row=7)
        Label(tab7, text=therm_so2_range, font=('Arial', 10)).grid(column=4, row=8)

        med_therm_nox = round_sig(np.median(nox_thermal_emissions))
        therm_nox_25 = round_sig(np.percentile(nox_thermal_emissions, 25))
        therm_nox_75 = round_sig(np.percentile(nox_thermal_emissions, 75))
        therm_nox_range = str(therm_nox_25) + '-' + str(therm_nox_75)
        Label(tab7, text=med_therm_nox, font=('Arial', 10)).grid(column=3, row=7)
        Label(tab7, text=therm_nox_range, font=('Arial', 10)).grid(column=3, row=8)

        med_therm_pm25 = round_sig(np.median(pm25_thermal_emissions))
        therm_pm25_25 = round_sig(np.percentile(pm25_thermal_emissions, 25))
        therm_pm25_75 = round_sig(np.percentile(pm25_thermal_emissions, 75))
        therm_pm25_range = str(therm_pm25_25) + '-' + str(therm_pm25_75)
        Label(tab7, text=med_therm_pm25, font=('Arial', 10)).grid(column=5, row=7)
        Label(tab7, text=therm_pm25_range, font=('Arial', 10)).grid(column=5, row=8)

        # Calculate and report thermal energy emission damages.

        therm_climate_damages = calculate_climate_damages(co2_thermal_emissions, basic_info)
        med_therm_climate = round_sig(np.median(therm_climate_damages))
        therm_climate_25 = round_sig(np.percentile(therm_climate_damages, 25))
        therm_climate_75 = round_sig(np.percentile(therm_climate_damages, 75))
        therm_climate_range = str(therm_climate_25) + '-' + str(therm_climate_75)
        Label(tab7, text=med_therm_climate, font=('Arial', 10)).grid(column=8, row=7)
        Label(tab7, text=therm_climate_range, font=('Arial', 10)).grid(column=8, row=8)

        # Calculate and report the total energy associated emissions.

        med_energy_co2 = round_sig(np.median(co2_thermal_emissions + co2_electricity_emissions))
        energy_co2_25 = round_sig(np.percentile(co2_thermal_emissions + co2_electricity_emissions, 25))
        energy_co2_75 = round_sig(np.percentile(co2_thermal_emissions + co2_electricity_emissions, 75))
        energy_co2_range = str(energy_co2_25) + '-' + str(energy_co2_75)
        Label(tab7, text=med_energy_co2, font=('Arial', 10, 'italic')).grid(column=6, row=3)
        Label(tab7, text=energy_co2_range, font=('Arial', 10, 'italic')).grid(column=6, row=4)

        med_energy_so2 = round_sig(np.median(so2_thermal_emissions + so2_electricity_emissions))
        energy_so2_25 = round_sig(np.percentile(so2_thermal_emissions + so2_electricity_emissions, 25))
        energy_so2_75 = round_sig(np.percentile(so2_thermal_emissions + so2_electricity_emissions, 75))
        energy_so2_range = str(energy_so2_25) + '-' + str(energy_so2_75)
        Label(tab7, text=med_energy_so2, font=('Arial', 10, 'italic')).grid(column=4, row=3)
        Label(tab7, text=energy_so2_range, font=('Arial', 10, 'italic')).grid(column=4, row=4)

        med_energy_nox = round_sig(np.median(nox_thermal_emissions + nox_electricity_emissions))
        energy_nox_25 = round_sig(np.percentile(nox_thermal_emissions + nox_electricity_emissions, 25))
        energy_nox_75 = round_sig(np.percentile(nox_thermal_emissions + nox_electricity_emissions, 75))
        energy_nox_range = str(energy_nox_25) + '-' + str(energy_nox_75)
        Label(tab7, text=med_energy_nox, font=('Arial', 10, 'italic')).grid(column=3, row=3)
        Label(tab7, text=energy_nox_range, font=('Arial', 10, 'italic')).grid(column=3, row=4)

        med_energy_pm25 = round_sig(np.median(pm25_thermal_emissions + pm25_electricity_emissions))
        energy_pm25_25 = round_sig(np.percentile(pm25_thermal_emissions + pm25_electricity_emissions, 25))
        energy_pm25_75 = round_sig(np.percentile(pm25_thermal_emissions + pm25_electricity_emissions, 75))
        energy_pm25_range = str(energy_pm25_25) + '-' + str(energy_pm25_75)
        Label(tab7, text=med_energy_pm25, font=('Arial', 10, 'italic')).grid(column=5, row=3)
        Label(tab7, text=energy_pm25_range, font=('Arial', 10, 'italic')).grid(column=5, row=4)

        # Calculate and report total energy emission damages.

        energy_climate_damages = calculate_climate_damages((co2_thermal_emissions + co2_electricity_emissions),
                                                           basic_info)
        med_energy_climate = round_sig(np.median(energy_climate_damages))
        energy_climate_25 = round_sig(np.percentile(energy_climate_damages, 25))
        energy_climate_75 = round_sig(np.percentile(energy_climate_damages, 75))
        energy_climate_range = str(therm_climate_25) + '-' + str(therm_climate_75)
        Label(tab7, text=med_energy_climate, font=('Arial', 10, 'italic')).grid(column=8, row=3)
        Label(tab7, text=energy_climate_range, font=('Arial', 10, 'italic')).grid(column=8, row=4)


        # Calculate and report chemical consumption.
        total_caoh_consumption, total_fecl3_consumption, total_hcl_consumption, total_nutrients_consumption, \
        total_soda_ash_consumption, total_gac_consumption, total_inorganics_consumption, \
        total_organics_consumption = calculate_chemical_consumption(basic_info, baseline_treatment_process_info,
                                                                    new_process_info)

        caoh_co2_chemical_emissions, caoh_so2_chemical_emissions, caoh_nox_chemical_emissions, \
        caoh_pm25_chemical_emissions, caoh_chem_manufacturing_distribution = chemical_emissions(geography_info, 'caoh',
                                                                                                total_caoh_consumption,
                                                                                                electrical_energy_consumption,
                                                                                                state_level_dictionary,
                                                                                                thermal_chemical_emissions,
                                                                                                direct_chemical_emissions)

        fecl3_co2_chemical_emissions, fecl3_so2_chemical_emissions, fecl3_nox_chemical_emissions, \
        fecl3_pm25_chemical_emissions, fecl3_chem_manufacturing_distribution = chemical_emissions(geography_info, 'fecl3',
                                                                                                total_fecl3_consumption,
                                                                                                electrical_energy_consumption,
                                                                                                state_level_dictionary,
                                                                                                thermal_chemical_emissions,
                                                                                                direct_chemical_emissions)

        hcl_co2_chemical_emissions, hcl_so2_chemical_emissions, hcl_nox_chemical_emissions, \
        hcl_pm25_chemical_emissions, hcl_chem_manufacturing_distribution = chemical_emissions(geography_info, 'hcl',
                                                                                                total_hcl_consumption,
                                                                                                electrical_energy_consumption,
                                                                                                state_level_dictionary,
                                                                                                thermal_chemical_emissions,
                                                                                                direct_chemical_emissions)

        nutrients_co2_chemical_emissions, nutrients_so2_chemical_emissions, nutrients_nox_chemical_emissions, \
        nutrients_pm25_chemical_emissions, nutrients_chem_manufacturing_distribution = chemical_emissions(geography_info, 'nutrients',
                                                                                                total_nutrients_consumption,
                                                                                                electrical_energy_consumption,
                                                                                                state_level_dictionary,
                                                                                                thermal_chemical_emissions,
                                                                                                direct_chemical_emissions)

        soda_ash_co2_chemical_emissions, soda_ash_so2_chemical_emissions, soda_ash_nox_chemical_emissions, \
        soda_ash_pm25_chemical_emissions, soda_ash_chem_manufacturing_distribution = chemical_emissions(geography_info, 'na2co3',
                                                                                                total_soda_ash_consumption,
                                                                                                electrical_energy_consumption,
                                                                                                state_level_dictionary,
                                                                                                thermal_chemical_emissions,
                                                                                                direct_chemical_emissions)

        gac_co2_chemical_emissions, gac_so2_chemical_emissions, gac_nox_chemical_emissions, \
        gac_pm25_chemical_emissions, gac_chem_manufacturing_distribution = chemical_emissions(geography_info, 'gac',
                                                                                                total_gac_consumption,
                                                                                                electrical_energy_consumption,
                                                                                                state_level_dictionary,
                                                                                                thermal_chemical_emissions,
                                                                                                direct_chemical_emissions)

        # hypochlorite_co2_chemical_emissions, hypochlorite_so2_chemical_emissions, hypochlorite_nox_chemical_emissions, \
        # hypochlorite_pm25_chemical_emissions, hypochlorite_chem_manufacturing_distribution = chemical_emissions(geography_info, 'hypochlorite',
        #                                                                                         total_inorganics_consumption,
        #                                                                                         electrical_energy_consumption,
        #                                                                                         state_level_dictionary,
        #                                                                                         thermal_chemical_emissions,
        #                                                                                         direct_chemical_emissions)

        inorganics_co2_chemical_emissions, inorganics_so2_chemical_emissions, inorganics_nox_chemical_emissions, \
        inorganics_pm25_chemical_emissions, inorganics_chem_manufacturing_distribution = chemical_emissions(geography_info, 'inorganics',
                                                                                                total_inorganics_consumption,
                                                                                                electrical_energy_consumption,
                                                                                                state_level_dictionary,
                                                                                                thermal_chemical_emissions,
                                                                                                direct_chemical_emissions)

        organics_co2_chemical_emissions, organics_so2_chemical_emissions, organics_nox_chemical_emissions, \
        organics_pm25_chemical_emissions, organics_chem_manufacturing_distribution = chemical_emissions(geography_info, 'organics',
                                                                                                total_organics_consumption,
                                                                                                electrical_energy_consumption,
                                                                                                state_level_dictionary,
                                                                                                thermal_chemical_emissions,
                                                                                                direct_chemical_emissions)

        co2_chemical_emissions = caoh_co2_chemical_emissions + fecl3_co2_chemical_emissions + \
                                 hcl_co2_chemical_emissions + nutrients_co2_chemical_emissions + \
                                 nutrients_co2_chemical_emissions + soda_ash_co2_chemical_emissions + \
                                 gac_co2_chemical_emissions + inorganics_co2_chemical_emissions + \
                                 organics_co2_chemical_emissions

        so2_chemical_emissions = caoh_so2_chemical_emissions + fecl3_so2_chemical_emissions + \
                                 hcl_so2_chemical_emissions + nutrients_so2_chemical_emissions + \
                                 nutrients_so2_chemical_emissions + soda_ash_so2_chemical_emissions + \
                                 gac_so2_chemical_emissions + inorganics_so2_chemical_emissions + \
                                 organics_so2_chemical_emissions

        nox_chemical_emissions = caoh_nox_chemical_emissions + fecl3_nox_chemical_emissions + \
                                 hcl_nox_chemical_emissions + nutrients_nox_chemical_emissions + \
                                 nutrients_nox_chemical_emissions + soda_ash_nox_chemical_emissions + \
                                 gac_nox_chemical_emissions + inorganics_nox_chemical_emissions + \
                                 organics_nox_chemical_emissions

        pm25_chemical_emissions = caoh_pm25_chemical_emissions + fecl3_pm25_chemical_emissions + \
                                  hcl_pm25_chemical_emissions + nutrients_pm25_chemical_emissions + \
                                  nutrients_co2_chemical_emissions + soda_ash_co2_chemical_emissions + \
                                  gac_pm25_chemical_emissions + inorganics_pm25_chemical_emissions + \
                                  organics_pm25_chemical_emissions

        med_chem_co2 = round_sig(np.median(co2_chemical_emissions))
        chem_co2_25 = round_sig(np.percentile(co2_chemical_emissions, 25))
        chem_co2_75 = round_sig(np.percentile(co2_chemical_emissions, 75))
        chem_co2_range = str(chem_co2_25) + '-' + str(chem_co2_75)
        Label(tab7, text=med_chem_co2, font=('Arial', 10, 'italic')).grid(column=6, row=9)
        Label(tab7, text=chem_co2_range, font=('Arial', 10, 'italic')).grid(column=6, row=10)

        med_chem_so2 = round_sig(np.median(so2_chemical_emissions))
        chem_so2_25 = round_sig(np.percentile(so2_chemical_emissions, 25))
        chem_so2_75 = round_sig(np.percentile(so2_chemical_emissions, 75))
        chem_so2_range = str(chem_so2_25) + '-' + str(chem_so2_75)
        Label(tab7, text=med_chem_so2, font=('Arial', 10, 'italic')).grid(column=4, row=9)
        Label(tab7, text=chem_so2_range, font=('Arial', 10, 'italic')).grid(column=4, row=10)

        med_chem_nox = round_sig(np.median(nox_chemical_emissions))
        chem_nox_25 = round_sig(np.percentile(nox_chemical_emissions, 25))
        chem_nox_75 = round_sig(np.percentile(nox_chemical_emissions, 75))
        chem_nox_range = str(chem_nox_25) + '-' + str(chem_nox_75)
        Label(tab7, text=med_chem_nox, font=('Arial', 10, 'italic')).grid(column=3, row=9)
        Label(tab7, text=chem_nox_range, font=('Arial', 10, 'italic')).grid(column=3, row=10)

        med_chem_pm25 = round_sig(np.median(pm25_chemical_emissions))
        chem_pm25_25 = round_sig(np.percentile(pm25_chemical_emissions, 25))
        chem_pm25_75 = round_sig(np.percentile(pm25_chemical_emissions, 75))
        chem_pm25_range = str(chem_pm25_25) + '-' + str(chem_pm25_75)
        Label(tab7, text=med_chem_pm25, font=('Arial', 10, 'italic')).grid(column=5, row=9)
        Label(tab7, text=chem_pm25_range, font=('Arial', 10, 'italic')).grid(column=5, row=10)

        med_caoh = round_sig(np.median(total_caoh_consumption))
        caoh_25 = round_sig(np.percentile(total_caoh_consumption, 25))
        caoh_75 = round_sig(np.percentile(total_caoh_consumption, 75))
        caoh_range = str(caoh_25) + '-' + str(caoh_75)
        Label(tab7, text=med_caoh, font=('Arial', 10,)).grid(column=1, row=11)
        Label(tab7, text=caoh_range, font=('Arial', 10,)).grid(column=1, row=12)

        med_caoh_co2 = round_sig(np.median(caoh_co2_chemical_emissions))
        caoh_co2_25 = round_sig(np.percentile(caoh_co2_chemical_emissions, 25))
        caoh_co2_75 = round_sig(np.percentile(caoh_co2_chemical_emissions, 75))
        caoh_co2_range = str(caoh_co2_25) + '-' + str(caoh_co2_75)
        Label(tab7, text=med_caoh_co2, font=('Arial', 10)).grid(column=6, row=11)
        Label(tab7, text=caoh_co2_range, font=('Arial', 10)).grid(column=6, row=12)

        med_caoh_so2 = round_sig(np.median(caoh_so2_chemical_emissions))
        caoh_so2_25 = round_sig(np.percentile(caoh_so2_chemical_emissions, 25))
        caoh_so2_75 = round_sig(np.percentile(caoh_so2_chemical_emissions, 75))
        caoh_so2_range = str(caoh_so2_25) + '-' + str(caoh_so2_75)
        Label(tab7, text=med_caoh_so2, font=('Arial', 10)).grid(column=4, row=11)
        Label(tab7, text=caoh_so2_range, font=('Arial', 10)).grid(column=4, row=12)

        med_caoh_nox = round_sig(np.median(caoh_nox_chemical_emissions))
        caoh_nox_25 = round_sig(np.percentile(caoh_nox_chemical_emissions, 25))
        caoh_nox_75 = round_sig(np.percentile(caoh_nox_chemical_emissions, 75))
        caoh_nox_range = str(caoh_nox_25) + '-' + str(caoh_nox_75)
        Label(tab7, text=med_caoh_nox, font=('Arial', 10)).grid(column=3, row=11)
        Label(tab7, text=caoh_nox_range, font=('Arial', 10)).grid(column=3, row=12)

        med_caoh_pm25 = round_sig(np.median(caoh_pm25_chemical_emissions))
        caoh_pm25_25 = round_sig(np.percentile(caoh_pm25_chemical_emissions, 25))
        caoh_pm25_75 = round_sig(np.percentile(caoh_pm25_chemical_emissions, 75))
        caoh_pm25_range = str(caoh_pm25_25) + '-' + str(caoh_pm25_75)
        Label(tab7, text=med_caoh_pm25, font=('Arial', 10)).grid(column=5, row=11)
        Label(tab7, text=caoh_pm25_range, font=('Arial', 10)).grid(column=5, row=12)

        med_fecl3 = round_sig(np.median(total_fecl3_consumption))
        fecl3_25 = round_sig(np.percentile(total_fecl3_consumption, 25))
        fecl3_75 = round_sig(np.percentile(total_fecl3_consumption, 75))
        fecl3_range = str(fecl3_25) + '-' + str(fecl3_75)
        Label(tab7, text=med_fecl3, font=('Arial', 10,)).grid(column=1, row=13)
        Label(tab7, text=fecl3_range, font=('Arial', 10,)).grid(column=1, row=14)

        med_fecl3_co2 = round_sig(np.median(fecl3_co2_chemical_emissions))
        fecl3_co2_25 = round_sig(np.percentile(fecl3_co2_chemical_emissions, 25))
        fecl3_co2_75 = round_sig(np.percentile(fecl3_co2_chemical_emissions, 75))
        fecl3_co2_range = str(fecl3_co2_25) + '-' + str(fecl3_co2_75)
        Label(tab7, text=med_fecl3_co2, font=('Arial', 10)).grid(column=6, row=13)
        Label(tab7, text=fecl3_co2_range, font=('Arial', 10)).grid(column=6, row=14)

        med_fecl3_so2 = round_sig(np.median(fecl3_so2_chemical_emissions))
        fecl3_so2_25 = round_sig(np.percentile(fecl3_so2_chemical_emissions, 25))
        fecl3_so2_75 = round_sig(np.percentile(fecl3_so2_chemical_emissions, 75))
        fecl3_so2_range = str(fecl3_so2_25) + '-' + str(fecl3_so2_75)
        Label(tab7, text=med_fecl3_so2, font=('Arial', 10)).grid(column=4, row=13)
        Label(tab7, text=fecl3_so2_range, font=('Arial', 10)).grid(column=4, row=14)

        med_fecl3_nox = round_sig(np.median(fecl3_nox_chemical_emissions))
        fecl3_nox_25 = round_sig(np.percentile(fecl3_nox_chemical_emissions, 25))
        fecl3_nox_75 = round_sig(np.percentile(fecl3_nox_chemical_emissions, 75))
        fecl3_nox_range = str(fecl3_nox_25) + '-' + str(fecl3_nox_75)
        Label(tab7, text=med_fecl3_nox, font=('Arial', 10)).grid(column=3, row=13)
        Label(tab7, text=fecl3_nox_range, font=('Arial', 10)).grid(column=3, row=14)

        med_fecl3_pm25 = round_sig(np.median(fecl3_pm25_chemical_emissions))
        fecl3_pm25_25 = round_sig(np.percentile(fecl3_pm25_chemical_emissions, 25))
        fecl3_pm25_75 = round_sig(np.percentile(fecl3_pm25_chemical_emissions, 75))
        fecl3_pm25_range = str(fecl3_pm25_25) + '-' + str(fecl3_pm25_75)
        Label(tab7, text=med_fecl3_pm25, font=('Arial', 10)).grid(column=5, row=13)
        Label(tab7, text=fecl3_pm25_range, font=('Arial', 10)).grid(column=5, row=14)

        med_hcl = round_sig(np.median(total_hcl_consumption))
        hcl_25 = round_sig(np.percentile(total_hcl_consumption, 25))
        hcl_75 = round_sig(np.percentile(total_hcl_consumption, 75))
        hcl_range = str(hcl_25) + '-' + str(hcl_75)
        Label(tab7, text=med_hcl, font=('Arial', 10,)).grid(column=1, row=15)
        Label(tab7, text=hcl_range, font=('Arial', 10,)).grid(column=1, row=16)

        med_hcl_co2 = round_sig(np.median(hcl_co2_chemical_emissions))
        hcl_co2_25 = round_sig(np.percentile(hcl_co2_chemical_emissions, 25))
        hcl_co2_75 = round_sig(np.percentile(hcl_co2_chemical_emissions, 75))
        hcl_co2_range = str(hcl_co2_25) + '-' + str(hcl_co2_75)
        Label(tab7, text=med_hcl_co2, font=('Arial', 10)).grid(column=6, row=15)
        Label(tab7, text=hcl_co2_range, font=('Arial', 10)).grid(column=6, row=16)

        med_hcl_so2 = round_sig(np.median(hcl_so2_chemical_emissions))
        hcl_so2_25 = round_sig(np.percentile(hcl_so2_chemical_emissions, 25))
        hcl_so2_75 = round_sig(np.percentile(hcl_so2_chemical_emissions, 75))
        hcl_so2_range = str(hcl_so2_25) + '-' + str(hcl_so2_75)
        Label(tab7, text=med_hcl_so2, font=('Arial', 10)).grid(column=4, row=15)
        Label(tab7, text=hcl_so2_range, font=('Arial', 10)).grid(column=4, row=16)

        med_hcl_nox = round_sig(np.median(hcl_nox_chemical_emissions))
        hcl_nox_25 = round_sig(np.percentile(hcl_nox_chemical_emissions, 25))
        hcl_nox_75 = round_sig(np.percentile(hcl_nox_chemical_emissions, 75))
        hcl_nox_range = str(hcl_nox_25) + '-' + str(hcl_nox_75)
        Label(tab7, text=med_hcl_nox, font=('Arial', 10)).grid(column=3, row=15)
        Label(tab7, text=hcl_nox_range, font=('Arial', 10)).grid(column=3, row=16)

        med_hcl_pm25 = round_sig(np.median(hcl_pm25_chemical_emissions))
        hcl_pm25_25 = round_sig(np.percentile(hcl_pm25_chemical_emissions, 25))
        hcl_pm25_75 = round_sig(np.percentile(hcl_pm25_chemical_emissions, 75))
        hcl_pm25_range = str(hcl_pm25_25) + '-' + str(hcl_pm25_75)
        Label(tab7, text=med_hcl_pm25, font=('Arial', 10)).grid(column=5, row=15)
        Label(tab7, text=hcl_pm25_range, font=('Arial', 10)).grid(column=5, row=16)

        med_nutrients = round_sig(np.median(total_nutrients_consumption))
        nutrients_25 = round_sig(np.percentile(total_nutrients_consumption, 25))
        nutrients_75 = round_sig(np.percentile(total_nutrients_consumption, 75))
        nutrients_range = str(nutrients_25) + '-' + str(nutrients_75)
        Label(tab7, text=med_nutrients, font=('Arial', 10,)).grid(column=1, row=17)
        Label(tab7, text=nutrients_range, font=('Arial', 10,)).grid(column=1, row=18)

        med_nutrients_co2 = round_sig(np.median(nutrients_co2_chemical_emissions))
        nutrients_co2_25 = round_sig(np.percentile(nutrients_co2_chemical_emissions, 25))
        nutrients_co2_75 = round_sig(np.percentile(nutrients_co2_chemical_emissions, 75))
        nutrients_co2_range = str(nutrients_co2_25) + '-' + str(nutrients_co2_75)
        Label(tab7, text=med_nutrients_co2, font=('Arial', 10)).grid(column=6, row=17)
        Label(tab7, text=nutrients_co2_range, font=('Arial', 10)).grid(column=6, row=18)

        med_nutrients_so2 = round_sig(np.median(nutrients_so2_chemical_emissions))
        nutrients_so2_25 = round_sig(np.percentile(nutrients_so2_chemical_emissions, 25))
        nutrients_so2_75 = round_sig(np.percentile(nutrients_so2_chemical_emissions, 75))
        nutrients_so2_range = str(nutrients_so2_25) + '-' + str(nutrients_so2_75)
        Label(tab7, text=med_nutrients_so2, font=('Arial', 10)).grid(column=4, row=17)
        Label(tab7, text=nutrients_so2_range, font=('Arial', 10)).grid(column=4, row=18)

        med_nutrients_nox = round_sig(np.median(nutrients_nox_chemical_emissions))
        nutrients_nox_25 = round_sig(np.percentile(nutrients_nox_chemical_emissions, 25))
        nutrients_nox_75 = round_sig(np.percentile(nutrients_nox_chemical_emissions, 75))
        nutrients_nox_range = str(nutrients_nox_25) + '-' + str(nutrients_nox_75)
        Label(tab7, text=med_nutrients_nox, font=('Arial', 10)).grid(column=3, row=17)
        Label(tab7, text=nutrients_nox_range, font=('Arial', 10)).grid(column=3, row=18)

        med_nutrients_pm25 = round_sig(np.median(nutrients_pm25_chemical_emissions))
        nutrients_pm25_25 = round_sig(np.percentile(nutrients_pm25_chemical_emissions, 25))
        nutrients_pm25_75 = round_sig(np.percentile(nutrients_pm25_chemical_emissions, 75))
        nutrients_pm25_range = str(nutrients_pm25_25) + '-' + str(nutrients_pm25_75)
        Label(tab7, text=med_nutrients_pm25, font=('Arial', 10)).grid(column=5, row=17)
        Label(tab7, text=nutrients_pm25_range, font=('Arial', 10)).grid(column=5, row=18)

        med_soda_ash = round_sig(np.median(total_soda_ash_consumption))
        soda_ash_25 = round_sig(np.percentile(total_soda_ash_consumption, 25))
        soda_ash_75 = round_sig(np.percentile(total_soda_ash_consumption, 75))
        soda_ash_range = str(soda_ash_25) + '-' + str(soda_ash_75)
        Label(tab7, text=med_soda_ash, font=('Arial', 10,)).grid(column=1, row=19)
        Label(tab7, text=soda_ash_range, font=('Arial', 10,)).grid(column=1, row=20)

        med_soda_ash_co2 = round_sig(np.median(soda_ash_co2_chemical_emissions))
        soda_ash_co2_25 = round_sig(np.percentile(soda_ash_co2_chemical_emissions, 25))
        soda_ash_co2_75 = round_sig(np.percentile(soda_ash_co2_chemical_emissions, 75))
        soda_ash_co2_range = str(soda_ash_co2_25) + '-' + str(soda_ash_co2_75)
        Label(tab7, text=med_soda_ash_co2, font=('Arial', 10)).grid(column=6, row=19)
        Label(tab7, text=soda_ash_co2_range, font=('Arial', 10)).grid(column=6, row=20)

        med_soda_ash_so2 = round_sig(np.median(soda_ash_so2_chemical_emissions))
        soda_ash_so2_25 = round_sig(np.percentile(soda_ash_so2_chemical_emissions, 25))
        soda_ash_so2_75 = round_sig(np.percentile(soda_ash_so2_chemical_emissions, 75))
        soda_ash_so2_range = str(soda_ash_so2_25) + '-' + str(soda_ash_so2_75)
        Label(tab7, text=med_soda_ash_so2, font=('Arial', 10)).grid(column=4, row=19)
        Label(tab7, text=soda_ash_so2_range, font=('Arial', 10)).grid(column=4, row=20)

        med_soda_ash_nox = round_sig(np.median(soda_ash_nox_chemical_emissions))
        soda_ash_nox_25 = round_sig(np.percentile(soda_ash_nox_chemical_emissions, 25))
        soda_ash_nox_75 = round_sig(np.percentile(soda_ash_nox_chemical_emissions, 75))
        soda_ash_nox_range = str(soda_ash_nox_25) + '-' + str(soda_ash_nox_75)
        Label(tab7, text=med_soda_ash_nox, font=('Arial', 10)).grid(column=3, row=19)
        Label(tab7, text=soda_ash_nox_range, font=('Arial', 10)).grid(column=3, row=20)

        med_soda_ash_pm25 = round_sig(np.median(soda_ash_pm25_chemical_emissions))
        soda_ash_pm25_25 = round_sig(np.percentile(soda_ash_pm25_chemical_emissions, 25))
        soda_ash_pm25_75 = round_sig(np.percentile(soda_ash_pm25_chemical_emissions, 75))
        soda_ash_pm25_range = str(soda_ash_pm25_25) + '-' + str(soda_ash_pm25_75)
        Label(tab7, text=med_soda_ash_pm25, font=('Arial', 10)).grid(column=5, row=19)
        Label(tab7, text=soda_ash_pm25_range, font=('Arial', 10)).grid(column=5, row=20)

        med_gac = round_sig(np.median(total_gac_consumption))
        gac_25 = round_sig(np.percentile(total_gac_consumption, 25))
        gac_75 = round_sig(np.percentile(total_gac_consumption, 75))
        gac_range = str(gac_25) + '-' + str(gac_75)
        Label(tab7, text=med_gac, font=('Arial', 10,)).grid(column=1, row=21)
        Label(tab7, text=gac_range, font=('Arial', 10,)).grid(column=1, row=22)

        med_gac_co2 = round_sig(np.median(gac_co2_chemical_emissions))
        gac_co2_25 = round_sig(np.percentile(gac_co2_chemical_emissions, 25))
        gac_co2_75 = round_sig(np.percentile(gac_co2_chemical_emissions, 75))
        gac_co2_range = str(gac_co2_25) + '-' + str(gac_co2_75)
        Label(tab7, text=med_gac_co2, font=('Arial', 10)).grid(column=6, row=21)
        Label(tab7, text=gac_co2_range, font=('Arial', 10)).grid(column=6, row=22)

        med_gac_so2 = round_sig(np.median(gac_so2_chemical_emissions))
        gac_so2_25 = round_sig(np.percentile(gac_so2_chemical_emissions, 25))
        gac_so2_75 = round_sig(np.percentile(gac_so2_chemical_emissions, 75))
        gac_so2_range = str(gac_so2_25) + '-' + str(gac_so2_75)
        Label(tab7, text=med_gac_so2, font=('Arial', 10)).grid(column=4, row=21)
        Label(tab7, text=gac_so2_range, font=('Arial', 10)).grid(column=4, row=22)

        med_gac_nox = round_sig(np.median(gac_nox_chemical_emissions))
        gac_nox_25 = round_sig(np.percentile(gac_nox_chemical_emissions, 25))
        gac_nox_75 = round_sig(np.percentile(gac_nox_chemical_emissions, 75))
        gac_nox_range = str(gac_nox_25) + '-' + str(gac_nox_75)
        Label(tab7, text=med_gac_nox, font=('Arial', 10)).grid(column=3, row=21)
        Label(tab7, text=gac_nox_range, font=('Arial', 10)).grid(column=3, row=22)

        med_gac_pm25 = round_sig(np.median(gac_pm25_chemical_emissions))
        gac_pm25_25 = round_sig(np.percentile(gac_pm25_chemical_emissions, 25))
        gac_pm25_75 = round_sig(np.percentile(gac_pm25_chemical_emissions, 75))
        gac_pm25_range = str(gac_pm25_25) + '-' + str(gac_pm25_75)
        Label(tab7, text=med_gac_pm25, font=('Arial', 10)).grid(column=5, row=21)
        Label(tab7, text=gac_pm25_range, font=('Arial', 10)).grid(column=5, row=22)

        med_inorganics = round_sig(np.median(total_inorganics_consumption))
        inorganics_25 = round_sig(np.percentile(total_inorganics_consumption, 25))
        inorganics_75 = round_sig(np.percentile(total_inorganics_consumption, 75))
        inorganics_range = str(inorganics_25) + '-' + str(inorganics_75)
        Label(tab7, text=med_inorganics, font=('Arial', 10,)).grid(column=1, row=23)
        Label(tab7, text=inorganics_range, font=('Arial', 10,)).grid(column=1, row=24)

        med_inorganics_co2 = round_sig(np.median(inorganics_co2_chemical_emissions))
        inorganics_co2_25 = round_sig(np.percentile(inorganics_co2_chemical_emissions, 25))
        inorganics_co2_75 = round_sig(np.percentile(inorganics_co2_chemical_emissions, 75))
        inorganics_co2_range = str(inorganics_co2_25) + '-' + str(inorganics_co2_75)
        Label(tab7, text=med_inorganics_co2, font=('Arial', 10)).grid(column=6, row=23)
        Label(tab7, text=inorganics_co2_range, font=('Arial', 10)).grid(column=6, row=24)

        med_inorganics_so2 = round_sig(np.median(inorganics_so2_chemical_emissions))
        inorganics_so2_25 = round_sig(np.percentile(inorganics_so2_chemical_emissions, 25))
        inorganics_so2_75 = round_sig(np.percentile(inorganics_so2_chemical_emissions, 75))
        inorganics_so2_range = str(inorganics_so2_25) + '-' + str(inorganics_so2_75)
        Label(tab7, text=med_inorganics_so2, font=('Arial', 10)).grid(column=4, row=23)
        Label(tab7, text=inorganics_so2_range, font=('Arial', 10)).grid(column=4, row=24)

        med_inorganics_nox = round_sig(np.median(inorganics_nox_chemical_emissions))
        inorganics_nox_25 = round_sig(np.percentile(inorganics_nox_chemical_emissions, 25))
        inorganics_nox_75 = round_sig(np.percentile(inorganics_nox_chemical_emissions, 75))
        inorganics_nox_range = str(inorganics_nox_25) + '-' + str(inorganics_nox_75)
        Label(tab7, text=med_inorganics_nox, font=('Arial', 10)).grid(column=3, row=23)
        Label(tab7, text=inorganics_nox_range, font=('Arial', 10)).grid(column=3, row=24)

        med_inorganics_pm25 = round_sig(np.median(inorganics_pm25_chemical_emissions))
        inorganics_pm25_25 = round_sig(np.percentile(inorganics_pm25_chemical_emissions, 25))
        inorganics_pm25_75 = round_sig(np.percentile(inorganics_pm25_chemical_emissions, 75))
        inorganics_pm25_range = str(inorganics_pm25_25) + '-' + str(inorganics_pm25_75)
        Label(tab7, text=med_inorganics_pm25, font=('Arial', 10)).grid(column=5, row=23)
        Label(tab7, text=inorganics_pm25_range, font=('Arial', 10)).grid(column=5, row=24)

        med_organics = round_sig(np.median(total_organics_consumption))
        organics_25 = round_sig(np.percentile(total_organics_consumption, 25))
        organics_75 = round_sig(np.percentile(total_organics_consumption, 75))
        organics_range = str(organics_25) + '-' + str(organics_75)
        Label(tab7, text=med_organics, font=('Arial', 10,)).grid(column=1, row=25)
        Label(tab7, text=organics_range, font=('Arial', 10,)).grid(column=1, row=26)

        med_organics_co2 = round_sig(np.median(organics_co2_chemical_emissions))
        organics_co2_25 = round_sig(np.percentile(organics_co2_chemical_emissions, 25))
        organics_co2_75 = round_sig(np.percentile(organics_co2_chemical_emissions, 75))
        organics_co2_range = str(organics_co2_25) + '-' + str(organics_co2_75)
        Label(tab7, text=med_organics_co2, font=('Arial', 10)).grid(column=6, row=25)
        Label(tab7, text=organics_co2_range, font=('Arial', 10)).grid(column=6, row=26)

        med_organics_so2 = round_sig(np.median(organics_so2_chemical_emissions))
        organics_so2_25 = round_sig(np.percentile(organics_so2_chemical_emissions, 25))
        organics_so2_75 = round_sig(np.percentile(organics_so2_chemical_emissions, 75))
        organics_so2_range = str(organics_so2_25) + '-' + str(organics_so2_75)
        Label(tab7, text=med_organics_so2, font=('Arial', 10)).grid(column=4, row=25)
        Label(tab7, text=organics_so2_range, font=('Arial', 10)).grid(column=4, row=26)

        med_organics_nox = round_sig(np.median(organics_nox_chemical_emissions))
        organics_nox_25 = round_sig(np.percentile(organics_nox_chemical_emissions, 25))
        organics_nox_75 = round_sig(np.percentile(organics_nox_chemical_emissions, 75))
        organics_nox_range = str(organics_nox_25) + '-' + str(organics_nox_75)
        Label(tab7, text=med_organics_nox, font=('Arial', 10)).grid(column=3, row=25)
        Label(tab7, text=organics_nox_range, font=('Arial', 10)).grid(column=3, row=26)

        med_organics_pm25 = round_sig(np.median(organics_pm25_chemical_emissions))
        organics_pm25_25 = round_sig(np.percentile(organics_pm25_chemical_emissions, 25))
        organics_pm25_75 = round_sig(np.percentile(organics_pm25_chemical_emissions, 75))
        organics_pm25_range = str(organics_pm25_25) + '-' + str(organics_pm25_75)
        Label(tab7, text=med_organics_pm25, font=('Arial', 10)).grid(column=5, row=25)
        Label(tab7, text=organics_pm25_range, font=('Arial', 10)).grid(column=5, row=26)

    # Calculate and report the damages resulting from chemical manufacturing emissions.

        chem_climate_damages = calculate_climate_damages(co2_chemical_emissions, basic_info)
        med_chem_climate = round_sig(np.median(chem_climate_damages))
        chem_climate_25 = round_sig(np.percentile(chem_climate_damages, 25))
        chem_climate_75 = round_sig(np.percentile(chem_climate_damages, 75))
        chem_climate_range = str(chem_climate_25) + '-' + str(chem_climate_75)
        Label(tab7, text=med_chem_climate, font=('Arial', 10, 'italic')).grid(column=8, row=9)
        Label(tab7, text=chem_climate_range, font=('Arial', 10, 'italic')).grid(column=8, row=10)

        caoh_climate_damages = calculate_climate_damages(caoh_co2_chemical_emissions, basic_info)
        med_caoh_climate = round_sig(np.median(caoh_climate_damages))
        caoh_climate_25 = round_sig(np.percentile(caoh_climate_damages, 25))
        caoh_climate_75 = round_sig(np.percentile(caoh_climate_damages, 75))
        caoh_climate_range = str(caoh_climate_25) + '-' + str(caoh_climate_75)
        Label(tab7, text=med_caoh_climate, font=('Arial', 10)).grid(column=8, row=11)
        Label(tab7, text=caoh_climate_range, font=('Arial', 10)).grid(column=8, row=12)

        fecl3_climate_damages = calculate_climate_damages(fecl3_co2_chemical_emissions, basic_info)
        med_fecl3_climate = round_sig(np.median(fecl3_climate_damages))
        fecl3_climate_25 = round_sig(np.percentile(fecl3_climate_damages, 25))
        fecl3_climate_75 = round_sig(np.percentile(fecl3_climate_damages, 75))
        fecl3_climate_range = str(fecl3_climate_25) + '-' + str(fecl3_climate_75)
        Label(tab7, text=med_fecl3_climate, font=('Arial', 10)).grid(column=8, row=13)
        Label(tab7, text=fecl3_climate_range, font=('Arial', 10)).grid(column=8, row=14)

        hcl_climate_damages = calculate_climate_damages(hcl_co2_chemical_emissions, basic_info)
        med_hcl_climate = round_sig(np.median(hcl_climate_damages))
        hcl_climate_25 = round_sig(np.percentile(hcl_climate_damages, 25))
        hcl_climate_75 = round_sig(np.percentile(hcl_climate_damages, 75))
        hcl_climate_range = str(hcl_climate_25) + '-' + str(hcl_climate_75)
        Label(tab7, text=med_hcl_climate, font=('Arial', 10)).grid(column=8, row=15)
        Label(tab7, text=hcl_climate_range, font=('Arial', 10)).grid(column=8, row=16)

        nutrients_climate_damages = calculate_climate_damages(nutrients_co2_chemical_emissions, basic_info)
        med_nutrients_climate = round_sig(np.median(nutrients_climate_damages))
        nutrients_climate_25 = round_sig(np.percentile(nutrients_climate_damages, 25))
        nutrients_climate_75 = round_sig(np.percentile(nutrients_climate_damages, 75))
        nutrients_climate_range = str(nutrients_climate_25) + '-' + str(nutrients_climate_75)
        Label(tab7, text=med_nutrients_climate, font=('Arial', 10)).grid(column=8, row=17)
        Label(tab7, text=nutrients_climate_range, font=('Arial', 10)).grid(column=8, row=18)

        soda_ash_climate_damages = calculate_climate_damages(soda_ash_co2_chemical_emissions, basic_info)
        med_soda_ash_climate = round_sig(np.median(soda_ash_climate_damages))
        soda_ash_climate_25 = round_sig(np.percentile(soda_ash_climate_damages, 25))
        soda_ash_climate_75 = round_sig(np.percentile(soda_ash_climate_damages, 75))
        soda_ash_climate_range = str(soda_ash_climate_25) + '-' + str(soda_ash_climate_75)
        Label(tab7, text=med_soda_ash_climate, font=('Arial', 10)).grid(column=8, row=19)
        Label(tab7, text=soda_ash_climate_range, font=('Arial', 10)).grid(column=8, row=20)

        gac_climate_damages = calculate_climate_damages(gac_co2_chemical_emissions, basic_info)
        med_gac_climate = round_sig(np.median(gac_climate_damages))
        gac_climate_25 = round_sig(np.percentile(gac_climate_damages, 25))
        gac_climate_75 = round_sig(np.percentile(gac_climate_damages, 75))
        gac_climate_range = str(gac_climate_25) + '-' + str(gac_climate_75)
        Label(tab7, text=med_gac_climate, font=('Arial', 10)).grid(column=8, row=21)
        Label(tab7, text=gac_climate_range, font=('Arial', 10)).grid(column=8, row=22)

        inorganics_climate_damages = calculate_climate_damages(inorganics_co2_chemical_emissions, basic_info)
        med_inorganics_climate = round_sig(np.median(inorganics_climate_damages))
        inorganics_climate_25 = round_sig(np.percentile(inorganics_climate_damages, 25))
        inorganics_climate_75 = round_sig(np.percentile(inorganics_climate_damages, 75))
        inorganics_climate_range = str(inorganics_climate_25) + '-' + str(inorganics_climate_75)
        Label(tab7, text=med_inorganics_climate, font=('Arial', 10)).grid(column=8, row=23)
        Label(tab7, text=inorganics_climate_range, font=('Arial', 10)).grid(column=8, row=24)

        organics_climate_damages = calculate_climate_damages(organics_co2_chemical_emissions, basic_info)
        med_organics_climate = round_sig(np.median(organics_climate_damages))
        organics_climate_25 = round_sig(np.percentile(organics_climate_damages, 25))
        organics_climate_75 = round_sig(np.percentile(organics_climate_damages, 75))
        organics_climate_range = str(organics_climate_25) + '-' + str(organics_climate_75)
        Label(tab7, text=med_organics_climate, font=('Arial', 10)).grid(column=8, row=25)
        Label(tab7, text=organics_climate_range, font=('Arial', 10)).grid(column=8, row=26)

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
