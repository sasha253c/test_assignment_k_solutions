from app import app

from app.forms import PaymentForm
from app._strategies import choose_strategy

from flask import request, render_template


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    form = PaymentForm()
    if form.validate_on_submit() and request.method == 'POST':
        strategy = choose_strategy(currency=form.currency.data)
        app.logger.info(f"Payment: {request.form.to_dict()}")
        res = strategy.execute(params=request.form.to_dict())
        return res
    return render_template('base.html', form=form)
