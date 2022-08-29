# Stori Card Test

This application generates a summary report from a transactions file and sends an email to the user.

The application was deployed as a Docker image to AWS Lambda using GitHub Actions on a Pull Request to the main branch of this repository.

The AWS Lambda service is triggered when uploading a file to a S3 bucket (more details in the usage section).

## Usage

The application was deployed to AWS Lambda. To generate a report you should upload a valid `csv` transactions file to the following S3 bucket:

The file object must have the prefix `txn/`. The file must be named as the email of the user. If the file name contains an invalid email the report will be sent to the default email (my email).   


```python
s3://stori-cmunoz-1/txn/email@domain.com.csv
```

Sample command to load a file:

```python
aws s3 cp [local_file_path] s3://stori-cmunoz-1/txn/email@domain.com.csv
```

Note: Credentials to upload the file will be provided.

### Usage (local but limited)

Another option, is to build the image included in the Docker file. 

```python
docker build -t stori-test .

docker run -p 9000:8080 stori-test

curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```

A sample event is provided in the `tests` folder to be passed in the curl request when executed locally. This option won't allow you to receive the email in your own account, unless you upload a file to the S3 bucket named as your email first.

This approach will require to set the email server, user, and password to correctly send the email.

## Comments

A test was included as part of AWS Lambda.

## License
[MIT](https://choosealicense.com/licenses/mit/)
