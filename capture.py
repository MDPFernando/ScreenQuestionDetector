import mss
import mss.tools

def capture_screen_center(output_filename="test.png"):
    with mss.mss() as sct:
        # Get information of primary monitor
        monitor = sct.monitors[1]
        
        # Calculate center 500x500 region
        width, height = 500, 500
        left = monitor["left"] + (monitor["width"] - width) // 2
        top = monitor["top"] + (monitor["height"] - height) // 2
        
        # Define the bounding box
        bbox = {"top": int(top), "left": int(left), "width": width, "height": height}
        
        # Grab the data
        sct_img = sct.grab(bbox)
        
        # Save to a file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_filename)
        print(f"Successfully captured screen region and saved to {output_filename}")
        return output_filename

if __name__ == "__main__":
    capture_screen_center()
