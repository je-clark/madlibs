from jinja2 import Environment, FileSystemLoader, meta
import argparse, os

def madlibs(directory, filename):
    env = Environment(
        loader = FileSystemLoader(searchpath=directory)
    )

    template_src = env.loader.get_source(env, filename)
    template = env.get_template(filename)
    parsed = env.parse(template_src)


    var = meta.find_undeclared_variables(parsed)
    keys = list(var)
    keys.sort()

    madlibs_substitutions = {}

    print("Welcome to Mad Libs! Please enter the parts of speech as prompted below.")
    print()

    for item in keys:
        prompt = ' '.join(item.split(r'_'))
        madlibs_substitutions[item] = input(f'{prompt}: ')

    result = template.render(madlibs_substitutions)

    print()
    print("Enjoy your literary masterpiece!")
    print()

    print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play Mad Libs!")
    parser.add_argument("path", action='store', help="File Path to Mad Libs Template")

    args = parser.parse_args()

    directory = os.path.dirname(args.path)
    filename = os.path.basename(args.path)

    madlibs(directory, filename)