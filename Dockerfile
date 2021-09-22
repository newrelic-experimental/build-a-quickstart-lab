FROM python:3.9
ADD db.py .
ADD simulator.py .
RUN pip install newrelic-telemetry-sdk
CMD [ "python", "./simulator.py" ]