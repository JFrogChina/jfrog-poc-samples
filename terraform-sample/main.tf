terraform {
  required_providers {
    artifactory = {
      source  = "jfrog/artifactory"
      version = "12.10.0"
    }
    platform = {
      source  = "jfrog/platform"
      version = "2.2.6"
    }
  }
}

# 从环境变量 JFROG_URL/JFROG_ACCESS_TOKEN 读取
provider "artifactory" {
  url          = var.artifactory_url != "" ? var.artifactory_url : var.platform_url
  access_token = var.access_token
}

provider "platform" {
  url          = var.platform_url
  access_token = var.access_token
}

# 示例：创建一个本地通用仓库
resource "artifactory_local_generic_repository" "worker_generic_local" {
  key = "worker-generic-alex-local"
}
# 可选：把 URL/Token 做成变量，优先环境变量

resource "platform_group" "my-group" {
  name = "my-group-member-alex"
  description = "My group alex"
  external_id = ""
  auto_join = true
  admin_privileges = false
}


variable "platform_url" {
  type    = string
  default = ""
}

variable "artifactory_url" {
  type    = string
  default = ""
}

variable "access_token" {
  type      = string
  sensitive = true
  default   = ""
}
