## upload.py
import os
import __main__
import sys


def upload_maven():
    """Upload artifact to Maven 2 repository"""
    params = (('repository', __main__.repository),)
   
    finalpath = __main__.path + '/' + __main__.artifact_name
    
    if ('tar.gz' in __main__.artifact_name):
        pass
    
    longname, file_extension = os.path.splitext(__main__.artifact_name)
    
    artname_lst = __main__.artifact_name.split("-", 10)
    
    if file_extension == '.war':
        versionnumber = artname_lst[-2]
        extension = 'war'
        actual_artifact_name = '-'.join(artname_lst[:-2])
    elif file_extension == '.zip':
        versionnumber = artname_lst[-1].strip(file_extension)
        extension = 'zip'
        actual_artifact_name = '-'.join(artname_lst[:-1])
    else:
        extension = file_extension[1:]
        versionnumber = artname_lst[-1]
        actual_artifact_name = '-'.join(artname_lst[:-1])


    files = {
        'maven2.groupId': (None, __main__.directory),
        'maven2.artifactId': (None, actual_artifact_name),
        'maven2.version': (None, versionnumber),
        'maven2.asset1': (__main__.artifact_name, open(finalpath, 'rb')),
        'maven2.asset1.extension': (None, extension),
        'maven2.generate-pom': (None, True)  ## dont know if this will work
    }

    response = __main__.requests.post(__main__.url, params=params, files=files, auth=__main__.auth, proxies=__main__.proxies, verify=False)
    if response.status_code == 204:
        print("Nexus Upload successful")
        return sys.exit(0)
    elif response.status_code == 400 and ("release" in __main__.repository or "staging" in __main__.repository):
        print("Nexus Upload failed. Please modify version number")
        return sys.exit(1)
    else:
        print("Nexus Upload failed")
        return sys.exit(1)
    print("Status code: ",response.status_code)



def upload_npm():
    """Upload artifact to NPM type repository"""
    params = (('repository', __main__.repository),)
    finalpath = __main__.path + '/' + __main__.artifact_name
    files = {
	  'npm.asset' : (None, finalpath),
    }
    response = requests.post(__main__.url, params=params, files=files, auth=__main__.auth)
    if response.status_code == 204:
        print("Nexus Upload successful")
        return sys.exit(0)
    else:
        print("Nexus Upload failed")
        return sys.exit(1)
    print("Status code: ",response.status_code)



def upload_raw():
    """Upload artifact to RAW type repository"""
    params = (('repository', __main__.repository),)
	
    finalpath = __main__.path + '/' + __main__.artifact_name
    print("Uploading to Nexus Repository: "+ __main__.repository)
    files = {

	  'raw.directory' : (None, __main__.directory),
	  'raw.asset1' : (None, finalpath),
	  'raw.asset1.filename': (None, __main__.artifact_name)
    }
	#raw.assetN : (None, 
	#raw.assetN.filename
    #response = requests.post("http://localhost:8081/service/rest/v1/components",params=params, files=files, auth=auth)
    response = requests.post(__main__.url, params=params, files=files, auth=__main__.auth)
    if response.status_code == 204:
        print("Nexus Upload successful")
        return sys.exit(0)
    elif response.status_code == 400 and ("release" in __main__.repository or "staging" in __main__.repository):
        print("Nexus Upload failed. Please modify version number")
        return sys.exit(1)
    else:
        print("Nexus Upload failed")
        return sys.exit(1)
    print("Status code: ",response.status_code)

