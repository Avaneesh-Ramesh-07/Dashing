
import numpy as np
import plotly.offline as py
import dash
from dash import dcc
from dash import html
import sys
import webbrowser
import threading
import time
from dash.dependencies import Input, Output


def dashboard_init(data_loaders, global_options):


	webpages = {}
	checklist_barchart = dcc.Checklist(
		id='Barchart',
		options=[
			{'label': 'Barchart', 'value': 'Barchart'}
			],
		value=['Barchart'],
		style={'display': 'block', 'font-family': 'georgia', 'font-size': '20px'}
	)
	checklist_heatmap = dcc.Checklist(
		id='Heatmap',
		options=[
			{'label': 'Heatmap', 'value': 'Heatmap'}
		],
		value=['Heatmap'],
		style={'display': 'block', 'font-family': 'georgia', 'font-size': '20px'}
	)
	checklist_sunburst = dcc.Checklist(
		id='Sunburst',
		options=[
			{'label': 'Sunburst', 'value': 'Sunburst'}
		],
		value=['Sunburst'],
		style={'display': 'block', 'font-family': 'georgia', 'font-size': '20px'}
	)
	checklist_rsm = dcc.Checklist(
		id='RSM',
		options=[
			{'label': 'RSM', 'value': 'RSM'}
		],
		value=['RSM'],
		style={'display': 'block', 'font-family': 'georgia', 'font-size': '20px'}
	)


	for app_name, data_loader in data_loaders.items():
		output_list = create_page(data_loader)
		if data_loader.options['charts']:
			webpages[app_name] = [checklist_barchart, checklist_heatmap, checklist_sunburst, checklist_rsm, html.Br(), html.Br(), html.Br(), output_list[0]]
	#			for fig in data_loader.options['charts']:
	#				fig.write_image("images/%s.pdf" % app_name)

	port = global_options['port'] if 'port' in global_options else 7050

	if len(webpages.keys()) > 0:
		start_server(webpages, port)
	"""webpages = {}


	for app_name, data_loader in data_loaders.items():
		if data_loader.options['charts']:
			output_list=create_page(data_loader)
			webpages[app_name] = output_list[0]
			print(output_list[0])
			
#			for fig in data_loader.options['charts']:
#				fig.write_image("images/%s.pdf" % app_name)
	
	port = global_options['port'] if 'port' in global_options else 7050 

	if len(webpages.keys()) > 0:
		start_server(webpages, port, output_list[0])"""

# creates a div element that represents a whole webpage
# containing all visualizations for an app
def create_page(data_loader):
	chart_dict={
		0:'Barchart',
		1:'Heatmap',
		2:'Sunburst',
		3:'RSM'
	}
	charts = data_loader["charts"]
	title = data_loader.get_option('title', 'untitled chart')
	chart_elems = list(html.H1(children=title))
	index=0
	for chart in charts:
		chart_elems.append(html.Div([html.H1(chart_dict[index], style={'display':'block', 'font-family':'georgia','font-size':'28px'}), dcc.Graph(id='chart'+str(index), figure=chart), html.Br(), html.Br()], style={'display':'block', 'font-family':'georgia','font-size':'16px'}))
		index+=1
	return html.Div(id='chart_list', children=chart_elems), chart_elems

def start_server(webpages, port):

	external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
	index_app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

	# nav bar
	nav_divs = []
	for page in webpages:
		nav_divs.append(html.Li(dcc.Link(page, href='/' + page)))
	nav = html.Ul(children=nav_divs, className="navbar")

	"""print(len(charts))
	for i in range(len(charts) - 1):
		print(str(i) + str(charts[i]))"""
	# home page
	index_divs = [dcc.Location(id='url', refresh=False)]
	index_divs.append(nav)
	index_divs.append(html.Div(id='page-content'))
	index_app.layout = html.Div(index_divs, style={'backgroundColor':'#E0DDDD'})

	# mimics having different webpages depending on the URL
	@index_app.callback(dash.dependencies.Output('page-content', 'children'),
						[dash.dependencies.Input('url', 'pathname')])
	def display_page(pathname):
		if pathname is None: return
		key = pathname[1:]
		if key in webpages:
			return webpages[key]
		else:
			return

	"""dash.dependencies.Output('chart2', 'style'),"""
	@index_app.callback(dash.dependencies.Output('chart0', 'style'),
						dash.dependencies.Input('Barchart', 'value'), suppress_callback_exceptions=True)
	def update_with_barchart(arg):
		if arg is None:return
		if len(arg)>0:
			return {'display':'block'}
		else:
			return {'display':'none'}

	@index_app.callback(dash.dependencies.Output('chart1', 'style'),
						dash.dependencies.Input('Heatmap', 'value'), suppress_callback_exceptions=True)
	def update_with_heatmap(arg):
		if arg is None: return
		if len(arg) > 0:
			return {'display': 'block'}
		else:
			return {'display': 'none'}

	@index_app.callback(dash.dependencies.Output('chart2', 'style'),
						dash.dependencies.Input('Sunburst', 'value'), suppress_callback_exceptions=True)
	def update_with_sunburst(arg):
		if arg is None: return
		if len(arg) > 0:
			return {'display': 'block'}
		else:
			return {'display': 'none'}

	@index_app.callback(dash.dependencies.Output('chart3', 'style'),
						dash.dependencies.Input('RSM', 'value'), suppress_callback_exceptions=True)
	def update_with_rsm(arg):
		if arg is None: return
		if len(arg) > 0:
			return {'display': 'block'}
		else:
			return {'display': 'none'}










	app_thread = threading.Thread(target=index_app.run_server,
								  kwargs={'debug': True, 'port': port, 'use_reloader': False})
	# index_app.run_server(debug=True, port=port, use_reloader=False)
	app_thread.start()
	webbrowser.open(f'http://127.0.0.1:{port}')
	"""def update_page(arg):
			return

			print(arg)
			index=0
			for value in arg:
				charts[int(value)] = html.Div(dcc.Graph(id=('chart' + value)), style={'display': 'block'})
			for indiv_chart in charts:
				if str(index) in arg:
					indiv_chart = html.Div([dcc.Graph(id='chart' + str(index), figure=[indiv_chart])])

					#return {'display': 'none'}
				index+=1"""

	# filtered_list = list(filter(None, arg))
	# if arg is None: return
	# chart_elems.append(html.Div(dcc.Graph(id='chart' + str(index), figure=chart), style={'display': 'block'}))

	"""for value in arg:
		charts[int(value)] = html.Div(dcc.Graph(id=('chart' + value)), style={'display': 'none'})"""

	"""@index_app.callback(dash.dependencies.Output('page-content', 'children'), dash.dependencies.Input('graph_checklist', 'value'), suppress_callback_exceptions=True)
    def display_page(arg):
        print(arg)
        #filtered_list = list(filter(None, arg))
        if arg is None:return
        #chart_elems.append(html.Div(dcc.Graph(id='chart' + str(index), figure=chart), style={'display': 'block'}))

        for value in arg:
            charts[int(value)]=html.Div(dcc.Graph(id=('chart'+value)), style={'display':'none'})
        return"""


"""charts[0]=html.Div([dcc.Graph(id=('chart0'), figure=chart)], style={'display':'none'})"""


"""external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
index_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# nav bar
nav_divs = []

for page in webpages:
	nav_divs.append(html.Li(dcc.Link(page, href='/'+page)))
nav = html.Ul(children = nav_divs, className="navbar")

checklist = dcc.Checklist(
	id='graph_checklist',
	options=[
		{'label': 'chart1', 'value': '1'},
		{'label': 'Montréal', 'value': 'MTL'},
		{'label': 'San Francisco', 'value': 'SF'}
	]
)

# home page
index_divs = [dcc.Location(id='url', refresh=False)]
index_divs.append(nav)
index_divs.append(html.Div(id='page-content'))
#index_divs.append(checklist)

index_app.layout = html.Div(index_divs)



# mimics having different webpages depending on the URL

@index_app.callback(dash.dependencies.Output('page-content', 'children'),
[dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
	if pathname is None: return
	key = pathname[1:]
	if key in webpages:
		return webpages[key]
	else:
		return

@index_app.callback(dash.dependencies.Output('chart1', 'label'),
[dash.dependencies.Input('graph_checklist', 'value')])
def display_page():
	print ("here")







app_thread = threading.Thread(target=index_app.run_server,
	kwargs={'debug':True, 'port':port, 'use_reloader':False})
#index_app.run_server(debug=True, port=port, use_reloader=False)
app_thread.start()
webbrowser.open(f'http://127.0.0.1:{port}')"""




#shelved

#	#search for events/resources/regions, highlight those divs?
#	@index_app.callback(
#		dash.dependencies.Output('placeholder', 'children'),
#		[dash.dependencies.Input('searchbar', 'value')])
#	def search(value):
#		print("searching for: ", value)
#		pagecontent = index_divs[2]
#		print(pagecontent)
		
	
