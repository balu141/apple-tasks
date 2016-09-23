HOW TO WORK WITH THE ARTIFACTORY ARTIFACTS USING JFROG CLI

==========================================================================================

How to install jfrog cli :-

curl -fL https://getcli.jfrog.io | sh

==========================================================================================

How to authenticate yourself :-

If Password encryption policy is "required" (Under Security -> General Configuration ),

then you need to authenticate with your API key

jfrog rt c --url=${ARTL_URL} --user=${ARTIFACTORY_USER} --apikey=${ARTL_API_KEY}

==========================================================================================

Examples to upload artifacts to Artifactory :-

------------------------------------------------------------------------------------------

1. Collect artifacts having .jar extension in current and sub-folders and upload to Artifactory

onto the target project/component folder( default recursive is true ).

> jfrog rt u "*.jar" internal-devops-maven-local/helloOnboarding

------------------------------------------------------------------------------------------

2. Collect artifacts having .jar extension in only current directory and upload to Artifactory

onto the target project/component folder.

> jfrog rt u "*.jar" internal-devops-maven-local/helloOnboarding --recursive=false

------------------------------------------------------------------------------------------

3. For each .jar in the source directory, upload the artifact to a corresponding target directory

with the same name

For eg. a file called hello-onboarding.jar will be uploaded to

internal-devops-maven-local/hello-onboarding/hello-onboarding.jar

> jfrog rt u "(*).jar" internal-devops-maven-local/{1}/ --recursive=false

------------------------------------------------------------------------------------------

4. Upload artifact to the root folder of the repository

> jfrog rt u "*.jar" internal-devops-maven-local -recursive=false

------------------------------------------------------------------------------------------

5. Upload target artifact with a different name

For eg. hello-onboarding.jar from source directory will be uploaded as helloAgain.jar in the

target directory

> jfrog rt u "hello-onboarding.jar" internal-devops-maven-local/helloOnboarding/helloAgain.jar 
--recursive=false

------------------------------------------------------------------------------------------

6. Collect all the tar.gz bundles under the "tar_archives" directory (including sub-directories),

and upload them to the internal-devops-generic-local repository, under each file named sub folder,

while maintaining the original names of the artifacts.

For eg. Uploading artifact:

https://artl-iag.apple.com/artifactory/internal-devops-generic-local/internal-devops/internal-devops.tar.gz

> jfrog rt u "tar-archives/(*).tar.gz" internal-devops-generic-local/{1}/{1}.tar.gz

------------------------------------------------------------------------------------------

7. Add suffix to the target filenames

For eg. Uploading artifact:

https://artl-iag.apple.com/artifactory/internal-devops-generic-local/internal-devops/internal-devops-new.tar.gz

> jfrog rt u "tar-archives/(*).tar.gz" internal-devops-generic-local/{1}/{1}-new.tar.gz

------------------------------------------------------------------------------------------

8. Collect "*.tar.gz" artifacts recursively and upload them to target repository with maintaining the original

name and folders

For eg.

Uploading artifact: 
https://artl-iag.apple.com/artifactory/internal-devops-generic-local/tarfiles/.m2/repository/com/sampleMaven/internal-devops/hello-onboarding/1.1.2/hello-onboarding-1.1.2-bin.tar.gz

> jfrog rt u "(*).tar.gz" internal-devops-generic-local/tarfiles/{1}.tar.gz

------------------------------------------------------------------------------------------

9. Upload all files in the current directory to the target repository and place them in directories which match their file extensions.

> jfrog rt u "(*).(.*)" internal-devops-generic-local/{2}/{1}.{2} --recursive=false

------------------------------------------------------------------------------------------

==========================================================================================


Examples to download artifacts from Artifactory :-

------------------------------------------------------------------------------------------

1. Download all artifacts from the root of the given repository

> jfrog rt dl apg-docker-local

Output like below -

Pinging Artifactory...
Searching Artifactory using AQL query: items.find({"repo": "apg-docker-local","$or": [{"$and": [{"path": {"$match":"*"},"name":{"$match":"*"}}]}]}).include("name","repo","path","actual_md5","actual_sha1","size")
Artifactory response: 200 OK
[Thread 2] Artifactory response: 200 OK
[Thread 0] Artifactory response: 200 OK
[Thread 1] Artifactory response: 200 OK
[Thread 2] [2]: 206 Partial Content...
[Thread 2] [1]: 206 Partial Content...
[Thread 2] [0]: 206 Partial Content...
[Thread 0] [1]: 206 Partial Content...
[Thread 0] [0]: 206 Partial Content...
[Thread 0] [2]: 206 Partial Content...
[Thread 1] [0]: 206 Partial Content...
[Thread 1] [2]: 206 Partial Content...
[Thread 1] [1]: 206 Partial Content...
[Thread 2] Done downloading.
[Thread 2] [2]: 206 Partial Content...
[Thread 2] [1]: 206 Partial Content...
[Thread 2] [0]: 206 Partial Content...
[Thread 0] Done downloading.
[Thread 0] Artifactory response: 200 OK
[Thread 0] Artifactory response: 200 OK
[Thread 1] Done downloading.
[Thread 1] Artifactory response: 200 OK
[Thread 1] Artifactory response: 200 OK
[Thread 2] Done downloading.
Downloaded 11 artifacts from Artifactory.

------------------------------------------------------------------------------------------

2. Download a specific artifact from the given repository

> jfrog rt dl internal-devops-generic-local/brew_test.log

Output like below -

Pinging Artifactory...
[Thread 0] : Artifactory response: 200 OK

------------------------------------------------------------------------------------------

3. Use regex to download matching files from the given repository

> jfrog rt dl internal-devops-generic-local/"brew*".log

Output like below -

Pinging Artifactory...
Searching Artifactory using AQL query: items.find({"repo": "internal-devops-generic-local","$or": [{"$and": [{"path": {"$match":"."},"name":{"$match":"brew*.log"}}]},{"$and": [{"path": {"$match":"brew*"},"name":{"$match":"*.log"}}]}]}).include("name","repo","path","actual_md5","actual_sha1","size")
Artifactory response: 200 OK
[Thread 1] Artifactory response: 200 OK
[Thread 0] Artifactory response: 200 OK
Downloaded 2 artifacts from Artifactory.

------------------------------------------------------------------------------------------

4. Download all the artifacts from internal-devops-generic-local/testlog into testlog in the current directory

> jfrog rt dl internal-devops-generic-local/testlog/

Output like below -

Pinging Artifactory...
Searching Artifactory using AQL query: items.find({"repo": "internal-devops-generic-local","$or": [{"$and": [{"path": {"$match":"testlog"},"name":{"$match":"*"}}]},{"$and": [{"path": {"$match":"testlog/*"},"name":{"$match":"*"}}]}]}).include("name","repo","path","actual_md5","actual_sha1","size")
Artifactory response: 200 OK
[Thread 0] Artifactory response: 200 OK
Downloaded 1 artifacts from Artifactory.

------------------------------------------------------------------------------------------

5. Do dry run and check what files would be downloaded. 

> jfrog rt dl internal-devops-generic-local/testlog/ --dry-run

Output like below -

Searching Artifactory using AQL query: items.find({"repo": "internal-devops-generic-local","$or": [{"$and": [{"path": {"$match":"testlog"},"name":{"$match":"*"}}]},{"$and": [{"path": {"$match":"testlog/*"},"name":{"$match":"*"}}]}]}).include("name","repo","path","actual_md5","actual_sha1","size")
Artifactory response: 200 OK
[Thread 0] [Dry run] Downloading https://artl-iag.apple.com/artifactory/internal-devops-generic-local/testlog/brew_test_data.txt
Downloaded 1 artifacts from Artifactory.

------------------------------------------------------------------------------------------


==========================================================================================

Examples to copy  artifacts in Artifactory :-

------------------------------------------------------------------------------------------

1. Copy all artifacts located under /testdata in the source repository into the same path

in the target repository.

> jfrog rt cp internal-devops-generic-local/testdata zaos-generic-local/testdata

Output like below -

Pinging Artifactory...
Copying artifact: internal-devops-generic-local/testdata to zaos-generic-local/testdata
Artifactory response: 200 OK

------------------------------------------------------------------------------------------

2. Copy all artifacts located under /testdata in the source repository into a different path

in the target repository.

> jfrog rt cp internal-devops-generic-local/testdata zaos-generic-local/test_newdata

Output like below -

Pinging Artifactory...
Copying artifact: internal-devops-generic-local/testdata to zaos-generic-local/test_newdata
Artifactory response: 200 OK

------------------------------------------------------------------------------------------

3. Copy only *.gz artifacts to the target repository under different sub folder

> jfrog rt cp internal-devops-generic-local/testdata/"*.gz" zaos-generic-local/test_newdata/

Pinging Artifactory...
Searching Artifactory using AQL query: items.find({"repo": "internal-devops-generic-local","$or": [{"$and": [{"path": {"$match":"testdata"},"name":{"$match":"*.gz"}}]},{"$and": [{"path": {"$match":"testdata/*"},"name":{"$match":"*.gz"}}]}]}).include("name","repo","path","actual_md5","actual_sha1","size")
Artifactory response: 200 OK
Copying artifact: internal-devops-generic-local/testdata/internal-devops.tar.gz to zaos-generic-local/test_newdata/testdata/internal-devops.tar.gz
Artifactory response: 200 OK
Copied 1 artifacts in Artifactory

------------------------------------------------------------------------------------------

==========================================================================================

Examples to move artifacts in Artifactory :-

------------------------------------------------------------------------------------------

1. Move all artifacts from the source sub folder to the same target sub folder between the

source and the target repository

> jfrog rt mv internal-devops-generic-local/test_tar/ zaos-generic-local/

Output like below -

Pinging Artifactory...
Searching Artifactory using AQL query: items.find({"repo": "internal-devops-generic-local","$or": [{"$and": [{"path": {"$match":"test_tar"},"name":{"$match":"*"}}]},{"$and": [{"path": {"$match":"test_tar/*"},"name":{"$match":"*"}}]}]}).include("name","repo","path","actual_md5","actual_sha1","size")
Artifactory response: 200 OK
Moving artifact: internal-devops-generic-local/test_tar/internal-devops.tar.gz to zaos-generic-local/test_tar/internal-devops.tar.gz
Artifactory response: 200 OK
Moved 1 artifacts in Artifactory

------------------------------------------------------------------------------------------

2. Move only *.gz artifacts between the repositories under same sub folder

> jfrog rt mv internal-devops-generic-local/test_tar/"*.gz" zaos-generic-local/

Output like below -

Pinging Artifactory...
Searching Artifactory using AQL query: items.find({"repo": "internal-devops-generic-local","$or": [{"$and": [{"path": {"$match":"test_tar"},"name":{"$match":"*.gz"}}]},{"$and": [{"path": {"$match":"test_tar/*"},"name":{"$match":"*.gz"}}]}]}).include("name","repo","path","actual_md5","actual_sha1","size")
Artifactory response: 200 OK
Moving artifact: internal-devops-generic-local/test_tar/internal-devops.tar.gz to zaos-generic-local/test_tar/internal-devops.tar.gz
Artifactory response: 200 OK
Moved 1 artifacts in Artifactory

------------------------------------------------------------------------------------------

==========================================================================================


Examples to delete artifacts in Artifactory :-

------------------------------------------------------------------------------------------

1. Delete all the artifacts under  testlog under the root of the repository

> jfrog rt del internal-devops-generic-local/testlog

Output like below -

Delete path internal-devops-generic-local/testlog? (y/n): y
Pinging Artifactory...
Deleting: https://artl-iag.apple.com/artifactory/internal-devops-generic-local/testlog
Artifactory response: 204 No Content

------------------------------------------------------------------------------------------

2. Delete only .log files under the root of the repository

> jfrog rt del internal-devops-generic-local/"*.log"

Output like below -

Delete path internal-devops-generic-local/*.log? (y/n): y
Pinging Artifactory...
Searching Artifactory using AQL query: items.find({"repo": "internal-devops-generic-local","$or": [{"$and": [{"path": {"$match":"."},"name":{"$match":"*.log"}}]},{"$and": [{"path": {"$match":"*"},"name":{"$match":"*.log"}}]}]}).include("name","repo","path","actual_md5","actual_sha1","size")
Artifactory response: 200 OK
Deleting: https://artl-iag.apple.com/artifactory/internal-devops-generic-local/brew.log
Artifactory response: 204 No Content
Deleting: https://artl-iag.apple.com/artifactory/internal-devops-generic-local/brew_test.log
Artifactory response: 204 No Content

------------------------------------------------------------------------------------------

3. Delete all the artifacts under the root of the repository

> jfrog rt del internal-devops-generic-local

Output like below -

Delete path internal-devops-generic-local? (y/n): y
Pinging Artifactory...
Searching Artifactory using AQL query: items.find({"repo": "internal-devops-generic-local","$or": [{"$and": [{"path": {"$match":"*"},"name":{"$match":"*"}}]}]}).include("name","repo","path","actual_md5","actual_sha1","size")
Artifactory response: 200 OK
Deleting: https://artl-iag.apple.com/artifactory/internal-devops-generic-local/internal-devops.tar.gz
Artifactory response: 204 No Content

------------------------------------------------------------------------------------------

4. Delete all the artifacts unnder subfolder matching test* under the root repository

> jfrog rt del internal-devops-generic-local/"test*"

Output like below -

Delete path internal-devops-generic-local/test*? (y/n): y
Pinging Artifactory...
Searching Artifactory using AQL query: items.find({"repo": "internal-devops-generic-local","$or": [{"$and": [{"path": {"$match":"."},"name":{"$match":"test*"}}]},{"$and": [{"path": {"$match":"test*"},"name":{"$match":"*"}}]}]}).include("name","repo","path","actual_md5","actual_sha1","size")
Artifactory response: 200 OK
Deleting: https://artl-iag.apple.com/artifactory/internal-devops-generic-local/testdata/internal-devops.tar.gz
Artifactory response: 204 No Content
Deleting: https://artl-iag.apple.com/artifactory/internal-devops-generic-local/testfiles/internal-devops.tar.gz
Artifactory response: 204 No Content
Deleting: https://artl-iag.apple.com/artifactory/internal-devops-generic-local/test_tar/internal-devops.tar.gz
Artifactory response: 204 No Content

------------------------------------------------------------------------------------------

==========================================================================================












