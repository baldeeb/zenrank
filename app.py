from flask import Flask, render_template, request, redirect, url_for


app =  Flask(__name__)
data = []

def output(data):
      return data

@app.route('/')
def webhomePage():
    	# data = ['GET', 'POST' ]
	# if request.method == 'POST':		
	# 	return redirect(url_for('results'))
	# return ("<p>" + "</p><p>".join(data1) + "</p>")

	return render_template("output.html",  # name of template
		number=len(data),  # value for `number` in template
		factors=output(data))

# @app.route('/results')
# def search_results(search):
# 	#the actual search action goes here
# 	#return results
# 	return render_template('results.html', results=results)

if __name__ == "__main__":
	import parser.Parser
	import nodeTools
	import builder
	import ranker
	import matcher

	p = parser.Parser.Parser()
	p.parse_repo('test/')

	searchwords = {"distance", "Pythagorous", "D"}
	import matcher
	import ranker

	matcher.matchKeyWordsToSearchWords(nodeTools.keywordDict, searchwords, verbose=True)
	ranker.rankGraph(nodeTools.keywordDict)

	# printGraph(keywordDict)

	data = builder.collectResults(nodeTools.keywordDict)

	app.run(debug=True)
