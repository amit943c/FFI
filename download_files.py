import os
import csv
import time
import requests
import boto3
import base64
import uuid
from botocore.config import Config
from botocore.exceptions import ClientError
from PIL import Image

celebrity_gender_map = {
    "riteish_deshmukh": "male",
    "akshay_kumar": "male",
    "imran_khan": "male",
    "govinda": "male",
    "shahid_kapoor": "male",
    "b_praak": "male",
    "r_madhavan": "male",
    "hrithik_roshan": "male",
    "ranveer_singh": "male",
    "tiger_shroff": "male",
    "sanjay_dutt": "male",
    "arjun_rampal": "male",
    "anupam_kher": "male",
    "ajay_devgn": "male",
    "saif_ali_khan": "male",
    "john_abraham": "male",
    "salman_khan": "male",
    "anil_kapoor": "male",
    "virat_kohli": "male",
    "aftab_shivdasani": "male",
    "shahrukh_khan": "male",
    "arjun_kapoor": "male",
    "bobby_deol": "male",
    "prabhas": "male",
    "abhimanyu": "male",
    "allu_arjun": "male",
    "rishi_kapoor": "male",
    "dilip_kumar": "male",
    "vinod_khanna": "male",
    "raj_kumar": "male",
    "dharmendra": "male",
    "sunny_deol": "male",
    "karan_deol": "male",
    "abhay_deol": "male",
    "aryan_khan": "male",
    "boman_irani": "male",
    "farhan_akhtar": "male",
    "ibrahim_ali_khan": "male",
    "farah_khan": "male",
    "sohail_khan": "male",
    "rajkummar_r": "male",
    "jimmy_shergill": "male",
    "rohit_suresh_saraf": "male",
    "ayushmann_khurrana": "male",
    "fardeen_khan": "male",
    "vivek_oberoi": "male",
    "vatsal_sheth": "male",
    "riteish_deshmukh": "male",
    "ratan_tata": "male",
    "karan_tacker": "male",
    "pulkit_samrat": "male",
    "suriya": "male",
    "irrfan_khan": "male",
    "sonu_nigam": "male",
    "mithun_chakraborty": "male",
    "aditya_roy_kapur": "male",
    "vijay": "male",
    "ram_charan_teja": "male",
    "amitabh_bachchan": "male",
    "amitabh_bachann": "male",
    "akshay_kumar": "male",
    "emraan_hashmi": "male",
    "vidyut_dev_singh_jammwal": "male",
    "sivakarthikeyan": "male",
    "chiranjeevi": "male",
    "sooraj_pancholi": "male",
    "tusshar_kapoor": "male",
    "ishaan_khattar": "male",
    "ali_fazal": "male",
    "mahesh_babu": "male",
    "karan_singh_grover": "male",
    "harshvardhan_rane": "male",
    "aamir_khan": "male",
    "rajeev_khandelwal": "male",
    "zayed_khan": "male",
    "sunny_singh": "male",
    "dino_morea": "male",
    "amit_sadh": "male",
    "fawad_khan": "male",
    "randeep_hooda": "male",
    "prabhu_deva": "male",
    "chunkey_pandey": "male",
    "akshaye_khanna": "male",
    "shaan": "male",
    "atif_aslam": "male",
    "rahul_bajaj": "male",
    "kailash_kher": "male",
    "kk": "male",
    "abhishek_bachchan": "male",
    "kapil_dev": "male",
    "m_s_dhoni": "male",
    "nakul_mehta": "male",
    "nawazuddin_siddique": "male",
    "rohit_sharma": "male",
    "yuvraj_singh": "male",
    "prince_narula": "male",
    "parmish_varma": "male",
    "anu_kapoor": "male",
    "jaani": "male",
    "amrinder_gill": "male",
    "bhuvam_bam": "male",
    "ajey_nagar": "male",
    "aashish_chanchlani": "male",
    "prajakta": "male",
    "gaurav_taneja": "male",
    "gaurav_choudhary": "male",
    "sajid_khan": "male",
    "salim": "male",
    "jay": "male",
    "karan": "male",
    "aditya_narayan": "male",
    "manish_paul": "male",
    "kushal_tandon": "male",
    "rithvik": "male",
    "karan_johar": "male",
    "hussain_kuwajerwala": "male",
    "rajat_kapoor": "male",
    "ronit_roy": "male",
    "uday_chopra": "male",
    "sanam_puri": "male",
    "randeep_rai": "male",
    "shaheer_shaikh": "male",
    "honey_singh": "male",
    "mika_singh": "male",
    "kapil_sharma": "male",
    "krushna_abhishek": "male",
    "jassi_gill": "male",
    "rohit_shetty": "male",
    "terence_lewis": "male",
    "karan_kundra": "male",
    "anu_malik": "male",
    "abhishek_verma": "male",
    "aly_goni": "male",
    "neeraj_chopra": "male",
    "abhishek_malik": "male",
    "gaurav_wadhwa": "male",
    "neel_motwani": "male",
    "darshan_raval": "male",
    "sumedh_mudgalakr": "male",
    "tanmay_bhatt": "male",
    "gurnaam_bhullar": "male",
    "rahul_dravid": "male",
    "sikander_kher": "male",
    "remo_dsouza": "male",
    "dharmesh_yelande": "male",
    "raghav_juyal": "male",
    "ar_rahman": "male",
    "sunil_chetri": "male",
    "jaspreet_bhumra": "male",
    "zakhir_khan": "male",
    "aadar_poonawala": "male",
    "gautam_adani": "male",
    "manjot_singh": "male",
    "varun_sharma": "male",
    "pankaj_tripathi": "male",
    "mukesh_ambani": "male",
    "manoj_bajpayee": "male",
    "jitendra_kumar": "male",
    "divyenndu": "male",
    "diljit_dosangh": "male",
    "vikrant_massey": "male",
    "gagan_arora": "male",
    "kl_rahul": "male",
    "rohan_preet_singh": "male",
    "harsh_gujral": "male",
    "badshah": "male",
    "sachin_tendulkar": "male",
    "arijit_singh": "male",
    "guru_randhawa": "male",
    "armaan_malik": "male",
    "manoj_tiwari": "male",
    "neel_nitin_mukesh": "male",
    "kriti_sanon": "female",
    "deepika_padukon": "female",
    "kajol": "female",
    "tapsee": "female",
    "saiyami_kher": "female",
    "priyanka_chopra": "female",
    "aishwarya_rai_bachchan": "female",
    "preity_zinta": "female",
    "sanya_malhotra": "female",
    "kangana_ranaut": "female",
    "shraddha_kapoor": "female",
    "katrina_kaif": "female",
    "disha_patni": "female",
    "kiara_adwani": "female",
    "tamanna_bhatia": "female",
    "pooja_hegde": "female",
    "sonu_kakkar": "female",
    "chitrangada_singh": "female",
    "sayyesha_saigal": "female",
    "vaani_kapoor": "female",
    "jennifer_winget": "female",
    "kajal_aggarwal": "female",
    "anushka_sharma": "female",
    "sonakshi_sinha": "female",
    "rakul_preet_singh": "female",
    "sara_ali_khan": "female",
    "alia_bhatt": "female",
    "sonam_kapoor": "female",
    "huma_qureshi": "female",
    "shilpa_shetty": "female",
    "rani_mukherjee": "female",
    "sushmita_sen": "female",
    "ananya_pandey": "female",
    "anushka_shetty": "female",
    "rhea_chakraborty": "female",
    "asin": "female",
    "vidhya_balan": "female",
    "nayanthara": "female",
    "daisy_shah": "female",
    "janhvi_kapoor": "female",
    "geeta_kapoor": "female",
    "bharti_singh": "female",
    "nimrat_khair": "female",
    "farah_khan": "female",
    "kareena_kapoor": "female",
    "sania_mirza": "female",
    "sonam_bajwa": "female",
    "tabassum_fatima_hashmi": "female",
    "shehnaaz_gill": "female",
    "zareen_khan": "female",
    "malaika_arora": "female",
    "hina_khan": "female",
    "jacqueline_fernandez": "female",
    "samantha_ruth_prabhu": "female",
    "sanjana_sanjhi": "female",
    "parineeti_chopra": "female",
    "rekha": "female",
    "shruti_haasan": "female",
    "ileana_dcruz": "female",
    "neha_kakkar": "female",
    "mouni_roy": "female",
    "shakti_mohan": "female",
    "mukti_mohan": "female",
    "neeti_mohan": "female",
    "shraddha_kapoor": "female",
    "smriti_mandhana": "female",
    "athiya_shetty": "female",
    "tara_sutaria": "female",
    "saina_nehwal": "female",
    "neeta_ambani": "female",
    "shriya_pilgaonkar": "female",
    "pv_sindhu": "female",
    "indra_nooyi": "female",
    "mithali_raj": "female",
    "palak_muchhal": "female",
    "divyakhosla_kumar": "female",
    "shreya_ghosal": "female",
    "kritika_khurana": "female",
    "sargun_mehta": "female",
    "urvashi_rautela": "female",
    "bipasha_basu": "female",
    "mary_kom": "female",
    "harnaaz_kaur_sandhu": "female",
    "namita_thappar": "female",
    "madhuri_dixit": "female",
    "vineeta_singh": "female",
    "ghazal_alagh": "female",
    "vaibhavi": "female",
    "karishma_tanna": "female",
    "amrita_singh" : "female",
    "aahana_kumra" : "female",
    "aamna_sharif" : "female",
    "adah_sharma" : "female",
    "aditi_govitrikar" : "female",
    "aditi_rao_hydari" : "female",
    "ahsaas_channa" : "female",
    "alaya_f" : "female",
    "ameesha_patel" : "female",
    "amrita_arora" : "female",
    "amrita_prakash" : "female",
    "amrita_puri" : "female",
    "amrita_raichand" : "female",
    "amruta_subhash" : "female",
    "angira_dhar" : "female",
    "anita_hassanandani" : "female",
    "anjana_sukhani" : "female",
    "anju_mahendru" : "female",
    "ankita_lokhande" : "female",
    "anupriya_goenka" : "female",
    "anusha_dandekar" : "female",
    "anushka_ranjan" : "female",
    "aruna_irani" : "female",
    "ashnoor_kaur" : "female",
    "ayesha_takia" : "female",
    "barkha_singh" : "female",
    "bhumi_pednekar" : "female",
    "chahatt_khanna" : "female",
    "deepti_naval" : "female",
    "delnaaz_irani" : "female",
    "dia_mirza" : "female",
    "diana_penty" : "female",
    "digangana_suryavanshi" : "female",
    "disha_parmar" : "female",
    "disha_vakani" : "female",
    "divya_dutta" : "female",
    "divyanka_tripathi" : "female",
    "drashti_dhami" : "female",
    "elli_avram" : "female",
    "esha_deol" : "female",
    "esha_gupta" : "female",
    "evelyn_sharma" : "female",
    "farida_jalal" : "female",
    "fatima_sana_shaikh" : "female",
    "freida_pinto" : "female",
    "gauahar_khan" : "female",
    "genelia_d_souza" : "female",
    "hazel_keech" : "female",
    "hema_malini" : "female",
    "ishita_dutta" : "female",
    "jasmin_bhasin" : "female",
    "jaya_bachchan" : "female",
    "jayaprada" : "female",
    "juhi_chawla" : "female",
    "kalki_koechlin" : "female",
    "kashmera_shah" : "female",
    "kirron_kher" : "female",
    "kirti_kulhari" : "female",
    "konkona_sen_sharma" : "female",
    "kriti_kharbanda" : "female",
    "lara_dutta" : "female",
    "lauren_gottlieb" : "female",
    "lisa_haydon" : "female",
    "mahira_khan" : "female",
    "mallika_sherawat" : "female",
    "mandira_bedi" : "female",
    "manisha_koirala" : "female",
    "mini_mathur" : "female",
    "mithila_palkar" : "female",
    "mona_singh" : "female",
    "monali_thakur" : "female",
    "munmun_dutta" : "female",
    "nauheed_cyrusi" : "female",
    "neena_gupta" : "female",
    "neetu_singh" : "female",
    "neha_sharma" : "female",
    "nora_fatehi" : "female",
    "nushrratt_bharuccha" : "female",
    "parul_gulati" : "female",
    "pooja_bedi" : "female",
    "pooja_bhatt" : "female",
    "prachi_desai" : "female",
    "radhika_apte" : "female",
    "radhika_madan" : "female",
    "ragini_khanna" : "female",
    "rashami_desai" : "female",
    "ratna_pathak_shah" : "female",
    "raveena_tandon" : "female",
    "diljit_dosanjh": "male",
    "akshaye_khanna": "male",
    "ali_zafar": "male",
    "amrish_puri": "male",
    "angad_bedi": "male",
    "arbaaz_khan": "male",
    "arshad_warsi": "male",
    "ashutosh_rana": "male",
    "cyrus_sahukar": "male",
    "darsheel_safary": "male",
    "dev_anand": "male",
    "dhanush": "male",
    "dulquer_salmaan": "male",
    "harshvardhan_kapoor": "male",
    "kamal_hasan": "male",
    "karan_wahi": "male",
    "kartik_aaryan": "male",
    "kunal_kapoor": "male",
    "milind_soman": "male",
    "mohanlal": "male",
    "paresh_rawal": "male",
    "rahul_bose": "male",
    "rajinikanth": "male",
    "ranbir_kapoor": "male",
    "saquib_saleem": "male",
    "sharman_joshi": "male",
    "shatrughan_sinha": "male",
    "sidharth_malhotra": "male",
    "sonu_sood": "male",
    "varun_dhawan": "male",
}

def download_image(path, url):
    base_path = os.getenv("BASE_PATH")
    file_path = base_path + path + ".jpg"
    r = download(url)
    if r:
        open(file_path, 'wb').write(r.content)

    return

def download(image_url):
    # print("############################.", image_url, "#######################")
    try:
        response = requests.get(image_url, stream=True)
        return response
    except ConnectionError as e:
        return None

def read_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            download_image(row['name'], row['image_url'])
            print(row['sr_no'], row['name'], row['image_url'])

def s3_image_upload(file_path, region=None, bucket_name="new-test-bkt-1"):
    object_name = file_path.split("/")[-1]
    print(object_name)
    
    base_path = os.getenv("BASE_PATH")
    file_path = base_path + file_path

    start_time = time.time()
    s3_client = create_boto_client_s3()

    im = Image.open(file_path)
    width, height = im.size
    im = im.convert('RGB')
    im = im.resize((640, int(height*640/width)))
    im.save(file_path)
    
    start_time_2 = time.time()
    print("resize and opening time: ", start_time_2-start_time)

    try:
        response = s3_client.upload_file(file_path, bucket_name, object_name)
    except ClientError as e:
        print(e)
        return
    start_time_3 = time.time()
    print("upload time: ", start_time_3-start_time_2)

    return

def create_boto_client_s3():
    region = os.getenv("AWS_REGION")
    s3_client = boto3.client('s3', region_name=region)

    return s3_client

def aws_index_image(object_name, region=None, bucket_name="new-test-bkt-1"):
    name_celeb = object_name.split(".")[0]
    gender = celebrity_gender_map.get(name_celeb, "")
    if gender == "female":
        collection_id = "celeb_female_ffi"
    else:
        collection_id = "celeb_male_ffi"

    print(name_celeb, gender, collection_id)
    client = create_boto_client_aws()
    try:
        response = client.index_faces(
            CollectionId=collection_id,
            Image={'S3Object':{'Bucket':bucket_name,'Name':object_name}},
            ExternalImageId=object_name,
            MaxFaces=1,
            QualityFilter="AUTO",
            DetectionAttributes=['ALL']
        )
    except ClientError as e:
        print(e)
        return False
    return True

def create_boto_client_aws():
    my_config = Config(
        region_name = 'us-west-2',
        signature_version = 'v4',
        retries = {
            'max_attempts': 10,
            'mode': 'standard'
        }
    )
    client = boto3.client('rekognition', config=my_config)

    return client

def create_collection(collection_id):

    # client=boto3.client('rekognition')
    client = create_boto_client_aws()
    #Create a collection
    print('Creating collection:' + collection_id)
    response=client.create_collection(CollectionId=collection_id)
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code: ' + str(response['StatusCode']))
    print('Done...')

if __name__ == '__main__':
    # read_csv('male.csv')

    base_path = os.getenv("BASE_PATH")
    for file in os.listdir(base_path):
     filename = os.fsdecode(file)
     if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"): 
         s3_image_upload(filename)
         aws_index_image(filename)
         continue
     else:
         continue