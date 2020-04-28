# uniofcam-recipes
Autopkg recipes from University of Cambridge Apple Support Team.

## To use the PostProcessor

    autopkg repo-add https://github.com/ucam-apple-support/autopkg_recipes.git

    autopkg run --post=com.github.autopkg.ucam-apple-support.postprocessors/TeamsPostJSS --key=webhook_url="https://outlook.office.com/webhook/<rest_of_url>" GoogleChrome.jss.recipe 