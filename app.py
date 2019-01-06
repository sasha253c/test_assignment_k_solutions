
from flask import Flask, render_template, flash, redirect, request
from flask_bootstrap import Bootstrap

from forms import PaymentForm
from config import DevelopmentConfig
from strategies import choose_strategy


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

bootstrap = Bootstrap(app)



@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    form = PaymentForm()
    if form.validate_on_submit() and request.method == 'POST':
        flash(f'Form data: {form.data}')
        strategy = choose_strategy(currency=form.currency.data)
        print('FORM: ', request.form.to_dict())
        print('*'*80)
        res = strategy.execute(params=request.form.to_dict())
        flash(f'RES: {res}')
        return res
    return render_template('base.html', form=form)


if __name__ == '__main__':
    app.run()
