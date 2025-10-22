# -*- encoding: utf-8 -*-


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, FloatField, FieldList, SelectField, HiddenField, SubmitField
from wtforms.validators import  DataRequired, Optional
from apps.cryptobot.models import EnumAverageType, EnumTimePeriod, EnumMarginMode, EnumSymbols

# login and registration
"""
    apiKey= "" 
    secret = "" 
    password = "" 
"""
class CreateAPIForm(FlaskForm):
    name = StringField('name',
                         id='name',
                         validators=[DataRequired()])
    apiKey = StringField('apiKey',
                         id='apiKey',
                         validators=[DataRequired()])
    secret = PasswordField('Secret',
                             id='secret',
                             validators=[DataRequired()])
    password = PasswordField('Password',
                             id='password',
                             validators=[DataRequired()])
"""
    params = {
        'symbol': 'BTC/USDT:USDT', #BTC:USDT',
        'timeframe': '1h',
        'margin_mode': 'isolated',  # 'cross'
        'balance_fraction': 1,
        'leverage': 3,
        'average_type': 'SMA',  # 'SMA', 'EMA', 'WMA', 'DCM' 
        'average_period': 6,
        'envelopes': [0.05, 0.06, 0.07],
        'stop_loss_pct': 0.3,
        'price_jump_pct': 0.3,  # optional, uncomment to use
        'use_longs': True,  # set to False if you want to use only shorts
        'use_shorts': True,  # set to False if you want to use only longs
    }
"""    
class StrategyParamsForm(FlaskForm):
    name = StringField('name',
                         id='name',
                         validators=[DataRequired()])
    symbol = SelectField('Symbol', choices=EnumSymbols.choices(),
                         id='symbol',
                         validators=[DataRequired()])
    timeframe = SelectField('Timeframe', choices=EnumTimePeriod.choices(),
                            id='timeframe',
                            validators=[DataRequired()])
    margin_mode = SelectField('Margin Mode', choices=EnumMarginMode.choices(),
                              id='margin_mode',
                              validators=[DataRequired()])
    balance_fraction = FloatField('Balance fraction',
                                  id='balance_fraction',
                                  validators=[DataRequired()])
    leverage = IntegerField('Leverage',
                            id='leverage',
                            validators=[DataRequired()])
    average_type = SelectField('Average type',choices=EnumAverageType.choices(),
                               id='average_type',
                               validators=[DataRequired()])
    average_period = IntegerField('Average period',
                                  id='average_period',
                                  validators=[DataRequired()])
    envelopes = FieldList(FloatField('envelope', validators=[DataRequired()]),
                          min_entries=3,
                          max_entries=10)
    stop_loss_pct = FloatField('Stop loss percent',
                               id='stop_loss_pct',
                               validators=[DataRequired()])
    price_jump_pct = FloatField('Price jump percent',
                                id='price_jump_pct',
                                validators=[Optional()])
    use_longs = BooleanField('Use Longs', id='use_longs')
    use_shorts = BooleanField('Use Shorts', id='use_shorts')
    id = HiddenField('id')
    s = SubmitField("Speichern")