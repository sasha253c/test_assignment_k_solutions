from app import app

from app.forms import PaymentForm
from app._strategies import choose_strategy

from flask import request, flash, render_template


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    form = PaymentForm()
    if form.validate_on_submit() and request.method == 'POST':
        # flash(f'Form data: { form.data}\n')
        strategy = choose_strategy(currency=form.currency.data)
        app.logger.info(f"Payment: {request.form.to_dict()}")
        print('FORM: ', request.form.to_dict())
        print('*'*80)
        res = strategy.execute(params=request.form.to_dict())
        # flash(f'RES: {res}')
        return res
    return render_template('base.html', form=form)


@app.route("/hello")
def hello():
    return "Hello World!"