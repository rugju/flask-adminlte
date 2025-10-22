
from flask import render_template, redirect, request, url_for
from flask_login import login_required, current_user
from apps.cryptobot import blueprint
from apps.cryptobot.forms import CreateAPIForm, StrategyParamsForm
from apps.cryptobot.models import API, StrategyParams

from .bitget_futures import BitgetFutures

@blueprint.route('/bots/<API_ID>', defaults={'id': None}, methods=['GET', 'POST'])
@blueprint.route('/bots/<API_ID>/<id>', methods=['GET', 'POST'])
@login_required
def bots(API_ID, id=None):
    data = None
    if id:
        data = StrategyParams.find_by_id(id, currentAPI_ID=API_ID)
        print("id", id, "data", data)
        data = data.to_dict()
        print("id", id, "data", data)
   
    form = StrategyParamsForm(data=data) 
    
    if form.validate_on_submit():
        data = StrategyParams(form.data)
        data.save(currentAPI_ID=API_ID )
        data = data.to_dict()
    
    return render_template('crypto/bot.html',segment='bot' ,parent='crypto', form=form, data=data, API_ID=API_ID )

@blueprint.route('/run_bots/<API_ID>/<id>', methods=['GET'])
@login_required
def runbot(API_ID, id):

    # 1) Get config
    try:
        crypto_api = API.find_by_id(API_ID, currentUser=current_user)
        config = StrategyParams.find_by_id(id, currentAPI_ID=API_ID)
        bitget = BitgetFutures(crypto_api.to_dict() )
        symbol = config.symbol
    except Exception as err:
        return f"1) Error getting config: {err}"
   
   # 2) --- CANCEL OPEN ORDERS ---
    orders = bitget.fetch_open_orders(symbol) 
    trigger_orders = bitget.fetch_open_trigger_orders(symbol=symbol)
    print(trigger_orders)


    return render_template('crypto/run-bot.html',segment='bot' ,parent='crypto',
                            symbol=symbol, trigger_orders=trigger_orders, orders=orders)


@blueprint.route('/api_details/<id>', methods=['GET'])
@login_required
def api_details(id): # https://python-adv-web-apps.readthedocs.io/en/latest/flask_forms.html#put-the-form-in-a-template
    crypto_api = API.find_by_id(id, currentUser=current_user)
    print("crypto_api", crypto_api.get_id())

    bitget = BitgetFutures(crypto_api.to_dict() )

    symbol='BTC/USDT:USDT'
    balance = bitget.fetch_balance()
    trades = bitget.fetch_open_trigger_orders(symbol=symbol)
    t = [
        {"symbol": i['symbol'],
        "datetime": i['datetime'],
        "type": i['type'],
        "side": i['side'],
        "amount": i['amount'],
        "stopPrice": i['stopPrice'],
        "orderType": i['info']['orderType'],
        "tradeSide": i['info']['tradeSide'],
        "triggerType": i['info']['posSide'],
        "triggerPrice": i['info']['triggerPrice'],
        "id": i['id']} 
        for i in trades
    ]

    positions = bitget.fetch_open_positions(symbol=symbol)
    p = [
        {"symbol": i['symbol'],
        "datetime": i['datetime'],
        "total": i['info']['total'],
        "side": i['side'],
        "amount": i['info']['total'],
        "entryPrice": i['entryPrice'],
        "marketPrice": i['markPrice'],
        "leverage": i['leverage'],
        "stopLossPrice": i['stopLossPrice'],
        "takeProfitPrice": i['takeProfitPrice'],
        #"triggerType": i['info']['posSide'],
        #"triggerPrice": i['info']['triggerPrice'],
        "unrealizedPL": i['info']['unrealizedPL']} 
        for i in positions
    ]

    #trades = bitget.fetch_open_orders(symbol='BTC/USDT:USDT')

    # Get APIs for current user
    apiList = API.getList(currentUser=current_user)

    botList = StrategyParams.getListKeys(currentAPI=crypto_api )

    #print(botList[0].to_dict())

    return render_template('crypto/api-details.html',segment='api-details'+id ,parent='crypto', API_LIST=apiList, API_detail=crypto_api, balance=balance, trades=t, positions=p, form=StrategyParamsForm(),
                           botList=botList, API_ID=id )

@blueprint.route('/api', methods=['GET', 'POST'])
@login_required
def api():
    APIForm = CreateAPIForm(request.form)
    if request.method == 'POST' and 'password' in request.form:
        name = request.form['name']
        apiKey = request.form['apiKey']
        secret = request.form['secret']
        password = request.form['password']

        crypto_api = API()
        crypto_api.name = name
        crypto_api.apiKey = apiKey
        crypto_api.secret = secret
        crypto_api.password = password
        crypto_api.save(currentUser=current_user)
        print(crypto_api.__entity__ )

    # Get APIs for current user
    apiList = API.getList(currentUser=current_user)

    #app.context_processor ( inject_crypt_apis )

    return render_template('crypto/api.html',segment='api',parent='crypto', form=APIForm, API_LIST=apiList)


@blueprint.route('/api_accounts', methods=['GET'])
@login_required
def api_accounts():
    APIForm = CreateAPIForm(request.form)
    if 'password' in request.form:
        name = request.form['name']
        apiKey = request.form['apiKey']
        secret = request.form['secret']
        password = request.form['password']

        crypto_api = API()
        crypto_api.name = name
        crypto_api.apiKey = apiKey
        crypto_api.secret = secret
        crypto_api.password = password
        crypto_api.save()

    return render_template('crypto/api.html', form=APIForm)    