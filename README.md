# Slack bot responds to SMILES strings with RDkit molecular descriptors
* Currently some bugs:
  * Responds to an invalid SMILES string with "Internal Server Error".
  * Responds to valid SMILES with raw json.dumps string of all molecular descriptors. (Should be formatted more nicely, or allow user to request specific descriptors.)
  * Responds to each request multiple times - something is wrong with the request/response handler to communicate with Slack.

# But why?? 
* Demonstrate a fun API use case.
* You have a quick cheminformatics question and want to ask a robot?

# Cool, how do I set this up?
* In the AWS console, go to the Lambda service and *create function*. It walks you through the steps. I chose Python 3.6 for the language. Use the Python code included here for your function. (But please, host your own RDkit API for production! Our demo will have to come down if it gets too expensive to host.)
* Follow a Slack Lambda tutorial. (This part doesn't work properly yet, see above.) https://api.slack.com/tutorials/tags/lambda-lambda-lambda
