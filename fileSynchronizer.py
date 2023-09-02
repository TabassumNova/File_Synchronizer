import filecmp
import os
import shutil
import logging
import time
import argparse

class File_Synchronizer():
    def __init__(self, base_path, interval, log_path):
        self.base_path = base_path
        self.interval = int(interval)
        self.log_file = log_path
        self.source_folder = None
        self.replica_folder = None
        self.source_replica_folder()

        logging.basicConfig(filename=self.log_file,
                            filemode='a',
                            format='%(asctime)s %(levelname)s %(message)s',
                            level=logging.DEBUG)

        logging.info("Logging start")
        logging.info('Source folder: %s',self.source_folder)
        logging.info('Replica folder: %s', self.replica_folder)

        print("Logging start")
        print('Source folder: ', self.source_folder)
        print('Replica folder: ', self.replica_folder)

    def source_replica_folder(self):
        '''
        Find 'source' and 'replica' folders with in base_path
        '''
        for path, subdir, file in os.walk(self.base_path):
            for dir in subdir:
                if dir == 'source':
                    self.source_folder = os.path.join(self.base_path, dir)
                elif dir == 'replica':
                    self.replica_folder = os.path.join(self.base_path, dir)
        pass

    def start_synchronization(self):
        while True:
            self.match_folder_contents()
            time.sleep(self.interval*60)

    def match_folder_contents(self):
        # remove extra file/folder from replica folder
        for root, subdirs, files in os.walk(self.replica_folder):
            folder_name = root.split(self.replica_folder)[1]
            for dir in subdirs:
                if dir not in os.listdir(self.source_folder):
                    shutil.rmtree(os.path.join(self.replica_folder, dir))
                    logging.info("%s directory is removed from replica folder", dir)
                    print(dir, " directory is removed from replica folder")

            for filename in files:
                if filename not in os.listdir(self.source_folder+folder_name):
                    os.remove(os.path.join(self.replica_folder+folder_name, filename))
                    logging.info("%s file is removed from replica/%s folder", filename, folder_name)
                    print(filename, " file is removed from replica/",folder_name)


        # add/modify file/folder of replica folder
        for root, subdirs, files in os.walk(self.source_folder):
            folder_name = root.split(self.source_folder)[1]
            for dir in subdirs:
                if dir not in os.listdir(self.replica_folder):
                    os.mkdir(os.path.join(self.replica_folder, dir))
                    logging.info("New directory %s is created at replica folder", dir)
                    print("New directory", dir, " is created at replica folder")
                pass
            for filename in files:
                if filename in os.listdir(self.replica_folder+folder_name):
                    self.match_file_content(folder_name, filename)
                else:
                    source_file = os.path.join(self.source_folder+folder_name, filename)
                    replica_file = os.path.join(self.replica_folder+folder_name, filename)
                    shutil.copyfile(source_file, replica_file)
                    logging.info("%s file is copied from Source folder to Replica folder", filename)
                    print(filename, " file is copied from Source folder to Replica folder")
        pass



    def match_file_content(self, folder_name, filename):
        source_file = os.path.join(self.source_folder+folder_name, filename)
        replica_file = os.path.join(self.replica_folder+folder_name, filename)
        compare = filecmp.cmp(source_file, replica_file)
        if not compare:
            if os.path.isfile(replica_file):
                os.remove(replica_file)
                logging.info("%s file is deleted from Replica folder", filename)
                print(filename, " file is deleted from Replica folder")
            shutil.copyfile(source_file, replica_file)
            logging.info("%s file is copied from Source folder to Replica folder", filename)
            print(filename, " file is copied from Source folder to Replica folder")


if __name__ == "__main__":
    '''
    -> base_path : this path contains two folders named 'source' and 'replica'
    -> interval :  synchronization interval (minutes)
    -> log_path : log file path
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_path")
    parser.add_argument("--interval")
    parser.add_argument("--log_path")
    args = parser.parse_args()

    f = File_Synchronizer(args.base_path, args.interval, args.log_path)
    f.start_synchronization()
    pass

