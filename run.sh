cd ~/design_hri_project
source ./venv/bin/activate
sudo pigpiod
pulseaudio --kill
jack_control start
python3 ./main.py
