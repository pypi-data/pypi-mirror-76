# make-sass-files

The make-sass-files script will give you the option to automate the creation of the Sass 7-1 or the Sass 3-1 file structure in your project. The 7-1 model is the recommended architecture for using Sass. The 3-1 model can be used for smaller projects such as single page applications (SPAs) 

The script will generate the following files:

**3-1** (option a)
   
    sass/_base.scss
    sass/_components.scss
    sass/_layouts.scss
    sass/main.scss


**7-1** (option b)

    sass/abstracts/_variables.scss
    sass/abstracts/_functions.scss
    sass/abstracts/_mixins.scss
    sass/base/_reset.scss
    sass/base/_typography.scss
    sass/components/_buttons.scss
    sass/components/_carousel.scss
    sass/components/_slider.scss
    sass/layout/_navigation.scss
    sass/layout/_grid.scss
    sass/layout/_header.scss
    sass/layout/_footer.scss
    sass/layout/_sidebar.scss
    sass/layout/_forms.scss
    sass/pages/_home.scss
    sass/pages/_about.scss
    sass/pages/_contact.scss
    sass/themes/_theme.scss
    sass/themes/_admin.scss
    sass/vendors/_bootstrap.scss
    sass/vendors/_jquery-ui.scss
    sass/main.scss
    
**Note**: The script will only install a path above if the path does not already exist in the project root. 

For example. Let's say you have a sass folder in the project root with the following files:

      sass/abstracts/_variables.scss
  
  The script will add the files below without altering the existing file:
  
      sass/abstracts/_functions.scss
      sass/abstracts/_mixins.scss


**Instructions**: 

**Step 1**: Install the package

          pip install make-sass-files
            
**Step 2**: Run the program

          python make-sass-files
          
**That's it!**


   
# make-sass-files

