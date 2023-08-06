#!/bin/bash
export CAPTCHA_ESPEAK_PATH=$(which espeak)
export CAPTCHA_SOX_PATH=$(which sox)
coverage run --rcfile .coveragerc manage.py test --failfast captcha
coverage xml
coverage html
