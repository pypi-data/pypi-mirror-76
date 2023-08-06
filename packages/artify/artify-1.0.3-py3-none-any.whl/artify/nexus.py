import __main__

def get_version_number():
    path = __main__.os.path.abspath(__main__.os.getcwd())
    ##make provision to get version number from java type project
    process_result = __main__.subprocess.Popen("node -p \"require('./package.json').version\"", shell=True, stdout=__main__.subprocess.PIPE, cwd=path)
    version_result = process_result.communicate()[0]
    return str(version_result, 'utf-8')


def upload_nexus_raw():
    params = (('repository', __main__.repository_name),)
	
    finalpath = __main__.work_directory + '/' + __main__.artifact_name
    print("Uploading to Nexus Repository: "+ __main__.repository_name)
    files = {

	  'raw.directory' : (None, __main__.directory),
	  'raw.asset1' : (None, finalpath),
	  'raw.asset1.filename': (None, __main__.artifact_name)
    }
	#raw.assetN : (None, 
	#raw.assetN.filename
    #response = requests.post("http://localhost:8081/service/rest/v1/components",params=params, files=files, auth=auth)
    response = __main__.requests.post(url=__main__.repository_full_url, params=params, files=files, proxies=__main__.proxies, auth=__main__.auth)
    if response.status_code == 204:
        print("Nexus Upload successful")
        return __main__.sys.exit(0)
    elif response.status_code == 400 and ("release" in __main__.repository_name or "staging" in __main__.repository_name):
        print("Nexus Upload failed. Please modify version number")
        return __main__.sys.exit(1)
    else:
        print("Nexus Upload failed")
        return __main__.sys.exit(1)
    print("Status code: ", response.status_code)

def upload_nexus_npm():
    params = (('repository', __main__.repository_name),)
    finalpath = __main__.work_directory + '/' + __main__.artifact_name
    files = {
	  'npm.asset' : (None, finalpath),
    }
    response = requests.post(url=__main__.repository_full_url, params=params, files=files, proxies=__main__.proxies, auth=__main__.auth)
    if response.status_code == 204:
        print("Nexus Upload successful")
        return __main__.sys.exit(0)
    else:
        print("Nexus Upload failed")
        return __main__.sys.exit(1)
    print("Status code: ", response.status_code)

def upload_nexus_maven():
    actual_artifact_name = ''
    
    params = (('repository', __main__.repository_name),)
   
    finalpath = __main__.work_directory + '/' + __main__.artifact_name
    
    if ('tar.gz' in __main__.artifact_name):
        pass
    
    longname, file_extension = __main__.os.path.splitext(__main__.artifact_name)
    
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
        'maven2.groupId': (None, __main__.group_id),
        'maven2.artifactId': (None, actual_artifact_name),
        'maven2.version': (None, versionnumber),
        'maven2.asset1': ( __main__.artifact_name, open(finalpath, 'rb')),
        'maven2.asset1.extension': (None, extension),
        'maven2.generate-pom': (None, True) 
    }

    response = __main__.requests.post(url=__main__.repository_full_url, params=params, files=files, auth=__main__.auth, proxies=__main__.proxies, verify=False)
    if response.status_code == 204:
        print("Nexus Upload successful")
        return __main__.sys.exit(0)
    elif response.status_code == 400 and ("release" in __main__.repository_name or "staging" in __main__.repository_name):
        print("Nexus Upload failed. Please modify version number")
        return __main__.sys.exit(1)
    else:
        print("Nexus Upload failed")
        print("Status code: ", response.status_code)
        return __main__.sys.exit(1)
