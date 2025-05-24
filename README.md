# eufyformatter
Python scripts to convert EufyLife scale data exports to FIT files that Garmin connect can import.

Although the script works on EufyLife scale csv data by default, csv exports from other systems
should work if the column headings on the csv file are changed appropriately

## Installing 

The easiest way to use this conversion script is to install [uv](https://github.com/astral-sh/uv) and 
use`uv run` to create a temporary environment with the required libraries. Alternatively
you can install the dependencies from the pyproject.toml and run the script directly.

## Running in batch mode

Use the `batch` argument to run the `convert_eufy.py` script in batch mode.  The 
arguments used are listed below:

| Argument | Example |                    Notes                    |
|:--------:| :---: |:-------------------------------------------:|
| filename | eufy_export.csv |     CSV file to process (**Required**)      |
| output | garmin.fit | Name of fit file to write to (**Required**) |
| start | 2025-05-01 |   Start of date range to export data from   |
| end | 2025-05-10 | End of date range to export data from |

If `start` and `end` arguments are not given all data in the csv file will
be exported.

## Running interactively

Use the `interactive` argument to run the `convert_eufy.py` script in interactive mode.  The 
arguments used are listed below:

| Argument | Example |                    Notes                    |
|:--------:| :---: |:-------------------------------------------:|
| filename | eufy_export.csv |     CSV file to process (**Required**)      |
| output | garmin.fit | Name of fit file to write to (**Required**) |

Once the script starts running, you can select columns to export and the 
date range from the file to export.

## Conversion details
The mapping between EufyLife csv data and FIT fields are as follows

|      CSV Column Name       |     FIT field     |                           Notes                            | 
|:--------------------------:|:-----------------:|:----------------------------------------------------------:|
|            Time            |     timestamp     |        date and time in YYYY-MM-DD HH:MM:SS format         |
|       Family Members       |      Ignored      |                                                            |
|        WEIGHT (kg)         |      weight       |                        Weight in kg                        |
|        WEIGHT (lbs)        |      weight       |        Weight in lbs -- converted to kg internally         |
|            BMI             |        bmi        |                      Body Mass Index                       |
|         BODY FAT %         |    percent_fat    |                    Body Fat percentage                     | 
|      HEART RATE (bpm)      |      Ignored      |                                                            |
|      MUSCLE MASS (kg)      |    muscle_mass    |                     Muscle mass in kg                      |
|     MUSCLE MASS (lbs)      |    muscle_mass    |      Muscle mass in lb  -- converted to kg internally      |
|       MUSCLE MASS %        |      Ignored      |                                                            |
|            BMR             |     basal_met     |                    Basal metabolic rate                    | 
|           WATER            | percent_hydration |             Percentage of body mass from water             |
|     BODY FAT MASS (kg)     |      Ignored      |                                                            |
|    BODY FAT MASS (lbs)     |      Ignored      |                                                            |
|    LEAN BODY MASS (kg)     |      Ignored      |                                                            |
|    LEAN BODY MASS (lbs)    |      Ignored      |                                                            |
|       BONE MASS (kg)       |     bone_mass     |                Mass of bones in body in kg                 |
|      BONE MASS (lbs)       |     bone_mass     | Mass of bones in body in lb  -- converted to kg internally |
|        BONE MASS %         |      Ignored      |                                                            |
|        VISCERAL FAT        | visceral_fat_mass |                     Not used by Garmin                     |
|         PROTEIN %          |      Ignored      |                                                            |
| SKELETAL MUSCLE MASS (kg)  |      Ignored      |                                                            |
| SKELETAL MUSCLE MASS (lbs) |      Ignored      |                                                            |
|     SUBCUTANEOUS FAT %     |      Ignored      |                                                            |
|          BODY AGE          |   metabolic_age   |                       Metabolic Age                        |
|         BODY TYPE          |      Ignored      |                                                            |
|       HEAD SIZE (cm)       |      Ignored      |                                                            |


