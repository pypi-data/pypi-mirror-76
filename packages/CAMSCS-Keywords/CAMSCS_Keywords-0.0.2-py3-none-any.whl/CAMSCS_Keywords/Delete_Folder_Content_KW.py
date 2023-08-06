import os
import shutil

def DeleteFolderContent(FolderPath):
    for root, dirs, files in os.walk(FolderPath):
    	for f in files:
        	os.unlink(os.path.join(root, f))
    	for d in dirs:
        	shutil.rmtree(os.path.join(root, d))