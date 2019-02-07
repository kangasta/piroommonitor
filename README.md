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
