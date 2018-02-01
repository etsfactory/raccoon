@echo off
pushd %~dp0
conda "install scipy>=0.17.0"
python -m pip install --editable %~dp0 -r requirements.txt
popd
