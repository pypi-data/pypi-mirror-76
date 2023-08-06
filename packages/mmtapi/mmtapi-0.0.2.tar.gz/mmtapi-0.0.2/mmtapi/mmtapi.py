import os, json, requests, re
from . import MMT_JSON_KEYS, MMT_CATALOG_ID, MMT_PROGRAM_ID, MMT_REQUIRED_KEYS, isInt, isFloat

class api():

    def __init__(self, target=None, token=None):

        self.base = 'https://scheduler.mmto.arizona.edu/APIv2'
        self.target = target

        if token is None:
            self.token = os.getenv('MMT_API_TOKEN')
        else:
            self.token = token

        self.request = None


    def build_url(self):
        assert self.target is not None, 'Target cannot be None'
        self.url = '{}/{}'.format(self.base, self.target)


    def post(self, d_json):
        self.build_url()
        self.request = requests.post(self.url, json=d_json)


    def get(self, d_json):
        self.build_url()
        r = requests.get(self.url+'/'+str(d_json['targetid']))
        self.request = r
        return r


    def put(self, d_json):
        self.build_url()
        r = requests.put(self.url+'/'+str(d_json['targetid']), json=d_json)
        self.request = r
        return r


    def delete(self, d_json):
        self.build_url()
        self.request = requests.delete(self.url+'/'+str(d_json['targetid']))


    def post_finder(self, data, files):
        self.build_url()
        self.request = requests.post(self.url+'/'+str(data['target_id']), data=data, files=files)


class Target():
    def __init__(self, token=None, verbose=True, payload={}):
        
        self.verbose = verbose
        ##### temporary #####
        self.catalogid = MMT_CATALOG_ID
        self.programid = MMT_PROGRAM_ID
        self.valid = False
        ##### eeeeeeeee #####

        assert token is not None, 'Token cannot be None'
        self.api = api('catalogTarget', token)

        allowed_keys = list(MMT_JSON_KEYS)
        self.__dict__.update((str(key).lower(), value) for key, value in payload.items() if str(key).lower() in allowed_keys)
        
        if 'targetid' in payload.keys():
            self.targetid = payload['targetid']
            self.get()

        self.validate(verbose=self.verbose)

    def validate(self, verbose=True):
        selfkeys = self.__dict__.keys()
        selfdict = self.__dict__
        errors, warnings = [], []

        #validating required keys
        if 'ra' in selfkeys:
            ra = selfdict['ra']
            r = re.compile('.{2}:.{2}:.{2}\.*')
            if not r.match(ra):
                errors.append('Invalid format for field \'ra\' ['+ra+']. Valid format is dd:dd:dd.d')
        else:
            errors.append('Field \'ra\' is required. Valid format is dd:dd:dd.d')

        if 'dec' in selfkeys:
            dec = selfdict['dec']
            r = re.compile('.{2}:.{2}:.{2}\.*')
            isNeg = dec.startswith('-')
            if '-' in dec:
                dec = dec.split('-')[1]
            if '+' in dec:
                dec = dec.split('+')[1]
            if not r.match(dec):
                errors.append('Invalid format for field \'dec\' ['+dec+']. Valid format is [+/-]dd:dd:dd.d')
            dec = '-' + dec if isNeg else '+' + dec
            self.__dict__.update({'dec':dec})

        else:
            errors.append('Field \'dec\' is required. Valid format is [+/-]dd:dd:d.d')

        if 'observationtype' in selfkeys:
            observationtype = selfdict['observationtype']
            if observationtype not in ['longslit', 'imaging', 'mask']:
                errors.append('Field \' observationtype\' must be either \'imaging\', \'longslit\', or \'mask\'')
            if observationtype == 'longslit':
                if 'grating' in selfkeys:
                    grating = selfdict['grating']
                    if grating not in ['270', 270, '600', 600, '1000', 1000]:
                        errors.append('For observationtype longslit, valid options for field \'grating\' are \'270\', \'600\', and \'1000\'')
                    if 'centralwavelength' in selfkeys:
                        centralwavelength = selfdict['centralwavelength']
                        if isFloat(centralwavelength):
                            cw = float(centralwavelength)
                            if grating in ['270', 270] and not (cw >= 5501 and cw <= 7838):
                                errors.append('For \'grating\' = 270: valid centralwavelength ['+str(centralwavelength)+'] must be between 5501-7838 Angstroms')
                            if grating in ['600', 600] and not (cw >= 5146 and cw <= 8783):
                                errors.append('For \'grating\' = 600: valid centralwavelength ['+str(centralwavelength)+'] must be between 5501-7838 Angstroms')
                            if grating in ['1000', 1000] and not ((cw >= 4108 and cw <= 4683) or (cw >= 5181 and cw <= 7273) or (cw >= 7363 and cw <= 7967) or (cw >= 8153 and cw <= 8772) or (cw >= 8897 and cw <= 9279)):
                                errors.append('For \'grating\' = 1000: valid centralwavelength must be between 4108-4683, 5181-7273, 7363-7967, 8153-8772 or 8897-9279')
                        else:
                            errors.append('Field \'centralwavelength\' must be float')
                    else:
                        errors.append('For observationtype: longslit, field \'centralwavelength\' is required \n \
                            Valid options are dependent on the field \'grating\' \n \
                            \'grating\' = 270: valid centralwavelength must be between 5501-7838 Angstroms \n \
                            \'grating\' = 600: valid centralwavelength must be between 5146-8783 Angstroms \n \
                            \'grating\' = 1000: valid centralwavelength must be between 4108-4683, 5181-7273, 7363-7967, 8153-8772 or 8897-9279')

                else:
                    errors.append('Field \'grating\' is required for observationtype: longslit \n \
                        Valid options are \'270\', \'600\', and \'1000\'')

                if 'slitwidth' in selfkeys:
                    slitwidth = selfdict['slitwidth']
                    if slitwidth not in ['Longslit0_75', 'Longslit1', 'Longslit1_25', 'Longslit1_5', 'Longslit5']:
                        errors.append('Field \'slitwidth\' valid options are: Longslit0_75, Longslit1, Longslit1_25, Longslit1_5, and Longslit5')
                else:
                    errors.append('For observationtype: longslit, field \'slitwidth\' is required. Valid options are: Longslit0_75, Longslit1, Longslit1_25, Longslit1_5, and Longslit5')


            if observationtype == 'imaging':
                self.__dict__.update({'centralwavelength':None})
                self.__dict__.update({'grating':None})

            if 'filter' in selfkeys:
                filt = selfdict['filter']
                if observationtype == 'imaging' and filt not in ['g', 'r', 'i', 'z']:
                    errors.append('For observationtype: imaging, valid options for field \'filter\' are: \'g\', \'r\', \'i\', and \'z\'.')
                if observationtype == 'longslit' and filt not in ['LP3800', 'LP3500']:
                    warnings.append('For observationtype: longslit, valid options for field \'filter\' are: \'LP3800\' and \'LP3500\' \n \
                                    Default setting \'filter\' to \'LP3800\'')
            else:
                if observationtype == 'longslit':
                    self.__dict__.update({'filter':'LP3800'})
                errors.append('Field \'filter\' is required for observation types \'imaging\' and \'longslit\' \n \
                               For imaging: valid options are \'g\', \'r\', \'i\', and \'z\'. \n \
                               For longslit: valid options are \'LP3800\' (default) and \'LP3500\'')

            if 'onevisitpernight' not in selfkeys:
                if observationtype == 'imaging':
                    self.__dict__.update({'onevisitpernight':0})
                if observationtype == 'longslit':
                    self.__dict__.update({'onevisitpernight':1})
            else:
                onevisitpernight = selfdict['onevisitpernight']
                if onevisitpernight not in [0, 1]:
                    errors.append('Field \'onevisitpernight\' must be either 0 or 1')
                
        else:
            errors.append('Field \'observationtype\' is required. Valid values are \'longslit\', \'imaging\', and \'mask\'')
        
        if 'epoch' not in selfkeys:
            warnings.append('Field \'epoch\' default set to 2000.0')
            self.__dict__.update({'epoch':2000.0})

        if 'exposuretime' in selfkeys:
            exposuretime = selfdict['exposuretime']
            if not isInt(exposuretime):
                errors.append('Field \'exposuretime\' valid format is integer (seconds)')
            elif not int(exposuretime) > 0:
                errors.append('Field \'exposuretime\' must be greater than zero you dingus')
        else:
            errors.append('Field \'exposuretime\' is required. Valid format is integer (seconds)')

        if 'instrumentid' in selfkeys:
            instrumentid = selfdict['instrumentid']
            if instrumentid not in [16, '16']:
                errors.append('Only supported instrument is Binospec: instrumentid=16')
        else:
            warnings.append('Only supported instrument right now is Binospec: setting instrumentid to 16')
            self.__dict__.update({'instrumentid':'16'})
        
        if 'magnitude' in selfkeys:
            magnitude = selfdict['magnitude']
            if not isFloat(magnitude):
                errors.append('Invalid format for field \'magnitude\'. Must be decimal/float')
        else:
            errors.append('Field \'magnitude\' is required for requested Target')

        if 'maskid' in selfkeys:
            maskid = selfdict['maskid']
            if not isInt(maskid):
                errors.append('Field \'maskid\' must be integer')
        else:
            errors.append('Field \'maskid\' is required \n \
                There are common mask ids for imaging/longslit slitwidths: \n \
                ----For imaging: 110 \n \
                ----Longslit0_75: 113 \n \
                ----Longslit1: 111 \n \
                ----Longslit1_25: 131 \n \
                ----Longslit1_5: 114 \n \
                ----Longslit5: 112')
            
        if 'numberexposures' in selfkeys:
            numberexposures = selfdict['numberexposures']
            if not isInt(numberexposures):
                errors.append('Field \'numberexposures\' must be integer')
        else:
            warnings.append('Field \'numberexposures\' is required. Setting value to 1')
            self.__dict__.update({'numberexposures':1})
        
        if 'objectid' in selfkeys:
            objectid = selfdict['objectid']
            if len(objectid) < 2 or len(objectid) > 50:
                errors.append('Field \'objectid\' must have a string length greater than 2 and less than 50.')
            if any(c for c in objectid if not c.isalnum() and not c.isspace()):
                errors.append('Field \'objectid\' must be alphanumeric and not contain any spaces')
        else:
            errors.append('Field \'objectid\' is required. ')

        if 'pa' in selfkeys:
            pa = selfdict['pa']
            if not isFloat(pa):
                errors.append('Field \'pa\' must be float and between -360.0 and 360.0')
            elif not (float(pa) >= -360 and float(pa) <= 360):
                errors.append('Field \'pa\' must be between -360 and 360')
        else:
            warnings.append('Field \'pa\' is set to 0.0')
            self.__dict__.update({'pa':0.0})

        if 'pm_dec' in selfkeys:
            pm_dec = selfdict['pm_dec']
            if not isFloat(pm_dec):
                errors.append('Field \'pm_dec\' must be float')
        else:
            warnings.append('Field \'pm_dec\' is set to 0')
            self.__dict__.update({'pm_dec':0.0})

        if 'pm_ra' in selfkeys:
            pm_ra = selfdict['pm_ra']
            if not isFloat(pm_ra):
                errors.append('Field \'pm_ra\' must be float')
        else:
            warnings.append('Field \'pm_ra\' is set to 0')
            self.__dict__.update({'pm_ra':0.0})

        if 'priority' in selfkeys:
            priority = selfdict['priority']
            if not isInt(priority):
                errors.append('Field \'priority\' must be an integer. Valid options are 1,2,3 where 1 is highest priority')
            elif priority not in [1, 2, 3, '1', '2', '3']:
                errors.append('Field \'priority\' valid options are 1,2,3 where 1 is highest priority')
        else:
            warnings.append('Field \'priority\' set to lowest value: 3')
            self.__dict__.update({'priority':3})

        if 'visits' in selfkeys:
            visits = selfdict['visits']
            if not isInt(visits):
                errors.append('Field \'visits\' must be an integer')
        else: 
            warnings.append('Field \'visits\' is set to 1')
            self.__dict__.update({'visits':1})

        #validating nonrequired fields and default values for Binospec

        if 'photometric' in selfkeys:
            photometric = selfdict['photometric']
            if not isInt(photometric):
                errors.append('Field \'photometric\' must be integer. \n \
                    0 = photometric conditions not required. \n \
                    1 = photometric conditions required.')
        else:
            self.__dict__.update({'photometric':0})

        if 'targetofopportunity' in selfkeys:
            too = selfdict['targetofopportunity']
            if not isInt(too):
                errors.append('Field \'targetofopportunity\' must be integer. \n \
                    0 = not a target of opportunity. \n \
                    1 = target of opportunity.')
        else:
            self.__dict__.update({'targetofopportunity':0})

        #Settings for limiting to only Binospec
        self.__dict__.update({'dithersize':None, 'gain':None, 'grism':None, 'moon':None, 'readtab':None})

        #Print out Errors and Warnings
        self.valid = (len(errors) == 0)
        if self.verbose:
            if not self.valid:
                print('INPUT TARGET ERRORS: ')
                for e in errors:
                    print(e)
                print()
            if len(warnings) > 0:
                print('INPUT TARGET WARNINGS: ')
                for w in warnings:
                    print(w)


    def dump(self):
        for d in self.__dict__:
            print('{}: {}'.format(d, self.__dict__[d]))
        print()


    def update(self, **kwargs):

        self.__dict__.update((key, value) for key, value in kwargs.items() if key in MMT_JSON_KEYS)
        self.validate()

        if self.valid:
            kwargs['targetid'] = self.__dict__['id']
            kwargs['catalogid'] = self.__dict__['catalogid']
            kwargs['token'] = self.api.token

            self.api.put(kwargs)
            r = self.api.request
            print(json.loads(r.text), r.status_code)

            if r.status_code == 200:
                self.__dict__.update((key, value) for key, value in json.loads(r.text).items())
            else:
                print('Something went wrong with the request. Envoke target.api.request to see request information')
        else:
            print('Invalid Target. Envoke target.validate() to see errors')


    def delete(self):
        data = {
            'token':self.api.token,
            'catalogid':self.__dict__['catalogid'],
            'targetid':self.__dict__['targetid']
        }
        self.api.delete(d_json=data)
        r = self.api.request
        if r.status_code == 200:
            print("Succesfully Deleted")
        else:
            print('Something went wrong with the request. Envoke target.api.request to see request information')
        if self.verbose:   
            print(json.loads(r.text), r.status_code)


    def post(self):
        if self.valid:
            payload = dict((key, value) for key, value in self.__dict__.items() if key in MMT_JSON_KEYS)
            payload['catalogid'] = self.catalogid
            self.api.post(payload)
            r = self.api.request
            if self.verbose:
                print(json.loads(r.text), r.status_code)
            if r.status_code == 200:
                    self.__dict__.update((key, value) for key, value in json.loads(r.text).items())
            else:
                print('Something went wrong with the request. Envoke target.api.request to see request information')
        else:
            print('Invalid Target parameters. Envoke target.validate() to see errors')

    def get(self):
        data = {
            'token':self.api.token,
            'catalogid':self.__dict__['catalogid'],
            'targetid':self.__dict__['targetid']
        }
        self.api.get(d_json=data)
        request = self.api.request
        r = json.loads(request.text)
        if request.status_code == 200:
            self.__dict__.update((key, value) for key, value in r.items())
        else:
            print('Something went wrong with the request. Envoke target.api.request to see request information')
            

    def upload_finder(self, finder_path):
        if self.valid:
            data = {
                'type':'finding_chart',
                'token':self.api.token,
                'catalog_id':str(self.__dict__['catalogid']),
                'program_id':str(self.__dict__['programid']),
                'target_id':str(self.__dict__['id']),
            }

            files = {
                'finding_chart_file': open(finder_path, 'rb')
            }

            self.api.post_finder(data, files)
            r = self.api.request
            if r.status_code == 200:
                self.__dict__.update((key, value) for key, value in json.loads(r.text).items())
            else:
                print('Something went wrong with the request. Envoke target.api.request to see request information')
            if self.verbose:
                print(json.loads(r.text), r.status_code)