# piroommonitor

Python script to push data from Raspberry Pi to fdbk backend.

## Installing

First, ensure that you have pigpiod installed. Then, run:
```
sudo pigpiod
sudo python3 setup.py install
```

## Usage

See scripts help by running:
```bash
piroommonitor --help
```

## Testing

Run unit tests with commands:

```bash
python3 -m unittest discover -s piroommonitor/tst/
```

Get test coverage with commands:
```bash
cd pi_si7021

coverage run -m unittest discover -s piroommonitor/tst/
coverage report -m
```
