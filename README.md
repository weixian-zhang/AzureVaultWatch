# AzureVaultWatch  

Azure Vault Watch supports detecting expiring Certificates, Keys and Secrets from multiple Key Vaults across subscriptions within a single tenant.  
Upon detection, VaultWatch also supports sending an email containing HTML-formated report on expiring objects.  


### Features 
* Detect expiring Key Vault Keys, Secrets and Certs objects from multiple Key Vaults across subscriptions within a single tenant. 
* Send once only - When an object is detected to be expiring, app sends the email report once only.
* Supports HTTP endpoint to retrieve expiring objects as Json data to support monitoring clients e.g: Grafana
* Supports container deployment


### How to Deploy

* Supports container deployment from [Docker Hub](https://hub.docker.com/r/wxzd/azurevaultwatch)
* For Kubernetes deployment, see [here](https://github.com/weixian-zhang/AzureVaultWatch/tree/main/infra-as-code/kubernetes)
* Dependent Azure Services
  * Azure Storage Table - used as database to store vault object versions that has previously sent notifications, to prevent spam sending notifications until the configured NUM_OF_DAYS_TO_RENOTIFY_EXPIRING_ITEMS is reached
  *  Azure Application Insights - VaultWatch uses [OpenTelemtry](https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable?tabs=aspnetcore) Tracing for monitoring calls to various Azure management APIs including Subscription and Key Vault APIs. Due to these HTTP dependencies, it is important to monitor the performance and error when call them
* Environment Variables
  
  NUM_OF_DAYS_NOTIFY_BEFORE_EXPIRY=60    
  NUM_OF_DAYS_TO_RENOTIFY_EXPIRING_ITEMS=2  
  STORAGE_ACCOUNT_NAME='strgvaultwatch'  
  STORAGE_TABLE_NAME='NotifiedExpiringVersions'  
  SMTP_CONFIG=<code>{
    "host": "smtp.azurecomm.net",
    "port": 587,
    "username":"commsvc-apac-dev.b6df10d2-13d4-4026-a3f0-d78bb4bc3d0c.f9f26aa0-c90e-4431-add4-7749d97ba420",
    "password": "spn client secret is used by azure comm service email SMTP server as SMTP password",
    "subject": "Azure Key Vault Expiring Artifacts",
    "senderAddress": "DoNotReply@674edb48-246c-4119-ac71-7eabf6c96aa5.azurecomm.net",
    "to": ["weixzha@microsoft.com"],
    "cc": []</code>  
  APP_INSIGHTS_CONN_STRING='app insights connection string'
