#
# Copyright of this file goes to sh1n1xs:
# https://gitlab.com/sh1n1xs/rock-paper-scissors-data-server/-/blob/main/example_request.py
#
# This file is sending the local wins to an api that tracks the wins
# from multiple people, so you can theoretically analyze what
# choice is used most often by people
# API source code: https://gitlab.com/sh1n1xs/rock-paper-scissors-data-server
#

import requests

# Sends a api request, returns status code; 0 means there was an exception
# The username should NOT contain any spaces and the vote variables have to be positive INT
def sendRequest(username, voteScissors, voteRock, votePaper, voteSpock, voteLizard, apiIP = "http://127.0.0.1:5000"):
    print(voteRock, votePaper, voteScissors, voteSpock, voteLizard)
    reqUrl = apiIP + "/v1/updateRecord"
    reqUrl+= "?username=" + str(username) + "&voteScissors=" + str(voteScissors)
    reqUrl+= "&voteRock=" + str(voteRock) + "&votePaper=" + str(votePaper)
    reqUrl+= "&voteSpock=" + str(voteSpock) + "&voteLizard=" + str(voteLizard)
    responseCode = 0
    try:
        response = requests.post(reqUrl, None)
        responseCode = response.status_code
        print("sent to api successfully")
    except:
        print("Api error")
        return 0
    return responseCode


if __name__ == "__main__":
    print("sending test request")
    code = sendRequest("testUsername", 1, 2, 3, 4, 5)
    print("Done")
    print("code=" + str(code))
