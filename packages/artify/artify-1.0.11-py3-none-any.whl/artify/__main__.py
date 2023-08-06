import sys, getopt
import os
import requests
import base64
import json
from subprocess import Popen, PIPE


from artify import nexus
from artify import deploy
from artify import syncrepo
from artify import change_version

debug = 0;

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

proxies = {
  "http": None,
  "https": None,
}

# Variables - Nexus
nexus_format = ''
artifact_name = ''
work_directory = ''
repository_name = ''
nexus_format = ''
repository_base_url = ''
repository_full_url = ''
username = ''
password = ''
directory = ''
group_id = ''
auth = ''
# Variables - Nexus

# Variables - Deploy AWX
encoded_string = ''  
url = ''
debug = 0
# Variables - Deploy AWX


def main(argv):  
    print("Copyright \N{COPYRIGHT SIGN} 2020 Stewartium ::: artify v\n")
    action = ''
    
    ## Variables - Deploy AWX
    global encoded_string 
    global url
    global debug
    ## Variables - Deploy AWX
    
    ## Variables - Nexus
    global nexus_format 
    global artifact_name
    global work_directory
    global repository_name
    global nexus_format
    global repository_base_url
    global repository_full_url
    global username
    global password
    global directory
    global group_id
    global auth
    ## Variables - Nexus
    
    
    try:
        opts, args = getopt.getopt(argv, "a:b:c:d:h:f:m:n:u:p:r:g:t:w:", ["command=", "help", 
                                                "artifactname=", "repository=","groupid=", "directory=", "nexushost=",
                                                "file=", "awxhost=",
                                                "type=", "archtype=",
                                                "message=", "branch="
                                               ])
    except getopt.GetoptError:
        print('Invalid syntax')
        print('To get help, type syntax below: ')
        print('python -m artify --help')
        return sys.exit(2)
    
    for opt, arg in opts:
        if opt == "--help":
            if arg == "nexus":
                print("How to use Nexus Artifact Upload module\n")
                print("Usage: python -m artify -c nexus [OPTION] NEXUS_URL\n")
                print("Mandatory arguments: ")
                print("-f, --format    Nexus repository format e.g npm, maven, raw, nuget")
                print("-h, --nexushost   Nexus host base url e.g https://nexus.<yourcompany>.com")
                print("")
                print("Optional arguments i.e Some can be passed in the environment variables")
                print("-w, --workdirectory Working directory of artifact to be uploaded to Nexus repository")
                print("-n, --artifactname  Artifact name")
                print("-r, --repository    Nexus repository to upload to: e.g <repository>-snapshots")
                print("-g, --groupid       Group ID for Maven2 type repository")
                print("-d, --directory     Directory for RAW type repository")
                print("-u, --username      Username of nexus user")
                print("-p, --password      Password of nexus user")
                return sys.exit(0)
            elif arg == "deploy":
                print("How to deploy app to AWX infrastructure")
                print('python -m artify -c deploy -f <manifest> -h <awx_host>')
                print("Or")
                print("python -m artify --command deploy --file <manifest> --awxhost <awx_host>")
                return sys.exit(0)
            elif arg == "syncrepo":
                print('')
                print("How to Push and Commit changes\n")
                print("Usage: python -m artify -c syncrepo [OPTION] COMMIT_MESSAGE\n")
                print("Mandatory arguments: ")
                print("-m, --message     Commit message")
                print("\nOptional arguments: ")
                print("-h, --host        Repository url")
                return sys.exit(0)
            elif arg == "deltav":
                print('')
                print('python -m artify -c deltav -t <version_change> -a <architecture_type>')
                print("Or")
                print("python -m artify --command deltav --type <version_change> --archtype <architecture_type>")
                print("")
                print("e.g --archtype npm, dotnet, springboot ")
                print()
                print("e.g --type major    1.0.0.0 => 2.0.0.0")
                print("e.g --type minor    1.0.0.0 => 1.1.0.0")
                print("e.g --type patch    1.0.0.0 => 1.0.1.0")
                print("e.g --type build    1.0.0.0 => 1.0.0.1   Experimental")
                return sys.exit(0)
            else:
                print('python -m artify --help nexus        Help on how to deploy to Nexus Repository')
                print('python -m artify --help deploy       Help on how to deploy to AWX host')
                print('python -m artify --help syncrepo     Help on how to commit and push code to repository')
                print('python -m artify --help deltav      Help on how to change version number')
        elif opt in ("-c", "--command"):
            action = arg
            if action == '':
                print("Invalid command specified")
                return sys.exit(2)
        ## Deploy-artifact-awx-host params START
        elif opt in ("-f", "--file", "--format"):
            if action == 'nexus':
                nexus_format = arg
                if nexus_format == '':
                    print("Please specify nexus repository format e.g npm, maven, raw, nuget")
                    return sys.exit(2) 
            elif action == 'deploy':
                with open(arg, "rb") as manifest_file:
                    encoded_string = base64.b64encode(manifest_file.read())
            else:
                print("Invalid command specified: param: -f")
                     
        ## Deploy-artifact-awx-host params END
        
        ## Change-version-number params START
        elif opt in ("-t", "--type"):
            change_type = arg
            
        elif opt in ("-a", "--archtype"):
            arch_type = arg      
            
         ## Change-version-number params END
        
        ## Deploy-artifact-nexus params START
        ## -h 
        elif opt in ("-h", "--nexushost", "--awxhost"):
            if action == 'nexus':
                repository_base_url = arg
                if repository_base_url == '':
                    print("Nexus base url cannot be left blank")
                    return sys.exit(2)
            elif action == 'deploy':
                url = arg
            else:
                print("Invalid {} host specified".format(action))
                return sys.exit(2)
        ## -u
        elif opt in ("-u", "--username"):
            username = arg
            if username == '':
                print("Nexus username cannot be left blank")
        
        
        ## -p
        elif opt in ("-p", "--password"):
            password = arg
            if password == '':
                print("Nexus password cannot be left blank")
                return sys.exit(2)
        
        ## -d 
        elif opt in ("-d", "--directory"):
            directory = arg
            if directory == '':
                print("Please specify directory to store artifact for RAW respository")
                return sys.exit(2)
            
        
        ## -w
        elif opt in ("-w", "--workdirectory"):
            work_directory = arg
            if work_directory == '':
                work_directory = path
                if work_directory == '':
                    print("Please specify artifact current directory")
                    return sys.exit(2)
         
        ## -n  
        elif opt in ("-n", "--artifactname"):
            artifact_name = arg
            if artifact_name == '':
                print("Please specify artifact name")
                return sys.exit(2)
        
        ## -g
        elif opt in ("-g", "--groupid"):
            group_id = arg
            if group_id == '':
                print("Please specify Group ID")
                return sys.exit(2)
                  
                  
        ## -r
        elif opt in ("-r", "--repository"):
            repository_name = arg
            if repository_name == '':
                print('Please specify repository name')
                return sys.exit(2)
        ## Deploy-artifact-nexus params START
        
        ## Change version (deltav) START
        elif opt in ("-t", "--type"):
            change_type = arg
        elif opt in ("-a", "--archtype"):
            arch_type = arg
        ## Change version (deltav) END
        elif opt in ("-m", "--message"):
                commit_message = arg
        elif opt in ("-b", "--branch"):
            branch = arg
        ## Commit-push changes repository START
        
        
        ## Commit-push changes repository END
         
    if action == 'nexus':
        nexus.setup_variables()
        print("Nexus Format entered: ", nexus_format)
        if nexus_format == 'raw':
            nexus.upload_nexus_raw()
        elif nexus_format == 'npm':
            nexus.upload_nexus_npm()
        elif nexus_format == 'maven':
            nexus.upload_nexus_maven()
        else:
            print("Invalid nexus format entered")
            
    if action == 'deltav':
        change_version.modify_version()
    if action == 'syncrepo':
        syncrepo.commit_push_changes()
    if action == 'deploy':
        deploy.deploy_app_awx()
    
    
if __name__ == "__main__":
    main(sys.argv[1:])    
        
        