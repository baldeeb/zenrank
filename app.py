from flask import Flask, render_template, request, redirect, url_for


app =  Flask(__name__)

def output(data):
      return [data]

@app.route('/')
def webhomePage(data):
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
    	app.run(debug=True)
