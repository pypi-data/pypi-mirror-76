import __main__


def get_version_generic(project_type):
    retrieve_ver_command = ''
    retrieve_ver_command2 = ''
    ## check type of project
    if project_type == 'npm':
        retrieve_ver_command  = "grep 'version'\s*:\s* package.json"
    if project_type == 'android':
        retrieve_ver_command1 = "grep 'versionCode\s app/build.gradle"
        retrieve_ver_command2 = "grep 'versionName\s app/build.gradle"
    if project_type == 'flutter':
        retrieve_ver_command = "grep 'version\s*:\s*' pubspec.yaml"
    if project_type == 'net':
        retrieve_ver_command = ''
    if project_type == 'netcore':
        retrieve_ver_command = ''        
         
    
def change_manifest():
    ## Retreive version number manifest
    ## grep "version\s*=\s*" manifest.yml  ## To-do Refactor to use this 
    
    ## check if manifest.yml exist
    sed_command_manifest = "sed -i 's/version: {}/version: {}/g' ./manifest.yml".format(version.rstrip(), new_version)
 
    ## update version number in manifest.yml
    process_sed_manifest = __main__.subprocess.Popen(sed_command_manifest, shell=True, stdout=__main__.subprocess.PIPE, cwd=path)

def modify_version():
    if __main__.arch_type == 'npm':
        major = 0
        minor = 0
        patch = 0 
        build = 0
        new_version = ''
        version_format = ''
        ## Update version number in package.json
        print("Architecture: React, Angular, Node, NPM")
        path = __main__.os.path.abspath(__main__.os.getcwd())    
        print("Working directory: ",path)
        ##version = subprocess.run(["node -p \"require('./package.json').version\""], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=path)
        ##version = subprocess.run(["echo 1.0.1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=path)
        process_result = __main__.subprocess.Popen("node -p \"require('./package.json').version\"", shell=True, stdout=subprocess.PIPE, cwd=path)
        version_result = process_result.communicate()[0]
        version = str(version_result, 'utf-8')
        version_lst = version.rstrip().split(".")
        if (len(version_lst) == 4):
            version_format = "modified"
            major, minor, patch, build = version_lst
        else:
            version_format = "standard"
            major, minor, patch = version_lst
            
        if __main__.change_type == "major":
            major = int(major) + 1
            if version_format == "standard":
                minor = 0
                patch = 0
            else:
                minor = 0
                patch = 0
                build = 0         
            
        if __main__.change_type == "minor":    
            minor = int(minor) + 1  
            patch = 0
            if version_format != "standard":
                build = 0
        if __main__.change_type == "patch":
            patch = int(patch) + 1
            if version_format != "standard":
                build = 0
        if __main__.change_type == "build":
            build = int(build) + 1
        
        if version_format == "standard":
            new_version = str(major) + '.' + str(minor) + '.' + str(patch)
        else:
            new_version = str(major) + '.' + str(minor) + '.' + str(patch) + '.' + str(build)
            
        
        git_checkout_command = "git checkout -b feature/modify-version"
        process_git_checkout = __main__.subprocess.Popen(git_checkout_command, shell=True, stdout=__main__.subprocess.PIPE, cwd=path)
        print("Checkout result: ", process_git_checkout.communicate()[0])
        
        ## update version number in package.json
        sed_command = "sed -i 's/\"version\": \"{}\"/\"version\": \"{}\"/g' ./package.json".format(version.rstrip(), new_version)
        ## print('SED command: ', sed_command)
        
        process_sed = __main__.subprocess.Popen(sed_command, shell=True, stdout=__main__.subprocess.PIPE, cwd=path)
        
        change_manifest()  ## Update manifest file
    
        print("Previous version: ", version.rstrip(), "  New Version:: ", new_version, "   Type: ", __main__.change_type)
        
        return sys.exit(0)
  
    elif __main__.arch_type == 'springboot':
        print("Architecture: Springboot: Java")
        change_manifest()  ## Update manifest file
        ## update version number in package.json
        sed_buildgradle_command = "sed -i 's/\"version\": \"{}\"/\"version\": \"{}\"/g' ./build.gradle".format(version.rstrip(), new_version)
        ## print('SED command: ', sed_command)
        process_sed = __main__.subprocess.Popen(sed_buildgradle_command, shell=True, stdout=__main__.subprocess.PIPE, cwd=path)
        
        return sys.exit(0)
    elif __main__.arch_type == 'dotnet':
        print("Architecture: .NET")
        return sys.exit(0)
    else: 
        print("Error: Cannot parse command")
        return sys.exit()