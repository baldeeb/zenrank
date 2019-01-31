from flask import Flask, render_template, request, redirect, url_for

app =  Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
	# if request.method == 'POST':
		
	# 	return redirect(url_for('results'))

	return render_template('index.html')

@app.route('/results')
def search_results(search):
	#the actual search action goes here
	#return results
	return render_template('results.html', results=results)

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=80)
