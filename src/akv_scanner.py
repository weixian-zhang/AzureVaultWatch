
from azure.identity import DefaultAzureCredential
from azure.keyvault.certificates import CertificateClient

class AKVScanner:

    def __init_subclass__(cls) -> None:
        pass

    