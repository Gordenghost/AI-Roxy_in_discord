@echo off
REM 激活 Roxy 环境
call conda activate Roxy

REM 运行第一条 python api2.py 指令
start cmd /k "cd /d %~dp0\GPT-SoVITS-v2-240807 && call conda activate Roxy && python api2.py -s "SoVITS_weights_v2/Roxy_e8_s512.pth" -g "GPT_weights_v2/Roxy-e15.ckpt" -dr "../prompt/1.wav" -dt "攻撃魔術,治癒魔術,召喚魔術,それぞれ初級" -dl "ja""

REM 运行第二条 python api2.py 指令
cd /d %~dp0
python main.py
pause