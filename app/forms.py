from flask_wtf import FlaskForm
from wtforms import DecimalField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets import TextArea


class PaymentForm(FlaskForm):
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0)], default=0)
    currency = SelectField('Currency', default='eur', choices=(('eur', 'EUR'),
                                                               ('usd', 'USD'),
                                                               ('rub', 'RUB'),
                                                               ), )
    shop_id = DecimalField('Shop ID', validators=[DataRequired(), NumberRange(min=0)], default=5, places=0, render_kw={'readonly': True})
    shop_order_id = DecimalField('Shop Order ID', validators=[DataRequired(), NumberRange(min=0)], default=15, places=0, render_kw={'readonly': True})
    description = StringField('Description', default='Test description', widget=TextArea())
    submit = SubmitField('Submit')
