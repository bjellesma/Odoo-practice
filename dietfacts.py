from odoo import models, fields, api

# Inherit the models
class Dietfacts_product_template(models.Model):
    # class attributes
    _name = 'product.template'
    _inherit ='product.template'
    # link to the nutrient ids 
    nutrient_ids = fields.One2many('product.template.nutrient', 'product_id')

    @api.depends('nutrient_ids', 'nutrient_ids.value', 'nutrient_ids.daily_percent')
    def _calcscore(self):
        # var to hold number of calories
        current_score = 0 
        for nutrient in self.nutrient_ids:
            # print(f'serving size: {mealitem.item_id.serving_size}')
            if nutrient.value == 2:
                nutrient.value = nutrient.value * 2
            current_score += nutrient.value
        self.score = current_score

    score = fields.Float(string="Nutrition Score", store=True, compute="_calcscore")
    # Create a calories integer field
    calories = fields.Integer("Calories Per Serving")
    serving_size = fields.Float("Serving Size")
    last_updated = fields.Date("Last Updated")

    

class Dietfacts_res_users_meal(models.Model):
    _name = "res.users.meal"
    _description = "This is to enter the meals"
    name = fields.Char("Meal Name")
    meal_date = fields.Datetime("Meal Date")
    # meal_id provides how we know which meal this goes with
    item_ids = fields.One2many('res.users.mealitem', 'meal_id')
    # Many users but only one can eat the meal
    user_id = fields.Many2one('res.users', 'Meal User') 

    # method to loop through all meal items and sum total calories
    # any time an item_ids change, we need to recalc
    @api.depends('item_ids', 'item_ids.servings')
    def _calccalories(self):
        # var to hold number of calories
        current_calories = 0 
        for mealitem in self.item_ids:
            # print(f'serving size: {mealitem.item_id.serving_size}')
            current_calories += mealitem.calories * mealitem.servings
        self.total_calories = current_calories

    # displaying the computed fields
    # calling the calccalories method
    total_calories = fields.Integer(string="Total Calories", store=True, compute="_calccalories")

    large_meal = fields.Boolean("Large meal")

    # Set large meal to true automatically if the total calories is more than 10
    @api.onchange('total_calories')
    def check_total_calories(self):
        if self.total_calories > 10:
            self.large_meal = True

    notes = fields.Text('Meal Notes')

class Dietfacts_res_users_mealitem(models.Model):
    _name = "res.users.mealitem"
    _description = "meal item"

    # tells meal item which meal it goes with
    meal_id = fields.Many2one('res.users.meal')
    item_id = fields.Many2one('product.template', 'Menu Item')
    servings = fields.Float(related="item_id.serving_size", readonly=True)
    # related will look at the field that you've specified as the relation (item id is a many2one) and see that it links to product.template
    # the ".calories" will get the calories field from the product.template table
    calories = fields.Integer(related="item_id.calories", string="Calories Per Serving", store=True, readonly=True)
    notes = fields.Text('meal item notes')

class DietFacts_product_nutrient(models.Model):
    _name = 'product.nutrient'
    name = fields.Char('Nutrient Name')
    diet_item_id = fields.Many2one('product.template', 'Diet Item')
    uom_id = fields.Many2one('uom.uom', 'Unit of Measure')
    description = fields.Text("Description")

# a join table to join a nutrient with a diet item
class DietFacts_product_template_nutrient(models.Model):
    _name = "product.template.nutrient"
    nutrient_id = fields.Many2one('product.nutrient', string='Product Nutrient')
    product_id = fields.Many2one('product.template')
    uom = fields.Char(related='nutrient_id.uom_id.name', string = "UOM", readyonly=True)
    value = fields.Float('Nutrient Value')
    daily_percent = fields.Float('Daily Recommended Value')