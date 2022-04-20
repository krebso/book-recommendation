from flask import Flask, request
from typing import List

from model import get_data


model_df, model = get_data()

app = Flask( __name__ )


def get_recommendations( title: str ) -> List[ str ]:
    row = model_df.iloc[ model_df.index == title ]
    if row.shape[ 0 ] == 0:
        return ["", f"Sorry, we do not have title '{ title }' in our database" ]
    
    _, recommendations = model.kneighbors( row.values.reshape(1, -1) )
    return [ model_df.index[ r ] for r in recommendations[ 0 ] ]
        

@app.route( "/" )
def index():
    return """
        <form action="/recommend", method="post">
        <p>
        <label for="title">Please enter a title you enjoyed: </label>
        <input type="text", name=title>
        </p>
        <p>
        <input type="submit">
        </p>
        </form>
           """


@app.route( "/recommend", methods=[ "POST" ] )
def recommend():
    title = request.form.get( "title" )
    assert title is not None and isinstance( title, str )
    recommendations = get_recommendations( title )
    return f"<h2>Recommendations for '{ title }'</h2>" + "\n".join( map( lambda s: f"<p>{ s }</p>",
        recommendations[1:] ) ) + "<br><a href='/'>Back to menu</a>"


app.run()
