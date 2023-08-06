# jblib-aws
## Author: Justin Bard

This module was written to minimize the need to write the functions I use often.

INSTALL:  ` python3 -m pip install jblibaws `

---
The source code can be viewed here: [https://github.com/ANamelessDrake/jblib-aws](https://github.com/ANamelessDrake/jblib-aws)

More of my projects can be found here: [http://justbard.com](http://justbard.com)

---

` from jblibaws import talk_with_dynamo `
```
    class talk_with_dynamo(table, boto_session, region='us-east-1')
            
        Example: 
            table_name = "table-name"
            boto_session = boto3.session.Session()
            dynamo = talk_with_dynamo(table_name, boto_session) ## Generate Database Object

            response = dynamo.query(partition_key=partition_key, partition_key_attribute=partition_key_attribute, sorting_key=sorting_key, sorting_key_attribute=sorting_key_attribute, index=index_key)
            print ("Resposne: {}".format(response))

            insert_resposne = dynamo.insert(json_object)
            print("Insert Response: {}".format(insert_response))

            update_response = dynamo.update(partition_key_attribute, sorting_key_attribute, update_key, update_attribute)
            
```

---
` from jblibaws import talk_with_cognito `
```
    class talk_with_cognito(boto_client, cognito_user_pool_id)
            
        Example: 

        Functions: 
            get_user_email(cognito_user_id)
            - Gets User Email Address
            
```
### More Documentation To Come