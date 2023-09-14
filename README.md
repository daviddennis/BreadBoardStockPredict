Stock Data Pipeline Prediction App
	by David Dennis

This application was designed for use with Python v3.11
If using a different Python version, please alter requirements.txt lib versions accordingly.

Full Flow:
1. Run `download_stocks_data.py` to download Stock data for a few popular stocks from Yahoo Finance.
	a. The data is saved to a CSV called `stock_opening_prices.csv`
2. Install requirements.txt & redis
3. Create the database "stocks" in Postgres.
4. Instantiate the DB schema: `python stock_db.py`
5. Run the flask app API: `python stock_api.py`
6. `export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`
7. cd into the `app` directory, run the redis queue: `rq worker`
8. POST the stock data to the API (`POST http://localhost:5000/stocks?symbol=AAPL`)
	a. A helpful script, `post_data_to_api.py` will POST the data to the API endpoint
9. Receive a job_id for use with `/next_day_prediction`
10. Poll /next_day_prediction with the job_id to get the prediction. A predicted value will be in the response when the Redis job has finished.

DB Schema:
	Tables:
		Name: `stock`
		Columns: id (SERIAL), symbol (VARCHAR), date (DATE), opening_price (FLOAT)
		Name: `stock_prediction`
		Columns: id (SERIAL), symbol (VARCHAR), date (DATE), predicted_opening_price (FLOAT)