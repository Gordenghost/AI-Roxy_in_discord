@echo off
REM ���� Roxy ����
call conda activate Roxy

REM ���е�һ�� python api2.py ָ��
start cmd /k "cd /d %~dp0\GPT-SoVITS-v2-240807 && call conda activate Roxy && python api2.py -s "SoVITS_weights_v2/Roxy_e8_s512.pth" -g "GPT_weights_v2/Roxy-e15.ckpt" -dr "../prompt/1.wav" -dt "����ħ�g,�ΰKħ�g,�ن�ħ�g,���줾�����" -dl "ja""

REM ���еڶ��� python api2.py ָ��
cd /d %~dp0
python main.py
pause