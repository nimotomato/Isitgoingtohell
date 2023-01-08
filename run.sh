#!/bin/bash
docker build -t isitgoingtohell-prod --target prod dockerfile.prod
docker run isitgoingtohell-prod