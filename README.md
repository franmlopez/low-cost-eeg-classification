
# Low Cost EEG Emotions Classification

The project uses a live EEG from the user to control a simplified keyboard using steady state visually evoked potentials.

On start-up, the user should stare at one of the checker boxes to record a baseline EEG. Once the checkerboxes start flashing, the user can start making selections. There are five flashing checkerboxes, each flashing at a different frequency. Each box also has some comma separated options above them, which can be selected
By the user looking and concentrating on it. The box will be highlighted and the options sub-divided between the checker boxes. This repeats until a single option is selected. If the option is a letter/number it will be displayed in the text box.

## Getting Started

1. Build the circuit as shown in the circuit schematic
2. Import and build the Nucleo code to whichever ARM compatible IDE you wish. I used SW4STM32.
3. Flash it to the Nucleo

1. Run eegBCI.py, you may need to change the serial port in this file.
2. See that the EEGScope window is receiving data. 
3. If it is, you can close the windows and connect up the electrodes.


### Prerequisites

The BCI uses Python3 and all of the dependencies are listed in requirments.txt in the BCI folder. 
Run "pip install -r requirements.txt" within the folder

Nucleo code was created with STM32CubeMX and edited in SW4STM32 but can be imported into other ARM based IDE

## Contributing

## Authors

* **Rodrigo Sanz** - *Initial work* - [rodrigosanzlongone](https://github.com/rodrigosanzlongone) - [Site](https://rodrigosanz.com/)
* **Francisco López-Guzmán** - *Initial work* - [XXX](https://github.com/) - 

## License

This project is licensed under the Apache 2 License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgements

* [Tim](https:///) for supervising the project and providing endless help and ideas

## Disclaimer
The designs for the EEG hardware and software shown in this repository have not been tested to comply with any medical device standards such as IEC 601. Therefore, any user which builds or uses the designs from this repository does so at their own risk. 

As of writing, the BCI designs in this repository are not very reliable so the software/hardware should not be modified to control dangerous machinery or provide a valid means of communication.
