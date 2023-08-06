# Jocasta
Library to extract data from serial and send it various services.

# Supported Services
Services and things Jocasta can send data to.

## Dweet https://dweet.io
Ridiculously simple messaging (and alerts) for the Internet of Things.

## IO https://io.adafruit.com/
Open beta of a simple to use graphing platform.

## Text File
A simple file in ```/tmp``` with a string of JSON.


# Setup
The below will get you going.
```
git clone git@github.com:chrishannam/jocasta.git
cd jocasta
[sudo] pip install virtualenv
virtualenv .
source bin/activate
pip install -r requirements.txt
python src/jocasta/collector.py
```

Assuming that works you will need to configure services.

# Configuring Third Party Services

```
cp src/jocasta/settings/__init__.py.example src/jocasta/settings/__init__.py


# populate the fields with the third party settings and uncomment the services you want
$EDITOR src/jocasta/settings/__init__.py

```
