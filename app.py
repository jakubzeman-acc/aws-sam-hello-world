from flask_lambda import FlaskLambda, logging
import boto3
import os
from botocore.exceptions import ClientError
from io import BytesIO


app = FlaskLambda(__name__)
MY_S3_BUCKET_VAR_NAME = 'S3_BUCKET_NAME'
MY_FILE = 'access-counter.txt'


def write_to_bucket(s3, counter: int):
    s3.put_object(Body=bytes(str(counter), 'utf-8'), Bucket=os.getenv(MY_S3_BUCKET_VAR_NAME), Key=MY_FILE)


def read_from_bucket(s3) -> int:
    ret = 0
    counter_i = BytesIO()
    s3.download_fileobj(os.getenv(MY_S3_BUCKET_VAR_NAME), MY_FILE, counter_i)
    read_value = counter_i.getvalue().decode('utf-8')
    logging.info('File ' + MY_FILE + ' content: "' + read_value + '"')
    if read_value.isdecimal():
        ret = int(read_value)
    counter_i.close()
    return ret


@app.route('/')
def hello():
    global MY_S3_BUCKET, MY_FILE
    logging.info('Root endpoint called.')
    s3 = boto3.client('s3')
    call_counter = 0
    try:
        # Read counter
        call_counter = read_from_bucket(s3)
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
                logging.error('Cannot write to ' + os.getenv(MY_S3_BUCKET_VAR_NAME) + '/' + MY_FILE + ': ' + str(e))
        else:
            logging.error('Cannot read from ' + os.getenv(MY_S3_BUCKET_VAR_NAME) + '/' + MY_FILE + ': ' + str(e))
    except Exception as e:
        logging.error('Cannot read/write from/to ' + os.getenv(MY_S3_BUCKET_VAR_NAME) + '/' + MY_FILE + ': ' + str(e))

    return 'Hello World! Access count = ' + str(call_counter)


if __name__ == '__main__':
    app.run(debug=True)
