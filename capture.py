import mss
from PIL import Image

def capture_window(bbox, output_filename="test.jpg"):
    with mss.mss() as sct:
        try:
            sct_img = sct.grab(bbox)
            # Convert raw bytes to PIL Image (C-optimized, extremely fast)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            
            # Downscale massive screens to save network upload time (1200px max)
            max_dim = 1600
            if img.width > max_dim or img.height > max_dim:
                img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
                
            # Save as optimized JPEG to slash file size from ~10MB down to ~150KB
            img.save(output_filename, format="JPEG", quality=80, optimize=True)
            return output_filename
        except Exception as e:
            print(f"Capture error: {e}")
            return None

if __name__ == "__main__":
    # Test fallback: capture a 500x500 box at the top left of the primary monitor
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
            test_bbox = {"top": monitor["top"], "left": monitor["left"], "width": 500, "height": 500}
            capture_window(test_bbox)
    except Exception as e:
        print(f"Error in test capture: {e}")
