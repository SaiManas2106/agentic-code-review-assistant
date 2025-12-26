#!/usr/bin/env bash
export $(grep -v '^#' .env | xargs)
python -m src.app
