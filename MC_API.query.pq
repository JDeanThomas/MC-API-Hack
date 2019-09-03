/*
This M script gets a bearer token and GETs all member data from the MC REST API.
https://api.membercentral.com/

 
IMPORTANT - The public and Secret keys should be treated as passwords.
*/
 
let
 // Concatenates the Consumer Key & Consumer Secret and converts to base64
 tokens = "{
                ""MCAPIKeyPublic"": "#MCAPIKeyPublic",
                ""MCAPIKeySecret"": "#MCAPIKeySecret"
            }",

 urlToken = "http://api.membercentral.com/v1/authenticate",
 // Uses the MC POST oauth2/token method to obtain a bearer token
 GetJson = Web.Contents(urlToken,
     [
         Headers = [#"Accept"="application/json"],
         Content = Text.ToBinary(tokens)
     ]
 ),
 FormatAsJson = Json.Document(GetJson),
 // Gets token from the Json response
 //AccessToken = FormatAsJson[token],


 AccessTokenHeader = "bearer " & AccessToken,
 // Uses GET method on /v1/members using the bearer token from the previous POST oauth2/token method
 urlGet = "https://api.membercentral.com/v1/member",
params = "{
		    ""count"": "4400"
		  }",
 GetJsonQuery = Web.Contents(urlGet,
     [
         Headers = [#"Authorization"=AccessTokenHeader,
                    #"Content-Type"="application/json"], 
         Content=Text.ToBinary(params)
     ]),
FormatAsJsonQuery = Json.Document(GetJsonQuery)
in
    #"FormatAsJsonQuery"