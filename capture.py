import mss
import mss.tools

def capture_window(bbox, output_filename="test.png"):
    """
    Captures a specific region of the screen defined by bbox.
    bbox should be a dictionary: {"top": y, "left": x, "width": w, "height": h}
    """
    with mss.MSS() as sct:
        try:
            # Grab the data using the provided bounding box
            sct_img = sct.grab(bbox)
            
            # Save to a file
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_filename)
            print(f"Successfully captured window region and saved to {output_filename}")
            return output_filename
        except Exception as e:
            print(f"Error capturing window: {e}")
            return None

if __name__ == "__main__":
    # Test fallback: capture a 500x500 box at the top left of the primary monitor
    try:
        with mss.MSS() as sct:
            monitor = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
            test_bbox = {"top": monitor["top"], "left": monitor["left"], "width": 500, "height": 500}
            capture_window(test_bbox)
    except Exception as e:
        print(f"Error in test capture: {e}")
