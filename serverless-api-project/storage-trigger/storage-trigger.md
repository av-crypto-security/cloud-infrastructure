# Object Storage Trigger for Serverless Functions

This document describes an event-driven architecture where
a serverless function uploads files to Object Storage and
another function is automatically triggered when a new object appears.

## Architecture

The system consists of three components:

Cloud Function  
Uploads a generated file to Object Storage.

Object Storage Bucket  
Stores uploaded files.

Trigger Function  
Executes automatically when a new object is created in the bucket.

This pattern is commonly used in data pipelines, image processing
systems, and log processing architectures.

## Object Storage Integration

The first function uses the S3-compatible API to upload files
to Object Storage. Authentication is performed using S3-compatible access keys
associated with a service account.

The function creates a temporary file, uploads it to the bucket,
and removes the local temporary file afterward.

## Environment Variables

Sensitive parameters are passed through environment variables:

- ACCESS_KEY
- SECRET_KEY
- BUCKET_NAME
- TIME_ZONE

These variables are injected during function deployment.

## Event Trigger

An Object Storage trigger is configured to listen for
`create-object` events.

When a new file appears in the bucket, the trigger invokes
the second function automatically.

The triggered function receives event metadata and logs
information about the object creation.

## Event-driven Workflow

1. user invokes the upload function
2. file is written to Object Storage
3. Object Storage emits event
4. trigger invokes the second function
5. function logs event details
