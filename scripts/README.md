## retrieve the list of all repositories in nexus 


```
curl -k https://nexus:9443/nexus/service/local/all_repositories -u admin:admin123
```

#### Retrive all Roles in nexus

```
curl -k https://nexus:9443/nexus/service/local/roles -u admin:admin123  
```

#### To Get Status of the nexus 

```
curl https://nexus:9443/nexus/service/local/status -u admin:admin123  
```

#### To Get available Users

```
curl -k https://nexus:9443/nexus/service/local/users -u admin:admin123
```

#### To Get Available Repositories

```
curl -k https://nexus:9443/nexus/service/local/repositories -u admin:admin123
```

#### To Retrieve account details
```
curl -k https://nexus:9443/nexus/service/local/user_account/admin -u admin:admin123
```

#### To create new user in nexus 
```
[vagrant@nexus ~]$ cat new_user.xml
<?xml version="1.0" encoding="UTF-8"?>
<user-request>
  <data>
    <userId>master</userId>
    <email>master@gmail.com</email>
    <status>active</status>
    <firstName>mind</firstName>
    <resourceURI>https://nexus:9443/nexus/service/local/roles/repository-any-full</resourceURI>
    <roles>
      <role>npm-all-view</role>
    </roles>
    <lastName>minder</lastName>
    <password>test123</password>
  </data>
</user-request>

Run the command for creating the new user as follows: 

curl -i -H "Accept: application/xml" -H "Content-Type: application/xml; charset=UTF-8"  -v -d "@new_user.xml" -u admin:admin123 https://nexus:9443/nexus/service/local/users

```
#### To create a Proxy repository using rest api. 
```
[vagrant@nexus ~]$ cat repo.json
{
    "data": {
        "repoType": "proxy",
        "id": "somerepo",
        "name": "Some Repo Name",
        "browseable": true,
        "indexable": true,
        "notFoundCacheTTL": 1440,
        "artifactMaxAge": -1,
        "metadataMaxAge": 1440,
        "itemMaxAge": 1440,
        "repoPolicy": "RELEASE",
        "provider": "maven2",
        "providerRole": "org.sonatype.nexus.proxy.repository.Repository",
        "downloadRemoteIndexes": true,
        "autoBlockActive": true,
        "fileTypeValidation": true,
        "exposed": true,
        "checksumPolicy": "WARN",
        "remoteStorage": {
            "remoteStorageUrl": "https://nexus:9091/local",
            "authentication": null,
            "connectionSettings": null
        }
    }
}


Run the command for creating the Proxy repository as follows : 

curl -k -H "Content-Type: application/json" -X POST -d @repo.json -u admin:admin123 https://nexus:9443/nexus/service/local/repositories

```

#### To create a Hosted Repository 

```
[vagrant@nexus ~]$ cat sample.xml
<?xml version='1.0' encoding='UTF-8'?>
<repository>
<data>
<id>my-release-new-xml</id>
<name>samplejava-release</name>
<exposed>true</exposed>
<repoType>hosted</repoType>
<repoPolicy>RELEASE</repoPolicy>
<providerRole>org.sonatype.nexus.proxy.repository.Repository</providerRole>
<provider>maven2</provider>
<format>maven2</format>
</data>
</repository>


Run the command for creating the hosted repository in nexus as follows: 

curl -k -i -H "Accept: application/xml" -H "Content-Type: application/xml" -X POST -v trace-ascii -d "@sample.xml" -u admin:admin123 https://nexus:9443/nexus/service/local/repositories
```

### command to retrieve the latest version of the artifact from snapshot repository
```
wget --user=aos-readonly --password=wiYNPtaJ/uD7N/lBXUtQAHmtw7kUp7a8jm9beyIiCx8H "https://retail-nexus.apple.com/nexus/service/local/artifact/maven/redirect?r=snapshots&g=com.apple.store.application&a=Cider&v=LATEST" --content-disposition

Specify the group id and artifactid of the artifact to retrieve.
```

### command to retrieve the latest version of the artifact from release repository 
```
wget --user=aos-readonly --password=wiYNPtaJ/uD7N/lBXUtQAHmtw7kUp7a8jm9beyIiCx8H "https://retail-nexus.apple.com/nexus/service/local/artifact/maven/redirect?r=releases&g=com.apple.store.application&a=Cider&v=LATEST" --content-disposition

Specify the group id and artifactid of the artifact
```
