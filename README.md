# Automated Secret Rotation using AWS Secrets Manager

This GitHub repository contains the implementation, code, dependencies, and design solution document for an automated secret rotation system using AWS Secrets Manager.

## Overview

Secret rotation is a crucial aspect of maintaining the security of sensitive information, such as database credentials. This project leverages AWS Secrets Manager to automate the rotation of secrets, specifically targeting multiple MySQL root user passwords.

### Repository Structure

1. **Implementation Guide:** Comprehensive documentation covering the implementation steps, including Lambda function setup, AWS Secrets Manager setup, and more.

2. **`lambda_function.py` Code:** Python code for the Lambda function responsible for rotating MySQL root user passwords. The code includes support for manual rotations, and logic to reset the rotation cycle.

3. **`pythonLambdaFunction.zip`:** A zip file containing the Lambda function code along with its dependencies. This zip file can be used for easy deployment of the Lambda function.

4. **Design Solution Document:** A detailed document explaining the design solution, architectural decisions, and considerations for the automated secret rotation system.

## Getting Started

To get started with the implementation, follow the steps outlined in the [Implementation Guide](./Implementation%20Guide).

### Lambda Function

The core of the secret rotation system is the Lambda function. The code in `lambda_function.py` can be modified and extended based on specific requirements.

### Dependencies

The `pythonLambdaFunction.zip` file contains the Lambda function code along with its dependencies. This zip file simplifies the deployment process and ensures that all required libraries are included.

## Design Solution

For a deeper understanding of the design choices, architecture, and considerations behind the automated secret rotation system, refer to the [Design Solution Document](./Design%20Solution%20Document).




