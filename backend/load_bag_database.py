# Copyright © 2021, United States Government, as represented by the Administrator of the 
# National Aeronautics and Space Administration. All rights reserved.
#
# The “ISAAC - Integrated System for Autonomous and Adaptive Caretaking platform” software is 
# licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. 
#
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the 
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, 
# either express or implied. See the License for the specific language governing 
# permissions and limitations under the License.
#
# ----------------------------------------------------------------------------------------------------
# ISAAC Interface
# Backend API
# ----------------------------------------------------------------------------------------------------
# Database interface class definition
# ----------------------------------------------------------------------------------------------------


from pyArango.connection import *
import rosbag, sys
import yaml
from os import listdir
from os.path import isfile, join
import time

# roslibpy needs a logger in order to output errors inside callbacks
import logging
logging.basicConfig()

class LoadBagDatabase:
    def __init__(self, path, topics):
        # Initiate the connection to http://127.0.0.1:8529
        time.sleep(5)
        print("Database: Initiating connection")
        self.conn = Connection(arangoURL="http://localhost:8529", username="root", password="isaac")
        # Open the database
        if not self.conn.hasDatabase("isaac"):
            self.conn.createDatabase(name="isaac")
        self.db = self.conn["isaac"]

        #TODO Marina: Recursively look into bag directory
        # Check the folder contents
        bagfiles = [f for f in listdir(path) if f.endswith(".bag")]
        print("bagfiles" + str(bagfiles) + "\ntopics" + str(topics))
        for bag in bagfiles:
            self.read_bag(path + bag, topics)

    #TODO Marina: automatically joint bags split into different parts
    def read_bag(self, bag_file, topics_list):
        # access bag
        print("Reading bag file")
        bag = rosbag.Bag(bag_file)
        bag_contents = bag.read_messages()
        bagName = bag.filename

        # get list of topics from the bag
        bag_topics = []
        for topic, msg, t in bag_contents:
            if topic in topics_list:
                bag_topics.append(topic)
        print("List of topics " + str(bag_topics))

        # create a new collection with the bag name
        # collection name needs to start with a letter
        bagFile = "bag_" + bagFile[:-4]
        print("Creating collection " + bagFile)
        if not self.db.hasCollection("yo"):
            self.db.createCollection(name="yo")
        # ensure index
        self.db["yo"].ensureSkiplistIndex(["header.stamp.secs"])

        # open
        for topic_name in bag_topics:
            # Go through all the messages in a topic
            for subtopic, msg, t in bag.read_messages(topic_name):
                msg = yaml.safe_load(str(msg))

                aql = "INSERT " + str(msg) + " INTO " + "yo" + " LET newDoc = NEW RETURN newDoc"
                queryResult = self.db.AQLQuery(aql)
        bag.close()

# Database connection
if __name__ == "__main__":
    # Load yaml configuration file
    with open("config.yaml", "r") as f:
        configuration = yaml.safe_load(f)
    topics = [topic['name'] for topic in configuration['topics']]

    # Get folder where bag files are stored
    path = configuration["bag_path"]
    LoadBagDatabase(path, topics)