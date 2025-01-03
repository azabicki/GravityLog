# OnTheScales

This Streamlit application serves as a tool for tracking and managing body measurements over time. It enables users to record, visualize, and analyze weight and body composition metrics: weight along with body fat, water content, and muscle mass. _OnTheScales_ is designed for individuals who want to monitor their body composition changes, whether for fitness goals, health monitoring, or weight management. While being comprehensive in its tracking capabilities, it maintains a straightforward and practical approach to data management and visualization.

--> check out [**OnTheScales @ streamlit.app**](https://onthescales.streamlit.app/) to see it in action!

## Features

**Data Visualization:**
- Chronological progress tracking
- Trend analysis with customizable time ranges
- Prediction when target weight will be reached based on current trend
- Body composition analysis (percentage or kg)

**Measurement Management:**
- Record and edit body measurements (weight in kg, body composition in %)
- Auto-fill feature based on previous measurements
- Date-based entries with update and delete capabilities
- Tabular overview of all recorded measurements

**User Management:**
- Multi-user support with individual profiles
- User profile customization (height and target weight)
- Basic user administration (add, edit, delete)
- Data persistence through CSV files

The interface aims to be straightforward and functional, focusing on providing useful information without unnecessary complexity. As the application runs entirely on your local machine, all data remains under your control and is stored locally in simple CSV files. This ensures complete data privacy while maintaining easy access to your data for backup or external analysis if desired.

## Installation

Clone this repository

```bash
git clone https://github.com/azabicki/OnTheScales
```

### virtual environment

_OnTheScales_ is written in `Python 3.11.2`.

#### venv
Install a virtual environment according to your OS:

##### MacOS & Linux

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

##### Windows

```bash
py -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### Conda

If you are using _*conda_, an environment.yml file is provided, which also installs the required python version `3.11.2`:

```bash
conda env create -f environment.yml
conda activate OnTheScales
```

## Usage

To start the app, run the following command:

```bash
streamlit run OnTheScales.py
```

The app will be available at http://localhost:8501.

Using _OnTheScales_ is straightforward. Simply select a user profile from the dropdown menu, and start tracking your body composition. You can also create multiple user profiles to track different persons.

## Raspberry Pi

_OnTheScales_ can also be run on a Raspberry Pi, I did it on an older Raspberry Pi 3B+. The following steps are required to install and run _OnTheScales_ on a Raspberry Pi:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### autostart

There is also script to start _OnTheScales_ in the `misc/RaspPi` folder. It will start the app in the background and automatically start when the Raspberry Pi boots.

In the following commands, first edit the `path` to the _OnTheScales_ folder, and then run these in your bash console:

```bash
EDIT_THIS_PATH="/path/to/OnTheScales"

chmod +x $EDIT_THIS_PATH/misc/RaspPi/autorun_OnTheScales.sh

echo "# ----- autostart OnTheScales after boot -----" >> ~/.bashrc
echo "if [ \$(tty) == /dev/tty1 ]; then" >> ~/.bashrc
echo "    $EDIT_THIS_PATH/misc/RaspPi/autorun_OnTheScales.sh" >> ~/.bashrc
echo "fi" >> ~/.bashrc
```

## Data Privacy

This application runs entirely locally on your machine. All user data is stored in CSV files in the `data/` directory, ensuring complete control over your personal information.

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
