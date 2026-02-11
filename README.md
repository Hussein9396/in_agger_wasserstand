# Agger Water Level Monitoring

A real-time monitoring system for tracking the water level of the river Agger in Germany. This application continuously monitors and records water level data to a CSV file with automatic alerts when the water level exceeds predefined thresholds.

## Overview

This repository contains a water level monitoring application for the river Agger, a river in Germany. The system runs continuously, collecting water level data at regular intervals and storing it for analysis and monitoring purposes.

## Features

- **Continuous Monitoring**: Runs indefinitely until manually stopped, ensuring uninterrupted water level tracking
- **CSV Data Logging**: Automatically creates and maintains a CSV file with water level measurements
- **Timestamp Recording**: Each measurement includes a precise timestamp for historical tracking
- **Threshold Alerts**: Sends notifications when water levels exceed configurable threshold values
- **Real-time Data**: Provides up-to-date water level information for the river Agger

## How It Works

1. The application starts monitoring the water level of the river Agger
2. At regular intervals, it records the current water level along with a timestamp
3. Data is continuously appended to a CSV file for persistent storage
4. When the water level exceeds a defined threshold, an alert is triggered
5. The monitoring continues until you manually stop the application

## Data Format

The application generates a CSV file containing:
- **Timestamp**: Date and time of the measurement
- **Water Level**: Current water level reading

## Alerts

The system monitors water levels and sends alerts when:
- Water level exceeds the configured threshold value
- This helps prevent potential flooding and enables timely response

## Usage

To stop the application:
- Manually interrupt the program (e.g., press `Ctrl+C` in the terminal)

## Requirements

- Internet connection for accessing water level data
- Sufficient disk space for CSV data storage
- Appropriate permissions for file creation and writing

## About

This application is designed to help monitor water conditions in the river Agger, supporting flood prevention and water resource management efforts in Germany.
