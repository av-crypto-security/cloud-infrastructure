# Creating a Cloud Function via CLI

This document demonstrates how to create and deploy a simple HTTP function
using the Yandex Cloud CLI. The goal is to understand the basic workflow
of serverless deployment and version management.

## Service Account

Each serverless component should run under a dedicated service account.
This ensures clear access control and traceability.

The service account is created using the CLI and granted the `editor`
role within the working folder.

Environment variables such as `SERVICE_ACCOUNT_ID` and `FOLDER_ID`
are exported locally to simplify subsequent commands.

## Function Creation

A serverless function named `cloud-function` is created.

The function runtime environment is Python and the entrypoint
is defined in the source file.

The function is deployed by uploading the source code and creating
a new version.

Important parameters during deployment include:

- memory allocation
- execution timeout
- runtime environment
- entrypoint
- service account identity

## Invocation

After deployment, the function can be invoked using the CLI.

Once public invocation is enabled, the function can also be accessed
via HTTP using the automatically generated endpoint URL.

Typical workflow:

1. create function
2. upload source code
3. create version
4. enable public invocation
5. test via CLI or HTTP
