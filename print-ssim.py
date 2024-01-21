from skimage.metrics import structural_similarity as compare_ssim
import cv2

# Assuming 'image1' and 'image2' are your images in OpenCV format
image1 = cv2.imread('reference/pridesticker.png')
image2 = cv2.imread('/Users/j/Library/Application Support/AetherSX2/textures/SLUS-21214/dumps/7e6ae4579bda66e9-b395a2462d00703b-00005554.png')

# Convert images to grayscale for SSIM comparison
gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

# Compute SSIM
ssim, _ = compare_ssim(gray_image1, gray_image2, full=True)

print(f"The Structural Similarity Index (SSIM) value is: {ssim:.4f}")

# Adjust the threshold as needed for your images
if ssim >= 0.93:  # Example threshold: SSIM value close to 1 indicates similarity
    print("The images are similar in color.")
else:
    print("The images differ significantly in color.")
