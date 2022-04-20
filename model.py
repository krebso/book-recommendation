import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.neighbors import NearestNeighbors


def get_data():
    books_df = pd.read_csv( "data/BX-Books.csv", encoding="latin-1", sep=";", on_bad_lines="skip", low_memory=False )
    ratings_df = pd.read_csv( "data/BX-Book-Ratings.csv", encoding="latin-1", sep=";", on_bad_lines="skip" )
    users_df = pd.read_csv( "data/BX-Users.csv", encoding="latin-1", sep=";", on_bad_lines="skip" )

    books_df.drop( columns=[ "Image-URL-S", "Image-URL-M", "Image-URL-L", "Publisher", "Year-Of-Publication" ], inplace=True )
    books_df.columns = [ "ISBN", "title", "author" ]
    users_df.columns = [ "user-id", "location", "age" ]
    ratings_df.columns = [ "user-id", "ISBN", "rating" ]

    user_reviews = ratings_df[ "user-id" ].value_counts()
    ratings_df = ratings_df[ ratings_df[ "user-id" ].isin( user_reviews[ ( user_reviews >= 50 ) & ( user_reviews <= 500 )].index ) ]

    books_with_ratings_df = ratings_df.merge( books_df, on="ISBN" )

    books_with_ratings_df.head()

    books_with_ratings_df = books_with_ratings_df.dropna(axis = 0, subset = ['title'])

    total_book_rating_counts_df = ( books_with_ratings_df.groupby( by=[ "ISBN" ] )[ "rating" ].count().reset_index().rename( columns={ "rating": "rating-count" } )[ [ "ISBN", "rating-count" ] ] )

    books_with_ratings_df = books_with_ratings_df.merge( total_book_rating_counts_df, how="inner" )
    books_with_ratings_df = books_with_ratings_df[ books_with_ratings_df[ "rating-count" ] >= 30 ]

    user_rating_df = books_with_ratings_df.merge( users_df, how="inner" )
    usa_user_rating_df = user_rating_df[ user_rating_df[ "location" ].str.contains( "usa|canada" ) ]
    usa_user_rating_df.head()
    usa_user_rating_df = usa_user_rating_df.drop_duplicates( [ "user-id", "ISBN" ] )

    model_df = usa_user_rating_df.pivot_table( columns="user-id", index="title", values="rating" )
    model_df.fillna( 0, inplace=True )


    model = NearestNeighbors( algorithm="brute" )
    model.fit( model_df )

    return model_df, model
