#Python (3.12) code for lambda function
import json
import boto3
import pymysql

secrets_manager = boto3.client('secretsmanager')

def rotate_mysql_password(event, context):
    # Replace with your MySQL secret name
    secret_name = "prod/prodData/MySQL"

    # Check if rotation is requested manually
    is_manual_rotation = event and event.get('is_manual_rotation', False)

    # Retrieve the current secret value
    current_secret = secrets_manager.get_secret_value(SecretId=secret_name)
    current_password = json.loads(current_secret['SecretString'])['password']

    # Generate a new password (you may want to use a more secure method)
    new_password = "new_password"

    # Update the MySQL secret in Secrets Manager
    response = secrets_manager.update_secret(
        SecretId=secret_name,
        SecretString=json.dumps({'password': new_password})
    )

    # Optionally, you may want to use the new password to update your MySQL user
    update_mysql_user(new_password)

    # Reset rotation cycle if done manually
    if is_manual_rotation:
        reset_rotation_cycle(secret_name)

    return {
        'statusCode': 200,
        'body': json.dumps('MySQL secret rotation successful!')
    }

def update_mysql_user(new_password):
    # Replace with your MySQL connection details
    connection = pymysql.connect(host="your-mysql-host",
                                 user="your-mysql-user",
                                 password="your-mysql-password",
                                 database="your-mysql-database")

    with connection.cursor() as cursor:
        # Replace with your MySQL user and host details
        cursor.execute(f"ALTER USER 'your-mysql-user'@'%' IDENTIFIED BY '{new_password}';")
        connection.commit()

def reset_rotation_cycle(secret_name):
    # Reset rotation cycle logic goes here
    # You may update a timestamp or counter in your Secrets Manager secret
    pass

# Uncomment the line below to test the rotation function locally
# rotate_mysql_password(None, None)

#Make sure to upload this code with pymysql file on code source while creating lambda function.
