# Go Project with JFrog Artifactory Integration

This guide demonstrates how to use JFrog Artifactory for Go module management, building, and publishing.

## Prerequisites

1. Go 1.16 or later
2. JFrog CLI installed
3. Access to JFrog Artifactory instance

## Project Structure

```
go-sample/
├── cmd/
│   └── main.go
├── go.mod
├── go.sum
└── README.md
```

## Configuration

### 1. Configure Go Environment

Set the following environment variables:

```bash
# For Linux/macOS
export GOPROXY=export GOPROXY="https://username:password@arti-server/artifactory/api/go/alex-go",direct

# For Windows
set GOPROXY=https://username:password@arti-server/artifactory/api/go/go,direct
set GOSUMDB=off
```

### 2. Configure JFrog CLI

```bash
# Configure Artifactory
jf c add artifactory

# Follow the prompts to enter:
# - Server ID: artifactory
# - Artifactory URL: https://<your-artifactory-url>
# - Username: <your-username>
# - Password/API Key: <your-password-or-api-key>
```

## Building

### 1. Build the Project

```bash
# Build the project
jf rt go build --build-name vulnerable-go-project --build-number 1
```

## Publishing

### 1. Configure Go Module

In your `go.mod` file, ensure the module name follows the pattern:

```go
module github.com/your-org/your-repo
```

### 2. Publish to Artifactory

```bash
# Publish the module
 jf gp v1.0.0 --build-name=vulnerable-go-project --build-number=3  

# This will:
# 1. Build the project
# 2. Publish the module to Artifactory
```

### 3. Verify Publication

Check the published module in Artifactory:
1. Go to Artifactory UI
2. Navigate to your Go repository
3. Verify the module is published with correct version

## Consuming the Module

Other projects can consume your published module by:

1. Setting the GOPROXY environment variable
2. Using `go get`:

```bash
go get github.com/your-org/your-repo@v1.0.0
```

## References

- [JFrog Go Documentation](https://docs.jfrog-applications.jfrog.io/jfrog-applications/jfrog-cli/binaries-management-with-jfrog-artifactory/package-managers-integration#building-go-packages)
