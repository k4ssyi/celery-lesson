import tasks

result = tasks.deploy_customer_server.delay()
print("doing...")
print(result)
