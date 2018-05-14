from flask_lambda import FlaskLambda, logging
import boto3
from botocore.exceptions import ClientError
from io import BytesIO


app = FlaskLambda(__name__)
MY_S3_BUCKET = 'jakub-sam-hello-world-bucket'
MY_FILE = 'access-counter.txt'


def write_to_bucket(s3, counter: int):
    global MY_S3_BUCKET, MY_FILE
    s3.put_object(Body=bytes(str(counter), 'utf-8'), Bucket=MY_S3_BUCKET, Key=MY_FILE)


@app.route('/')
def hello():
    global MY_S3_BUCKET, MY_FILE
    logging.info('Root endpoint called.')
    s3 = boto3.client('s3')
    call_counter = 0
    try:
        # Read counter
        counter_i = BytesIO()
        s3.download_fileobj(MY_S3_BUCKET, MY_FILE, counter_i)
        read_value = counter_i.getvalue().decode('utf-8')
        logging.info('File ' + MY_FILE + ' content: "' + read_value + '"')
        if read_value.isdecimal():
            call_counter = int(read_value)
        counter_i.close()

        call_counter += 1

        # Write counter
        write_to_bucket(s3, call_counter)
    except ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if 404 == error_code or 403 == error_code:
            try:
                # Write counter
                call_counter += 1
                write_to_bucket(s3, call_counter)
            except Exception as e:
                logging.error('Cannot write to ' + MY_S3_BUCKET + '/' + MY_FILE + ": " + str(e))
        else:
            logging.error('Cannot read from ' + MY_S3_BUCKET + '/' + MY_FILE + ": " + str(e))
    except Exception as e:
        logging.error('Cannot read/write from/to ' + MY_S3_BUCKET + '/' + MY_FILE + ": " + str(e))

    return "Hello World! Access count = " + str(call_counter)


if __name__ == '__main__':
    app.run(debug=True)
