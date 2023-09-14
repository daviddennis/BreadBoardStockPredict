from flask import Flask, request, jsonify
from models import app, db, Stock, StockPrediction
import redis
from rq import Queue

from etl import prediction_task


# Start Redis
listen = ['default']
redis_url = 'redis://localhost:6379'
conn = redis.from_url(redis_url)
rq = Queue(connection=conn)


@app.route('/stocks', methods=['GET'])
def get_stocks():
    all_stocks = Stock.query.all()
    result = []
    for stock in all_stocks:
        result.append({
            'Symbol': stock.symbol,
            'Date': stock.date.strftime('%Y-%m-%d'),
            'Opening Price': stock.opening_price
        })
    
    return jsonify(result)

@app.route('/stocks', methods=['POST'])
def add_stocks():
    data = request.get_json()
    symbol = request.args.get('symbol')

    if not data:
        return jsonify({'message': 'No data provided'}), 400

    # Store new stock data in DB
    for item in data:
        symbol = item['Symbol']
        row_date = item['Date']
        opening_price = str(item['Opening Price'])
        if not all([symbol, row_date]) or (not opening_price and opening_price != 0) \
            or opening_price.upper() in ('NA', 'N/A', 'NONE', ''):
            # Drop rows with missing/invalid values
            continue
        stock = Stock(symbol=item['Symbol'], date=item['Date'], opening_price=item['Opening Price'])
        db.session.add(stock)
    db.session.commit()

    if not symbol:
        # Default to first symbol if not provided as a url param
        symbol = data[0]['Symbol']

    job = rq.enqueue(prediction_task, args=(symbol,))#, result_ttl=5000)
    job_id = job.get_id()

    return jsonify({'job_id': job_id}), 202

@app.route('/next_day_prediction', methods=['GET'])
def get_prediction():
    job_id = request.args.get('job_id')
    if not job_id:
        return jsonify({'message': 'Missing job ID'}), 400

    job = rq.fetch_job(job_id)
    if job.is_finished:
        # Get most recent prediction
        prediction = StockPrediction.query.filter_by(symbol=job.args[0]).order_by(StockPrediction.date.desc()).first()
        return jsonify({
            'predicted_opening_price': prediction.predicted_opening_price,
            'date': prediction.date
        }), 200
    else:
        return jsonify({'status': 'pending'}), 202

if __name__ == '__main__':
    app.run(debug=True)
