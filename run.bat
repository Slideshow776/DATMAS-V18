@echo This program assumes python with pip is installed.
@echo Installing dependencies ...

python -m pip install Pillow==5.0.0
python -m pip install numpy==1.14.0
python -m pip install matplotlib==2.1.2
python -m pip install openpyxl==2.4.10
python -m pip install twitter==1.18.0
python -m pip install polyline==1.3.2

@echo Loading project's main program ...
cd Frontend
python gui.py