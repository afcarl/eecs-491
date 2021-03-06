#github data scrapper

"""
variables of interest:
    indp. variables
    - language, given as a binary variable. Need 4 positions for 5 langagues
    - #number of days created ago, 1 position
    - has wiki? Boolean, 1 position
    - followers, 1 position
    - following, 1 position
    - constant
    
    dep. variables
    -stars/watchers
    -forks
"""
from json import loads
import datetime
import numpy as np
from requests import get


MAX = 8000000
today =  datetime.datetime.today()
randint = np.random.randint
N = 120 #sample size. 
auth = ("WillKoehrsen", "4Q#eKphooHXaSOS" )

language_mappings = {"Python": 0, "JavaScript": 1, "Ruby": 2, "Java":3, "Shell":4, "PHP":5, "R":6}

#define data matrix: 
X = np.zeros( (N , 13), dtype = int )

for i in range(N):
    is_fork = True
    is_valid_language = False
    
    while is_fork == True or is_valid_language == False:
        is_fork = True
        is_valid_language = False
        
        params = {"since":randint(0, MAX ) }
        r = get("https://api.github.com/repositories", params = params, auth=auth )
        results = loads( r.text )[0]

        #im only interested in the first one, and if it is not a fork.
        is_fork = results["fork"]
        
        r = get( results["url"], auth = auth)
        
        #check the language
        repo_results = loads( r.text )
        try: 
            language_mappings[ repo_results["language" ] ]
            is_valid_language = True
        except:
            pass

    #languages 
    X[ i, language_mappings[ repo_results["language" ] ] ] = 1
    
    #delta time
    X[ i, 7] = ( today - datetime.datetime.strptime( repo_results["created_at"][:10], "%Y-%m-%d" ) ).days
    
    #haswiki
    X[i, 8] = repo_results["has_wiki"]
    
    #get user information
    r = get( results["owner"]["url"] , auth = auth)
    user_results = loads( r.text )
    X[i, 9] = user_results["following"]
    X[i, 10] = user_results["followers"]
    
    #get dep. data
    X[i, 11] = repo_results["watchers_count"]
    X[i, 12] = repo_results["forks_count"]
    print() 
    print(" -------------- ")
    print(i, ": ", results["full_name"], repo_results["language" ], repo_results["watchers_count"], repo_results["forks_count"])
    print(" -------------- ")
    print() 
    
np.savetxt("../data/github_data_update.csv", X, delimiter=",", fmt="%d" )