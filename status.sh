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

echo "--------------------------------------------------------------------------------------------------"
echo "Diagnosing the NASA ISAAC User Interface"
echo "--------------------------------------------------------------------------------------------------"

if [ $(docker container ls | grep idi_frontend | wc -l) -lt 1 ]; then
    echo "ERROR! The ISAAC UI frontend is not running correctly."
    exit 1
fi

if [ $(docker container ls | grep idi_backend | wc -l) -lt 1 ]; then
    echo "ERROR! The ISAAC UI backend is not running correctly."
    exit 1
fi

if [ $(docker container ls | grep idi_arangodb | wc -l) -lt 1 ]; then
    echo "ERROR! The ISAAC UI database is not running correctly."
    exit 1
fi

if [ $(docker container ls | grep rosbridge | wc -l) -lt 1 ]; then
    echo "ERROR! The ISAAC UI ROS Bridge node is not running correctly."
    exit 1
fi

if [ $(docker container ls | grep rosvideo | wc -l) -lt 1 ]; then
    echo "ERROR! The ISAAC UI ROS Video node is not running correctly."
    exit 1
fi

echo "All ISAAC UI Docker containers appear to be running."