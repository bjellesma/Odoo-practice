{
    'name': "DietFacts",
    'version': "1.0",
    'author': 'Bill Jellesma',
    # Modules that our module will depend on
    'depends': ['sale'],
    # data will use any additional files
    'data': ['dietfacts_view.xml', 'meals.xml', 'nutrients.xml', 'dietfacts_report.xml', 'security/ir.model.access.csv'],
    'description': 'This is a test module',
    'installable': True
}