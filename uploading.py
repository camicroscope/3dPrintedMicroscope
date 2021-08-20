from Lens_movement import hardware_action
from flask import render_template,Flask
from flask_cors import CORS
from flask import jsonify
import re
from io import BytesIO
from PIL import Image
import base64
import os
from template_matching import match_common_region
from flask import request,make_response,redirect
from logs import make_log,get_data_rec,get_file_name,get_three_anchor_coordinates
import urllib.request
import datetime
import time
import numpy as np

app=Flask(__name__)
CORS(app)

#Redirect to
redirect_to_client=None

#global variables
CHANCE=''
SLIDEID=''
filename=''
final_stage_coordinates={}
redirect_to_client=''

app.config['TEMPLATES_AUTO_RELOAD']=True

#WSI image params
params={}

#Directory to store the wsi images
wsi_dir="./static/wsi_images/"

#Directory to store the stage images
stage_dir="./static/stage_images/"

@app.route("/")
def index():
    return render_template("demo.html")


@app.route("/preview_two_images/",methods=["GET","POST"])
def confirm_registration():
    global SLIDEID
    global CHANCE
    image1=get_file_name(SLIDEID,str(CHANCE),'stage')
    image2=get_file_name(SLIDEID,str(CHANCE),'wsi')
    print(image1)
    print(image2)
    return render_template("display.html",path1="../static/stage_images/"+image1,path2="../static/matching_region/"+image2)
    

        

@app.route("/take_wsi_image",methods=["POST"])
def take_wsi_image():
        global filename
        global redirect_to_client
        
        print('yes')
        print(request.form['information'])
        image_url=request.form['wsi_file']
        extract=request.form['information']
        extract=extract.split('-')
        print("image url")
        print(image_url)
        #redirect_to_client=request.form['redirect_to']
        
        params['x']=float(extract[0])
        params['y']=float(extract[1])
        params['width']=float(extract[2])
        params['height']=float(extract[3])
        params['name']=extract[4]
        slideid,wsi,step=params['name'].split("_")
        SLIDEID=slideid
        CHANCE=step
        #chance=slideid+"_"+step
        timestamp=time.time()
        timestamp=datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d-%H:%M:%S')
        filename=params['name']+"_"+timestamp+".png"
        urllib.request.urlretrieve(image_url,wsi_dir+filename)
        
        #image_data=re.sub('^data:image/.+;base64,','',encoded_data)
        #im=Image.open(BytesIO(base64.b64decode(image_data)))
        #im.save(wsi_dir+params['name']+".png")
        #make_log([params['height'],params['width']],slideid,step,'registration'+step,wsi_dir,"wsi",params)
        redirect_to_client=request.form['redirect_to']
        return redirect(request.form['redirect_to'])


@app.route("/template_matching",methods=["POST"])
def template_match():
    global CHANCE
    global SLIDEID
    

    #CODE FOR TEMPLATE MATCHING
    which_slide=request.form['slideid-value'].split('-')
    print(which_slide)
    get_stage_file=get_file_name(which_slide[0],which_slide[1],"stage")
    
    #stage_image=stage_dir+which_slide[0]+"_stage_"+which_slide[1]+".png"
    wsi_image=filename
    coordin={}
    if os.path.exists(stage_dir+get_stage_file) and os.path.exists(wsi_dir+wsi_image):
        print("stage_file",get_stage_file)
        print("wsi_file",wsi_image)
        coordin=match_common_region(stage_dir+get_stage_file,wsi_dir+wsi_image,0,request.form['slideid-value'])
    print("in uploading",coordin)
    if coordin!={}:
        
        height=coordin["endY"]-coordin["startY"]
        width=coordin["endX"]-coordin["startX"]

        slideid,wsi,step=params['name'].split("_")
        params['x']=params['x']+coordin['startX']
        params['y']=params['y']+coordin['startY']
        params['width']=width
        params['height']=height
        params['center_x']=params['x']+ float(width/2)
        params['center_y']=params['y']+float(height/2)

        CHANCE=step
        SLIDEID=slideid
        make_log([height,width],slideid,step,'registration'+step,wsi_dir,"wsi",coordin['filename'],params)
    
    return redirect(redirect_to_client)


@app.route("/get_coordinates_data/",methods=["GET","POST"])
def get_coordiates_data():

    data=get_data_rec(SLIDEID,str(CHANCE))
    if data['wsi_x']==0 and data['wsi_y']==0 and data['stage_x']==0 and data['stage_y']==0:
        data['status']="false"
    else:
        data['status']="true"
    data['step']=CHANCE
    return jsonify(data)

@app.route("/final_confirmation",methods=["POST"])
def final_confirmation():
    global final_stage_coordinates
    #calculate the transformation and represent in a matrix format
    #new wsi points as an input from client

    #output is calculated stage points
    x_new_wsi=float(request.form['x-coord-wsi'])
    y_new_wsi=float(request.form['y-coord-wsi'])
    
    wsi_coordi=np.array([x_new_wsi,y_new_wsi])

    
    
    coordinates=get_three_anchor_coordinates('60df2c463aaaa80033cd72fb')
    point1=coordinates['anchor1']
    point2=coordinates['anchor2']
    point3=coordinates['anchor3']
    matrix1=[[point2['wsi_x']-point1['wsi_x'],point3['wsi_x']-point1['wsi_x']],[point2['wsi_y']-point1['wsi_y'],point3['wsi_y']-point1['wsi_y']]]
    matrix2=[[point2['stage_x']-point1['stage_x'],point3['stage_x']-point1['stage_x']],[point2['stage_y']-point1['stage_y'],point3['stage_y']-point1['stage_y']]]

    wsi_1_coordi=np.array([point1['wsi_x'],point1['wsi_y']])
    stage_1_coordi=np.array([point1['stage_x'],point1['stage_y']])
    
    matrix_wsi=np.array(matrix1)
    matrix_stage=np.array(matrix2)

    inverse=np.linalg.inv(matrix_wsi)
    subtract= np.subtract(wsi_coordi,wsi_1_coordi)
    inverse_sub_mul= inverse @ subtract
    stage_inverse_mul = matrix_stage @ inverse_sub_mul

    
    stage_coord = np.add(stage_inverse_mul,stage_1_coordi)

    final_stage_coordinates['stage_x']=stage_coord[0]
    final_stage_coordinates['stage_y']=stage_coord[1]
    
    print(final_stage_coordinates)
    return redirect(request.form['redirect_to'])
    
@app.route("/return_calculated_coordinates/",methods=['POST','GET'])
def return_calculated_coordinates():
    if(final_stage_coordinates!={}):
        pres_pos=open('present_position.txt','r')
        pres_pos=pres_pos.read()
        coordinates_pres=pres_pos.split(' ')
        print(coordinates_pres)
        print(type(coordinates_pres[0]))
        x=float(coordinates_pres[0])
        y=float(coordinates_pres[1])

        print(x,y)
        hardware_action(x,y,40,int(final_stage_coordinates['stage_x']),int(final_stage_coordinates['stage_y']),40)
        file=open('present_position.txt','w')
        file.write(str(final_stage_coordinates['stage_x'])+" "+str(final_stage_coordinates['stage_y']))
        return jsonify(final_stage_coordinates)
    else:
        return jsonify({"stage_x":0,"stage_y":0})
    
if __name__ == '__main__':
    app.jinja_env.auto_reload=True
    app.config['TEMPLATES_AUTO_RELOAD']=True
    app.run(host="0.0.0.0",port=8020)
