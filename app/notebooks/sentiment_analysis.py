import requests
import pandas as pd
from dotenv import load_dotenv
from GoogleNews import GoogleNews
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

class NewsSearcher:
    def __init__(self, period: str = '7d', lang:str = 'pt', encode: str = 'utf-8'):
        self.period = period
        self.lang = lang
        self.encode = encode
        self.news_df = None
    
    def get_news(self, query):
        googlenews = GoogleNews(period=self.period, lang=self.lang, encode=self.encode)
        googlenews.enableException(True)
        googlenews.search(query)
        return googlenews.results()

class SentimentAnalyzerNotebook:
    def __init__(self, period: str = '7d', lang: str = 'pt', encode: str = 'utf-8'):
        """
        Initializes a SentimentAnalyzerNotebook object with a given URL for the sentiment prediction server.

        Parameters:
        url (str): URL for the sentiment prediction server.

        Attributes:
        url (str): URL for the sentiment prediction server.
        news_df (Pandas DataFrame): DataFrame containing news data, with columns 'title', 'desc', and 'query'.
        __sentiment_indicator (Pandas DataFrame): DataFrame containing the sentiment indicator, with columns 'query' and 'sentiment_weight'.
        """
        self.period = period
        self.lang = lang
        self.encode = encode
        self.news_df = None
        self.__sentiment_indicator = None
        

    @property
    def sentiment_indicator(self):
        """
        Returns the sentiment indicator, a Pandas DataFrame with two columns: 'query' and 'sentiment_weight',
        where 'sentiment_weight' is the mean sentiment weight for each query, multiplied by 100. The weights are:
        - Very Positive: 2
        - Positive: 1
        - Neutral: 0
        - Negative: -1
        - Very Negative: -2
        """
        return self.__sentiment_indicator
    
    def __get_news_df(self,*args):
        """
        Concatenates news dataframes from Google News queries into a single Pandas DataFrame and assigns it to the news_df attribute of the class.
        
        Parameters:
        *args (str): Google News queries to search for.
        """
        news_data = []
        googlenews = NewsSearcher(period=self.period, lang=self.lang, encode=self.encode)
        required_fields = ['title', 'desc', 'img','date']
        for query in args:  
            news = googlenews.get_news(query)
            df = pd.DataFrame(news)
            df = df[required_fields]
            df['query'] = query
            news_data.append(df.reset_index(drop=True))
        self.news_df = pd.concat(news_data, ignore_index=True)


    def __sentiment_prediction(self, text: str):
        """
        Posts a request to the sentiment analysis server to predict the sentiment of a given text.

        Parameters:
            text (str): The text to be analyzed.

        Returns:
            dict: A dictionary with the predicted sentiment label and its confidence score.
        """
        body = {'text': text}
        url = 'http://sentiment_api:8000/analyze'
        response = requests.post(url, json=body)
        
        return response.json()
    

    def __feature_engineering(self):
        
        """
        Performs feature engineering on the news DataFrame by predicting the sentiment
        label for each news description.

        This function applies sentiment prediction to the 'desc' column of the DataFrame
        and assigns the predicted sentiment label to a new column named 'sentiment'.
        """

        def predict_sentiment(description):
            return self.__sentiment_prediction(description)['predicted_label']

        def pooled_sentiment_prediction(descriptions, max_workers=1):
            results = []
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                results = list(executor.map(predict_sentiment, descriptions))
                return results

        self.news_df['sentiment'] = pooled_sentiment_prediction(self.news_df['desc'])
    
    def __cleaning(self):
        self.news_df.dropna(inplace=True)
        self.news_df.drop_duplicates(inplace=True)
        self.news_df.reset_index(drop=True, inplace=True)
    def __set_sentiment_indicator(self):
        """
        Calculates the sentiment indicator for each query by mapping sentiment labels to
        predefined weights and computing the mean weight for each query.

        The weights are:
        - Very Positive: 2
        - Positive: 1
        - Neutral: 0
        - Negative: -1
        - Very Negative: -2

        The sentiment indicator is a DataFrame with two columns: 'query' and 'sentiment_weight',
        where 'sentiment_weight' is the mean sentiment weight for each query, multiplied by 100.

        The sentiment indicator is stored in the 'sentiment_indicator' attribute of the class instance.
        """
        sentiment_weights = {
            "Very Positive": 2,
            "Positive": 1,
            "Neutral": 0,
            "Negative": -1,
            "Very Negative": -2
        }
        self.news_df['sentiment_weight'] = self.news_df['sentiment'].map(sentiment_weights)
        sentiment_indicator = self.news_df.groupby('query')['sentiment_weight'].mean().reset_index()
        sentiment_indicator.columns = ['query', 'sentiment_weight']
        sentiment_indicator['sentiment_weight'] *= 100    
        self.__sentiment_indicator = sentiment_indicator

    
    def main(self, queries: list[str]):
        """
        Executes the sentiment analysis process.

        Args:
            queries (list[str]): A list of query terms to search for news articles.

        This function retrieves news data for the given queries, performs sentiment prediction,
        and calculates the sentiment indicator for each query.
        """

        self.__get_news_df(*queries)
        self.__cleaning()
        self.__feature_engineering()
        self.__set_sentiment_indicator()
        

        
if __name__ == '__main__':
    # Example usage
    # Initialize the SentimentAnalyzerNotebook class
    # and run the main method with a list of queries
    analyzer = SentimentAnalyzerNotebook()
    analyzer.main(['bitcoin', 'ethereum', 'dogecoin', 'litecoin', 'ripple'])
    