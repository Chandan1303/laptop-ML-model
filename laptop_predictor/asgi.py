# Project Title: LaptopPilot
# Subject: Software Testing and Quality Assurance
# Team Members:
# USN1: 4NI23IS252
# Name1: Dayanand Shivananda Sagar
# USN2: 4NI23IS253
# Name2: Chandan Shridhar Hegde
# USN3: 4NI24IS408
# Name3: Harsha S
# USN4: 4NI24IS412
# Name4: Mohammad Masood Hassan HA
# Date of code writing: 14-09-2026 to 25-09-2026

"""
ASGI config for laptop_predictor project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'laptop_predictor.settings')

application = get_asgi_application()
