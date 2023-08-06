# MMT API

This repository is designed to facilitate submitting a rapid Target of Opprotunity (ToO) observation to the [MMT](https://www.mmto.org/) with the goal to enable same-night spectroscopy of interesting transients. Here we will provide examples to install and upload targets.

## Install
To get the repository (in a bash/unix terminal)
```bash
pip3 install mmtapi
```

## Using the API Wrapper

Here we describe the process to POST, GET, UPDATE, and DELETE a MMT Target. The `Target` class also contains an `api` class that calls each of the API methods. This class contains the request information for each request method so that it can debugged in the command line. 

```python
import mmtapi.mmtapi as mmtapi

target = mmtapi.Target(token=API_TOKEN, ...)
#once a request is made

target.**action() #post, delete, update... etc

#the request response can be viewed by
t.api.request

#which contains all of the expected request response information:
#   t.api.request.content
#   t.api.request.text
#   t.api.request.status_code
#   etc
```

### Creating a Target

To create a target there are a lot of required fields and conditional parameters based on the observation type. To begin with the metadata for the target itself:

* `objectid`: This is the name of the target. The requirements for this field is that it contains no special characters and spaces. It must also be greater than 2 characters and less than 50 characters.
* `ra`: Right Ascension of the target. Required format to be: `dd:dd:dd.d`
* `dec`: Declination of the target. Required format to be: `[+/-]dd:dd:dd.d`
* `magnitude`: Magnitude of the target. Must be a `float`
* `epoch`: The epoch of the target. Defaults to 2000.0

The target exposure information is based on the the field `observationtype`:

For `observationtype:imaging`:
* `filter`: Must be `g`, `r`, `i`, or `z`
* `maskid`: can be `110` or a predefined mask set up prior to target request
* `exposuretime`: The observation exposure time in seconds

For `observationtype:longslit`:
* `grating`: Valid options are `270`, `600`, and `1000`
* `centralwavelength`: Depending on the chosen `grating`:
  * For `grating=270`, valid options are between `5501-7838`
  * For `grating=600`, valid options are between `5146-8783`
  * For `grating=1000`, valid options are between `4108-4683`, `5181-7273`, `7363-7967`, `8153-8772` or `8897-9279`
* `slitwidth`: valid options are `Longslit0_75`, `Longslit1`, `Longslit1_25`, `Longslit1_5`, `Longslit5`
* `filter`: valid options are `LP3800` or `LP3500`. Defaults to `LP3800`
* `maskid`: Can be a predefined mask, or there are common `maskid`s depending on the chosen slitwidth:
  * For `Longslit0_75`: id `113`
  * For `Longslit1`: id `111`
  * For `Longslit1_25`: id `131`
  * For `Longslit1_5`: id `114`
  * For `Longslit5`: id `112`

Other observation metadata:

* `pa`: The parralactic angle. Defaults to 0
* `pm_ra` and `pm_dec`: Proper motion of of the RA and DEC parameters. Defaults to 0.0 respectively
* `numberexposures`: Number of exposures. Defaults to 1
* `visits`: Visits. Defaults to 1
* `priority`: Ranks for all targets in the users catalog. Valid options are 1,2,3 where 1 is the highest priority. Defaults to 3
* `photometric`: Valid options are 0 for non-photometric conditions or 1 for photometric conditions. Defaults to 0
* `targetofopportunity`: Valid options are 0 for non ToO or 1 for requesting a ToO.

All metadata will be validated upon initialization. Once the target object has been validated as True, it can be posted to the MMT schedule.

```python
import mmtapi.mmtapi as mmtapi

#example for imaging target payload:

payload = {
  'objectid':'TARGETNAME',
  'ra':'12:34:56.78',
  'dec':'+87:65:43:21',
  'magnitude':21,
  'epoch':2000,
  'filter':g,
  'maskid':110,
  'exposuretime':400,
  'visits':1,
  'numberexposures':2,
  'priority':1
}


#example payload for longslit target payload

payload = {
  'objectid':'Targetname',
  'ra':'12:34:56.78',
  'dec':'+87:65:43:21',
  'magnitude':21,
  'epoch':2000,
  'grating':1000,
  'centralwavelength':7380,
  'slitwidth':'Longslit1_25',
  `maskid`:131,
  `filter`:'LP380'
  'visits':1,
  'numberexposures':2,
  'priority':1,
  'targetofopportunity':1
}

#this will create the target along with validating the payload information. It will inform the user of any errors or warnings associated with the metadata
target = mmtapi.Target(token=API_TOKEN, 
                       verbose=True, 
                       payload=payload)
#this will send the information to the scheduler if it is a valid target
target.post()
```

### Getting Target Information

To get Target Information the only parameters to be passed into the Target class initation are the `token` and `targetid`. This will populate the Target with all of the MMT Target's keywords. If the request is successful, print out all of the target information with the `.dump()` method.

```python
import mmtapi.mmtapi as mmtapi

target=mmtapi.Target(token=API_TOKEN,
                     verbose=True,
                     payload={'targetid':TARGETID})
target.dump()
```

### Uploading a Finder Image

Once a target is either created, or retrieved with the API GET method, a finder image can be uploaded. If an finder image already exists, this will overwrite it. All that is needed the pathway to the finder image.

```python
target.upload_finder(finder_path=PATH_TO_IMAGE)
```

### Updating Target Information

Once a target is created, or retrieved with the API GET method, its meta-data can be updated. All that is required is passing in the valid keyword arguments and their respective values. The updated information will be validated before being submitted to the API.

```python
#the kwargs can be defined as: KEY_WORD1=VAlUE1, KEY_WORD2=VALUE2... etc 
target.update(KEY_WORD1=VAlUE1, KEY_WORD2=VALUE2... etc)
```

Valid MMT Target `KEY_WORD`'s:

```python
[
  'id', 'ra', 'objectid', 'observationtype', 'moon', 'seeing', 'photometric', 'priority', 'dec', 'ra_decimal', 
  'dec_decimal', 'pm_ra', 'pm_dec', 'magnitude', 'exposuretime', 'numberexposures', 'visits', 
  'onevisitpernight', 'filter', 'grism', 'grating', 'centralwavelength', 'readtab', 'gain', 'dithersize', 
  'epoch', 'submitted', 'modified', 'notes', 'pa', 'maskid', 'slitwidth', 'slitwidthproperty', 'iscomplete',
  'disabled', 'notify', 'locked', 'findingchartfilename', 'instrumentid', 'targetofopportunity', 'reduced',
  'exposuretimeremaining', 'totallength', 'totallengthformatted', 'exposuretimeremainingformatted', 
  'exposuretimecompleted', 'percentcompleted', 'offsetstars', 'details', 'mask'
]
```

### Deleting a Target

Once a target is created or retireved with the API GET method, it can be deleted from the Observatory scheduler.

```python
target.delete()
```
