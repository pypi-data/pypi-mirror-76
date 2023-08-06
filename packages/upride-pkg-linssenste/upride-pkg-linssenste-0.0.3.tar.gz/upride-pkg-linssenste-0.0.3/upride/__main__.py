import requests
import json
from geojson import LineString
import tqdm


class Upride(): 
    """
    This is the lightweight form of the Upride API aimed specifically for Python. 
    It can be used to query all trackers (and their meta information) all tracks 
    with the raw position data. The data can be returned as JSON or immediately 
    as GeoJSON. In addition, the individual requests offer the possibility to 
    use specific filter mechanisms

    Attributes
    ----------
    apiKey : str
        required API Authentication key (contact Upride for Access)
   
    Methods
    -------
    getTrackIMU(trackID, trackerID)
        Returns the aggregate, ordered and pre-processed IMU data from a dedicated track of a specific tracker
    
    getAllTrackers(min_numb_tracks=None)
        Returns all trackers in the associated campaign (defined by API tokens), where it is also filterable 
        by the minimum number of tracks
        
    getTrackByID(trackID, geojson=False) 
        Returns the data of a single specific track (after the trackID) as JSON, where GeoJSON can also be 
        specified as return type by the 'geojson=True' param
    
    getAllTracks(tracker=None, full_track=False, min_distance=None, max_distance=None, geojson=False)
        With this function the meta information (such as ID, length, duration, etc.) of each track in the 
        whole campaign is returned. You can filter by minimum and maximum length as well as by specific 
        trackers. Furthermore you can use the 'full_track=True' param to get the whole data as JSON and 
        also this data can be returned as GeoJSON using the "geojson=True" param
        
    """
    
    def __init__(self, apiKey):
        """
        Parameters
        ----------
        apiKey : str
            required API Authentication key (contact Upride for Access; mail: (steffen [at] upride [dot] io))
        """
        
        self.API_SCHEME = {
            'baseURL':    "https://api.upride.io/v1/query/", 
            'baseHeader': {'accept': 'application/json'},
            'auth':       ('?apiKey=' + apiKey),   
            'req': {
                'allTrackers': 'trackers',
                'trackByID':   'track/', 
                'allTracks':   'tracks'
            }
        }
    
    
    def __doRequest(self, uri, isJSON=True, full_url=False):
        """
        private help function to execute the requests
        
        Parameters
        ----------
        uri : str
            API node URI
        
        isJSON: bool, optional
            Optional param to return as raw text and not as parsed JSON (for newline JSON, like IMU)
        
        full_url: bool, optional
            Optional for specific request where URL is prebuild
        
        """
        
        # Request URL 
        if not full_url:
            reqURL = self.API_SCHEME['baseURL'] + uri + self.API_SCHEME['auth']
        
        else: 
            reqURL = uri
        try: 
            apiResp = requests.request("GET", reqURL, headers=self.API_SCHEME['baseHeader'])
            
        except: 
            return False
       
    
        if isJSON:
            return json.loads(apiResp.text.encode('utf8'))
        else: 
            return apiResp.text.encode('utf8')
            
            
            
    def __extractPoints(self, listData):
        """
        private help function to extract all Points as tuple array (for GeoJSON conversion)
        
        Parameters
        ----------
        listData : list
            list with track geodata
        
        """
        
        pointDataSet = []
        for pos in listData['points']: 
            pointDataSet.append(tuple((pos['lat'], pos['lng'])))
        
        return pointDataSet
    
    def getTrackIMU(self, trackID, trackerID): 
        """
        Returns the aggregate, ordered and pre-processed IMU data from a dedicated track of a specific 
        tracker. Note however, that not all Tracks have the IMU Data ready to access, if so, this function 
        returns False (we are working on that!)
        
        Parameters
        ----------
        trackID : str
            unique ID number of Track
        
        trackerID: str
            Tracker ID Number; must be the tracker of the trackID
        
        """
        
        reqURL = (                                         \
                    self.API_SCHEME['baseURL'] +           \
                    self.API_SCHEME['req']['trackByID'] +  \
                    trackID + "/imu" +                     \
                    self.API_SCHEME['auth'] +              \
                    '&tracker=' + trackerID                \
                 )
        
        imu_resp = self.__doRequest(reqURL, full_url = True, isJSON = False)

        if imu_resp == False or imu_resp == b'Track has no imu file.': 
            return False
        else: 
            imu_json = '['+ imu_resp.decode('utf-8').replace("\n", ",")
            imu_json = imu_json[:-1] + ']'

            return json.loads(imu_json)
      
    
    
    def getAllTrackers(self, min_numb_tracks=None): 
        """
        Returns all trackers in the associated campaign (defined by API tokens), where it is also filterable 
        by the minimum number of tracks
        
        Parameters
        ----------
        min_numb_tracks : int, optional
            minimum number of trackers a tracker must have to be returned

        """
        
        tracker_data = self.__doRequest((self.API_SCHEME['req']['allTrackers']))
        
        if tracker_data is not False: 
            if min_numb_tracks: 
                filtered_tr = []
                [filtered_tr.append(tr) for tr in trackerData if tr['count_tracks'] >= min_numb_tracks]
                tracker_data = filtered_tr
        
        return tracker_data
        
        
    
    def getTrackByID(self, trackID, geojson=False): 
        """
        Returns the data of a single specific track (after the trackID) as JSON, where GeoJSON can also be 
        specified as return type by the 'geojson=True' param
        
        Parameters
        ----------
        trackID : str
            unique ID number of Track
        
        geojson: bool, optional
            definition if output shall be JSON or GeoJSON

        """
        track_data = self.__doRequest((self.API_SCHEME['req']['trackByID'] + trackID))
        
        if track_data is not False:
            if geojson: 
                track_data = LineString(self.__extractPoints(track_data))
            
        return track_data
    
    
    
    
    def getAllTracks(self, tracker = None, full_track = False, min_distance = None, max_distance = None, geojson=False): 
        """
        With this function the meta information (such as ID, length, duration, etc.) of each track in the 
        whole campaign is returned. You can filter by minimum and maximum length as well as by specific 
        trackers. Furthermore you can use the 'full_track=True' param to get the whole data as JSON and 
        also this data can be returned as GeoJSON using the "geojson=True" param
        
        Parameters
        ----------
        tracker : str, optional
            if only tracks of a specific tracker is required provide tracker ID; if tracker is non existent 
            it returns all tracks
        
        full_track: bool, optional
            to not only get meta-information but also all points this param must bei True
            
        geojson: bool, optional
            definition if output shall be JSON or GeoJSON (if True, full_track param is set True)
        
        min_distance: int, optional
            minimum distance in meter of track to be returned (if higher than max_distance param Exception is raised)
        
        max_distance: int, optional
            maximum distance in meter of track to be returned (if lowe than min_distance param Exception is raised)
        """
        track_data = self.__doRequest((self.API_SCHEME['req']['allTracks']))
        
        if track_data is not False: 
            if tracker: 
                all_trackers = self.getAllTrackers()
                tracker_exists = False

                for tracker_type in all_trackers: 
                    if tracker == tracker_type['id']: 
                        tracker_exists = True
                        break

                if tracker_exists: 
                    tracker_data = []
                    for track in track_data:
                        if track['tracker'] == tracker:
                            tracker_data.append(track)

                    track_data = tracker_data

                else: 
                    print("Note: Tracker ID #" + tracker + " is non existend - returning all Tracks")



            # if a filter for distance was applied firstly filtering all datasets
            if min_distance or max_distance: 
                dist_filter_data = []

                if min_distance and max_distance and min_distance >= max_distance:
                    raise Exception('min_distance must be smaller and not bigger or equal than max_distance')

                for track in track_data: 
                    if (min_distance and track['distance'] >= min_distance):
                        if (max_distance and track['distance'] <= max_distance):
                            dist_filter_data.append(track)

                    elif (max_distance and track['distance'] <= max_distance):
                        if (min_distance and track['distance'] >= min_distance):
                            dist_filter_data.append(track)

                track_data = dist_filter_data

            if full_track or geojson:

                status_bar = tqdm.tqdm(total = len(track_data), desc='Track Requests', position=0)
                full_tracks = []
                for track in track_data: 
                    full_tracks.append(self.getTrackByID(track['id'], geojson = geojson))
                    status_bar.update(1)

                track_data = full_tracks

        
        return track_data
