import os
from ftplib import FTP
import datetime
import dateparser as parser

# Define Remote Host and local folder
remote_host = "tgftp.nws.noaa.gov"
remote_user = "anonymous"
remote_password = "anonymous"
remote_directory = "/data/observations/metar/stations"
local_metar_directory = "./METARS"

# Create Local folder METARS if not existing
if not os.path.exists(local_metar_directory):
    os.mkdir(local_metar_directory)
# Move into the new created folder
os.chdir(local_metar_directory)

# Connect to the FTP server
ftp = FTP(remote_host)
ftp.login(remote_user, remote_password)

# Navigate into the remote directory and store the content in the file_list list
file_list = []
ftp.dir(remote_directory, file_list.append)
ftp.cwd(remote_directory)
# Extract date and filename for each item on the list
for file in file_list:
    # Split the string
    token = file.split(maxsplit=9)

    # define filename
    filename = token[8]
    # Extract date and time and convert to datetime format
    time_str = f'{token[5]} {token[6]} {token[7]}'
    time = parser.parse(time_str)
    # Define datetime we are interested in
    file_to_download = datetime.datetime.utcnow() - datetime.timedelta(minutes=60)

    # Download files if they have been uploaded less than 60 minutes ago
    if time > file_to_download and time <= datetime.datetime.utcnow():
        try:
            ftp.retrbinary("RETR " + filename, open(filename, "wb").write)
        except Exception as e:
            print(f'Could not download {filename} due to: \n {e}')

# Once done close connection
ftp.quit()

# I forgot an important thing... move into the remote directory to download Data

# NOW WE ARE READY TO TEST OUR SCRIPT

## IT WORKSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
