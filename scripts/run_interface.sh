# Open the interface for the agents
export FLASK_APP="interface/main.py"
echo $FLASK_APP
python3 -m flask run

unset FLASK_APP