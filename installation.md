# Installation on Linux:
1 step:
sudo apt-get install build-essential python3-numpy python3-cffi python3-aiohttp \
        libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev \
        libswscale-dev libswresample-dev libavfilter-dev libopus-dev \
        libvpx-dev pkg-config libsrtp2-dev python3-opencv pulseaudio
        
2 step:
sudo pip3 install rtcbot
 
# Installation on Windows:
1 step:
pip install aiohttp cffi numpy opencv-python
 
2 step:
pip install aiortc

3 step:
pip install rtcbot

If needed (camera errors), set environment variable OPENCV_VIDEOIO_PRIORITY_MSMF to 0
