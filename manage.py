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

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'laptop_predictor.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
