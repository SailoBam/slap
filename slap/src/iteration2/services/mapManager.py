import json
import requests
from dotenv import load_dotenv
import os

class MapManager:


    def getGeoJson(self, waypoints):
        
        geojson = {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "LineString",
                "coordinates": waypoints
            }
        }

        return geojson

    def uploadToMapbox(self, dataset_name, readings):
        # Load credentials from .env file
        load_dotenv()
        access_token = os.getenv('MAPBOX_ACCESS_TOKEN')
        username = os.getenv('MAPBOX_USERNAME')

        # Get the GeoJSON
        geojson_data = self.getGeoJson(readings)
        print(geojson_data)

        # Create a new dataset
        dataset_url = f"https://api.mapbox.com/datasets/v1/{username}?access_token={access_token}"
        dataset_payload = {
            "name": dataset_name,
            "description": "Track with waypoints"
        }
        
        print(f"Creating dataset '{dataset_name}'...")
        response = requests.post(dataset_url, json=dataset_payload)
        
        if response.status_code not in [200, 201]:
            print(f"Failed to create dataset: {response.text}")
            return

        # Get the dataset ID from the response
        dataset_id = response.json()['id']
        print(f"Dataset created with ID: {dataset_id}")

        # Add an ID to the GeoJSON feature and upload it
        geojson_data['id'] = 'track1'
        feature_url = f"https://api.mapbox.com/datasets/v1/{username}/{dataset_id}/features/track1?access_token={access_token}"
        
        print("Uploading track data...")
        response = requests.put(feature_url, json=geojson_data)
        
        if response.status_code != 200:
            print(f"Failed to upload track: {response.text}")
            return

        print("\nTrack uploaded successfully!")
        print("\nView your track at:")
        print(f"https://studio.mapbox.com/datasets/{dataset_id}")