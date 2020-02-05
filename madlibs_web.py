from flask import Flask, request
from jinja2 import Environment, FileSystemLoader, meta
import os, json
import madlibs_helpers

app = Flask(__name__)
web_env = Environment(
        loader=FileSystemLoader(searchpath=r'./html_templates')
    )
story_env = Environment(
        loader=FileSystemLoader(searchpath=r'./stories/templates'),
        trim_blocks=True
    )



@app.route('/')
def home_page():
    '''
    Render a list of story options. Include links to the form for each.
    '''
    
    home_page_template = web_env.get_template('home.html')
    stories = madlibs_helpers.get_story_list()
    home_page = home_page_template.render(story_list=stories)
    
    return home_page

@app.route('/show_form')
def madlib_form():
    '''
    Get the story, discover the undeclared variables, and present a form to fill in.
    '''
    story_id = request.args.get('id')

    
    story = madlibs_helpers.get_story_from_id(story_id)
    
    form_page_template = web_env.get_template('show_form.html')
    form_page = form_page_template.render(story)
    return form_page

@app.route('/show_output', methods=['POST'])
def present_madlib():
    '''
    Take the results from the form in madlib_form(), render the result, and present to the user.
    '''
    story_vars = request.form.to_dict()

    story_id = story_vars.pop('id') # Returns the value and deletes it from the dictionary
    story_info = madlibs_helpers.get_story_from_id(story_id)

    story_template = story_env.get_template(story_info["template"])
    story = story_template.render(story_vars)
    render = {
        "story": story,
        "attributes": story_vars
    }
    story_info["render"] = render

    print(story_info)
    try:
        # This is the single most dangerous operation in the whole application.
        # Multiple threads could end up attempting to write to the same file
        # at the same time. If there's a conflict, I would rather have an 
        # incomplete archive than have the entire page fail to load.
        madlibs_helpers.save_story(story)
    except:
        pass
    web_template = web_env.get_template('show_output.html')
    show_output = web_template.render(story_info)
    return show_output


if __name__ == "__main__":
    app.run(debug=True)
