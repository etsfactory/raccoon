Primeros Pasos
==============

Empezando a utilizar ``Raccoon``:

**Publicar un mensaje de forma asíncrona**

.. code-block:: python

    import logging.config

    from raccoon import Publisher

    import ..settings as st


    BUS_HOST = config.get('bus', 'host')
    BUS_USER = config.get('bus', 'user')
    BUS_PASSWORD = config.get('bus', 'password')
    EXCHANGE_ERROR = 'Error'

    msg = {"error": "Unhandled system error"}

    with Publisher(st.BUS_HOST, st.BUS_USER, st.BUS_PASSWORD, st.EXCHANGE_ERROR) as bus:
        bus.publish_msg(msg)


**Publicar un mensaje de forma síncrona**

.. code-block:: python

    import logging.config

    from raccoon import Publisher

    import ..settings as st


    BUS_HOST = config.get('bus', 'host')
    BUS_USER = config.get('bus', 'user')
    BUS_PASSWORD = config.get('bus', 'password')
    EXCHANGE_CREATE_SYMBOL = 'CreateSymbols'

    data = {
        'symbolType' = 'Exchange Trade Funds',
        # .. #
        'username' = 'James Gordon'
    }

    with RpcPublisher(st.BUS_HOST, st.BUS_USER, st.BUS_PASSWORD, st.EXCHANGE_CREATE_SYMBOL,
                      source_app=st.APP_NAME) as bus:
        symbol_id = bus.rpc_call(data)
        print(symbol_id)

