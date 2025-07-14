# Configuring AWS and JFrog Private Link

This document outlines the steps to configure AWS and JFrog Private Link to ensure a secure connection using AWS VPC endpoints. We will include instructions for creating the endpoint and security rules.

## Prerequisites

- Ensure you have an AWS account with permissions to create VPCs, Endpoints, and Security Groups.

## Step 1: Create a VPC Endpoint

1. **Login to AWS Management Console:**
   - Go to the [AWS Management Console](https://aws.amazon.com/console/).

2. **Navigate to VPC:**
   - Go to the `VPC` console.
   ![VPC](image/1.png)

3. **Create Endpoint:**
   - In the left menu, select `Endpoints`.
   - Click on the `Create Endpoint` button.
   ![Endpoint](image/2.png)
4. **Select the Service:**
   - Choose `PrivateLink Ready partner services`.
   - Enter the JFrog service name, e.g., `com.amazonaws.vpce....`.( Find in https://jfrog.com/help/r/myjfrog-portal/step-1-create-the-endpoint-in-aws)
   ![Create Endpoint](image/3.png)
5. **Select VPC:**
   - Choose the VPC that you want to connect to JFrog.
   ![Create Endpoint](image/4.png)
   - VPC need to config `DNS hostnames Enabled`
   ![VPC Config](image/6.png) 
6. **Configure Subnets:**
   - Select the appropriate subnets of the VPC.
   ![Create Endpoint](image/5.png)
7. **Configure Security Groups:**
   - Select one or more security groups to control access to this endpoint.
   ![Create Endpoint](image/7.png)
   - Security group need to peon port 443  for outbound connections.
   ![Create Endpoint](image/8.png)
8. **Create Endpoint:**
   - Click `Create Endpoint`.

## Step 2: Setup Endpoint Configuration In JFrog 

1. **Create Endpoint In MyJFrog:**
   - Login MyJFrog ，choose `Security -- Private Connections`
   ![Create Endpoint](image/9.png)

2. **Create Endpoint:**
   - Config Endpoint ID in MyJFrog
   ![Create Endpoint](image/10.png)
   - You can find you Endpoint IN in AWS Endpoint Page
   ![Create Endpoint](image/11.png)

## Step 3: Setup DNS in Route53

1. **Create Hosted zone in Route53:**
   - Open AWS Route53 console
   ![Create Endpoint](image/12.png)

2. **Create Private Hosted zone:**
   - Setting up private hostedzone for you VPC
   ![Create Endpoint](image/13.png)

2. **Create Private Record For you JFrog :**
   - Add a CNAME record 
   ![Create Endpoint](image/14.png)
2. **Verify your connection from your VM to jfrog saas platform :**
  ```
[ec2-user@ip-10-0-0-12 ~]$ nslookup yoursaas.pe.jfrog.io
Server:		10.0.0.2
Address:	10.0.0.2#53
  ```
   ![alt text](image.png)