#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install diagrams


# In[1]:


from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.network import APIGateway, CloudFront
from diagrams.aws.storage import S3
from diagrams.aws.ml import Comprehend
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.security import Cognito
from diagrams.aws.devtools import Codepipeline, Codebuild, Codedeploy
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.client import Client

with Diagram("PinkBird Web Application Architecture", show=True):
    user = Client("User Browser")
    
    # Frontend
    frontend = CloudFront("CloudFront CDN")
    hosting = S3("S3 Hosting (React App)")
    
    # API Gateway and Backend
    api_gateway = APIGateway("API Gateway")
    auth = Cognito("User Authentication (Cognito)")
    backend = [Lambda("Lambda Function 1"), Lambda("Lambda Function 2"), Lambda("Lambda Function 3")]
    
    # Database
    database = Dynamodb("Document Store (DynamoDB)")
    
    # NLP and Machine Learning
    nlp_ml = Comprehend("NLP Analysis (Amazon Comprehend)")
    
    # Asynchronous Processing
    sqs = SQS("Queue Service (SQS)")
    sns = SNS("Notification Service (SNS)")
    
    # Monitoring
    monitoring = Cloudwatch("Monitoring & Logging (CloudWatch)")
    
    # CI/CD
    ci_cd_pipeline = Codepipeline("CI/CD Pipeline")
    ci_cd_build = Codebuild("CodeBuild")
    ci_cd_deploy = Codedeploy("CodeDeploy")

    # Connections
    user >> frontend >> hosting >> api_gateway
    api_gateway >> auth
    api_gateway >> backend
    backend >> database
    backend >> nlp_ml
    backend >> sqs
    backend >> sns
    backend >> monitoring
    database >> monitoring
    ci_cd_pipeline >> ci_cd_build >> ci_cd_deploy >> hosting

