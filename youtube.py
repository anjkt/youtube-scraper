import requests
import csv
import json
import pandas as pd

#access_token for the api call
access_token = "PUT your Access Token Here"

#Reading the CSV with channel_ids
df1 = pd.read_csv('channel_ids.csv', sep=',') 
df2 = list(df1['handle_channelid']) #Header of the column the CSV with channel_ids

#open the CSV writer
with open('videos-id.csv', mode='w', newline='') as generated_csv:
    generated_writer = csv.writer(generated_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    generated_writer.writerow(['Channel-ID', 'Video-IDs'])
    #initiate the for loop to iterate total channel_ids
    for j in range(len(df2)):
        channel_id = df2[j]
        #Hitting the API by channel ID
        url_address = "https://www.googleapis.com/youtube/v3/activities?part=snippet,contentDetails&channelId="+channel_id+"&key=" + access_token + "&maxResults=50"
        url_content = requests.get(url_address)
        #Recievig the Response in JSON format
        file_new = url_content.json()
        length_arr = len(file_new["items"])
        print("\nSending Request for "+channel_id)
        #Use Channel ID to search VideoID
        for i in range(length_arr):
            a = "bulletin"
            b = "upload"
            #Channel has Video in the form of playlist
            if a in file_new["items"][i]["contentDetails"]:
                length = file_new["items"][i]['contentDetails']['bulletin']['resourceId']['videoId']
                generated_writer.writerow([channel_id,length])
            #Channel has Video as normal video
            elif b in file_new["items"][i]["contentDetails"]:
                length = file_new["items"][i]['contentDetails']['upload']['videoId']
                generated_writer.writerow([channel_id,length])
            #Channel has No Video
            else:
                generated_writer.writerow([channel_id,"null"])
        print(" Recieved Response from "+channel_id)
    
    print("Data Written on CSV. Thank you")
