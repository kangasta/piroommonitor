# piroommonitor

Python script to push data from Raspberry Pi to fdbk backend.

## Installing

First, ensure that you have pigpiod installed. Then, run:

```bash
sudo pigpiod
sudo python3 setup.py install
```

If you see an error about conflicting version for requests package, remove the earlier installation with

```bash
sudo apt-get remove python3-requests
```

before installing the package.

## Usage

See scripts help by running:
```bash
piroommonitor --help
```

### Getting started on Raspberry Pi Zero

```bash
git clone --depth 1 https://github.com/kangasta/fdbk-webapp.git;
pushd fdbk-webapp/docker-build/;
	sudo docker build -f Dockerfile-RPiZero -t fdbk .;
popd;

docker run -dp 8080:8080 fdbk;

piroommonitor http://localhost:8080 -v -l 19 20 21 -l 22 23 24 -b 0.05 -m 4 --new-topic-id;
```

To automatically start fdbk (without persistent data storage) and piroommonitor after boot, add following cron job (with `crontab -e`):

```cron
@reboot /usr/bin/docker run -dp 8080:8080 fdbk && /usr/local/bin/piroommonitor http://localhost:8080 -v -l 19 20 21 -l 22 23 24 -b 0.05 -m 4 --new-topic-id
```

### Adding support for new I2C sensors

To add support for additional I2C sensors, create a wrapper for the library provided by the sensor vendor under `piroommonitor/sensors/`, import the wrapper in [`sensors/__init__.py`](./piroommonitor/sensors/__init__.py), add the sensor to supported sensors list in [`piroommonitor/i2c_sensors.py`](./piroommonitor/i2c_sensors.py), and add dependency libraries to `setup.py` and `requirements.txt`.

The wrapper should provide three properties: address, data and units. The address property should be an integer value of the I2C address, the data property should be a dict of measurements provided by the sensor, and the units property should be a dict of measurement values and corresponding units. The two dicts should share the same set of keys. For unitless masurement fields, use `None` as the unit value. See the current set of wrappers for an example.

## Testing

Run unit tests with commands:

```bash
python3 -m unittest discover -s piroommonitor/tst/
```

Get test coverage with commands:
```bash
coverage run -m unittest discover -s piroommonitor/tst/
coverage report -m
```
