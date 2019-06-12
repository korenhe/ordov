#!/bin/bash

sudo rm -rf ./accounts/migrations/__pycache__
sudo rm -rf ./candidates/migrations/__pycache__
sudo rm -rf ./companies/migrations/__pycache__
sudo rm -rf ./experiences/migrations/__pycache__
sudo rm -rf ./interviews/migrations/__pycache__
sudo rm -rf ./resumes/migrations/__pycache__
sudo rm -rf ./smart_analyse/migrations/__pycache__

sudo rm -rf ./accounts/migrations/0*.py*
sudo rm -rf ./candidates/migrations/0*.py*
sudo rm -rf ./companies/migrations/0*.py*
sudo rm -rf ./experiences/migrations/0*.py*
sudo rm -rf ./interviews/migrations/0*.py*
sudo rm -rf ./resumes/migrations/0*.py*
sudo rm -rf ./smart_analyse/migrations/0*.py*
