# Slack bot responds to SMILES strings with RDkit molecular descriptors
* If you would like to contribute:
  * Better docs on the setup would be nice.
  * In particular, I followed a Lambda/Python tutorial for this current version, and it receives each request from Slack multiple times. I think this is a Lambda setup issue not a timeout issue, because it happens even with an immediate 200 response.

# But why?? 
* Demonstrate a fun API use case.
* You have a quick cheminformatics question and want to ask a robot?

![caffeine](https://user-images.githubusercontent.com/45920345/56064948-55bc7580-5d28-11e9-846b-47850a039d25.png)
![not smiles](https://user-images.githubusercontent.com/45920345/56064949-55bc7580-5d28-11e9-9ffc-50bab81df4b3.png)

# Cool, how do I set this up?
* In the AWS console, go to the Lambda service and *create function*. It walks you through the steps. I chose Python 3.6 for the language. Use the Python code included here for your function. (But please, host your own RDkit API for production! Our demo will have to come down if it gets too expensive to host.)
* In slack, create an App with incoming webhooks: https://api.slack.com/incoming-webhooks
* Note the Lambda integration doesn't work quite right yet (see above) but there are many helpful tutorials here: https://api.slack.com/tutorials/tags/lambda-lambda-lambda
