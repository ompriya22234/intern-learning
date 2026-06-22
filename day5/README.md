 # Day 5 - FastAPI Docker App

## Description
This project is a Dockerized FastAPI application.

## Endpoint

GET /about

Returns:
- Name
- Skills learned this week

## Install Dependencies

pip install -r requirements.txt

## Run Locally

python -m uvicorn main:app --reload

## Build Docker Image

docker build -t day5-api .

## Run Docker Container

docker run -p 8000:8000 day5-api

## API Documentation

http://localhost:8000/docs