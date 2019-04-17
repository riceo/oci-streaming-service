import oci
import sys
import logging
import base64
import time


def print_usage_instructions():
    usage = """
    A utility for producing and consuming test messages on Oracle
    Cloud Infrastructure's Streaming Service.

    USAGE: python main.py producer|consumer STREAM_ID OSS_ENDPOINT
    """
    print(usage)


def get_cursor_by_partition(client, stream_id, partition):
    """
    Creates a new cursor object for consuming messages from a given stream and
    partition. We use the "TYPE_LATEST" cursor type to consume messages from
    the point that the cursor was created.
    """
    logging.info("Creating a cursor for partition {}".format(partition))

    cursor_details = oci.streaming.models.CreateCursorDetails(
        partition=partition,
        type=oci.streaming.models.CreateCursorDetails.TYPE_LATEST)

    response = client.create_cursor(stream_id, cursor_details)

    return response.data.value


def consumer_loop(client, stream_id, initial_cursor):

    # The cursor position to start with
    cursor = initial_cursor

    while True:

        # Sleep for a second, so we don't get rate-limited by the OCI API
        time.sleep(1)

        get_response = client.get_messages(stream_id, cursor)

        # No messages to process. return.
        if not get_response.data:
            logging.info("No new messages...")
            continue

        # Process the messages
        print(" Read {} messages".format(len(get_response.data)))
        for message in get_response.data:
            if not message.key:
                key = None
            else:
                key = base64.b64decode(message.key)

            logging.info("[MESSAGE] {}: {}".format(
                    key.decode(),
                    base64.b64decode(message.value).decode()
                )
            )

        # Get the next cursor for passing to the next iteration of the loop
        cursor = get_response.headers["opc-next-cursor"]


def producer_loop(client, stream_id):
    """
    Produces a message containing the current epoch time every 1 second
    """

    key = base64.b64encode(b"time").decode()

    while True:
        # Get the current time as a byte string. time.time() returns a float
        # which is a little too explicit for what we want, so we convert it in
        # to an int before a string, then finally encode that to unicode
        value = str(int(time.time())).encode()

        logging.info("Producing message for {}".format(value.decode()))

        # The OCI API expects a list of messages, so we place our message
        # into a list containing one element, formatted to conform to the
        # PutMessagesDetailsEntry model, which includes having its contents
        # base64 encoded
        message = [
            oci.streaming.models.PutMessagesDetailsEntry(
                key=key,
                value=base64.b64encode(value).decode()
            )
        ]

        # Format the message details to conform to the PutMessagesDetails model
        message = oci.streaming.models.PutMessagesDetails(messages=message)

        # Send the message!
        result = client.put_messages(stream_id, message)

        # The result object will contain error information for each message.
        # since in this case we only had one message, we don't need to iterate
        # over the object.
        if result.data.entries[0].error:
            logging.error("Error ({}) : {}".format(
                    result.data.entries[0].error,
                    result.data.entries[0].error_message
                )
            )
        else:
            logging.info(
                "Published message to partition {} , offset {}".format(
                    result.data.entries[0].partition,
                    result.data.entries[0].offset
                )
            )

        time.sleep(1)


def run_producer(client, stream_id):
    """
    Starts a producer loop
    """
    logging.info("Starting a producer...")

    producer_loop(client, stream_id)


def run_consumer(client, stream_id):
    """
    Gets a new cursor object then starts a consumer loop
    """
    logging.info("Starting a consumer...")

    cursor = get_cursor_by_partition(client, stream_id, partition="0")
    consumer_loop(client, stream_id, initial_cursor=cursor)


if __name__ == "__main__":

    # Check the application has the correct number of arguments passed to it
    if len(sys.argv) < 4:
        print_usage_instructions()
        sys.exit()

    stream_id = sys.argv[2]
    message_endpoint = sys.argv[3]

    # Pass OCI CLI config file
    config = oci.config.from_file("~/.oci/config", "DEFAULT")

    # Create an OCI client
    client = oci.streaming.StreamClient(
        config, service_endpoint=message_endpoint
    )

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s %(message)s"
    )

    # Decide which mode to run in
    if sys.argv[1] == "consumer":
        run_consumer(client, stream_id)
    elif sys.argv[1] == "producer":
        run_producer(client, stream_id)
    else:
        print_usage_instructions()
        sys.exit()
