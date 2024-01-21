from PIL import Image
import imagehash

# Load the image
image_path = "/Users/j/Library/Application Support/AetherSX2/textures/SLUS-21214/dumps/7e6ae4579bda66e9-b395a2462d00703b-00005554.png"
# image_path = "/Users/j/Library/Application Support/AetherSX2/textures/SLUS-21214/dumps/faf01b33cbdc0f1a-c701ccdd92cb19f8-00005993.png"
image = Image.open(image_path)

# Calculate the hash
hash_phash = imagehash.phash(image)
hash_dhash = imagehash.dhash(image)
hash_average = imagehash.average_hash(image)

# Print the hashes
print("Perceptual Hash (phash):", hash_phash)
print("Difference Hash (dhash):", hash_dhash)
print("Average Hash:", hash_average)