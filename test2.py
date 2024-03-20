import os
import time
from mmdet.apis import inference_detector, init_detector

classes = ['0_Bulls Eye', '11_1', '12_2', '13_3', '14_4', '15_5', '16_6', '17_7',
            '18_8', '19_9', '20_A', '21_B', '22_C', '23_D', '24_E', '25_F', '26_G',
            '27_H', '28_S', '29_T', '30_U', '31_V', '32_W', '33_X', '34_Y', '35_Z',
            '36_Up', '37_Down', '38_Right', '39_Left', 'Stop']

def process_image(image_path):
    # Your custom function to process the right image
    result = inference_detector(model, image_path)
    is_right_image = result.pred_instances.labels.nelement() > 0
    if is_right_image:
        return classes[result.pred_instances.labels[0]], result.pred_instances.bboxes[0] 
    else:
        return None
    


folder_path = "//192.168.30.1/admin/Desktop/shared/img"
shared_folder = "//192.168.30.1/admin/Desktop/shared"
file_prefix = "img"
file_extension = ".jpg"
current_index = 1
bullseyeIndex = 0

config = './configs/mdp/mdpv30.py'
# Setup a checkpoint file to load
checkpoint = './work_dirs/mdpv30/epoch_300.pth'
# initialize the detector
model = init_detector(config, checkpoint, device='cpu')



# while True:
#     # Construct the expected file name
#     file_name = f"{file_prefix}{current_index}{file_extension}"
#     file_path = os.path.join(folder_path, file_name)

#     # Check if the file exists
#     if os.path.exists(file_path):


#         print(f"Found new image: {file_name}")

#         # Check if it's the right image
#         while True: 
#             try:
#                 detected = process_image(file_path)
#                 break
#             except Exception as e:
#                 print(f"Failed to process, taking another picture")
#                 print(e)

#                 time.sleep(0.2)
#                 open(f'{shared_folder}/poll/continue.txt','x')
#                 current_index += 1
#                 file_name = f"{file_prefix}{current_index}{file_extension}"
#                 file_path = os.path.join(folder_path, file_name)
#                 continue
            
#         if detected is not None:
#             print(f"Detected {detected}!")
#             current_index+=1
#             arg = 'ssh admin@192.168.30.1 "echo -n sssss > /dev/ttyUSB0"'
#             if detected == classes[0]:
#                 arg = 'ssh admin@192.168.30.1 "echo -n b30.0l90.0f20.0r180. > /dev/ttyUSB0"'
#                 if(bullseyeIndex < 1):
#                     arg = 'ssh admin@192.168.30.1 "echo -n f20.0 > /dev/ttyUSB0"'
#                 bullseyeIndex+=1
#                 os.system(arg)
#                 time.sleep(10)
#                 open(f'{shared_folder}/poll/continue.txt','x')

#             #arg = 'ssh admin@192.168.30.1 "echo -n sssss > /dev/ttyUSB0"'
#             else:
#                 break
                
#             #os.system(arg)
#             #break  # or continue, depending on your use case
#         else:
#             print("Nothing detected!")
#             # scan around obstacle
#             arg = 'ssh admin@192.168.30.1 "echo -n b30.0l90.0f20.0r180. > /dev/ttyUSB0"'
#             if(current_index==1):
#                 arg = 'ssh admin@192.168.30.1 "echo -n f10.0 > /dev/ttyUSB0"'
#                 os.system(arg)
#                 time.sleep(5)
#                 open(f'{shared_folder}/poll/continue.txt','x')
#                 current_index += 1
#                 continue
            
#             os.system(arg)
#             # ask for the next image!
#             time.sleep(10)

#             open(f'{shared_folder}/poll/continue.txt','x')


#             # while not detected
#             # l90.0
#             # r190.0
#             # Increment index for next image
#             current_index += 1
#             print(f"current index = {current_index}")
#     else:
#         print(f"Waiting for image: {file_name}")

#     # Wait for a short period before checking again
#     time.sleep(2)  # Adjust the sleep duration as needed
