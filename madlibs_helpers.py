import os, json, datetime

def get_story_list():
    with open(r'./stories/story_index.json') as story_index_file:
        stories = json.load(story_index_file)["stories"]

    return stories

def get_story_from_id(id):
    with open(r'./stories/story_index.json') as story_index_file:
        stories = json.load(story_index_file)["stories"]
    
    return [story for story in stories if int(id) == story["id"]][0]

def save_story(story_text):

    with open(f'.\\story_archive\\archive_{datetime.date.today().isoformat()}.txt', 'a+', encoding="utf-8") as archive:

        archive.write(f'{story_text}\n\n\n\n')
    return True