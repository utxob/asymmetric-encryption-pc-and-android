from Crypto.PublicKey import RSA

# Function to generate RSA public and private keys
def generate_rsa_keys():
    # Generate a new RSA key pair (2048-bit)
    key = RSA.generate(2048)
    
    # Export the private key in PEM format
    private_key = key.export_key()
    with open("private.pem", "wb") as private_file:
        private_file.write(private_key)
    
    # Export the public key in PEM format
    public_key = key.publickey().export_key()
    with open("public.pem", "wb") as public_file:
        public_file.write(public_key)
    
    print("RSA keys have been generated and saved as public.pem and private.pem")

# Generate the RSA keys
generate_rsa_keys()
