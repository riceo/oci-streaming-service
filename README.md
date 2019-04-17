# Oracle Streaming Service Demo

A simple Python application that can either produce or consume messages on an existing [OCI Streaming Service](https://docs.cloud.oracle.com/iaas/Content/Streaming/Concepts/streamingoverview.htm) stream.

## Requirements

* An Oracle Cloud Infrastructure account with Streaming Service access
* An already configured OCI SDK with the config file in the default location `/.oci/config`.
* The OCID of an existing OSS Stream
* The endpoint URL for OSS in your region, which can be found at https://docs.cloud.oracle.com/iaas/Content/API/Concepts/apiref.htm.
* A Python 3 installation
* A [Pipenv](https://pipenv.readthedocs.io/en/latest/) installation

The application was written and tested on MacOS. It may run under other operating systems with minor tweaks (notably the OCI config path).

## Running

Once checked out, the application can be started in either mode via:

```
pipenv run python main.py <producer|consumer> <STREAM OCID> <OSS ENDPOINT URL>
```

For the purposes of demoing Oracle Streaming Service, it is recommended to start both modes in separate terminal sessions and watch their output simultaneously.

## Producer Mode

This mode will create a message on the given queue every 1 second until exited.

## Consumer mode

This mode will consume any messages added to the queue from the moment the consumer was started. It will poll every 1 second for new messages until exited.