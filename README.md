# cheminformatics_slackbot

# Slack bot that responds to SMILES strings with RDkit molecular descriptors
* Currently some bugs:
** Responds to an invalid SMILES string with "Internal Server Error".
** Responds to valid SMILES with raw json.dumps string of all molecular descriptors. Should be formatted more nicely, or allow user to request specific descriptors.
** Responds to each request multiple times - probably need to use a different request/response handler to communicate with Slack.

# But why?? 
* Demonstrate a fun API use case.
* You have a quick cheminformatics question and want to ask a robot?

# How do I set this up?
* In the AWS console, go to the Lambda service and *create function*. It walks you through the steps very helpfully. I chose Python 3.6 for the language. Use the Python code included here for your function. (But please, host your own RDkit API! Otherwise our demo will have to come down.)
* Follow a Slack Lambda tutorial. (Obviously, I have not gotten this part to work perfectly yet.) https://api.slack.com/tutorials/tags/lambda-lambda-lambda
