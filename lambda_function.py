#Python (3.12) code for lambda function
import json
import boto3
import pymysql
from datetime import datetime, timedelta

secrets_manager = boto3.client('secretsmanager')
sns_client = boto3.client('sns')

def rotate_mysql_password(event, context):
    # Replace with your MySQL secret name
    secret_name = "prod/prodData/MySQL"

    # Check if rotation is requested manually
    is_manual_rotation = event and event.get('is_manual_rotation', False)

    # Calculate the rotation date 40 days from now
    rotation_date = (datetime.now() + timedelta(days=40)).strftime('%Y-%m-%d')

    # Retrieve the current secret value once
    current_secret = secrets_manager.get_secret_value(SecretId=secret_name)
    secret_data = json.loads(current_secret['SecretString'])
    users_data = secret_data.get("users", [])

    for user_info in users_data:
        username = user_info.get("username")
        current_password = user_info.get("password")

        # Generate a new password 
        new_password = "new_password"

        # Update the MySQL secret in Secrets Manager
        secrets_manager.update_secret(
            SecretId=secret_name,
            SecretString=json.dumps(secret_data)
        )

        # Update the MySQL user password
        update_mysql_user(username, new_password)

        # Send notification immediately after rotation
        send_notification(f"Password for MySQL user '{username}' rotated successfully!", subject='Rotation Completed')

    # Send notification 5 days before rotation
    send_notification(f"MySQL secret rotation is scheduled for {rotation_date}.", subject='Rotation Scheduled')

    # Reset rotation cycle if done manually
    if is_manual_rotation:
        reset_rotation_cycle(secret_name)

    return {
        'statusCode': 200,
        'body': json.dumps('MySQL secret rotation successful!')
    }

def update_mysql_user(username, new_password):
    # Replace with MySQL connection details
    connection = pymysql.connect(host="your-mysql-host",
                                 user="your-mysql-user",
                                 password="your-mysql-password",
                                 database="your-mysql-database")

    with connection.cursor() as cursor:
        # Replace with your MySQL user and host details
        cursor.execute(f"ALTER USER '{username}'@'%' IDENTIFIED BY '{new_password}';")
        connection.commit()

def reset_rotation_cycle(secret_name):
    # The rotation type is stored as 'timestamp' in the Secrets Manager secret
    rotation_type = 'timestamp'

    # Retrieve the current secret value
    current_secret = secrets_manager.get_secret_value(SecretId=secret_name)
    secret_data = json.loads(current_secret['SecretString'])

    if rotation_type == 'timestamp':
        # Update the rotation timestamp to the current time
        secret_data['rotation_timestamp'] = datetime.now().isoformat()
    elif rotation_type == 'counter':
        # Update the rotation counter (assuming you have a 'rotation_counter' field)
        secret_data['rotation_counter'] += 1
    else:
        # Handle other rotation types if needed
        pass

    # Update the MySQL secret in Secrets Manager
    secrets_manager.update_secret(
        SecretId=secret_name,
        SecretString=json.dumps(secret_data)
    )

def send_notification(message, subject='MySQL Secret Rotation Notification'):
    # Replace 'your-topic-arn' with the actual ARN of your SNS topic
    topic_arn = 'arn:aws:sns:your-region:your-account-id:MySQLRotationNotification'
    
    sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject=subject
    )


# Uncomment the line below to test the rotation function locally
rotate_mysql_password(None, None)

#Make sure to upload this code with pymysql file on code source while creating lambda function.
