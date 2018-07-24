import ccxt
from flask import render_template, request, jsonify

from config.cst import CONFIG_EXCHANGES, CONFIG_CATEGORY_SERVICES, CONFIG_CATEGORY_NOTIFICATION, \
    CONFIG_TRADER, CONFIG_SIMULATOR, CONFIG_CRYPTO_CURRENCIES, GLOBAL_CONFIG_KEY, EVALUATOR_CONFIG_KEY
from interfaces import get_bot

from interfaces.web import server_instance
from interfaces.web.models.configuration import get_evaluator_config, update_evaluator_config, \
    get_evaluator_startup_config, get_services_list, get_symbol_list, update_global_config, get_global_config
from interfaces.web.util.flask_util import get_rest_reply


@server_instance.route("/config")
@server_instance.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        request_data = request.get_json()
        success = False

        if request_data:
            # update global config if required
            if GLOBAL_CONFIG_KEY in request_data and request_data[GLOBAL_CONFIG_KEY]:
                success = update_global_config(request_data[GLOBAL_CONFIG_KEY])

            # update evaluator config if required
            if EVALUATOR_CONFIG_KEY in request_data and request_data[EVALUATOR_CONFIG_KEY]:
                success = update_evaluator_config(request_data[EVALUATOR_CONFIG_KEY])

        if success:
            # return get_rest_reply(jsonify({
            #     GLOBAL_CONFIG_KEY: get_global_config(),
            #     EVALUATOR_CONFIG_KEY: get_evaluator_config()
            # }))
            return get_rest_reply("")
        else:
            return get_rest_reply('{"update": "ko"}', 500)
    else:
        g_config = get_bot().get_config()
        user_exchanges = [e for e in g_config[CONFIG_EXCHANGES]]
        return render_template('config.html',

                               config_exchanges=g_config[CONFIG_EXCHANGES],
                               config_trader=g_config[CONFIG_TRADER],
                               config_trader_simulator=g_config[CONFIG_SIMULATOR],
                               config_notifications=g_config[CONFIG_CATEGORY_NOTIFICATION],
                               config_services=g_config[CONFIG_CATEGORY_SERVICES],
                               config_symbols=g_config[CONFIG_CRYPTO_CURRENCIES],

                               ccxt_exchanges=list(set(ccxt.exchanges) - set(user_exchanges)),
                               services_list=get_services_list(),
                               symbol_list=get_symbol_list([exchange for exchange in g_config[CONFIG_EXCHANGES]]),
                               get_evaluator_config=get_evaluator_config,
                               get_evaluator_startup_config=get_evaluator_startup_config)
