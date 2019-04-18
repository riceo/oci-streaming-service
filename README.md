# Oracle Streaming Service Demo

A simple Python application that can either produce or consume messages on an existing [OCI Streaming Service](https://docs.cloud.oracle.com/iaas/Content/Streaming/Concepts/streamingoverview.htm) stream.

It takes advantage of [Consumer Groups and Group Cursors](https://docs.cloud.oracle.com/iaas/Content/Streaming/Tasks/consuming.htm) to allow multiple consumers to consume from a stream simultaneously. 

## Requirements

* An Oracle Cloud Infrastructure account with Streaming Service access
* An already configured OCI SDK with a config file somewhere accessible by the application.
* The OCID of an existing OSS Stream
* The endpoint URL for OSS in your region, which can be found at https://docs.cloud.oracle.com/iaas/Content/API/Concepts/apiref.htm.
* A Python 3 installation
* A [Pipenv](https://pipenv.readthedocs.io/en/latest/) installation

The application was written and tested on MacOS. It may run under other operating systems with minor tweaks (notably the OCI config path, which can be configured with an optional environment variable, as below).

## Running

Once checked out, the application can be started in either mode via:

```
pipenv run python main.py <producer|consumer> <STREAM OCID> <OSS ENDPOINT URL>
```

For the purposes of demoing Oracle Streaming Service, it is recommended to start run multiple instances of the application on different terminal windows by:

1. Launch at least two consumer instances in separate terminals
2. Launch at least one producer instance in a separate terminal
3. Watch messages being consumed by one consumer
4. Kill that consumer and watch messages be consumed by one of the other consumers

### Optional Environment Variables

* `OCI_CONFIG`: Path to your OCI SDK configuration file. Defaults to `~/.oci/config`
* `OSS_GROUP_NAME`: The consumer group name to use. Defaults to `tutorial`
* `OSS_INSTANCE_NAME`: The instant identifier for this member of the consumer group. Defaults to a random 8 character string. 

## Producer Mode

This mode will create a message on the given stream every 1 second until exited.

## Consumer mode

This mode will consume any messages added to the stream from the moment the consumer was started. It will poll every 1 second for new messages until exited.

By default, Consumer mode will generate a unique instance ID on startup then join or create a consumer group with the name "tutorial".
