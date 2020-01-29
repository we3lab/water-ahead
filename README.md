# Water Associated Health and Environmental Air Damages Tool
The Water *A*ssociated *H*ealth and *E*nvironmental *A*ir *D*amages Tool is a model to predict the emissions and damages associated with treating drinking water, municipal wastewater, and industrial wastewater.  We include the following emissions:
<ul>
  <li> Criteria Air Pollutants </li>
    <ul>
      <li> NO<sub>x</sub> </li>
      <li> SO<sub>2</sub> </li>
      <li> PM<sub>2.5</sub> </li>
  </ul>
  <li> Greenhouse Gas Emissions </li>
    <ul>
      <li> CO<sub>2</sub> </li>
  </ul>
</ul>
  
A user can specify the type of a treatment plant, the plant's capacity, the geography of the plant and where it sources its chemicals from, and the processes installed.  In addition to specifying what processes the plant has installed, the user can also specify how many of a given unit are installed and what the recovery is for these processes.  The model then outputs an inventory of the energy (thermal and electrical) and chemicals consumed; the emissions associated with with these energy and chemical inputs; and the health, environmental, and climate damages associated with those emissions.  For more information on the tool (including a list of the papers underlying the life cycle inventories) and how to use the GUI, please see the <a href="https://osf.io/p28ax/"> Open Science Foundation project </a>. 

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Creating an instance of the GUI using Python
<b>You will need to download the data files separately.  They are located at <a href="https://osf.io/p28ax/files/"> Open Science Foundation project Files </a>.  Once you have downloaded them you will need to place the Data folder at the same level in your directory as the Code folder. </b>

To create the GUI using Python, run the water_ahead_GUI.py file located in the Code/GUI directory.

### Installing the GUI 
We are currently in the process of developing a installer for the Graphical User Interface.  Stay tuned for updates on when the Installer will be available for download!

## Contributing
Please read <a href="https://github.com/we3lab/water-ahead/blob/master/CONTRIBUTING.md"> CONTRIBUTING.md </a> for details of our code of conduct, and the process for submitting pull requests to us.

### Reporting a Bug
To report a bug, create an issue in the GitHub Repository.  Please use the <a href="https://github.com/we3lab/water-ahead/issues/new?assignees=&labels=&template=bug_report.md&title="> Bug Report template </a>.

### Requesting a Feature
To requiest a feature, create an issue in the GitHub Repository.  Please use the <a href="https://github.com/we3lab/water-ahead/issues/new?assignees=&labels=&template=feature_request.md&title="> Feature Request template </a>.

## Authors
<ul> 
  <li> Daniel Gingerich, Stanford University, (Current Location The Ohio State University), gingerich.62@osu.edu </li>
  </ul>

## Citation
To cite the Water AHEAD Tool, use the following citation:


## License
This project is licensed under the GNU General Public License v. 3.0 - see the <a href="https://github.com/we3lab/water-ahead/blob/master/LICENSE"> LICENSE </a> file for details.

## Acknowledgements
The development of the tool was supervised and funding was secured by Professor Meagan S. Mauter.  

In adition, we would like to thank the following funding sources:  
<ul>
  <li> U.S. National Science Foundation under contract SEES-1215845 and CBET-1554117 </li>
  <li> The Pittsburgh Chapter of the ARCS (Achievement Rewards for College Scientists) Foundation
