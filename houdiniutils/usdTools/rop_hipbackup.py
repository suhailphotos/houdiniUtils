org_file_path = hou.hipFile.path() #set the original houdini file path
org_file_name = hou.hipFile.basename() #grab the original houdini file name and exentionsion

rop_path = hou.node(".").parm("lopoutput").eval() #grab the usd rop path

split_path = rop_path.split("/") #create array of strings to remove file name
to_replace = split_path[-1] #identify .usd file string

remove_ext = org_file_name.split(".") #create array of strings to remove .hip extension
hipname = org_file_name.replace("." + remove_ext[-1], "") #removes whatever .hip extension is being used

data_path = "data/" + hipname + "/" #determine path for backup .hipfile
new_file_path = rop_path.replace(to_replace, data_path) #creates filepath for new hipfile

from pathlib import Path
Path(new_file_path).mkdir(parents=True, exist_ok=True) #creates folders if they do not exist

new_hipfile = new_file_path + org_file_name # combine the new file path with the current hip file name

hou.hipFile.save(file_name=new_hipfile, save_to_recent_files=False) #write out backup
hou.hipFile.setName(org_file_path) #restore current

print("The following backup file has been saved: " + new_hipfile)