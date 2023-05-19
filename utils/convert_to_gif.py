import cv2
import imageio
 
def convert_to_gif(name, data_loaded):
    cap = cv2.VideoCapture(name)
    image_lst = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_lst.append(frame_rgb)
        
        cv2.imshow('a', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    
    # Convert to gif using the imageio.mimsave method
    path = 'github_viz/' + data_loaded['video']['output_name'][:-4] + '.gif'
    imageio.mimsave(path, image_lst, loop=0)