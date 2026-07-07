# {{PROJECT_NAME}} application configuration
# Application configuration only. Business configuration lives in the database.

app:
  name: "{{PROJECT_NAME}}"
  version: "{{VERSION}}"
  env: development

database:
  url: "sqlite:///labaps.db"

api:
  prefix: "/api/v1"
  host: "127.0.0.1"
  port: 5000
