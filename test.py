import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from mmdet.apis import inference_detector, init_detector

import os

# ... [Other parts of your script] ...
classes = ['0_Bulls Eye', '11_1', '12_2', '13_3', '14_4', '15_5', '16_6', '17_7',
            '18_8', '19_9', '20_A', '21_B', '22_C', '23_D', '24_E', '25_F', '26_G',
            '27_H', '28_S', '29_T', '30_U', '31_V', '32_W', '33_X', '34_Y', '35_Z',
            '36_Up', '37_Down', '38_Right', '39_Left', 'Stop']


class Watcher:
    def __init__(self, directory_to_watch, k, callback):
        self.DIRECTORY_TO_WATCH = directory_to_watch
        self.k = k
        self.callback = callback
        self.photos = []
        self.observer = Observer()

    def run(self):
        event_handler = Handler(self)
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()

class Handler(FileSystemEventHandler):
    # ... [Rest of the Handler class] ...
    def __init__(self, watcher):
        self.watcher = watcher

        # init model
        config = './configs/mdp/mdpv30.py'
        # Setup a checkpoint file to load
        checkpoint = './work_dirs/mdpv8_grp30_continue/epoch_50.pth'
        # initialize the detector
        self.model = init_detector(config, checkpoint, device='cpu')

    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print(f"Received created event - {event.src_path}.")
            self.handle_new_photo(event.src_path)

    def handle_new_photo(self, path):
        if path.endswith(".jpg") or path.endswith(".png"):  # check for specific file types
            self.watcher.photos.append(path)
            print(f"Photo added: {path}")

            if len(self.watcher.photos) >= self.watcher.k:
                self.perform_function()
                self.watcher.photos = []  # Reset the photo list

    def perform_function(self):
        print("Detection Start!")
        results = inference_detector(self.model, self.watcher.photos)
        self.watcher.callback(results)  # Call the callback with the results

def process_results(results):
    # Define how to process the results here
    # print("Processing results...")
    # print(results)
    if results[0].pred_instances.labels.nelement() > 0:
        print(f"Find Sign {classes[results[0].pred_instances.labels[0]+1]}")
        # detected!
    else:
        print("Nothing found!")
        # nothing!
    
    # detected = classes[results[0].pred_instances.labels[0] + 1] == '40_Stop'
    arg = 'ssh MDP \'bash -c \"sudo su; echo -n \'F100 \' > /dev/ttyUSB0\"\''
    print(arg)
    os.system(arg)
    

if __name__ == '__main__':
    w = Watcher("/Volumes/admin/Desktop/shared", k=1, callback=process_results)
    w.run()
