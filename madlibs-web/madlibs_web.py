from flask import Flask, request
from jinja2 import Environment, FileSystemLoader, meta
import os

app = Flask(__name__)


@app.route('/')
def home_page():
    '''
    Render a list of story options. Include links to the form for each.
    '''
    stories = os.listdir(r'./stories')
    env = Environment(
        loader=FileSystemLoader(searchpath=r'./html_templates')
    )
    home_page_template = env.get_template('home.html')
    home_page = home_page_template.render(story_list=stories)
    
    return home_page

@app.route('/show_form')
def madlib_form():
    '''
    Get the story, discover the undeclared variables, and present a form to fill in.
    '''
    story_name = request.args.get('story')
    web_env = Environment(
        loader=FileSystemLoader(searchpath=r'./html_templates')
    )
    story_env = Environment(
        loader=FileSystemLoader(searchpath=r'./stories')
    )
    story_src = story_env.loader.get_source(story_env, story_name)
    story_parsed = story_env.parse(story_src)
    story_vars = meta.find_undeclared_variables(story_parsed)
    try:
        story_vars.remove('range')
    except:
        pass
    story_vars = list(story_vars)
    story_vars.sort()

    form_page_template = web_env.get_template('show_form.html')
    form_page = form_page_template.render(story_name=story_name, variables=story_vars)
    return form_page

@app.route('/show_output', methods=['POST'])
def present_madlib():
    '''
    Take the results from the form in madlib_form(), render the result, and present to the user.
    '''
    story_vars = request.form.to_dict()
    web_env = Environment(
        loader=FileSystemLoader(searchpath=r'./html_templates')
    )
    story_env = Environment(
        loader=FileSystemLoader(searchpath=r'./stories'),
        trim_blocks=True
    )

    story_template = story_env.get_template(story_vars.pop('story_name'))
    story = story_template.render(story_vars)

    web_template = web_env.get_template('show_output.html')
    show_output = web_template.render(story=story)
    return show_output


if __name__ == "__main__":
    app.run(debug=True)