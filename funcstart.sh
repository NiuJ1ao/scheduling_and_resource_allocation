# install dependencies for local execution
cd ~/WorkflowSchedulingCwk/functions
python3 -m venv .venv
source .venv/bin/activate
sudo apt -y install python3-opencv
pip install --upgrade pip
pip install -r requirements.txt

# start Azure Function locally
func host start &
