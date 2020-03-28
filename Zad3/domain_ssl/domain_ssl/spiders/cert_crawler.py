import scrapy #2.0 version
import pymongo
from cryptography.hazmat.primitives import serialization

#docs: https://docs.scrapy.org/en/latest/topics/practices.html
#https://cryptography.io/en/latest/hazmat/primitives/asymmetric/serialization

#TODO: write comments about PEM,DER and PKCS1,SubjectPublicKeyInfo
class CertSpider(scrapy.Spider):
    name = "cert_crawler"

    def __init__(self):
        db=pymongo.MongoClient('mongodb://localhost:27017')
        self.certs=db['crypto']['certs']

        self.certs.create_index([('url',1)],unique=True)
        self.certs.create_index([('keyHash',1)])



    def start_requests(self):
        urls = [
            'https://google.pl',
            'https://wykop.pl'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if not self.certs.find_one({'url':response.url}):
            cert=response.certificate
            
            doc={'url':response.url}
            doc['cert_PEM']=cert.dumpPEM()
            doc['keyHash']=cert.getPublicKey().keyHash() 

            #OpenSSL.crypto.PKey
            pkey=cert.original
            pub_key=pkey.get_pubkey()

            doc['bits']=pub_key.bits()
            doc['is_only_pub']=pub_key._only_public
            #specific cast
            pub_key=pub_key.to_cryptography_key()
            doc['key_type']=str(type(pub_key))
            doc['key_PEM']=pub_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo).decode('utf-8')
            if "RSA" in doc['key_type']:
                doc['rsa_PEM']=pub_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.PKCS1).decode('utf-8')

            #save to db
            self.certs.insert_one(doc)


