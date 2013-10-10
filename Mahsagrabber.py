import TwitterAPI
import json as json
from config import access_tokens
import os,sys
import time



def archive_endpoint(endpoint, name):
    print "[%s] Running archive_endpoint for %s" % (time.time(), endpoint)  #print statement to let me know the script is running in my log
    api = TwitterAPI.TwitterAPI(**access_tokens)

    params = { 'q' : 'xbox1','q' : 'xbox 1', 'q' : 'xboxone', 'q' : 'PS4', 'q' : 'playstation4','count' : 100}
    try:
        min_id = json.load(open("max_ID_%s" %name))
        params.update(min_id)
    except:
        print "This is the first time this has been run"
    print "Making request to twitter"
    updated_timeline = api.request(endpoint, params)
    data_file = time.strftime("%Y/%m/%d/%H-" + name)

    try:
        directory = os.path.dirname(data_file)
        os.makedirs(directory)
    except:
        print "directory already exists"

    new_id = 0

    print "saving data"
    with open(data_file, "a+") as fd:
        count = 0
        for item in updated_timeline.get_iterator():
            new_json = json.dumps(item) + '\n'
            fd.write(new_json)
            new_id = max(new_id, item['id'])
            count+=1
        print "saved %d items" % count

    if new_id:
        print " saving new_id = %d" % new_id
        future_load_value = {"since_id" : new_id}
        json.dump(future_load_value, open("max_ID_%s" % name, "w+"))

if __name__ == "__main__":
    archive_endpoint("search/tweets", "tweets")


