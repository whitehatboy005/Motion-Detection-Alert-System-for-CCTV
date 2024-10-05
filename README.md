# IP Camera Motion Detection with Telegram Alerts

This repository contains two main tools:
1. **ROI Selector Tool**: A graphical tool to help users easily select a Region of Interest (ROI) from the screen.
2. **IP Camera Motion Detection Tool**: A CCTV-like system that monitors an IP camera feed for motion within the defined ROI and sends alerts via Telegram.

## Features

### 1. ROI Point Finder Tool:
- Graphically select the **Region of Interest (ROI)** on your screen.
- Print the start and end coordinates of the ROI for use in motion detection.
- Simplifies the process of defining an ROI for motion detection.

### 2. IP Camera Motion Detection Tool:
- **Monitor an IP camera stream**: Detect motion in a specified area of the video feed (ROI).
- **Send Telegram alerts**: When motion is detected, a snapshot of the frame is sent to a Telegram chat.
- **Configurable settings**: Set up the Telegram Bot Token, IP Camera URL, and ROI coordinates via environment variables.
- **Efficient motion detection**: Only monitors motion within the defined ROI to minimize unnecessary alerts.

## Installation
## Clone the Repository
```bash
git clone https://github.com/whitehatboy005/Motion-Detection-Alert-System-for-CCTV
```
## Move the file
```bash
cd Motion-Detection-Alert-System-for-CCTV
```
## Install Dependencies
```bash
pip install -r requirements.txt
```
## Find ROI Point for alert zone
```bash
python ROI_point_finder.py
```
## Config The Details
```bash
notepad config.env
```
## Run the Program
```bash
python CCTV_Alert.py
```

## Instructions

To get Chat ID visit [@GetMyChatID_Bot](https://t.me/GetMyChatID_Bot) Now you will copy the chat Id and config it.

To access the bot [@SecurityAlertBot](https://t.me/ProjectResultBot) and START it.

## License

This project is licensed under the terms of the [MIT license](LICENSE.md).
