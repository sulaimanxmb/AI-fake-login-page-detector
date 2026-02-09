from model.train_model import build_feature_dataset, train_model

if __name__ == "__main__":
    print("--- Starting Training Pipeline ---")
    
    # 1. Build features from raw URLs
    print("1. Extracting features from URLs...")
    build_feature_dataset()
    
    # 2. Train the model
    print("\n2. Training the model...")
    train_model()
    
    print("\n--- Pipeline Complete ---")