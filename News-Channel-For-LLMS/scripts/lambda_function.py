import json
import http.client
import urllib.parse
from datetime import datetime
import psycopg2
import os
from utils.schemas import NEWS_TABLE_SCHEMA
from utils.functions import validated_data


def lambda_handler(event, context):
    # Database connection
    try:
        db_conn = psycopg2.connect(
            dbname=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT']
        )
        cursor = db_conn.cursor()
    except Exception as e:
        error_msg = f"Database connection failed due to: {e}"
        print(error_msg)
        return {
            'statusCode': 500,
            'body': json.dumps(error_msg)
        }
    
    
    date_today = datetime.today().strftime('%Y-%m-%d')
    params = urllib.parse.urlencode({
        'access_key': os.environ['API_ACCESS_KEY'],
        'sources': '-cnn',
        'categories': 'health, science, technology, -general,-sports',
        'languages': 'en',
        'date': date_today,
        'sort': 'published_desc',
        'limit': 100,
    })
    
    
    conn = http.client.HTTPConnection('api.mediastack.com')
    conn.request('GET', '/v1/news?' + params)
    res = conn.getresponse()
    data = res.read()
    news_data = json.loads(data.decode('utf-8'))
    conn.close()
    
    # Check for data presence row count expectation check
    if 'data' not in news_data:
        return {
            
            'statusCode': 204,
            'body': json.dumps('No news data to process.'),
            'news_data':json.dumps(news_data)
        }
    
   # Data insertion into the database
    try:
        for item in news_data['data']:
            
            # check and compare with old records, if old records set to False
            cursor.execute("""
                UPDATE news_articles
                SET is_latest = FALSE
                WHERE url = %s AND is_latest = TRUE;
            """, (item['url'],))
            
            validated_data_dict = validated_data(item, NEWS_TABLE_SCHEMA) # do validation with schema
            if not validated_data_dict:
                print("Data validation failed.")
                continue  # Skip insertion if data is not valid
            
            columns = ', '.join(validated_data_dict.keys())
            placeholders = ', '.join(['%s'] * len(validated_data_dict))
            values = tuple(validated_data_dict[key] for key in validated_data_dict.keys())
            sql = f"INSERT INTO news_articles ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, values)  
        db_conn.commit()

    except (ValueError, TypeError) as e:
        error_msg = f"Data validation error: {e}"
        print(error_msg)
        db_conn.rollback()
        return {'statusCode': 400, 'body': json.dumps(error_msg)}

    except Exception as e:
        error_msg = f"Failed to insert data due to error: {e}"
        print(error_msg)
        db_conn.rollback()
        return {'statusCode': 500, 'body': json.dumps(error_msg)}

    finally:
        cursor.close()
        db_conn.close()
        
