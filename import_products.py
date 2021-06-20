import xmlrpc.client
import dotenv
import os
import csv

# env vars
dotenv.load_dotenv()
server = os.getenv('SERVER')
port = os.getenv('PORT')
database = os.getenv('DATABASE')
user = os.getenv('USER')
# TODO in odoo 14, you should be able to setup developer keys
password=os.getenv('PASSWORD')

common = xmlrpc.client.ServerProxy(f'http://{server}:{port}/xmlrpc/2/common')
# Get the user id of our logged in user
# necessary for object calls in the script
uid = common.authenticate(database, user, password, {})
# The object endpoint is used to perform actions on the instance
odoo_api = xmlrpc.client.ServerProxy(f'http://{server}:{port}/xmlrpc/2/object')
# count items in model
filter = [[['calories', '<', '100']]]
product_count = odoo_api.execute_kw(database,uid, password, 'product.template', 'search_count', filter)

filename = 'importdata.csv'
with open(filename, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        meal_name = row[0]
        calories = row[1]

        # search to see if the meal name is part of this model already
        filter = [[('name','=',meal_name)]]
        product_id = odoo_api.execute_kw(database,uid,password,'product.template','search',filter)
        if not product_id:
            record = [{
                'name': meal_name,
                'calories': calories
            }]
            inserted_record = odoo_api.execute_kw(database,uid, password, "product.template", 'create', record)
            print(f'inserted record: {inserted_record}')
        # if the product already exists, we want to update the record
        else:
            record = {
                'name': meal_name,
                'calories': calories
            }
            odoo_api.execute_kw(database,uid, password, "product.template", 'write', [product_id, record])
            updated_record = odoo_api.execute_kw(database,uid, password, "product.template", 'name_get', [product_id])
            print(f'updated record: {updated_record}')