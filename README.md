# File_Synchronizer
- This program synchronizes two folders: source and replica
- Synchronization is done one-way: after the synchronization content of the replica folder will be modified to exactly match content of the source folder
- Synchronization is performed periodically
- File creation/copying/removal operations are logged to a file and to the console output
# Usage
Folder paths, synchronization interval and log file path can be provided using the command line arguments
```
python3 fileSynchronizer.py --base_path=PATH_THAT_CONTAINS_TWO_FOLDERS_'source'_AND_'replica' --interval=SYNCHRONIZATION_INTERVAL_IN_MINUTE --log_path=PATH_TO_LOG_FILE
