# solar_data_collection
A proof of concept to collect solar data from my sunsynk inverter as well as weather data. 

# Using modified code from [James Ridgway's sunsynk api git repo](https://github.com/jamesridgway/sunsynk-api-client):
Original code collects latest readings. 
Modifications aim to collect hostoric graph data.
API call urls can be found with the web developer network inspection tools on the sunsynk.net website. 

# you need to store your credentials in these enivornment vairables
`export SUNSYNK_USERNAME='name@domain.com'`

`export SUNSYNK_PASSWORD='your password'`

# install your python's SSL certificates
`Install certificates.command`

# Github actions
- Github action action.yaml triggers once a week 
- Action is on the main (default) branch of the repo 
    - must be on branch main to be picked-up by github or modified
- The action runs on the data branch 
    - make modifications here to non action items for the data run