# Azure VaultWatch  
<span style="font-size:0.4em;color:blue">*Inspired and donated by Project Beacon*</span>

Azure Vault Watch detects expiring Certificates, Keys and Secrets from multiple Key Vaults across subscriptions within a single tenant.  
Upon detection, VaultWatch also supports sending an email containing HTML-formated report on expiring objects.  

<br > 

## Features 
* Detects expiring Key Vault Keys, Secrets and Certs objects from multiple Key Vaults across subscriptions within a single tenant.
* The duration of expiration detetction can be configured with environment variable NUM_OF_DAYS_NOTIFY_BEFORE_EXPIRY
* Notify once - When one or more expiring objects are detected an email notification will be sent. To prevent spam-send, user can configure environment variable NUM_OF_DAYS_TO_RENOTIFY_EXPIRING_ITEMS with a large number of days. Conversely, if user wants to receive email notification frequently e.g every 3 days, user can set  NUM_OF_DAYS_TO_RENOTIFY_EXPIRING_ITEMS=3.
* Provides a HTTP endpoint */api/objects/expire/v1* for monitoring clients like Grafana, to retrieve expiring objects as Json data
* Supports [container](https://hub.docker.com/r/wxzd/azurevaultwatch) deployment, <code>docker pull wxzd/azurevaultwatch</code>
* Supports sending email to any SMTP server by configuring environment variable SMTP_CONFIG in [How to Deploy](#how-to-deploy).  
  * able to send to multiple email addresses  
  (Example below using [Azure Communication Service SMTP Support](https://learn.microsoft.com/en-us/azure/communication-services/concepts/email/email-smtp-overview))
* customizable Jinja2 template used to render HTML report in email
  ![image](https://github.com/user-attachments/assets/7263183c-8079-40b1-98ad-b2eee7d2fd05)
* App uses OpenTelemetry Trace to trace Azure API calls and exports to Application Insights, for performance monitoring and ease of troubleshooting

<br >

## Architecture Design  
![image](https://github.com/user-attachments/assets/271da0bb-76fa-4500-b89e-159774f8d42a)




<br >  

## How to Deploy

* Supports container deployment from [Docker Hub](https://hub.docker.com/r/wxzd/azurevaultwatch)
* For Kubernetes deployment, see [here](https://github.com/weixian-zhang/AzureVaultWatch/tree/main/infra-as-code/kubernetes)
* Dependent Azure Services
  * Azure Storage Table - leverage as persistent storage to save vault object versions that were previously had notifications sent, to prevent spam sending notifications until the configured NUM_OF_DAYS_TO_RENOTIFY_EXPIRING_ITEMS is reached
  * Managed identity VaultWatch container image can be hosted on App Service or [Workload Identity](https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview?tabs=dotnet) if hosting in AKS
    * RBAC - managed identity or workload identity (which is a user assigned managed identity)
      * with Key Vault Reader role assigned to 1 or more Subscriptions, Resource Group or Key Vault level
      * with Storage Table Data Contributor role assgined to Azure Storage
  * Azure Application Insights - VaultWatch uses [OpenTelemtry](https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable?tabs=aspnetcore) Tracing for monitoring calls to various Azure management APIs including Subscription and Key Vault APIs. Due to these HTTP dependencies, it is important to monitor the performance and error when call them
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
    "subject": "Azure Key Vault Expiring Objects",
    "senderAddress": "DoNotReply@674edb48-246c-4119-ac71-7eabf6c96aa5.azurecomm.net",
    "to": ["weixzha@microsoft.com"],
    "cc": []</code>  
  APP_INSIGHTS_CONN_STRING='app insights connection string'
