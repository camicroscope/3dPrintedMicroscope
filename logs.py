import yaml
import datetime
import os

#Directory to store the log data
log_dir="./static/logs/"
def get_three_anchor_coordinates(SLIDEID):
        coordi={}
        coordi['anchor1']=get_data_rec(SLIDEID,"1")
        coordi['anchor2']=get_data_rec(SLIDEID,"2")
        coordi['anchor3']=get_data_rec(SLIDEID,"3")
        return coordi
def get_file_name(SLIDEID,STEP,chance):
        file=''
        if os.path.exists(log_dir+SLIDEID+".yaml"):
                with open(log_dir+SLIDEID+".yaml",'r') as stream:
                        parse=yaml.safe_load(stream)
                        pair=parse['info']['registration'+STEP]
                        if(chance=='stage'):
                                file=pair['stage_image'+STEP]['filename']
                        else:
                                file=pair['wsi_image'+STEP]['cropped-region-info']['filename']
        else:
                file='not_found'
        return file
                
                
def get_data_rec(SLIDEID,STEP):
        coordinates={}
        if os.path.exists(log_dir+SLIDEID+".yaml"):
                
                with open(log_dir+SLIDEID+".yaml",'r') as stream:
                        try:
                                parse=yaml.safe_load(stream)
                                pair=parse['info']['registration'+STEP]
                                wsi_data={}
                                stage_data={}
                                if 'wsi_image'+STEP in pair:
                                        wsi_data=pair['wsi_image'+STEP]
                                if 'stage_image'+STEP in pair:
                                        stage_data=pair['stage_image'+STEP]
                                print("wsi")
                                print(wsi_data)
                                print("stage")
                                print(stage_data)
                                if wsi_data!={} and 'center_x' in wsi_data['cropped-region-info']:
                                        coordinates['wsi_x']=wsi_data['cropped-region-info']['center_x']
                                        coordinates['wsi_y']=wsi_data['cropped-region-info']['center_y']
                                else:
                                        coordinates['wsi_x']=0
                                        coordinates['wsi_y']=0

                                if stage_data!={} and 'center_x' in stage_data:
                                        coordinates['stage_x']=stage_data['center_x']
                                        coordinates['stage_y']=stage_data['center_y']

                                else:
                                        coordinates['stage_x']=0
                                        coordinates['stage_y']=0
                                
                                
                        except yaml.YAMLError as exc:
                                print(exc,"has occured")
        else:
                coordinates['wsi_x']=0
                coordinates['wsi_y']=0
                coordinates['stage_x']=0
                coordinates['stage_y']=0

        return coordinates
                        
def insert_data_rec(iterable, search_key, data):

        print(search_key)
        print(iterable)
        if isinstance(iterable, list):

                for item in iterable:
                        if isinstance(item, (list, dict)):
                                insert_data_rec(item, search_key, data)

        elif isinstance(iterable, dict):
                print("dict instance")
                for k, v in iterable.items():
                        print("loop",k,v)
                        if k == search_key:
                                print(k)
                                print(iterable[k])
                                iterable[k].update(data)
                        if isinstance(v, (list, dict)):
                                insert_data_rec(v, search_key, data)
                                
def make_log(shape,name,step,key,dire,field,filename,params={}):
        timestamp=datetime.datetime.now()
        formated=timestamp.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        print(name)
        check=False
        if(os.path.exists(log_dir+name+".yaml")==False):
                print("updating again")
                print("------")
                print("------")
                with open(log_dir+name+".yaml","w") as f:
                        f.close()
        else:
                with open(log_dir+name+".yaml",'r') as stream:
                        data=yaml.safe_load(stream)
                        if "registration1" in data['info']:
                                check=True
                        
        if(field=="stage" and step=="1" and check==False):
                print(key)
                new_yaml_data_dict={
                        key:{
                                "registration"+str(step):{
                                        field+"_image"+step:{
                                        field+"_id":name+"_"+field+"_"+step,
                                        "moved_date":formated,
                                        "file_path":dire+name+"_"+field+"_"+step+".png",
                                        "height":shape[0],
                                        "width":shape[1],
                                        "center_x":params['x'],
                                        "center_y":params['y'],
                                        "filename":filename
                                    }
                                }

                    },
                "slideId":name

                }
                print("data:")
                print(new_yaml_data_dict)
                with open(log_dir+name+".yaml","w") as file:
                        sdump=yaml.dump(new_yaml_data_dict,default_flow_style=False,sort_keys=False)
                        file.write(sdump)
                        file.close()
        else:
                with open(log_dir+name+".yaml") as yml_file:
                        print("else section")
                        data=yaml.safe_load(yml_file)
                        value={}
                        if(field=="stage"):
                                value={
                                        "registration"+step:{
                                                field+"_image"+step:{
                                                        field+"_id":name+"_"+field+"_"+step,
                                                        "moved_date":formated,
                                                        "file_path":dire+name+"_"+field+"_"+step+".png",
                                                        "height":shape[0],
                                                        "width":shape[1],
                                                        "center_x":params['x'],
                                                        "center_y":params['y'],
                                                        "filename":filename
                                                }
                                        }

                                }
                        else:
                                value={
                                        field+"_image"+step:{
                                                field+"_id":name+"_"+field+"_"+step,
                                                "moved_date":formated,
                                                "file_path":dire+name+"_"+field+"_"+step+".png",
                                                "height":shape[0],
                                                "width":shape[1],
                                                "cropped-region-info":{
                                                   "top-left-x":params['x'],
                                                   "top-left-y":params['y'],
                                                   "width":params['width'],
                                                   "height":params['height'],
                                                   "center_x":params['center_x'],
                                                   "center_y":params['center_y'],
                                                   "filename":filename


                                                }
                                        }
                                }

                        insert_data_rec(data,search_key=key,data=value)
                        with open(log_dir+name+".yaml","w") as fp:
                                yaml.safe_dump(data,fp,default_flow_style=False,sort_keys=False)


#make_log((100,100),"example",1,"info","./static/stage_images/","stage")
#print("----------")
#make_log((100,100),"example",1,"registration1","./static/stage_images/","wsi")
#print("---section1")
#make_log((100,100),"example",2,"info","./static/stage_images/","stage")
#print("----------")
#smake_log((100,100),"example",2,"registration2","./static/stage_images/","wsi")
