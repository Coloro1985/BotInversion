# src/webhook_server.py

from flask import Flask, request, jsonify
import json
from .bot.strategy_manager import StrategyManager

# Inicializamos la aplicación Flask
app = Flask(__name__)

# Esta es una referencia global a nuestro gestor de estrategias.
# La inicializaremos desde nuestro runner principal.
strategy_manager = None 

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """
    Este es el endpoint que recibirá las alertas de TradingView.
    Debe ser accesible desde internet para que TradingView pueda enviarle datos.
    """
    global strategy_manager
    if not strategy_manager:
        return jsonify({"status": "error", "message": "Strategy Manager no inicializado"}), 500

    print("\n🚀 ¡Webhook de TradingView recibido! 🚀")
    
    try:
        # El mensaje de la alerta de TradingView viene en el cuerpo de la petición.
        data = request.data.decode('utf-8')
        
        # Opcional: Si el mensaje es un JSON, lo procesamos.
        try:
            payload = json.loads(data)
            print("Payload JSON:", payload)
        except json.JSONDecodeError:
            # Si no es JSON, lo tratamos como texto plano.
            payload = {"message": data}
            print("Payload de texto:", data)

        # --- Lógica para procesar la alerta ---
        # Aquí es donde traduces el mensaje en una acción de trading.
        # Por ejemplo, el mensaje de TradingView podría ser:
        # { "action": "buy", "symbol": "BTCUSDT", "quantity_usd": 50 }
        
        action = payload.get('action', '').lower()
        symbol = payload.get('symbol', '').upper()
        quantity_usd = payload.get('quantity_usd')

        if not all([action, symbol, quantity_usd]):
            return jsonify({"status": "error", "message": "Datos incompletos en el webhook"}), 400

        # Obtenemos el adaptador del exchange desde el manager
        exchange = strategy_manager.strategies[0].exchange
        
        # Calculamos la cantidad de cripto a comprar/vender
        price = exchange.get_price(symbol)
        quantity_crypto = float(quantity_usd) / price
        
        print(f"Ejecutando orden de webhook: {action} {quantity_crypto:.6f} de {symbol}")
        
        # Ejecutamos la orden
        order_result = exchange.create_order(
            symbol=symbol,
            order_type='MARKET',
            side=action.upper(),
            quantity=quantity_crypto
        )
        
        return jsonify({"status": "success", "order": order_result}), 200

    except Exception as e:
        print(f"Error al procesar el webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

def run_webhook_server(manager: StrategyManager):
    """
    Función para iniciar el servidor Flask.
    
    :param manager: Una instancia del StrategyManager para poder ejecutar órdenes.
    """
    global strategy_manager
    strategy_manager = manager
    
    print("\n--- 🌐 Iniciando servidor de Webhooks en http://0.0.0.0:5000/webhook ---")
    print("El bot ahora está listo para recibir alertas de TradingView.")
    # 'host="0.0.0.0"' hace que el servidor sea accesible desde fuera de tu máquina.
    app.run(host='0.0.0.0', port=5000)