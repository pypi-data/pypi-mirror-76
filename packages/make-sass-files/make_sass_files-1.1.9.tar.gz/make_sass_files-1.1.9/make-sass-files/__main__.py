 
import os
import json
import time

while True:
    choice = input(
        "Sass 3-1: a\nSass 7-1: b\n\nPlease choose option a or b (q to quit): ")

    if choice.lower() == 'b':
        try:
            os.mkdir('sass')
        except FileExistsError:
            print("\nThe sass folder already exists.\n\nThe following files have been added to the sass directory if they did not already exist.\n")

            with open('scss_files.json') as json_file:
                data = json.load(json_file)

                for e in data["abstracts"]:
                    print(e)

                for e in data["base"]:
                    print(e)

                for e in data["components"]:
                    print(e)

                for e in data["layout"]:
                    print(e)

                for e in data["pages"]:
                    print(e)

                for e in data["themes"]:
                    print(e)

                for e in data["vendors"]:
                    print(e)

        finally:
            # make the main.scss file if it does not exist
            open('sass/main.scss', "a")

            with open('scss_files.json') as json_file:
                data = json.load(json_file)

                # make the sub directories
                for folder in data["folders"]:
                    try:
                        os.mkdir(folder)
                    except FileExistsError:
                        pass

                # make all the files for the sub directories
                for scss_file in data["abstracts"]:
                    open(scss_file, "a")

                for scss_file in data["base"]:
                    open(scss_file, "a")

                for scss_file in data["components"]:
                    open(scss_file, "a")

                for scss_file in data["layout"]:
                    open(scss_file, "a")

                for scss_file in data["pages"]:
                    open(scss_file, "a")

                for scss_file in data["themes"]:
                    open(scss_file, "a")

                for scss_file in data["vendors"]:
                    open(scss_file, "a")

            files = (
                ["// Add any additional imports here",
                    "@import 'abstracts/variables.scss'",
                    "@import 'abstracts/functions.scss'",
                    "@import 'abstracts/mixins.scss'",
                    "@import 'base/reset.scss'",
                    "@import 'base/typography.scss'",
                    "@import 'components/buttons.scss'",
                    "@import 'components/carousel.scss'",
                    "@import 'components/slider.scss'",
                    "@import 'layout/navigation.scss'",
                    "@import 'layout/grid.scss'",
                    "@import 'layout/header.scss'",
                    "@import 'layout/footer.scss'",
                    "@import 'layout/sidebar.scss'",
                    "@import 'layout/forms.scss'",
                    "@import 'pages/home.scss'",
                    "@import 'pages/about.scss'",
                    "@import 'pages/contact.scss'",
                    "@import 'themes/theme.scss'",
                    "@import 'themes/admin.scss'",
                    "@import 'vendors/bootstrap.scss'",
                    "@import 'vendors/jquery-ui.scss'",
                    ]
            )
            with open('sass/main.scss', "w+") as outfile:
                for e in files:
                    outfile.write(e)
                    outfile.writelines(';\n')

            print("\nSuccess!")
            break
    elif choice.lower() == 'a':
        try:
            os.mkdir('sass')
        except FileExistsError:
            print("\nThe sass folder already exists.\n\nThe following files have been added to the sass directory if they did not already exist.")
        finally:
            print('\n')
            files = ['sass/_base.scss', 'sass/_components.scss',
                        'sass/_layouts.scss', 'sass/main.scss']
            for e in files:
                print(e)
            open('sass/_base.scss', "a")
            open('sass/_components.scss', "a")
            open('sass/_layout.scss', "a")
            files = (["// Add any additional imports here", "@import 'base.scss'",
                        "@import 'components.scss'", "@import 'layout.scss'"])
            with open('sass/main.scss', "w+") as outfile:
                for e in files:
                    outfile.write(e)
                    outfile.writelines(';\n')

            print("\nSuccess!")
            break

    elif choice.lower() == 'q':
        break