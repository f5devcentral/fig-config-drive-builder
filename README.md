# Flask bsae ConfigDrive ISO builder for the f5-icontrol-gateway

This application publishes an a python flask WSGI app as an nginx unit application into the [f5-icontrol-gateway](https://hub.docker.com/r/f5devcentral/f5-icontrol-gateway) container. 

The application takes a typical cloud-init YAML file containing user_data and produces an ISO9660 ISO image suitable for use as a cloud-init ConfigDrive data source. Attach the ISO images as an IDE CDROM device to a VM and cloud-init enabled operating systmes should process the user_data content.

The application supports two API methods:

```
GET /fig-config-drive-builder
```

which produces an HTML form suitable for uploading your YAML file from a browser.

```
POST /fig-config-drive-builder
```

wher the request body should be your user_data YAML.

The output of the POST API method is a HTTP binary attachment of your ISO image.

curl usage from the CLI for the application running locally:

```
curl --output configdrive.iso -X POST http://localhost:5000/fig-config-drive-builder -H 'Content-Type: text/x-yaml' --data-binary @userdata.yaml
```

curl usage from the CLI for the application running in the f5-icontol-gateway:

```
curl -u 'admin:admin' --output configdrive.iso -X POST https://localhost:8443/fig-config-drive-builder -H 'Content-Type: text/x-yaml' --data-binary @userdata.yaml
```

The `unit_config.conf` file provides the needed route and application information for nginx unit to add a URI namespace for your application.

## Run Your Application Locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
deactivate
```

## Build Your f5-icontrol-gateway Application Container

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
docker build -t fig-config-drive-builder .
deactivate
```

## Run Your f5-icontrol-gateaway Application

```bash
docker run --rm -p 8443:443 --name fig-config-drive-builder fig-config-drive-builder:latest
```

You should then be able to access your application at:

[https://localhost:8443/fig-config-drive-builder](https://localhost:8443/fig-config-drive-builder)
