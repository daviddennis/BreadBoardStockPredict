from datetime import date
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from models import db, Stock, StockPrediction, app


def prediction_task(symbol):
    with app.app_context():
        # Load all stock data from DB for the given symbol
        all_data_for_symbol = Stock.query.filter_by(symbol=symbol).all()

        if len(all_data_for_symbol) < 2:
            print(f"Not enough data points for symbol: {symbol}")
            return

        # Clean and normalize data using pandas (ideally would optimize this part)
        dict_list = [obj.__dict__ for obj in all_data_for_symbol]
        df = pd.DataFrame.from_records(dict_list)
        # Drop rows with NaN
        df.dropna(inplace=True)
        clean_data = df.to_dict('records')

        dates = np.array([[d['date'].toordinal()] for d in clean_data]).reshape(-1, 1)
        opening_prices = np.array([d['opening_price'] for d in clean_data])

        # Split the data into test/train datasets
        X_train, X_test, y_train, y_test = train_test_split(dates, opening_prices, test_size=0.2, shuffle=False)

        # Train the model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Make prediction for the next day
        next_day = np.array([[dates[-1][0] + 1]])  # Last date + 1
        next_day_prediction = model.predict(next_day)
        next_day_prediction_val = float(next_day_prediction[0])

        # Store the prediction into StockPrediction table
        next_day_date = date.fromordinal(next_day[0][0])
        new_prediction = StockPrediction(symbol=symbol,
                                         date=next_day_date,
                                         predicted_opening_price=next_day_prediction_val)
        db.session.add(new_prediction)
        db.session.commit()
