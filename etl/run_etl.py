import httpx
import pandas as pd
import argparse
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

Base = declarative_base()

class Signal(Base):
    __tablename__ = 'signal'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    data = Column(String)
    timestamp = Column(DateTime)
    signal_id = Column(String)
    value = Column(Float)

def main(date_str):
    base_url = "http://api:8000/data/"

    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    start_date = date_obj.isoformat()
    end_date = (date_obj + timedelta(days=1)).isoformat()

    params = {
        "start_date": start_date,
        "end_date": end_date,
        "variables": ["wind_speed", "power", "ambient_temperature"]
    }

    try:
        response = httpx.get(base_url, params=params)
        response.raise_for_status()

        print("Resposta da API (texto):", response.text)
        response_json = response.json()
        print("Resposta da API (JSON):", response_json)

        data = response_json.get('data', [])
        df = pd.DataFrame(data)

        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)

            agg_df = df.resample('10min').agg({
                'wind_speed': ['mean', 'min', 'max', 'std'],
                'power': ['mean', 'min', 'max', 'std'],
                'ambient_temperature': ['mean', 'min', 'max', 'std']
            })
            agg_df.columns = agg_df.columns.map('{0[0]}_{0[1]}'.format)
            agg_df.reset_index(inplace=True)
            agg_df = agg_df.melt(id_vars='timestamp', var_name='name', value_name='value')

            agg_df[['signal', 'stat']] = agg_df['name'].str.rsplit('_', n=1, expand=True)
            agg_df['signal_id'] = agg_df['name']
            agg_df['data'] = date_str
            final_df = agg_df[['name', 'data', 'timestamp', 'signal_id', 'value']]

            engine = create_engine("postgresql://postgres:postgres@alvo_db:5432/alvo_db")
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            session = Session()

            for _, row in final_df.iterrows():
                signal = Signal(
                    name=row['name'],
                    data=row['data'],
                    timestamp=row['timestamp'],
                    signal_id=row['signal_id'],
                    value=row['value']
                )
                session.add(signal)
            session.commit()
            session.close()

            print(f"Dados para {date_str} processados e inseridos.")

        else:
            print(f"Nenhum dado para processar para {date_str}.")

    except httpx.HTTPError as e:
        print(f"Erro HTTP: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Executa o ETL para uma data específica.")
    parser.add_argument("--date", required=True, help="Data no formato YYYY-MM-DD.")
    args = parser.parse_args()
    main(args.date)