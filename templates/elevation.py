import simplejson
import urllib

ELEVATION_BASE_URL = 'http://maps.googleapis.com/maps/api/elevation/json'

to add at the end of the elevation_base_url:
(locations="latitude,longitude",sensor="false",**elvtn_args):
  elvtn_args.update({

    })

      url = ELEVATION_BASE_URL + '?' + urllib.urlencode(elvtn_args)
      response = simplejson.load(urllib.urlopen(url))

# Create a dictionary for each results[] object
elevationArray = []

for resultset in response['results']:
  elevationArray.append(resultset['elevation'])


if __name__ == '__main__':
    getElevation()